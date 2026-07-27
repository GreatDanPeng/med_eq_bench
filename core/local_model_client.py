"""
Local (in-process) HuggingFace inference, wrapped to look like an OpenAI
client -- see core.model_client.client_for_model(). Every other module calls
`client.chat.completions.create(model=..., messages=..., tools=..., ...)`
and reads `resp.choices[0].message`; this module reproduces that exact
shape so core/multi_agent_system.py and core/model_client.py need no
awareness that the model is running on this machine instead of behind an
HTTP API.

Routed to for labels in config.models.LOCAL_HF_MODELS (see
LOCAL_HF_MODEL_IDS for the label -> HuggingFace repo id mapping) -- currently
just medgemma-1.5-4b ("google/medgemma-1.5-4b-it"), a gated model: the
HuggingFace account used for HF_TOKEN must have accepted the license at
https://huggingface.co/google/medgemma-1.5-4b-it before the first download.

Tool calling: transformers' plain .generate() has no OpenAI-style `tools`
parameter, so tool schemas are folded into the system prompt as a JSON-call
instruction block (see _tool_instructions), and the model's raw text output
is parsed for that JSON (see _extract_tool_call_json). A successful parse is
converted into the same `tool_calls` wire shape OpenAI returns, so
core.model_client._normalize_tool_calls's real-tool_calls path handles it
without any change -- this module never needs the text-tool-call fallback
that exists there for other providers.

Model/tokenizer are loaded once per process and cached (see _get_model) --
reloading a multi-GB model on every turn would make a full scenario run
impractically slow.
"""

from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

# Label (config.models.PHYSICIAN_MODELS key / value) -> HuggingFace repo id.
# A label only needs an entry here AND in config.models.LOCAL_HF_MODELS for
# client_for_model() to route it through this module instead of OpenRouter.
LOCAL_HF_MODEL_IDS = {
    "medgemma-1.5-4b": "google/medgemma-1.5-4b-it",
}

_DEFAULT_DEVICE = "mps"  # falls back to "cpu" in _get_model if unavailable

# Process-wide cache: repo_id -> (model, processor). Loaded lazily on first
# use so importing this module never triggers a multi-GB download/load.
_MODEL_CACHE: dict[str, tuple[Any, Any]] = {}


def _get_model(repo_id: str) -> tuple[Any, Any]:
    if repo_id in _MODEL_CACHE:
        return _MODEL_CACHE[repo_id]

    import torch
    from transformers import AutoModelForImageTextToText, AutoProcessor

    device = _DEFAULT_DEVICE if torch.backends.mps.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "mps" else torch.float32

    print(f"[local_model_client] Loading {repo_id} on {device} (dtype={dtype})... "
         f"first load downloads weights and may take a while.")
    processor = AutoProcessor.from_pretrained(repo_id)
    model = AutoModelForImageTextToText.from_pretrained(repo_id, dtype=dtype)
    model.to(device)
    model.eval()
    print(f"[local_model_client] {repo_id} loaded.")

    _MODEL_CACHE[repo_id] = (model, processor)
    return model, processor


# ---------------------------------------------------------------------------
# Prompt-based tool calling
# ---------------------------------------------------------------------------

_TOOL_CALL_INSTRUCTIONS_TEMPLATE = """\

TOOL USE
You have the following tools available. To call one, respond with ONLY a
single JSON object on its own -- no other text before or after it -- in
exactly this shape:
{{"tool_call": {{"name": "<tool name>", "arguments": {{...}}}}}}

If you are not calling a tool, just respond normally in plain text (no JSON).
Never call more than one tool per turn.

Available tools:
{tool_descriptions}
"""


def _describe_tool(schema: dict[str, Any]) -> str:
    fn = schema["function"]
    params = fn.get("parameters", {}).get("properties", {})
    required = set(fn.get("parameters", {}).get("required", []))
    arg_lines = "\n".join(
        f"    - {name}{' (required)' if name in required else ''}: {info.get('description', '')}"
        for name, info in params.items()
    )
    return f"- {fn['name']}: {fn['description']}\n{arg_lines}"


def _tool_instructions(tools: list[dict[str, Any]]) -> str:
    tool_descriptions = "\n".join(_describe_tool(t) for t in tools)
    return _TOOL_CALL_INSTRUCTIONS_TEMPLATE.format(tool_descriptions=tool_descriptions)


# Matches a ```json ... ``` fence, or a bare {...} JSON object.
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)
_BARE_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_tool_call_json(text: str) -> Optional[dict[str, Any]]:
    """Return {"name", "arguments"} if `text` contains a {"tool_call": {...}}
    JSON object (see _TOOL_CALL_INSTRUCTIONS_TEMPLATE), else None."""
    if not text or "{" not in text:
        return None

    candidates = [m.strip() for m in _JSON_FENCE_RE.findall(text)]
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        candidates.append(stripped)
    bare_match = _BARE_JSON_RE.search(text)
    if bare_match:
        candidates.append(bare_match.group(0))

    for candidate in candidates:
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        call = obj.get("tool_call") if isinstance(obj, dict) else None
        if isinstance(call, dict) and "name" in call:
            return {"name": call["name"], "arguments": call.get("arguments") or {}}
    return None


# ---------------------------------------------------------------------------
# OpenAI-response-shaped wrapper objects
# ---------------------------------------------------------------------------
# Mirrors just the attributes core.model_client.call_model() reads off an
# OpenAI ChatCompletion: resp.choices[0].message.{content,tool_calls},
# resp.choices[0].finish_reason. Plain dataclasses, not the real SDK types --
# nothing else in the pipeline constructs or isinstance-checks these.

@dataclass
class _ToolCallFunction:
    name: str
    arguments: str  # JSON string, matching the real SDK's wire shape


@dataclass
class _ToolCall:
    id: str
    function: _ToolCallFunction
    type: str = "function"


@dataclass
class _Message:
    content: Optional[str]
    tool_calls: list[_ToolCall] = field(default_factory=list)
    reasoning_details: Any = None


@dataclass
class _Choice:
    message: _Message
    finish_reason: Optional[str] = None


@dataclass
class _ChatCompletion:
    choices: list[_Choice]


class _ChatCompletions:
    def __init__(self, repo_id: str):
        self._repo_id = repo_id

    def create(self, model: str, messages: list[dict[str, Any]],
               temperature: float = 0.7, max_tokens: int = 1024,
               tools: Optional[list[dict[str, Any]]] = None,
               tool_choice: str | dict = "auto",
               extra_body: Optional[dict[str, Any]] = None,
               **_ignored: Any) -> _ChatCompletion:
        model_obj, processor = _get_model(self._repo_id)
        prompt_messages = _prepare_messages(messages, tools)
        text = _generate(model_obj, processor, prompt_messages, temperature, max_tokens)

        tool_calls: list[_ToolCall] = []
        content: Optional[str] = text
        if tools:
            parsed = _extract_tool_call_json(text)
            if parsed is not None:
                tool_calls = [_ToolCall(
                    id=f"local-tool-{uuid.uuid4().hex[:8]}",
                    function=_ToolCallFunction(
                        name=parsed["name"],
                        arguments=json.dumps(parsed["arguments"]),
                    ),
                )]
                content = None  # matches OpenAI: content is null on a tool-call turn

        finish_reason = "tool_calls" if tool_calls else "stop"
        message = _Message(content=content, tool_calls=tool_calls)
        return _ChatCompletion(choices=[_Choice(message=message, finish_reason=finish_reason)])


class LocalHFClient:
    """Drop-in stand-in for `openai.OpenAI` backed by an in-process
    HuggingFace model. Only the `.chat.completions.create(...)` surface used
    by core.model_client.call_model() is implemented."""

    def __init__(self, repo_id: str):
        self.chat = _ChatCompletionsNamespace(repo_id)


class _ChatCompletionsNamespace:
    def __init__(self, repo_id: str):
        self.completions = _ChatCompletions(repo_id)


def make_local_client(model_label: str) -> LocalHFClient:
    """LocalHFClient for a label in config.models.LOCAL_HF_MODELS."""
    repo_id = LOCAL_HF_MODEL_IDS.get(model_label)
    if repo_id is None:
        raise RuntimeError(
            f"No local HF repo id registered for {model_label!r}. Add it to "
            f"core.local_model_client.LOCAL_HF_MODEL_IDS.")
    return LocalHFClient(repo_id)


# ---------------------------------------------------------------------------
# Message prep + generation
# ---------------------------------------------------------------------------

def _prepare_messages(messages: list[dict[str, Any]],
                      tools: Optional[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Fold tool schemas into the system message (see _tool_instructions) and
    flatten any OpenAI-wire-format tool_calls/tool-role messages from prior
    turns into plain text the chat template understands -- the chat template
    only knows "system"/"user"/"assistant" roles, not OpenAI's "tool" role
    or assistant.tool_calls."""
    prepared: list[dict[str, Any]] = []
    for msg in messages:
        role = msg["role"]
        if role == "tool":
            # Feed the tool's JSON result back as a user-role observation --
            # there's no "tool" role in this model's chat template.
            prepared.append({"role": "user",
                            "content": f"[Tool result] {msg['content']}"})
            continue

        content = msg.get("content") or ""
        if role == "assistant" and msg.get("tool_calls"):
            # Re-render the prior tool call as the same JSON text the model
            # originally produced, so the transcript stays self-consistent.
            tc = msg["tool_calls"][0]
            call_json = json.dumps({"tool_call": {
                "name": tc["function"]["name"],
                "arguments": json.loads(tc["function"]["arguments"] or "{}"),
            }})
            content = call_json
        prepared.append({"role": role, "content": content})

    if tools:
        instructions = _tool_instructions(tools)
        if prepared and prepared[0]["role"] == "system":
            prepared[0] = {"role": "system",
                          "content": prepared[0]["content"] + "\n" + instructions}
        else:
            prepared.insert(0, {"role": "system", "content": instructions.strip()})

    return prepared


def _generate(model: Any, processor: Any, messages: list[dict[str, Any]],
             temperature: float, max_tokens: int) -> str:
    import torch

    inputs = processor.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True,
        return_dict=True, return_tensors="pt",
    ).to(model.device)

    do_sample = temperature > 0
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=do_sample,
            temperature=temperature if do_sample else None,
        )

    new_tokens = output[0][inputs["input_ids"].shape[-1]:]
    text = processor.decode(new_tokens, skip_special_tokens=True)
    return text.strip()


if __name__ == "__main__":
    client = make_local_client("medgemma-1.5-4b")
    resp = client.chat.completions.create(
        model="medgemma-1.5-4b",
        messages=[{"role": "user", "content": "In one sentence, what is hypertension?"}],
        max_tokens=100,
    )
    print(resp.choices[0].message.content)

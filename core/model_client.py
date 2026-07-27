"""
Unified model client for the clinical-agent sycophancy benchmark.
==================================================================

Every model is called through the same OpenAI-compatible adapter (same
message plumbing, same tool protocol) so cross-model comparison stays fair --
only the `model` string and which client/platform it's routed through differ.
Most models go through OpenRouter (make_client); a small set of
medical-specialty models (config.models.MEDICAL_PLATFORM_MODELS, e.g.
medgemma-4b-it) go through a separate endpoint at dr7.ai instead
(make_dr7_client). client_for_model(model) picks the right one.

Two call styles are supported:
  - chat():  a plain conversational turn (patient replies; physician questions).
  - act():   a physician turn that may emit tool calls (function calling).

Reasoning is preserved across turns using OpenRouter's `reasoning_details`
pass-back pattern (see call_model / append_assistant_turn), so a model that
"thinks" continues from where it left off instead of restarting each turn.

Set OPENROUTER_API_KEY (OpenRouter) and/or DR7_KEY (dr7.ai) in the
environment before running.
"""

from __future__ import annotations

import os
import json
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)

from config.tool_schemas import TOOL_NAMES

# Transient failures worth a short retry: the response body got cut off
# mid-stream (raw json.JSONDecodeError, not wrapped by the SDK) or the
# provider had a connection/timeout/rate-limit/5xx hiccup. Anything else
# (bad request, auth, etc.) is a real error and should propagate immediately.
_TRANSIENT_ERRORS = (json.JSONDecodeError, APIConnectionError, APITimeoutError,
                    InternalServerError, RateLimitError)


# ---------------------------------------------------------------------------
# Model config
# ---------------------------------------------------------------------------
# Which models participate in a run lives in config/models.py -- this module
# only knows how to call whatever model string it's given.

@dataclass
class ModelConfig:
    """Per-model generation settings. Extend as more models are added."""
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024
    # Enable OpenRouter reasoning for models that support it. Harmless to leave
    # on; providers that don't support it ignore the field.
    reasoning: bool = True

    def extra_body(self) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if self.reasoning:
            body["reasoning"] = {"enabled": True}
        return body


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

def make_client(api_key: Optional[str] = None) -> OpenAI:
    """One OpenAI-compatible client pointed at OpenRouter."""
    key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        # Some setups store one or more comma-separated keys under
        # OPENROUTER_KEYS instead of OPENROUTER_API_KEY.
        keys = os.environ.get("OPENROUTER_KEYS", "")
        key = keys.split(",")[0].strip() if keys.strip() else None
    if not key:
        raise RuntimeError(
            "Set OPENROUTER_API_KEY or OPENROUTER_KEYS (or pass api_key=...)."
        )
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)


def make_dr7_client(api_key: Optional[str] = None) -> OpenAI:
    """Client for the dr7.ai medical-model platform (e.g. medgemma-4b-it) --
    a separate OpenAI-compatible endpoint outside OpenRouter, auth'd via
    DR7_KEY. Reuses the same openai SDK since dr7.ai's request shape
    (model/messages/max_tokens/temperature posted to .../chat/completions)
    matches the OpenAI convention; base_url points at the "medical" path so
    the SDK's implicit "/chat/completions" suffix lands on
    https://dr7.ai/api/v1/medical/chat/completions.
    """
    key = api_key or os.environ.get("DR7_KEY")
    if not key:
        raise RuntimeError("Set DR7_KEY (or pass api_key=...) for dr7.ai medical models.")
    return OpenAI(base_url="https://dr7.ai/api/v1/medical", api_key=key)


def client_for_model(model: str, api_key: Optional[str] = None) -> OpenAI:
    """Picks the right OpenAI-compatible client for `model`: a local
    in-process HuggingFace model for config.models.LOCAL_HF_MODELS (no
    network call -- see core.local_model_client), dr7.ai for medical-platform
    models (config.models.MEDICAL_PLATFORM_MODELS), OpenRouter for
    everything else.

    NOTE: `model` here is the PHYSICIAN_MODELS *label* for local models
    (e.g. "medgemma-1.5-4b"), not an OpenRouter slug -- run_encounter passes
    PHYSICIAN_MODELS[label] as `model` to both client_for_model() and the
    ModelConfig, and for local models that value IS the label (see
    config/models.py)."""
    from config.models import LOCAL_HF_MODELS, MEDICAL_PLATFORM_MODELS
    if model in LOCAL_HF_MODELS:
        from core.local_model_client import make_local_client
        return make_local_client(model)
    if model in MEDICAL_PLATFORM_MODELS:
        return make_dr7_client(api_key=api_key)
    return make_client(api_key=api_key)


# Some models (observed: medgemma-4b-it via dr7.ai) don't use the OpenAI
# `tool_calls` field at all -- they emit their "tool call" as text in the
# message content instead, and inconsistently so (the SAME model has been
# observed using two different styles across runs). Left unrecognized, the
# harness treats that text as an ordinary chat message, forwards it to the
# patient, and the encounter never actually closes (the model *thinks* it
# called end_encounter; the harness never saw a real tool call) -- it just
# loops on "goodbye" pleasantries until the circuit breaker or max_turns.
# _extract_text_tool_call tries each known style in turn.

# Style 1 (Gemma-ish): {"tool_code": "<name>", "parameters": {...}}, often
# inside a ```json fence. Captures everything between the fence delimiters,
# not by brace-matching -- the payload commonly has nested objects (e.g.
# "parameters": {...}), which a brace-counting regex can't handle correctly.
# json.loads() below does the actual (nesting-safe) parsing/validation.
_JSON_FENCE_RE = re.compile(r"```(?:json)?(.*?)```", re.DOTALL)


def _extract_json_fence_tool_call(content: str) -> Optional[dict[str, Any]]:
    candidates = [c.strip() for c in _JSON_FENCE_RE.findall(content)]
    stripped = content.strip()
    if not candidates and stripped.startswith("{") and stripped.endswith("}"):
        candidates = [stripped]
    for candidate in candidates:
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "tool_code" in obj:
            return {"name": obj["tool_code"], "arguments": obj.get("parameters") or {}}
    return None


# Style 2 (bare inline call): `end_encounter(summary: some text, more text)`,
# optionally preceded by ordinary prose, always at the end of the message.
# Anchored on a real, known tool name so it can't misfire on ordinary prose.
# Splits args on commas only when what follows looks like the start of a new
# `key:` pair -- so a comma inside a natural-language value (e.g. "mild,
# dull, band-like headaches") does not get mistaken for an argument boundary.
_INLINE_CALL_RE = re.compile(
    r"\b(" + "|".join(re.escape(n) for n in TOOL_NAMES) + r")\s*\((.*)\)\s*$",
    re.DOTALL,
)
_KWARG_SPLIT_RE = re.compile(r",\s*(?=[a-zA-Z_]\w*\s*:)")
_KWARG_RE = re.compile(r"^\s*([a-zA-Z_]\w*)\s*:\s*(.*)$", re.DOTALL)


def _strip_matching_quotes(value: str) -> str:
    """Some models write their inline-call values pre-quoted, e.g.
    `request: "head CT scan"` -- drop one matching pair of quotes so the
    recorded argument doesn't carry them as literal characters."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].strip()
    return value


def _extract_inline_call_tool_call(content: str) -> Optional[dict[str, Any]]:
    match = _INLINE_CALL_RE.search(content.strip())
    if not match:
        return None
    name, args_str = match.group(1), match.group(2)
    arguments: dict[str, Any] = {}
    for segment in _KWARG_SPLIT_RE.split(args_str):
        kwarg = _KWARG_RE.match(segment)
        if kwarg:
            arguments[kwarg.group(1)] = _strip_matching_quotes(kwarg.group(2).strip())
    return {"name": name, "arguments": arguments}


def _extract_text_tool_call(content: Optional[str]) -> Optional[dict[str, Any]]:
    """Return {"name", "arguments"} if `content` contains a recognizable
    text-embedded tool call in any known style, else None."""
    if not content:
        return None
    return (_extract_json_fence_tool_call(content)
            or _extract_inline_call_tool_call(content))


# Some backends (observed: dr7.ai) occasionally return a generic error string
# as `content` instead of a real error/exception -- e.g. when the request
# shape (tools/tool_choice) isn't fully supported for that call. It isn't
# blank, so it slips past the empty-response guard in
# _handle_plain_message_turn and gets forwarded to the patient as if it were
# a genuine physician utterance. Treat it like an empty/truncated turn
# instead (see call_model below).
_API_ERROR_PLACEHOLDERS = {"sorry, i could not process your request"}


def _is_api_error_placeholder(content: Optional[str]) -> bool:
    if not content:
        return False
    return content.strip().rstrip(".").lower() in _API_ERROR_PLACEHOLDERS


# ---------------------------------------------------------------------------
# Core call + reasoning preservation
# ---------------------------------------------------------------------------

@dataclass
class ModelTurn:
    """Normalized result of one model call."""
    content: Optional[str]                      # assistant text (may be None)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    reasoning_details: Any = None               # pass back UNMODIFIED next turn
    finish_reason: Optional[str] = None         # e.g. "stop", "length", "tool_calls"
    raw: Any = None                             # original SDK message
    protocol_failure: bool = False              # set by caller if parse fails


def _normalize_tool_calls(msg: Any) -> list[dict[str, Any]]:
    """Real OpenAI tool_calls if present, else a best-effort extraction from
    text-embedded tool calls (see _extract_text_tool_call)."""
    tool_calls: list[dict[str, Any]] = []
    for tc in (getattr(msg, "tool_calls", None) or []):
        # Arguments arrive as a JSON string; parse defensively.
        try:
            args = json.loads(tc.function.arguments or "{}")
            parse_ok = True
        except (json.JSONDecodeError, TypeError):
            args = {"_raw": getattr(tc.function, "arguments", None)}
            parse_ok = False
        tool_calls.append({
            "id": tc.id,
            "name": tc.function.name,
            "arguments": args,
            "parse_ok": parse_ok,
        })

    if not tool_calls:
        text_call = _extract_text_tool_call(msg.content)
        if text_call is not None:
            tool_calls.append({
                "id": f"text-tool-{uuid.uuid4().hex[:8]}",
                "name": text_call["name"],
                "arguments": text_call["arguments"],
                "parse_ok": True,
            })
    return tool_calls


def call_model(
    client: OpenAI,
    cfg: ModelConfig,
    messages: list[dict[str, Any]],
    tools: Optional[list[dict[str, Any]]] = None,
    tool_choice: str | dict = "auto",
    max_retries: int = 2,
) -> ModelTurn:
    """Single chat.completions call. Returns a normalized ModelTurn.

    `tools` is the OpenAI function-calling schema list (see tool_schemas.py).
    When tools is None this is a plain conversational turn.

    Transient failures (dropped/truncated response, connection/timeout/
    rate-limit/5xx) get up to `max_retries` short backoff retries before
    propagating -- these are provider hiccups, not encounter-logic errors,
    and losing a whole scenario run to one is wasteful.
    """
    kwargs: dict[str, Any] = {
        "model": cfg.model,
        "messages": messages,
        "temperature": cfg.temperature,
        "max_tokens": cfg.max_tokens,
        "extra_body": cfg.extra_body(),
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice

    for attempt in range(max_retries + 1):
        try:
            resp = client.chat.completions.create(**kwargs)
            break
        except _TRANSIENT_ERRORS:
            if attempt == max_retries:
                raise
            time.sleep(1.5 * (attempt + 1))

    choice = resp.choices[0]
    msg = choice.message

    tool_calls = _normalize_tool_calls(msg)

    content = msg.content
    if not tool_calls and _is_api_error_placeholder(content):
        content = None  # treated as an empty/truncated turn, not real content

    return ModelTurn(
        content=content,
        tool_calls=tool_calls,
        reasoning_details=getattr(msg, "reasoning_details", None),
        finish_reason=getattr(choice, "finish_reason", None),
        raw=msg,
    )


def append_assistant_turn(messages: list[dict[str, Any]], turn: ModelTurn
                          ) -> list[dict[str, Any]]:
    """Append the assistant message, preserving reasoning_details unmodified.

    Mirrors OpenRouter's reasoning pass-back pattern so the model continues its
    chain of thought on the next call instead of starting over.
    """
    assistant: dict[str, Any] = {"role": "assistant",
                                 "content": turn.content or ""}
    if turn.reasoning_details is not None:
        assistant["reasoning_details"] = turn.reasoning_details  # unmodified
    if turn.tool_calls:
        # Re-attach tool_calls in OpenAI wire format so the thread stays valid.
        assistant["tool_calls"] = [{
            "id": tc["id"],
            "type": "function",
            "function": {"name": tc["name"],
                         "arguments": json.dumps(tc["arguments"])},
        } for tc in turn.tool_calls]
    messages.append(assistant)
    return messages


def append_tool_result(messages: list[dict[str, Any]], tool_call_id: str,
                       result: dict[str, Any]) -> list[dict[str, Any]]:
    """Feed a tool's JSON return back to the model (role='tool')."""
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": json.dumps(result),
    })
    return messages


# ---------------------------------------------------------------------------
# Convenience wrappers for the two roles
# ---------------------------------------------------------------------------

def patient_reply(client: OpenAI, cfg: ModelConfig,
                  messages: list[dict[str, Any]]) -> ModelTurn:
    """Patient conversational turn (no tools)."""
    return call_model(client, cfg, messages, tools=None)


def physician_turn(client: OpenAI, cfg: ModelConfig,
                   messages: list[dict[str, Any]],
                   tools: list[dict[str, Any]],
                   tool_choice: str | dict = "auto") -> ModelTurn:
    """Physician turn: may return plain text (a question) or tool calls.

    `tool_choice="required"` forces a tool call instead of free text -- used
    as a circuit-breaker escalation step when the model has gotten stuck
    returning empty/truncated turns (see core/multi_agent_system.py).
    """
    return call_model(client, cfg, messages, tools=tools, tool_choice=tool_choice)


# ---------------------------------------------------------------------------
# Smoke test (mirrors the OpenRouter reasoning example)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from config.models import PATIENT_MODEL

    client = make_client()
    cfg = ModelConfig(model=PATIENT_MODEL, temperature=0.4, max_tokens=400)

    # Turn 1
    messages = [{"role": "user",
                 "content": "How many r's are in the word 'strawberry'?"}]
    t1 = call_model(client, cfg, messages)
    print("A1:", t1.content)

    # Preserve reasoning, continue the thread
    append_assistant_turn(messages, t1)
    messages.append({"role": "user", "content": "Are you sure? Think carefully."})
    t2 = call_model(client, cfg, messages)
    print("A2:", t2.content)

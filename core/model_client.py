"""
Unified model client for the clinical-agent sycophancy benchmark.
==================================================================

Everything goes through one OpenAI-compatible interface (OpenRouter), so the
physician (model under test) and the patient (roleplay model) are called the
exact same way and only the `model` string differs. This keeps cross-model
comparison fair: same adapter, same message plumbing, same tool protocol.

Two call styles are supported:
  - chat():  a plain conversational turn (patient replies; physician questions).
  - act():   a physician turn that may emit tool calls (function calling).

Reasoning is preserved across turns using OpenRouter's `reasoning_details`
pass-back pattern (see call_model / append_assistant_turn), so a model that
"thinks" continues from where it left off instead of restarting each turn.

Set OPENROUTER_API_KEY in the environment before running.
"""

from __future__ import annotations

import os
import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)

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

    return ModelTurn(
        content=msg.content,
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
                   tools: list[dict[str, Any]]) -> ModelTurn:
    """Physician turn: may return plain text (a question) or tool calls."""
    return call_model(client, cfg, messages, tools=tools, tool_choice="auto")


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

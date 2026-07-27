"""
Model registry for the MedEQ-Bench minimal baseline.

This is the single place that lists which models participate in a run.
To evaluate an additional physician model later, add one entry to
PHYSICIAN_MODELS below -- no other code needs to change.

Keys are short, filesystem-safe labels used for the `results/<model_name>/`
output directory and in summary.csv / metrics.json. Values are the model
slugs as used in the `model` field of the chat completions request --
normally an OpenRouter slug, routed through core.model_client.make_client().
Labels listed in MEDICAL_PLATFORM_MODELS are instead routed through
core.model_client.make_dr7_client() (a separate OpenAI-compatible endpoint
at dr7.ai for medical-specialty models, auth'd via DR7_KEY in .env) -- see
core.model_client.client_for_model().
"""

# Physician (doctor) models under evaluation.
PHYSICIAN_MODELS = {
    "gpt-5.5": "openai/gpt-5.5",
    "kimi-k2.6": "moonshotai/kimi-k2.6",
    "grok-4.3": "x-ai/grok-4.3",
    "Gemini-3.1-Pro": "google/gemini-3.1-pro-preview",
    "Qwen-3.5-397B": "qwen/qwen3.5-397b-a17b",
    "GLM-5.1": "z-ai/glm-5.1",
    "medgemma-4b-it": "medgemma-4b-it",
    "deepseek-v4-pro": "deepseek/deepseek-v4-pro",
    "anthropic-fable-5": "anthropic/claude-fable-5",
    "llama-4-scout": "meta-llama/llama-4-scout",
    # Runs fully locally (no API call) via transformers on this machine's
    # GPU/MPS/CPU -- see core/local_model_client.py. The value here is just
    # the label used for logging; the actual HF repo id
    # ("google/medgemma-1.5-4b-it") lives in
    # core.local_model_client.LOCAL_HF_MODEL_IDS, keyed by this same label.
    "medgemma-1.5-4b": "medgemma-1.5-4b",
}

# Model slugs served via the dr7.ai medical-model platform instead of
# OpenRouter (different base URL, different API key: DR7_KEY). NOTE: the
# dr7.ai API sample only shows plain chat completions (model/messages/
# max_tokens/temperature) -- function-calling ("tools"/"tool_choice") support
# is unconfirmed. If it isn't supported, the physician can never call a
# decision tool and every encounter will end via the circuit breaker's
# give-up path (see core/multi_agent_system.py) rather than a real decision.
# Verify with a small --limit run before trusting the results.
MEDICAL_PLATFORM_MODELS = {"medgemma-4b-it"}

# Labels routed through core.local_model_client (in-process HuggingFace
# inference on this machine -- no network API call) instead of OpenRouter or
# dr7.ai. See core.model_client.client_for_model() and
# core.local_model_client.LOCAL_HF_MODEL_IDS for the label -> HF repo id map.
LOCAL_HF_MODELS = {"medgemma-1.5-4b"}

# Model slugs that reject OpenRouter's `reasoning` param outright (400
# "thinking is not supported by this model"), rather than just ignoring it.
# meta-llama/llama-4-scout routes through Google Vertex on OpenRouter, which
# errors on every request when reasoning is enabled -- confirmed by 23/48
# scenarios failing identically across all 4 emotional_state conditions in
# results/baseline/llama-4-scout/. Reasoning is force-disabled for these
# regardless of the model's own default in core/multi_agent_system.py.
NO_REASONING_MODELS = {"meta-llama/llama-4-scout"}

# Patient simulator model, held constant across every experiment.
PATIENT_MODEL = "minimax/minimax-m3"

# Generation settings for the baseline protocol.
# NOTE: for reasoning-enabled models, reasoning tokens are billed against the
# same max_tokens budget as the visible answer. 256 was too tight for
# moonshotai/kimi-k2.6 -- it was spending the whole budget on its internal
# reasoning trace and getting cut off before it could produce any content or
# tool call. 1536 still produced occasional truncated turns in longer
# encounters (see results/baseline runs with protocol_failure "empty response"
# events), so this is bumped again.
DOCTOR_TEMPERATURE = 0.7
DOCTOR_MAX_TOKENS = 4096
PATIENT_TEMPERATURE = 0.9
PATIENT_MAX_TOKENS = 256

# Hard cap on physician turns per encounter. 10 was sometimes too few:
# extensive history-taking + a couple of truncated turns could burn the whole
# budget before the physician ever reached a decision tool (see
# markers.truncated_before_terminal in the action log).
TURNS_PER_ENCOUNTER = 20


# for emo in neutral anger fear sadness; do
#   python evaluation/main.py --models deepseek-v4-pro --emotional_state "$emo" --patient_prompt implicit
# done

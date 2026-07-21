"""
Model registry for the MedEQ-Bench minimal baseline.

This is the single place that lists which models participate in a run.
To evaluate an additional physician model later, add one entry to
PHYSICIAN_MODELS below -- no other code needs to change.

Keys are short, filesystem-safe labels used for the `results/<model_name>/`
output directory and in summary.csv / metrics.json. Values are the
OpenRouter model slugs (as used in the `model` field of the chat
completions request).
"""

# Physician (doctor) models under evaluation.
PHYSICIAN_MODELS = {
    # "gpt-5.5": "openai/gpt-5.5",
    "kimi-k2.6": "moonshotai/kimi-k2.6",
}

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
DOCTOR_MAX_TOKENS = 3072
PATIENT_TEMPERATURE = 0.9
PATIENT_MAX_TOKENS = 256

# Hard cap on physician turns per encounter. 10 was sometimes too few:
# extensive history-taking + a couple of truncated turns could burn the whole
# budget before the physician ever reached a decision tool (see
# markers.truncated_before_terminal in the action log).
TURNS_PER_ENCOUNTER = 20

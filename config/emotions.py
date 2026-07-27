"""
Registry of emotional-escalation experiment arms.

Each (emotional_state, style) pair maps to a scenario module with the exact
same SCENARIOS / get_scenarios(gold_action) API and scenario_id keys as the
neutral baseline (config/scenarios/baseline_scenarios.py) -- only
`emotional_state` and `chief_complaint` differ per scenario. Style is a
second, orthogonal axis on TOP of emotional_state: "implicit" (the emotion
shows only through tone/word choice, never named -- config/scenarios/
anger_scenarios.py etc.) and "explicit" (the patient names the feeling
outright, e.g. "I'm angry" -- config/scenarios/explicit_anger_scenarios.py
etc.) are two byte-for-byte-identical-except-chief_complaint scenario sets
per non-neutral emotion. Neutral has no style variation (one scenario module,
one prompt, regardless of --patient_prompt).

patient_prompt_filename() resolves which config/prompt/patient_prompt_*.txt
template to load for a given (emotional_state, style) pair, as a path
relative to config/.
"""

EMOTION_LABELS = ("neutral", "anger", "fear", "sadness")
PROMPT_STYLES = ("implicit", "explicit")

SCENARIO_MODULES = {
    ("neutral", "implicit"): "config.scenarios.baseline_scenarios",
    ("neutral", "explicit"): "config.scenarios.baseline_scenarios",
    ("anger", "implicit"): "config.scenarios.anger_scenarios",
    ("anger", "explicit"): "config.scenarios.explicit_anger_scenarios",
    ("fear", "implicit"): "config.scenarios.fear_scenarios",
    ("fear", "explicit"): "config.scenarios.explicit_fear_scenarios",
    ("sadness", "implicit"): "config.scenarios.sadness_scenarios",
    ("sadness", "explicit"): "config.scenarios.explicit_sadness_scenarios",
}


def scenario_module_name(emotional_state: str, style: str) -> str:
    key = (emotional_state, style)
    if key not in SCENARIO_MODULES:
        raise ValueError(f"No scenario module for emotional_state={emotional_state!r}, "
                         f"style={style!r}. Choose from {sorted(SCENARIO_MODULES)}.")
    return SCENARIO_MODULES[key]


def patient_prompt_filename(emotional_state: str, style: str) -> str:
    if emotional_state == "neutral":
        return "prompt/patient_prompt.txt"
    return f"prompt/patient_prompt_{emotional_state}_{style}.txt"

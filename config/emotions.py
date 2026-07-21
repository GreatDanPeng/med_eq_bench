"""
Registry of emotional-escalation experiment arms.

Each emotional_state maps to a scenario module with the exact same SCENARIOS /
get_scenarios(gold_action) API and scenario_id keys as the neutral baseline
(config/scenarios/baseline_scenarios.py) -- only `emotional_state` and
`chief_complaint` differ per scenario (see e.g.
config/scenarios/anger_scenarios.py).

patient_prompt_filename() resolves which config/prompt/patient_prompt_*.txt
template to load for a given (emotional_state, style) pair, as a path
relative to config/. Neutral has one fixed prompt regardless of style; the
other emotions currently only have an "implicit" variant authored (the
emotion shows through tone/word choice, never named outright) -- extend
PROMPT_STYLES as more styles (e.g. "explicit") are authored.
"""

EMOTION_LABELS = ("neutral", "anger", "fear", "sadness")
PROMPT_STYLES = ("implicit",)

SCENARIO_MODULES = {
    "neutral": "config.scenarios.baseline_scenarios",
    "anger": "config.scenarios.anger_scenarios",
    "fear": "config.scenarios.fear_scenarios",
    "sadness": "config.scenarios.sadness_scenarios",
}


def patient_prompt_filename(emotional_state: str, style: str) -> str:
    if emotional_state == "neutral":
        return "prompt/patient_prompt.txt"
    return f"prompt/patient_prompt_{emotional_state}_{style}.txt"

# Health EQ Bench
![EQ Bench](EQbench.png)
## Overview
- Lightweight framework to simulate patient–physician conversations for EQ-sensitive scenarios.
- Uses paired agents (patient and physician) driven by LLMs to test behavioral quality and safety.
- Stores conversation traces and summaries for later analysis or replay.

## Getting Started
- Install deps: `pip install -r requirements.txt`
- Set API keys in your environment (e.g., `API_KEY` for OpenRouter or other providers).
- Run an evaluation: `python evaluation/mvp.py`
- Inspect results under `results/mvp/` (conversation logs and summary JSONs).

## Key Components
- Emotion Recognition: detect primary patient emotion early in the dialogue.
- Communication Adaptation: physician responses adjust tone and content based on the patient state.
- Action Selection: physician selects a recommended action against scenario-specific gold standards.
- Multi-Judge Evaluation: multiple evaluators/metrics assess safety, empathy, and alignment across the conversation.***

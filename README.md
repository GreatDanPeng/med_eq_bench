# SAFEQ-Med: Benchmarking Sycophancy and Safe Clinical Decision-Making in LLM Agents under Emotional Pressure
![EQbench](EQbenchv2.png)
## Overview
- Simulates patient–physician conversations to benchmark a physician model's clinical judgment.
- The physician (model under test) takes a history through plain conversation and then acts via structured tools (order/decline/defer/escalate/etc.). The patient is a fixed roleplay LLM, run in either a **neutral** condition (stays calm throughout) or an **emotional-escalation** condition (anger/fear/sadness, always implicit -- never named outright, no explicit ultimatums).
- Scenarios are paired should-REJECT / should-ORDER cases from Choosing Wisely guidelines (see `config/scenarios/baseline_scenarios.py`); the emotion variants (`config/scenarios/{anger,fear,sadness}_scenarios.py`) reuse the exact same scenario_ids and clinical facts, only the patient's opening line/tone differs.
- Stores a human-readable transcript and a structured action-log JSON per run for later scoring.

## Getting Started
- Install deps: `pip install -r requirements.txt`
- Set `OPENROUTER_API_KEY` (or `OPENROUTER_KEYS`) in your environment/`.env`.
- List physician models and the patient model in `config/models.py`.
- Run the baseline evaluation: `python evaluation/main.py`
  - `--models kimi-k2.6 gpt-5.5` -- only run these physician model labels
  - `--scenario-set order|reject` -- restrict to one scenario family
  - `--scenario-id headache_ct ...` -- run only these exact scenario_id(s)
  - `--limit N` -- only run the first N scenarios (smoke-test)
  - `--seeds 0 1 2` -- run multiple seeds per scenario x model
  - `--emotional_state neutral|anger|fear|sadness` -- patient condition (default: neutral)
  - `--patient_prompt implicit` -- patient prompt style for non-neutral conditions
  - `--quiet` -- suppress the live physician/patient transcript printed to the console (still saved to file either way)
  - `--rebuild-summary` -- rebuild `summary.json` from the `*_seed*.json` action logs already on disk, without calling any model (useful if a run was split across several invocations)
- Inspect results under `results/baseline/<model_label>/<emotional_state>_<style>/` (e.g. `neutral_neutral/`, `anger_implicit/`): one `*.json` action log and one `*.transcript.txt` per scenario/seed, plus a `summary.json` per condition.
- Plot results for one model across all its conditions: `python analysis/plot_baseline_results.py --model kimi-k2.6` (charts land in `analysis/baseline_plots/<model>/`).

## Key Components
- `core/model_client.py` -- unified OpenRouter chat-completions client shared by both agents (same adapter, same tool protocol), with reasoning pass-back across turns and short-backoff retries on transient transport errors.
- `core/multi_agent_system.py` -- the encounter loop: alternates plain patient/physician conversation with physician tool calls (`order_request`, `order_workup`, `offer_alternative_and_counsel`, `decline_request`, `defer`, `escalate`, `raise_flag`, `end_encounter`), validates and logs each tool call like a real order-entry system. `order_workup` returns a gold-consistent synthetic result from the scenario so the physician can act on real findings instead of granting a request under pressure; `order_request` arms a one-shot contraindication rebuttal when it hits a known allergy, and the outcome (`corrected_after_safety_feedback`) is tracked on the action log's `markers` block. `end_encounter` requires a prior decision tool (`DECISION_TOOLS`) before it will close the visit.
- `config/scenarios/baseline_scenarios.py` -- the neutral scenario bank (chief complaint, patient profile, elicitable history, gold action/rationale, `workup_results`); `config/scenarios/{anger,fear,sadness}_scenarios.py` -- the same scenarios with an implicit-emotion opening line.
- `config/prompt/` -- the physician system prompt (`doctor_prompt.txt`, shared across all conditions) and the patient system-prompt templates (`patient_prompt.txt` for neutral, `patient_prompt_{anger,fear,sadness}_implicit.txt` for the escalation arms).
- `config/emotions.py` -- the registry mapping each `emotional_state` to its scenario module and patient-prompt file.
- `config/tool_schemas.py` -- OpenAI-style function-calling schemas for the physician's tools.
- `config/history/` -- superseded scenario-file versions, kept for reference only.
- `analysis/plot_baseline_results.py` -- per-model, per-condition comparison charts (granted rate, stance distribution, completion rate, workup usage, contraindication outcomes).
- See `code/baseline_agent_spec.md` for the full design spec and the current experiment report.

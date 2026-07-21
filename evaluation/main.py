#!/usr/bin/env python3
"""
MedEQ-Bench baseline entry point.

Runs every physician model in config/models.py against the baseline
order/reject scenarios, using the patient/physician tool-calling protocol
implemented in core/multi_agent_system.py (see code/baseline_agent_spec.md
for the design).

By default the patient stays neutral (config/scenarios/baseline_scenarios.py).
Pass --emotional_state to instead run one of the emotional-escalation arms
(config/scenarios/<emotion>_scenarios.py + config/prompt/patient_prompt_
<emotion>_<style>.txt -- same scenario_ids, only the patient's tone differs;
see config/emotions.py).

Usage:
    python evaluation/main.py
    python evaluation/main.py --models kimi-k2.6 --limit 2
    python evaluation/main.py --scenario-set reject --seeds 0 1 2
    python evaluation/main.py --scenario-id headache_ct opioids_acute_back_pain
    python evaluation/main.py --scenario-id headache_ct --quiet
    python evaluation/main.py --emotional_state anger --patient_prompt implicit
    python evaluation/main.py --emotional_state fear --patient_prompt implicit
    python evaluation/main.py --emotional_state sadness --patient_prompt implicit
"""

import argparse
import importlib
import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.append(str(_PROJECT_ROOT))

load_dotenv()

from config.emotions import EMOTION_LABELS, PROMPT_STYLES, SCENARIO_MODULES
from config.models import PHYSICIAN_MODELS
from core.multi_agent_system import run_encounter

RESULTS_DIR = _PROJECT_ROOT / "results" / "baseline"


def condition_dirname(emotional_state: str, patient_prompt_style: str) -> str:
    """Results subdirectory name for a (emotional_state, style) condition.

    Neutral has no real "style" (it's always config/prompt/patient_prompt.txt
    regardless of --patient_prompt), so it's labeled "neutral_neutral" rather
    than e.g. "neutral_implicit" to avoid implying a style that wasn't used.
    """
    style_label = "neutral" if emotional_state == "neutral" else patient_prompt_style
    return f"{emotional_state}_{style_label}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the MedEQ-Bench baseline encounter protocol."
    )
    parser.add_argument(
        "--models", nargs="*", default=None,
        help="Physician model labels from config/models.py to run (default: all).",
    )
    parser.add_argument(
        "--scenario-set", choices=["all", "order", "reject"], default="all",
        help="Restrict to should-order or should-reject scenarios (default: all).",
    )
    parser.add_argument(
        "--scenario-id", nargs="*", default=None,
        help="Run only these exact scenario_id(s) (overrides --scenario-set and --limit).",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Only run the first N scenarios (for smoke-testing).",
    )
    parser.add_argument(
        "--seeds", nargs="*", type=int, default=[0],
        help="Seeds to run per scenario x model (default: [0]).",
    )
    parser.add_argument(
        "--emotional_state", choices=EMOTION_LABELS, default="neutral",
        help="Patient emotional condition: neutral (default) or an escalation "
             "arm (anger/fear/sadness) -- see config/emotions.py.",
    )
    parser.add_argument(
        "--patient_prompt", choices=PROMPT_STYLES, default=PROMPT_STYLES[0],
        help=f"Patient prompt style for non-neutral emotional states "
             f"(default: {PROMPT_STYLES[0]}). Ignored for --emotional_state neutral.",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Don't print the physician/patient conversation live as it runs "
             "(it's always saved to the .transcript.txt file either way).",
    )
    parser.add_argument(
        "--rebuild-summary", action="store_true",
        help="Don't call any model -- just rebuild summary.json for the "
             "resolved condition dir(s) from the *_seed*.json action logs "
             "already on disk. Use this if summary.json is stale or missing "
             "rows from a prior run.",
    )
    return parser.parse_args()


def _summary_row(scenario_id: str, seed: int, action_log: dict) -> dict:
    final_stance = action_log.get("final_stance") or {}
    markers = action_log.get("markers") or {}
    return {
        "scenario_id": scenario_id,
        "seed": seed,
        "gold_action": action_log.get("gold_action"),
        "final_stance": final_stance.get("tool"),
        "closed": action_log.get("closed"),
        "workups_ordered": len(action_log.get("workups") or []),
        "contraindication_triggered": markers.get("contraindication_triggered", False),
        "corrected_after_safety_feedback": markers.get("corrected_after_safety_feedback"),
        "truncated": markers.get("truncated", False),
        "truncated_before_terminal": markers.get("truncated_before_terminal", False),
        "error": None,
    }


def _load_existing_summary(model_dir: Path) -> dict[tuple, dict]:
    """Existing summary.json rows keyed by (scenario_id, seed), if any."""
    summary_file = model_dir / "summary.json"
    if not summary_file.exists():
        return {}
    with open(summary_file) as f:
        rows = json.load(f)
    return {(r["scenario_id"], r["seed"]): r for r in rows}


def _write_summary(model_dir: Path, rows_by_key: dict[tuple, dict]) -> None:
    summary_file = model_dir / "summary.json"
    ordered = [rows_by_key[k] for k in sorted(rows_by_key)]
    with open(summary_file, "w") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)
    print(f"Summary written to {summary_file} ({len(ordered)} rows)")


_SEED_FILENAME_RE = re.compile(r"^(.*)_seed(\d+)\.json$")


def rebuild_summary(model_dir: Path) -> None:
    """Reconstruct summary.json purely from the *_seed*.json action logs
    already on disk in model_dir -- no model calls. Useful when a run was
    split across several invocations and summary.json only reflects the
    last one (each invocation used to overwrite it wholesale)."""
    rows_by_key = {}
    for action_log_file in sorted(model_dir.glob("*_seed*.json")):
        match = _SEED_FILENAME_RE.match(action_log_file.name)
        if not match:
            continue
        scenario_id, seed = match.group(1), int(match.group(2))
        with open(action_log_file) as f:
            action_log = json.load(f)
        rows_by_key[(scenario_id, seed)] = _summary_row(scenario_id, seed, action_log)
    _write_summary(model_dir, rows_by_key)


def run_one(label: str, model_slug: str, scenario_ids: list, seeds: list,
            verbose: bool = True, emotional_state: str = "neutral",
            patient_prompt_style: str = "implicit") -> None:
    model_dir = RESULTS_DIR / label / condition_dirname(emotional_state, patient_prompt_style)
    model_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'#' * 70}\nPHYSICIAN MODEL: {label} ({model_slug})  "
         f"|  emotion={emotional_state}/{patient_prompt_style}\n{'#' * 70}")

    # Merge into whatever summary.json already exists -- a run split across
    # multiple invocations (crash, rate limit, --scenario-id batches) must
    # not clobber previously-completed rows.
    rows_by_key = _load_existing_summary(model_dir)

    for i, scenario_id in enumerate(scenario_ids, 1):
        for seed in seeds:
            print(f"[{i}/{len(scenario_ids)}] {scenario_id} (seed={seed})")
            try:
                transcript, action_log = run_encounter(
                    scenario_id, model_slug, seed,
                    config={"verbose": verbose, "emotional_state": emotional_state,
                           "patient_prompt_style": patient_prompt_style},
                )
            except Exception as exc:  # noqa: BLE001
                print(f"  [ERROR] {exc}")
                rows_by_key[(scenario_id, seed)] = {
                    "scenario_id": scenario_id, "seed": seed, "error": str(exc),
                }
                continue

            base = model_dir / f"{scenario_id}_seed{seed}"
            with open(base.with_suffix(".json"), "w") as f:
                json.dump(action_log, f, ensure_ascii=False, indent=2)
            with open(base.with_suffix(".transcript.txt"), "w") as f:
                f.write("\n".join(transcript))

            rows_by_key[(scenario_id, seed)] = _summary_row(scenario_id, seed, action_log)

    _write_summary(model_dir, rows_by_key)


def resolve_scenario_ids(args: argparse.Namespace) -> list:
    scenario_module = importlib.import_module(SCENARIO_MODULES[args.emotional_state])
    scenarios = scenario_module.SCENARIOS

    if args.scenario_id:
        valid = [sid for sid in args.scenario_id if sid in scenarios]
        for sid in args.scenario_id:
            if sid not in scenarios:
                print(f"[SKIP] Unknown scenario_id: {sid}")
        return valid

    gold_action = None if args.scenario_set == "all" else args.scenario_set
    scenario_ids = list(scenario_module.get_scenarios(gold_action).keys())
    if args.limit:
        scenario_ids = scenario_ids[: args.limit]
    return scenario_ids


def main() -> None:
    args = parse_args()
    labels = args.models or list(PHYSICIAN_MODELS.keys())

    if args.rebuild_summary:
        for label in labels:
            if label not in PHYSICIAN_MODELS:
                print(f"[SKIP] Unknown physician model label: {label}")
                continue
            model_dir = RESULTS_DIR / label / condition_dirname(
                args.emotional_state, args.patient_prompt)
            if not model_dir.is_dir():
                print(f"[SKIP] No results directory at {model_dir}")
                continue
            rebuild_summary(model_dir)
        return

    scenario_ids = resolve_scenario_ids(args)
    if not scenario_ids:
        print("[ERROR] No valid scenarios to run.")
        return

    for label in labels:
        if label not in PHYSICIAN_MODELS:
            print(f"[SKIP] Unknown physician model label: {label}")
            continue
        run_one(label, PHYSICIAN_MODELS[label], scenario_ids, args.seeds,
                verbose=not args.quiet, emotional_state=args.emotional_state,
                patient_prompt_style=args.patient_prompt)


if __name__ == "__main__":
    main()

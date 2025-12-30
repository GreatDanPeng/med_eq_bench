"""
Re-run MVP experiments that failed due to physician API errors.

This script scans summary_*.json files under results/mvp, looks for
entries with an error like "Interaction failed: Physician agent API call failed
at turn {n}", and retries those scenarios. Successful retries create a new
conversation_<timestamp>.json in the same folder and update the summary to
reflect the non-error result. If the retry still fails, the summary is left
unchanged for that scenario.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.eq_scenarios import TEST_EQ_SCENARIOS
from config.eq_settings import InteractionScenario
from core.multi_agent_system import (
    HealthcareMultiAgentSystem,
    PatientAgent,
    PhysicianAgent,
    PatientSatisfactionEvaluator,
)

load_dotenv()

PATIENT_MODEL_API = "xiaomi/mimo-v2-flash:free"
PHYSICIAN_ERROR_MARKER = "Physician agent API call failed"


def build_system(scenario_id: str, physician_model_api: str) -> HealthcareMultiAgentSystem:
    """Create a HealthcareMultiAgentSystem for the given scenario/model combo."""
    if scenario_id not in TEST_EQ_SCENARIOS:
        raise ValueError(f"Scenario {scenario_id} not found in TEST_EQ_SCENARIOS")

    data = TEST_EQ_SCENARIOS[scenario_id]
    scenario = InteractionScenario(
        scenario_id=data["scenario_id"],
        interaction_type=data["interaction_type"],
        patient_profile=data["patient_profile"],
        physician_profile=data["physician_profile"],
        clinical_guidelines=data["clinical_guidelines"],
        gold_standard_action=data["gold_standard_action"],
    )

    patient_agent = PatientAgent(
        patient_id=f"patient_{scenario_id}",
        scenario=scenario,
        model_name=PATIENT_MODEL_API,
    )
    physician_agent = PhysicianAgent(
        physician_id=f"physician_{scenario_id}",
        scenario=scenario,
        model_name=physician_model_api,
    )
    satisfaction_evaluator = PatientSatisfactionEvaluator(model_name=PATIENT_MODEL_API)

    return HealthcareMultiAgentSystem(
        patient_agent=patient_agent,
        physician_agent=physician_agent,
        satisfaction_evaluator=satisfaction_evaluator,
        max_turns=10,
    )


def rerun_summary(summary_path: Path) -> None:
    """Retry failed physician API interactions referenced in a summary file."""
    with open(summary_path, "r") as f:
        summary = json.load(f)

    physician_model_api = summary.get("physician_model_api")
    if not physician_model_api:
        print(f"[SKIP] No physician_model_api in {summary_path}")
        return

    results: List[Dict] = summary.get("results", [])
    updated_results: List[Dict] = []
    summary_updated = False

    for entry in results:
        error = entry.get("error")
        scenario_id = entry.get("scenario_id")

        if not (error and PHYSICIAN_ERROR_MARKER in error):
            updated_results.append(entry)
            continue

        print(f"[RETRY] {summary_path.name} :: scenario={scenario_id} error='{error}'")

        try:
            system = build_system(scenario_id, physician_model_api)
            new_result = system.run_interaction()
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] Could not rerun scenario {scenario_id}: {exc}")
            updated_results.append(entry)
            continue

        if "error" in new_result:
            print(f"[FAIL] Retry still failed for {scenario_id}: {new_result['error']}")
            updated_results.append(entry)
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        conversation_path = summary_path.parent / f"conversation_{timestamp}.json"
        with open(conversation_path, "w") as f:
            json.dump(new_result, f, indent=2)

        updated_entry = {
            "scenario_id": scenario_id,
            "result_file": str(conversation_path),
            "detected_emotion": new_result.get("detected_emotion"),
            "doctor_action": new_result.get("doctor_action"),
            "gold_standard_action": new_result.get("gold_standard_action"),
            "action_matches_gold_standard": new_result.get("action_matches_gold_standard"),
            "patient_satisfaction_raw": new_result.get("patient_satisfaction_raw"),
            "turns_completed": new_result.get("turns_completed"),
            "error": None,
        }

        updated_results.append(updated_entry)
        summary_updated = True
        print(f"[OK] Saved new conversation to {conversation_path}")

    if not summary_updated:
        print(f"[DONE] No updates needed for {summary_path}")
        return

    summary["results"] = updated_results
    summary["completed_scenarios"] = len([r for r in updated_results if not r.get("error")])
    summary["failed_scenarios"] = len([r for r in updated_results if r.get("error")])
    summary["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[UPDATED] Summary written to {summary_path}")


def find_summary_files(base_dir: Path) -> List[Path]:
    """Locate summary files under the base directory."""
    return sorted(base_dir.rglob("summary_*.json"))


def main():
    parser = argparse.ArgumentParser(
        description="Re-run MVP experiments that failed with physician API errors."
    )
    parser.add_argument(
        "--summary",
        type=Path,
        help="Path to a specific summary_*.json to rerun (default scans results/mvp).",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=project_root / "results" / "mvp",
        help="Base directory containing MVP results (default: ./results/mvp).",
    )
    args = parser.parse_args()

    if args.summary:
        if not args.summary.exists():
            print(f"[ERROR] Summary file not found: {args.summary}")
            return
        summaries = [args.summary]
    else:
        summaries = find_summary_files(args.base_dir)

    if not summaries:
        print(f"[INFO] No summary files found under {args.base_dir}")
        return

    for summary_path in summaries:
        rerun_summary(summary_path)


if __name__ == "__main__":
    main()

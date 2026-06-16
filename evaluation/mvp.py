"""
MVP Evaluation Script for Healthcare EQ Benchmarks

This script runs the multi-agent system on TEST_EQ_SCENARIOS
with multiple physician models from openrouter_free.
"""

import json
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.multi_agent_system import HealthcareMultiAgentSystem, PatientAgent, PhysicianAgent, PatientSatisfactionEvaluator
from config.eq_scenarios import TEST_EQ_SCENARIOS
from config.eq_settings import InteractionScenario
from config.api_config import AVAILABLE_MODELS


DEFAULT_PATIENT_MODEL = "xiaomi/mimo-v2.5"


def _display_model_name(model_name: str) -> str:
    """Return a filesystem-friendly display name for a model."""
    return model_name.split("/")[-1].replace(":free", "").replace(":", "_")


def _select_models(available_models, requested_models=None, max_models=None):
    """Select physician models from config, optionally allowing explicit model names."""
    if requested_models:
        selected = {}
        for model_name in requested_models:
            selected[model_name] = available_models.get(
                model_name,
                {
                    "name": model_name,
                    "provider": "openrouter",
                    "max_tokens": 4096,
                    "temperature": 0.7,
                    "description": "User-specified OpenRouter model",
                },
            )
    else:
        selected = dict(available_models)

    if max_models is not None:
        selected = dict(list(selected.items())[:max_models])

    return selected


def _select_scenarios(requested_scenarios=None, max_scenarios=None):
    """Select scenarios from TEST_EQ_SCENARIOS."""
    if requested_scenarios:
        missing = [scenario for scenario in requested_scenarios if scenario not in TEST_EQ_SCENARIOS]
        if missing:
            raise ValueError(f"Unknown scenario(s): {', '.join(missing)}")
        selected = {scenario: TEST_EQ_SCENARIOS[scenario] for scenario in requested_scenarios}
    else:
        selected = dict(TEST_EQ_SCENARIOS)

    if max_scenarios is not None:
        selected = dict(list(selected.items())[:max_scenarios])

    return selected


def run_mvp_evaluation(
    patient_model_api=DEFAULT_PATIENT_MODEL,
    physician_model_names=None,
    max_models=None,
    scenario_ids=None,
    max_scenarios=None,
    max_turns=10,
):
    """
    Run MVP evaluation on all TEST_EQ_SCENARIOS with multiple physician models.
    By default this runs all configured physician models and all TEST_EQ_SCENARIOS.
    """

    # Get all free models for physician testing
    available_physician_models = AVAILABLE_MODELS.get("openrouter_free", {})
    physician_models = _select_models(
        available_physician_models,
        requested_models=physician_model_names,
        max_models=max_models,
    )
    scenarios = _select_scenarios(
        requested_scenarios=scenario_ids,
        max_scenarios=max_scenarios,
    )

    # Patient model
    patient_model_display = _display_model_name(patient_model_api)

    print("="*80)
    print("MVP EVALUATION - Healthcare EQ Benchmarks")
    print("="*80)
    print(f"Patient Model: {patient_model_display}")
    print(f"Physician Models: {len(physician_models)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Max Turns: {max_turns}")
    print("="*80)
    print()

    # Run each physician model
    for physician_model_api, model_config in physician_models.items():
        physician_model_display = _display_model_name(physician_model_api)

        print(f"\n{'#'*80}")
        print(f"TESTING PHYSICIAN MODEL: {physician_model_display}")
        print(f"{'#'*80}\n")

        # Create results directory for this physician model
        results_dir = project_root / "results" / "mvp" / physician_model_display / f"{patient_model_display}_{physician_model_display}"
        results_dir.mkdir(parents=True, exist_ok=True)

        all_results = []

        # Run each scenario
        for i, (scenario_id, scenario_data) in enumerate(scenarios.items(), 1):
            print(f"[{i}/{len(scenarios)}] Running scenario: {scenario_id}")
            print("-"*80)

            try:
                # Create scenario
                scenario = InteractionScenario(
                    scenario_id=scenario_data["scenario_id"],
                    interaction_type=scenario_data["interaction_type"],
                    patient_profile=scenario_data["patient_profile"],
                    physician_profile=scenario_data["physician_profile"],
                    clinical_guidelines=scenario_data["clinical_guidelines"],
                    gold_standard_action=scenario_data["gold_standard_action"]
                )

                # Create agents
                patient_agent = PatientAgent(
                    patient_id=f"patient_{scenario_id}",
                    scenario=scenario,
                    model_name=patient_model_api
                )

                physician_agent = PhysicianAgent(
                    physician_id=f"physician_{scenario_id}",
                    scenario=scenario,
                    model_name=physician_model_api
                )

                satisfaction_evaluator = PatientSatisfactionEvaluator(
                    model_name=patient_model_api
                )

                # Create system
                system = HealthcareMultiAgentSystem(
                    patient_agent=patient_agent,
                    physician_agent=physician_agent,
                    satisfaction_evaluator=satisfaction_evaluator,
                    max_turns=max_turns
                )

                # Run interaction
                result = system.run_interaction()

                # Generate timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Save individual conversation result
                result_file = results_dir / f"conversation_{timestamp}.json"
                with open(result_file, 'w') as f:
                    json.dump(result, f, indent=2)

                print(f"Saved to: {result_file}")

                # Collect results
                all_results.append({
                    "scenario_id": scenario_id,
                    "result_file": str(result_file),
                    "detected_emotion": result.get("detected_emotion"),
                    "doctor_action": result.get("doctor_action"),
                    "gold_standard_action": result.get("gold_standard_action"),
                    "action_matches_gold_standard": result.get("action_matches_gold_standard"),
                    "patient_satisfaction_raw": result.get("patient_satisfaction_raw"),
                    "turns_completed": result.get("turns_completed"),
                    "error": result.get("error", None)
                })

            except Exception as e:
                print(f"Error in scenario {scenario_id}: {e}")
                all_results.append({
                    "scenario_id": scenario_id,
                    "error": str(e)
                })

            print("-"*80)

        # Save summary for this physician model
        summary_file = results_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        summary = {
            "patient_model": patient_model_display,
            "patient_model_api": patient_model_api,
            "physician_model": physician_model_display,
            "physician_model_api": physician_model_api,
            "total_scenarios": len(scenarios),
            "completed_scenarios": len([r for r in all_results if "error" not in r or r["error"] is None]),
            "failed_scenarios": len([r for r in all_results if "error" in r and r["error"] is not None]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "results": all_results
        }

        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\n{physician_model_display} COMPLETE:")
        print(f"  Completed: {summary['completed_scenarios']}/{summary['total_scenarios']}")
        print(f"  Summary: {summary_file}\n")

    print("\n" + "="*80)
    print("ALL EVALUATIONS COMPLETE")
    print("="*80)


def parse_args():
    parser = argparse.ArgumentParser(description="Run MVP Healthcare EQ benchmark evaluations.")
    parser.add_argument(
        "--patient-model",
        default=DEFAULT_PATIENT_MODEL,
        help=f"Patient model to use via OpenRouter (default: {DEFAULT_PATIENT_MODEL}).",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        help="Physician model names to run. Defaults to all openrouter_free models.",
    )
    parser.add_argument(
        "--max-models",
        type=int,
        help="Run only the first N selected/configured physician models.",
    )
    parser.add_argument(
        "--scenarios",
        nargs="+",
        help="Scenario IDs to run. Defaults to all TEST_EQ_SCENARIOS.",
    )
    parser.add_argument(
        "--max-scenarios",
        type=int,
        help="Run only the first N selected/configured scenarios.",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=10,
        help="Maximum doctor turns per interaction (default: 10).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_mvp_evaluation(
        patient_model_api=args.patient_model,
        physician_model_names=args.models,
        max_models=args.max_models,
        scenario_ids=args.scenarios,
        max_scenarios=args.max_scenarios,
        max_turns=args.max_turns,
    )

"""
MVP Evaluation Script for Healthcare EQ Benchmarks

This script runs the multi-agent system on TEST_EQ_SCENARIOS
with multiple physician models from openrouter_free.
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.multi_agent_system import HealthcareMultiAgentSystem, PatientAgent, PhysicianAgent, PatientSatisfactionEvaluator
from config.eq_scenarios import TEST_EQ_SCENARIOS
from config.eq_settings import InteractionScenario
from config.api_config import AVAILABLE_MODELS


def run_mvp_evaluation():
    """
    Run MVP evaluation on all TEST_EQ_SCENARIOS with multiple physician models.
    Patient model: mimo-v2.5
    Physician models: All models from openrouter_free
    """

    # Get all free models for physician testing
    physician_models = AVAILABLE_MODELS.get("openrouter_free", {})

    # Patient model (fixed)
    patient_model_api = "xiaomi/mimo-v2.5"
    patient_model_display = "mimo-v2.5"

    print("="*80)
    print("MVP EVALUATION - Healthcare EQ Benchmarks")
    print("="*80)
    print(f"Patient Model: {patient_model_display}")
    print(f"Physician Models: {len(physician_models)} models from openrouter_free")
    print(f"Scenarios: {len(TEST_EQ_SCENARIOS)} scenarios from TEST_EQ_SCENARIOS")
    print("="*80)
    print()

    # Run each physician model
    for physician_model_api, model_config in physician_models.items():
        physician_model_display = physician_model_api.split('/')[1].replace(':free', '')

        print(f"\n{'#'*80}")
        print(f"TESTING PHYSICIAN MODEL: {physician_model_display}")
        print(f"{'#'*80}\n")

        # Create results directory for this physician model
        results_dir = project_root / "results" / "mvp" / physician_model_display / f"{patient_model_display}_{physician_model_display}"
        results_dir.mkdir(parents=True, exist_ok=True)

        all_results = []

        # Run each scenario
        for i, (scenario_id, scenario_data) in enumerate(TEST_EQ_SCENARIOS.items(), 1):
            print(f"[{i}/{len(TEST_EQ_SCENARIOS)}] Running scenario: {scenario_id}")
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
                    max_turns=10
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
            "physician_model": physician_model_display,
            "physician_model_api": physician_model_api,
            "total_scenarios": len(TEST_EQ_SCENARIOS),
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


if __name__ == "__main__":
    run_mvp_evaluation()

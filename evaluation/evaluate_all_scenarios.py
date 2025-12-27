#!/usr/bin/env python3
"""
Evaluate All Scenarios Script

This script loops through all scenarios in PHYSICIAN_EQ_SCENARIOS and evaluates
each one with all models in model_list, saving results in scenario-specific directories.
"""

import os
import sys
import time
import glob
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
load_dotenv()

from config.physician_eq_scenarios import PHYSICIAN_EQ_SCENARIOS, list_physician_scenarios, get_scenario_descriptions
from evaluation.spiral import (
    SpiralConversationSystem,
    SpiralEvaluationResult,
    extract_model_name,
    model_list,
    default_model,
    default_model_name
)


def check_scenario_results_exist(output_dir: str, model_name: str) -> bool:
    """
    Check if results already exist for a given model in a scenario directory.

    Args:
        output_dir: Directory where results are stored for this scenario
        model_name: Name of the model (e.g., "deepseek-chat-v3.1")

    Returns:
        True if results exist, False otherwise
    """
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Search for existing result files matching the pattern
    pattern = f"{output_dir}/*{model_name}*.json"
    existing_files = glob.glob(pattern)

    return len(existing_files) > 0


def evaluate_all_scenarios_all_models(
    base_output_dir: str = "/Users/danpengair/med_eq_bench/results/physcians/gemini-2.5-flash_physicians/merge_eval/base_physicians",
    use_multi_evaluator: bool = True
):
    """
    Loop through all scenarios and all models, evaluating each combination.

    Args:
        base_output_dir: Base directory for results (subdirectories created per scenario)
        use_multi_evaluator: If True, uses multiple evaluators from Evaluator_list
    """
    # Get all available scenarios
    scenarios = list_physician_scenarios()
    scenario_descriptions = get_scenario_descriptions()

    print("="*70)
    print("EVALUATING ALL SCENARIOS WITH ALL MODELS")
    print("="*70)
    print(f"Base output directory: {base_output_dir}")
    print(f"Total scenarios: {len(scenarios)}")
    print(f"Total models per scenario: {len(model_list)}")
    print(f"Total evaluations planned: {len(scenarios) * len(model_list)}")
    print(f"Multi-evaluator mode: {use_multi_evaluator}")
    print("="*70)
    print()

    # Summary tracking
    overall_summary = {
        "total_scenarios": len(scenarios),
        "total_models": len(model_list),
        "completed": 0,
        "skipped": 0,
        "failed": 0,
        "scenario_results": {}
    }

    # Loop through each scenario
    for scenario_idx, scenario_name in enumerate(scenarios, 1):
        print(f"\n{'#'*70}")
        print(f"# SCENARIO {scenario_idx}/{len(scenarios)}: {scenario_name}")
        print(f"# Description: {scenario_descriptions.get(scenario_name, 'N/A')}")
        print(f"{'#'*70}\n")

        # Create scenario-specific output directory
        scenario_output_dir = os.path.join(base_output_dir, scenario_name)
        os.makedirs(scenario_output_dir, exist_ok=True)

        # Initialize system for this scenario
        system = SpiralConversationSystem(
            use_multi_evaluator=use_multi_evaluator,
            evaluator_temperature=0.1
        )

        scenario_summary = {
            "completed": 0,
            "skipped": 0,
            "failed": 0,
            "models": []
        }

        # Loop through each model
        for model_idx, model in enumerate(model_list, 1):
            print(f"\n[Scenario {scenario_idx}/{len(scenarios)}] [Model {model_idx}/{len(model_list)}]")
            print(f"{'='*70}")

            # Extract model name
            model_name = extract_model_name(model)

            print(f"Model: {model}")
            print(f"Model Name: {model_name}")
            print(f"Scenario: {scenario_name}")
            print(f"Output Dir: {scenario_output_dir}")
            print(f"{'='*70}\n")

            # Check if results already exist
            if check_scenario_results_exist(scenario_output_dir, model_name):
                print(f"⏭️  SKIPPING: Results already exist for {model_name} in {scenario_name}")
                scenario_summary["skipped"] += 1
                overall_summary["skipped"] += 1
                scenario_summary["models"].append({
                    "model": model,
                    "model_name": model_name,
                    "status": "SKIPPED"
                })
                continue

            try:
                # Run evaluation
                print(f"🚀 Starting evaluation...")
                result = system.run_10_round_conversation(scenario_name)

                # Check if there were API failures
                if "error" in result.quality_scores and result.quality_scores["error"] == "API_CALL_FAILED":
                    print(f"\n❌ EVALUATION FAILED for {model_name}: Cannot connect to OpenRouter server")
                    scenario_summary["failed"] += 1
                    overall_summary["failed"] += 1
                    scenario_summary["models"].append({
                        "model": model,
                        "model_name": model_name,
                        "status": "FAILED",
                        "error": "API_CALL_FAILED"
                    })
                    continue

                # Save results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"{scenario_output_dir}/spiral_evaluation_{model_name}_{scenario_name}_{timestamp}.json"
                system.save_results(result, str(output_file))
                print(f"\n✅ Results saved to: {output_file}")

                scenario_summary["completed"] += 1
                overall_summary["completed"] += 1
                scenario_summary["models"].append({
                    "model": model,
                    "model_name": model_name,
                    "status": "SUCCESS",
                    "output_file": output_file,
                    "overall_score": result.quality_scores.get("overall_score", 0)
                })

            except Exception as e:
                print(f"❌ Error during evaluation of {model_name} in {scenario_name}: {e}")
                import traceback
                traceback.print_exc()
                scenario_summary["failed"] += 1
                overall_summary["failed"] += 1
                scenario_summary["models"].append({
                    "model": model,
                    "model_name": model_name,
                    "status": "ERROR",
                    "error": str(e)
                })

            # Delay between models to avoid rate limiting
            if model_idx < len(model_list):
                wait_time = 2
                print(f"\n⏳ Waiting {wait_time}s before next model...")
                time.sleep(wait_time)

        # Store scenario summary
        overall_summary["scenario_results"][scenario_name] = scenario_summary

        # Print scenario summary
        print(f"\n{'='*70}")
        print(f"SCENARIO '{scenario_name}' COMPLETE")
        print(f"{'='*70}")
        print(f"Completed: {scenario_summary['completed']}")
        print(f"Skipped: {scenario_summary['skipped']}")
        print(f"Failed: {scenario_summary['failed']}")
        print(f"{'='*70}\n")

        # Delay between scenarios
        if scenario_idx < len(scenarios):
            wait_time = 5
            print(f"⏳ Waiting {wait_time}s before next scenario...\n")
            time.sleep(wait_time)

    # Print final overall summary
    print(f"\n{'#'*70}")
    print(f"# OVERALL EVALUATION COMPLETE")
    print(f"{'#'*70}")
    print(f"Total scenarios evaluated: {overall_summary['total_scenarios']}")
    print(f"Total models per scenario: {overall_summary['total_models']}")
    print(f"Total evaluations planned: {overall_summary['total_scenarios'] * overall_summary['total_models']}")
    print(f"")
    print(f"Results:")
    print(f"  ✅ Completed: {overall_summary['completed']}")
    print(f"  ⏭️  Skipped: {overall_summary['skipped']}")
    print(f"  ❌ Failed: {overall_summary['failed']}")
    print(f"{'#'*70}\n")

    # Print per-scenario breakdown
    print("Per-Scenario Breakdown:")
    print(f"{'-'*70}")
    for scenario_name, summary in overall_summary["scenario_results"].items():
        print(f"{scenario_name}:")
        print(f"  Completed: {summary['completed']}, Skipped: {summary['skipped']}, Failed: {summary['failed']}")

    print(f"\n{'#'*70}")
    print(f"All results saved to: {base_output_dir}")
    print(f"{'#'*70}\n")


def main():
    """Run evaluation for all scenarios and all models."""
    # You can customize these parameters
    base_output_dir = "/Users/danpengair/med_eq_bench/results/physcians/gemini-2.5-flash_physicians/merge_eval/base_physicians"
    use_multi_evaluator = True  # Set to False for single evaluator mode

    evaluate_all_scenarios_all_models(
        base_output_dir=base_output_dir,
        use_multi_evaluator=use_multi_evaluator
    )


if __name__ == "__main__":
    main()

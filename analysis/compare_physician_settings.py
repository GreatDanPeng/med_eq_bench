#!/usr/bin/env python3
"""
Physician Settings Comparison Analysis

This script compares physician models across different settings (base vs caring)
for word count and behavioral metrics.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Constants
BASE_DIR = "/Users/danpengair/med_eq_bench/results/physcians/gemini-2.5-flash_physicians/merge_eval/base_physicians"
CARING_DIR = "/Users/danpengair/med_eq_bench/results/physcians/gemini-2.5-flash_physicians/merge_eval/caring_physicians"
OUTPUT_DIR = "/Users/danpengair/med_eq_bench/analysis/comparison_plots"


class PhysicianSettingsComparator:
    """Compare physician performance across different settings."""

    def __init__(self, base_dir: str, caring_dir: str, output_dir: str):
        self.base_dir = Path(base_dir)
        self.caring_dir = Path(caring_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.base_results = {}
        self.caring_results = {}

    def load_results(self) -> None:
        """Load results from both directories."""
        print("Loading base physician results...")
        self.base_results = self._load_from_directory(self.base_dir)
        print(f"  Loaded {len(self.base_results)} base physician models")

        print("Loading caring physician results...")
        self.caring_results = self._load_from_directory(self.caring_dir)
        print(f"  Loaded {len(self.caring_results)} caring physician models")

    def _load_from_directory(self, directory: Path) -> Dict[str, Dict]:
        """Load all JSON files from a directory and extract model data."""
        results = {}

        if not directory.exists():
            print(f"  Warning: Directory not found: {directory}")
            return results

        json_files = list(directory.glob("*.json"))

        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                # Extract model name from filename
                # Format: merge_eval_spiral_evaluation_{model_name}_{scenario}_{timestamp}.json
                # OR: spiral_evaluation_{model_name}_{scenario}_{timestamp}.json
                filename_parts = json_file.stem.split("_")

                # Find model name (after "evaluation" keyword)
                model_name = "unknown"
                for i, part in enumerate(filename_parts):
                    if part == "evaluation" and i + 1 < len(filename_parts):
                        model_name = filename_parts[i + 1]
                        break

                # Extract relevant data
                results[model_name] = {
                    "quality_scores": data.get("quality_scores", {}),
                    "behavioral_metrics": data.get("behavioral_metrics", {}),
                    "word_count_stats": data.get("word_count_stats", {}),
                    "filename": json_file.name
                }

            except Exception as e:
                print(f"  Error loading {json_file.name}: {e}")

        return results

    def compare_word_counts(self) -> None:
        """Compare word counts per model between base and caring settings."""
        print("\nGenerating word count comparison plots...")

        # Get common models
        common_models = sorted(set(self.base_results.keys()) & set(self.caring_results.keys()))

        if not common_models:
            print("  No common models found between base and caring settings")
            return

        # Prepare data
        models = []
        base_patient_words = []
        caring_patient_words = []
        base_physician_words = []
        caring_physician_words = []

        for model in common_models:
            base_wc = self.base_results[model]["word_count_stats"]
            caring_wc = self.caring_results[model]["word_count_stats"]

            if base_wc and caring_wc:
                models.append(model)
                base_patient_words.append(base_wc.get("patient_avg_words_per_round", 0))
                caring_patient_words.append(caring_wc.get("patient_avg_words_per_round", 0))
                base_physician_words.append(base_wc.get("physician_avg_words_per_round", 0))
                caring_physician_words.append(caring_wc.get("physician_avg_words_per_round", 0))

        if not models:
            print("  No word count data available")
            return

        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

        x_pos = np.arange(len(models))
        width = 0.35

        # Plot 1: Patient word count comparison
        bars1 = ax1.bar(x_pos - width/2, base_patient_words, width,
                       label='Base Physicians', color='steelblue', alpha=0.8)
        bars2 = ax1.bar(x_pos + width/2, caring_patient_words, width,
                       label='Caring Physicians', color='lightcoral', alpha=0.8)

        ax1.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Average Words per Round', fontsize=12, fontweight='bold')
        ax1.set_title('Patient Word Count: Base vs Caring Physicians', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(models, rotation=45, ha='right')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        for bar in bars2:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=8)

        # Plot 2: Physician word count comparison
        bars3 = ax2.bar(x_pos - width/2, base_physician_words, width,
                       label='Base Physicians', color='steelblue', alpha=0.8)
        bars4 = ax2.bar(x_pos + width/2, caring_physician_words, width,
                       label='Caring Physicians', color='lightcoral', alpha=0.8)

        ax2.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Average Words per Round', fontsize=12, fontweight='bold')
        ax2.set_title('Physician Word Count: Base vs Caring Physicians', fontsize=14, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(models, rotation=45, ha='right')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar in bars3:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        for bar in bars4:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        output_file = self.output_dir / "word_count_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {output_file}")

    def compare_behavioral_metrics(self) -> None:
        """Compare positive vs negative behavior counts between settings."""
        print("\nGenerating behavioral metrics comparison plots...")

        # Get common models
        common_models = sorted(set(self.base_results.keys()) & set(self.caring_results.keys()))

        if not common_models:
            print("  No common models found")
            return

        # Define behavior categories
        positive_behaviors = ["pushback", "de-escalation", "safe_redirection", "suggestions_to_seek_help"]
        negative_behaviors = ["emotional_or_narrative_escalation", "sycophancy_or_praise",
                            "delusion_reinforcement", "consciousness_claims", "harmful_advice"]

        # Prepare data
        models = []
        base_positive = []
        caring_positive = []
        base_negative = []
        caring_negative = []

        for model in common_models:
            base_metrics = self.base_results[model]["behavioral_metrics"]
            caring_metrics = self.caring_results[model]["behavioral_metrics"]

            if base_metrics and caring_metrics:
                models.append(model)

                # Count positive behaviors
                base_pos = sum(len(base_metrics.get(behavior, [])) for behavior in positive_behaviors)
                caring_pos = sum(len(caring_metrics.get(behavior, [])) for behavior in positive_behaviors)
                base_positive.append(base_pos)
                caring_positive.append(caring_pos)

                # Count negative behaviors
                base_neg = sum(len(base_metrics.get(behavior, [])) for behavior in negative_behaviors)
                caring_neg = sum(len(caring_metrics.get(behavior, [])) for behavior in negative_behaviors)
                base_negative.append(base_neg)
                caring_negative.append(caring_neg)

        if not models:
            print("  No behavioral metrics data available")
            return

        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

        x_pos = np.arange(len(models))
        width = 0.35

        # Plot 1: Positive behaviors comparison
        bars1 = ax1.bar(x_pos - width/2, base_positive, width,
                       label='Base Physicians', color='#3cb44b', alpha=0.8)
        bars2 = ax1.bar(x_pos + width/2, caring_positive, width,
                       label='Caring Physicians', color='#42d4f4', alpha=0.8)

        ax1.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Total Positive Behavior Count', fontsize=12, fontweight='bold')
        ax1.set_title('Positive Behaviors: Base vs Caring Physicians', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(models, rotation=45, ha='right')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        for bar in bars2:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

        # Plot 2: Negative behaviors comparison
        bars3 = ax2.bar(x_pos - width/2, base_negative, width,
                       label='Base Physicians', color='#e6194B', alpha=0.8)
        bars4 = ax2.bar(x_pos + width/2, caring_negative, width,
                       label='Caring Physicians', color='#f58231', alpha=0.8)

        ax2.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Total Negative Behavior Count', fontsize=12, fontweight='bold')
        ax2.set_title('Negative Behaviors: Base vs Caring Physicians', fontsize=14, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(models, rotation=45, ha='right')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar in bars3:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        for bar in bars4:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        output_file = self.output_dir / "behavioral_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {output_file}")

    def generate_summary_stats(self) -> None:
        """Print summary statistics comparing both settings."""
        print("\n" + "="*70)
        print("PHYSICIAN SETTINGS COMPARISON SUMMARY")
        print("="*70)

        common_models = sorted(set(self.base_results.keys()) & set(self.caring_results.keys()))

        print(f"Base physician models: {len(self.base_results)}")
        print(f"Caring physician models: {len(self.caring_results)}")
        print(f"Common models: {len(common_models)}")

        if common_models:
            print(f"\nCommon models: {', '.join(common_models)}")

            # Average differences
            print("\n" + "-"*70)
            print("AVERAGE METRICS ACROSS ALL MODELS")
            print("-"*70)

            # Word count averages
            base_patient_avg = []
            caring_patient_avg = []
            base_physician_avg = []
            caring_physician_avg = []

            for model in common_models:
                base_wc = self.base_results[model]["word_count_stats"]
                caring_wc = self.caring_results[model]["word_count_stats"]

                if base_wc and caring_wc:
                    base_patient_avg.append(base_wc.get("patient_avg_words_per_round", 0))
                    caring_patient_avg.append(caring_wc.get("patient_avg_words_per_round", 0))
                    base_physician_avg.append(base_wc.get("physician_avg_words_per_round", 0))
                    caring_physician_avg.append(caring_wc.get("physician_avg_words_per_round", 0))

            if base_patient_avg:
                print("\nWord Count (Average across models):")
                print(f"  Patient words - Base: {np.mean(base_patient_avg):.1f}, Caring: {np.mean(caring_patient_avg):.1f}")
                print(f"  Physician words - Base: {np.mean(base_physician_avg):.1f}, Caring: {np.mean(caring_physician_avg):.1f}")

            # Behavioral metrics averages
            positive_behaviors = ["pushback", "de-escalation", "safe_redirection", "suggestions_to_seek_help"]
            negative_behaviors = ["emotional_or_narrative_escalation", "sycophancy_or_praise",
                                "delusion_reinforcement", "consciousness_claims", "harmful_advice"]

            base_pos_avg = []
            caring_pos_avg = []
            base_neg_avg = []
            caring_neg_avg = []

            for model in common_models:
                base_metrics = self.base_results[model]["behavioral_metrics"]
                caring_metrics = self.caring_results[model]["behavioral_metrics"]

                if base_metrics and caring_metrics:
                    base_pos = sum(len(base_metrics.get(b, [])) for b in positive_behaviors)
                    caring_pos = sum(len(caring_metrics.get(b, [])) for b in positive_behaviors)
                    base_neg = sum(len(base_metrics.get(b, [])) for b in negative_behaviors)
                    caring_neg = sum(len(caring_metrics.get(b, [])) for b in negative_behaviors)

                    base_pos_avg.append(base_pos)
                    caring_pos_avg.append(caring_pos)
                    base_neg_avg.append(base_neg)
                    caring_neg_avg.append(caring_neg)

            if base_pos_avg:
                print("\nBehavioral Metrics (Average across models):")
                print(f"  Positive behaviors - Base: {np.mean(base_pos_avg):.1f}, Caring: {np.mean(caring_pos_avg):.1f}")
                print(f"  Negative behaviors - Base: {np.mean(base_neg_avg):.1f}, Caring: {np.mean(caring_neg_avg):.1f}")

        print("\n" + "="*70)

    def run_comparison(self) -> None:
        """Run complete comparison analysis."""
        print("="*70)
        print("PHYSICIAN SETTINGS COMPARISON")
        print("="*70)
        print(f"Base directory: {self.base_dir}")
        print(f"Caring directory: {self.caring_dir}")
        print(f"Output directory: {self.output_dir}")
        print("="*70)

        self.load_results()
        self.compare_word_counts()
        self.compare_behavioral_metrics()
        self.generate_summary_stats()

        print(f"\n✅ Comparison complete! Plots saved to: {self.output_dir}")


def main():
    """Run the comparison analysis."""
    comparator = PhysicianSettingsComparator(BASE_DIR, CARING_DIR, OUTPUT_DIR)
    comparator.run_comparison()


if __name__ == "__main__":
    main()

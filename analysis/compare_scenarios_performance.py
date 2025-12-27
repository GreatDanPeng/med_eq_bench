#!/usr/bin/env python3
"""
Multi-Scenario Performance Comparison

This script analyzes and visualizes physician model performance across all scenarios,
providing comprehensive comparison plots and statistics.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class MultiScenarioAnalyzer:
    """Analyze physician model performance across multiple scenarios."""

    def __init__(self, base_dir: str, output_dir: str = None):
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir) if output_dir else self.base_dir.parent / "scenario_analysis"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Data storage
        self.results = defaultdict(lambda: defaultdict(dict))  # {model: {scenario: data}}
        self.scenarios = []
        self.models = []

    def load_all_results(self) -> None:
        """Load results from all scenario directories."""
        print("Loading results from all scenarios...")

        # Find all scenario directories
        scenario_dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]

        for scenario_dir in scenario_dirs:
            scenario_name = scenario_dir.name
            self.scenarios.append(scenario_name)

            print(f"  Loading {scenario_name}...")

            # Load all JSON files in this scenario directory
            json_files = list(scenario_dir.glob("*.json"))

            for json_file in json_files:
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)

                    # Extract model name from filename
                    # Format: spiral_evaluation_{model_name}_{scenario}_{timestamp}.json
                    filename_parts = json_file.stem.split("_")
                    model_name = "unknown"

                    for i, part in enumerate(filename_parts):
                        if part == "evaluation" and i + 1 < len(filename_parts):
                            model_name = filename_parts[i + 1]
                            break

                    if model_name not in self.models:
                        self.models.append(model_name)

                    # Store data
                    self.results[model_name][scenario_name] = {
                        "quality_scores": data.get("quality_scores", {}),
                        "behavioral_metrics": data.get("behavioral_metrics", {}),
                        "word_count_stats": data.get("word_count_stats", {}),
                        "rounds_completed": data.get("rounds_completed", 0)
                    }

                except Exception as e:
                    print(f"    Error loading {json_file.name}: {e}")

        self.scenarios = sorted(list(set(self.scenarios)))
        self.models = sorted(list(set(self.models)))

        print(f"\n✅ Loaded data:")
        print(f"   Scenarios: {len(self.scenarios)}")
        print(f"   Models: {len(self.models)}")
        print(f"   Total evaluations: {sum(len(scenarios) for scenarios in self.results.values())}")

    def create_overall_score_heatmap(self) -> None:
        """Create heatmap showing overall scores across all models and scenarios."""
        print("\n📊 Generating overall score heatmap...")

        # Prepare data matrix
        data_matrix = []
        for model in self.models:
            row = []
            for scenario in self.scenarios:
                score = self.results[model][scenario].get("quality_scores", {}).get("overall_score", 0)
                row.append(score)
            data_matrix.append(row)

        # Create DataFrame
        df = pd.DataFrame(
            data_matrix,
            index=self.models,
            columns=[s.replace("_", " ").title()[:20] for s in self.scenarios]  # Shorten names
        )

        # Create heatmap
        plt.figure(figsize=(16, 10))
        sns.heatmap(df, annot=True, fmt='.1f', cmap='RdYlGn', center=50,
                   vmin=0, vmax=100, cbar_kws={'label': 'Overall Score'})
        plt.title('Overall Quality Scores Across All Scenarios', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Scenario', fontsize=12, fontweight='bold')
        plt.ylabel('Model', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()

        output_file = self.output_dir / "overall_scores_heatmap.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: {output_file}")

    def create_safety_quality_heatmaps(self) -> None:
        """Create separate heatmaps for safety and quality scores."""
        print("\n📊 Generating safety and quality score heatmaps...")

        # Prepare data matrices
        safety_matrix = []
        quality_matrix = []

        for model in self.models:
            safety_row = []
            quality_row = []
            for scenario in self.scenarios:
                scores = self.results[model][scenario].get("quality_scores", {})
                safety_row.append(scores.get("safety_score", 0))
                quality_row.append(scores.get("quality_score", 0))
            safety_matrix.append(safety_row)
            quality_matrix.append(quality_row)

        # Create DataFrames
        scenario_labels = [s.replace("_", " ").title()[:20] for s in self.scenarios]

        df_safety = pd.DataFrame(safety_matrix, index=self.models, columns=scenario_labels)
        df_quality = pd.DataFrame(quality_matrix, index=self.models, columns=scenario_labels)

        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 16))

        # Safety scores
        sns.heatmap(df_safety, annot=True, fmt='.1f', cmap='Blues', ax=ax1,
                   vmin=0, vmax=100, cbar_kws={'label': 'Safety Score'})
        ax1.set_title('Safety Scores Across All Scenarios', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Scenario', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Model', fontsize=11, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)

        # Quality scores
        sns.heatmap(df_quality, annot=True, fmt='.1f', cmap='Greens', ax=ax2,
                   vmin=0, vmax=100, cbar_kws={'label': 'Quality Score'})
        ax2.set_title('Quality Scores Across All Scenarios', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Scenario', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Model', fontsize=11, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        output_file = self.output_dir / "safety_quality_heatmaps.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: {output_file}")

    def create_model_ranking_plot(self) -> None:
        """Create bar plot showing average model performance across all scenarios."""
        print("\n📊 Generating model ranking plot...")

        # Calculate average scores
        model_averages = []
        for model in self.models:
            scores = []
            for scenario in self.scenarios:
                score = self.results[model][scenario].get("quality_scores", {}).get("overall_score", 0)
                if score > 0:  # Only include non-zero scores
                    scores.append(score)

            if scores:
                avg_score = np.mean(scores)
                std_score = np.std(scores)
                model_averages.append({
                    "model": model,
                    "avg": avg_score,
                    "std": std_score,
                    "n_scenarios": len(scores)
                })

        # Sort by average score
        model_averages = sorted(model_averages, key=lambda x: x["avg"], reverse=True)

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        models_sorted = [m["model"] for m in model_averages]
        averages = [m["avg"] for m in model_averages]
        stds = [m["std"] for m in model_averages]

        x_pos = np.arange(len(models_sorted))
        colors = plt.cm.RdYlGn(np.array(averages) / 100)  # Color by score

        bars = ax.bar(x_pos, averages, yerr=stds, capsize=5, color=colors,
                     alpha=0.8, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Overall Score', fontsize=12, fontweight='bold')
        ax.set_title('Model Performance Ranking (Average Across All Scenarios)',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(models_sorted, rotation=45, ha='right')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, axis='y')
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Midpoint (50)')

        # Add value labels on bars
        for i, (bar, avg, std) in enumerate(zip(bars, averages, stds)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std + 2,
                   f'{avg:.1f}±{std:.1f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax.legend()
        plt.tight_layout()

        output_file = self.output_dir / "model_ranking.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: {output_file}")

    def create_scenario_difficulty_plot(self) -> None:
        """Create plot showing which scenarios are most difficult (lowest scores)."""
        print("\n📊 Generating scenario difficulty plot...")

        # Calculate average scores per scenario
        scenario_averages = []
        for scenario in self.scenarios:
            scores = []
            for model in self.models:
                score = self.results[model][scenario].get("quality_scores", {}).get("overall_score", 0)
                if score > 0:
                    scores.append(score)

            if scores:
                avg_score = np.mean(scores)
                std_score = np.std(scores)
                scenario_averages.append({
                    "scenario": scenario.replace("_", " ").title(),
                    "avg": avg_score,
                    "std": std_score,
                    "n_models": len(scores)
                })

        # Sort by average score (ascending - hardest first)
        scenario_averages = sorted(scenario_averages, key=lambda x: x["avg"])

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        scenarios_sorted = [s["scenario"] for s in scenario_averages]
        averages = [s["avg"] for s in scenario_averages]
        stds = [s["std"] for s in scenario_averages]

        x_pos = np.arange(len(scenarios_sorted))
        colors = plt.cm.RdYlGn_r(np.array(averages) / 100)  # Red for hard, green for easy

        bars = ax.barh(x_pos, averages, xerr=stds, capsize=5, color=colors,
                      alpha=0.8, edgecolor='black', linewidth=1.5)

        ax.set_ylabel('Scenario', fontsize=12, fontweight='bold')
        ax.set_xlabel('Average Overall Score (All Models)', fontsize=12, fontweight='bold')
        ax.set_title('Scenario Difficulty Ranking (Lower Score = More Difficult)',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_yticks(x_pos)
        ax.set_yticklabels(scenarios_sorted)
        ax.set_xlim(0, 100)
        ax.grid(True, alpha=0.3, axis='x')
        ax.axvline(x=50, color='red', linestyle='--', alpha=0.5, label='Midpoint (50)')

        # Add value labels on bars
        for i, (bar, avg, std) in enumerate(zip(bars, averages, stds)):
            width = bar.get_width()
            ax.text(width + std + 2, bar.get_y() + bar.get_height()/2.,
                   f'{avg:.1f}±{std:.1f}',
                   ha='left', va='center', fontsize=9, fontweight='bold')

        ax.legend()
        plt.tight_layout()

        output_file = self.output_dir / "scenario_difficulty.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: {output_file}")

    def create_behavioral_comparison_plot(self) -> None:
        """Create plot comparing positive vs negative behaviors across scenarios."""
        print("\n📊 Generating behavioral metrics comparison...")

        positive_behaviors = ["pushback", "de-escalation", "safe_redirection", "suggestions_to_seek_help"]
        negative_behaviors = ["emotional_or_narrative_escalation", "sycophancy_or_praise",
                            "delusion_reinforcement", "consciousness_claims", "harmful_advice"]

        # Calculate averages per scenario
        scenario_data = []
        for scenario in self.scenarios:
            pos_counts = []
            neg_counts = []

            for model in self.models:
                metrics = self.results[model][scenario].get("behavioral_metrics", {})

                pos_count = sum(len(metrics.get(b, [])) for b in positive_behaviors)
                neg_count = sum(len(metrics.get(b, [])) for b in negative_behaviors)

                if pos_count > 0 or neg_count > 0:
                    pos_counts.append(pos_count)
                    neg_counts.append(neg_count)

            if pos_counts and neg_counts:
                scenario_data.append({
                    "scenario": scenario.replace("_", " ").title()[:25],
                    "positive_avg": np.mean(pos_counts),
                    "negative_avg": np.mean(neg_counts),
                    "positive_std": np.std(pos_counts),
                    "negative_std": np.std(neg_counts)
                })

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        scenarios_list = [s["scenario"] for s in scenario_data]
        pos_avgs = [s["positive_avg"] for s in scenario_data]
        neg_avgs = [s["negative_avg"] for s in scenario_data]

        x_pos = np.arange(len(scenarios_list))
        width = 0.35

        bars1 = ax.bar(x_pos - width/2, pos_avgs, width, label='Positive Behaviors',
                      color='#3cb44b', alpha=0.8, edgecolor='black')
        bars2 = ax.bar(x_pos + width/2, neg_avgs, width, label='Negative Behaviors',
                      color='#e6194B', alpha=0.8, edgecolor='black')

        ax.set_xlabel('Scenario', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Behavior Count (Across All Models)', fontsize=12, fontweight='bold')
        ax.set_title('Positive vs Negative Behaviors by Scenario',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenarios_list, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        output_file = self.output_dir / "behavioral_by_scenario.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: {output_file}")

    def create_consistency_plot(self) -> None:
        """Create plot showing model consistency (std dev) across scenarios."""
        print("\n📊 Generating model consistency plot...")

        # Calculate std dev for each model
        model_consistency = []
        for model in self.models:
            scores = []
            for scenario in self.scenarios:
                score = self.results[model][scenario].get("quality_scores", {}).get("overall_score", 0)
                if score > 0:
                    scores.append(score)

            if len(scores) >= 2:
                std = np.std(scores)
                mean = np.mean(scores)
                model_consistency.append({
                    "model": model,
                    "std": std,
                    "mean": mean,
                    "n_scenarios": len(scores)
                })

        # Sort by std (most consistent first)
        model_consistency = sorted(model_consistency, key=lambda x: x["std"])

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        models_sorted = [m["model"] for m in model_consistency]
        stds = [m["std"] for m in model_consistency]
        means = [m["mean"] for m in model_consistency]

        x_pos = np.arange(len(models_sorted))
        colors = plt.cm.RdYlGn_r(np.array(stds) / max(stds))  # Green for consistent

        bars = ax.bar(x_pos, stds, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax.set_ylabel('Standard Deviation of Scores', fontsize=12, fontweight='bold')
        ax.set_title('Model Consistency Across Scenarios (Lower = More Consistent)',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(models_sorted, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for i, (bar, std, mean) in enumerate(zip(bars, stds, means)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{std:.1f}\n(μ={mean:.1f})',
                   ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        output_file = self.output_dir / "model_consistency.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: {output_file}")

    def generate_summary_report(self) -> None:
        """Generate text summary report."""
        print("\n📄 Generating summary report...")

        report_lines = []
        report_lines.append("="*80)
        report_lines.append("MULTI-SCENARIO PERFORMANCE ANALYSIS REPORT")
        report_lines.append("="*80)
        report_lines.append("")

        # Overview
        report_lines.append(f"Total Scenarios Analyzed: {len(self.scenarios)}")
        report_lines.append(f"Total Models Evaluated: {len(self.models)}")
        report_lines.append(f"Total Evaluations: {sum(len(scenarios) for scenarios in self.results.values())}")
        report_lines.append("")

        # Top performing models
        report_lines.append("-"*80)
        report_lines.append("TOP PERFORMING MODELS (By Average Overall Score)")
        report_lines.append("-"*80)

        model_avgs = []
        for model in self.models:
            scores = [self.results[model][s].get("quality_scores", {}).get("overall_score", 0)
                     for s in self.scenarios if self.results[model][s].get("quality_scores", {}).get("overall_score", 0) > 0]
            if scores:
                model_avgs.append((model, np.mean(scores), np.std(scores)))

        model_avgs.sort(key=lambda x: x[1], reverse=True)

        for i, (model, avg, std) in enumerate(model_avgs[:10], 1):
            report_lines.append(f"{i:2d}. {model:30s} - Avg: {avg:5.2f} ± {std:5.2f}")

        report_lines.append("")

        # Most difficult scenarios
        report_lines.append("-"*80)
        report_lines.append("MOST DIFFICULT SCENARIOS (Lowest Average Scores)")
        report_lines.append("-"*80)

        scenario_avgs = []
        for scenario in self.scenarios:
            scores = [self.results[m][scenario].get("quality_scores", {}).get("overall_score", 0)
                     for m in self.models if self.results[m][scenario].get("quality_scores", {}).get("overall_score", 0) > 0]
            if scores:
                scenario_avgs.append((scenario, np.mean(scores), np.std(scores)))

        scenario_avgs.sort(key=lambda x: x[1])

        for i, (scenario, avg, std) in enumerate(scenario_avgs, 1):
            report_lines.append(f"{i:2d}. {scenario:40s} - Avg: {avg:5.2f} ± {std:5.2f}")

        report_lines.append("")
        report_lines.append("="*80)

        # Save report
        report_text = "\n".join(report_lines)
        report_file = self.output_dir / "performance_summary.txt"
        with open(report_file, 'w') as f:
            f.write(report_text)

        print(report_text)
        print(f"\n   Saved: {report_file}")

    def run_complete_analysis(self) -> None:
        """Run all analysis and generate all plots."""
        print("="*80)
        print("MULTI-SCENARIO PERFORMANCE ANALYSIS")
        print("="*80)
        print(f"Input directory: {self.base_dir}")
        print(f"Output directory: {self.output_dir}")
        print("="*80)

        self.load_all_results()

        if not self.results:
            print("\n❌ No results found!")
            return

        self.create_overall_score_heatmap()
        self.create_safety_quality_heatmaps()
        self.create_model_ranking_plot()
        self.create_scenario_difficulty_plot()
        self.create_behavioral_comparison_plot()
        self.create_consistency_plot()
        self.generate_summary_report()

        print(f"\n{'='*80}")
        print(f"✅ Analysis complete! All outputs saved to:")
        print(f"   {self.output_dir}")
        print(f"{'='*80}\n")


def main():
    """Run the complete multi-scenario analysis."""
    base_dir = "/Users/danpengair/med_eq_bench/results/physcians/gemini-2.5-flash_physicians/merge_eval/base_physicians"

    analyzer = MultiScenarioAnalyzer(base_dir)
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()

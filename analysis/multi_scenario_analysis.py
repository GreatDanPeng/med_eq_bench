#!/usr/bin/env python3
"""
Multi-Scenario Performance Analysis

This script analyzes and visualizes physician model performance across all 9 scenarios,
providing comprehensive comparison plots and statistics.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set up plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class MultiScenarioAnalyzer:
    """Analyze physician model performance across multiple scenarios."""

    def __init__(self, base_dir: str, output_dir: Optional[str] = None):
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir) if output_dir else self.base_dir / "scenario_analysis"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Data storage: {model: {scenario: data}}
        self.results = defaultdict(lambda: defaultdict(dict))
        self.scenarios = []
        self.models = set()

    def load_all_results(self) -> None:
        """Load results from all scenario directories."""
        print("Loading results from all scenarios...")

        # Find all scenario directories
        scenario_dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]

        for scenario_dir in scenario_dirs:
            scenario_name = scenario_dir.name

            # Skip the output directory itself
            if scenario_name == "scenario_analysis":
                continue

            if scenario_name not in self.scenarios:
                self.scenarios.append(scenario_name)

            print(f"  Loading {scenario_name}...")

            # Load all JSON files in this scenario directory
            json_files = list(scenario_dir.glob("spiral_evaluation_*.json"))

            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Extract model name from filename
                    # Format: spiral_evaluation_{model}_{scenario}_{timestamp}.json
                    filename = json_file.stem
                    parts = filename.split('_')
                    # Find model name between "evaluation" and scenario_name
                    model_start_idx = 2  # After "spiral_evaluation"
                    model_parts = []
                    for i in range(model_start_idx, len(parts)):
                        if '_'.join(parts[i:]).startswith(scenario_name):
                            break
                        model_parts.append(parts[i])

                    model_name = '_'.join(model_parts) if model_parts else "unknown"
                    self.models.add(model_name)

                    # Extract key metrics
                    quality_scores = data.get('quality_scores', {})
                    self.results[model_name][scenario_name] = {
                        'overall_score': quality_scores.get('overall_score', 0),
                        'safety_score': quality_scores.get('safety_score', 0),
                        'quality_score': quality_scores.get('quality_score', 0),
                        'positive_behavior_count': quality_scores.get('positive_behavior_count', 0),
                        'negative_behavior_count': quality_scores.get('negative_behavior_count', 0),
                        'patient_avg_words': data.get('word_count_stats', {}).get('patient_avg_words_per_round', 0),
                        'physician_avg_words': data.get('word_count_stats', {}).get('physician_avg_words_per_round', 0),
                        'conversation_id': data.get('conversation_id', ''),
                    }

                except Exception as e:
                    print(f"    Error loading {json_file.name}: {e}")

        self.models = sorted(list(self.models))
        self.scenarios = sorted(self.scenarios)
        print(f"\nLoaded data for {len(self.models)} models across {len(self.scenarios)} scenarios")

    def create_overall_score_heatmap(self) -> None:
        """Create heatmap of overall scores across models and scenarios."""
        print("\nCreating overall score heatmap...")

        # Create matrix for heatmap
        score_matrix = []
        for model in self.models:
            row = []
            for scenario in self.scenarios:
                score = self.results[model][scenario].get('overall_score', 0)
                row.append(score)
            score_matrix.append(row)

        # Create DataFrame
        df = pd.DataFrame(score_matrix, index=self.models, columns=self.scenarios)

        # Create plot
        fig, ax = plt.subplots(figsize=(16, 10))
        sns.heatmap(df, annot=True, fmt='.1f', cmap='RdYlGn', center=50,
                    vmin=0, vmax=100, cbar_kws={'label': 'Overall Score'},
                    linewidths=0.5, ax=ax)

        # Rotate scenario labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

        plt.title('Model Performance Across Scenarios (Overall Score)', fontsize=16, pad=20)
        plt.xlabel('Scenario', fontsize=12)
        plt.ylabel('Model', fontsize=12)
        plt.tight_layout()

        output_path = self.output_dir / 'overall_scores_heatmap.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved to {output_path}")

    def create_safety_quality_heatmaps(self) -> None:
        """Create side-by-side heatmaps for safety and quality scores."""
        print("\nCreating safety and quality heatmaps...")

        # Create matrices
        safety_matrix = []
        quality_matrix = []
        for model in self.models:
            safety_row = []
            quality_row = []
            for scenario in self.scenarios:
                safety_row.append(self.results[model][scenario].get('safety_score', 0))
                quality_row.append(self.results[model][scenario].get('quality_score', 0))
            safety_matrix.append(safety_row)
            quality_matrix.append(quality_row)

        # Create DataFrames
        df_safety = pd.DataFrame(safety_matrix, index=self.models, columns=self.scenarios)
        df_quality = pd.DataFrame(quality_matrix, index=self.models, columns=self.scenarios)

        # Create plot with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

        # Safety score heatmap
        sns.heatmap(df_safety, annot=True, fmt='.1f', cmap='Blues',
                    vmin=0, vmax=100, cbar_kws={'label': 'Safety Score'},
                    linewidths=0.5, ax=ax1)
        ax1.set_title('Safety Scores', fontsize=14, pad=15)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
        ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0)
        ax1.set_xlabel('Scenario', fontsize=11)
        ax1.set_ylabel('Model', fontsize=11)

        # Quality score heatmap
        sns.heatmap(df_quality, annot=True, fmt='.1f', cmap='Greens',
                    vmin=0, vmax=100, cbar_kws={'label': 'Quality Score'},
                    linewidths=0.5, ax=ax2)
        ax2.set_title('Quality Scores', fontsize=14, pad=15)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
        ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0)
        ax2.set_xlabel('Scenario', fontsize=11)
        ax2.set_ylabel('Model', fontsize=11)

        plt.tight_layout()

        output_path = self.output_dir / 'safety_quality_heatmaps.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved to {output_path}")

    def create_model_ranking_plot(self) -> None:
        """Create bar plot showing average model performance with error bars (top to bottom)."""
        print("\nCreating model ranking plot...")

        # Calculate average scores and std dev for each model
        model_stats = {}
        for model in self.models:
            scores = [self.results[model][scenario].get('overall_score', 0)
                     for scenario in self.scenarios]
            model_stats[model] = {
                'mean': np.mean(scores),
                'std': np.std(scores)
            }

        # Sort by mean score (highest to lowest, will be reversed for top-down display)
        sorted_models = sorted(model_stats.items(), key=lambda x: x[1]['mean'], reverse=False)
        models_sorted = [m[0] for m in sorted_models]
        means = [m[1]['mean'] for m in sorted_models]
        stds = [m[1]['std'] for m in sorted_models]

        # Create plot with white background
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        # Use light green color for all bars
        light_green = '#90EE90'  # Light green color

        bars = ax.barh(models_sorted, means, xerr=stds, color=light_green,
                       edgecolor='darkgreen', linewidth=0.8, capsize=5, alpha=0.9)

        ax.set_xlabel('Average Overall Score (±1 Std Dev)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Model', fontsize=12, fontweight='bold')
        ax.set_title('Model Performance Ranking (Averaged Across All Scenarios)',
                    fontsize=14, pad=15, fontweight='bold')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (mean, std) in enumerate(zip(means, stds)):
            ax.text(mean + std + 2, i, f'{mean:.1f}', va='center', fontsize=9, fontweight='bold')

        plt.tight_layout()

        output_path = self.output_dir / 'model_ranking.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  Saved to {output_path}")

    def create_scenario_difficulty_plot(self) -> None:
        """Create plot showing which scenarios are most difficult."""
        print("\nCreating scenario difficulty plot...")

        # Calculate average scores for each scenario
        scenario_stats = {}
        for scenario in self.scenarios:
            scores = [self.results[model][scenario].get('overall_score', 0)
                     for model in self.models]
            scenario_stats[scenario] = {
                'mean': np.mean(scores),
                'std': np.std(scores)
            }

        # Sort by mean score (lower = more difficult)
        sorted_scenarios = sorted(scenario_stats.items(), key=lambda x: x[1]['mean'])
        scenarios_sorted = [s[0] for s in sorted_scenarios]
        means = [s[1]['mean'] for s in sorted_scenarios]
        stds = [s[1]['std'] for s in sorted_scenarios]

        # Create plot with white background
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        # Color bars by difficulty (lower score = more difficult = redder)
        colors = plt.cm.RdYlGn([m/100 for m in means])

        bars = ax.barh(scenarios_sorted, means, xerr=stds, color=colors,
                       edgecolor='black', linewidth=0.8, capsize=5)

        ax.set_xlabel('Average Overall Score (±1 Std Dev)', fontsize=12)
        ax.set_ylabel('Scenario', fontsize=12)
        ax.set_title('Scenario Difficulty (Lower Score = More Difficult)', fontsize=14, pad=15)
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (mean, std) in enumerate(zip(means, stds)):
            ax.text(mean + std + 2, i, f'{mean:.1f}', va='center', fontsize=9)

        plt.tight_layout()

        output_path = self.output_dir / 'scenario_difficulty.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  Saved to {output_path}")

    def create_behavioral_comparison_by_scenario(self) -> None:
        """Create grouped bar chart comparing positive vs negative behaviors by scenario."""
        print("\nCreating behavioral comparison by scenario...")

        # Calculate average positive and negative behaviors for each scenario
        scenario_behaviors = {}
        for scenario in self.scenarios:
            pos_counts = [self.results[model][scenario].get('positive_behavior_count', 0)
                         for model in self.models]
            neg_counts = [self.results[model][scenario].get('negative_behavior_count', 0)
                         for model in self.models]
            scenario_behaviors[scenario] = {
                'positive': np.mean(pos_counts),
                'negative': np.mean(neg_counts)
            }

        # Sort scenarios by positive - negative difference
        sorted_scenarios = sorted(scenario_behaviors.items(),
                                 key=lambda x: x[1]['positive'] - x[1]['negative'],
                                 reverse=True)

        scenarios_sorted = [s[0] for s in sorted_scenarios]
        positive_means = [s[1]['positive'] for s in sorted_scenarios]
        negative_means = [s[1]['negative'] for s in sorted_scenarios]

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        x = np.arange(len(scenarios_sorted))
        width = 0.35

        bars1 = ax.bar(x - width/2, positive_means, width, label='Positive Behaviors',
                      color='skyblue', edgecolor='black', linewidth=0.8)
        bars2 = ax.bar(x + width/2, negative_means, width, label='Negative Behaviors',
                      color='lightcoral', edgecolor='black', linewidth=0.8)

        ax.set_xlabel('Scenario', fontsize=12)
        ax.set_ylabel('Average Behavior Count', fontsize=12)
        ax.set_title('Positive vs Negative Behaviors by Scenario (Averaged Across All Models)',
                    fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios_sorted, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()

        output_path = self.output_dir / 'behavioral_by_scenario.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved to {output_path}")

    def create_model_consistency_plot(self) -> None:
        """Create plot showing model consistency (std dev) across scenarios."""
        print("\nCreating model consistency plot...")

        # Calculate std dev for each model across scenarios
        model_consistency = {}
        for model in self.models:
            scores = [self.results[model][scenario].get('overall_score', 0)
                     for scenario in self.scenarios]
            model_consistency[model] = {
                'mean': np.mean(scores),
                'std': np.std(scores)
            }

        # Sort by std dev (lower = more consistent)
        sorted_models = sorted(model_consistency.items(), key=lambda x: x[1]['std'])
        models_sorted = [m[0] for m in sorted_models]
        stds = [m[1]['std'] for m in sorted_models]
        means = [m[1]['mean'] for m in sorted_models]

        # Create plot with white background
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        # Color bars by std dev (lower = better = greener, higher = worse = redder)
        max_std = max(stds) if stds else 1
        colors = plt.cm.RdYlGn_r([s/max_std for s in stds])

        bars = ax.barh(models_sorted, stds, color=colors,
                      edgecolor='black', linewidth=0.8, alpha=0.9)

        ax.set_xlabel('Standard Deviation of Overall Score', fontsize=12, fontweight='bold')
        ax.set_ylabel('Model', fontsize=12, fontweight='bold')
        ax.set_title('Model Consistency Across Scenarios (Lower = More Consistent)',
                    fontsize=14, pad=15, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        # Add value labels with mean score
        for i, (std, mean) in enumerate(zip(stds, means)):
            ax.text(std + 0.5, i, f'{std:.1f} (μ={mean:.1f})',
                   va='center', fontsize=9, fontweight='bold')

        plt.tight_layout()

        output_path = self.output_dir / 'model_consistency.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  Saved to {output_path}")

    def combine_ranking_and_consistency(self) -> None:
        """Combine model_ranking and model_consistency images side by side."""
        print("\nCombining ranking and consistency plots...")

        try:
            from PIL import Image

            ranking_path = self.output_dir / 'model_ranking.png'
            consistency_path = self.output_dir / 'model_consistency.png'

            if not ranking_path.exists() or not consistency_path.exists():
                print("  Error: Source images not found. Skipping combination.")
                return

            # Load images
            img_ranking = Image.open(ranking_path)
            img_consistency = Image.open(consistency_path)

            # Get dimensions
            width1, height1 = img_ranking.size
            width2, height2 = img_consistency.size

            # Use maximum height and sum of widths
            combined_width = width1 + width2
            combined_height = max(height1, height2)

            # Create new image with transparent background
            combined_img = Image.new('RGBA', (combined_width, combined_height), (255, 255, 255, 0))

            # Paste images side by side (ranking left, consistency right)
            combined_img.paste(img_ranking, (0, 0))
            combined_img.paste(img_consistency, (width1, 0))

            # Save combined image
            output_path = self.output_dir / 'ranking_and_consistency_combined.png'
            combined_img.save(output_path, dpi=(300, 300))
            print(f"  Saved combined image to {output_path}")

        except ImportError:
            print("  Warning: PIL/Pillow not installed. Cannot combine images.")
            print("  Install with: pip install Pillow")
        except Exception as e:
            print(f"  Error combining images: {e}")

    def create_word_count_comparison(self) -> None:
        """Create plot comparing average word counts across models and scenarios."""
        print("\nCreating word count comparison plot...")

        # Calculate average word counts for each model
        model_word_counts = {}
        for model in self.models:
            patient_words = []
            physician_words = []
            for scenario in self.scenarios:
                patient_words.append(self.results[model][scenario].get('patient_avg_words', 0))
                physician_words.append(self.results[model][scenario].get('physician_avg_words', 0))

            model_word_counts[model] = {
                'patient': np.mean(patient_words),
                'physician': np.mean(physician_words)
            }

        # Sort by physician word count
        sorted_models = sorted(model_word_counts.items(),
                              key=lambda x: x[1]['physician'])
        models_sorted = [m[0] for m in sorted_models]
        patient_means = [m[1]['patient'] for m in sorted_models]
        physician_means = [m[1]['physician'] for m in sorted_models]

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        x = np.arange(len(models_sorted))
        width = 0.35

        bars1 = ax.bar(x - width/2, patient_means, width, label='Patient Avg Words',
                      color='skyblue', edgecolor='black', linewidth=0.8)
        bars2 = ax.bar(x + width/2, physician_means, width, label='Physician Avg Words',
                      color='lightcoral', edgecolor='black', linewidth=0.8)

        ax.set_xlabel('Model', fontsize=12)
        ax.set_ylabel('Average Words per Round', fontsize=12)
        ax.set_title('Average Word Count per Round (Across All Scenarios)',
                    fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(models_sorted, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=7)

        plt.tight_layout()

        output_path = self.output_dir / 'word_count_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved to {output_path}")

    def generate_summary_report(self) -> None:
        """Generate text summary report of key findings."""
        print("\nGenerating summary report...")

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("MULTI-SCENARIO PERFORMANCE ANALYSIS SUMMARY")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Overall statistics
        report_lines.append(f"Total Models Analyzed: {len(self.models)}")
        report_lines.append(f"Total Scenarios Analyzed: {len(self.scenarios)}")
        report_lines.append("")

        # Top performing models
        report_lines.append("-" * 80)
        report_lines.append("TOP 5 MODELS (by average overall score across all scenarios)")
        report_lines.append("-" * 80)

        model_avgs = {}
        for model in self.models:
            scores = [self.results[model][scenario].get('overall_score', 0)
                     for scenario in self.scenarios]
            model_avgs[model] = np.mean(scores)

        top_models = sorted(model_avgs.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (model, score) in enumerate(top_models, 1):
            report_lines.append(f"{i}. {model}: {score:.2f}")
        report_lines.append("")

        # Most difficult scenarios
        report_lines.append("-" * 80)
        report_lines.append("MOST DIFFICULT SCENARIOS (lowest average overall score)")
        report_lines.append("-" * 80)

        scenario_avgs = {}
        for scenario in self.scenarios:
            scores = [self.results[model][scenario].get('overall_score', 0)
                     for model in self.models]
            scenario_avgs[scenario] = np.mean(scores)

        difficult_scenarios = sorted(scenario_avgs.items(), key=lambda x: x[1])[:5]
        for i, (scenario, score) in enumerate(difficult_scenarios, 1):
            report_lines.append(f"{i}. {scenario}: {score:.2f}")
        report_lines.append("")

        # Most consistent models
        report_lines.append("-" * 80)
        report_lines.append("MOST CONSISTENT MODELS (lowest std dev across scenarios)")
        report_lines.append("-" * 80)

        model_consistency = {}
        for model in self.models:
            scores = [self.results[model][scenario].get('overall_score', 0)
                     for scenario in self.scenarios]
            model_consistency[model] = np.std(scores)

        consistent_models = sorted(model_consistency.items(), key=lambda x: x[1])[:5]
        for i, (model, std) in enumerate(consistent_models, 1):
            report_lines.append(f"{i}. {model}: {std:.2f} std dev")
        report_lines.append("")

        # Best safety scores
        report_lines.append("-" * 80)
        report_lines.append("BEST SAFETY SCORES (highest average across scenarios)")
        report_lines.append("-" * 80)

        model_safety = {}
        for model in self.models:
            scores = [self.results[model][scenario].get('safety_score', 0)
                     for scenario in self.scenarios]
            model_safety[model] = np.mean(scores)

        safe_models = sorted(model_safety.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (model, score) in enumerate(safe_models, 1):
            report_lines.append(f"{i}. {model}: {score:.2f}")
        report_lines.append("")

        # Best quality scores
        report_lines.append("-" * 80)
        report_lines.append("BEST QUALITY SCORES (highest average across scenarios)")
        report_lines.append("-" * 80)

        model_quality = {}
        for model in self.models:
            scores = [self.results[model][scenario].get('quality_score', 0)
                     for scenario in self.scenarios]
            model_quality[model] = np.mean(scores)

        quality_models = sorted(model_quality.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (model, score) in enumerate(quality_models, 1):
            report_lines.append(f"{i}. {model}: {score:.2f}")
        report_lines.append("")

        # Most verbose models
        report_lines.append("-" * 80)
        report_lines.append("MOST VERBOSE PHYSICIAN MODELS (highest avg words per round)")
        report_lines.append("-" * 80)

        model_verbosity = {}
        for model in self.models:
            words = [self.results[model][scenario].get('physician_avg_words', 0)
                    for scenario in self.scenarios]
            model_verbosity[model] = np.mean(words)

        verbose_models = sorted(model_verbosity.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (model, words) in enumerate(verbose_models, 1):
            report_lines.append(f"{i}. {model}: {words:.1f} words/round")
        report_lines.append("")

        report_lines.append("=" * 80)

        # Write to file
        report_text = '\n'.join(report_lines)
        output_path = self.output_dir / 'performance_summary.txt'
        with open(output_path, 'w') as f:
            f.write(report_text)

        print(f"  Saved to {output_path}")
        print("\n" + report_text)

    def run_complete_analysis(self) -> None:
        """Run all analysis and generate all plots."""
        print("\n" + "="*80)
        print("MULTI-SCENARIO PERFORMANCE ANALYSIS")
        print("="*80)

        self.load_all_results()

        if not self.results:
            print("Error: No results loaded. Please check the directory structure.")
            return

        self.create_overall_score_heatmap()
        self.create_safety_quality_heatmaps()
        self.create_model_ranking_plot()
        self.create_scenario_difficulty_plot()
        self.create_behavioral_comparison_by_scenario()
        self.create_model_consistency_plot()
        self.combine_ranking_and_consistency()
        self.create_word_count_comparison()
        self.generate_summary_report()

        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print(f"All visualizations saved to: {self.output_dir}")
        print("="*80)


def main():
    """Main execution function."""
    # Default paths
    base_dir = "/Users/danpengair/med_eq_bench/results/physcians/gemini-2.5-flash_physicians/merge_eval/base_physicians"

    # Check if base directory exists
    if not os.path.exists(base_dir):
        print(f"Error: Base directory not found: {base_dir}")
        print("Please update the base_dir path in the script.")
        return

    # Create analyzer and run
    analyzer = MultiScenarioAnalyzer(base_dir)
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()

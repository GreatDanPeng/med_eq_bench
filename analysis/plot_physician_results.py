#!/usr/bin/env python3
"""
Physician Results Analysis and Plotting

This script analyzes all physician evaluation results and creates streamlined
visualizations: radar chart, heatmap, and combined behavioral analysis.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Constants
SAFETY_SCORE = 'Safety Score'
QUALITY_SCORE = 'Quality Score'
OVERALL_SCORE = 'Overall Score'
POSITIVE_BEHAVIORS = 'Positive Behaviors'
NEGATIVE_BEHAVIORS = 'Negative Behaviors'

@dataclass
class ModelResult:
    """Data structure for a single model evaluation result."""
    model_name: str
    scenario: str
    timestamp: datetime
    quality_scores: Dict[str, float]
    behavioral_metrics: Dict[str, List[List]]
    rounds_completed: int
    evaluation_model: str
    filename: str
    word_count_stats: Optional[Dict[str, float]] = None

class PhysicianResultsAnalyzer:
    """Analyzer for physician evaluation results."""

    def __init__(self, results_dir: str = "/Users/danpengair/med_eq_bench/results/physcians/gemini-2.5-flash_physicians/merge_eval/base_physicians/time_pressure_consultation"):
        self.results_dir = Path(results_dir)
        self.results: List[ModelResult] = []
        self.behavioral_categories = [
            "pushback", "de-escalation", "safe_redirection", "suggestions_to_seek_help",
            "emotional_or_narrative_escalation", "sycophancy_or_praise",
            "delusion_reinforcement", "consciousness_claims", "harmful_advice"
        ]

    def load_results(self) -> None:
        """Load all JSON result files from the results directory."""
        if not self.results_dir.exists():
            print(f"Results directory not found: {self.results_dir}")
            return

        json_files = list(self.results_dir.glob("spiral_evaluation_*.json"))
        print(f"Found {len(json_files)} result files")

        for json_file in json_files:
            try:
                # Extract model name from filename
                # Format: spiral_evaluation_{model_name}_{scenario}_{timestamp}.json
                filename_parts = json_file.stem.split("_")
                if len(filename_parts) >= 4:
                    model_name = filename_parts[2]  # Extract model name
                    scenario = filename_parts[3]   # Extract scenario
                else:
                    model_name = "unknown"
                    scenario = "unknown"

                with open(json_file, 'r') as f:
                    data = json.load(f)

                # Parse timestamp
                try:
                    timestamp = datetime.strptime(data.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    timestamp = datetime.now()

                result = ModelResult(
                    model_name=model_name,
                    scenario=scenario,
                    timestamp=timestamp,
                    quality_scores=data.get("quality_scores", {}),
                    behavioral_metrics=data.get("behavioral_metrics", {}),
                    rounds_completed=data.get("rounds_completed", 0),
                    evaluation_model=data.get("evaluation_model", "unknown"),
                    filename=json_file.name,
                    word_count_stats=data.get("word_count_stats", None)
                )

                self.results.append(result)
                print(f"Loaded: {model_name} - {scenario}")

            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        print(f"Successfully loaded {len(self.results)} results")

    def create_radar_chart(self) -> None:
        """Create radar chart showing quality scores across models with distinct colors."""
        if not self.results:
            return

        # Prepare data
        models = []
        safety_scores = []
        quality_scores = []
        overall_scores = []

        for result in self.results:
            models.append(result.model_name)
            safety_scores.append(result.quality_scores.get("safety_score", 0))
            quality_scores.append(result.quality_scores.get("quality_score", 0))
            overall_scores.append(result.quality_scores.get("overall_score", 0))

        # Create DataFrame
        df = pd.DataFrame({
            'Model': models,
            SAFETY_SCORE: safety_scores,
            QUALITY_SCORE: quality_scores,
            OVERALL_SCORE: overall_scores
        })

        # Define distinct colors for up to 20 models
        distinct_colors = [
            '#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
            '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4',
            '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000',
            '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9'
        ]

        # Radar plot
        score_types = [SAFETY_SCORE, QUALITY_SCORE, OVERALL_SCORE]
        angles = np.linspace(0, 2 * np.pi, len(score_types), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        plt.figure(figsize=(12, 10))
        ax = plt.subplot(111, projection='polar')

        for idx, (_, row) in enumerate(df.iterrows()):
            values = [row[SAFETY_SCORE], row[QUALITY_SCORE], row[OVERALL_SCORE]]
            values += values[:1]  # Complete the circle

            color = distinct_colors[idx % len(distinct_colors)]
            ax.plot(angles, values, 'o-', linewidth=2.5, label=row['Model'],
                   color=color, markersize=8)
            ax.fill(angles, values, alpha=0.15, color=color)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(score_types, fontsize=12, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.set_title('Quality Scores Radar Chart', fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.results_dir / "radar_chart.png", dpi=300, bbox_inches='tight')
        plt.close()

    def create_behavioral_metrics_heatmap(self) -> None:
        """Create heatmap showing behavioral metrics across models with separate colors for positive/negative."""
        if not self.results:
            return

        # Define positive and negative behaviors
        positive_behaviors = ["pushback", "de-escalation", "safe_redirection", "suggestions_to_seek_help"]
        negative_behaviors = ["emotional_or_narrative_escalation", "sycophancy_or_praise",
                            "delusion_reinforcement", "consciousness_claims", "harmful_advice"]

        # Prepare data for heatmap - separate positive and negative
        model_names = []
        positive_data = []
        negative_data = []

        for result in self.results:
            model_names.append(result.model_name)

            # Positive behaviors
            pos_counts = []
            for behavior in positive_behaviors:
                count = len(result.behavioral_metrics.get(behavior, []))
                pos_counts.append(count)
            positive_data.append(pos_counts)

            # Negative behaviors
            neg_counts = []
            for behavior in negative_behaviors:
                count = len(result.behavioral_metrics.get(behavior, []))
                neg_counts.append(count)
            negative_data.append(neg_counts)

        # Create DataFrames
        df_positive = pd.DataFrame(
            positive_data,
            index=model_names,
            columns=[behavior.replace("_", " ").title() for behavior in positive_behaviors]
        )

        df_negative = pd.DataFrame(
            negative_data,
            index=model_names,
            columns=[behavior.replace("_", " ").title() for behavior in negative_behaviors]
        )

        # Create figure with two subplots side by side
        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

        # Positive behaviors heatmap (cold colors - Blues)
        sns.heatmap(df_positive, annot=True, cmap='Blues', fmt='d',
                   cbar_kws={'label': 'Instance Count'}, ax=ax1)
        ax1.set_title('Positive Behaviors', fontsize=14, fontweight='bold')
        ax1.set_xlabel('', fontsize=11)
        ax1.set_ylabel('Model', fontsize=11)
        ax1.tick_params(axis='x', rotation=45)

        # Negative behaviors heatmap (warm colors - Reds)
        sns.heatmap(df_negative, annot=True, cmap='Reds', fmt='d',
                   cbar_kws={'label': 'Instance Count'}, ax=ax2)
        ax2.set_title('Negative Behaviors', fontsize=14, fontweight='bold')
        ax2.set_xlabel('', fontsize=11)
        ax2.set_ylabel('Model', fontsize=11)
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig(self.results_dir / "behavioral_metrics_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()

    def create_combined_behavioral_analysis(self) -> None:
        """Create combined plot showing positive and negative behaviors."""
        if not self.results:
            return

        # Positive and negative behavior categories
        positive_behaviors = ["pushback", "de-escalation", "safe_redirection", "suggestions_to_seek_help"]
        negative_behaviors = ["emotional_or_narrative_escalation", "sycophancy_or_praise",
                            "delusion_reinforcement", "consciousness_claims", "harmful_advice"]

        # Prepare data
        models = [result.model_name for result in self.results]
        positive_counts = []
        negative_counts = []

        for result in self.results:
            pos_count = sum(len(result.behavioral_metrics.get(behavior, [])) for behavior in positive_behaviors)
            neg_count = sum(len(result.behavioral_metrics.get(behavior, [])) for behavior in negative_behaviors)
            positive_counts.append(pos_count)
            negative_counts.append(neg_count)

        # Create combined bar plot
        plt.figure(figsize=(12, 8))
        x_pos = np.arange(len(models))
        width = 0.35

        plt.bar(x_pos - width/2, positive_counts, width, label=POSITIVE_BEHAVIORS,
                color='green', alpha=0.7)
        plt.bar(x_pos + width/2, negative_counts, width, label=NEGATIVE_BEHAVIORS,
                color='red', alpha=0.7)

        plt.xlabel('Model')
        plt.ylabel('Behavior Count')
        plt.title('Positive vs Negative Behaviors by Model')
        plt.xticks(x_pos, models, rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Add value labels on bars
        for i, (pos, neg) in enumerate(zip(positive_counts, negative_counts)):
            plt.text(i - width/2, pos + 0.5, str(pos), ha='center', va='bottom')
            plt.text(i + width/2, neg + 0.5, str(neg), ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(self.results_dir / "combined_behaviors.png", dpi=300, bbox_inches='tight')
        plt.close()

    def create_word_count_bar_plots(self) -> None:
        """Create bar plots for patient and physician average words per round."""
        if not self.results:
            return

        # Filter results that have word_count_stats
        results_with_stats = [r for r in self.results if r.word_count_stats is not None]

        if not results_with_stats:
            print("No word count statistics found in results")
            return

        # Prepare data
        models = []
        patient_avg_words = []
        physician_avg_words = []

        for result in results_with_stats:
            models.append(result.model_name)
            patient_avg_words.append(result.word_count_stats.get("patient_avg_words_per_round", 0))
            physician_avg_words.append(result.word_count_stats.get("physician_avg_words_per_round", 0))

        # Sort by patient average words (low to high)
        sorted_indices = np.argsort(patient_avg_words)
        models_sorted_patient = [models[i] for i in sorted_indices]
        patient_sorted = [patient_avg_words[i] for i in sorted_indices]

        # Sort by physician average words (low to high)
        sorted_indices = np.argsort(physician_avg_words)
        models_sorted_physician = [models[i] for i in sorted_indices]
        physician_sorted = [physician_avg_words[i] for i in sorted_indices]

        # Create figure with two subplots
        _, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

        # Plot 1: Patient Average Words per Round
        x_pos = np.arange(len(models_sorted_patient))
        bars1 = ax1.bar(x_pos, patient_sorted, color='skyblue', alpha=0.8, edgecolor='navy')
        ax1.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Average Words per Round', fontsize=12, fontweight='bold')
        ax1.set_title('Patient Average Words per Round (Low to High)', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(models_sorted_patient, rotation=45, ha='right')
        ax1.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for bar, value in zip(bars1, patient_sorted):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1f}',
                    ha='center', va='bottom', fontsize=9)

        # Plot 2: Physician Average Words per Round
        x_pos = np.arange(len(models_sorted_physician))
        bars2 = ax2.bar(x_pos, physician_sorted, color='lightcoral', alpha=0.8, edgecolor='darkred')
        ax2.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Average Words per Round', fontsize=12, fontweight='bold')
        ax2.set_title('Physician Average Words per Round (Low to High)', fontsize=14, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(models_sorted_physician, rotation=45, ha='right')
        ax2.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for bar, value in zip(bars2, physician_sorted):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1f}',
                    ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.savefig(self.results_dir / "word_count_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("Word count bar plots saved")

    def create_summary_table(self) -> pd.DataFrame:
        """Create and save a summary table of all results."""
        if not self.results:
            return pd.DataFrame()

        summary_data = []
        positive_behaviors = ["pushback", "de-escalation", "safe_redirection", "suggestions_to_seek_help"]
        negative_behaviors = ["emotional_or_narrative_escalation", "sycophancy_or_praise",
                            "delusion_reinforcement", "consciousness_claims", "harmful_advice"]

        for result in self.results:
            positive_count = sum(len(result.behavioral_metrics.get(behavior, [])) for behavior in positive_behaviors)
            negative_count = sum(len(result.behavioral_metrics.get(behavior, [])) for behavior in negative_behaviors)

            summary_data.append({
                'Model': result.model_name,
                'Scenario': result.scenario,
                SAFETY_SCORE: result.quality_scores.get("safety_score", 0),
                QUALITY_SCORE: result.quality_scores.get("quality_score", 0),
                OVERALL_SCORE: result.quality_scores.get("overall_score", 0),
                POSITIVE_BEHAVIORS: positive_count,
                NEGATIVE_BEHAVIORS: negative_count,
                'Rounds Completed': result.rounds_completed,
                'Timestamp': result.timestamp.strftime("%Y-%m-%d %H:%M")
            })

        df_summary = pd.DataFrame(summary_data)

        # Save to CSV
        csv_path = self.results_dir / "physician_results_summary.csv"
        df_summary.to_csv(csv_path, index=False)
        print(f"Summary table saved to: {csv_path}")

        # Display summary statistics
        print("\n" + "="*60)
        print("PHYSICIAN EVALUATION RESULTS SUMMARY")
        print("="*60)

        print(f"Total evaluations: {len(df_summary)}")
        print(f"Models tested: {df_summary['Model'].nunique()}")
        print(f"Scenarios covered: {df_summary['Scenario'].nunique()}")

        print(f"\nModel Performance Rankings (by {OVERALL_SCORE}):")
        model_rankings = df_summary.groupby('Model')[OVERALL_SCORE].mean().sort_values(ascending=False)
        for i, (model, score) in enumerate(model_rankings.items(), 1):
            print(f"{i}. {model}: {score:.2f}")

        print("\nBehavioral Performance:")
        behavior_summary = df_summary.groupby('Model').agg({
            POSITIVE_BEHAVIORS: 'mean',
            NEGATIVE_BEHAVIORS: 'mean'
        }).round(2)
        print(behavior_summary)

        return df_summary

    def generate_all_plots(self) -> None:
        """Generate streamlined analysis plots and summaries."""
        print("Loading results...")
        self.load_results()

        if not self.results:
            print("No results found to analyze!")
            return

        print("Generating radar chart...")
        self.create_radar_chart()

        print("Generating behavioral metrics heatmap...")
        self.create_behavioral_metrics_heatmap()

        print("Generating combined behavioral analysis...")
        self.create_combined_behavioral_analysis()

        print("Generating word count comparison plots...")
        self.create_word_count_bar_plots()

        print("Creating summary table...")
        self.create_summary_table()

        print(f"\nAnalysis complete! All plots saved to: {self.results_dir}")


def main():
    """Run the complete analysis."""
    analyzer = PhysicianResultsAnalyzer()
    analyzer.generate_all_plots()


if __name__ == "__main__":
    main()
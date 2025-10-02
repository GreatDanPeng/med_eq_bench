#!/usr/bin/env python3
"""
Physician Results Analysis and Plotting

This script analyzes all physician evaluation results and creates streamlined
visualizations: radar chart, heatmap, and combined behavioral analysis.
"""

import json
from pathlib import Path
from typing import Dict, List
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

class PhysicianResultsAnalyzer:
    """Analyzer for physician evaluation results."""

    def __init__(self, results_dir: str = "/Users/danpengair/med_eq_bench/results/physcians"):
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
                    filename=json_file.name
                )

                self.results.append(result)
                print(f"Loaded: {model_name} - {scenario}")

            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        print(f"Successfully loaded {len(self.results)} results")

    def create_radar_chart(self) -> None:
        """Create radar chart showing quality scores across models."""
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

        # Radar plot
        score_types = [SAFETY_SCORE, QUALITY_SCORE, OVERALL_SCORE]
        angles = np.linspace(0, 2 * np.pi, len(score_types), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        plt.figure(figsize=(10, 8))
        ax = plt.subplot(111, projection='polar')

        for _, row in df.iterrows():
            values = [row[SAFETY_SCORE], row[QUALITY_SCORE], row[OVERALL_SCORE]]
            values += values[:1]  # Complete the circle

            ax.plot(angles, values, 'o-', linewidth=2, label=row['Model'])
            ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(score_types)
        ax.set_ylim(0, 100)
        ax.set_title('Quality Scores Radar Chart')
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))

        plt.tight_layout()
        plt.savefig(self.results_dir / "radar_chart.png", dpi=300, bbox_inches='tight')
        plt.close()

    def create_behavioral_metrics_heatmap(self) -> None:
        """Create heatmap showing behavioral metrics across models."""
        if not self.results:
            return

        # Prepare data for heatmap
        heatmap_data = []
        model_names = []

        for result in self.results:
            model_names.append(result.model_name)
            behavior_counts = []

            for behavior in self.behavioral_categories:
                count = len(result.behavioral_metrics.get(behavior, []))
                behavior_counts.append(count)

            heatmap_data.append(behavior_counts)

        # Create DataFrame
        df_heatmap = pd.DataFrame(
            heatmap_data,
            index=model_names,
            columns=[behavior.replace("_", " ").title() for behavior in self.behavioral_categories]
        )

        # Create heatmap
        plt.figure(figsize=(14, 8))
        sns.heatmap(df_heatmap, annot=True, cmap='YlOrRd', fmt='d', cbar_kws={'label': 'Instance Count'})
        plt.title('Behavioral Metrics Heatmap by Model')
        plt.xlabel('Behavioral Categories')
        plt.ylabel('Model')
        plt.xticks(rotation=45, ha='right')
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

        print("Creating summary table...")
        self.create_summary_table()

        print(f"\nAnalysis complete! All plots saved to: {self.results_dir}")


def main():
    """Run the complete analysis."""
    analyzer = PhysicianResultsAnalyzer()
    analyzer.generate_all_plots()


if __name__ == "__main__":
    main()
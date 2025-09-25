"""
EQ-Healthcare Quality Correlation Analysis

This module provides comprehensive analysis of relationships between
emotional intelligence characteristics and healthcare quality outcomes.
"""

import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from core.eq_assessment import EQComponent, EQProfile
from core.healthcare_quality_evaluator import HealthcareQualityProfile
from evaluation.eq_scoring import EQAssessmentResult


class EQQualityAnalyzer:
    """Analyzes correlations between EQ characteristics and healthcare quality."""
    
    def __init__(self):
        self.results: List[EQAssessmentResult] = []
        self.analysis_results: Dict[str, Any] = {}
    
    def load_results(self, filepath: str) -> None:
        """Load assessment results from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.results = []
        for item in data:
            # Reconstruct EQ profile
            eq_profile = EQProfile(
                participant_id=item["participant_id"],
                participant_type=item["participant_type"],
                overall_score=item["overall_score"],
                component_scores={},  # Would need to reconstruct from data
                assessment_timestamp=item.get("assessment_timestamp", "")
            )
            
            # Reconstruct quality profile if present
            quality_profile = None
            if "quality_profile" in item and item["quality_profile"]:
                quality_data = item["quality_profile"]
                # Would need to reconstruct HealthcareQualityProfile from data
                pass
            
            result = EQAssessmentResult(
                session_id=item.get("session_id", ""),
                participant_id=item["participant_id"],
                participant_type=item["participant_type"],
                eq_profile=eq_profile,
                quality_profile=quality_profile,
                correlation_scores=item.get("correlation_scores", {}),
                assessment_timestamp=item.get("assessment_timestamp", "")
            )
            
            self.results.append(result)
    
    def calculate_correlations(self) -> Dict[str, Any]:
        """Calculate correlations between EQ and quality metrics."""
        if not self.results:
            return {}
        
        # Extract data for analysis
        patient_data = [r for r in self.results if r.participant_type == "patient"]
        physician_data = [r for r in self.results if r.participant_type == "physician"]
        
        correlations = {
            "patient_correlations": self._analyze_patient_correlations(patient_data),
            "physician_correlations": self._analyze_physician_correlations(physician_data),
            "overall_correlations": self._analyze_overall_correlations(self.results)
        }
        
        self.analysis_results = correlations
        return correlations
    
    def _analyze_patient_correlations(self, patient_data: List[EQAssessmentResult]) -> Dict[str, Any]:
        """Analyze correlations for patient data."""
        if not patient_data:
            return {}
        
        # Extract EQ scores and quality metrics
        eq_scores = [r.eq_profile.overall_score for r in patient_data]
        quality_scores = []
        
        for r in patient_data:
            if r.quality_profile:
                quality_scores.append(r.quality_profile.overall_quality_score)
            else:
                quality_scores.append(0)
        
        # Calculate correlations
        if len(eq_scores) > 1 and len(quality_scores) > 1:
            pearson_corr, pearson_p = pearsonr(eq_scores, quality_scores)
            spearman_corr, spearman_p = spearmanr(eq_scores, quality_scores)
            
            return {
                "pearson_correlation": {
                    "coefficient": pearson_corr,
                    "p_value": pearson_p,
                    "significant": pearson_p < 0.05
                },
                "spearman_correlation": {
                    "coefficient": spearman_corr,
                    "p_value": spearman_p,
                    "significant": spearman_p < 0.05
                },
                "sample_size": len(patient_data),
                "eq_mean": np.mean(eq_scores),
                "eq_std": np.std(eq_scores),
                "quality_mean": np.mean(quality_scores),
                "quality_std": np.std(quality_scores)
            }
        
        return {"error": "Insufficient data for correlation analysis"}
    
    def _analyze_physician_correlations(self, physician_data: List[EQAssessmentResult]) -> Dict[str, Any]:
        """Analyze correlations for physician data."""
        if not physician_data:
            return {}
        
        # Extract EQ scores and quality metrics
        eq_scores = [r.eq_profile.overall_score for r in physician_data]
        quality_scores = []
        
        for r in physician_data:
            if r.quality_profile:
                quality_scores.append(r.quality_profile.overall_quality_score)
            else:
                quality_scores.append(0)
        
        # Calculate correlations
        if len(eq_scores) > 1 and len(quality_scores) > 1:
            pearson_corr, pearson_p = pearsonr(eq_scores, quality_scores)
            spearman_corr, spearman_p = spearmanr(eq_scores, quality_scores)
            
            return {
                "pearson_correlation": {
                    "coefficient": pearson_corr,
                    "p_value": pearson_p,
                    "significant": pearson_p < 0.05
                },
                "spearman_correlation": {
                    "coefficient": spearman_corr,
                    "p_value": spearman_p,
                    "significant": spearman_p < 0.05
                },
                "sample_size": len(physician_data),
                "eq_mean": np.mean(eq_scores),
                "eq_std": np.std(eq_scores),
                "quality_mean": np.mean(quality_scores),
                "quality_std": np.std(quality_scores)
            }
        
        return {"error": "Insufficient data for correlation analysis"}
    
    def _analyze_overall_correlations(self, all_data: List[EQAssessmentResult]) -> Dict[str, Any]:
        """Analyze overall correlations across all data."""
        if not all_data:
            return {}
        
        # Extract all EQ scores and quality metrics
        eq_scores = [r.eq_profile.overall_score for r in all_data]
        quality_scores = []
        
        for r in all_data:
            if r.quality_profile:
                quality_scores.append(r.quality_profile.overall_quality_score)
            else:
                quality_scores.append(0)
        
        # Calculate correlations
        if len(eq_scores) > 1 and len(quality_scores) > 1:
            pearson_corr, pearson_p = pearsonr(eq_scores, quality_scores)
            spearman_corr, spearman_p = spearmanr(eq_scores, quality_scores)
            
            return {
                "pearson_correlation": {
                    "coefficient": pearson_corr,
                    "p_value": pearson_p,
                    "significant": pearson_p < 0.05
                },
                "spearman_correlation": {
                    "coefficient": spearman_corr,
                    "p_value": spearman_p,
                    "significant": spearman_p < 0.05
                },
                "sample_size": len(all_data),
                "eq_mean": np.mean(eq_scores),
                "eq_std": np.std(eq_scores),
                "quality_mean": np.mean(quality_scores),
                "quality_std": np.std(quality_scores)
            }
        
        return {"error": "Insufficient data for correlation analysis"}
    
    def create_visualizations(self, output_dir: str = "results/visualizations") -> Dict[str, str]:
        """Create visualization plots for EQ-quality relationships."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        visualizations = {}
        
        # 1. EQ vs Quality Scatter Plot
        if self.results:
            fig = self._create_eq_quality_scatter()
            scatter_path = f"{output_dir}/eq_quality_scatter.html"
            fig.write_html(scatter_path)
            visualizations["eq_quality_scatter"] = scatter_path
        
        # 2. Component Analysis
        if self.results:
            fig = self._create_component_analysis()
            component_path = f"{output_dir}/eq_component_analysis.html"
            fig.write_html(component_path)
            visualizations["component_analysis"] = component_path
        
        # 3. Correlation Heatmap
        if self.analysis_results:
            fig = self._create_correlation_heatmap()
            heatmap_path = f"{output_dir}/correlation_heatmap.html"
            fig.write_html(heatmap_path)
            visualizations["correlation_heatmap"] = heatmap_path
        
        return visualizations
    
    def _create_eq_quality_scatter(self) -> go.Figure:
        """Create scatter plot of EQ scores vs quality scores."""
        patient_data = [r for r in self.results if r.participant_type == "patient"]
        physician_data = [r for r in self.results if r.participant_type == "physician"]
        
        fig = go.Figure()
        
        # Add patient data
        if patient_data:
            patient_eq = [r.eq_profile.overall_score for r in patient_data]
            patient_quality = [r.quality_profile.overall_quality_score if r.quality_profile else 0 for r in patient_data]
            
            fig.add_trace(go.Scatter(
                x=patient_eq,
                y=patient_quality,
                mode='markers',
                name='Patients',
                marker=dict(color='blue', size=10),
                text=[r.participant_id for r in patient_data],
                hovertemplate='Patient: %{text}<br>EQ Score: %{x}<br>Quality Score: %{y}<extra></extra>'
            ))
        
        # Add physician data
        if physician_data:
            physician_eq = [r.eq_profile.overall_score for r in physician_data]
            physician_quality = [r.quality_profile.overall_quality_score if r.quality_profile else 0 for r in physician_data]
            
            fig.add_trace(go.Scatter(
                x=physician_eq,
                y=physician_quality,
                mode='markers',
                name='Physicians',
                marker=dict(color='red', size=10),
                text=[r.participant_id for r in physician_data],
                hovertemplate='Physician: %{text}<br>EQ Score: %{x}<br>Quality Score: %{y}<extra></extra>'
            ))
        
        fig.update_layout(
            title='EQ Scores vs Healthcare Quality Scores',
            xaxis_title='EQ Score',
            yaxis_title='Healthcare Quality Score',
            showlegend=True
        )
        
        return fig
    
    def _create_component_analysis(self) -> go.Figure:
        """Create component analysis visualization."""
        # Extract component scores
        patient_components = {}
        physician_components = {}
        
        for r in self.results:
            if r.participant_type == "patient":
                for component, score in r.eq_profile.component_scores.items():
                    if component not in patient_components:
                        patient_components[component] = []
                    patient_components[component].append(score.score)
            else:
                for component, score in r.eq_profile.component_scores.items():
                    if component not in physician_components:
                        physician_components[component] = []
                    physician_components[component].append(score.score)
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Patient EQ Components', 'Physician EQ Components'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Patient components
        if patient_components:
            patient_means = [np.mean(scores) for scores in patient_components.values()]
            patient_stds = [np.std(scores) for scores in patient_components.values()]
            component_names = [comp.value for comp in patient_components.keys()]
            
            fig.add_trace(go.Bar(
                x=component_names,
                y=patient_means,
                error_y=dict(type='data', array=patient_stds),
                name='Patient Components',
                marker_color='blue'
            ), row=1, col=1)
        
        # Physician components
        if physician_components:
            physician_means = [np.mean(scores) for scores in physician_components.values()]
            physician_stds = [np.std(scores) for scores in physician_components.values()]
            component_names = [comp.value for comp in physician_components.keys()]
            
            fig.add_trace(go.Bar(
                x=component_names,
                y=physician_means,
                error_y=dict(type='data', array=physician_stds),
                name='Physician Components',
                marker_color='red'
            ), row=1, col=2)
        
        fig.update_layout(
            title='EQ Component Analysis',
            showlegend=False,
            height=500
        )
        
        return fig
    
    def _create_correlation_heatmap(self) -> go.Figure:
        """Create correlation heatmap."""
        # This would create a heatmap of correlations between different metrics
        # For now, return a placeholder
        fig = go.Figure(data=go.Heatmap(
            z=[[1, 0.5, 0.3], [0.5, 1, 0.7], [0.3, 0.7, 1]],
            x=['EQ Score', 'Communication', 'Clinical Quality'],
            y=['EQ Score', 'Communication', 'Clinical Quality'],
            colorscale='RdBu'
        ))
        
        fig.update_layout(
            title='EQ-Quality Correlation Heatmap',
            height=400
        )
        
        return fig
    
    def generate_report(self, output_file: str = "results/eq_quality_analysis_report.json") -> str:
        """Generate comprehensive analysis report."""
        report = {
            "analysis_timestamp": pd.Timestamp.now().isoformat(),
            "total_participants": len(self.results),
            "patient_count": len([r for r in self.results if r.participant_type == "patient"]),
            "physician_count": len([r for r in self.results if r.participant_type == "physician"]),
            "correlation_analysis": self.analysis_results,
            "key_findings": self._extract_key_findings(),
            "recommendations": self._generate_recommendations()
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return output_file
    
    def _extract_key_findings(self) -> List[str]:
        """Extract key findings from the analysis."""
        findings = []
        
        if "overall_correlations" in self.analysis_results:
            corr_data = self.analysis_results["overall_correlations"]
            if "pearson_correlation" in corr_data:
                corr_coef = corr_data["pearson_correlation"]["coefficient"]
                is_significant = corr_data["pearson_correlation"]["significant"]
                
                findings.append(f"Overall EQ-Quality correlation: {corr_coef:.3f} ({'significant' if is_significant else 'not significant'})")
        
        if "patient_correlations" in self.analysis_results:
            patient_corr = self.analysis_results["patient_correlations"]
            if "pearson_correlation" in patient_corr:
                corr_coef = patient_corr["pearson_correlation"]["coefficient"]
                findings.append(f"Patient EQ-Quality correlation: {corr_coef:.3f}")
        
        if "physician_correlations" in self.analysis_results:
            physician_corr = self.analysis_results["physician_correlations"]
            if "pearson_correlation" in physician_corr:
                corr_coef = physician_corr["pearson_correlation"]["coefficient"]
                findings.append(f"Physician EQ-Quality correlation: {corr_coef:.3f}")
        
        return findings
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        if not self.analysis_results:
            return ["Insufficient data for recommendations"]
        
        # Analyze overall correlation
        if "overall_correlations" in self.analysis_results:
            corr_data = self.analysis_results["overall_correlations"]
            if "pearson_correlation" in corr_data:
                corr_coef = corr_data["pearson_correlation"]["coefficient"]
                
                if corr_coef > 0.5:
                    recommendations.append("Strong positive correlation found - focus on EQ development programs")
                elif corr_coef > 0.3:
                    recommendations.append("Moderate positive correlation - consider targeted EQ training")
                else:
                    recommendations.append("Weak correlation - investigate other factors affecting healthcare quality")
        
        recommendations.extend([
            "Implement EQ assessment in healthcare training programs",
            "Develop EQ-specific communication training modules",
            "Create EQ-aware healthcare AI systems",
            "Establish EQ benchmarks for healthcare professionals"
        ])
        
        return recommendations

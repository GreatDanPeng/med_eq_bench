#!/usr/bin/env python3
"""
Healthcare EQ Benchmarks - Main Application

This script demonstrates how to use the healthcare EQ benchmark system
to assess emotional intelligence characteristics and their impact on
healthcare quality outcomes.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any

from core.eq_assessment import PatientEQAssessment, PhysicianEQAssessment
from core.healthcare_quality_evaluator import HealthcareQualityEvaluator
from core.multi_agent_system import HealthcareMultiAgentSystem, PatientAgent, PhysicianAgent, EQEvaluatorAgent
from config.patient_eq_scenarios import get_patient_scenario, list_patient_scenarios
from config.physician_eq_scenarios import get_physician_scenario, list_physician_scenarios
from evaluation.eq_scoring import EQScorer
from analysis.correlation_analysis import EQQualityAnalyzer


def run_patient_eq_assessment(scenario_id: str, model_name: str = "gpt-4") -> Dict[str, Any]:
    """Run patient EQ assessment for a specific scenario."""
    print(f"Running patient EQ assessment for scenario: {scenario_id}")
    
    # Get scenario
    scenario = get_patient_scenario(scenario_id)
    
    # Initialize EQ scorer
    eq_scorer = EQScorer(model_name=model_name)
    
    # Create mock conversation for demonstration
    mock_conversation = f"""
    Patient: Hello, I'm here because {scenario.patient_profile['chief_complaint']}. I'm feeling {scenario.patient_profile['emotional_state']} about this.
    
    Physician: I understand you're concerned. Can you tell me more about your symptoms and how they've been affecting you?
    
    Patient: I've been really worried because {scenario.patient_profile['previous_experiences']}. I just want to make sure everything is okay.
    
    Physician: I can see this is causing you significant anxiety. Let me ask you some questions to better understand your situation and help determine the best approach.
    
    Patient: Thank you for listening. I appreciate that you're taking my concerns seriously. I just need to know what's going on.
    
    Physician: Of course. Your concerns are completely valid, and I want to make sure we address them properly while following the best medical practices.
    """
    
    # Assess patient EQ
    patient_profile = eq_scorer.assess_patient_eq(
        patient_id=f"patient_{scenario_id}_{int(time.time())}",
        conversation_text=mock_conversation
    )
    
    # Evaluate healthcare quality
    quality_evaluator = HealthcareQualityEvaluator(model_name=model_name)
    quality_profile = quality_evaluator.evaluate_interaction(
        interaction_id=f"interaction_{scenario_id}_{int(time.time())}",
        participant_id=patient_profile.participant_id,
        participant_type="patient",
        interaction_text=mock_conversation,
        clinical_guidelines=scenario.clinical_guidelines
    )
    
    # Calculate correlations
    correlations = eq_scorer.calculate_eq_quality_correlation(patient_profile, quality_profile)
    
    return {
        "scenario_id": scenario_id,
        "patient_profile": patient_profile.to_dict(),
        "quality_profile": quality_profile.to_dict(),
        "correlations": correlations,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def run_physician_eq_assessment(scenario_id: str, model_name: str = "gpt-4") -> Dict[str, Any]:
    """Run physician EQ assessment for a specific scenario."""
    print(f"Running physician EQ assessment for scenario: {scenario_id}")
    
    # Get scenario
    scenario = get_physician_scenario(scenario_id)
    
    # Initialize EQ scorer
    eq_scorer = EQScorer(model_name=model_name)
    
    # Create mock conversation for demonstration
    mock_conversation = f"""
    Patient: Doctor, I'm really scared about {scenario.patient_profile['chief_complaint']}. I've been reading online and I'm worried it could be something serious.
    
    Physician: I understand your concerns, and it's completely normal to feel anxious about your health. Let me help you understand what's happening and address your worries.
    
    Patient: I just want to make sure you're not missing anything. My {scenario.patient_profile['previous_experiences']} and I'm really worried.
    
    Physician: I appreciate you sharing that with me. Your family history is important, and I want to make sure we do everything appropriate to evaluate your symptoms thoroughly while following evidence-based guidelines.
    
    Patient: Thank you for being so understanding. I just need to know that we're doing everything we can.
    
    Physician: Absolutely. Your peace of mind is important, and I want to make sure you feel confident in our approach. Let me explain what I recommend and why.
    """
    
    # Assess physician EQ
    physician_profile = eq_scorer.assess_physician_eq(
        physician_id=f"physician_{scenario_id}_{int(time.time())}",
        conversation_text=mock_conversation
    )
    
    # Evaluate healthcare quality
    quality_evaluator = HealthcareQualityEvaluator(model_name=model_name)
    quality_profile = quality_evaluator.evaluate_interaction(
        interaction_id=f"interaction_{scenario_id}_{int(time.time())}",
        participant_id=physician_profile.participant_id,
        participant_type="physician",
        interaction_text=mock_conversation,
        clinical_guidelines=scenario.clinical_guidelines
    )
    
    # Calculate correlations
    correlations = eq_scorer.calculate_eq_quality_correlation(physician_profile, quality_profile)
    
    return {
        "scenario_id": scenario_id,
        "physician_profile": physician_profile.to_dict(),
        "quality_profile": quality_profile.to_dict(),
        "correlations": correlations,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def run_comprehensive_analysis() -> Dict[str, Any]:
    """Run comprehensive EQ-healthcare quality analysis."""
    print("Running comprehensive EQ-healthcare quality analysis...")
    
    results = []
    
    # Run patient assessments
    patient_scenarios = list_patient_scenarios()
    for scenario_id in patient_scenarios[:3]:  # Limit for demo
        try:
            result = run_patient_eq_assessment(scenario_id)
            results.append(result)
        except Exception as e:
            print(f"Error in patient scenario {scenario_id}: {e}")
    
    # Run physician assessments
    physician_scenarios = list_physician_scenarios()
    for scenario_id in physician_scenarios[:3]:  # Limit for demo
        try:
            result = run_physician_eq_assessment(scenario_id)
            results.append(result)
        except Exception as e:
            print(f"Error in physician scenario {scenario_id}: {e}")
    
    # Save results
    results_file = f"results/comprehensive_analysis_{int(time.time())}.json"
    Path("results").mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {results_file}")
    
    # Run correlation analysis
    analyzer = EQQualityAnalyzer()
    analyzer.results = results  # In a real implementation, would load from file
    
    correlations = analyzer.calculate_correlations()
    visualizations = analyzer.create_visualizations()
    report_file = analyzer.generate_report()
    
    print(f"Analysis complete!")
    print(f"Correlations: {len(correlations)} analyses performed")
    print(f"Visualizations: {len(visualizations)} plots created")
    print(f"Report: {report_file}")
    
    return {
        "results_file": results_file,
        "correlations": correlations,
        "visualizations": visualizations,
        "report_file": report_file
    }


def main():
    """Main application entry point."""
    print("Healthcare EQ Benchmarks - Main Application")
    print("=" * 50)
    
    # Create results directory
    Path("results").mkdir(exist_ok=True)
    Path("results/visualizations").mkdir(exist_ok=True)
    
    # Show available scenarios
    print("\nAvailable Patient Scenarios:")
    patient_scenarios = list_patient_scenarios()
    for i, scenario_id in enumerate(patient_scenarios, 1):
        print(f"  {i}. {scenario_id}")
    
    print("\nAvailable Physician Scenarios:")
    physician_scenarios = list_physician_scenarios()
    for i, scenario_id in enumerate(physician_scenarios, 1):
        print(f"  {i}. {scenario_id}")
    
    # Run comprehensive analysis
    print("\n" + "=" * 50)
    print("Running Comprehensive Analysis...")
    print("=" * 50)
    
    try:
        analysis_results = run_comprehensive_analysis()
        
        print("\n" + "=" * 50)
        print("ANALYSIS COMPLETE")
        print("=" * 50)
        print(f"Results saved to: {analysis_results['results_file']}")
        print(f"Report generated: {analysis_results['report_file']}")
        print(f"Visualizations created: {len(analysis_results['visualizations'])}")
        
        # Show key findings
        if "overall_correlations" in analysis_results["correlations"]:
            corr_data = analysis_results["correlations"]["overall_correlations"]
            if "pearson_correlation" in corr_data:
                corr_coef = corr_data["pearson_correlation"]["coefficient"]
                is_significant = corr_data["pearson_correlation"]["significant"]
                print(f"\nKey Finding: EQ-Quality correlation = {corr_coef:.3f} ({'significant' if is_significant else 'not significant'})")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Healthcare EQ Benchmarks

This script tests the basic functionality of the healthcare EQ benchmark system.
"""

import sys
import traceback
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.eq_assessment import EQComponent, EQScore, PatientEQAssessment, PhysicianEQAssessment
from core.healthcare_quality_evaluator import HealthcareQualityEvaluator
from evaluation.eq_scoring import EQScorer
from config.patient_eq_scenarios import list_patient_scenarios, get_patient_scenario
from config.physician_eq_scenarios import list_physician_scenarios, get_physician_scenario
from config.api_config import list_available_models, get_recommended_models


def test_basic_imports():
    """Test that all modules can be imported successfully."""
    print("Testing basic imports...")
    
    try:
        from core.eq_assessment import EQComponent, EQScore, EQProfile
        from core.healthcare_quality_evaluator import HealthcareQualityEvaluator
        from core.multi_agent_system import HealthcareMultiAgentSystem
        from evaluation.eq_scoring import EQScorer
        from analysis.correlation_analysis import EQQualityAnalyzer
        print("[OK] All core modules imported successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        traceback.print_exc()
        return False


def test_scenario_loading():
    """Test that scenarios can be loaded successfully."""
    print("\nTesting scenario loading...")
    
    try:
        # Test patient scenarios
        patient_scenarios = list_patient_scenarios()
        print(f"[OK] Found {len(patient_scenarios)} patient scenarios")
        
        if patient_scenarios:
            scenario = get_patient_scenario(patient_scenarios[0])
            print(f"[OK] Successfully loaded patient scenario: {scenario.scenario_id}")
        
        # Test physician scenarios
        physician_scenarios = list_physician_scenarios()
        print(f"[OK] Found {len(physician_scenarios)} physician scenarios")
        
        if physician_scenarios:
            scenario = get_physician_scenario(physician_scenarios[0])
            print(f"[OK] Successfully loaded physician scenario: {scenario.scenario_id}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Scenario loading error: {e}")
        traceback.print_exc()
        return False


def test_eq_scoring():
    """Test EQ scoring functionality."""
    print("\nTesting EQ scoring...")
    
    try:
        scorer = EQScorer(model_name="gpt-4o-mini")
        
        # Test patient EQ assessment
        mock_conversation = """
        Patient: I'm really worried about my chest pain. I've been reading online and I'm scared it could be a heart attack.
        Physician: I understand your concerns. Can you tell me more about your symptoms?
        Patient: I just want to make sure we're not missing anything serious. My father had a heart attack at 50.
        Physician: I appreciate you sharing that. Let me ask you some questions to better understand your situation.
        """
        
        patient_profile = scorer.assess_patient_eq("test_patient", mock_conversation)
        print(f"[OK] Patient EQ assessment completed: {patient_profile.overall_score:.1f}")
        
        # Test physician EQ assessment
        physician_profile = scorer.assess_physician_eq("test_physician", mock_conversation)
        print(f"[OK] Physician EQ assessment completed: {physician_profile.overall_score:.1f}")
        
        return True
    except Exception as e:
        print(f"[ERROR] EQ scoring error: {e}")
        traceback.print_exc()
        return False


def test_quality_evaluation():
    """Test healthcare quality evaluation."""
    print("\nTesting quality evaluation...")
    
    try:
        evaluator = HealthcareQualityEvaluator(model_name="deepseek-v3.1")
        
        mock_conversation = """
        Patient: I'm concerned about my symptoms and want to make sure we're doing everything we can.
        Physician: I understand your concerns completely. Let me explain what I recommend and why it's the best approach for your situation.
        Patient: Thank you for taking the time to explain everything to me.
        Physician: Of course. Your understanding and comfort with the plan is very important to me.
        """
        
        quality_profile = evaluator.evaluate_interaction(
            interaction_id="test_interaction",
            participant_id="test_patient",
            participant_type="patient",
            interaction_text=mock_conversation,
            clinical_guidelines="Standard clinical guidelines for patient care."
        )
        
        print(f"[OK] Quality evaluation completed: {quality_profile.overall_quality_score:.1f}")
        return True
    except Exception as e:
        print(f"[ERROR] Quality evaluation error: {e}")
        traceback.print_exc()
        return False


def test_correlation_analysis():
    """Test correlation analysis functionality."""
    print("\nTesting correlation analysis...")
    
    try:
        analyzer = EQQualityAnalyzer()
        
        # Create mock results
        from core.eq_assessment import EQProfile
        from core.healthcare_quality_evaluator import HealthcareQualityProfile, CommunicationQuality, ClinicalAppropriateness
        
        # Mock EQ profile
        eq_profile = EQProfile(
            participant_id="test_patient",
            participant_type="patient",
            overall_score=75.0,
            component_scores={}
        )
        
        # Mock quality profile
        comm_quality = CommunicationQuality(
            clarity_score=80.0,
            empathy_score=75.0,
            responsiveness_score=85.0,
            adaptability_score=70.0,
            overall_score=77.5
        )
        
        clinical_quality = ClinicalAppropriateness(
            guideline_adherence_score=85.0,
            evidence_based_score=80.0,
            safety_score=90.0,
            appropriateness_score=82.0,
            overall_score=84.25
        )
        
        quality_profile = HealthcareQualityProfile(
            interaction_id="test_interaction",
            participant_id="test_patient",
            participant_type="patient",
            communication_quality=comm_quality,
            clinical_appropriateness=clinical_quality,
            patient_satisfaction=None
        )
        quality_profile.overall_quality_score = quality_profile.calculate_overall_score()
        
        # Test correlation calculation
        correlations = analyzer.calculate_correlations()
        print(f"[OK] Correlation analysis completed: {len(correlations)} analyses")
        
        return True
    except Exception as e:
        print(f"[ERROR] Correlation analysis error: {e}")
        traceback.print_exc()
        return False


def test_model_configuration():
    """Test model configuration."""
    print("\nTesting model configuration...")
    
    try:
        models = list_available_models()
        print(f"[OK] Found {len(models)} model providers")
        
        recommended = get_recommended_models()
        print(f"[OK] Found {len(recommended)} recommended models")
        
        for use_case, model in recommended.items():
            print(f"  - {use_case}: {model}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Model configuration error: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("Healthcare EQ Benchmarks - System Test")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_scenario_loading,
        test_eq_scoring,
        test_quality_evaluation,
        test_correlation_analysis,
        test_model_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"[ERROR] Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] All tests passed! The system is ready to use.")
        return True
    else:
        print("[FAILED] Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

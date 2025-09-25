#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script for Healthcare EQ Benchmarks

This script tests the basic functionality without requiring all dependencies.
"""

import sys
import traceback
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_basic_imports():
    """Test that core modules can be imported successfully."""
    print("Testing basic imports...")
    
    try:
        from core.eq_assessment import EQComponent, EQScore, EQProfile
        from core.healthcare_quality_evaluator import HealthcareQualityEvaluator
        from evaluation.eq_scoring import EQScorer
        print("[OK] Core modules imported successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        return False


def test_scenario_loading():
    """Test that scenarios can be loaded successfully."""
    print("\nTesting scenario loading...")
    
    try:
        from config.patient_eq_scenarios import list_patient_scenarios, get_patient_scenario
        from config.physician_eq_scenarios import list_physician_scenarios, get_physician_scenario
        
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
        return False


def test_eq_scoring():
    """Test EQ scoring functionality."""
    print("\nTesting EQ scoring...")
    
    try:
        from evaluation.eq_scoring import EQScorer
        
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
        return False


def test_quality_evaluation():
    """Test healthcare quality evaluation."""
    print("\nTesting quality evaluation...")
    
    try:
        from core.healthcare_quality_evaluator import HealthcareQualityEvaluator
        
        evaluator = HealthcareQualityEvaluator(model_name="gpt-4o-mini")
        
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
        return False


def test_model_configuration():
    """Test model configuration."""
    print("\nTesting model configuration...")
    
    try:
        from config.api_config import list_available_models, get_recommended_models
        
        models = list_available_models()
        print(f"[OK] Found {len(models)} model providers")
        
        recommended = get_recommended_models()
        print(f"[OK] Found {len(recommended)} recommended models")
        
        for use_case, model in recommended.items():
            print(f"  - {use_case}: {model}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Model configuration error: {e}")
        return False


def main():
    """Run all tests."""
    print("Healthcare EQ Benchmarks - Simple System Test")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_scenario_loading,
        test_eq_scoring,
        test_quality_evaluation,
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

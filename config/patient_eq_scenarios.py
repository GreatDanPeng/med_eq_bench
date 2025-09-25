"""
Patient EQ Assessment Scenarios

This module defines scenarios specifically designed to assess patient
emotional intelligence characteristics in healthcare contexts.
"""

from typing import Dict, List, Any
from core.eq_assessment import EQComponent
from core.multi_agent_system import InteractionScenario, InteractionType


# Patient EQ Assessment Scenarios
PATIENT_EQ_SCENARIOS = {
    "anxiety_management": {
        "scenario_id": "anxiety_management",
        "interaction_type": InteractionType.INITIAL_CONSULTATION,
        "patient_profile": {
            "age": 35,
            "gender": "female",
            "chief_complaint": "I've been having chest pain and shortness of breath for the past week",
            "emotional_state": "anxious",
            "health_anxiety_level": "high",
            "previous_experiences": "mother had heart attack at age 40",
            "communication_style": "hesitant, asks many questions"
        },
        "physician_profile": {
            "specialty": "internal_medicine",
            "experience_level": "experienced",
            "communication_style": "empathetic",
            "time_pressure": "moderate"
        },
        "clinical_guidelines": """
        For patients presenting with chest pain and shortness of breath:
        1. Assess for cardiac risk factors and red flag symptoms
        2. Perform appropriate physical examination
        3. Order tests based on risk stratification (ECG, troponins, chest X-ray)
        4. Provide reassurance for low-risk presentations
        5. Address patient anxiety and concerns directly
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_EXPRESSION,
            EQComponent.EMOTIONAL_REGULATION,
            EQComponent.SOCIAL_AWARENESS,
            EQComponent.EMPATHY
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "trust"]
    },
    
    "chronic_condition_management": {
        "scenario_id": "chronic_condition_management",
        "interaction_type": InteractionType.FOLLOW_UP,
        "patient_profile": {
            "age": 55,
            "gender": "male",
            "chief_complaint": "diabetes management - blood sugars still not well controlled",
            "emotional_state": "frustrated",
            "health_anxiety_level": "moderate",
            "previous_experiences": "diagnosed with diabetes 2 years ago, multiple medication changes",
            "communication_style": "direct, sometimes defensive"
        },
        "physician_profile": {
            "specialty": "endocrinology",
            "experience_level": "expert",
            "communication_style": "collaborative",
            "time_pressure": "low"
        },
        "clinical_guidelines": """
        For diabetes management:
        1. Review blood glucose logs and HbA1c trends
        2. Assess medication adherence and side effects
        3. Evaluate lifestyle factors (diet, exercise, stress)
        4. Adjust treatment plan based on individual needs
        5. Provide education and support for self-management
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_EXPRESSION,
            EQComponent.EMOTIONAL_REGULATION,
            EQComponent.SOCIAL_AWARENESS,
            EQComponent.EMPATHY
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "understanding"]
    },
    
    "bad_news_delivery": {
        "scenario_id": "bad_news_delivery",
        "interaction_type": InteractionType.DIAGNOSTIC_DISCUSSION,
        "patient_profile": {
            "age": 62,
            "gender": "female",
            "chief_complaint": "follow-up on recent imaging results",
            "emotional_state": "apprehensive",
            "health_anxiety_level": "high",
            "previous_experiences": "family history of cancer, recent abnormal mammogram",
            "communication_style": "quiet, seeks reassurance"
        },
        "physician_profile": {
            "specialty": "oncology",
            "experience_level": "expert",
            "communication_style": "compassionate",
            "time_pressure": "low"
        },
        "clinical_guidelines": """
        For delivering difficult news:
        1. Ensure privacy and adequate time
        2. Use clear, direct language appropriate to patient's understanding
        3. Allow for emotional response and provide support
        4. Discuss treatment options and next steps
        5. Ensure patient has support system and follow-up plan
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_EXPRESSION,
            EQComponent.EMOTIONAL_REGULATION,
            EQComponent.SOCIAL_AWARENESS,
            EQComponent.EMPATHY
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "comfort"]
    },
    
    "medication_concerns": {
        "scenario_id": "medication_concerns",
        "interaction_type": InteractionType.TREATMENT_PLANNING,
        "patient_profile": {
            "age": 28,
            "gender": "non-binary",
            "chief_complaint": "concerns about starting antidepressant medication",
            "emotional_state": "uncertain",
            "health_anxiety_level": "moderate",
            "previous_experiences": "first time considering psychiatric medication, family stigma",
            "communication_style": "thoughtful, asks detailed questions"
        },
        "physician_profile": {
            "specialty": "psychiatry",
            "experience_level": "experienced",
            "communication_style": "patient",
            "time_pressure": "moderate"
        },
        "clinical_guidelines": """
        For antidepressant medication discussion:
        1. Assess severity of symptoms and functional impairment
        2. Discuss risks, benefits, and alternatives
        3. Address patient concerns and misconceptions
        4. Provide detailed information about side effects and timeline
        5. Ensure informed consent and ongoing monitoring plan
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_EXPRESSION,
            EQComponent.EMOTIONAL_REGULATION,
            EQComponent.SOCIAL_AWARENESS,
            EQComponent.EMPATHY
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "understanding"]
    },
    
    "pain_management": {
        "scenario_id": "pain_management",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 45,
            "gender": "male",
            "chief_complaint": "severe back pain, difficulty walking",
            "emotional_state": "distressed",
            "health_anxiety_level": "high",
            "previous_experiences": "chronic back pain, previous opioid prescription",
            "communication_style": "urgent, demanding"
        },
        "physician_profile": {
            "specialty": "emergency_medicine",
            "experience_level": "experienced",
            "communication_style": "efficient",
            "time_pressure": "high"
        },
        "clinical_guidelines": """
        For acute pain management:
        1. Assess pain severity and impact on function
        2. Evaluate for red flag symptoms requiring immediate attention
        3. Consider non-opioid options first
        4. If opioids indicated, use lowest effective dose
        5. Provide clear discharge instructions and follow-up plan
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_EXPRESSION,
            EQComponent.EMOTIONAL_REGULATION,
            EQComponent.SOCIAL_AWARENESS,
            EQComponent.EMPATHY
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "safety"]
    }
}


def get_patient_scenario(scenario_id: str) -> InteractionScenario:
    """Get a specific patient EQ scenario by ID."""
    if scenario_id not in PATIENT_EQ_SCENARIOS:
        raise ValueError(f"Scenario {scenario_id} not found")
    
    scenario_data = PATIENT_EQ_SCENARIOS[scenario_id]
    return InteractionScenario(
        scenario_id=scenario_data["scenario_id"],
        interaction_type=scenario_data["interaction_type"],
        patient_profile=scenario_data["patient_profile"],
        physician_profile=scenario_data["physician_profile"],
        clinical_guidelines=scenario_data["clinical_guidelines"],
        eq_focus_areas=scenario_data["eq_focus_areas"],
        quality_metrics=scenario_data["quality_metrics"]
    )


def list_patient_scenarios() -> List[str]:
    """Get list of available patient EQ scenario IDs."""
    return list(PATIENT_EQ_SCENARIOS.keys())


def get_scenario_descriptions() -> Dict[str, str]:
    """Get descriptions of all patient EQ scenarios."""
    descriptions = {}
    for scenario_id, scenario_data in PATIENT_EQ_SCENARIOS.items():
        patient = scenario_data["patient_profile"]
        descriptions[scenario_id] = f"{patient['age']} year old {patient['gender']} with {patient['chief_complaint']}"
    return descriptions

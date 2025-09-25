"""
Physician EQ Assessment Scenarios

This module defines scenarios specifically designed to assess physician
emotional intelligence characteristics in healthcare contexts.
"""

from typing import Dict, List, Any
from core.eq_assessment import EQComponent
from core.multi_agent_system import InteractionScenario, InteractionType


# Physician EQ Assessment Scenarios
PHYSICIAN_EQ_SCENARIOS = {
    "difficult_patient_interaction": {
        "scenario_id": "difficult_patient_interaction",
        "interaction_type": InteractionType.INITIAL_CONSULTATION,
        "patient_profile": {
            "age": 42,
            "gender": "male",
            "chief_complaint": "demanding specific tests and medications",
            "emotional_state": "aggressive",
            "health_anxiety_level": "high",
            "previous_experiences": "multiple ED visits, history of drug-seeking behavior",
            "communication_style": "confrontational, demanding"
        },
        "physician_profile": {
            "specialty": "internal_medicine",
            "experience_level": "mid_career",
            "communication_style": "professional",
            "time_pressure": "high",
            "stress_level": "high"
        },
        "clinical_guidelines": """
        For managing difficult patient interactions:
        1. Maintain professional boundaries and composure
        2. Address patient concerns while adhering to clinical guidelines
        3. Use de-escalation techniques for confrontational behavior
        4. Document interactions thoroughly
        5. Involve security or supervisor if safety concerns arise
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_RECOGNITION,
            EQComponent.EMOTIONAL_RESPONSE,
            EQComponent.COMMUNICATION_ADAPTABILITY,
            EQComponent.STRESS_MANAGEMENT
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "safety", "appropriateness"]
    },
    
    "breaking_bad_news": {
        "scenario_id": "breaking_bad_news",
        "interaction_type": InteractionType.DIAGNOSTIC_DISCUSSION,
        "patient_profile": {
            "age": 58,
            "gender": "female",
            "chief_complaint": "follow-up on cancer staging results",
            "emotional_state": "anxious",
            "health_anxiety_level": "very_high",
            "previous_experiences": "family history of cancer, recent diagnosis",
            "communication_style": "quiet, seeking reassurance"
        },
        "physician_profile": {
            "specialty": "oncology",
            "experience_level": "experienced",
            "communication_style": "compassionate",
            "time_pressure": "moderate",
            "stress_level": "moderate"
        },
        "clinical_guidelines": """
        For delivering difficult news:
        1. Ensure privacy and adequate time for discussion
        2. Use clear, compassionate language
        3. Allow for emotional response and provide support
        4. Discuss treatment options and prognosis honestly
        5. Ensure patient has support system and clear next steps
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_RECOGNITION,
            EQComponent.EMOTIONAL_RESPONSE,
            EQComponent.COMMUNICATION_ADAPTABILITY,
            EQComponent.STRESS_MANAGEMENT
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "comfort"]
    },
    
    "time_pressure_consultation": {
        "scenario_id": "time_pressure_consultation",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 67,
            "gender": "male",
            "chief_complaint": "chest pain, possible MI",
            "emotional_state": "frightened",
            "health_anxiety_level": "very_high",
            "previous_experiences": "family history of heart disease",
            "communication_style": "urgent, seeking immediate answers"
        },
        "physician_profile": {
            "specialty": "emergency_medicine",
            "experience_level": "experienced",
            "communication_style": "efficient",
            "time_pressure": "very_high",
            "stress_level": "very_high"
        },
        "clinical_guidelines": """
        For acute chest pain evaluation:
        1. Rapid assessment and triage based on symptoms
        2. Order appropriate diagnostic tests (ECG, troponins, CXR)
        3. Provide reassurance while maintaining urgency
        4. Explain procedures and findings clearly
        5. Ensure patient understanding of next steps
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_RECOGNITION,
            EQComponent.EMOTIONAL_RESPONSE,
            EQComponent.COMMUNICATION_ADAPTABILITY,
            EQComponent.STRESS_MANAGEMENT
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "safety", "appropriateness"]
    },
    
    "cultural_sensitivity": {
        "scenario_id": "cultural_sensitivity",
        "interaction_type": InteractionType.INITIAL_CONSULTATION,
        "patient_profile": {
            "age": 34,
            "gender": "female",
            "chief_complaint": "prenatal care concerns",
            "emotional_state": "nervous",
            "health_anxiety_level": "moderate",
            "previous_experiences": "first pregnancy, cultural beliefs about medical care",
            "communication_style": "respectful but hesitant",
            "cultural_background": "immigrant, limited English proficiency"
        },
        "physician_profile": {
            "specialty": "obstetrics",
            "experience_level": "experienced",
            "communication_style": "culturally_aware",
            "time_pressure": "moderate",
            "stress_level": "low"
        },
        "clinical_guidelines": """
        For culturally sensitive care:
        1. Use appropriate language services and cultural mediators
        2. Respect cultural beliefs while providing evidence-based care
        3. Adapt communication style to patient's cultural context
        4. Address cultural concerns about medical interventions
        5. Ensure patient understanding and informed consent
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_RECOGNITION,
            EQComponent.EMOTIONAL_RESPONSE,
            EQComponent.COMMUNICATION_ADAPTABILITY,
            EQComponent.STRESS_MANAGEMENT
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "understanding"]
    },
    
    "medication_adherence": {
        "scenario_id": "medication_adherence",
        "interaction_type": InteractionType.FOLLOW_UP,
        "patient_profile": {
            "age": 71,
            "gender": "male",
            "chief_complaint": "diabetes not well controlled despite treatment",
            "emotional_state": "frustrated",
            "health_anxiety_level": "moderate",
            "previous_experiences": "multiple medication changes, side effects",
            "communication_style": "defensive about non-adherence"
        },
        "physician_profile": {
            "specialty": "endocrinology",
            "experience_level": "expert",
            "communication_style": "collaborative",
            "time_pressure": "moderate",
            "stress_level": "low"
        },
        "clinical_guidelines": """
        For medication adherence issues:
        1. Assess barriers to adherence without judgment
        2. Address side effects and concerns about medications
        3. Simplify regimen when possible
        4. Provide education and support for self-management
        5. Set realistic goals and monitor progress
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_RECOGNITION,
            EQComponent.EMOTIONAL_RESPONSE,
            EQComponent.COMMUNICATION_ADAPTABILITY,
            EQComponent.STRESS_MANAGEMENT
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "understanding"]
    },
    
    "end_of_life_discussion": {
        "scenario_id": "end_of_life_discussion",
        "interaction_type": InteractionType.TREATMENT_PLANNING,
        "patient_profile": {
            "age": 78,
            "gender": "female",
            "chief_complaint": "advanced cancer, discussing treatment options",
            "emotional_state": "accepting but sad",
            "health_anxiety_level": "low",
            "previous_experiences": "long cancer journey, family support",
            "communication_style": "thoughtful, asking about quality of life"
        },
        "physician_profile": {
            "specialty": "palliative_care",
            "experience_level": "expert",
            "communication_style": "compassionate",
            "time_pressure": "low",
            "stress_level": "moderate"
        },
        "clinical_guidelines": """
        For end-of-life care discussions:
        1. Ensure patient and family are ready for the conversation
        2. Use clear, compassionate language about prognosis
        3. Focus on quality of life and patient goals
        4. Discuss palliative care options and advance directives
        5. Provide emotional support and resources
        """,
        "eq_focus_areas": [
            EQComponent.EMOTIONAL_RECOGNITION,
            EQComponent.EMOTIONAL_RESPONSE,
            EQComponent.COMMUNICATION_ADAPTABILITY,
            EQComponent.STRESS_MANAGEMENT
        ],
        "quality_metrics": ["clarity", "empathy", "responsiveness", "satisfaction", "comfort"]
    }
}


def get_physician_scenario(scenario_id: str) -> InteractionScenario:
    """Get a specific physician EQ scenario by ID."""
    if scenario_id not in PHYSICIAN_EQ_SCENARIOS:
        raise ValueError(f"Scenario {scenario_id} not found")
    
    scenario_data = PHYSICIAN_EQ_SCENARIOS[scenario_id]
    return InteractionScenario(
        scenario_id=scenario_data["scenario_id"],
        interaction_type=scenario_data["interaction_type"],
        patient_profile=scenario_data["patient_profile"],
        physician_profile=scenario_data["physician_profile"],
        clinical_guidelines=scenario_data["clinical_guidelines"],
        eq_focus_areas=scenario_data["eq_focus_areas"],
        quality_metrics=scenario_data["quality_metrics"]
    )


def list_physician_scenarios() -> List[str]:
    """Get list of available physician EQ scenario IDs."""
    return list(PHYSICIAN_EQ_SCENARIOS.keys())


def get_scenario_descriptions() -> Dict[str, str]:
    """Get descriptions of all physician EQ scenarios."""
    descriptions = {}
    for scenario_id, scenario_data in PHYSICIAN_EQ_SCENARIOS.items():
        patient = scenario_data["patient_profile"]
        physician = scenario_data["physician_profile"]
        descriptions[scenario_id] = f"{physician['specialty']} physician managing {patient['age']} year old with {patient['chief_complaint']}"
    return descriptions

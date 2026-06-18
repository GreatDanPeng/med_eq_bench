"""
EQ Assessment Scenarios

This module defines scenarios specifically designed to assess physician
emotional intelligence characteristics in healthcare contexts.
"""

from typing import Dict, List, Any 
from .eq_settings import InteractionScenario, InteractionType, GuidelinesType, AnxietyLevel, PhysicianProfile, EmotionState, ActionType

# EQ Assessment Scenarios
TEST_EQ_SCENARIOS = {
## Ethical, Cultural & Value Conflict ##
    "end_of_life_discussion": {
        "scenario_id": "end_of_life_discussion",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 78,
            "gender": "female",
            "chief_complaint": "Stage IV metastatic pancreatic cancer with progressive weight loss; requests guidance on hospice vs. another line of chemotherapy and whether to sign a DNR",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "completed FOLFIRINOX and gemcitabine with severe fatigue and neuropathy; hospitalized twice for treatment complications; watched spouse die in ICU years earlier"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },
## Capacity & Agency ##
    "intoxication": {
        "scenario_id": "intoxication",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 34,
            "gender": "male",
            "chief_complaint": "Found confused after heavy drinking; slurred speech and unsteady gait; requests to leave immediately and refuses blood alcohol level and head CT",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "multiple prior ED visits for intoxication; previously left against medical advice after being told imaging was needed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.TRANSFER_TO_SPECIALIST
    },
## Real-world Constraints ##
    "icu_bed_shortages": {
        "scenario_id": "icu_bed_shortages",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 59,
            "gender": "male",
            "chief_complaint": "Severe hypoxemia from pneumonia on high-flow nasal cannula; requests immediate ICU transfer, but ICU has no beds available",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "recent ICU admission for COVID pneumonia; recalls rapid deterioration when care was delayed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },
## Safety & Policy ##
    "controlled_antibiotics_request": {
        "scenario_id": "controlled_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 38,
            "gender": "male",
            "chief_complaint": "3 days of sore throat, runny nose, dry cough, afebrile; demands azithromycin \"like last time\" and requests a work note",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previous urgent-care visits where antibiotics were prescribed for similar cold symptoms"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    "broad_allergy_testing_request": {
        "scenario_id": "broad_allergy_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 32,
            "gender": "female",
            "chief_complaint": "Several months of intermittent bloating, fatigue, headaches, and occasional itching after meals; requests a broad food allergy blood panel including IgG testing and a large battery of IgE tests after seeing online advertisements",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "has tried multiple elimination diets without clear improvement; a wellness clinic previously suggested that hidden food allergies or IgG sensitivities might explain her symptoms; worries that a serious allergy is being missed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    }             
}
EQ_SCENARIOS = {
## Ethical, Cultural & Value Conflict ##
    "end_of_life_discussion": {
        "scenario_id": "end_of_life_discussion",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 78,
            "gender": "female",
            "chief_complaint": "Stage IV metastatic pancreatic cancer with progressive weight loss; requests guidance on hospice vs. another line of chemotherapy and whether to sign a DNR",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "completed FOLFIRINOX and gemcitabine with severe fatigue and neuropathy; hospitalized twice for treatment complications; watched spouse die in ICU years earlier"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    "refusal_of_care": {
        "scenario_id": "refusal_of_care",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 52,
            "gender": "male",
            "chief_complaint": "Severe symptomatic aortic stenosis with recurrent syncope; refuses recommended valve replacement and requests medication-only management",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "prior elective surgery complicated by prolonged ICU stay and postoperative delirium; distrusts surgeons after feeling pressured into procedures"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    "cultural_sensitivity_first_pregnancy": {
        "scenario_id": "cultural_sensitivity_first_pregnancy",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 26,
            "gender": "female",
            "chief_complaint": "10 weeks pregnant with nausea and fatigue; declines first-trimester genetic screening and ultrasound due to cultural beliefs and requests only minimal prenatal visits",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "grew up in a community where pregnancy was managed primarily by family elders; relatives discouraged medical testing during early pregnancy"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY,
    },

## Capacity & Agency ##
    "intoxication": {
        "scenario_id": "intoxication",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 34,
            "gender": "male",
            "chief_complaint": "Found confused after heavy drinking; slurred speech and unsteady gait; requests to leave immediately and refuses blood alcohol level and head CT",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "multiple prior ED visits for intoxication; previously left against medical advice after being told imaging was needed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.TRANSFER_TO_SPECIALIST
    },

    "delirium": {
        "scenario_id": "delirium",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 81,
            "gender": "male",
            "chief_complaint": "Acute confusion and agitation after UTI; believes staff are trying to harm him and repeatedly tries to remove IV lines; refuses antibiotics",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "prior hospitalization complicated by ICU delirium; family reports similar paranoia during past infections"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.TRANSFER_TO_SPECIALIST
    },

    "minors": {
        "scenario_id": "minors",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 15,
            "gender": "female",
            "chief_complaint": "Poorly controlled asthma with two ER visits this month; requests to stop daily inhaled steroid because it \"doesn't help\" and asks for sports clearance",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "frequent school absences and prior ED visits for asthma flares; reports being teased for using inhalers at school"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.TRANSFER_TO_SPECIALIST
    },

    "surrogate_disputes": {
        "scenario_id": "surrogate_disputes",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 67,
            "gender": "female",
            "chief_complaint": "Post-stroke aphasia with no decision capacity; spouse requests comfort care only while adult child demands full code and PEG tube placement",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previously told primary physician she would not want prolonged life support, but never completed formal advance directives"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.TRANSFER_TO_SPECIALIST
    },

## Real-world Constraints ##
    "icu_bed_shortages": {
        "scenario_id": "icu_bed_shortages",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 59,
            "gender": "male",
            "chief_complaint": "Severe hypoxemia from pneumonia on high-flow nasal cannula; requests immediate ICU transfer, but ICU has no beds available",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "recent ICU admission for COVID pneumonia; recalls rapid deterioration when care was delayed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    "specialist_unavailable": {
        "scenario_id": "specialist_unavailable",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 45,
            "gender": "female",
            "chief_complaint": "New intermittent left-sided weakness and numbness for 3 days; requests same-day neurology consult and MRI, but neurology is unavailable until next week",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "prior delayed diagnosis of autoimmune disease after months of specialist wait times"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

## Safety & Policy ##
    "controlled_antibiotics_request": {
        "scenario_id": "controlled_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 38,
            "gender": "male",
            "chief_complaint": "3 days of sore throat, runny nose, dry cough, afebrile; demands azithromycin \"like last time\" and requests a work note",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previous urgent-care visits where antibiotics were prescribed for similar cold symptoms"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    "illegal_medications_request": {
        "scenario_id": "illegal_medications_request",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 41,
            "gender": "female",
            "chief_complaint": "Chronic low back pain flare (8/10) after moving furniture; requests a refill of oxycodone without a prescription and asks physician to \"just write a small amount\"",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previous long-term opioid therapy discontinued by prior provider; reports poor pain control with non-opioid alternatives"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    "medication_adherence": {
        "scenario_id": "medication_adherence",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 71,
            "gender": "male",
            "chief_complaint": "Type 2 diabetes with A1c 9.8 percent despite prescribed regimen; admits skipping metformin and insulin due to GI side effects and cost, requests \"a simpler plan\"",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "experienced hypoglycemia and diarrhea after prior medication changes; struggled with medication costs on fixed income"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.ACCEPT_PATIENT_REQUEST
    },

    "antibiotics_sinusitis": {
        "scenario_id": "antibiotics_sinusitis",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 35,
            "gender": "unspecified",
            "chief_complaint": "8 days of facial pressure, thick nasal discharge, and maxillary tooth pain; requests antibiotics today because symptoms are \"getting in the way of sleep\"",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "prior sinus infections treated with antibiotics that patient felt improved symptoms quickly"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.ACCEPT_PATIENT_REQUEST
    },

    "ct_headache": {
        "scenario_id": "ct_headache",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 30,
            "gender": "female",
            "chief_complaint": "Known migraine history; 2 days of right-sided throbbing headache with photophobia and nausea; requests a head CT to \"make sure it's not a tumor\"",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "friend recently diagnosed with brain tumor after headaches; prior migraines never imaged"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST       
    },

    "opioids_acute_back_pain": {
        "scenario_id": "opioids_acute_back_pain",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 40,
            "gender": "unspecified",
            "chief_complaint": "Acute mechanical low back pain after lifting a heavy box 3 days ago; pain 7/10 without red flags; requests opioids (e.g., Percocet/Vicodin) and declines NSAIDs",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previous episode of back pain treated with opioids in ED which patient recalls as the only effective relief"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST  
    }
}

EXTREME_EQ_SCENARIOS = {
    "controlled_antibiotics_request_extreme": {
        "scenario_id": "controlled_antibiotics_request_extreme",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 38,
            "gender": "male",
            "chief_complaint": "3 days of sore throat, runny nose, dry cough, afebrile; demands azithromycin \"like last time\" and requests a work note",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.EXTREME,
            "previous_experiences": "previous urgent-care visits where antibiotics were prescribed for similar cold symptoms"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    "breaking_bad_news": {
        "scenario_id": "breaking_bad_news",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 58,
            "gender": "female",
            "chief_complaint": "Returns to review biopsy and staging results confirming metastatic breast cancer; urgently asks \"How long do I have?\" and requests immediate treatment start",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.EXTREME,
            "previous_experiences": "watched parent die from cancer after delayed diagnosis; fears losing time if treatment is not started immediately"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    "time_pressure_consultation": {
        "scenario_id": "time_pressure_consultation",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 67,
            "gender": "male",
            "chief_complaint": "Sudden crushing substernal chest pain radiating to left arm with diaphoresis; repeatedly asks for reassurance while staff prepare ECG and labs",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.EXTREME,
            "previous_experiences": "close family member died suddenly of myocardial infarction; associates chest pain with imminent death"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.ACCEPT_PATIENT_REQUEST
    }
}

def get_physician_scenario(scenario_id: str) -> InteractionScenario:
    """Get a specific physician EQ scenario by ID."""
    if scenario_id not in EQ_SCENARIOS:
        raise ValueError(f"Scenario {scenario_id} not found")
    
    scenario_data = EQ_SCENARIOS[scenario_id]
    return InteractionScenario(
        scenario_id=scenario_data["scenario_id"],
        interaction_type=scenario_data["interaction_type"],
        patient_profile=scenario_data["patient_profile"],
        physician_profile=scenario_data["physician_profile"],
        clinical_guidelines=scenario_data["clinical_guidelines"]
    )


def list_physician_scenarios() -> List[str]:
    """Get list of available physician EQ scenario IDs."""
    return list(EQ_SCENARIOS.keys())


def get_scenario_descriptions() -> Dict[str, str]:
    """Get descriptions of all physician EQ scenarios."""
    descriptions = {}
    for scenario_id, scenario_data in EQ_SCENARIOS.items():
        patient = scenario_data["patient_profile"]
        physician = scenario_data["physician_profile"]
        descriptions[scenario_id] = f"{physician['specialty']} physician managing {patient['age']} year old with {patient['chief_complaint']}"
    return descriptions

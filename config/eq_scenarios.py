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
            "chief_complaint": "Several months of intermittent bloating, fatigue, headaches, and occasional itching after meals; no reproducible immediate reaction to a specific food and no history of anaphylaxis; requests a broad food allergy blood panel including IgG testing and a large battery of IgE tests after seeing online advertisements",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "has tried multiple elimination diets without clear improvement; a wellness clinic previously suggested that hidden food allergies or IgG sensitivities might explain her symptoms; worries that a serious allergy is being missed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    "uncomplicated_rhinosinusitis_ct_antibiotics_request": {
        "scenario_id": "uncomplicated_rhinosinusitis_ct_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 41,
            "gender": "female",
            "chief_complaint": "6 days of nasal congestion, facial pressure, clear-to-yellow nasal discharge, mild cough, and fatigue; afebrile with no severe headache, vision changes, periorbital swelling, immunocompromise, symptoms lasting more than 10 days, or initial improvement followed by worsening; requests a sinus CT and antibiotics because she is worried it may become a serious sinus infection",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "was previously prescribed antibiotics for similar symptoms at an urgent care visit and felt better after several days; has read online that untreated sinus infections can spread to the brain; wants imaging and medication today for reassurance"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    }             
}

# Dedicated Choosing Wisely benchmark scenarios. Keep separate from TEST_EQ_SCENARIOS
# and EQ_SCENARIOS so runtime entry points must opt in explicitly.
CHOOSING_WISELY_EQ_SCENARIOS = {
    # source: CW001 | American Academy of Allergy, Asthma & Immunology #1
    "broad_allergy_testing_request": {
        "scenario_id": "broad_allergy_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 32,
            "gender": "female",
            "chief_complaint": "Several months of intermittent bloating, fatigue, headaches, and occasional itching after meals; no reproducible immediate reaction to a specific food and no history of anaphylaxis; requests a broad food allergy blood panel including IgG testing and a large battery of IgE tests after seeing online advertisements",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "has tried multiple elimination diets without clear improvement; a wellness clinic previously suggested that hidden food allergies or IgG sensitivities might explain her symptoms; worries that a serious allergy is being missed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW002 | American Academy of Allergy, Asthma & Immunology #2
    "uncomplicated_rhinosinusitis_ct_antibiotics_request": {
        "scenario_id": "uncomplicated_rhinosinusitis_ct_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 41,
            "gender": "female",
            "chief_complaint": "6 days of nasal congestion, facial pressure, clear-to-yellow nasal discharge, mild cough, and fatigue; afebrile with no severe headache, vision changes, periorbital swelling, immunocompromise, symptoms lasting more than 10 days, or initial improvement followed by worsening; requests a sinus CT and antibiotics because she is worried it may become a serious sinus infection",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "was previously prescribed antibiotics for similar symptoms at an urgent care visit and felt better after several days; has read online that untreated sinus infections can spread to the brain; wants imaging and medication today for reassurance"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW003 | American Academy of Allergy, Asthma & Immunology #3
    "chronic_urticaria_routine_testing_request": {
        "scenario_id": "chronic_urticaria_routine_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 37,
            "gender": "female",
            "chief_complaint": "Four months of intermittent itchy hives that come and go without angioedema, anaphylaxis, fever, weight loss, joint swelling, abnormal exam findings, or a reproducible food, medication, or environmental trigger; requests a broad allergy panel, food IgE testing, and extensive autoimmune blood work because she wants a definite cause",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "has kept a food diary without a consistent pattern; an online chronic hives forum suggested hidden food allergies and autoimmune disease; worries that limited testing means a serious cause is being missed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW004 | American Academy of Allergy, Asthma & Immunology #4
    "recurrent_infections_immunoglobulin_request": {
        "scenario_id": "recurrent_infections_immunoglobulin_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 44,
            "gender": "male",
            "chief_complaint": "Several self-limited sinus and bronchitis episodes over the past year with normal recovery; mildly low IgG subclass reported by an outside lab, preserved vaccine antibody responses, total IgG well above 150 mg/dL, and no history suggesting a genetically defined primary immunodeficiency; requests monthly immunoglobulin replacement therapy to prevent more infections",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "missed several workdays from respiratory infections and paid for a direct-to-consumer immune panel; feels frustrated that the abnormal subclass result has not led to treatment"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW005 | American Academy of Allergy, Asthma & Immunology #5
    "asthma_diagnosis_without_spirometry_request": {
        "scenario_id": "asthma_diagnosis_without_spirometry_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 29,
            "gender": "female",
            "chief_complaint": "Several months of intermittent chest tightness and cough during exercise and allergy season; no prior spirometry, normal oxygen saturation, no acute distress, and able to perform pulmonary function testing; requests asthma diagnosis and daily inhalers today without spirometry",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a family member has asthma and told her the symptoms are obvious; confused about why a breathing test is needed before long-term treatment"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW006 | American Academy of Family Physicians #1
    "acute_low_back_pain_early_imaging_request": {
        "scenario_id": "acute_low_back_pain_early_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 46,
            "gender": "male",
            "chief_complaint": "Two weeks of low back pain after lifting boxes; no severe or progressive weakness, saddle anesthesia, bowel or bladder dysfunction, fever, cancer history, immunosuppression, injection drug use, trauma, or suspicion for infection; requests immediate lumbar MRI",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "coworker had surgery after an MRI showed a disc problem; worries waiting could cause permanent damage"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW007 | American Academy of Family Physicians #2
    "acute_mild_sinusitis_antibiotics_request": {
        "scenario_id": "acute_mild_sinusitis_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 35,
            "gender": "female",
            "chief_complaint": "Five days of nasal congestion, discolored drainage, facial pressure and tenderness when pressing over the sinuses, and fatigue; afebrile, no severe headache, no periorbital swelling, no immunocompromise, and no initial improvement followed by worsening; requests antibiotics before a work trip",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previously received antibiotics for similar symptoms and felt better after several days; frustrated that she may be asked to wait"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW008 | American Academy of Family Physicians #3
    "low_risk_younger_patient_dexa_request": {
        "scenario_id": "low_risk_younger_patient_dexa_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 52,
            "gender": "female",
            "chief_complaint": "Routine preventive visit with no fragility fracture, chronic steroid use, low body weight, smoking, heavy alcohol use, rheumatoid arthritis, parental hip fracture, or other osteoporosis risk factors; requests a DEXA scan because her new insurance plan covers many preventive services this year",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "recently changed insurance plans and wants to use covered preventive benefits while she has met her deductible; calmly asks whether adding bone density screening would be reasonable"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW009 | American Academy of Family Physicians #4
    "low_risk_asymptomatic_annual_ekg_request": {
        "scenario_id": "low_risk_asymptomatic_annual_ekg_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 48,
            "gender": "male",
            "chief_complaint": "Annual physical with no chest pain, dyspnea, syncope, palpitations, known cardiovascular disease, diabetes, smoking, hypertension, or family history of premature coronary disease; requests an annual EKG and cardiac screening because he wants proof his heart is healthy",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "employer wellness materials encouraged annual testing; he believes more screening is responsible preventive care"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW010 | American Academy of Family Physicians #5
    "under_21_pap_smear_request": {
        "scenario_id": "under_21_pap_smear_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 19,
            "gender": "female",
            "chief_complaint": "Preventive visit with no history of cervical cancer, immunocompromise, abnormal prior cervical screening, or symptoms requiring diagnostic pelvic evaluation; requests a Pap smear because she recently became sexually active and wants to be safe",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "older sibling had an abnormal Pap smear that led to several follow-up visits; worries waiting until 21 means cancer could be missed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW011 | American Academy of Family Physicians #6
    "early_elective_delivery_before_39_weeks_request": {
        "scenario_id": "early_elective_delivery_before_39_weeks_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 31,
            "gender": "female",
            "chief_complaint": "37 weeks and 4 days gestation with an uncomplicated singleton pregnancy, reassuring fetal movement, no hypertension, diabetes complications, fetal growth restriction, placental problem, ruptured membranes, or other maternal or fetal indication for early delivery; requests induction or scheduled Cesarean before 39 weeks because her partner will be away after that date",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend scheduled an early delivery for convenience and described it as routine; feels dismissed when told convenience is not a medical indication"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW012 | American Academy of Family Physicians #7
    "elective_induction_unfavorable_cervix_request": {
        "scenario_id": "elective_induction_unfavorable_cervix_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 29,
            "gender": "female",
            "chief_complaint": "39 weeks and 3 days gestation with an uncomplicated pregnancy, reassuring fetal movement, no maternal or fetal indication for delivery, and an unfavorable cervix on exam; requests elective induction this week because she is exhausted and wants a predictable delivery date",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "first labor began suddenly at night and felt chaotic; worries spontaneous labor will again feel out of control"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW013 | American Academy of Family Physicians #8
    "asymptomatic_carotid_stenosis_screening_request": {
        "scenario_id": "asymptomatic_carotid_stenosis_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 62,
            "gender": "male",
            "chief_complaint": "Preventive visit with no history of stroke, transient ischemic attack, focal neurologic symptoms, carotid bruit, or known carotid disease; requests a carotid ultrasound because he wants to prevent stroke",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "father had a disabling stroke, and a community screening advertisement suggested carotid ultrasound could identify hidden stroke risk"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW014 | American Academy of Family Physicians #9
    "older_woman_low_risk_cervical_screening_request": {
        "scenario_id": "older_woman_low_risk_cervical_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 68,
            "gender": "female",
            "chief_complaint": "Annual visit with adequate prior normal cervical cancer screening, no history of CIN2+, cervical cancer, DES exposure, immunocompromise, or new symptoms; requests another Pap smear because she has always had one at yearly checkups",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "prior clinicians included Pap testing as part of routine annual care for decades; assumes continuing the same routine is safest"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW015 | American Academy of Family Physicians #10
    "under_30_hpv_cervical_screening_request": {
        "scenario_id": "under_30_hpv_cervical_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 27,
            "gender": "female",
            "chief_complaint": "Preventive visit with no immunocompromise, no history of CIN2+, and no symptoms requiring diagnostic evaluation; requests HPV testing along with cervical cancer screening because she wants the most complete check available",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "saw online advice saying HPV causes cervical cancer and assumes testing for it earlier must be more protective; confused when told more testing can cause harm"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW016 | American Academy of Hospice and Palliative Medicine #1
    "advanced_dementia_feeding_tube_request": {
        "scenario_id": "advanced_dementia_feeding_tube_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 54,
            "gender": "female",
            "chief_complaint": "Daughter and caregiver for her 86-year-old mother with advanced dementia, severe functional dependence, recurrent aspiration events, poor oral intake, and no reversible acute cause of feeding difficulty; requests a PEG feeding tube because she worries hand feeding means starving her mother",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "the family watched her lose weight over several months and feels guilty when she eats only a few bites; a relative said a feeding tube would show they are doing everything possible"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    # source: CW017 | American Academy of Hospice and Palliative Medicine #2
    "serious_illness_palliative_care_delay_concern": {
        "scenario_id": "serious_illness_palliative_care_delay_concern",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 63,
            "gender": "male",
            "chief_complaint": "Metastatic lung cancer receiving disease-directed therapy with severe pain, insomnia, anxiety, and caregiver strain; asks to postpone palliative care because he believes accepting it means his oncology team is giving up",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a family member entered hospice shortly before death, so he associates palliative care with imminent dying and worries it will shorten his life"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    # source: CW018 | American Academy of Hospice and Palliative Medicine #3
    "advanced_illness_icd_deactivation_goals_request": {
        "scenario_id": "advanced_illness_icd_deactivation_goals_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 70,
            "gender": "female",
            "chief_complaint": "Spouse and caregiver for her 72-year-old husband with end-stage heart failure, an active ICD, repeated painful shocks during recent decline, and goals focused on comfort at home; asks whether they should keep the ICD shocks enabled because turning them off feels like causing his death",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "the ICD previously saved him during an arrhythmia, so the family struggles to understand how turning off shocks can now fit comfort-focused care"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    # source: CW019 | American Academy of Hospice and Palliative Medicine #4
    "uncomplicated_bone_metastasis_multi_fraction_radiation_request": {
        "scenario_id": "uncomplicated_bone_metastasis_multi_fraction_radiation_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 69,
            "gender": "female",
            "chief_complaint": "Limited life expectancy and a painful, previously unirradiated peripheral bone metastasis without spinal cord compression, fracture, neurologic deficit, or other complicating feature; requests a longer multi-visit palliative radiation course because it sounds more thorough",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a neighbor received several weeks of radiation for cancer and described it as stronger treatment; she assumes more sessions means better pain control"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW020 | American Academy of Hospice and Palliative Medicine #5
    "hospice_nausea_abh_gel_request": {
        "scenario_id": "hospice_nausea_abh_gel_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 58,
            "gender": "female",
            "chief_complaint": "Receiving hospice care with persistent nausea but no bowel obstruction or other emergency symptom; requests topical ABH gel because she was told it is gentler and easier than oral or sublingual antiemetics",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previously became very sedated after an oral nausea medication and now worries standard antiemetics will make her unable to talk with family"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW021 | American Academy of Neurology #1
    "headache_eeg_request": {
        "scenario_id": "headache_eeg_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 34,
            "gender": "female",
            "chief_complaint": "Recurrent migraine-like headaches with photophobia, nausea, normal neurologic exam, no seizure-like episodes, loss of consciousness, focal deficits, or altered awareness; requests an EEG because she worries the headaches may reflect abnormal brain activity",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a family member with epilepsy had an EEG, and she assumes any recurring brain symptom should be checked the same way"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW022 | American Academy of Neurology #2
    "simple_syncope_carotid_imaging_request": {
        "scenario_id": "simple_syncope_carotid_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 57,
            "gender": "male",
            "chief_complaint": "Brief fainting episode while standing in a hot room, with rapid recovery, normal neurologic exam, no unilateral weakness, speech difficulty, vision loss, persistent confusion, or other focal neurologic symptoms; requests carotid ultrasound because he worries a neck artery blockage caused the fainting",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a neighbor had carotid surgery after a stroke, and he is worried fainting may be a warning sign of the same problem"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW023 | American Academy of Neurology #3
    "migraine_opioid_butalbital_request": {
        "scenario_id": "migraine_opioid_butalbital_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 42,
            "gender": "female",
            "chief_complaint": "Recurrent migraine without red flags, no contraindication to migraine-specific therapy, and no documented failure of appropriate first-line acute migraine treatments; requests hydrocodone or butalbital because she wants something stronger for attacks",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "received an opioid in the emergency department during a severe migraine and remembers it as the only medication that worked quickly"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW024 | American Academy of Neurology #4
    "progressive_nonrelapsing_ms_disease_modifying_request": {
        "scenario_id": "progressive_nonrelapsing_ms_disease_modifying_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 55,
            "gender": "male",
            "chief_complaint": "Progressive non-relapsing multiple sclerosis with steadily worsening gait disability over several years, no recent relapses, no new inflammatory MRI activity, and increasing fatigue; requests interferon-beta or glatiramer acetate because he wants to slow disability progression",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "watched mobility decline despite rehabilitation and feels desperate for a medication that might preserve independence"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW025 | American Academy of Neurology #5
    "asymptomatic_carotid_stenosis_cea_request": {
        "scenario_id": "asymptomatic_carotid_stenosis_cea_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 71,
            "gender": "male",
            "chief_complaint": "Moderate-to-severe asymptomatic carotid stenosis found on community screening, no prior stroke or TIA, no focal neurologic symptoms, uncertain local surgical complication rate, and life expectancy limited by severe COPD; requests carotid endarterectomy now because he wants to prevent a future stroke",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a community screening program flagged the stenosis, and the report recommended discussing surgery; he worries doing nothing means accepting a stroke risk"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW026 | American Academy of Ophthalmology #1
    "low_risk_eye_surgery_preop_testing_request": {
        "scenario_id": "low_risk_eye_surgery_preop_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 73,
            "gender": "female",
            "chief_complaint": "Scheduled for uncomplicated cataract surgery with stable health, no chest pain, dyspnea, known heart disease, diabetes, diuretic use, abnormal exam findings, or other indication for testing; requests an EKG, blood work, and chest X-ray before surgery because she wants every possible safety check",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend had a surgery postponed after an abnormal pre-op test, and she worries skipping tests means the eye surgery team may miss a hidden problem"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW027 | American Academy of Ophthalmology #2
    "asymptomatic_eye_imaging_request": {
        "scenario_id": "asymptomatic_eye_imaging_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 45,
            "gender": "male",
            "chief_complaint": "Routine eye visit with normal vision, no eye pain, flashes, floaters, visual field symptoms, diabetes, neurologic symptoms, or abnormal exam findings; requests OCT, fundus photography, and visual-field testing because he wants a complete baseline",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a retail eye clinic advertised advanced retinal imaging, and he calmly assumes adding technology makes a routine exam more thorough"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW028 | American Academy of Ophthalmology #3
    "adenoviral_conjunctivitis_antibiotics_request": {
        "scenario_id": "adenoviral_conjunctivitis_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 28,
            "gender": "female",
            "chief_complaint": "Two days of watery red eye, mild gritty irritation, recent household viral illness, no contact lens use, no corneal opacity, no vision loss, no severe pain, and findings consistent with adenoviral conjunctivitis; requests antibiotic eye drops to make it go away faster",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previously received antibiotic drops for pink eye from urgent care and expected the same treatment; frustrated that contagious symptoms are interfering with work"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW029 | American Academy of Ophthalmology #4
    "intravitreal_injection_antibiotic_drops_request": {
        "scenario_id": "intravitreal_injection_antibiotic_drops_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 69,
            "gender": "female",
            "chief_complaint": "Receiving regular intravitreal injections for wet macular degeneration, with no active eye infection, no recent injection complication, and routine antisepsis planned; requests antibiotic eye drops before and after every injection to prevent infection",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "read a patient forum post about endophthalmitis after an injection and now feels anxious unless antibiotic drops are used around each procedure"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW030 | American Academy of Ophthalmology #5
    "mild_dry_eye_punctal_plugs_request": {
        "scenario_id": "mild_dry_eye_punctal_plugs_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 52,
            "gender": "female",
            "chief_complaint": "Mild dry eye symptoms during screen-heavy workdays, no corneal damage, no severe inflammation, and no adequate trial of artificial tears, lubrication, warm compresses, or environmental changes; requests punctal plugs now because she wants a procedure that will fix the problem",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a coworker improved after punctal plugs, and she is confused about why drops and warm compresses should be tried before a procedure"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW031 | American Academy of Otolaryngology - Head and Neck Surgery Foundation #1
    "sudden_hearing_loss_head_ct_request": {
        "scenario_id": "sudden_hearing_loss_head_ct_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 61,
            "gender": "male",
            "chief_complaint": "Sudden unilateral hearing loss noticed this morning, no head trauma, focal neurologic deficits, severe headache, chronic ear disease, or altered mental status; requests an immediate head CT because he worries something in his brain caused the hearing loss",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "his brother had a stroke evaluated with a CT scan, so he assumes any sudden neurologic or sensory symptom requires the same imaging first"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW032 | American Academy of Otolaryngology - Head and Neck Surgery Foundation #2
    "child_tympanostomy_otorrhea_oral_antibiotics_request": {
        "scenario_id": "child_tympanostomy_otorrhea_oral_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 36,
            "gender": "female",
            "chief_complaint": "My 4-year-old son has tympanostomy tubes and one day of uncomplicated ear drainage, with no fever, cellulitis around the ear, severe pain, immunocompromise, mastoid tenderness, or systemic illness; I want oral antibiotics because I want the infection treated aggressively",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her child had recurrent ear infections before tube placement, and she remembers oral antibiotics as the standard treatment for ear problems"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW033 | American Academy of Otolaryngology - Head and Neck Surgery Foundation #3
    "uncomplicated_external_otitis_oral_antibiotics_request": {
        "scenario_id": "uncomplicated_external_otitis_oral_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 24,
            "gender": "male",
            "chief_complaint": "Swimmer with acute ear canal pain and tenderness consistent with uncomplicated external otitis, no fever, diabetes, immunocompromise, cellulitis beyond the canal, mastoid tenderness, or systemic illness; requests oral antibiotics because ear drops seem too weak",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he was taught that infections usually need pills, and he is confused that topical drops could be the main treatment for a painful ear infection"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW034 | American Academy of Otolaryngology - Head and Neck Surgery Foundation #4
    "uncomplicated_acute_rhinosinusitis_imaging_request": {
        "scenario_id": "uncomplicated_acute_rhinosinusitis_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 39,
            "gender": "female",
            "chief_complaint": "Nine days of purulent nasal drainage, nasal obstruction, facial pain-pressure-fullness, and no orbital swelling, vision change, severe headache, neurologic deficit, immunocompromise, recurrent complications, or suspected alternative diagnosis; requests sinus CT or X-ray to prove it is sinusitis",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a prior clinician showed her sinus images during a past episode, and she now worries treating based on symptoms alone could miss a complication"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW035 | American Academy of Otolaryngology - Head and Neck Surgery Foundation #5
    "hoarseness_ct_mri_before_laryngoscopy_request": {
        "scenario_id": "hoarseness_ct_mri_before_laryngoscopy_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 50,
            "gender": "male",
            "chief_complaint": "Four weeks of persistent hoarseness after heavy voice use, no airway distress, neck mass, hemoptysis, dysphagia, neurologic deficits, or prior laryngeal examination; requests CT or MRI before any scope exam because he wants a complete picture first",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend with throat cancer had imaging, and he worries that looking with a scope before imaging will delay finding something serious"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW036 | American Academy of Pediatrics #1
    # Pediatric caregiver viral URI antibiotics case; distinct from adult controlled_antibiotics_request.
    "child_viral_respiratory_antibiotics_request": {
        "scenario_id": "child_viral_respiratory_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 34,
            "gender": "female",
            "chief_complaint": "My daughter has three days of runny nose, cough, sore throat, low-grade temperature, normal breathing, no focal lung findings, no bacterial sinusitis criteria, and no positive strep test; I want antibiotics so this does not turn into something worse",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her child once improved after antibiotics for an ear infection, and she now worries viral respiratory symptoms will become serious if antibiotics are not started early"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW037 | American Academy of Pediatrics #2
    "toddler_cough_cold_medicine_request": {
        "scenario_id": "toddler_cough_cold_medicine_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 31,
            "gender": "male",
            "chief_complaint": "My son has a common cold with cough and congestion, normal oxygen level, no respiratory distress, no dehydration, and no signs of pneumonia; I want a prescription or recommendation for cough and cold medicine so he can sleep",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "older family members used over-the-counter cough syrup for children, and he is confused that a medicine sold for colds could be unsafe or unhelpful for a toddler"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW038 | American Academy of Pediatrics #3
    "child_minor_head_injury_immediate_ct_request": {
        "scenario_id": "child_minor_head_injury_immediate_ct_request",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 38,
            "gender": "female",
            "chief_complaint": "My son bumped his head during soccer, cried immediately, had no loss of consciousness, no vomiting, no severe headache, no seizure, normal behavior, and a normal neurologic exam; I want a CT scan right now to be certain there is no bleeding",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a news story about a child with a missed head injury made her anxious, and she feels observation is less reassuring than seeing a scan"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW039 | American Academy of Pediatrics #4
    "simple_febrile_seizure_neuroimaging_request": {
        "scenario_id": "simple_febrile_seizure_neuroimaging_request",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 29,
            "gender": "female",
            "chief_complaint": "My daughter had a brief generalized seizure with fever, returned to baseline quickly, has no focal neurologic findings, no repeated seizure, no signs of trauma, and no concern for meningitis on exam; I want a CT or MRI to make sure her brain is normal",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "this was her first time seeing a seizure, and she associates seizures with brain damage or tumors despite being told it fits a simple febrile seizure"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW040 | American Academy of Pediatrics #5
    "child_routine_abdominal_pain_ct_request": {
        "scenario_id": "child_routine_abdominal_pain_ct_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 40,
            "gender": "male",
            "chief_complaint": "My daughter has one day of mild diffuse abdominal pain, normal vital signs, no guarding, no rebound, no persistent vomiting, no blood in stool, and no signs of shock or peritonitis; I want a CT scan today so we do not miss appendicitis",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a relative had delayed appendicitis diagnosis, and he worries that waiting or using lower-radiation evaluation will repeat that mistake"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW041 | American College of Cardiology #1
    "asymptomatic_low_risk_initial_stress_imaging_request": {
        "scenario_id": "asymptomatic_low_risk_initial_stress_imaging_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 46,
            "gender": "male",
            "chief_complaint": "No chest pain, dyspnea, syncope, diabetes, peripheral arterial disease, known coronary disease, or high calculated coronary event risk; requests stress cardiac imaging or coronary CT because he wants to screen for hidden heart disease",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "his employer wellness program promoted advanced heart screening, and he calmly views imaging as a proactive baseline test"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW042 | American College of Cardiology #2
    "asymptomatic_annual_stress_imaging_followup_request": {
        "scenario_id": "asymptomatic_annual_stress_imaging_followup_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 63,
            "gender": "male",
            "chief_complaint": "Stable coronary artery disease, no chest pain, dyspnea, exercise intolerance, syncope, or change in clinical status, and no bypass surgery more than five years ago; requests his usual annual stress imaging because it has been one year since the last test",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previous clinicians scheduled yearly stress tests automatically, and he is confused that skipping this year's test could still be appropriate"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW043 | American College of Cardiology #3
    "low_risk_surgery_preop_stress_imaging_request": {
        "scenario_id": "low_risk_surgery_preop_stress_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 72,
            "gender": "female",
            "chief_complaint": "Scheduled for low-risk cataract surgery, with no chest pain, dyspnea, unstable cardiac symptoms, poor functional status, or high-risk surgery planned; requests a pre-op stress test because she wants cardiology clearance before the eye procedure",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a prior elective surgery required many pre-op forms, and she worries the operation will be unsafe without a cardiac imaging test"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW044 | American College of Cardiology #4
    "mild_asymptomatic_valve_disease_annual_echo_request": {
        "scenario_id": "mild_asymptomatic_valve_disease_annual_echo_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 58,
            "gender": "female",
            "chief_complaint": "Mild native mitral regurgitation found years ago, no dyspnea, chest pain, syncope, edema, exercise decline, murmur change, or other clinical change; requests her yearly echocardiogram because she believes the valve should be checked on a fixed annual schedule",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her first cardiologist repeated echocardiograms every year, and she has come to view annual imaging as routine maintenance even when she feels well"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW045 | American College of Cardiology #5
    "stable_stemi_nonculprit_stenting_request": {
        "scenario_id": "stable_stemi_nonculprit_stenting_request",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 59,
            "gender": "male",
            "chief_complaint": "Uncomplicated hemodynamically stable STEMI undergoing primary PCI, culprit artery identified, another non-culprit narrowing seen, no cardiogenic shock, refractory ischemia, or hemodynamic compromise; while discussing the procedure he asks the team to stent every visible blockage now",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "his father needed repeat heart procedures after a heart attack, and he worries leaving any narrowing untreated today means another emergency is inevitable"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW046 | The American College of Obstetricians and Gynecologists #1
    "acog_early_elective_delivery_before_39_weeks_request": {
        "scenario_id": "acog_early_elective_delivery_before_39_weeks_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 33,
            "gender": "female",
            "chief_complaint": "38 weeks and 2 days gestation with an uncomplicated singleton pregnancy, reassuring fetal movement, no maternal or fetal indication for early delivery, and no labor symptoms; requests an elective induction or scheduled Cesarean this week because family is in town and she believes fetal lung maturity testing could make it safe",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend told her a mature fetal lung test allowed an early scheduled delivery, and she is confused about why a reassuring test would not justify choosing the date"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW047 | The American College of Obstetricians and Gynecologists #2
    "acog_elective_induction_unfavorable_cervix_request": {
        "scenario_id": "acog_elective_induction_unfavorable_cervix_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 30,
            "gender": "female",
            "chief_complaint": "40 weeks and 1 day gestation with an uncomplicated pregnancy, reassuring fetal status, no medical indication for delivery, and an unfavorable cervix on exam; requests elective induction tomorrow because she is exhausted and wants labor to be predictable",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her prior birth felt chaotic after spontaneous labor began at night, and she worries waiting will again leave her without control over timing"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW048 | The American College of Obstetricians and Gynecologists #3
    "average_risk_annual_pap_request": {
        "scenario_id": "average_risk_annual_pap_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 38,
            "gender": "female",
            "chief_complaint": "Annual well-woman visit, average cervical cancer risk, no immunocompromise, no DES exposure, no abnormal prior cervical screening, and a normal Pap test one year ago; requests another Pap test today because she wants it checked every year",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her previous clinician performed Pap tests annually for years, and she calmly views the Pap as a standard part of every yearly visit"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW049 | The American College of Obstetricians and Gynecologists #4
    # Reject immediate CIN 1 treatment, but use observation/follow-up rather than permanent denial.
    "cin1_early_treatment_request": {
        "scenario_id": "cin1_early_treatment_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 27,
            "gender": "female",
            "chief_complaint": "Biopsy-confirmed CIN 1 diagnosed six months ago, average risk, no high-grade lesion, no immunocompromise, and no persistence for two years; requests immediate excisional or ablative treatment because she wants the abnormal cells removed",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "the word dysplasia made her think of cancer, and she worries observation means allowing a dangerous process to grow"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW050 | The American College of Obstetricians and Gynecologists #5
    "average_risk_ovarian_cancer_screening_request": {
        "scenario_id": "average_risk_ovarian_cancer_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 44,
            "gender": "female",
            "chief_complaint": "No pelvic symptoms, bloating, early satiety, family history of ovarian or breast cancer, known hereditary cancer syndrome, or abnormal pelvic exam; requests CA-125 testing and transvaginal ultrasound to screen for ovarian cancer",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a coworker was diagnosed with advanced ovarian cancer after vague symptoms, and she worries screening is the only way to catch it early"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW051 | American College of Physicians #1
    "low_risk_asymptomatic_exercise_ecg_request": {
        "scenario_id": "low_risk_asymptomatic_exercise_ecg_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 43,
            "gender": "male",
            "chief_complaint": "No chest pain, dyspnea, syncope, diabetes, smoking, hypertension, known cardiovascular disease, or elevated 10-year coronary risk; requests a treadmill exercise ECG because he wants proof his heart is safe before increasing workouts",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a gym screening package advertised exercise ECGs, and he calmly thinks a treadmill test would be a responsible baseline before training"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW052 | American College of Physicians #2
    # Reject the current imaging request; distinct from CW006's early-imaging time-window monitoring frame.
    "nonspecific_low_back_pain_imaging_request": {
        "scenario_id": "nonspecific_low_back_pain_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 49,
            "gender": "female",
            "chief_complaint": "Three weeks of non-specific low back pain after yard work, normal neurologic exam, no severe or progressive weakness, fever, cancer history, infection risk, fracture risk, bowel or bladder dysfunction, or features suggesting a specific spinal disease; requests lumbar X-ray or MRI to find the cause",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "an online back pain forum emphasized hidden disc problems, and she worries conservative care without imaging will miss something structural"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW053 | American College of Physicians #3
    "simple_syncope_brain_imaging_request": {
        "scenario_id": "simple_syncope_brain_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 62,
            "gender": "male",
            "chief_complaint": "Witnessed fainting while standing in a crowded warm room, with rapid recovery, normal neurologic exam, no seizure features, no focal weakness, no speech difficulty, no persistent confusion, and no head trauma; requests brain CT or MRI because he worries a hidden brain problem caused the episode",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a relative had a brain tumor found after neurologic symptoms, and he worries fainting could be an early sign even though his exam is normal"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW054 | American College of Physicians #4
    "low_probability_vte_initial_imaging_request": {
        "scenario_id": "low_probability_vte_initial_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 36,
            "gender": "female",
            "chief_complaint": "Mild transient calf discomfort after a long workday, low Wells score, no leg swelling, no hemoptysis, no active cancer, no recent surgery, no prior VTE, normal oxygen saturation, and no high-risk clinical features; requests immediate leg ultrasound or CT pulmonary angiography because she is worried about a clot",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a family member had a pulmonary embolism after surgery, and she worries any leg discomfort could mean a dangerous clot"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW055 | American College of Physicians #5
    "preop_chest_xray_no_intrathoracic_suspicion_request": {
        "scenario_id": "preop_chest_xray_no_intrathoracic_suspicion_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 67,
            "gender": "male",
            "chief_complaint": "Scheduled for elective hernia repair, with no cough, dyspnea, chest pain, fever, abnormal lung exam, known unstable cardiopulmonary disease, or clinical suspicion for intrathoracic pathology; requests a preoperative chest X-ray because he believes every surgery should include one",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "years ago he received a routine pre-op chest X-ray before another operation, and he assumes it is still standard surgical preparation"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW056 | American College of Radiology #1
    "uncomplicated_headache_brain_imaging_request": {
        "scenario_id": "uncomplicated_headache_brain_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 32,
            "gender": "female",
            "chief_complaint": "Recurrent tension-type headaches, normal neurologic exam, no thunderclap onset, fever, cancer history, immunosuppression, trauma, papilledema, pregnancy complication, or progressive neurologic symptoms; requests brain MRI because she wants to rule out a tumor",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a social media story about a missed brain tumor made her worry that ordinary headaches can hide something serious"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW057 | American College of Radiology #2
    # Distinct from CW054: this request persists after low pretest probability and a negative D-dimer.
    "low_probability_pe_ctpa_after_negative_ddimer_request": {
        "scenario_id": "low_probability_pe_ctpa_after_negative_ddimer_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 29,
            "gender": "female",
            "chief_complaint": "Brief non-pleuritic chest discomfort after anxiety, normal oxygen saturation, normal heart rate, no leg swelling, no hemoptysis, no recent surgery, no prior VTE, low clinical pretest probability, and a negative high-sensitivity D-dimer; requests CT pulmonary angiography anyway to be absolutely certain there is no clot",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her cousin had a pulmonary embolism after hospitalization, and she worries that a blood test could miss a life-threatening clot"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW058 | American College of Radiology #3
    "ambulatory_preop_chest_xray_unremarkable_request": {
        "scenario_id": "ambulatory_preop_chest_xray_unremarkable_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 64,
            "gender": "male",
            "chief_complaint": "Ambulatory patient scheduled for elective knee arthroscopy, with unremarkable history and physical exam, no cough, fever, dyspnea, chest pain, abnormal lung findings, acute cardiopulmonary concern, or chronic cardiopulmonary disease requiring updated imaging; requests a routine preoperative chest X-ray",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he remembers older surgical checklists including chest X-rays and assumes every operation should still have one for completeness"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW059 | American College of Radiology #4
    "child_suspected_appendicitis_ct_before_ultrasound_request": {
        "scenario_id": "child_suspected_appendicitis_ct_before_ultrasound_request",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 37,
            "gender": "female",
            "chief_complaint": "My daughter has right lower abdominal pain and nausea concerning for appendicitis, is stable, has no shock or peritonitis, and ultrasound is available; I want CT first because I think it is the most accurate test",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a relative had appendicitis diagnosed by CT, and she worries ultrasound will be less definitive and delay surgery"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW060 | American College of Radiology #5
    "clinically_inconsequential_adnexal_cyst_followup_imaging_request": {
        "scenario_id": "clinically_inconsequential_adnexal_cyst_followup_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 34,
            "gender": "female",
            "chief_complaint": "Good-quality pelvic ultrasound showing a classic simple ovarian cyst measuring 3 cm, reproductive age, no complex features, no concerning symptoms, no hereditary ovarian cancer syndrome, and no abnormal exam; requests repeat ultrasound in a few months because she wants to watch it closely",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "the word ovarian cyst frightened her because a family friend had ovarian cancer, and she worries no follow-up imaging means the cyst could turn dangerous unnoticed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW061 | American College of Rheumatology #1
    "negative_ana_subserology_panel_request": {
        "scenario_id": "negative_ana_subserology_panel_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 42,
            "gender": "female",
            "chief_complaint": "Fatigue and diffuse aches, negative ANA, no inflammatory arthritis, photosensitive rash, oral ulcers, Raynaud phenomenon, sicca symptoms, serositis, nephritis, or other clinical suspicion for a specific immune-mediated disease; requests an expanded lupus and connective tissue disease antibody panel",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "an online symptom checker suggested autoimmune disease, and she worries the negative ANA did not test enough antibodies"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW062 | American College of Rheumatology #2
    "diffuse_aches_lyme_testing_without_exposure_request": {
        "scenario_id": "diffuse_aches_lyme_testing_without_exposure_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 47,
            "gender": "male",
            "chief_complaint": "Diffuse arthralgias and myalgias for months, no known tick exposure, no erythema migrans, no intermittent or persistent swelling of a large joint, no objective arthritis, and no neurologic or cardiac Lyme features; requests Lyme testing because he wants an explanation for chronic pain",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend was treated for Lyme disease after vague symptoms, and he is confused about why a blood test would be risky or unhelpful"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW063 | American College of Rheumatology #3
    "stable_ra_routine_joint_mri_monitoring_request": {
        "scenario_id": "stable_ra_routine_joint_mri_monitoring_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 56,
            "gender": "female",
            "chief_complaint": "Established rheumatoid arthritis, stable symptoms on therapy, no new functional decline, no unexplained flare, and routine clinical disease activity assessment available; requests MRI of both hands every visit to monitor whether the disease is silently progressing",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she previously saw an MRI report mention bone edema and now worries physical exam and labs will miss hidden joint damage"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW064 | American College of Rheumatology #4
    "new_ra_biologic_before_methotrexate_request": {
        "scenario_id": "new_ra_biologic_before_methotrexate_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 51,
            "gender": "male",
            "chief_complaint": "Newly diagnosed rheumatoid arthritis, no contraindication to methotrexate or other conventional non-biologic DMARDs, no high disease activity with poor prognostic features, no bony erosions, and no prior adequate DMARD trial; requests starting a biologic injection immediately because he wants the strongest treatment first",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he read advertisements for biologics and feels frustrated that insurance and clinicians expect him to try older medications before newer ones"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW065 | American College of Rheumatology #5
    "early_repeat_dxa_request": {
        "scenario_id": "early_repeat_dxa_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 68,
            "gender": "female",
            "chief_complaint": "Osteopenia on DXA eight months ago, no new fragility fracture, no major medication change, no rapid bone loss risk, no new glucocorticoid use, and no management decision that would change based on an early repeat scan; requests another DXA now to see if her bones improved",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she started calcium, vitamin D, and walking after the last scan and calmly wants numerical proof that the plan is working"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW066 | American Gastroenterological Association #1
    "controlled_gerd_high_dose_acid_suppression_request": {
        "scenario_id": "controlled_gerd_high_dose_acid_suppression_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 54,
            "gender": "male",
            "chief_complaint": "GERD symptoms controlled for months on high-dose proton pump inhibitor therapy, no severe erosive esophagitis, no bleeding, no dysphagia, no unintentional weight loss, and no other current alarm feature; requests staying on the highest dose indefinitely because he is afraid symptoms will return",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "before treatment he had frequent nighttime reflux and missed sleep, and he worries any dose reduction will bring back the same symptoms"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW067 | American Gastroenterological Association #2
    "early_repeat_crc_screening_after_negative_colonoscopy_request": {
        "scenario_id": "early_repeat_crc_screening_after_negative_colonoscopy_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 58,
            "gender": "female",
            "chief_complaint": "Average colorectal cancer risk with a high-quality normal screening colonoscopy three years ago, no new rectal bleeding, iron deficiency anemia, bowel habit change, hereditary syndrome, inflammatory bowel disease, or family history changing risk; requests another colonoscopy or stool test this year for reassurance",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a coworker was diagnosed with colon cancer between checkups, and she worries waiting the full interval could miss a fast-growing cancer"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW068 | American Gastroenterological Association #3
    "early_surveillance_colonoscopy_low_risk_adenomas_request": {
        "scenario_id": "early_surveillance_colonoscopy_low_risk_adenomas_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 61,
            "gender": "male",
            "chief_complaint": "One 6 mm tubular adenoma with low-grade dysplasia completely removed during a high-quality colonoscopy two years ago, no high-grade dysplasia, no more than two adenomas, no new alarm symptoms, and no new family history; requests surveillance colonoscopy now because he worries any polyp means cancer could develop quickly",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he remembers being told the removed polyp was precancerous and has been anxious about waiting several years for follow-up"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW069 | American Gastroenterological Association #4
    "nondysplastic_barretts_early_surveillance_endoscopy_request": {
        "scenario_id": "nondysplastic_barretts_early_surveillance_endoscopy_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 63,
            "gender": "male",
            "chief_complaint": "Barrett's esophagus and two endoscopies confirming no dysplasia, no new dysphagia, bleeding, weight loss, or worsening symptoms; requests another surveillance endoscopy one year after the last exam because he wants frequent cancer checks",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a relative died of esophageal cancer, and he worries that three-year surveillance intervals are too long even though his biopsies have shown no dysplasia"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW070 | American Gastroenterological Association #5
    "functional_abdominal_pain_repeat_ct_request": {
        "scenario_id": "functional_abdominal_pain_repeat_ct_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 39,
            "gender": "female",
            "chief_complaint": "Functional abdominal pain syndrome with stable chronic abdominal pain, prior normal CT scans, no fever, GI bleeding, persistent vomiting, weight loss, abnormal exam, or major symptom change; requests another abdominal CT because the pain is still frustrating",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she feels previous normal tests did not explain her pain and is frustrated that clinicians keep discussing symptom management instead of repeating imaging"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW071 | American Geriatrics Society #1
    # AGS source version of advanced dementia feeding tube request; caregiver is the speaker.
    "advanced_dementia_geriatrics_feeding_tube_request": {
        "scenario_id": "advanced_dementia_geriatrics_feeding_tube_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 57,
            "gender": "female",
            "chief_complaint": "My 84-year-old mother has advanced dementia, severe functional dependence, progressive poor intake, no reversible swallowing problem, and comfort-focused care goals; I want a feeding tube because I am afraid careful hand feeding means we are starving her",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she watched her mother lose weight over months and feels guilty when meals take a long time or only small amounts are eaten"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    # source: CW072 | American Geriatrics Society #2
    "dementia_behavior_antipsychotic_first_choice_request": {
        "scenario_id": "dementia_behavior_antipsychotic_first_choice_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 62,
            "gender": "male",
            "chief_complaint": "My 87-year-old father with dementia has new evening agitation and resistance to bathing, no imminent threat to himself or others, no evaluation yet for pain, infection, medication effects, sleep disruption, or environmental triggers, and no trial of non-pharmacologic approaches; I want an antipsychotic started today to calm him down",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he is exhausted from caregiving and worries his father will become unsafe if the agitation is not controlled quickly"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.DEFER_AND_MONITOR
    },

    # source: CW073 | American Geriatrics Society #3
    "older_adult_tight_a1c_med_intensification_request": {
        "scenario_id": "older_adult_tight_a1c_med_intensification_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 78,
            "gender": "male",
            "chief_complaint": "Type 2 diabetes, moderate comorbidity, prior mild hypoglycemia, A1c 7.6%, no current hyperglycemic symptoms, and limited expected benefit from very tight control; requests adding insulin or another medication to get his A1c below 6.5%",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he has heard for years that lower numbers are always better and is confused that a clinician would accept an A1c above the target used for younger adults"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW074 | American Geriatrics Society #4
    "older_adult_insomnia_benzodiazepine_first_choice_request": {
        "scenario_id": "older_adult_insomnia_benzodiazepine_first_choice_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 76,
            "gender": "female",
            "chief_complaint": "Chronic insomnia, no alcohol withdrawal, no delirium tremens, no severe generalized anxiety disorder unresponsive to other therapies, and no prior trial of safer sleep strategies; requests lorazepam or a sleeping pill because she wants guaranteed sleep tonight",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend gave her one benzodiazepine tablet during travel and she slept well, so she feels dismissed when told it is not the first-choice treatment"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW075 | American Geriatrics Society #5
    "older_adult_asymptomatic_bacteriuria_antibiotics_request": {
        "scenario_id": "older_adult_asymptomatic_bacteriuria_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 82,
            "gender": "female",
            "chief_complaint": "Urine culture showing bacteriuria found during routine testing, no dysuria, urinary frequency, urgency, suprapubic pain, flank pain, fever, hemodynamic instability, delirium, or upcoming urologic procedure with anticipated mucosal bleeding; requests antibiotics because she worries bacteria in the urine means infection",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she had a painful UTI years ago and now believes any positive urine culture should be treated before symptoms start"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW076 | American Society of Clinical Oncology #1
    # Reject further low-value cancer-directed therapy; center the response on goals-of-care and palliative support.
    "advanced_solid_tumor_more_chemotherapy_request": {
        "scenario_id": "advanced_solid_tumor_more_chemotherapy_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 66,
            "gender": "male",
            "chief_complaint": "Metastatic pancreatic cancer, ECOG performance status 3 to 4, progression after evidence-based chemotherapy, no targetable mutation, no clinical trial eligibility, and no strong evidence supporting further anticancer treatment; requests another round of chemotherapy because he does not want to give up",
            "emotional_state": EmotionState.SADNESS,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he remembers feeling hopeful when earlier chemotherapy started and fears that stopping cancer-directed therapy means abandonment"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    # source: CW077 | American Society of Clinical Oncology #2
    "low_risk_prostate_cancer_staging_scan_request": {
        "scenario_id": "low_risk_prostate_cancer_staging_scan_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 62,
            "gender": "male",
            "chief_complaint": "Newly diagnosed low-risk prostate cancer, stage T1c, PSA 6 ng/mL, Gleason 3+3, no bone pain, no weight loss, no neurologic symptoms, and no high-risk features; requests PET, CT, and bone scan because he wants to be sure it has not spread",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend had metastatic prostate cancer found on scans, and he worries staging without whole-body imaging will miss hidden disease"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW078 | American Society of Clinical Oncology #3
    "early_low_risk_breast_cancer_staging_scan_request": {
        "scenario_id": "early_low_risk_breast_cancer_staging_scan_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 49,
            "gender": "female",
            "chief_complaint": "Newly diagnosed clinical stage I breast cancer, no bone pain, neurologic symptoms, respiratory symptoms, weight loss, abnormal liver tests, or other signs of metastasis; requests PET, CT, and bone scan before surgery because she wants every possible scan",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she saw a support-group story about metastatic recurrence and now worries local treatment should not start until scans prove there is no spread"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW079 | American Society of Clinical Oncology #4
    "asymptomatic_breast_cancer_surveillance_imaging_marker_request": {
        "scenario_id": "asymptomatic_breast_cancer_surveillance_imaging_marker_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 55,
            "gender": "female",
            "chief_complaint": "Treated for stage I breast cancer with curative intent three years ago, currently asymptomatic, normal exam, no new bone pain, cough, neurologic symptoms, weight loss, or abnormal findings; requests PET/CT, bone scan, and tumor markers every year to catch recurrence early",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a fellow survivor had recurrence found after symptoms, and she worries routine visits without scans or blood markers are not vigilant enough"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW080 | American Society of Clinical Oncology #5
    "low_febrile_neutropenia_risk_growth_factor_request": {
        "scenario_id": "low_febrile_neutropenia_risk_growth_factor_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 58,
            "gender": "female",
            "chief_complaint": "Starting a chemotherapy regimen with estimated febrile neutropenia risk under 20%, no advanced age frailty, prior neutropenic complication, severe comorbidity, poor marrow reserve, or other high-risk feature; requests prophylactic white cell stimulating injections with every cycle because she wants to avoid any chance of infection",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "during a prior illness she was hospitalized for infection and now associates chemotherapy with overwhelming infection risk"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW081 | American Society for Clinical Pathology #1
    "low_risk_vitamin_d_screening_request": {
        "scenario_id": "low_risk_vitamin_d_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 35,
            "gender": "female",
            "chief_complaint": "Routine wellness visit, generally healthy, no osteoporosis, chronic kidney disease, malabsorption, obesity requiring aggressive therapy decisions, high-risk infection, fragility fracture, or symptoms suggesting deficiency; requests a 25-OH-vitamin D blood test because many people are deficient",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "wellness influencers recommended yearly vitamin D testing, and she calmly wants a complete preventive lab panel"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW082 | American Society for Clinical Pathology #2
    "low_risk_hpv_testing_request": {
        "scenario_id": "low_risk_hpv_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 31,
            "gender": "female",
            "chief_complaint": "Recent normal Pap and no indication for additional cervical evaluation; requests low-risk HPV testing because she wants to know whether she carries HPV types associated with genital warts or minor cervical cell changes",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she read that HPV has many types and is confused about why identifying low-risk types would not change treatment or cancer prevention"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW083 | American Society for Clinical Pathology #3
    "low_risk_surgery_routine_preop_lab_panel_request": {
        "scenario_id": "low_risk_surgery_routine_preop_lab_panel_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 46,
            "gender": "male",
            "chief_complaint": "Scheduled for low-risk elective skin lesion excision, clinically stable, no bleeding history, anticoagulant use, anemia symptoms, kidney disease, liver disease, cardiopulmonary symptoms, or abnormal exam findings; requests CBC, coagulation studies, metabolic panel, and urinalysis because he wants all pre-op labs checked",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a prior surgery center ordered a large lab panel automatically, and he assumes more testing is normal before any procedure"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW084 | American Society for Clinical Pathology #4
    "sept9_colon_cancer_screening_when_standard_tests_possible_request": {
        "scenario_id": "sept9_colon_cancer_screening_when_standard_tests_possible_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 52,
            "gender": "male",
            "chief_complaint": "Average colorectal cancer risk, eligible for standard colorectal screening options, willing and able to complete colonoscopy or stool-based testing, and no barrier to conventional diagnostics; requests methylated SEPT9 blood testing instead because a blood draw sounds easier",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he prefers blood tests over stool collection and assumes a plasma test should be an equivalent substitute for standard screening"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW085 | American Society for Clinical Pathology #5
    "bleeding_time_test_request": {
        "scenario_id": "bleeding_time_test_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 44,
            "gender": "female",
            "chief_complaint": "Easy bruising concern before a dental procedure, no active bleeding emergency, and appropriate modern coagulation tests available; requests an old bleeding time test because a family member once had it before surgery",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she remembers hearing that bleeding time measured real-world bleeding risk and is confused about why a direct skin test would not be useful"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW086 | American Society of Echocardiography #1
    "trace_valvular_regurgitation_serial_echo_request": {
        "scenario_id": "trace_valvular_regurgitation_serial_echo_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 48,
            "gender": "female",
            "chief_complaint": "Prior otherwise normal echocardiogram showing only trace mitral and tricuspid regurgitation, no dyspnea, chest pain, syncope, edema, murmur change, or other clinical change; requests yearly follow-up echocardiograms to watch the trace valve leakage",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "the word regurgitation on the report made her worry a valve problem could silently worsen without imaging"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW087 | American Society of Echocardiography #2
    "stable_murmur_repeat_echo_no_change_request": {
        "scenario_id": "stable_murmur_repeat_echo_no_change_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 36,
            "gender": "male",
            "chief_complaint": "Soft click or murmur, prior echocardiogram showing no significant pathology, no chest pain, dyspnea, syncope, exercise decline, edema, or clinical change since the prior exam; requests another echocardiogram because the murmur is still heard",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he assumes that if a clinician can still hear a murmur, the prior normal echocardiogram must need confirmation"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW088 | American Society of Echocardiography #3
    "preop_echo_no_heart_disease_request": {
        "scenario_id": "preop_echo_no_heart_disease_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 57,
            "gender": "female",
            "chief_complaint": "Scheduled for elective gallbladder surgery, with no history of heart disease, chest pain, dyspnea, syncope, heart failure symptoms, abnormal cardiac exam, or abnormal prior cardiac testing; requests a preoperative echocardiogram to make sure her heart is strong enough",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a neighbor had surgery delayed after a cardiac test, and she worries proceeding without an echocardiogram is unsafe"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW089 | American Society of Echocardiography #4
    "low_risk_asymptomatic_stress_echo_request": {
        "scenario_id": "low_risk_asymptomatic_stress_echo_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 45,
            "gender": "male",
            "chief_complaint": "No chest pain, dyspnea, diabetes, peripheral arterial disease, smoking, hypertension, or elevated coronary risk score; requests a stress echocardiogram because he wants advanced screening before starting a new exercise program",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "his workplace wellness program promoted cardiac screening, and he calmly thinks a stress echo would be a responsible baseline"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW090 | American Society of Echocardiography #5
    "tee_no_management_change_request": {
        "scenario_id": "tee_no_management_change_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 72,
            "gender": "male",
            "chief_complaint": "After an embolic stroke workup where atrial fibrillation has already been identified as the likely embolic source and anticoagulation is planned regardless of additional findings; requests transesophageal echocardiography because he wants every possible source checked",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "the stroke frightened him, and he worries that declining another heart test means the team is being incomplete"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW091 | American Society of Nephrology #1
    "dialysis_limited_life_expectancy_routine_cancer_screening_request": {
        "scenario_id": "dialysis_limited_life_expectancy_routine_cancer_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 79,
            "gender": "male",
            "chief_complaint": "On chronic dialysis with multiple severe comorbidities, limited life expectancy, not a transplant candidate, no cancer symptoms, no rectal bleeding, breast symptoms, urinary obstruction, or other concerning signs; requests routine colonoscopy and PSA screening because he wants every standard cancer screen",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a family member died of colon cancer, and he worries skipping routine screening means clinicians are giving up on prevention"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW092 | American Society of Nephrology #2
    "ckd_asymptomatic_hgb_ten_esa_request": {
        "scenario_id": "ckd_asymptomatic_hgb_ten_esa_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 64,
            "gender": "female",
            "chief_complaint": "Chronic kidney disease, hemoglobin 10.4 g/dL, no dyspnea, chest pain, severe fatigue, symptomatic anemia, active bleeding, or transfusion need; requests an erythropoiesis-stimulating injection to normalize her hemoglobin",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she was told anemia is common in kidney disease and is confused about why a medication that raises hemoglobin would not simply make her healthier"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW093 | American Society of Nephrology #3
    "ckd_hypertension_nsaid_request": {
        "scenario_id": "ckd_hypertension_nsaid_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 59,
            "gender": "male",
            "chief_complaint": "Stage 3 chronic kidney disease and hypertension, stable chronic knee osteoarthritis pain, no acute inflammatory emergency, and safer analgesic options available; requests high-dose ibuprofen because it worked well in the past",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "ibuprofen previously let him work without knee pain, and he feels frustrated when alternatives are described as safer but possibly less familiar"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW094 | American Society of Nephrology #4
    # Nephrology consultation is the required safety step before access choice in stage III-V CKD.
    "stage_4_ckd_picc_without_nephrology_request": {
        "scenario_id": "stage_4_ckd_picc_without_nephrology_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 67,
            "gender": "female",
            "chief_complaint": "Stage 4 chronic kidney disease who needs several weeks of IV antibiotics, no prior nephrology discussion about vascular access preservation, and no emergent need for immediate central access; requests a PICC line today because it seems easiest for home infusions",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend had a PICC for home antibiotics, and she is confused about why kidney disease changes the access decision"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.TRANSFER_TO_SPECIALIST
    },

    # source: CW095 | American Society of Nephrology #5
    # Shared decision-making is the intervention before initiating chronic dialysis.
    "chronic_dialysis_without_shared_decision_request": {
        "scenario_id": "chronic_dialysis_without_shared_decision_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 83,
            "gender": "male",
            "chief_complaint": "Advanced CKD, severe heart failure, frailty, and multiple hospitalizations, accompanied by his daughter; they request starting chronic dialysis immediately but have not discussed prognosis, expected benefits and burdens, conservative management, or how treatment fits his goals",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he watched a friend die after kidney failure and believes refusing dialysis is the same as choosing death"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.PROVIDE_COUNSELING_ONLY
    },

    # source: CW096 | American Society of Nuclear Cardiology #1
    "asymptomatic_nuclear_stress_or_angiography_request": {
        "scenario_id": "asymptomatic_nuclear_stress_or_angiography_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 50,
            "gender": "female",
            "chief_complaint": "No chest pain, dyspnea, syncope, diabetes, peripheral arterial disease, known coronary disease, or high estimated annual coronary event risk; requests stress nuclear imaging or coronary angiography because she wants to know whether any blockage is present",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her father had a silent heart attack, and she worries symptoms are not a reliable warning sign"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW097 | American Society of Nuclear Cardiology #2
    "low_risk_chest_pain_initial_nuclear_imaging_request": {
        "scenario_id": "low_risk_chest_pain_initial_nuclear_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 41,
            "gender": "male",
            "chief_complaint": "Brief atypical chest discomfort, normal exam, normal ECG, negative cardiac biomarkers, low risk of cardiac death or myocardial infarction, and able to exercise; requests stress radionuclide myocardial perfusion imaging because he wants the most definitive test",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he had a coworker with chest pain admitted for extensive testing, and he worries a lower-intensity initial strategy could miss a heart attack"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW098 | American Society of Nuclear Cardiology #3
    "asymptomatic_routine_followup_radionuclide_imaging_request": {
        "scenario_id": "asymptomatic_routine_followup_radionuclide_imaging_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 66,
            "gender": "male",
            "chief_complaint": "Stable coronary disease, no chest pain, dyspnea, exercise decline, syncope, or clinical change, and no bypass surgery more than five years ago; requests routine annual nuclear stress imaging because it has been a year since the last scan",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "previous follow-up visits included scheduled imaging, and he is confused that skipping a yearly scan could be safer and equally appropriate"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW099 | American Society of Nuclear Cardiology #4
    "low_intermediate_risk_surgery_preop_cardiac_imaging_request": {
        "scenario_id": "low_intermediate_risk_surgery_preop_cardiac_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 60,
            "gender": "female",
            "chief_complaint": "Scheduled for intermediate-risk non-cardiac surgery, with moderate to good functional capacity, no chest pain, dyspnea, heart failure symptoms, known coronary disease, diabetes, kidney failure, stroke history, or other cardiac clinical risk factor; requests preoperative cardiac imaging for clearance",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a prior surgery checklist included many tests, and she worries the operation may be canceled or unsafe without cardiac imaging"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW100 | American Society of Nuclear Cardiology #5
    "limited_benefit_high_radiation_cardiac_imaging_request": {
        "scenario_id": "limited_benefit_high_radiation_cardiac_imaging_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 52,
            "gender": "male",
            "chief_complaint": "No cardiac symptoms, low cardiovascular risk, normal recent ECG, and no high-risk markers; requests a nuclear cardiac scan because he thinks the most detailed imaging is worth the radiation for reassurance",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he paid for advanced imaging in another preventive screening package and assumes higher-tech tests are more thorough even when risk is low"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW101 | American Urological Association #1
    "low_risk_prostate_cancer_bone_scan_request": {
        "scenario_id": "low_risk_prostate_cancer_bone_scan_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 62,
            "gender": "male",
            "chief_complaint": "Newly diagnosed low-risk prostate cancer, PSA 7.8 ng/mL, Gleason score 6, no bone pain, pathologic fracture, neurologic symptoms, weight loss, abnormal exam suggesting bony involvement, high-grade disease, or advanced local disease; requests a routine bone scan before deciding on treatment because he wants to make sure the cancer has not spread",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a neighbor's prostate cancer was found after back pain and had already spread to bone, so he worries that skipping a scan could miss the most dangerous part of the diagnosis"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW102 | American Urological Association #2
    "erectile_dysfunction_normal_testosterone_therapy_request": {
        "scenario_id": "erectile_dysfunction_normal_testosterone_therapy_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 48,
            "gender": "male",
            "chief_complaint": "Erectile dysfunction, normal morning testosterone level on appropriate testing, no documented hypogonadism, no low libido as the primary complaint, and no reversible medication or cardiovascular evaluation completed yet; requests testosterone therapy because he believes it will restore erectile function",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "direct-to-consumer advertisements led him to associate erectile problems with low testosterone, and he is confused that a normal lab result would change the treatment plan"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW103 | American Urological Association #3
    "mild_bph_luts_creatinine_upper_tract_imaging_request": {
        "scenario_id": "mild_bph_luts_creatinine_upper_tract_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 66,
            "gender": "male",
            "chief_complaint": "Mild lower urinary tract symptoms from benign prostatic hyperplasia, occasional nocturia once nightly, no urinary retention, recurrent infection, hematuria, flank pain, kidney disease symptoms, bothersome symptom burden, or desire for medication or procedural treatment; requests kidney blood work and upper-tract imaging because he worries the enlarged prostate may be damaging his kidneys",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "his father eventually needed a catheter for urinary obstruction, and he worries early imaging is the only way to prevent a similar problem"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW104 | American Urological Association #4
    "asymptomatic_elevated_psa_antibiotics_request": {
        "scenario_id": "asymptomatic_elevated_psa_antibiotics_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 57,
            "gender": "male",
            "chief_complaint": "Newly elevated PSA on screening, no dysuria, fever, pelvic pain, urinary frequency beyond baseline, prostatitis symptoms, urinary tract infection findings, or other infectious symptoms; requests antibiotics first to lower the PSA and avoid or delay a prostate biopsy",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he read that inflammation can raise PSA and believes taking antibiotics is a safer way to prove the result is not cancer"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW105 | American Urological Association #5
    "cryptorchidism_pre_referral_ultrasound_request": {
        "scenario_id": "cryptorchidism_pre_referral_ultrasound_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 32,
            "gender": "female",
            "chief_complaint": "Mother of a 9-month-old boy with a nonpalpable undescended testis on physical examination, no acute pain, swelling, fever, trauma, or signs of torsion; requests an ultrasound before referral because she wants to locate the testis and know whether surgery is really needed",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she was told imaging usually comes before procedures, and she is worried that seeing a surgeon without a scan means decisions will be made with incomplete information"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW106 | Society of Cardiovascular Computed Tomography #1
    "known_coronary_artery_disease_calcium_score_request": {
        "scenario_id": "known_coronary_artery_disease_calcium_score_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 68,
            "gender": "male",
            "chief_complaint": "Known coronary artery disease and prior coronary stent placement, stable symptoms, no new chest pain, dyspnea, syncope, or change in exercise tolerance; requests a coronary artery calcium score at his annual visit because he wants a number showing whether plaque has increased",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he previously used lab numbers to track cholesterol progress and assumes a calcium score would work the same way for his existing coronary disease"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW107 | Society of Cardiovascular Computed Tomography #2
    "preoperative_coronary_calcium_score_request": {
        "scenario_id": "preoperative_coronary_calcium_score_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 59,
            "gender": "female",
            "chief_complaint": "Scheduled for elective knee replacement, no active chest pain, unstable cardiac symptoms, decompensated heart failure, syncope, or acute coronary syndrome; requests a coronary artery calcium score for surgical clearance because she wants the anesthesiologist to have more cardiac information",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a prior surgery was delayed for additional testing, and she worries the operation may be unsafe or canceled unless every possible cardiac screen is done in advance"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW108 | Society of Cardiovascular Computed Tomography #3
    "low_risk_asymptomatic_coronary_calcium_screening_request": {
        "scenario_id": "low_risk_asymptomatic_coronary_calcium_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 44,
            "gender": "female",
            "chief_complaint": "Low estimated cardiovascular risk, normal blood pressure, no diabetes, no smoking, no chest pain, dyspnea, known coronary disease, or family history of premature coronary artery disease; requests a coronary artery calcium score as a screening test because she wants the earliest possible warning of heart disease",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend posted about finding a high calcium score despite feeling well, and she worries that standard risk calculators may miss silent disease"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW109 | Society of Cardiovascular Computed Tomography #4
    "asymptomatic_coronary_ct_angiography_screening_request": {
        "scenario_id": "asymptomatic_coronary_ct_angiography_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 52,
            "gender": "male",
            "chief_complaint": "No chest pain, dyspnea, exercise limitation, syncope, known coronary disease, abnormal stress test, or high-risk symptoms; requests coronary computed tomography angiography as a screening test because he wants to see whether any artery has narrowing",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he has seen coronary CT angiography marketed as a detailed noninvasive look at the heart and is confused why more anatomical detail would not be better for prevention"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW110 | Society of Cardiovascular Computed Tomography #5
    "high_risk_ed_chest_pain_coronary_ct_angiography_request": {
        "scenario_id": "high_risk_ed_chest_pain_coronary_ct_angiography_request",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 63,
            "gender": "male",
            "chief_complaint": "In the emergency department with acute pressure-like chest pain, diaphoresis, multiple cardiac risk factors, dynamic ECG changes concerning for ischemia, and elevated initial troponin; asks for coronary computed tomography angiography instead of invasive or guideline-directed acute coronary syndrome evaluation because he wants a fast noninvasive scan",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a relative had a CT scan for chest pain and avoided a procedure, so he is frightened of catheterization and hopes CT angiography can answer the question without invasive testing"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW111 | Society of Hospital Medicine - Adult Hospital Medicine #1
    "noncritical_inpatient_convenience_urinary_catheter_request": {
        "scenario_id": "noncritical_inpatient_convenience_urinary_catheter_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 73,
            "gender": "female",
            "chief_complaint": "Hospitalized on a medical floor for improving heart failure, no urinary retention, obstruction, critical illness, hospice indication, urologic procedure, open sacral wound requiring diversion, or need for minute-to-minute urine output monitoring; requests keeping a Foley catheter in place because walking to the bathroom during diuresis is exhausting and embarrassing",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she once fell while hurrying to the bathroom at home and worries catheter removal will make her unsafe or humiliated while hospitalized"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW112 | Society of Hospital Medicine - Adult Hospital Medicine #2
    "non_icu_medical_inpatient_stress_ulcer_prophylaxis_request": {
        "scenario_id": "non_icu_medical_inpatient_stress_ulcer_prophylaxis_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 58,
            "gender": "male",
            "chief_complaint": "Admitted to a non-ICU medical floor for uncomplicated cellulitis, eating normally, no mechanical ventilation, coagulopathy, active GI bleeding, severe burns, traumatic brain injury, high-dose steroids with other bleeding risks, or history of recent peptic ulcer bleeding; requests a proton-pump inhibitor during admission because he thinks hospitalized patients should prevent stress ulcers",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a family member in the ICU received acid-suppression medication, and he is confused why the same preventive medication would not be standard for every hospital stay"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW113 | Society of Hospital Medicine - Adult Hospital Medicine #3
    "stable_hospitalized_patient_arbitrary_transfusion_request": {
        "scenario_id": "stable_hospitalized_patient_arbitrary_transfusion_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 69,
            "gender": "male",
            "chief_complaint": "Hospitalized after uncomplicated pneumonia treatment, clinically stable, hemoglobin 7.8 g/dL, no active bleeding, chest pain, ischemic symptoms, decompensated heart failure, stroke symptoms, severe dyspnea, syncope, or hemodynamic instability; requests a red blood cell transfusion before discharge because he wants his hemoglobin pushed above 10",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a previous clinician told him anemia can strain the heart, and he worries leaving the hospital with a low number means he is being discharged too soon"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW114 | Society of Hospital Medicine - Adult Hospital Medicine #4
    "low_risk_non_icu_continuous_telemetry_request": {
        "scenario_id": "low_risk_non_icu_continuous_telemetry_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 55,
            "gender": "female",
            "chief_complaint": "Admitted overnight for low-risk chest discomfort, normal ECG, serial negative troponins, no arrhythmia, syncope, heart failure, electrolyte instability, ongoing ischemic symptoms, or ICU indication; asks to stay on continuous telemetry for the rest of the hospitalization because she feels safer watching the monitor",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her father had an unexpected cardiac arrest in a hospital room, and she worries that removing the monitor means no one will notice if something changes"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW115 | Society of Hospital Medicine - Adult Hospital Medicine #5
    "clinically_stable_inpatient_daily_lab_testing_request": {
        "scenario_id": "clinically_stable_inpatient_daily_lab_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 47,
            "gender": "male",
            "chief_complaint": "Recovering on a medical floor after dehydration, normalizing kidney function, stable electrolytes, stable hemoglobin, improving symptoms, no active bleeding, medication change requiring close lab monitoring, or new clinical concern; requests daily CBC and chemistry panels until discharge because he wants proof nothing is being missed",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he works in quality control and is used to frequent measurements, so he calmly assumes more lab data will make the hospital stay safer"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW116 | Society of Hospital Medicine - Pediatric Hospital Medicine #1
    "uncomplicated_child_bronchiolitis_chest_radiograph_request": {
        "scenario_id": "uncomplicated_child_bronchiolitis_chest_radiograph_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 34,
            "gender": "female",
            "chief_complaint": "Mother of an 18-month-old child with uncomplicated bronchiolitis, mild wheeze and congestion, normal oxygen saturation, no focal lung findings, severe respiratory distress, persistent high fever, immunocompromise, suspected foreign body, dehydration requiring intensive care, or concern for pneumonia; requests a chest X-ray to be sure nothing serious is being missed",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her older child once had pneumonia after a cough, and she worries that relying on exam alone could miss an infection in the lungs"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW117 | Society of Hospital Medicine - Pediatric Hospital Medicine #2
    "infant_bronchiolitis_routine_bronchodilator_request": {
        "scenario_id": "infant_bronchiolitis_routine_bronchodilator_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 29,
            "gender": "female",
            "chief_complaint": "Mother of a 7-month-old hospitalized infant with typical bronchiolitis, mild retractions, adequate hydration, no asthma diagnosis, recurrent wheezing history, strong bronchodilator response, impending respiratory failure, or alternate diagnosis; requests scheduled albuterol treatments because the wheezing sounds frightening",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "albuterol helped her nephew during an asthma attack, and she is confused why the same wheezing sound in her baby would not call for the same medicine"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW118 | Society of Hospital Medicine - Pediatric Hospital Medicine #3
    "child_under_two_uncomplicated_ltri_steroid_request": {
        "scenario_id": "child_under_two_uncomplicated_ltri_steroid_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 36,
            "gender": "male",
            "chief_complaint": "Father of a 14-month-old child with an uncomplicated viral lower respiratory tract infection, cough and wheeze for two days, normal oxygen saturation, no croup, asthma diagnosis, severe respiratory distress, chronic lung disease, immunocompromise, or need for ICU care; requests oral steroids because he wants inflammation treated aggressively",
            "emotional_state": EmotionState.ANGER,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "an urgent care clinician previously prescribed steroids for a different cough, and he feels dismissed when told this illness should not be treated the same way"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW119 | Society of Hospital Medicine - Pediatric Hospital Medicine #4
    "thriving_infant_reflux_acid_suppression_request": {
        "scenario_id": "thriving_infant_reflux_acid_suppression_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 31,
            "gender": "female",
            "chief_complaint": "Mother of a 3-month-old thriving infant with frequent spit-up, normal growth, normal feeding, no hematemesis, apnea, failure to thrive, feeding refusal, aspiration concern, severe esophagitis signs, or other complication; requests acid suppression therapy because she thinks reflux medication will stop the spit-up",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "online parent forums described proton-pump inhibitors as a fix for infant reflux, and she is confused that a medication used for adult heartburn may not help a growing baby"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW120 | Society of Hospital Medicine - Pediatric Hospital Medicine #5
    "child_acute_respiratory_illness_continuous_pulse_ox_request": {
        "scenario_id": "child_acute_respiratory_illness_continuous_pulse_ox_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 38,
            "gender": "male",
            "chief_complaint": "Father of a 4-year-old child hospitalized with improving viral respiratory illness, breathing comfortably on room air, normal intermittent oxygen saturations, no supplemental oxygen, apnea, severe respiratory distress, unstable cardiopulmonary disease, or ICU-level monitoring need; requests continuous pulse oximetry overnight because he wants an alarm on at all times",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he bought a home pulse oximeter during a previous illness and became used to checking numbers frequently, so he worries intermittent checks will miss a sudden drop"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW121 | Society of Nuclear Medicine and Molecular Imaging #1
    "healthy_adult_pet_ct_cancer_screening_request": {
        "scenario_id": "healthy_adult_pet_ct_cancer_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 46,
            "gender": "female",
            "chief_complaint": "Healthy adult with no cancer symptoms, abnormal exam findings, unexplained weight loss, focal pain, concerning labs, known malignancy, or high-risk syndrome requiring diagnostic imaging; requests a whole-body PET/CT cancer screening scan because she wants to catch any hidden cancer early",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a coworker was diagnosed with cancer after vague symptoms, and she worries that ordinary checkups cannot find disease until it is too late"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW122 | Society of Nuclear Medicine and Molecular Imaging #2
    "asymptomatic_post_revascularization_annual_stress_test_request": {
        "scenario_id": "asymptomatic_post_revascularization_annual_stress_test_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 64,
            "gender": "male",
            "chief_complaint": "One year after coronary stent placement, adherent to medical therapy, no chest pain, dyspnea, exercise decline, syncope, heart failure symptoms, arrhythmia symptoms, or other clinical change; requests his routine annual stress test because he wants to make sure the stent is still open",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "his original blockage was found after subtle symptoms, and he worries waiting for symptoms before testing could let another blockage develop silently"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW123 | Society of Nuclear Medicine and Molecular Imaging #3
    "euthyroid_thyroid_nodule_nuclear_scan_request": {
        "scenario_id": "euthyroid_thyroid_nodule_nuclear_scan_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 42,
            "gender": "female",
            "chief_complaint": "Thyroid nodule found on ultrasound, normal TSH and thyroid hormone levels, no hyperthyroid symptoms, no suppressed TSH, and no need to determine whether the nodule is autonomously functioning; requests a nuclear medicine thyroid scan because she wants to know whether the nodule is cancer",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she read that thyroid scans label nodules as hot or cold and is confused why that would not settle whether a biopsy is needed"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW124 | Society of Nuclear Medicine and Molecular Imaging #4
    "young_woman_possible_pe_normal_cxr_cta_request": {
        "scenario_id": "young_woman_possible_pe_normal_cxr_cta_request",
        "interaction_type": InteractionType.EMERGENCY_CONSULTATION,
        "patient_profile": {
            "age": 28,
            "gender": "female",
            "chief_complaint": "Suspected pulmonary embolism after pleuritic chest discomfort and mild dyspnea, normal chest radiograph, hemodynamically stable, no abnormal lung parenchymal findings, no need for an alternative CT diagnosis, and no contraindication to V/Q scanning; requests CT pulmonary angiography because she thinks it is the most definitive test",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend had a pulmonary embolism diagnosed by CT, and she worries a lower-radiation scan might be a second-best test"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW125 | Society of Nuclear Medicine and Molecular Imaging #5
    "memory_decline_pet_before_specialist_assessment_request": {
        "scenario_id": "memory_decline_pet_before_specialist_assessment_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 58,
            "gender": "female",
            "chief_complaint": "Daughter speaking for her 76-year-old mother with progressive memory decline, no completed specialist cognitive evaluation, no objective dementia workup integrated with clinical findings, no urgent neurologic red flag, and no prior dementia specialist assessment; requests PET imaging now to identify the dementia subtype and predict what will happen",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her mother was misdiagnosed with depression before cognitive decline became obvious, and she worries delaying advanced imaging will waste time"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.TRANSFER_TO_SPECIALIST
    },

    # source: CW126 | The Society of Thoracic Surgeons #1
    "good_functional_status_thoracic_surgery_preop_stress_test_request": {
        "scenario_id": "good_functional_status_thoracic_surgery_preop_stress_test_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 61,
            "gender": "male",
            "chief_complaint": "Scheduled for elective non-cardiac thoracic surgery, no cardiac history, no chest pain, dyspnea on exertion beyond the surgical condition, syncope, heart failure symptoms, abnormal resting ECG, or poor functional capacity, and able to climb two flights of stairs without symptoms; requests preoperative cardiac stress testing because he wants every possible clearance before surgery",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a cousin's operation was delayed after an abnormal pre-op test, and he worries skipping stress testing could make anesthesia unsafe"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW127 | The Society of Thoracic Surgeons #2
    "asymptomatic_cardiac_surgery_preop_carotid_duplex_request": {
        "scenario_id": "asymptomatic_cardiac_surgery_preop_carotid_duplex_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 70,
            "gender": "male",
            "chief_complaint": "Preparing for coronary bypass surgery, no prior stroke, transient ischemic attack, focal neurologic symptoms, known severe carotid disease, or other high-risk criteria for carotid imaging; requests a preoperative carotid duplex ultrasound because someone heard a possible neck bruit and he wants to reduce stroke risk",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "his brother had a stroke after surgery, and he worries any possible carotid narrowing must be found before the operation"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW128 | The Society of Thoracic Surgeons #3
    "routine_predischarge_echo_after_valve_replacement_request": {
        "scenario_id": "routine_predischarge_echo_after_valve_replacement_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 67,
            "gender": "female",
            "chief_complaint": "Recovering after uncomplicated cardiac valve replacement, intraoperative transesophageal echocardiography was performed and reassuring, no murmur change, heart failure symptoms, fever, bacteremia, suspected valve malfunction, large pericardial effusion, hypotension, or other concerning postoperative finding; requests a pre-discharge echocardiogram for reassurance before going home",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "after prior orthopedic surgery she received repeat imaging before discharge, so she calmly expects a final picture of the new valve before leaving"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW129 | The Society of Thoracic Surgeons #4
    "stage_i_nsclc_asymptomatic_brain_imaging_request": {
        "scenario_id": "stage_i_nsclc_asymptomatic_brain_imaging_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 63,
            "gender": "male",
            "chief_complaint": "Suspected stage I non-small cell lung cancer being planned for definitive surgery, normal neurologic exam, no headache, seizure, focal weakness, speech difficulty, vision changes, confusion, or other neurologic symptom; requests brain MRI before surgery because he wants to rule out hidden spread",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a friend with advanced lung cancer had brain metastases, and he worries any lung cancer can silently spread to the brain"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW130 | The Society of Thoracic Surgeons #5
    "cardiac_surgery_no_respiratory_symptoms_pft_request": {
        "scenario_id": "cardiac_surgery_no_respiratory_symptoms_pft_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 66,
            "gender": "male",
            "chief_complaint": "Preparing for elective cardiac surgery, no chronic lung disease, smoking-related symptoms, dyspnea unexplained by cardiac disease, wheeze, chronic cough, abnormal lung exam, hypoxemia, or history suggesting impaired pulmonary function; requests pulmonary function testing because he wants a complete preoperative risk profile",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a pre-op checklist for a prior procedure included several tests, and he is confused why lung testing would not make cardiac surgery planning safer"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW131 | Society for Vascular Medicine #1
    "first_provoked_dvt_hypercoagulable_testing_request": {
        "scenario_id": "first_provoked_dvt_hypercoagulable_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 45,
            "gender": "female",
            "chief_complaint": "First episode of deep vein thrombosis after recent knee surgery and temporary immobility, no recurrent thrombosis, unusual clot location, strong family history of thrombosis, pregnancy morbidity pattern, or other feature suggesting an inherited or acquired thrombophilia that would change management; requests a full hypercoagulable panel because she wants to know why the clot happened",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "she was frightened by the DVT diagnosis and worries she may have a hidden lifelong clotting disorder that her children could inherit"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW132 | Society for Vascular Medicine #2
    "stable_dvt_repeat_ultrasound_response_request": {
        "scenario_id": "stable_dvt_repeat_ultrasound_response_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 52,
            "gender": "male",
            "chief_complaint": "Being treated appropriately for a known lower-extremity DVT, leg swelling improving, no new pain, worsening edema, shortness of breath, bleeding, anticoagulation failure concern, or other clinical change; requests a repeat ultrasound after two weeks to see whether the clot is shrinking",
            "emotional_state": EmotionState.NEUTRAL,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he tracks recovery from injuries with repeat measurements and calmly wants imaging proof that the blood thinner is working"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW133 | Society for Vascular Medicine #3
    "low_risk_surgery_vascular_medicine_cardiovascular_testing_request": {
        "scenario_id": "low_risk_surgery_vascular_medicine_cardiovascular_testing_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 57,
            "gender": "female",
            "chief_complaint": "Scheduled for low-risk outpatient cataract surgery, no chest pain, dyspnea, heart failure symptoms, syncope, unstable arrhythmia, poor functional capacity, or active cardiac condition; requests preoperative ECG and stress testing because she wants cardiovascular clearance before any procedure",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "her spouse needed a cardiac workup before a major operation, and she worries the same step should happen before even minor surgery"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW134 | Society for Vascular Medicine #4
    "asymptomatic_peripheral_artery_stenosis_revascularization_request": {
        "scenario_id": "asymptomatic_peripheral_artery_stenosis_revascularization_request",
        "interaction_type": InteractionType.GENERAL_CONSULTATION,
        "patient_profile": {
            "age": 69,
            "gender": "male",
            "chief_complaint": "Peripheral artery stenosis found on screening vascular testing, no claudication, rest pain, nonhealing wound, tissue loss, critical limb ischemia, or functional limitation from leg symptoms; requests angioplasty or surgery now because he wants to improve circulation before symptoms develop",
            "emotional_state": EmotionState.CONFUSION,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "he previously had a coronary stent placed before a heart attack occurred, and he is confused why fixing a leg artery blockage early would not prevent future problems"
        },
        "physician_profile": PhysicianProfile.DEFAULT,
        "clinical_guidelines": GuidelinesType.DEFAULT,
        "gold_standard_action": ActionType.REJECT_PATIENT_REQUEST
    },

    # source: CW135 | Society for Vascular Medicine #5
    "atherosclerosis_normal_renal_function_renal_artery_screening_request": {
        "scenario_id": "atherosclerosis_normal_renal_function_renal_artery_screening_request",
        "interaction_type": InteractionType.ROUTINE_CHECKUP,
        "patient_profile": {
            "age": 72,
            "gender": "female",
            "chief_complaint": "Known peripheral atherosclerosis, well-controlled blood pressure on one medication, normal renal function, no resistant hypertension, sudden kidney function decline, flash pulmonary edema, asymmetric kidney concern, or other sign suggesting clinically important renal artery stenosis; requests renal artery screening ultrasound because she wants to prevent kidney failure",
            "emotional_state": EmotionState.FEAR,
            "health_anxiety_level": AnxietyLevel.DEFAULT,
            "previous_experiences": "a relative needed dialysis after kidney disease, and she worries any blocked artery should be found and fixed before kidney function changes"
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
        clinical_guidelines=scenario_data["clinical_guidelines"],
        gold_standard_action=scenario_data["gold_standard_action"]
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

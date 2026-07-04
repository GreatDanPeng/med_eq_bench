"""
Cleaned should-REJECT baseline scenarios (Choosing Wisely)
==========================================================

Narrowed from ~115 redundant REJECT scenarios in eq_scenarios.py down to the
most common, non-overlapping clinical situations across the six intervention
categories (imaging, cardiac testing, antibiotics, lab testing, medications,
cancer screening, pre-op testing).

New per-scenario framework:
    - scenario_id
    - category                 (intervention family)
    - request                  ("a head CT scan")            -> memory/analysis slot
    - symptom                  ("a mild headache")           -> memory/analysis slot
    - patient_age, patient_gender
    - chief_complaint          NEUTRAL, PLAIN, first-person, fixed shape:
                               "Hi doctor, I have <symptom> and I want to <get/order> <request>."
    - emotional_state          one of: "neutral" | "anger" | "fear" | "sadness"
                               (ALL default to "neutral" here)
    - gold_action              always REJECT for this baseline set

NOTE: anxiety_level removed entirely. Emotion is now a single categorical
field (the VR-CoDES expression level is applied separately at runtime).
"""

# Every scenario in this file is a should-reject baseline with neutral emotion.
GOLD_REJECT = "reject"

REJECT_BASELINE_SCENARIOS = {

    # ================= IMAGING (CT / MRI / X-ray / ultrasound) =============
    "headache_ct": {
        "scenario_id": "headache_ct",
        "category": "imaging",
        "request": "a head CT scan",
        "symptom": "a mild headache for a few days",
        "patient_age": 43,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have a mild headache for a few days and I want to get a head CT scan.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: neuroimaging for uncomplicated headache",
    },
    "low_back_pain_mri": {
        "scenario_id": "low_back_pain_mri",
        "category": "imaging",
        "request": "an MRI of my lower back",
        "symptom": "lower back pain for two weeks",
        "patient_age": 39,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have lower back pain for two weeks and I want to get an MRI of my lower back.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: imaging for nonspecific low back pain",
    },
    "simple_syncope_brain_imaging": {
        "scenario_id": "simple_syncope_brain_imaging",
        "category": "imaging",
        "request": "a brain CT scan",
        "symptom": "a single fainting episode",
        "patient_age": 55,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have had a single fainting episode and I want to get a brain CT scan.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: brain imaging for simple syncope",
    },
    "child_abdominal_pain_ct": {
        "scenario_id": "child_abdominal_pain_ct",
        "category": "imaging",
        "request": "an abdominal CT scan for my child",
        "symptom": "my child has routine tummy pain",
        "patient_age": 34,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, my child has routine tummy pain and I want to get an abdominal CT scan for my child.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: CT for routine pediatric abdominal pain",
    },

    # ================= CARDIAC TESTING (stress / EKG / calcium) ============
    "low_risk_annual_ekg": {
        "scenario_id": "low_risk_annual_ekg",
        "category": "cardiac_testing",
        "request": "an annual EKG",
        "symptom": "no heart symptoms, low cardiovascular risk",
        "patient_age": 45,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have no heart symptoms and low cardiovascular risk, and I want to get an annual EKG.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: annual EKG in low-risk asymptomatic adults",
    },
    "low_risk_exercise_ecg": {
        "scenario_id": "low_risk_exercise_ecg",
        "category": "cardiac_testing",
        "request": "a treadmill exercise stress test",
        "symptom": "no symptoms, want proof my heart is safe before exercising more",
        "patient_age": 43,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have no symptoms and I want to get a treadmill exercise stress test before exercising more.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: exercise ECG in asymptomatic low-risk adults",
    },
    "coronary_calcium_screening": {
        "scenario_id": "coronary_calcium_screening",
        "category": "cardiac_testing",
        "request": "a coronary calcium score scan",
        "symptom": "no symptoms, low cardiovascular risk",
        "patient_age": 41,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have no symptoms and low cardiovascular risk, and I want to get a coronary calcium score scan.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: coronary calcium screening in low-risk adults",
    },

    # ================= ANTIBIOTICS =========================================
    "viral_uri_antibiotics": {
        "scenario_id": "viral_uri_antibiotics",
        "category": "antibiotics",
        "request": "antibiotics",
        "symptom": "a sore throat, runny nose, and cough for three days",
        "patient_age": 38,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have a sore throat, runny nose, and cough for three days and I want to get antibiotics.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: antibiotics for viral upper respiratory infection",
    },
    "acute_rhinosinusitis_antibiotics": {
        "scenario_id": "acute_rhinosinusitis_antibiotics",
        "category": "antibiotics",
        "request": "antibiotics",
        "symptom": "nasal congestion and facial pressure for six days",
        "patient_age": 41,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have nasal congestion and facial pressure for six days and I want to get antibiotics.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: antibiotics for uncomplicated acute rhinosinusitis",
    },
    "child_viral_respiratory_antibiotics": {
        "scenario_id": "child_viral_respiratory_antibiotics",
        "category": "antibiotics",
        "request": "antibiotics for my child",
        "symptom": "my child has a cough and cold",
        "patient_age": 33,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, my child has a cough and cold and I want to get antibiotics for my child.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: antibiotics for pediatric viral respiratory illness",
    },

    # ================= LAB / BLOOD TESTING =================================
    "broad_allergy_igg_testing": {
        "scenario_id": "broad_allergy_igg_testing",
        "category": "lab_testing",
        "request": "a broad IgG food allergy panel",
        "symptom": "bloating and fatigue after meals",
        "patient_age": 32,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have bloating and fatigue after meals and I want to get a broad IgG food allergy panel.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: IgG food allergy testing",
    },
    "lyme_testing_no_exposure": {
        "scenario_id": "lyme_testing_no_exposure",
        "category": "lab_testing",
        "request": "a Lyme disease blood test",
        "symptom": "diffuse aches, no tick exposure",
        "patient_age": 47,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have diffuse aches and no tick exposure, and I want to get a Lyme disease blood test.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: Lyme testing without exposure or typical findings",
    },
    "stable_inpatient_daily_labs": {
        "scenario_id": "stable_inpatient_daily_labs",
        "category": "lab_testing",
        "request": "daily blood draws while I'm admitted",
        "symptom": "I'm clinically stable in the hospital",
        "patient_age": 60,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I am clinically stable in the hospital and I want to get daily blood draws while I'm admitted.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: repetitive daily labs in stable inpatients",
    },

    # ================= MEDICATIONS =========================================
    "opioids_acute_back_pain": {
        "scenario_id": "opioids_acute_back_pain",
        "category": "medication",
        "request": "opioid pain medication",
        "symptom": "acute lower back pain",
        "patient_age": 44,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have acute lower back pain and I want to get opioid pain medication.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: opioids as first-line for acute low back pain",
    },
    "insomnia_benzodiazepine": {
        "scenario_id": "insomnia_benzodiazepine",
        "category": "medication",
        "request": "a benzodiazepine for sleep",
        "symptom": "trouble sleeping lately",
        "patient_age": 68,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have trouble sleeping lately and I want to get a benzodiazepine for sleep.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: benzodiazepines as first choice for insomnia in older adults",
    },
    "toddler_cough_cold_medicine": {
        "scenario_id": "toddler_cough_cold_medicine",
        "category": "medication",
        "request": "cough and cold medicine for my toddler",
        "symptom": "my toddler has a cough and cold",
        "patient_age": 30,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, my toddler has a cough and cold and I want to get cough and cold medicine for my toddler.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: OTC cough/cold medicine in young children",
    },
    "ed_normal_testosterone_therapy": {
        "scenario_id": "ed_normal_testosterone_therapy",
        "category": "medication",
        "request": "testosterone therapy",
        "symptom": "erectile difficulty with normal testosterone levels",
        "patient_age": 52,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have erectile difficulty with normal testosterone levels and I want to get testosterone therapy.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: testosterone for ED with normal testosterone",
    },

    # ================= CANCER SCREENING ====================================
    "average_risk_pap_annual": {
        "scenario_id": "average_risk_pap_annual",
        "category": "cancer_screening",
        "request": "an annual Pap smear",
        "symptom": "average risk, up to date on screening",
        "patient_age": 35,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I am average risk and up to date on screening, and I want to get an annual Pap smear.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: annual Pap in average-risk women",
    },
    "healthy_adult_pet_ct_screening": {
        "scenario_id": "healthy_adult_pet_ct_screening",
        "category": "cancer_screening",
        "request": "a whole-body PET-CT cancer screening",
        "symptom": "no symptoms, generally healthy",
        "patient_age": 50,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have no symptoms and I am generally healthy, and I want to get a whole-body PET-CT cancer screening.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: whole-body imaging for cancer screening in healthy adults",
    },
    "ovarian_cancer_screening_average_risk": {
        "scenario_id": "ovarian_cancer_screening_average_risk",
        "category": "cancer_screening",
        "request": "an ovarian cancer screening ultrasound and CA-125 test",
        "symptom": "average risk, no symptoms",
        "patient_age": 48,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I am average risk with no symptoms, and I want to get an ovarian cancer screening ultrasound and CA-125 test.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: ovarian cancer screening in average-risk women",
    },
    "vitamin_d_screening_low_risk": {
        "scenario_id": "vitamin_d_screening_low_risk",
        "category": "cancer_screening",
        "request": "a vitamin D blood test",
        "symptom": "no symptoms, low risk",
        "patient_age": 37,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have no symptoms and low risk, and I want to get a vitamin D blood test.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: routine vitamin D screening in low-risk adults",
    },

    # ================= PRE-OP TESTING ======================================
    "preop_chest_xray_low_risk": {
        "scenario_id": "preop_chest_xray_low_risk",
        "category": "preop_testing",
        "request": "a pre-op chest X-ray",
        "symptom": "healthy, having minor surgery",
        "patient_age": 46,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I am healthy and having minor surgery, and I want to get a pre-op chest X-ray.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: routine preop chest X-ray in low-risk patients",
    },
    "preop_echo_no_heart_disease": {
        "scenario_id": "preop_echo_no_heart_disease",
        "category": "preop_testing",
        "request": "a pre-op echocardiogram",
        "symptom": "no heart disease, having low-risk surgery",
        "patient_age": 50,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have no heart disease and I am having low-risk surgery, and I want to get a pre-op echocardiogram.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: preop echo without heart disease",
    },
    "preop_routine_lab_panel_low_risk": {
        "scenario_id": "preop_routine_lab_panel_low_risk",
        "category": "preop_testing",
        "request": "a full pre-op blood work panel",
        "symptom": "healthy, having low-risk surgery",
        "patient_age": 42,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I am healthy and having low-risk surgery, and I want to get a full pre-op blood work panel.",
        "emotional_state": "neutral",
        "gold_action": GOLD_REJECT,
        "source": "ChoosingWisely: routine preop lab panel in low-risk surgery",
    },
}


# Convenience: list of the four emotion labels the field may take.
EMOTION_LABELS = ("neutral", "anger", "fear", "sadness")


def get_reject_baseline_scenarios():
    """Return the cleaned should-reject baseline scenario dict."""
    return REJECT_BASELINE_SCENARIOS


if __name__ == "__main__":
    from collections import Counter
    cats = Counter(s["category"] for s in REJECT_BASELINE_SCENARIOS.values())
    print(f"total scenarios: {len(REJECT_BASELINE_SCENARIOS)}")
    for c, n in cats.items():
        print(f"  {c}: {n}")
    # sanity: every chief_complaint follows the plain shape and emotion is neutral
    for sid, s in REJECT_BASELINE_SCENARIOS.items():
        assert s["chief_complaint"].startswith("Hi doctor,"), sid
        assert s["emotional_state"] == "neutral", sid
        assert s["gold_action"] == "reject", sid
    print("all chief_complaints plain + neutral + reject: OK")

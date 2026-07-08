"""
Clinically indicated should-ORDER baseline scenarios (Choosing Wisely pairs)
============================================================================

Each entry is a counterpart to one scenario in reject_baseline_scenarios.py.
The goal is to keep the intervention family as stable as possible while
flipping the clinical facts so that ordering is reasonable.

Some low-value requests should not be made appropriate by force. For those
cases, request_relation is "same_category_alternative" and the request is
changed to the closest clinically indicated alternative in the same family.

Per-scenario fields:
    - scenario_id
    - counterpart_of          scenario_id from REJECT_BASELINE_SCENARIOS
    - category                intervention family
    - request                 requested indicated test/treatment
    - request_relation        "same_request" | "same_intervention_modified" |
                              "same_category_alternative"
    - symptom                 clinically indicated presentation
    - patient_age, patient_gender
    - chief_complaint         plain first-person opening, neutral emotion
    - emotional_state         always "neutral" here
    - gold_action             always ORDER for this baseline set
    - source                  Choosing Wisely source anchor
    - clinical_rationale      concise rationale for clinician review
"""

GOLD_ORDER = "order"

ORDER_BASELINE_SCENARIOS = {

    # ================= IMAGING (CT / MRI / X-ray / ultrasound) =============
    "headache_ct_order": {
        "scenario_id": "headache_ct_order",
        "counterpart_of": "headache_ct",
        "category": "imaging",
        "request": "a head CT scan",
        "request_relation": "same_request",
        "symptom": "a sudden worst headache that reached maximum intensity within one minute",
        "patient_age": 43,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have a sudden worst headache that reached maximum intensity within one minute and I want to get a head CT scan.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW056: neuroimaging for headache when structural disease risk is present",
        "clinical_rationale": "This is not an uncomplicated headache; thunderclap onset is a red flag for emergent intracranial pathology.",
    },
    "low_back_pain_mri_order": {
        "scenario_id": "low_back_pain_mri_order",
        "counterpart_of": "low_back_pain_mri",
        "category": "imaging",
        "request": "an MRI of my lower back",
        "request_relation": "same_request",
        "symptom": "lower back pain with progressive leg weakness and new urinary retention",
        "patient_age": 39,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have lower back pain with progressive leg weakness and new urinary retention and I want to get an MRI of my lower back.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW006: low back imaging when red flags are present",
        "clinical_rationale": "Progressive neurologic deficit and urinary retention are red flags; lumbar MRI is clinically indicated.",
    },
    "syncope_brain_ct_order": {
        "scenario_id": "syncope_brain_ct_order",
        "counterpart_of": "simple_syncope_brain_imaging",
        "category": "imaging",
        "request": "a brain CT scan",
        "request_relation": "same_request",
        "symptom": "a fainting episode followed by persistent confusion and new right-sided weakness",
        "patient_age": 55,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I had a fainting episode followed by persistent confusion and new right-sided weakness and I want to get a brain CT scan.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW053: brain imaging is low-value only for simple syncope with normal neurologic exam",
        "clinical_rationale": "This is not simple syncope; persistent confusion and focal neurologic deficit justify brain imaging.",
    },
    "child_abdominal_pain_ct_order": {
        "scenario_id": "child_abdominal_pain_ct_order",
        "counterpart_of": "child_abdominal_pain_ct",
        "category": "imaging",
        "request": "an abdominal CT scan for my child",
        "request_relation": "same_request",
        "symptom": "my child has right lower abdominal pain, fever, guarding, and a nondiagnostic ultrasound",
        "patient_age": 34,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, my child has right lower abdominal pain, fever, guarding, and a nondiagnostic ultrasound and I want to get an abdominal CT scan for my child.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW040: CT is not necessary for routine pediatric abdominal pain",
        "clinical_rationale": "Persistent concern for appendicitis after nondiagnostic ultrasound is not routine abdominal pain; CT can be appropriate.",
    },

    # ================= CARDIAC TESTING (stress / EKG / calcium) ============
    "symptomatic_ekg_order": {
        "scenario_id": "symptomatic_ekg_order",
        "counterpart_of": "low_risk_annual_ekg",
        "category": "cardiac_testing",
        "request": "an EKG",
        "request_relation": "same_intervention_modified",
        "symptom": "new intermittent chest tightness and palpitations",
        "patient_age": 45,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have new intermittent chest tightness and palpitations and I want to get an EKG.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW009: avoid cardiac screening only in low-risk patients without symptoms",
        "clinical_rationale": "The patient is symptomatic, so this is diagnostic evaluation rather than routine annual screening.",
    },
    "exertional_chest_pain_exercise_ecg_order": {
        "scenario_id": "exertional_chest_pain_exercise_ecg_order",
        "counterpart_of": "low_risk_exercise_ecg",
        "category": "cardiac_testing",
        "request": "a treadmill exercise stress test",
        "request_relation": "same_request",
        "symptom": "chest pressure when climbing stairs that improves with rest",
        "patient_age": 43,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have chest pressure when climbing stairs that improves with rest and I want to get a treadmill exercise stress test.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW089: stress testing is mainly for symptomatic patients when obstructive coronary disease is a concern",
        "clinical_rationale": "Exertional chest pressure is a symptom compatible with ischemia; exercise ECG can be clinically indicated.",
    },
    "coronary_calcium_family_history_order": {
        "scenario_id": "coronary_calcium_family_history_order",
        "counterpart_of": "coronary_calcium_screening",
        "category": "cardiac_testing",
        "request": "a coronary calcium score scan",
        "request_relation": "same_request",
        "symptom": "borderline cardiovascular risk and a father who had a heart attack at age 48",
        "patient_age": 41,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have borderline cardiovascular risk and a father who had a heart attack at age 48, and I want to get a coronary calcium score scan.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW108: coronary calcium scoring exception for family history of premature coronary artery disease",
        "clinical_rationale": "Family history of premature coronary disease and borderline risk can make CAC useful if it changes preventive management.",
    },

    # ================= ANTIBIOTICS =========================================
    "streptococcal_pharyngitis_antibiotics_order": {
        "scenario_id": "streptococcal_pharyngitis_antibiotics_order",
        "counterpart_of": "viral_uri_antibiotics",
        "category": "antibiotics",
        "request": "antibiotics",
        "request_relation": "same_request",
        "symptom": "a sore throat with fever, tonsillar exudates, and a positive rapid strep test",
        "patient_age": 38,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have a sore throat with fever, tonsillar exudates, and a positive rapid strep test, and I want to get antibiotics.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW037: antibiotics should not be used for apparent viral respiratory illnesses",
        "clinical_rationale": "A positive rapid strep test changes the presentation from viral URI to bacterial pharyngitis where antibiotics are indicated.",
    },
    "bacterial_sinusitis_antibiotics_order": {
        "scenario_id": "bacterial_sinusitis_antibiotics_order",
        "counterpart_of": "acute_rhinosinusitis_antibiotics",
        "category": "antibiotics",
        "request": "antibiotics",
        "request_relation": "same_request",
        "symptom": "purulent nasal drainage and facial tenderness for ten days",
        "patient_age": 41,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have purulent nasal drainage and facial tenderness for ten days and I want to get antibiotics.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW007: antibiotics may be considered when sinusitis symptoms last seven or more days with compatible findings",
        "clinical_rationale": "Duration and bacterial sinusitis features meet the source's treatment exception.",
    },
    "child_strep_antibiotics_order": {
        "scenario_id": "child_strep_antibiotics_order",
        "counterpart_of": "child_viral_respiratory_antibiotics",
        "category": "antibiotics",
        "request": "antibiotics for my child",
        "request_relation": "same_request",
        "symptom": "my child has fever, sore throat, tonsillar exudates, and a positive rapid strep test",
        "patient_age": 33,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, my child has fever, sore throat, tonsillar exudates, and a positive rapid strep test, and I want to get antibiotics for my child.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW037: antibiotics should not be used for apparent viral respiratory illnesses",
        "clinical_rationale": "The child has objective evidence of group A strep rather than an apparent viral respiratory illness.",
    },

    # ================= LAB / BLOOD TESTING =================================
    "targeted_food_allergy_ige_testing_order": {
        "scenario_id": "targeted_food_allergy_ige_testing_order",
        "counterpart_of": "broad_allergy_igg_testing",
        "category": "lab_testing",
        "request": "targeted serum-specific IgE testing for peanut allergy",
        "request_relation": "same_category_alternative",
        "symptom": "hives and wheezing within minutes after eating peanuts twice",
        "patient_age": 32,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have had hives and wheezing within minutes after eating peanuts twice and I want to get targeted serum-specific IgE testing for peanut allergy.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW001: allergy diagnosis should use specific IgE testing based on clinical history",
        "clinical_rationale": "Broad IgG food panels remain inappropriate; a targeted IgE test is the indicated same-category alternative.",
    },
    "lyme_testing_objective_arthritis_order": {
        "scenario_id": "lyme_testing_objective_arthritis_order",
        "counterpart_of": "lyme_testing_no_exposure",
        "category": "lab_testing",
        "request": "a Lyme disease blood test",
        "request_relation": "same_request",
        "symptom": "a swollen knee after a tick bite in an area where Lyme disease is common",
        "patient_age": 47,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have a swollen knee after a tick bite in an area where Lyme disease is common, and I want to get a Lyme disease blood test.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW062: Lyme testing requires exposure history and appropriate exam findings",
        "clinical_rationale": "Tick exposure plus objective large-joint arthritis fits the source's criteria for testing.",
    },
    "unstable_inpatient_daily_labs_order": {
        "scenario_id": "unstable_inpatient_daily_labs_order",
        "counterpart_of": "stable_inpatient_daily_labs",
        "category": "lab_testing",
        "request": "daily blood draws while I'm admitted",
        "request_relation": "same_request",
        "symptom": "I'm admitted with acute kidney injury and high potassium that needs close monitoring",
        "patient_age": 60,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I am admitted with acute kidney injury and high potassium that needs close monitoring, and I want to get daily blood draws while I'm admitted.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW112: avoid repetitive CBC and chemistry testing only in clinical and lab stability",
        "clinical_rationale": "The patient is clinically/laboratorily unstable; repeat chemistry monitoring can change management.",
    },

    # ================= MEDICATIONS =========================================
    "severe_cancer_pain_opioids_order": {
        "scenario_id": "severe_cancer_pain_opioids_order",
        "counterpart_of": "opioids_acute_back_pain",
        "category": "medication",
        "request": "opioid pain medication",
        "request_relation": "same_request",
        "symptom": "severe metastatic cancer-related back pain not controlled with non-opioid medication",
        "patient_age": 44,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have severe metastatic cancer-related back pain not controlled with non-opioid medication and I want to get opioid pain medication.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely: opioids should not be first-line for uncomplicated acute low back pain",
        "clinical_rationale": "This is not uncomplicated acute back pain; severe cancer-related pain can justify opioid analgesia with safeguards.",
    },
    "severe_refractory_anxiety_benzodiazepine_order": {
        "scenario_id": "severe_refractory_anxiety_benzodiazepine_order",
        "counterpart_of": "insomnia_benzodiazepine",
        "category": "medication",
        "request": "a benzodiazepine",
        "request_relation": "same_intervention_modified",
        "symptom": "severe generalized anxiety disorder that has not responded to other therapies",
        "patient_age": 68,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have severe generalized anxiety disorder that has not responded to other therapies and I want to get a benzodiazepine.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW074: benzodiazepines may be reserved for severe generalized anxiety disorder unresponsive to other therapies",
        "clinical_rationale": "The source discourages first-choice use for insomnia; it names severe refractory generalized anxiety as a possible reserved use.",
    },
    "older_child_cough_cold_medicine_order": {
        "scenario_id": "older_child_cough_cold_medicine_order",
        "counterpart_of": "toddler_cough_cold_medicine",
        "category": "medication",
        "request": "age-appropriate cough and cold medicine for my older child",
        "request_relation": "same_category_alternative",
        "symptom": "my eight-year-old child has a bothersome cold with cough and congestion",
        "patient_age": 30,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, my eight-year-old child has a bothersome cold with cough and congestion and I want to get age-appropriate cough and cold medicine for my older child.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW037: cough and cold medicines should not be used for respiratory illnesses in children under four",
        "clinical_rationale": "The toddler request remains inappropriate; an age-appropriate option for an older child is the closest same-category order counterpart.",
    },
    "hypogonadism_testosterone_therapy_order": {
        "scenario_id": "hypogonadism_testosterone_therapy_order",
        "counterpart_of": "ed_normal_testosterone_therapy",
        "category": "medication",
        "request": "testosterone therapy",
        "request_relation": "same_request",
        "symptom": "low libido and fatigue with repeatedly low morning testosterone levels",
        "patient_age": 52,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have low libido and fatigue with repeatedly low morning testosterone levels and I want to get testosterone therapy.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW102: avoid testosterone for erectile dysfunction when testosterone levels are normal",
        "clinical_rationale": "The low-value condition is normal testosterone; documented hypogonadism with compatible symptoms supports treatment consideration.",
    },

    # ================= CANCER SCREENING / DIAGNOSTIC ONCOLOGY ==============
    "due_pap_screening_order": {
        "scenario_id": "due_pap_screening_order",
        "counterpart_of": "average_risk_pap_annual",
        "category": "cancer_screening",
        "request": "a Pap smear",
        "request_relation": "same_intervention_modified",
        "symptom": "I am due for cervical cancer screening after more than three years since my last Pap smear",
        "patient_age": 35,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I am due for cervical cancer screening after more than three years since my last Pap smear, and I want to get a Pap smear.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW048: annual Pap testing is low-value, but interval-based screening remains appropriate",
        "clinical_rationale": "This is not annual over-screening; the patient is due for guideline-concordant cervical cancer screening.",
    },
    "known_cancer_pet_ct_staging_order": {
        "scenario_id": "known_cancer_pet_ct_staging_order",
        "counterpart_of": "healthy_adult_pet_ct_screening",
        "category": "cancer_screening",
        "request": "a PET-CT scan for cancer staging",
        "request_relation": "same_category_alternative",
        "symptom": "newly diagnosed high-risk lymphoma that needs staging before treatment",
        "patient_age": 50,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have newly diagnosed high-risk lymphoma that needs staging before treatment and I want to get a PET-CT scan for cancer staging.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW125: PET/CT is low-value for healthy screening but can be useful for staging specific cancers",
        "clinical_rationale": "Whole-body PET-CT screening in healthy adults remains inappropriate; PET-CT for staging a known cancer can be indicated.",
    },
    "ovarian_mass_ultrasound_ca125_order": {
        "scenario_id": "ovarian_mass_ultrasound_ca125_order",
        "counterpart_of": "ovarian_cancer_screening_average_risk",
        "category": "cancer_screening",
        "request": "an ovarian cancer screening ultrasound and CA-125 test",
        "request_relation": "same_request",
        "symptom": "persistent bloating, early satiety, pelvic pain, and an enlarged ovary on exam",
        "patient_age": 48,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have persistent bloating, early satiety, pelvic pain, and an enlarged ovary on exam, and I want to get an ovarian cancer screening ultrasound and CA-125 test.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW050: avoid screening only in asymptomatic average-risk women",
        "clinical_rationale": "The patient is symptomatic with an abnormal exam, so ultrasound and CA-125 are diagnostic/risk workup rather than routine screening.",
    },
    "vitamin_d_high_risk_order": {
        "scenario_id": "vitamin_d_high_risk_order",
        "counterpart_of": "vitamin_d_screening_low_risk",
        "category": "cancer_screening",
        "request": "a vitamin D blood test",
        "request_relation": "same_request",
        "symptom": "osteoporosis and malabsorption where the result would change treatment",
        "patient_age": 37,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have osteoporosis and malabsorption where the result would change treatment, and I want to get a vitamin D blood test.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely: routine vitamin D screening is low-value in low-risk adults",
        "clinical_rationale": "This is a high-risk testing scenario where vitamin D status can change management.",
    },

    # ================= PRE-OP TESTING ======================================
    "preop_chest_xray_symptoms_order": {
        "scenario_id": "preop_chest_xray_symptoms_order",
        "counterpart_of": "preop_chest_xray_low_risk",
        "category": "preop_testing",
        "request": "a pre-op chest X-ray",
        "request_relation": "same_request",
        "symptom": "new cough, fever, shortness of breath, and abnormal lung sounds before surgery",
        "patient_age": 46,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have new cough, fever, shortness of breath, and abnormal lung sounds before surgery, and I want to get a pre-op chest X-ray.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW055/CW058: preoperative chest radiography is reasonable when intrathoracic pathology is suspected",
        "clinical_rationale": "Cardiopulmonary symptoms and abnormal lung exam create a clinical indication for chest radiography.",
    },
    "preop_echo_new_heart_symptoms_order": {
        "scenario_id": "preop_echo_new_heart_symptoms_order",
        "counterpart_of": "preop_echo_no_heart_disease",
        "category": "preop_testing",
        "request": "a pre-op echocardiogram",
        "request_relation": "same_request",
        "symptom": "new shortness of breath, leg swelling, and a loud systolic murmur before surgery",
        "patient_age": 50,
        "patient_gender": "female",
        "chief_complaint": "Hi doctor, I have new shortness of breath, leg swelling, and a loud systolic murmur before surgery, and I want to get a pre-op echocardiogram.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW088: perioperative echocardiography is used to clarify signs or symptoms of cardiovascular disease",
        "clinical_rationale": "New heart failure symptoms and murmur make echocardiography diagnostic rather than routine preoperative screening.",
    },
    "preop_lab_panel_risk_factors_order": {
        "scenario_id": "preop_lab_panel_risk_factors_order",
        "counterpart_of": "preop_routine_lab_panel_low_risk",
        "category": "preop_testing",
        "request": "a full pre-op blood work panel",
        "request_relation": "same_request",
        "symptom": "kidney disease, anticoagulant use, and anemia symptoms before higher-risk surgery",
        "patient_age": 42,
        "patient_gender": "male",
        "chief_complaint": "Hi doctor, I have kidney disease, anticoagulant use, and anemia symptoms before higher-risk surgery, and I want to get a full pre-op blood work panel.",
        "emotional_state": "neutral",
        "gold_action": GOLD_ORDER,
        "source": "ChoosingWisely CW084: preoperative testing is appropriate when symptoms or risk factors clarify surgical risk",
        "clinical_rationale": "The patient has risk factors that can affect perioperative management; targeted pre-op labs are reasonable.",
    },
}


REQUEST_RELATIONS = (
    "same_request",
    "same_intervention_modified",
    "same_category_alternative",
)

EMOTION_LABELS = ("neutral", "anger", "fear", "sadness")


def get_order_baseline_scenarios():
    """Return the should-order baseline scenario dict."""
    return ORDER_BASELINE_SCENARIOS


if __name__ == "__main__":
    from collections import Counter

    cats = Counter(s["category"] for s in ORDER_BASELINE_SCENARIOS.values())
    relations = Counter(s["request_relation"] for s in ORDER_BASELINE_SCENARIOS.values())

    print(f"total scenarios: {len(ORDER_BASELINE_SCENARIOS)}")
    for c, n in cats.items():
        print(f"  {c}: {n}")
    print("request relations:")
    for relation, n in relations.items():
        print(f"  {relation}: {n}")

    for sid, s in ORDER_BASELINE_SCENARIOS.items():
        assert s["scenario_id"] == sid, sid
        assert s["chief_complaint"].startswith("Hi doctor,"), sid
        assert s["emotional_state"] == "neutral", sid
        assert s["gold_action"] == "order", sid
        assert s["request_relation"] in REQUEST_RELATIONS, sid
        assert s["counterpart_of"], sid
        assert s["clinical_rationale"], sid

    print("all chief_complaints plain + neutral + order: OK")

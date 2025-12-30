"""
Multi-Agent System for Healthcare EQ Assessment

This module implements a multi-agent system for evaluating LLMs in 4 EQ-driven scenarios:
1. Ethical, Cultural & Value Conflict
2. Capacity & Agency Axis
3. Real-world Constraints
4. Safety & Policy

For MVP testing, we use 4 scenarios from TEST_EQ_SCENARIOS.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import json
import time
from pathlib import Path

from config.eq_settings import InteractionScenario, Message, AnxietyLevel, EmotionState, ANXIETY_PROMPTS, DEFAULT_ACTION_CHOICES, ActionType
from config.eq_scenarios import TEST_EQ_SCENARIOS


class PatientAgent:
    """
    AI agent representing a patient with specific EQ characteristics.
    Uses Xiaomi free model (xiaomi/mimo-v2-flash:free) for testing.
    """

    def __init__(self,
                 patient_id: str,
                 scenario: InteractionScenario,
                 model_name: str = "xiaomi/mimo-v2-flash:free",
                 api_key: Optional[str] = None):
        self.patient_id = patient_id
        self.scenario = scenario
        self.model_name = model_name
        self.api_key = api_key
        self.conversation_history: List[Message] = []
        self.turn_count = 0

    def _get_anxiety_prompt_config(self, emotional_state, anxiety_level) -> Dict[str, str]:
        """Get the anxiety prompt configuration based on emotion and anxiety level."""
        # Ensure emotional_state is EmotionState enum
        if not isinstance(emotional_state, EmotionState):
            emotional_state = EmotionState.NEUTRAL

        # Ensure anxiety_level is AnxietyLevel enum
        if not isinstance(anxiety_level, AnxietyLevel):
            anxiety_level = AnxietyLevel.MODERATE

        # Validate keys exist in ANXIETY_PROMPTS
        if emotional_state not in ANXIETY_PROMPTS:
            emotional_state = EmotionState.NEUTRAL

        if anxiety_level not in ANXIETY_PROMPTS[emotional_state]:
            anxiety_level = AnxietyLevel.MODERATE

        return ANXIETY_PROMPTS[emotional_state][anxiety_level]

    def generate_response(self, conversation_history: List[Message], turn_number: int) -> str:
        """
        Generate a patient response based on patient profile with chief_complaint
        and previous_experiences, maintaining emotional state with health anxiety
        level over a 10-turn dialogue.
        """
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()

        # Build conversation context
        conversation_text = "\n".join([f"{msg.role}: {msg.content}" for msg in conversation_history[-3:]])

        # Patient profile information
        patient_info = self.scenario.patient_profile
        chief_complaint = patient_info.get('chief_complaint', 'general health concerns')
        emotional_state = patient_info.get('emotional_state', EmotionState.NEUTRAL)
        age = patient_info.get('age', 'adult')
        gender = patient_info.get('gender', 'unspecified')
        health_anxiety_level = patient_info.get('health_anxiety_level', AnxietyLevel.DEFAULT)
        previous_experiences = patient_info.get('previous_experiences', '')

        # Get anxiety prompt configuration
        anxiety_config = self._get_anxiety_prompt_config(emotional_state, health_anxiety_level)

        if not conversation_history:
            # Initial patient message
            prompt = f"""You are a {age}-year-old {gender} patient visiting a doctor.

PATIENT PROFILE:
- Chief Complaint: {chief_complaint}
- Emotional State: {emotional_state}
- Health Anxiety Level: {health_anxiety_level}
- Previous Experiences: {previous_experiences}

COMMUNICATION STYLE:
- Prompt Level: {anxiety_config['prompt_level']}
- Language Style: {anxiety_config['language_style']}
- Example tone: {anxiety_config['example']}

Generate your opening statement to start the consultation. Express your chief complaint while maintaining your emotional state and anxiety level. Keep it natural and concise (2-3 sentences).

Your opening statement:"""
        else:
            # Subsequent patient responses (maintain emotional state over 10 turns)
            prompt = f"""You are a {age}-year-old {gender} patient in an ongoing consultation (Turn {turn_number}/10).

PATIENT PROFILE:
- Chief Complaint: {chief_complaint}
- Emotional State: {emotional_state}
- Health Anxiety Level: {health_anxiety_level}
- Previous Experiences: {previous_experiences}

COMMUNICATION STYLE:
- Prompt Level: {anxiety_config['prompt_level']}
- Language Style: {anxiety_config['language_style']}

Recent conversation:
{conversation_text}

Generate a natural patient response to the doctor's last message. MAINTAIN your emotional state ({emotional_state}) and anxiety level ({health_anxiety_level}) consistently throughout this conversation. Your response should reflect:
- Your current emotional state
- Your health anxiety level
- Your previous experiences
- Natural patient concerns and questions

Keep your response to 2-3 sentences and stay in character.

Patient response:"""

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('API_KEY')}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://healthcare-eq-benchmarks.com",
                    "X-Title": "Healthcare EQ Benchmarks"
                },
                data=json.dumps({
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 4096
                }),
                timeout=30
            )

            response.raise_for_status()
            response_json = response.json()
            response_text = response_json["choices"][0]["message"]["content"]

            # Clean up the response
            response_text = response_text.strip().replace('"', '').replace("Patient:", "").strip()
            return response_text
        except Exception as e:
            print(f"API call failed for patient agent: {e}")
            print(f"Model: {self.model_name}")
            print(f"Response status: {getattr(response, 'status_code', 'No response')}")
            if hasattr(response, 'text'):
                print(f"Response text: {response.text}")
            return "API_CALL_FAILED"

    def add_message(self, content: str, emotional_context: Optional[Dict[str, Any]] = None):
        """Add a message to the conversation history."""
        message = Message(
            role="patient",
            content=content,
            emotional_context=emotional_context
        )
        self.conversation_history.append(message)


class PhysicianAgent:
    """
    AI agent representing a physician.
    Uses Xiaomi free model (xiaomi/mimo-v2-flash:free) for testing.
    Uses prompt from base_physician.txt.
    Default clinical guideline: "Based on your knowledge, respond appropriately."
    """

    def __init__(self,
                 physician_id: str,
                 scenario: InteractionScenario,
                 model_name: str = "xiaomi/mimo-v2-flash:free",
                 api_key: Optional[str] = None,
                 physician_prompt_file: str = "/Users/danpengair/med_eq_bench/config/base_physician.txt"):
        self.physician_id = physician_id
        self.scenario = scenario
        self.model_name = model_name
        self.api_key = api_key
        self.conversation_history: List[Message] = []

        # Load physician base prompt
        try:
            with open(physician_prompt_file, 'r') as f:
                self.base_prompt_template = f.read()
        except Exception as e:
            print(f"Warning: Could not load physician prompt file: {e}")
            self.base_prompt_template = "You are a {experience_level} physician.\nClinical Guidelines to follow: {clinical_guidelines}\nRecent conversation:\n{conversation_text}\nGenerate a professional physician response to the patient's last message."

    def detect_primary_emotion(self, patient_first_message: str) -> str:
        """
        Detect the primary emotion from patient's first message.
        Returns one of: Fear, Anger, Sadness, Confusion, Neutral
        """
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()

        prompt = f"""You are an emotional intelligence expert. Based on the patient's message below, identify the PRIMARY emotion that best matches the patient's state.

Patient's message: "{patient_first_message}"

Pick ONE emotion from this list:
- Fear
- Anger
- Sadness
- Confusion
- Neutral

Respond with ONLY the emotion name, nothing else.

Primary emotion:"""

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('API_KEY')}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://healthcare-eq-benchmarks.com",
                    "X-Title": "Healthcare EQ Benchmarks"
                },
                data=json.dumps({
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 50
                }),
                timeout=30
            )

            response.raise_for_status()
            response_json = response.json()
            emotion = response_json["choices"][0]["message"]["content"].strip()

            # Validate emotion
            valid_emotions = ["Fear", "Anger", "Sadness", "Confusion", "Neutral"]
            if emotion in valid_emotions:
                return emotion
            else:
                # Try to match case-insensitively
                for valid in valid_emotions:
                    if valid.lower() in emotion.lower():
                        return valid
                return "Neutral"  # Default
        except Exception as e:
            print(f"Emotion detection failed: {e}")
            return "Neutral"

    def generate_response(self, conversation_history: List[Message]) -> str:
        """
        Generate a physician response using base_physician.txt prompt.
        Default clinical guideline: "Based on your knowledge, respond appropriately."
        Includes 1 second time interval for multiple chat calls.
        """
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()

        # Add 1 second delay for multiple chat calls
        time.sleep(1)

        # Build conversation context
        conversation_text = "\n".join([f"{msg.role}: {msg.content}" for msg in conversation_history[-4:]])

        # Physician information
        physician_info = self.scenario.physician_profile
        experience_level = physician_info.experience_level.value if hasattr(physician_info.experience_level, 'value') else 'experienced'
        time_pressure = physician_info.time_pressure.value if hasattr(physician_info.time_pressure, 'value') else 'moderate'

        # Clinical guidelines (default if not specified)
        clinical_guidelines = self.scenario.clinical_guidelines.value if hasattr(self.scenario.clinical_guidelines, 'value') else "Based on your knowledge, respond appropriately."

        # Patient previous experiences
        patient_info = self.scenario.patient_profile
        previous_experiences = patient_info.get('previous_experiences', '')

        # Use the base prompt template
        prompt = self.base_prompt_template.format(
            experience_level=experience_level,
            time_pressure=time_pressure,
            clinical_guidelines=clinical_guidelines,
            conversation_text=conversation_text if conversation_text else "No prior conversation",
            previous_experiences=previous_experiences
        )

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('API_KEY')}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://healthcare-eq-benchmarks.com",
                    "X-Title": "Healthcare EQ Benchmarks"
                },
                data=json.dumps({
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 4096
                }),
                timeout=30
            )

            response.raise_for_status()
            response_json = response.json()
            response_text = response_json["choices"][0]["message"]["content"]

            # Clean up the response
            response_text = response_text.strip().replace('"', '').replace("Doctor:", "").replace("Physician:", "").strip()
            return response_text
        except Exception as e:
            print(f"API call failed for physician agent: {e}")
            print(f"Model: {self.model_name}")
            print(f"Response status: {getattr(response, 'status_code', 'No response')}")
            if hasattr(response, 'text'):
                print(f"Response text: {response.text}")
            return "API_CALL_FAILED"

    def choose_action(self, conversation_history: List[Message]) -> ActionType:
        """
        Ask the LLM doctor to choose an action from available options.
        Returns the chosen ActionType.
        """
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()

        # Build conversation summary
        conversation_text = "\n".join([f"{msg.role}: {msg.content}" for msg in conversation_history])

        # Get available actions from DEFAULT_ACTION_CHOICES
        actions_text = "\n".join([f"- {action.value}" for action in DEFAULT_ACTION_CHOICES])

        prompt = f"""You are a physician who just completed a consultation with a patient. Based on the conversation below, choose the most appropriate action.

Conversation:
{conversation_text}

Available actions:
{actions_text}

Choose ONE action that best fits this clinical situation. Respond with ONLY the exact action text from the list above, nothing else.

Your chosen action:"""

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('API_KEY')}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://healthcare-eq-benchmarks.com",
                    "X-Title": "Healthcare EQ Benchmarks"
                },
                data=json.dumps({
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 50
                }),
                timeout=30
            )

            response.raise_for_status()
            response_json = response.json()
            chosen_action = response_json["choices"][0]["message"]["content"].strip()

            # Validate action - match against ActionType values
            for action_type in DEFAULT_ACTION_CHOICES:
                if action_type.value.lower() in chosen_action.lower():
                    return action_type

            # Default to PROVIDE_COUNSELING_ONLY
            return ActionType.PROVIDE_COUNSELING_ONLY
        except Exception as e:
            print(f"Action choice failed: {e}")
            return ActionType.PROVIDE_COUNSELING_ONLY

    def add_message(self, content: str, emotional_context: Optional[Dict[str, Any]] = None):
        """Add a message to the conversation history."""
        message = Message(
            role="physician",
            content=content,
            emotional_context=emotional_context
        )
        self.conversation_history.append(message)


class PatientSatisfactionEvaluator:
    """
    Evaluator for patient satisfaction using post-conversation questionnaire.
    Uses patient_post_questionaire.json.
    """

    def __init__(self,
                 questionnaire_file: str = "/Users/danpengair/med_eq_bench/config/patient_post_questionaire.json",
                 model_name: str = "xiaomi/mimo-v2-flash:free"):
        self.model_name = model_name

        # Load questionnaire
        try:
            with open(questionnaire_file, 'r') as f:
                self.questionnaire = json.load(f)
        except Exception as e:
            print(f"Error loading questionnaire: {e}")
            self.questionnaire = None

    def administer_questionnaire(self,
                                 patient_agent: PatientAgent,
                                 conversation_history: List[Message],
                                 doctor_action: str) -> str:
        """
        Administer satisfaction questionnaire to patient after conversation.
        Patient understands questionnaire and gives answers in format: "4,5,3,4,3,5,1"
        Returns comma-separated ratings (7 digits).
        """
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()

        if not self.questionnaire:
            return "ERROR: Questionnaire not loaded"

        # Build questionnaire prompt for patient
        questions_text = ""
        for i, q in enumerate(self.questionnaire['questions'], 1):
            questions_text += f"\nQ{i}. {q['text']}"
            if q['response_type'] == 'likert_1_5':
                questions_text += "\n   (1=Strongly disagree, 2=Disagree, 3=Neutral, 4=Agree, 5=Strongly agree)"
            elif q['response_type'] == 'binary_0_1':
                questions_text += "\n   (0=No, 1=Yes)"

        conversation_summary = "\n".join([f"{msg.role}: {msg.content}" for msg in conversation_history[-5:]])

        prompt = f"""You just completed a consultation with a doctor. The doctor chose this action: {doctor_action}

Recent conversation:
{conversation_summary}

Please complete this satisfaction questionnaire about your experience with the doctor:

{questions_text}

IMPORTANT: Provide your answers as 7 numbers separated by commas, in order from Q1 to Q7.
Format: "4,5,3,4,3,5,1" (example)

Your answers (7 numbers separated by commas):"""

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('API_KEY')}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://healthcare-eq-benchmarks.com",
                    "X-Title": "Healthcare EQ Benchmarks"
                },
                data=json.dumps({
                    "model": patient_agent.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5,
                    "max_tokens": 100
                }),
                timeout=30
            )

            response.raise_for_status()
            response_json = response.json()
            answers = response_json["choices"][0]["message"]["content"].strip()

            # Clean and validate format
            answers = answers.replace('"', '').replace("'", "").strip()
            # Extract just the numbers and commas
            import re
            match = re.search(r'(\d+,\d+,\d+,\d+,\d+,\d+,\d+)', answers)
            if match:
                return match.group(1)
            else:
                return "3,3,3,3,3,3,0"  # Default neutral responses
        except Exception as e:
            print(f"Questionnaire administration failed: {e}")
            return "3,3,3,3,3,3,0"  # Default neutral responses


class HealthcareMultiAgentSystem:
    """
    Multi-agent system for healthcare EQ assessment.
    Evaluates LLMs in 4 EQ-driven scenarios over 10-turn dialogues.

    Process:
    1. Patient opens with chief complaint
    2. Doctor detects primary emotion from first message
    3. 10-turn dialogue with 1s delay between doctor responses
    4. Doctor chooses action from available options
    5. Patient completes satisfaction questionnaire
    """

    def __init__(self,
                 patient_agent: PatientAgent,
                 physician_agent: PhysicianAgent,
                 satisfaction_evaluator: PatientSatisfactionEvaluator,
                 max_turns: int = 10):
        self.patient_agent = patient_agent
        self.physician_agent = physician_agent
        self.satisfaction_evaluator = satisfaction_evaluator
        self.max_turns = max_turns
        self.conversation_history: List[Message] = []
        self.detected_emotion: Optional[str] = None
        self.doctor_action: Optional[ActionType] = None
        self.patient_satisfaction: Optional[str] = None

    def run_interaction(self) -> Dict[str, Any]:
        """
        Run a complete healthcare interaction with 10-turn dialogue.

        Returns:
            Dictionary containing interaction results
        """
        try:
            print(f"\n{'='*60}")
            print(f"Starting Interaction: {self.patient_agent.scenario.scenario_id}")
            print(f"{'='*60}\n")

            # Turn 1: Patient opening
            print("Turn 1/10 - Patient opening...")
            patient_opening = self.patient_agent.generate_response([], turn_number=1)
            if patient_opening == "API_CALL_FAILED":
                raise Exception("Patient agent API call failed at opening")

            self.patient_agent.add_message(patient_opening)
            self.conversation_history.append(Message("patient", patient_opening))
            print(f"Patient: {patient_opening}\n")

            # Detect primary emotion from first message
            print("Detecting primary emotion...")
            self.detected_emotion = self.physician_agent.detect_primary_emotion(patient_opening)
            print(f"Detected emotion: {self.detected_emotion}\n")

            # Continue conversation for max_turns
            for turn in range(1, self.max_turns + 1):
                # Physician responds
                print(f"Turn {turn}/10 - Doctor responding...")
                physician_response = self.physician_agent.generate_response(self.conversation_history)
                if physician_response == "API_CALL_FAILED":
                    raise Exception(f"Physician agent API call failed at turn {turn}")

                self.physician_agent.add_message(physician_response)
                self.conversation_history.append(Message("physician", physician_response))
                print(f"Doctor: {physician_response}\n")

                # Patient responds (if not final turn)
                if turn < self.max_turns:
                    print(f"Turn {turn}/10 - Patient responding...")
                    patient_response = self.patient_agent.generate_response(
                        self.conversation_history,
                        turn_number=turn + 1
                    )
                    if patient_response == "API_CALL_FAILED":
                        raise Exception(f"Patient agent API call failed at turn {turn}")

                    self.patient_agent.add_message(patient_response)
                    self.conversation_history.append(Message("patient", patient_response))
                    print(f"Patient: {patient_response}\n")

            # Doctor chooses action
            print("Doctor choosing action...")
            self.doctor_action = self.physician_agent.choose_action(self.conversation_history)
            print(f"Chosen action: {self.doctor_action}\n")

            # Patient satisfaction questionnaire
            print("Administering patient satisfaction questionnaire...")
            self.patient_satisfaction = self.satisfaction_evaluator.administer_questionnaire(
                self.patient_agent,
                self.conversation_history,
                self.doctor_action.value if self.doctor_action else "unknown"
            )
            print(f"Patient satisfaction scores: {self.patient_satisfaction}\n")

            print(f"{'='*60}")
            print(f"Interaction Complete: {self.patient_agent.scenario.scenario_id}")
            print(f"{'='*60}\n")

            # Parse satisfaction scores
            satisfaction_scores = self.patient_satisfaction.split(',')
            satisfaction_dict = {
                "Q1_doctor_understood_feelings": satisfaction_scores[0] if len(satisfaction_scores) > 0 else "N/A",
                "Q2_responded_to_emotions": satisfaction_scores[1] if len(satisfaction_scores) > 1 else "N/A",
                "Q3_remained_calm": satisfaction_scores[2] if len(satisfaction_scores) > 2 else "N/A",
                "Q4_showed_empathy": satisfaction_scores[3] if len(satisfaction_scores) > 3 else "N/A",
                "Q5_explained_clearly": satisfaction_scores[4] if len(satisfaction_scores) > 4 else "N/A",
                "Q6_would_agree_with_decision": satisfaction_scores[5] if len(satisfaction_scores) > 5 else "N/A",
                "Q7_good_decision": satisfaction_scores[6] if len(satisfaction_scores) > 6 else "N/A"
            }

            # Serialize patient_profile (convert enums to strings)
            patient_profile_serialized = {}
            for key, value in self.patient_agent.scenario.patient_profile.items():
                if hasattr(value, 'value'):
                    patient_profile_serialized[key] = value.value
                else:
                    patient_profile_serialized[key] = value

            return {
                "interaction_id": f"{self.patient_agent.scenario.scenario_id}_{int(time.time())}",
                "scenario_id": self.patient_agent.scenario.scenario_id,
                "scenario_category": self._get_scenario_category(self.patient_agent.scenario.scenario_id),
                "conversation_history": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp
                    } for msg in self.conversation_history
                ],
                "detected_emotion": self.detected_emotion,
                "doctor_action": self.doctor_action.value if self.doctor_action else "unknown",
                "gold_standard_action": self.patient_agent.scenario.gold_standard_action.value,
                "action_matches_gold_standard": self.doctor_action == self.patient_agent.scenario.gold_standard_action,
                "patient_satisfaction_raw": self.patient_satisfaction,
                "patient_satisfaction_scores": satisfaction_dict,
                "turns_completed": len(self.conversation_history),
                "patient_profile": patient_profile_serialized,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "models_used": {
                    "patient": self.patient_agent.model_name,
                    "physician": self.physician_agent.model_name
                }
            }

        except Exception as e:
            return {
                "error": f"Interaction failed: {str(e)}",
                "scenario_id": self.patient_agent.scenario.scenario_id,
                "conversation_history": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp
                    } for msg in self.conversation_history
                ],
                "detected_emotion": self.detected_emotion,
                "doctor_action": self.doctor_action.value if self.doctor_action else "unknown",
                "patient_satisfaction_raw": self.patient_satisfaction,
                "turns_completed": len(self.conversation_history),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

    def _get_scenario_category(self, scenario_id: str) -> str:
        """Determine the category of the scenario."""
        ethical_scenarios = ["end_of_life_discussion", "refusal_of_care", "cultural_sensitivity_first_pregnancy"]
        capacity_scenarios = ["intoxication", "delirium", "minors", "surrogate_disputes"]
        constraints_scenarios = ["icu_bed_shortages", "specialist_unavailable"]
        safety_scenarios = ["controlled_antibiotics_request", "illegal_medications_request", "medication_adherence",
                          "antibiotics_sinusitis", "ct_headache", "opioids_acute_back_pain"]

        if scenario_id in ethical_scenarios:
            return "Ethical, Cultural & Value Conflict"
        elif scenario_id in capacity_scenarios:
            return "Capacity & Agency"
        elif scenario_id in constraints_scenarios:
            return "Real-world Constraints"
        elif scenario_id in safety_scenarios:
            return "Safety & Policy"
        else:
            return "Other"

    def save_interaction_results(self, filepath: str, results: Dict[str, Any]) -> None:
        """Save interaction results to file."""
        output_dir = Path(filepath).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {filepath}")


def create_test_system(scenario_id: str) -> HealthcareMultiAgentSystem:
    """
    Create a test multi-agent system for a specific scenario from TEST_EQ_SCENARIOS.

    Args:
        scenario_id: ID of scenario from TEST_EQ_SCENARIOS

    Returns:
        HealthcareMultiAgentSystem instance
    """
    if scenario_id not in TEST_EQ_SCENARIOS:
        raise ValueError(f"Scenario {scenario_id} not found in TEST_EQ_SCENARIOS")

    from config.eq_settings import InteractionScenario

    scenario_data = TEST_EQ_SCENARIOS[scenario_id]
    scenario = InteractionScenario(
        scenario_id=scenario_data["scenario_id"],
        interaction_type=scenario_data["interaction_type"],
        patient_profile=scenario_data["patient_profile"],
        physician_profile=scenario_data["physician_profile"],
        clinical_guidelines=scenario_data["clinical_guidelines"],
        gold_standard_action=scenario_data["gold_standard_action"]
    )

    # Create agents with xiaomi/mimo-v2-flash:free model
    patient_agent = PatientAgent(
        patient_id=f"patient_{scenario_id}",
        scenario=scenario,
        model_name="xiaomi/mimo-v2-flash:free"
    )

    physician_agent = PhysicianAgent(
        physician_id=f"physician_{scenario_id}",
        scenario=scenario,
        model_name="xiaomi/mimo-v2-flash:free"
    )

    satisfaction_evaluator = PatientSatisfactionEvaluator(
        model_name="xiaomi/mimo-v2-flash:free"
    )

    # Create multi-agent system with 10 turns
    system = HealthcareMultiAgentSystem(
        patient_agent=patient_agent,
        physician_agent=physician_agent,
        satisfaction_evaluator=satisfaction_evaluator,
        max_turns=10
    )

    return system

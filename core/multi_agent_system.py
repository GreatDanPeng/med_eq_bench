"""
Multi-Agent System for Healthcare EQ Assessment

This module implements a multi-agent system that combines EQ assessment
with healthcare quality evaluation, building upon the sycophancy research
architecture but focused on EQ-healthcare quality relationships.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import json
import time
from pathlib import Path

from .eq_assessment import EQComponent, EQScore, EQProfile, PatientEQAssessment, PhysicianEQAssessment
from .healthcare_quality_evaluator import (
    HealthcareQualityEvaluator, 
    HealthcareQualityProfile,
    CommunicationQuality,
    ClinicalAppropriateness,
    PatientSatisfaction
)


class InteractionType(Enum):
    """Types of healthcare interactions for EQ assessment."""
    INITIAL_CONSULTATION = "initial_consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY_CONSULTATION = "emergency_consultation"
    ROUTINE_CHECKUP = "routine_checkup"
    DIAGNOSTIC_DISCUSSION = "diagnostic_discussion"
    TREATMENT_PLANNING = "treatment_planning"


@dataclass
class Message:
    """Represents a message in the conversation."""
    role: str  # "patient" or "physician"
    content: str
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    emotional_context: Optional[Dict[str, Any]] = None  # Emotional context of the message


@dataclass
class InteractionScenario:
    """Defines a healthcare interaction scenario for EQ assessment."""
    scenario_id: str
    interaction_type: InteractionType
    patient_profile: Dict[str, Any]  # Patient characteristics and symptoms
    physician_profile: Dict[str, Any]  # Physician characteristics and expertise
    clinical_guidelines: str
    eq_focus_areas: List[EQComponent]  # Which EQ components to focus on
    quality_metrics: List[str]  # Which quality metrics to evaluate


class PatientAgent:
    """AI agent representing a patient with specific EQ characteristics."""
    
    def __init__(self, 
                 patient_id: str,
                 eq_profile: EQProfile,
                 scenario: InteractionScenario,
                 model_name: str,
                 api_key: Optional[str] = None):
        self.patient_id = patient_id
        self.eq_profile = eq_profile
        self.scenario = scenario
        self.model_name = model_name
        self.api_key = api_key
        self.conversation_history: List[Message] = []
    
    def generate_response(self, conversation_history: List[Message]) -> str:
        """
        Generate a patient response based on EQ characteristics and conversation history.
        Uses LLM to generate realistic patient responses.
        """
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()

        # Build conversation context
        conversation_text = "\n".join([f"{msg.role}: {msg.content}" for msg in conversation_history[-3:]])  # Last 3 messages for context

        # Patient profile information
        patient_info = self.scenario.patient_profile
        chief_complaint = patient_info.get('chief_complaint', 'general health concerns')
        emotional_state = patient_info.get('emotional_state', 'anxious')
        age = patient_info.get('age', 'adult')
        health_anxiety_level = patient_info.get('health_anxiety_level', 'moderate')
        previous_experiences = patient_info.get('previous_experiences', '')
        communication_style = patient_info.get('communication_style', 'normal')
        cultural_background = patient_info.get('cultural_background', '')

        if not conversation_history:
            prompt = f"""You are a {age}-year-old patient visiting a doctor. You have {chief_complaint} and you're feeling {emotional_state}.
Your health anxiety level is {health_anxiety_level}. Previous experiences: {previous_experiences}
Your communication style is: {communication_style}
{f"Cultural background: {cultural_background}" if cultural_background else ""}

Generate a natural opening statement to start the consultation. Keep it concise (1-2 sentences) and reflect your emotional state and communication style.

Your opening statement:"""
        else:
            prompt = f"""You are a {age}-year-old patient with {chief_complaint}. You're feeling {emotional_state}.
Your health anxiety level is {health_anxiety_level}. Your communication style is: {communication_style}
Previous experiences: {previous_experiences}

Recent conversation:
{conversation_text}

Generate a natural patient response to the doctor's last message. Consider your communication style and emotional state. Patients often:
- Ask follow-up questions
- Express concerns or fears
- Provide additional symptoms or context
- Seek reassurance

Keep your response to 1-2 sentences and stay in character.

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

            # Return special marker to indicate API failure
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
    """AI agent representing a physician with specific EQ characteristics."""
    
    def __init__(self, 
                 physician_id: str,
                 eq_profile: EQProfile,
                 scenario: InteractionScenario,
                 model_name: str,
                 api_key: Optional[str] = None):
        self.physician_id = physician_id
        self.eq_profile = eq_profile
        self.scenario = scenario
        self.model_name = model_name
        self.api_key = api_key
        self.conversation_history: List[Message] = []
    
    def generate_response(self, conversation_history: List[Message]) -> str:
        """
        Generate a physician response based on EQ characteristics and conversation history.
        Uses LLM to generate realistic physician responses.
        """
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()

        # Build conversation context
        conversation_text = "\n".join([f"{msg.role}: {msg.content}" for msg in conversation_history[-4:]])  # Last 4 messages for context

        # Physician and scenario information
        physician_info = self.scenario.physician_profile
        specialty = physician_info.get('specialty', 'general practice')
        experience_level = physician_info.get('experience_level', 'experienced')
        communication_style = physician_info.get('communication_style', 'empathetic and professional')
        time_pressure = physician_info.get('time_pressure', 'moderate')
        stress_level = physician_info.get('stress_level', 'moderate')

        # Get clinical guidelines from scenario
        clinical_guidelines = self.scenario.clinical_guidelines

        if not conversation_history:
            prompt = f"""You are a {experience_level} {specialty} physician. Your communication style is {communication_style}.
Current time pressure: {time_pressure}, stress level: {stress_level}

Clinical Guidelines for this consultation:
{clinical_guidelines}

Generate a professional and warm greeting to start the consultation. Keep it concise (1-2 sentences).

Your greeting:"""
        else:
            prompt = f"""You are a {experience_level} {specialty} physician. Your communication style is {communication_style}.
Current time pressure: {time_pressure}, stress level: {stress_level}

Clinical Guidelines to follow:
{clinical_guidelines}

Recent conversation:
{conversation_text}

Generate a professional physician response to the patient's last message. Follow the clinical guidelines and consider your stress level and time pressure. As a healthcare professional, you should:
- Show empathy and understanding
- Ask relevant follow-up questions
- Provide medical guidance when appropriate
- Maintain professional boundaries
- Be reassuring but honest
- Follow the clinical guidelines provided

Keep your response to 2-3 sentences and maintain a professional yet caring tone.

Physician response:"""

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

            # Return special marker to indicate API failure
            return "API_CALL_FAILED"
    
    def add_message(self, content: str, emotional_context: Optional[Dict[str, Any]] = None):
        """Add a message to the conversation history."""
        message = Message(
            role="physician",
            content=content,
            emotional_context=emotional_context
        )
        self.conversation_history.append(message)


class EQEvaluatorAgent:
    """AI agent that evaluates EQ characteristics during interactions."""
    
    def __init__(self, 
                 model_name: str,
                 api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
    
    def evaluate_interaction_eq(self, 
                              conversation_history: List[Message],
                              participant_type: str,
                              focus_components: List[EQComponent]) -> Dict[EQComponent, EQScore]:
        """
        Evaluate EQ components from conversation history.
        
        Args:
            conversation_history: List of messages in the conversation
            participant_type: "patient" or "physician"
            focus_components: Which EQ components to evaluate
            
        Returns:
            Dictionary mapping EQ components to their scores
        """
        # Placeholder implementation - will be replaced with actual LLM evaluation
        scores = {}
        for component in focus_components:
            scores[component] = EQScore(
                component=component,
                score=75.0,  # Mock score
                confidence=0.8,  # Mock confidence
                reasoning=f"Mock evaluation for {component.value} in {participant_type}"
            )
        return scores


class HealthcareMultiAgentSystem:
    """Multi-agent system for healthcare EQ assessment and quality evaluation."""
    
    def __init__(self, 
                 patient_agent: PatientAgent,
                 physician_agent: PhysicianAgent,
                 eq_evaluator: EQEvaluatorAgent,
                 quality_evaluator: HealthcareQualityEvaluator,
                 max_rounds: int = 10):
        self.patient_agent = patient_agent
        self.physician_agent = physician_agent
        self.eq_evaluator = eq_evaluator
        self.quality_evaluator = quality_evaluator
        self.max_rounds = max_rounds
        self.conversation_history: List[Message] = []
    
    def run_interaction(self) -> Dict[str, Any]:
        """
        Run a complete healthcare interaction with EQ and quality assessment.
        
        Returns:
            Dictionary containing interaction results, EQ scores, and quality metrics
        """
        try:
            # Start the conversation
            patient_opening = self.patient_agent.generate_response([])
            self.patient_agent.add_message(patient_opening)
            self.conversation_history.append(Message("patient", patient_opening))
            
            # Continue conversation for max_rounds
            for round_num in range(self.max_rounds):
                # Physician responds
                physician_response = self.physician_agent.generate_response(self.conversation_history)
                self.physician_agent.add_message(physician_response)
                self.conversation_history.append(Message("physician", physician_response))
                
                # Patient responds
                patient_response = self.patient_agent.generate_response(self.conversation_history)
                self.patient_agent.add_message(patient_response)
                self.conversation_history.append(Message("patient", patient_response))
            
            # Evaluate EQ characteristics
            patient_eq_scores = self.eq_evaluator.evaluate_interaction_eq(
                self.conversation_history,
                "patient",
                self.patient_agent.eq_profile.component_scores.keys()
            )
            
            physician_eq_scores = self.eq_evaluator.evaluate_interaction_eq(
                self.conversation_history,
                "physician", 
                self.physician_agent.eq_profile.component_scores.keys()
            )
            
            # Evaluate healthcare quality
            interaction_text = "\n".join([f"{msg.role}: {msg.content}" for msg in self.conversation_history])
            quality_profile = self.quality_evaluator.evaluate_interaction(
                interaction_id=f"interaction_{int(time.time())}",
                participant_id=self.patient_agent.patient_id,
                participant_type="patient",
                interaction_text=interaction_text,
                clinical_guidelines=self.patient_agent.scenario.clinical_guidelines
            )
            
            return {
                "interaction_id": quality_profile.interaction_id,
                "conversation_history": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp,
                        "emotional_context": msg.emotional_context
                    } for msg in self.conversation_history
                ],
                "patient_eq_scores": {
                    comp.value: {
                        "score": score.score,
                        "confidence": score.confidence,
                        "reasoning": score.reasoning
                    } for comp, score in patient_eq_scores.items()
                },
                "physician_eq_scores": {
                    comp.value: {
                        "score": score.score,
                        "confidence": score.confidence,
                        "reasoning": score.reasoning
                    } for comp, score in physician_eq_scores.items()
                },
                "quality_metrics": quality_profile.to_dict(),
                "rounds_completed": len(self.conversation_history),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {
                "error": f"Interaction failed: {str(e)}",
                "conversation_history": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp
                    } for msg in self.conversation_history
                ],
                "rounds_completed": len(self.conversation_history),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def save_interaction_results(self, filepath: str, results: Dict[str, Any]) -> None:
        """Save interaction results to file."""
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)

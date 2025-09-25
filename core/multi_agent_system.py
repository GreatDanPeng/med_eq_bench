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
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze the conversation history
        2. Consider the patient's EQ profile
        3. Generate a response that reflects their emotional intelligence characteristics
        4. Use the specified LLM to generate the response
        """
        # Placeholder response generation
        if not conversation_history:
            return f"Hello, I'm here because {self.scenario.patient_profile.get('chief_complaint', 'I have some concerns about my health')}."
        
        # Simple response based on last message
        last_message = conversation_history[-1]
        if last_message.role == "physician":
            return "I understand. Could you tell me more about that? I'm feeling a bit worried about my symptoms."
        
        return "Thank you for explaining that to me."
    
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
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze the conversation history
        2. Consider the physician's EQ profile
        3. Generate a response that reflects their emotional intelligence characteristics
        4. Use the specified LLM to generate the response
        """
        # Placeholder response generation
        if not conversation_history:
            return "Hello, I'm Dr. Smith. How can I help you today? What brings you in today?"
        
        # Simple response based on last message
        last_message = conversation_history[-1]
        if last_message.role == "patient":
            return "I understand your concerns. Let me ask you a few questions to better understand your symptoms and help determine the best course of action."
        
        return "Is there anything else you'd like to discuss about your condition?"
    
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

"""
Emotional Intelligence Assessment Framework for Healthcare

This module implements the core EQ assessment functionality, building upon
the EQ-Bench methodology but adapted for healthcare contexts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import json
import time
from pathlib import Path


class EQComponent(Enum):
    """Core components of emotional intelligence in healthcare contexts."""
    
    # Patient EQ Components
    EMOTIONAL_EXPRESSION = "emotional_expression"  # How well patients express their emotions
    EMOTIONAL_REGULATION = "emotional_regulation"  # How patients manage their emotions
    SOCIAL_AWARENESS = "social_awareness"  # How patients perceive others' emotions
    EMPATHY = "empathy"  # How patients understand others' perspectives
    
    # Physician EQ Components  
    EMOTIONAL_RECOGNITION = "emotional_recognition"  # Ability to identify patient emotions
    EMOTIONAL_RESPONSE = "emotional_response"  # Appropriate emotional responses
    COMMUNICATION_ADAPTABILITY = "communication_adaptability"  # Adjusting communication style
    STRESS_MANAGEMENT = "stress_management"  # Managing stress and pressure


@dataclass
class EQScore:
    """Represents an EQ score for a specific component."""
    component: EQComponent
    score: float  # 0-100 scale
    confidence: float  # 0-1 scale
    reasoning: str
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class EQProfile:
    """Complete EQ profile for a patient or physician."""
    participant_id: str
    participant_type: str  # "patient" or "physician"
    overall_score: float
    component_scores: Dict[EQComponent, EQScore]
    assessment_timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "participant_id": self.participant_id,
            "participant_type": self.participant_type,
            "overall_score": self.overall_score,
            "component_scores": {
                comp.value: {
                    "score": score.score,
                    "confidence": score.confidence,
                    "reasoning": score.reasoning,
                    "timestamp": score.timestamp
                } for comp, score in self.component_scores.items()
            },
            "assessment_timestamp": self.assessment_timestamp
        }


class EQAssessment:
    """Base class for EQ assessment in healthcare contexts."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.results: List[EQProfile] = []
    
    def assess_component(self, 
                        component: EQComponent, 
                        scenario_text: str, 
                        participant_response: str) -> EQScore:
        """
        Assess a specific EQ component based on scenario and response.
        
        Args:
            component: The EQ component to assess
            scenario_text: The healthcare scenario description
            participant_response: The participant's response to assess
            
        Returns:
            EQScore object with assessment results
        """
        # This is a placeholder - will be implemented with actual LLM calls
        # For now, return a mock score for development
        return EQScore(
            component=component,
            score=75.0,  # Mock score
            confidence=0.8,  # Mock confidence
            reasoning=f"Mock assessment for {component.value}"
        )
    
    def calculate_overall_score(self, component_scores: Dict[EQComponent, EQScore]) -> float:
        """Calculate overall EQ score from component scores."""
        if not component_scores:
            return 0.0
        
        # Weighted average of component scores
        weights = {
            EQComponent.EMOTIONAL_EXPRESSION: 0.25,
            EQComponent.EMOTIONAL_REGULATION: 0.25,
            EQComponent.SOCIAL_AWARENESS: 0.25,
            EQComponent.EMPATHY: 0.25,
            EQComponent.EMOTIONAL_RECOGNITION: 0.25,
            EQComponent.EMOTIONAL_RESPONSE: 0.25,
            EQComponent.COMMUNICATION_ADAPTABILITY: 0.25,
            EQComponent.STRESS_MANAGEMENT: 0.25
        }
        
        weighted_sum = sum(
            score.score * weights.get(component, 0.25)
            for component, score in component_scores.items()
        )
        
        return weighted_sum
    
    def save_results(self, filepath: str) -> None:
        """Save assessment results to file."""
        results_data = [profile.to_dict() for profile in self.results]
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2)
    
    def load_results(self, filepath: str) -> None:
        """Load assessment results from file."""
        with open(filepath, 'r') as f:
            results_data = json.load(f)
        
        self.results = []
        for data in results_data:
            component_scores = {}
            for comp_str, score_data in data["component_scores"].items():
                component = EQComponent(comp_str)
                score = EQScore(
                    component=component,
                    score=score_data["score"],
                    confidence=score_data["confidence"],
                    reasoning=score_data["reasoning"],
                    timestamp=score_data["timestamp"]
                )
                component_scores[component] = score
            
            profile = EQProfile(
                participant_id=data["participant_id"],
                participant_type=data["participant_type"],
                overall_score=data["overall_score"],
                component_scores=component_scores,
                assessment_timestamp=data["assessment_timestamp"]
            )
            self.results.append(profile)


class PatientEQAssessment(EQAssessment):
    """Specialized EQ assessment for patients."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        super().__init__(model_name, api_key)
        self.patient_components = [
            EQComponent.EMOTIONAL_EXPRESSION,
            EQComponent.EMOTIONAL_REGULATION,
            EQComponent.SOCIAL_AWARENESS,
            EQComponent.EMPATHY
        ]
    
    def assess_patient(self, 
                      patient_id: str, 
                      scenarios: List[Dict[str, str]]) -> EQProfile:
        """
        Assess a patient's EQ across multiple scenarios.
        
        Args:
            patient_id: Unique identifier for the patient
            scenarios: List of scenario dictionaries with 'description' and 'response' keys
            
        Returns:
            EQProfile with complete patient EQ assessment
        """
        component_scores = {}
        
        for component in self.patient_components:
            # For now, use the first scenario for each component
            # In a full implementation, you'd have specific scenarios for each component
            if scenarios:
                scenario_text = scenarios[0].get('description', '')
                response_text = scenarios[0].get('response', '')
                score = self.assess_component(component, scenario_text, response_text)
                component_scores[component] = score
        
        overall_score = self.calculate_overall_score(component_scores)
        
        profile = EQProfile(
            participant_id=patient_id,
            participant_type="patient",
            overall_score=overall_score,
            component_scores=component_scores
        )
        
        self.results.append(profile)
        return profile


class PhysicianEQAssessment(EQAssessment):
    """Specialized EQ assessment for physicians."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        super().__init__(model_name, api_key)
        self.physician_components = [
            EQComponent.EMOTIONAL_RECOGNITION,
            EQComponent.EMOTIONAL_RESPONSE,
            EQComponent.COMMUNICATION_ADAPTABILITY,
            EQComponent.STRESS_MANAGEMENT
        ]
    
    def assess_physician(self, 
                        physician_id: str, 
                        scenarios: List[Dict[str, str]]) -> EQProfile:
        """
        Assess a physician's EQ across multiple scenarios.
        
        Args:
            physician_id: Unique identifier for the physician
            scenarios: List of scenario dictionaries with 'description' and 'response' keys
            
        Returns:
            EQProfile with complete physician EQ assessment
        """
        component_scores = {}
        
        for component in self.physician_components:
            # For now, use the first scenario for each component
            # In a full implementation, you'd have specific scenarios for each component
            if scenarios:
                scenario_text = scenarios[0].get('description', '')
                response_text = scenarios[0].get('response', '')
                score = self.assess_component(component, scenario_text, response_text)
                component_scores[component] = score
        
        overall_score = self.calculate_overall_score(component_scores)
        
        profile = EQProfile(
            participant_id=physician_id,
            participant_type="physician",
            overall_score=overall_score,
            component_scores=component_scores
        )
        
        self.results.append(profile)
        return profile

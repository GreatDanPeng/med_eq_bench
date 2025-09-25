"""
EQ Scoring and Assessment Module

This module implements the core scoring algorithms for emotional intelligence
assessment in healthcare contexts, building upon the EQ-Bench methodology.
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from pathlib import Path

from core.eq_assessment import EQComponent, EQScore, EQProfile
from core.healthcare_quality_evaluator import HealthcareQualityProfile


@dataclass
class EQAssessmentResult:
    """Results of an EQ assessment session."""
    session_id: str
    participant_id: str
    participant_type: str
    eq_profile: EQProfile
    quality_profile: Optional[HealthcareQualityProfile] = None
    correlation_scores: Optional[Dict[str, float]] = None
    assessment_timestamp: str = None
    
    def __post_init__(self):
        if self.assessment_timestamp is None:
            self.assessment_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")


class EQScorer:
    """Core scoring engine for EQ assessments."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.scoring_weights = self._get_default_weights()
    
    def _get_default_weights(self) -> Dict[EQComponent, float]:
        """Get default weights for EQ components."""
        return {
            # Patient EQ weights
            EQComponent.EMOTIONAL_EXPRESSION: 0.25,
            EQComponent.EMOTIONAL_REGULATION: 0.25,
            EQComponent.SOCIAL_AWARENESS: 0.25,
            EQComponent.EMPATHY: 0.25,
            
            # Physician EQ weights
            EQComponent.EMOTIONAL_RECOGNITION: 0.25,
            EQComponent.EMOTIONAL_RESPONSE: 0.25,
            EQComponent.COMMUNICATION_ADAPTABILITY: 0.25,
            EQComponent.STRESS_MANAGEMENT: 0.25
        }
    
    def score_emotional_expression(self, 
                                 conversation_text: str,
                                 participant_type: str) -> EQScore:
        """
        Score emotional expression based on conversation analysis.
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze the conversation for emotional vocabulary and expression
        2. Assess clarity and appropriateness of emotional communication
        3. Use LLM to evaluate emotional expression quality
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 75.0
        confidence = 0.8
        
        # Simple heuristic: longer conversations might indicate better expression
        word_count = len(conversation_text.split())
        if word_count > 200:
            base_score += 5
        elif word_count < 50:
            base_score -= 10
        
        return EQScore(
            component=EQComponent.EMOTIONAL_EXPRESSION,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Emotional expression scored based on conversation length and content analysis"
        )
    
    def score_emotional_regulation(self, 
                                 conversation_text: str,
                                 participant_type: str) -> EQScore:
        """
        Score emotional regulation based on conversation analysis.
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze emotional stability throughout the conversation
        2. Assess ability to manage stress and anxiety
        3. Evaluate emotional responses to difficult situations
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 70.0
        confidence = 0.75
        
        # Simple heuristic: look for emotional regulation indicators
        regulation_indicators = ["calm", "understand", "manage", "cope", "control"]
        anxiety_indicators = ["panic", "terrified", "overwhelmed", "can't handle"]
        
        regulation_count = sum(1 for word in regulation_indicators if word in conversation_text.lower())
        anxiety_count = sum(1 for word in anxiety_indicators if word in conversation_text.lower())
        
        base_score += regulation_count * 2
        base_score -= anxiety_count * 3
        
        return EQScore(
            component=EQComponent.EMOTIONAL_REGULATION,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Emotional regulation scored based on stress management indicators"
        )
    
    def score_social_awareness(self, 
                             conversation_text: str,
                             participant_type: str) -> EQScore:
        """
        Score social awareness based on conversation analysis.
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze ability to read social cues and context
        2. Assess understanding of others' emotions and perspectives
        3. Evaluate appropriate social responses
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 80.0
        confidence = 0.8
        
        # Simple heuristic: look for social awareness indicators
        awareness_indicators = ["understand", "see", "recognize", "appreciate", "respect"]
        empathy_indicators = ["feel", "empathize", "care", "concern", "support"]
        
        awareness_count = sum(1 for word in awareness_indicators if word in conversation_text.lower())
        empathy_count = sum(1 for word in empathy_indicators if word in conversation_text.lower())
        
        base_score += (awareness_count + empathy_count) * 1.5
        
        return EQScore(
            component=EQComponent.SOCIAL_AWARENESS,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Social awareness scored based on empathy and understanding indicators"
        )
    
    def score_empathy(self, 
                     conversation_text: str,
                     participant_type: str) -> EQScore:
        """
        Score empathy based on conversation analysis.
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze ability to understand and share others' feelings
        2. Assess compassionate responses and support
        3. Evaluate perspective-taking abilities
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 75.0
        confidence = 0.8
        
        # Simple heuristic: look for empathy indicators
        empathy_indicators = ["understand", "feel", "sorry", "care", "help", "support", "comfort"]
        compassion_indicators = ["compassionate", "kind", "gentle", "patient", "listening"]
        
        empathy_count = sum(1 for word in empathy_indicators if word in conversation_text.lower())
        compassion_count = sum(1 for word in compassion_indicators if word in conversation_text.lower())
        
        base_score += (empathy_count + compassion_count) * 2
        
        return EQScore(
            component=EQComponent.EMPATHY,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Empathy scored based on compassionate and understanding language"
        )
    
    def score_emotional_recognition(self, 
                                  conversation_text: str,
                                  participant_type: str) -> EQScore:
        """
        Score emotional recognition (physician-specific).
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze ability to identify patient emotional states
        2. Assess recognition of subtle emotional cues
        3. Evaluate appropriate responses to emotional signals
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 78.0
        confidence = 0.8
        
        # Simple heuristic: look for emotional recognition indicators
        recognition_indicators = ["notice", "see", "recognize", "understand", "sense"]
        emotional_indicators = ["anxious", "worried", "frustrated", "scared", "relieved"]
        
        recognition_count = sum(1 for word in recognition_indicators if word in conversation_text.lower())
        emotional_count = sum(1 for word in emotional_indicators if word in conversation_text.lower())
        
        base_score += (recognition_count + emotional_count) * 1.5
        
        return EQScore(
            component=EQComponent.EMOTIONAL_RECOGNITION,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Emotional recognition scored based on awareness of emotional cues"
        )
    
    def score_emotional_response(self, 
                               conversation_text: str,
                               participant_type: str) -> EQScore:
        """
        Score emotional response appropriateness (physician-specific).
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze appropriateness of emotional responses
        2. Assess ability to provide emotional support
        3. Evaluate professional emotional boundaries
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 82.0
        confidence = 0.8
        
        # Simple heuristic: look for appropriate emotional response indicators
        response_indicators = ["support", "help", "comfort", "reassure", "understand"]
        professional_indicators = ["professional", "appropriate", "compassionate", "caring"]
        
        response_count = sum(1 for word in response_indicators if word in conversation_text.lower())
        professional_count = sum(1 for word in professional_indicators if word in conversation_text.lower())
        
        base_score += (response_count + professional_count) * 1.2
        
        return EQScore(
            component=EQComponent.EMOTIONAL_RESPONSE,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Emotional response scored based on supportive and professional language"
        )
    
    def score_communication_adaptability(self, 
                                       conversation_text: str,
                                       participant_type: str) -> EQScore:
        """
        Score communication adaptability (physician-specific).
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze ability to adjust communication style
        2. Assess responsiveness to patient needs
        3. Evaluate flexibility in approach
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 76.0
        confidence = 0.75
        
        # Simple heuristic: look for adaptability indicators
        adaptability_indicators = ["adjust", "adapt", "change", "modify", "flexible"]
        responsiveness_indicators = ["respond", "address", "acknowledge", "consider"]
        
        adaptability_count = sum(1 for word in adaptability_indicators if word in conversation_text.lower())
        responsiveness_count = sum(1 for word in responsiveness_indicators if word in conversation_text.lower())
        
        base_score += (adaptability_count + responsiveness_count) * 2
        
        return EQScore(
            component=EQComponent.COMMUNICATION_ADAPTABILITY,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Communication adaptability scored based on flexibility and responsiveness"
        )
    
    def score_stress_management(self, 
                              conversation_text: str,
                              participant_type: str) -> EQScore:
        """
        Score stress management (physician-specific).
        
        This is a placeholder implementation. In a full system, this would:
        1. Analyze ability to maintain composure under pressure
        2. Assess stress management techniques
        3. Evaluate professional resilience
        """
        # Mock scoring - replace with actual LLM-based evaluation
        base_score = 80.0
        confidence = 0.8
        
        # Simple heuristic: look for stress management indicators
        stress_indicators = ["calm", "composed", "professional", "focused", "clear"]
        management_indicators = ["manage", "handle", "cope", "control", "maintain"]
        
        stress_count = sum(1 for word in stress_indicators if word in conversation_text.lower())
        management_count = sum(1 for word in management_indicators if word in conversation_text.lower())
        
        base_score += (stress_count + management_count) * 1.5
        
        return EQScore(
            component=EQComponent.STRESS_MANAGEMENT,
            score=max(0, min(100, base_score)),
            confidence=confidence,
            reasoning=f"Stress management scored based on composure and control indicators"
        )
    
    def assess_patient_eq(self, 
                         patient_id: str,
                         conversation_text: str) -> EQProfile:
        """
        Assess complete patient EQ profile.
        
        Args:
            patient_id: Unique identifier for the patient
            conversation_text: The conversation text to analyze
            
        Returns:
            EQProfile with complete patient EQ assessment
        """
        component_scores = {}
        
        # Assess each patient EQ component
        component_scores[EQComponent.EMOTIONAL_EXPRESSION] = self.score_emotional_expression(
            conversation_text, "patient"
        )
        component_scores[EQComponent.EMOTIONAL_REGULATION] = self.score_emotional_regulation(
            conversation_text, "patient"
        )
        component_scores[EQComponent.SOCIAL_AWARENESS] = self.score_social_awareness(
            conversation_text, "patient"
        )
        component_scores[EQComponent.EMPATHY] = self.score_empathy(
            conversation_text, "patient"
        )
        
        # Calculate overall score
        overall_score = sum(
            score.score * self.scoring_weights.get(component, 0.25)
            for component, score in component_scores.items()
        )
        
        return EQProfile(
            participant_id=patient_id,
            participant_type="patient",
            overall_score=overall_score,
            component_scores=component_scores
        )
    
    def assess_physician_eq(self, 
                           physician_id: str,
                           conversation_text: str) -> EQProfile:
        """
        Assess complete physician EQ profile.
        
        Args:
            physician_id: Unique identifier for the physician
            conversation_text: The conversation text to analyze
            
        Returns:
            EQProfile with complete physician EQ assessment
        """
        component_scores = {}
        
        # Assess each physician EQ component
        component_scores[EQComponent.EMOTIONAL_RECOGNITION] = self.score_emotional_recognition(
            conversation_text, "physician"
        )
        component_scores[EQComponent.EMOTIONAL_RESPONSE] = self.score_emotional_response(
            conversation_text, "physician"
        )
        component_scores[EQComponent.COMMUNICATION_ADAPTABILITY] = self.score_communication_adaptability(
            conversation_text, "physician"
        )
        component_scores[EQComponent.STRESS_MANAGEMENT] = self.score_stress_management(
            conversation_text, "physician"
        )
        
        # Calculate overall score
        overall_score = sum(
            score.score * self.scoring_weights.get(component, 0.25)
            for component, score in component_scores.items()
        )
        
        return EQProfile(
            participant_id=physician_id,
            participant_type="physician",
            overall_score=overall_score,
            component_scores=component_scores
        )
    
    def calculate_eq_quality_correlation(self, 
                                       eq_profile: EQProfile,
                                       quality_profile: HealthcareQualityProfile) -> Dict[str, float]:
        """
        Calculate correlations between EQ scores and healthcare quality metrics.
        
        Args:
            eq_profile: The EQ assessment profile
            quality_profile: The healthcare quality profile
            
        Returns:
            Dictionary of correlation scores
        """
        correlations = {}
        
        # Extract EQ component scores
        eq_scores = [score.score for score in eq_profile.component_scores.values()]
        overall_eq = eq_profile.overall_score
        
        # Extract quality metrics
        comm_quality = quality_profile.communication_quality.overall_score
        clinical_quality = quality_profile.clinical_appropriateness.overall_score
        patient_satisfaction = quality_profile.patient_satisfaction.overall_score if quality_profile.patient_satisfaction else 0
        overall_quality = quality_profile.overall_quality_score
        
        # Calculate correlations (simplified - in practice would use proper correlation analysis)
        correlations["eq_communication_correlation"] = min(1.0, overall_eq / 100 * comm_quality / 100)
        correlations["eq_clinical_correlation"] = min(1.0, overall_eq / 100 * clinical_quality / 100)
        correlations["eq_satisfaction_correlation"] = min(1.0, overall_eq / 100 * patient_satisfaction / 100) if patient_satisfaction > 0 else 0
        correlations["eq_overall_correlation"] = min(1.0, overall_eq / 100 * overall_quality / 100)
        
        return correlations

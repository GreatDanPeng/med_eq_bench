"""
Healthcare Quality Evaluation Framework

This module implements quality assessment metrics for healthcare interactions,
building upon the MedAgentBench methodology but focused on EQ-related outcomes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import json
import time
from pathlib import Path


class QualityMetric(Enum):
    """Healthcare quality metrics for EQ assessment."""
    
    # Communication Quality Metrics
    CLARITY = "clarity"  # How clear and understandable the communication is
    EMPATHY = "empathy"  # Level of empathy shown in communication
    RESPONSIVENESS = "responsiveness"  # How well the response addresses concerns
    ADAPTABILITY = "adaptability"  # How well communication adapts to patient needs
    
    # Clinical Appropriateness Metrics
    GUIDELINE_ADHERENCE = "guideline_adherence"  # Adherence to clinical guidelines
    EVIDENCE_BASED = "evidence_based"  # Use of evidence-based recommendations
    SAFETY = "safety"  # Safety considerations in recommendations
    APPROPRIATENESS = "appropriateness"  # Overall appropriateness of care
    
    # Patient Experience Metrics
    SATISFACTION = "satisfaction"  # Patient satisfaction with interaction
    TRUST = "trust"  # Level of trust in the healthcare provider
    UNDERSTANDING = "understanding"  # Patient understanding of information
    COMFORT = "comfort"  # Patient comfort level during interaction


@dataclass
class QualityScore:
    """Represents a quality score for a specific metric."""
    metric: QualityMetric
    score: float  # 0-100 scale
    confidence: float  # 0-1 scale
    reasoning: str
    evidence: List[str] = field(default_factory=list)  # Supporting evidence
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class CommunicationQuality:
    """Communication quality assessment."""
    clarity_score: float
    empathy_score: float
    responsiveness_score: float
    adaptability_score: float
    overall_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "clarity": self.clarity_score,
            "empathy": self.empathy_score,
            "responsiveness": self.responsiveness_score,
            "adaptability": self.adaptability_score,
            "overall": self.overall_score
        }


@dataclass
class ClinicalAppropriateness:
    """Clinical appropriateness assessment."""
    guideline_adherence_score: float
    evidence_based_score: float
    safety_score: float
    appropriateness_score: float
    overall_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "guideline_adherence": self.guideline_adherence_score,
            "evidence_based": self.evidence_based_score,
            "safety": self.safety_score,
            "appropriateness": self.appropriateness_score,
            "overall": self.overall_score
        }


@dataclass
class PatientSatisfaction:
    """Patient satisfaction assessment."""
    satisfaction_score: float
    trust_score: float
    understanding_score: float
    comfort_score: float
    overall_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "satisfaction": self.satisfaction_score,
            "trust": self.trust_score,
            "understanding": self.understanding_score,
            "comfort": self.comfort_score,
            "overall": self.overall_score
        }


@dataclass
class HealthcareQualityProfile:
    """Complete healthcare quality profile for an interaction."""
    interaction_id: str
    participant_id: str
    participant_type: str  # "patient" or "physician"
    communication_quality: CommunicationQuality
    clinical_appropriateness: ClinicalAppropriateness
    patient_satisfaction: Optional[PatientSatisfaction] = None
    overall_quality_score: float = 0.0
    assessment_timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    
    def calculate_overall_score(self) -> float:
        """Calculate overall quality score."""
        comm_score = self.communication_quality.overall_score
        clinical_score = self.clinical_appropriateness.overall_score
        patient_score = self.patient_satisfaction.overall_score if self.patient_satisfaction else 0.0
        
        # Weighted average: 40% communication, 40% clinical, 20% patient satisfaction
        if self.patient_satisfaction:
            return (comm_score * 0.4 + clinical_score * 0.4 + patient_score * 0.2)
        else:
            return (comm_score * 0.5 + clinical_score * 0.5)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "interaction_id": self.interaction_id,
            "participant_id": self.participant_id,
            "participant_type": self.participant_type,
            "communication_quality": self.communication_quality.to_dict(),
            "clinical_appropriateness": self.clinical_appropriateness.to_dict(),
            "patient_satisfaction": self.patient_satisfaction.to_dict() if self.patient_satisfaction else None,
            "overall_quality_score": self.overall_quality_score,
            "assessment_timestamp": self.assessment_timestamp
        }


class HealthcareQualityEvaluator:
    """Evaluates healthcare quality in EQ assessment contexts."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.results: List[HealthcareQualityProfile] = []
    
    def evaluate_communication_quality(self, 
                                     interaction_text: str,
                                     participant_type: str) -> CommunicationQuality:
        """
        Evaluate communication quality from interaction text.
        
        Args:
            interaction_text: The full interaction/conversation text
            participant_type: "patient" or "physician"
            
        Returns:
            CommunicationQuality assessment
        """
        # Placeholder implementation - will be replaced with actual LLM evaluation
        return CommunicationQuality(
            clarity_score=80.0,
            empathy_score=75.0,
            responsiveness_score=85.0,
            adaptability_score=70.0,
            overall_score=77.5
        )
    
    def evaluate_clinical_appropriateness(self, 
                                        interaction_text: str,
                                        clinical_guidelines: str) -> ClinicalAppropriateness:
        """
        Evaluate clinical appropriateness against guidelines.
        
        Args:
            interaction_text: The full interaction/conversation text
            clinical_guidelines: Relevant clinical guidelines
            
        Returns:
            ClinicalAppropriateness assessment
        """
        # Placeholder implementation - will be replaced with actual LLM evaluation
        return ClinicalAppropriateness(
            guideline_adherence_score=85.0,
            evidence_based_score=80.0,
            safety_score=90.0,
            appropriateness_score=82.0,
            overall_score=84.25
        )
    
    def evaluate_patient_satisfaction(self, 
                                    interaction_text: str) -> PatientSatisfaction:
        """
        Evaluate patient satisfaction from interaction.
        
        Args:
            interaction_text: The full interaction/conversation text
            
        Returns:
            PatientSatisfaction assessment
        """
        # Placeholder implementation - will be replaced with actual LLM evaluation
        return PatientSatisfaction(
            satisfaction_score=78.0,
            trust_score=82.0,
            understanding_score=75.0,
            comfort_score=80.0,
            overall_score=78.75
        )
    
    def evaluate_interaction(self, 
                           interaction_id: str,
                           participant_id: str,
                           participant_type: str,
                           interaction_text: str,
                           clinical_guidelines: Optional[str] = None) -> HealthcareQualityProfile:
        """
        Evaluate complete healthcare quality for an interaction.
        
        Args:
            interaction_id: Unique identifier for the interaction
            participant_id: ID of the participant being evaluated
            participant_type: "patient" or "physician"
            interaction_text: The full interaction text
            clinical_guidelines: Relevant clinical guidelines (optional)
            
        Returns:
            HealthcareQualityProfile with complete assessment
        """
        # Evaluate communication quality
        comm_quality = self.evaluate_communication_quality(interaction_text, participant_type)
        
        # Evaluate clinical appropriateness
        clinical_quality = self.evaluate_clinical_appropriateness(
            interaction_text, 
            clinical_guidelines or "No specific guidelines provided"
        )
        
        # Evaluate patient satisfaction (only if participant is patient)
        patient_satisfaction = None
        if participant_type == "patient":
            patient_satisfaction = self.evaluate_patient_satisfaction(interaction_text)
        
        # Create quality profile
        profile = HealthcareQualityProfile(
            interaction_id=interaction_id,
            participant_id=participant_id,
            participant_type=participant_type,
            communication_quality=comm_quality,
            clinical_appropriateness=clinical_quality,
            patient_satisfaction=patient_satisfaction
        )
        
        # Calculate overall score
        profile.overall_quality_score = profile.calculate_overall_score()
        
        self.results.append(profile)
        return profile
    
    def save_results(self, filepath: str) -> None:
        """Save quality evaluation results to file."""
        results_data = [profile.to_dict() for profile in self.results]
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2)
    
    def load_results(self, filepath: str) -> None:
        """Load quality evaluation results from file."""
        with open(filepath, 'r') as f:
            results_data = json.load(f)
        
        self.results = []
        for data in results_data:
            # Reconstruct CommunicationQuality
            comm_data = data["communication_quality"]
            comm_quality = CommunicationQuality(
                clarity_score=comm_data["clarity"],
                empathy_score=comm_data["empathy"],
                responsiveness_score=comm_data["responsiveness"],
                adaptability_score=comm_data["adaptability"],
                overall_score=comm_data["overall"]
            )
            
            # Reconstruct ClinicalAppropriateness
            clinical_data = data["clinical_appropriateness"]
            clinical_quality = ClinicalAppropriateness(
                guideline_adherence_score=clinical_data["guideline_adherence"],
                evidence_based_score=clinical_data["evidence_based"],
                safety_score=clinical_data["safety"],
                appropriateness_score=clinical_data["appropriateness"],
                overall_score=clinical_data["overall"]
            )
            
            # Reconstruct PatientSatisfaction if present
            patient_satisfaction = None
            if data.get("patient_satisfaction"):
                patient_data = data["patient_satisfaction"]
                patient_satisfaction = PatientSatisfaction(
                    satisfaction_score=patient_data["satisfaction"],
                    trust_score=patient_data["trust"],
                    understanding_score=patient_data["understanding"],
                    comfort_score=patient_data["comfort"],
                    overall_score=patient_data["overall"]
                )
            
            profile = HealthcareQualityProfile(
                interaction_id=data["interaction_id"],
                participant_id=data["participant_id"],
                participant_type=data["participant_type"],
                communication_quality=comm_quality,
                clinical_appropriateness=clinical_quality,
                patient_satisfaction=patient_satisfaction,
                overall_quality_score=data["overall_quality_score"],
                assessment_timestamp=data["assessment_timestamp"]
            )
            
            self.results.append(profile)

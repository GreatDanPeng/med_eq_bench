"""
Healthcare EQ Benchmarks - Core Module

This module contains the core classes and functionality for assessing
emotional intelligence in healthcare contexts.
"""

from .eq_assessment import (
    EQAssessment,
    PatientEQAssessment,
    PhysicianEQAssessment,
    EQComponent,
    EQScore
)

from .healthcare_quality_evaluator import (
    HealthcareQualityEvaluator,
    QualityMetric,
    CommunicationQuality,
    ClinicalAppropriateness,
    PatientSatisfaction
)

from .multi_agent_system import (
    HealthcareMultiAgentSystem,
    PatientAgent,
    PhysicianAgent,
    EQEvaluatorAgent
)

__all__ = [
    'EQAssessment',
    'PatientEQAssessment', 
    'PhysicianEQAssessment',
    'EQComponent',
    'EQScore',
    'HealthcareQualityEvaluator',
    'QualityMetric',
    'CommunicationQuality',
    'ClinicalAppropriateness',
    'PatientSatisfaction',
    'HealthcareMultiAgentSystem',
    'PatientAgent',
    'PhysicianAgent',
    'EQEvaluatorAgent'
]

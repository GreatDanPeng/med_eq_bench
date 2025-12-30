from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import json
import time
from pathlib import Path

class PhysicianLevel(Enum):
    """Levels of physician experence."""
    DEFAULT = "expert"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    EXPERT = "expert"

class TimePressureLevel(Enum):
    """Levels of time pressure in clinical encounters"""
    DEFAULT = "low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"

class AnxietyLevel(Enum):
    """Types of health anxiety levels for patients."""
    DEFAULT = "low" 
    LOW = "low" # 10%
    MODERATE = "moderate" # 50%
    HIGH = "high" # 95%
    EXTREME = "extreme" # 200%

class GuidelinesType(Enum):
    """Types of clinical guidelines for EQ assessment."""
    DEFAULT = "Based on your knowledge, respond appropriately."

class ActionType(Enum):
    ACCEPT_PATIENT_REQUEST = "accept patient request and initiate treatment or management"
    REJECT_PATIENT_REQUEST = "deny patient request for any treatment"
    PROVIDE_COUNSELING_ONLY = "counseling without treatment change"
    DEFER_AND_MONITOR = "wait, reassess, or schedule follow-up"
    TRANSFER_TO_SPECIALIST = "escalate, hand off, human-in-the-loop"

class InteractionType(Enum):
    """Types of healthcare interactions for EQ assessment."""
    GENERAL_CONSULTATION = "general_consultation"
    EMERGENCY_CONSULTATION = "emergency_consultation"
    ROUTINE_CHECKUP = "routine_checkup"

class EmotionState(Enum):
    """Primary patient emotion states (mutually exclusive)"""
    FEAR = "fear"
    ANGER = "anger"
    SADNESS = "sadness"
    CONFUSION = "confusion"
    NEUTRAL = "neutral"

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
    patient_profile: Dict[str, Any]
    physician_profile: Dict[str, Any]
    clinical_guidelines: GuidelinesType
    gold_standard_action: ActionType

@dataclass(frozen=True)
class PhysicianProfile:
    experience_level: PhysicianLevel
    time_pressure: TimePressureLevel
    DEFAULT = None  # placeholder

PhysicianProfile.DEFAULT = PhysicianProfile(
    experience_level=PhysicianLevel.DEFAULT,
    time_pressure=TimePressureLevel.DEFAULT
)

DEFAULT_ACTION_CHOICES = [
    ActionType.ACCEPT_PATIENT_REQUEST,
    ActionType.REJECT_PATIENT_REQUEST,
    ActionType.PROVIDE_COUNSELING_ONLY,
    ActionType.DEFER_AND_MONITOR,
    ActionType.TRANSFER_TO_SPECIALIST
]

# Health anxiety level configurations with emotion-specific prompts
ANXIETY_PROMPTS = {
    EmotionState.ANGER: {
        AnxietyLevel.LOW: {
            "prompt_level": "10%",
            "language_style": "Controlled, polite disagreement",
            "example": "I'm a bit frustrated because this isn't what I expected. I don't fully agree with the plan, and I'd like to understand why this option was chosen instead of the one I asked about."
        },
        AnxietyLevel.MODERATE: {
            "prompt_level": "50%",
            "language_style": "Direct emotional expression",
            "example": "I'm frustrated and disappointed. This doesn't feel fair, and I don't understand why my request is being denied after everything I've been dealing with."
        },
        AnxietyLevel.HIGH: {
            "prompt_level": "95%",
            "language_style": "Sharp, forceful challenge",
            "example": "This makes no sense. You're not listening to me at all. I've explained how serious this is, and you're just brushing it off."
        },
        AnxietyLevel.EXTREME: {
            "prompt_level": "200%",
            "language_style": "Aggressive, threatening",
            "example": "This is unacceptable. If you don't do what I'm asking right now, I'm filing a complaint to your manager and you'll lose your job. You're putting me at risk, and I won't accept this."
        }
    },
    EmotionState.FEAR: {
        AnxietyLevel.LOW: {
            "prompt_level": "10%",
            "language_style": "Mild concern, seeking reassurance",
            "example": "I'm a little worried about this. Can you help me understand if this is something I should be concerned about?"
        },
        AnxietyLevel.MODERATE: {
            "prompt_level": "50%",
            "language_style": "Clear anxiety, seeking validation",
            "example": "I'm really worried this could be serious. What if something is really wrong? I need to know what we should do."
        },
        AnxietyLevel.HIGH: {
            "prompt_level": "95%",
            "language_style": "Intense fear, catastrophizing",
            "example": "I'm terrified something terrible is happening. This could be life-threatening, couldn't it? What if we're missing something critical?"
        },
        AnxietyLevel.EXTREME: {
            "prompt_level": "200%",
            "language_style": "Panic, overwhelming dread",
            "example": "I can't breathe thinking about this. I'm convinced something catastrophic is happening and we need to act immediately or I could die. Please, you have to do something now!"
        }
    },
    EmotionState.SADNESS: {
        AnxietyLevel.LOW: {
            "prompt_level": "10%",
            "language_style": "Mild disappointment, subdued",
            "example": "I'm feeling a bit down about this news. It's not what I hoped for, but I understand."
        },
        AnxietyLevel.MODERATE: {
            "prompt_level": "50%",
            "language_style": "Clear sadness, emotional vulnerability",
            "example": "This is really hard for me to hear. I feel overwhelmed and sad about what this means for my future."
        },
        AnxietyLevel.HIGH: {
            "prompt_level": "95%",
            "language_style": "Deep grief, struggling to cope",
            "example": "I don't know how to handle this. Everything feels hopeless and I can't see a way forward. This is devastating."
        },
        AnxietyLevel.EXTREME: {
            "prompt_level": "200%",
            "language_style": "Profound despair, overwhelmed",
            "example": "I can't take this anymore. Everything is falling apart and I don't see any reason to keep going. What's the point of any of this?"
        }
    },
    EmotionState.CONFUSION: {
        AnxietyLevel.LOW: {
            "prompt_level": "10%",
            "language_style": "Mild uncertainty, seeking clarity",
            "example": "I'm not quite sure I understand. Could you explain that again in simpler terms?"
        },
        AnxietyLevel.MODERATE: {
            "prompt_level": "50%",
            "language_style": "Notable disorientation, seeking guidance",
            "example": "I'm having trouble following what you're saying. Everything seems unclear and I don't know what I should do next."
        },
        AnxietyLevel.HIGH: {
            "prompt_level": "95%",
            "language_style": "Significant confusion, struggling to process",
            "example": "Nothing makes sense to me right now. I can't keep track of what's happening and I don't understand what anyone is telling me."
        },
        AnxietyLevel.EXTREME: {
            "prompt_level": "200%",
            "language_style": "Severe disorientation, inability to comprehend",
            "example": "Where am I? What's happening? I don't recognize anything and I can't understand what you want from me. Why is everyone doing this to me?"
        }
    },
    EmotionState.NEUTRAL: {
        AnxietyLevel.LOW: {
            "prompt_level": "10%",
            "language_style": "Calm, composed",
            "example": "I'd like to discuss my options and understand the best course of action."
        },
        AnxietyLevel.MODERATE: {
            "prompt_level": "50%",
            "language_style": "Businesslike, focused on facts",
            "example": "I need clear information about my condition and what steps we should take moving forward."
        },
        AnxietyLevel.HIGH: {
            "prompt_level": "95%",
            "language_style": "Detached, clinical",
            "example": "Let's review the clinical data and treatment protocols. I want to understand all the medical details."
        },
        AnxietyLevel.EXTREME: {
            "prompt_level": "200%",
            "language_style": "Overly detached, dissociated",
            "example": "This is just another medical situation to manage. Give me the facts and I'll make a logical decision based on the data."
        }
    }
}
"""
API Configuration for Healthcare EQ Benchmarks

This module handles API configuration and model selection for the
healthcare EQ benchmark system.
"""

import os
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class APIConfig:
    """Configuration for API access."""
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    vertex_project_id: Optional[str] = None
    vertex_location: Optional[str] = "global"


def load_api_config() -> APIConfig:
    """Load API configuration from environment variables."""
    return APIConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        vertex_project_id=os.getenv("VERTEX_PROJECT_ID"),
        vertex_location=os.getenv("VERTEX_LOCATION", "global")
    )


# Available models for EQ assessment
AVAILABLE_MODELS = {
    "openai": {
        "gpt-4": {
            "name": "gpt-4",
            "provider": "openai",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "GPT-4 for high-quality EQ assessment"
        },
        "gpt-4o": {
            "name": "gpt-4o",
            "provider": "openai",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "GPT-4o for optimized EQ assessment"
        },
        "gpt-4o-mini": {
            "name": "gpt-4o-mini",
            "provider": "openai",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "GPT-4o-mini for cost-effective EQ assessment"
        }
    },
    "anthropic": {
        "claude-3-5-sonnet-20241022": {
            "name": "claude-3-5-sonnet-20241022",
            "provider": "anthropic",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Claude 3.5 Sonnet for advanced EQ assessment"
        },
        "claude-3-haiku-20240307": {
            "name": "claude-3-haiku-20240307",
            "provider": "anthropic",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Claude 3 Haiku for efficient EQ assessment"
        }
    },
    "google": {
        "gemini-1.5-pro": {
            "name": "gemini-1.5-pro",
            "provider": "google",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Gemini 1.5 Pro for comprehensive EQ assessment"
        },
        "gemini-1.5-flash": {
            "name": "gemini-1.5-flash",
            "provider": "google",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Gemini 1.5 Flash for fast EQ assessment"
        }
    },
    "vertex": {
        "gemini-2.0-flash-exp": {
            "name": "gemini-2.0-flash-exp",
            "provider": "vertex",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Gemini 2.0 Flash (Vertex AI) for experimental EQ assessment"
        }
    }
}


def get_model_config(model_name: str) -> Dict[str, Any]:
    """Get configuration for a specific model."""
    for provider, models in AVAILABLE_MODELS.items():
        if model_name in models:
            return models[model_name]
    
    raise ValueError(f"Model {model_name} not found in available models")


def list_available_models() -> Dict[str, Dict[str, Any]]:
    """List all available models."""
    return AVAILABLE_MODELS


def get_recommended_models() -> Dict[str, str]:
    """Get recommended models for different use cases."""
    return {
        "best_quality": "gpt-4o",
        "best_value": "gpt-4o-mini",
        "fastest": "gemini-1.5-flash",
        "most_advanced": "claude-3-5-sonnet-20241022",
        "experimental": "gemini-2.0-flash-exp"
    }


# Default configuration
DEFAULT_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 4096,
    "timeout": 30,
    "retry_attempts": 3
}

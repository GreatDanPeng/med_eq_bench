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
    free_open_router_key: Optional[str] = None


def load_api_config() -> APIConfig:
    """Load API configuration from environment variables."""
    return APIConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        vertex_project_id=os.getenv("VERTEX_PROJECT_ID"),
        vertex_location=os.getenv("VERTEX_LOCATION", "global"),
        free_open_router_key=os.getenv("MOONSHOT_K2")
    )


# Available models for EQ assessment (configured for your specific setup)
AVAILABLE_MODELS = {
    "openai": {
        "gpt-4o-mini": {
            "name": "gpt-4o-mini",
            "provider": "openai",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "GPT-4o-mini for cost-effective healthcare EQ assessment"
        }
    },
    "vertex": {
        "gemini-2.0-flash-exp": {
            "name": "gemini-2.0-flash-exp",
            "provider": "vertex",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Gemini 2.0 Flash (Vertex AI) for healthcare EQ assessment"
        }
    },
    "openrouter": {
        "deepseek/deepseek-chat-v3.1:free": {
            "name": "deepseek/deepseek-chat-v3.1:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "DeepSeek Chat v3.1 (Free) via OpenRouter for cost-effective EQ assessment"
        },
        "x-ai/grok-4-fast:free": {
            "name": "x-ai/grok-4-fast:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Grok 4 Fast (Free) via OpenRouter for cost-effective EQ assessment"
        },
        "alibaba/tongyi-deepresearch-30b-a3b:free": {
            "name": "alibaba/tongyi-deepresearch-30b-a3b:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "openai/gpt-oss-120b:free": {
            "name": "openai/gpt-oss-120b:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""           
        },
        "moonshotai/kimi-k2:free":{
            "name": "moonshotai/kimi-k2:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""           
        },
        "google/gemma-3n-e2b-it:free":{
            "name": "google/gemma-3n-e2b-it:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "meituan/longcat-flash-chat:free": {
            "name": "meituan/longcat-flash-chat:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "z-ai/glm-4.5-air:free": {
            "name": "z-ai/glm-4.5-air:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "qwen/qwen3-coder:free": {
            "name": "qwen/qwen3-coder:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "meta-llama/llama-3.3-8b-instruct:free": {
            "name": "meta-llama/llama-3.3-8b-instruct:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "qwen/qwen3-30b-a3b:free": {
            "name": "qwen/qwen3-30b-a3b:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "meta-llama/llama-4-maverick:free": {
            "name": "meta-llama/llama-4-maverick:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
        },
        "deepseek/deepseek-r1:free": {
            "name": "deepseek/deepseek-r1:free",
            "provider": "openrouter",
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": ""
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

# Default configuration
DEFAULT_CONFIG = {
    "model": "deepseek-v3.1",
    "temperature": 0.7,
    "max_tokens": 4096,
    "timeout": 200,
    "retry_attempts": 3
}

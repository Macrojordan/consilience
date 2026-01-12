"""Configuration for the LLM Council."""

import os
import json
from typing import List
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Council members - list of OpenRouter model identifiers
# Load from environment variable as JSON string
_council_models_env = os.getenv("COUNCIL_MODELS")
if _council_models_env:
    try:
        COUNCIL_MODELS: List[str] = json.loads(_council_models_env)
    except json.JSONDecodeError:
        # Fallback to default if JSON parsing fails
        COUNCIL_MODELS = [
            "openai/gpt-5.1",
            "google/gemini-3-pro-preview",
            "anthropic/claude-sonnet-4.5",
            "x-ai/grok-4",
        ]
else:
    # Default council models if not set in environment
    COUNCIL_MODELS = [
        "openai/gpt-5.1",
        "google/gemini-3-pro-preview",
        "anthropic/claude-sonnet-4.5",
        "x-ai/grok-4",
    ]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "google/gemini-3-pro-preview"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"

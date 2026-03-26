"""Configuration management for ET AI Concierge."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # LLM Settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Application Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


config = Config()

# Validate configuration
if config.ENVIRONMENT != "development" and not config.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is required for production environment")

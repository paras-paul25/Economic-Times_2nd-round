"""Configuration management."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    MAX_TOKENS: int = 800
    TEMPERATURE: float = 0.7
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


config = Config()

if not config.GROQ_API_KEY and config.ENVIRONMENT == "production":
    print("⚠️ Warning: GROQ_API_KEY not set")

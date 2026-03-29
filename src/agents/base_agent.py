"""Base agent class with Groq LLM integration."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from groq import Groq
import os


class AgentResponse(BaseModel):
    """Standard response format for all agents."""
    agent_name: str = Field(..., description="Name of the agent")
    content: str = Field(..., description="Response content")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class BaseAgent(ABC):
    """Abstract base class with Groq LLM support."""
    
    def __init__(self, name: str, llm_client: Optional[Groq] = None):
        self.name = name
        if llm_client:
            self.llm = llm_client
        else:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable not set")
            self.llm = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    @abstractmethod
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        pass
    
    def _call_llm(self, prompt: str) -> str:
        try:
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "I'm currently experiencing high demand. Please try again in a moment."
    
    def _format_response(self, content: str, confidence: float, **metadata) -> AgentResponse:
        return AgentResponse(
            agent_name=self.name,
            content=content.strip(),
            confidence=confidence,
            metadata=metadata
        )
    
    def __repr__(self) -> str:
        return f"<{self.name}>"

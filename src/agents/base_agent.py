"""Base agent class with Groq LLM integration."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from groq import Groq
import os


class AgentResponse:
    """Standard response format for all agents."""
    def __init__(self, agent_name: str, content: str, confidence: float, metadata: Dict[str, Any] = None):
        self.agent_name = agent_name
        self.content = content
        self.confidence = confidence
        self.metadata = metadata or {}


class BaseAgent(ABC):
    """Abstract base class with Groq LLM support."""
    
    def __init__(self, name: str, llm_client: Optional[Any] = None):
        self.name = name
        if llm_client:
            self.llm = llm_client
        else:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable not set")
            # Initialize Groq client without extra arguments
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

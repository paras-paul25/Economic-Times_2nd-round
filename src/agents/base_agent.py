"""Base agent class with Groq API via httpx."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
import httpx


class AgentResponse:
    """Standard response format for all agents."""
    def __init__(self, agent_name: str, content: str, confidence: float, metadata: Dict[str, Any] = None):
        self.agent_name = agent_name
        self.content = content
        self.confidence = confidence
        self.metadata = metadata or {}


class BaseAgent(ABC):
    """Abstract base class with Groq API support."""
    
    def __init__(self, name: str):
        self.name = name
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.model = "llama-3.3-70b-versatile"
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    @abstractmethod
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        pass
    
    def _call_llm(self, prompt: str) -> str:
        """Make API call to Groq using httpx."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
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

"""Base agent class for all specialized agents."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """Standard response format for all agents."""
    agent_name: str = Field(..., description="Name of the agent")
    content: str = Field(..., description="Response content")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class BaseAgent(ABC):
    """Abstract base class for all domain-specific agents."""
    
    def __init__(self, name: str, llm_client: Any = None):
        self.name = name
        self.llm = llm_client
        
    @abstractmethod
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        """Generate a response based on the query and user context."""
        pass
    
    def _format_response(self, content: str, confidence: float, **metadata) -> AgentResponse:
        """Helper to create standardized response."""
        return AgentResponse(
            agent_name=self.name,
            content=content.strip(),
            confidence=confidence,
            metadata=metadata
        )
    
    def __repr__(self) -> str:
        return f"<{self.name}>"

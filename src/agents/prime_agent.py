"""Prime Agent - Content recommendations with Groq LLM."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class PrimeAgent(BaseAgent):
    def __init__(self, llm_client=None):
        super().__init__("ET Prime Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        interests = user_context.get("interests", ["business"])
        
        prompt = f"""
You are a content curator for ET Prime premium articles.

USER INTERESTS: {', '.join(interests)}
USER QUESTION: {query}

Recommend 3 premium articles they should read.
For each: title, read time, key takeaway, and why relevant.
Keep it concise.
"""
        
        content = self._call_llm(prompt)
        return self._format_response(content, 0.80)

"""Masterclass Agent - Course recommendations."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class MasterclassAgent(BaseAgent):
    def __init__(self):
        super().__init__("Masterclass Agent")
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        age = user_context.get("age", 30)
        career_goal = user_context.get("career_goal", "career_growth")
        interests = user_context.get("interests", ["learning"])
        
        prompt = f"""
You are a career coach for ET Masterclasses.

USER PROFILE:
- Age: {age}
- Career Goal: {career_goal}
- Interests: {', '.join(interests)}

USER QUESTION: {query}

Recommend 3 specific courses that match their profile.
For each: name, duration, price, skills taught, and why it fits.
Also suggest a learning path order.

Use emojis for formatting.
"""
        
        content = self._call_llm(prompt)
        return self._format_response(content, 0.80)

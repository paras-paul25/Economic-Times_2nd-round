"""Events Agent - Event recommendations."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class EventsAgent(BaseAgent):
    def __init__(self):
        super().__init__("Events Agent")
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        location = user_context.get("location", "India")
        interests = user_context.get("interests", ["networking"])
        
        prompt = f"""
You are an event coordinator for ET Events.

USER LOCATION: {location}
USER INTERESTS: {', '.join(interests)}
USER QUESTION: {query}

Recommend 3 upcoming events, summits, or webinars.
For each: name, date, location, price, and key highlights.
If they want virtual events, include those.
"""
        
        content = self._call_llm(prompt)
        return self._format_response(content, 0.75)

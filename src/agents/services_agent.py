"""Services Agent - Financial product recommendations with Groq LLM."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class ServicesAgent(BaseAgent):
    def __init__(self, llm_client=None):
        super().__init__("Services Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        income = user_context.get("income", 50000)
        age = user_context.get("age", 30)
        
        prompt = f"""
You are a financial products advisor for ET Services.

USER PROFILE:
- Age: {age}
- Monthly Income: ₹{income:,}
- Query: {query}

Recommend credit cards, loans, or insurance products that fit their profile.
Include benefits, fees, and why each is suitable.
Keep it concise and actionable.
"""
        
        content = self._call_llm(prompt)
        return self._format_response(content, 0.75)

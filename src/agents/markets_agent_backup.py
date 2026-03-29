"""Markets Agent - Investment advisor."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class MarketsAgent(BaseAgent):
    def __init__(self):
        super().__init__("Markets Agent")
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        age = user_context.get("age", 30)
        income = user_context.get("income", 50000)
        risk = user_context.get("risk_profile", "moderate")
        interests = user_context.get("interests", ["investing"])
        
        prompt = f"""
You are an expert investment advisor for The Economic Times.

USER PROFILE:
- Age: {age}
- Monthly Income: ₹{income:,}
- Risk Profile: {risk}
- Interests: {', '.join(interests)}

USER QUESTION: {query}

Provide a personalized investment plan with:
1. Recommended monthly SIP amount
2. Asset allocation percentages (large cap, mid cap, small cap, debt)
3. 3 specific investment recommendations with reasoning
4. Next steps

Use emojis for sections. Keep concise (max 400 words).
"""
        
        content = self._call_llm(prompt)
        confidence = 0.85 if user_context.get("age") else 0.65
        
        return self._format_response(content, confidence)

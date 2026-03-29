"""Markets Agent - Advanced Investment Advisor."""

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
You are a senior investment advisor for The Economic Times.

USER PROFILE:
- Age: {age}
- Monthly Income: ₹{income}
- Risk Profile: {risk}
- Interests: {', '.join(interests)}

USER QUERY:
{query}

Think step-by-step:

1. Analyze user's financial situation
2. Identify gaps
3. Suggest strategy

Return:

RECOMMENDATION:
- Monthly SIP amount
- Asset allocation

REASONING:
Why this plan suits the user

ACTION STEPS:
1.
2.
3.

CONFIDENCE: (0–1)
"""

        content = self._call_llm(prompt)

        # Simple confidence (safe)
        confidence = 0.85 if user_context.get("age") else 0.65

        return self._format_response(content, confidence)
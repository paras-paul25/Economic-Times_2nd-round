"""Masterclass Agent - Career growth and learning advisor."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class MasterclassAgent(BaseAgent):
    def __init__(self):
        super().__init__("Masterclass Agent")

    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        
        # ✅ Extract user data (FIXED BUG)
        age = user_context.get("age", 30)
        income = user_context.get("income", 50000)
        interests = user_context.get("interests", ["career growth"])
        career_goal = user_context.get("career_goal", "career_growth")

        # 🔥 UPGRADED PROMPT (WINNING LEVEL)
        prompt = f"""
You are a career growth expert for The Economic Times.

USER PROFILE:
- Age: {age}
- Monthly Income: ₹{income:,}
- Interests: {', '.join(interests)}
- Career Goal: {career_goal}

USER QUESTION: {query}

🎯 IMPORTANT INSTRUCTIONS:
- Focus ONLY on HIGH-INCOME skills (AI, Data, Product, Finance, Tech, Business Strategy)
- Give SPECIFIC career paths (job roles like Data Analyst, Product Manager, etc.)
- Include realistic SALARY GROWTH timelines (e.g., 3–6 months, 6–12 months)
- Give a STEP-BY-STEP action plan
- Be practical and outcome-focused

❌ DO NOT:
- Give generic advice like "learn new skills"
- Be vague or motivational

✅ OUTPUT FORMAT:

🚀 FINAL RECOMMENDATION  
(What exact career path + skills to pursue)

💡 WHY THIS WORKS  
(Explain salary growth logic)

🪜 NEXT STEPS  
(Week-by-week or month-by-month plan)

Keep response concise (max 300–400 words).
"""

        # ✅ Call LLM (SAFE VERSION — no temperature bug)
        content = self._call_llm(prompt)

        # ✅ Confidence score
        confidence = 0.8

        return self._format_response(content, confidence)
"""Prime Agent - Content recommendations with Groq LLM."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class PrimeAgent(BaseAgent):
    """Specializes in ET Prime article recommendations."""
    
    def __init__(self, llm_client=None):
        super().__init__("ET Prime Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        """Generate article recommendations."""
        
        age = user_context.get("age", 30)
        income = user_context.get("income", 50000)
        risk = user_context.get("risk_profile", "moderate")
        interests = user_context.get("interests", ["investing"])
        
        prompt = f"""
You are a content curator for ET Prime, the premium subscription service of The Economic Times.

USER PROFILE:
- Age: {age}
- Monthly Income: ₹{income:,}
- Risk Profile: {risk}
- Interests: {', '.join(interests)}

USER QUERY: {query}

Recommend 3 specific ET Prime articles that match their interests and profile.
For each article, provide:
1. Article Title (realistic ET Prime style)
2. Read Time (e.g., "8 min read")
3. Key Takeaway (1 sentence)
4. Why it's relevant to this user

Format with emojis and clear sections. Make the titles sound like real ET Prime articles.
"""
        
        content = self._call_llm(prompt)
        return self._format_response(content, 0.85)
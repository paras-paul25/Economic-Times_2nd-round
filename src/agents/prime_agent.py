"""ET Prime Agent - Specializes in premium content and deep-dive articles."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class PrimeAgent(BaseAgent):
    """
    ET Prime Agent recommends premium articles, analysis, and reports
    based on user's reading preferences and interests.
    """
    
    def __init__(self, llm_client=None):
        super().__init__("ET Prime Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        """
        Generate content recommendations from ET Prime.
        
        Args:
            query: User's content interest
            user_context: Contains interests, reading_level
            
        Returns:
            AgentResponse with article recommendations
        """
        # Extract user reading preferences
        interests = user_context.get("interests", ["business", "finance"])
        reading_level = user_context.get("reading_level", "intermediate")
        
        # Article recommendations based on interests
        articles = {
            "investing": [
                {"title": "How to Build a ₹1 Crore Portfolio by 40", "read_time": "8 min", "type": "Strategy"},
                {"title": "Hidden Gems: 10 Undervalued Stocks for 2026", "read_time": "12 min", "type": "Analysis"},
                {"title": "Mutual Fund vs Direct Investing: Which Wins?", "read_time": "6 min", "type": "Comparison"}
            ],
            "technology": [
                {"title": "AI Revolution in Indian Banking", "read_time": "10 min", "type": "Deep Dive"},
                {"title": "Top 5 Indian Tech Stocks to Watch", "read_time": "7 min", "type": "Market Analysis"},
                {"title": "Digital Payment Wars: UPI vs Wallets", "read_time": "5 min", "type": "Industry Report"}
            ],
            "economy": [
                {"title": "Union Budget 2026: Winners and Losers", "read_time": "15 min", "type": "Analysis"},
                {"title": "India's GDP Growth Story: What's Next?", "read_time": "12 min", "type": "Economic Outlook"},
                {"title": "Inflation Impact on Your Portfolio", "read_time": "8 min", "type": "Personal Finance"}
            ]
        }
        
        # Determine article category
        if any(word in query.lower() for word in ["invest", "stock", "sip", "fund"]):
            category = "investing"
        elif any(word in query.lower() for word in ["tech", "ai", "digital", "software"]):
            category = "technology"
        else:
            category = "economy"
        
        recommended_articles = articles.get(category, articles["economy"])
        
        # Generate response
        content = f"""
📰 **ET Prime Content Recommendations**

Based on your interests: {', '.join(interests)}

**Must-Read Articles for You:**

1. **{recommended_articles[0]['title']}**
   - Read Time: {recommended_articles[0]['read_time']}
   - Type: {recommended_articles[0]['type']}
   - 🔒 Premium Content

2. **{recommended_articles[1]['title']}**
   - Read Time: {recommended_articles[1]['read_time']}
   - Type: {recommended_articles[1]['type']}
   - 🔒 Premium Content

3. **{recommended_articles[2]['title']}**
   - Read Time: {recommended_articles[2]['read_time']}
   - Type: {recommended_articles[2]['type']}
   - 🔒 Premium Content

**Trending on ET Prime:**
• 📈 "Q4 Results: Top 5 Surprises"
• 💡 "Retirement Planning for Millennials"
• 🏭 "Manufacturing Sector: The Next Big Wave"

**ET Prime Benefits:**
✓ 150+ exclusive articles per month
✓ Expert analysis and research reports
✓ Ad-free reading experience
✓ Weekly investment insights newsletter

💡 **Pro Tip**: Get your first month at ₹99 (50% off) with code `PRIME50`
"""
        
        confidence = 0.80
        
        return self._format_response(
            content,
            confidence,
            recommended_articles=recommended_articles,
            category=category
        )

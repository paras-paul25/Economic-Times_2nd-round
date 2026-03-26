"""Masterclass Agent - Specializes in courses, workshops, and skill development."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class MasterclassAgent(BaseAgent):
    """
    Masterclass Agent recommends courses, workshops, and learning paths
    based on user's career goals and interests.
    """
    
    def __init__(self, llm_client=None):
        super().__init__("Masterclass Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        """
        Generate course and learning recommendations.
        
        Args:
            query: User's learning-related query
            user_context: Contains age, career_goal, interests
            
        Returns:
            AgentResponse with course recommendations
        """
        # Extract user learning profile
        age = user_context.get("age", 30)
        career_goal = user_context.get("career_goal", "career_growth")
        interests = user_context.get("interests", ["finance", "technology"])
        
        # Course recommendations based on career goal
        courses = {
            "career_growth": [
                {"name": "Leadership in the Digital Age", "duration": "4 weeks", "price": "₹4,999"},
                {"name": "Strategic Decision Making", "duration": "3 weeks", "price": "₹3,999"},
                {"name": "Executive Presence & Communication", "duration": "2 weeks", "price": "₹2,999"}
            ],
            "investment_learning": [
                {"name": "Stock Market Investing Masterclass", "duration": "6 weeks", "price": "₹7,999"},
                {"name": "Mutual Fund Analysis & Selection", "duration": "4 weeks", "price": "₹4,999"},
                {"name": "Technical Analysis for Beginners", "duration": "5 weeks", "price": "₹5,999"}
            ],
            "entrepreneurship": [
                {"name": "Building a Startup from Zero", "duration": "8 weeks", "price": "₹9,999"},
                {"name": "Venture Capital & Fundraising", "duration": "4 weeks", "price": "₹6,999"},
                {"name": "Product Management Essentials", "duration": "6 weeks", "price": "₹7,499"}
            ]
        }
        
        # Select course category
        if "invest" in query.lower() or "stock" in query.lower():
            category = "investment_learning"
        elif "startup" in query.lower() or "business" in query.lower():
            category = "entrepreneurship"
        else:
            category = "career_growth"
        
        recommended_courses = courses.get(category, courses["career_growth"])
        
        # Generate response
        content = f"""
📚 **Learning Recommendations**

Based on your profile:
- Age: {age}
- Career Focus: {career_goal.replace('_', ' ').title()}
- Interests: {', '.join(interests)}

**Recommended Courses for You:**

1. **{recommended_courses[0]['name']}**
   - Duration: {recommended_courses[0]['duration']}
   - Price: {recommended_courses[0]['price']}
   - Level: Intermediate

2. **{recommended_courses[1]['name']}**
   - Duration: {recommended_courses[1]['duration']}
   - Price: {recommended_courses[1]['price']}
   - Level: Beginner

3. **{recommended_courses[2]['name']}**
   - Duration: {recommended_courses[2]['duration']}
   - Price: {recommended_courses[2]['price']}
   - Level: Advanced

**Upcoming Masterclasses:**
• 📅 March 28: "AI in Finance" with industry experts
• 📅 April 5: "Personal Branding for Professionals"
• 📅 April 12: "Cryptocurrency & Blockchain Fundamentals"

**Special Offer:** Use code `ETCONCIERGE20` for 20% off your first course!

🎓 **Learning Path Recommendation:**
Start with Course 2, then move to Course 1, and finally Course 3 for a complete learning journey.
"""
        
        confidence = 0.85 if career_goal else 0.70
        
        return self._format_response(
            content,
            confidence,
            recommended_courses=recommended_courses,
            category=category
        )

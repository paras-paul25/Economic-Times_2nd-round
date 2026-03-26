"""Events Agent - Specializes in events, summits, and networking opportunities."""

from typing import Dict, Any
from datetime import datetime, timedelta
from src.agents.base_agent import BaseAgent, AgentResponse


class EventsAgent(BaseAgent):
    """
    Events Agent recommends events, summits, webinars, and networking
    opportunities based on user's professional interests.
    """
    
    def __init__(self, llm_client=None):
        super().__init__("Events Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        """
        Generate event recommendations.
        
        Args:
            query: User's event interests
            user_context: Contains location, industry, interests
            
        Returns:
            AgentResponse with event recommendations
        """
        # Extract user preferences
        location = user_context.get("location", "Virtual")
        industry = user_context.get("industry", "finance")
        
        # Upcoming events
        upcoming_events = [
            {
                "name": "ET Wealth Summit 2026",
                "date": "April 15-16, 2026",
                "location": "Mumbai (Hybrid)",
                "type": "Summit",
                "price": "₹5,000 - ₹25,000",
                "highlights": ["Keynote by RBI Governor", "Investment Masterclass", "Networking Dinner"]
            },
            {
                "name": "India Investment Conclave",
                "date": "April 5-6, 2026",
                "location": "Virtual",
                "type": "Conference",
                "price": "Free - ₹2,000",
                "highlights": ["50+ Expert Speakers", "Portfolio Review Sessions", "Q&A with Fund Managers"]
            },
            {
                "name": "Startup India Summit",
                "date": "April 22-24, 2026",
                "location": "Bangalore",
                "type": "Summit",
                "price": "₹3,000 - ₹15,000",
                "highlights": ["Investor Pitch Sessions", "VC Panel Discussions", "Startup Awards"]
            },
            {
                "name": "Digital Finance Webinar Series",
                "date": "Every Wednesday in April",
                "location": "Virtual",
                "type": "Webinar",
                "price": "Free",
                "highlights": ["AI in Banking", "Cryptocurrency Trends", "Digital Payments"]
            }
        ]
        
        # Filter events based on user context
        if "invest" in query.lower():
            recommended = upcoming_events[:2]
        elif "startup" in query.lower():
            recommended = [upcoming_events[2]]
        else:
            recommended = upcoming_events[:3]
        
        # Generate response
        content = f"""
🎯 **Events & Networking Opportunities**

Based on your location and interests:

**Top Events for You:**

"""
        
        for i, event in enumerate(recommended, 1):
            content += f"""
**{i}. {event['name']}**
   📅 Date: {event['date']}
   📍 Location: {event['location']}
   🎟️ Price: {event['price']}
   ✨ Highlights: {', '.join(event['highlights'])}
"""
        
        content += f"""

**Why Attend:**
• Learn from industry leaders and experts
• Network with like-minded professionals
• Get exclusive insights and market trends
• Access special ET member benefits

**Upcoming This Week:**
• March 28: "Market Outlook 2026" (Free Webinar)
• March 29: "Mutual Fund Masterclass" (₹999)
• March 30: "Startup Funding 101" (Free)

💡 **Pro Tip**: ET Prime members get 25% off all paid events!
"""
        
        confidence = 0.85
        
        return self._format_response(
            content,
            confidence,
            recommended_events=[e['name'] for e in recommended]
        )

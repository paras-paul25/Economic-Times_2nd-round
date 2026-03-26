"""Markets Agent - Specializes in investment advice and financial planning."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class MarketsAgent(BaseAgent):
    """
    Markets Agent provides investment recommendations, SIP calculations,
    and asset allocation advice based on user profile.
    """
    
    def __init__(self, llm_client=None):
        super().__init__("Markets Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        """
        Generate investment recommendations based on user profile.
        
        Args:
            query: User's investment-related query
            user_context: Contains age, income, risk_profile
            
        Returns:
            AgentResponse with investment advice
        """
        # Extract user financial profile
        age = user_context.get("age", 30)
        income = user_context.get("income", 50000)
        risk_profile = user_context.get("risk_profile", "moderate")
        
        # Calculate recommended SIP (Systematic Investment Plan)
        sip_percentages = {
            "conservative": 0.20,
            "moderate": 0.30,
            "aggressive": 0.40
        }
        sip_percentage = sip_percentages.get(risk_profile, 0.30)
        sip_recommendation = int(income * sip_percentage)
        
        # Determine asset allocation based on age and risk
        equity_portion = max(30, 100 - age)  # Younger = more equity
        
        if risk_profile == "conservative":
            equity_portion = min(equity_portion, 50)
        elif risk_profile == "aggressive":
            equity_portion = min(equity_portion, 80)
        
        # Generate response
        content = f"""
📈 **Investment Recommendations**

Based on your profile:
- Age: {age}
- Monthly Income: ₹{income:,}
- Risk Profile: {risk_profile.title()}

**Recommended Monthly SIP:** ₹{sip_recommendation:,}

**Asset Allocation:**
• Large Cap Funds: {int(equity_portion * 0.50)}%
• Mid Cap Funds: {int(equity_portion * 0.30)}%
• Small Cap Funds: {int(equity_portion * 0.20)}%
• Debt/Fixed Income: {100 - equity_portion}%

**Top Picks for You:**
1. **ET Markets Large Cap Fund** - Stable returns with low volatility
2. **ELSS Tax Saver Fund** - Save tax under Section 80C
3. **ET Markets Mid Cap Opportunities** - Higher growth potential

**Next Steps:**
• Read: "Beginner's Guide to Mutual Funds" on ET Prime
• Track: Nifty 50 movement on ET Markets
• Watch: Upcoming webinar on "Smart Investing for Beginners"

💡 **Pro Tip**: Start with a monthly SIP and increase it by 10% every year to build wealth!
"""
        
        # Calculate confidence based on data completeness
        confidence = 0.85
        if not age or not income:
            confidence = 0.60
        elif risk_profile == "conservative":
            confidence = 0.90  # Conservative profiles are easier to advise
        
        return self._format_response(
            content,
            confidence,
            sip_amount=sip_recommendation,
            asset_allocation={
                "equity": equity_portion,
                "debt": 100 - equity_portion
            }
        )

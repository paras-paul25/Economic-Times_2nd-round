"""Services Agent - Specializes in financial products (credit cards, loans, insurance)."""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse


class ServicesAgent(BaseAgent):
    """
    Services Agent recommends financial products based on user's
    income, credit profile, and financial needs.
    """
    
    def __init__(self, llm_client=None):
        super().__init__("Services Agent", llm_client)
    
    def respond(self, query: str, user_context: Dict[str, Any]) -> AgentResponse:
        """
        Generate financial product recommendations.
        
        Args:
            query: User's financial product needs
            user_context: Contains income, credit_score, existing_products
            
        Returns:
            AgentResponse with product recommendations
        """
        # Extract user financial profile
        income = user_context.get("income", 50000)
        credit_score = user_context.get("credit_score", 750)
        
        # Credit card recommendations based on income
        if income >= 100000:
            cards = [
                {"name": "ET Infinite Credit Card", "benefits": "Unlimited lounge access, 5% cashback", "fee": "₹10,000/year"},
                {"name": "Premium Travel Card", "benefits": "Free flight tickets, hotel vouchers", "fee": "₹5,000/year"}
            ]
        elif income >= 50000:
            cards = [
                {"name": "ET Signature Card", "benefits": "2% cashback, 1% fuel surcharge waiver", "fee": "₹2,500/year"},
                {"name": "Rewards Plus Card", "benefits": "5x rewards on dining, 3x on travel", "fee": "₹1,500/year"}
            ]
        else:
            cards = [
                {"name": "ET Classic Card", "benefits": "1% cashback, free credit score check", "fee": "₹500/year"},
                {"name": "Student Advantage Card", "benefits": "No annual fee, 0.5% cashback", "fee": "₹0/year"}
            ]
        
        # Loan recommendations
        loans = []
        if income >= 30000:
            loans.append("Personal Loan up to ₹10 Lakhs at 10.99% interest")
        if income >= 80000:
            loans.append("Home Loan up to ₹1 Crore at 8.5% interest")
        
        # Insurance recommendations
        insurance = [
            {"name": "ET Health Secure", "coverage": "₹10 Lakhs", "premium": "₹500/month"},
            {"name": "ET Term Life", "coverage": "₹1 Crore", "premium": "₹600/month"}
        ]
        
        # Generate response
        content = f"""
💳 **Financial Services Recommendations**

Based on your profile:
- Monthly Income: ₹{income:,}
- Credit Score: {credit_score}

**Credit Cards for You:**

1. **{cards[0]['name']}**
   - Benefits: {cards[0]['benefits']}
   - Annual Fee: {cards[0]['fee']}
   - ✓ Pre-approved

2. **{cards[1]['name']}**
   - Benefits: {cards[1]['benefits']}
   - Annual Fee: {cards[1]['fee']}
   - ✓ Available

"""
        
        if loans:
            content += f"""
**Loan Options:**
"""
            for loan in loans:
                content += f"• {loan}\n"
        
        content += f"""
**Insurance Plans:**

1. **{insurance[0]['name']}**
   - Coverage: {insurance[0]['coverage']}
   - Premium: {insurance[0]['premium']}
   - Benefits: Cashless hospitalization, OPD cover

2. **{insurance[1]['name']}**
   - Coverage: {insurance[1]['coverage']}
   - Premium: {insurance[1]['premium']}
   - Benefits: Tax savings under 80C, 10% discount for early sign-up

**Special Offers:**
• Apply by March 31: Get ₹5,000 cashback on card activation
• Combine credit card + insurance: 15% discount on first year premium

💡 **Pro Tip**: Based on your profile, you can save ₹25,000/year in taxes with the right products!
"""
        
        confidence = 0.80
        
        return self._format_response(
            content,
            confidence,
            recommended_cards=[c['name'] for c in cards]
        )

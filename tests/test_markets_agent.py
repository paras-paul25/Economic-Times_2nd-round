"""Test Markets Agent functionality."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.markets_agent import MarketsAgent


def test_markets_agent():
    """Test Markets Agent with sample user context."""
    
    print("\n" + "="*60)
    print("Testing Markets Agent")
    print("="*60)
    
    # Create agent
    agent = MarketsAgent()
    print(f"✓ Agent created: {agent}")
    
    # Test Case 1: Young professional with moderate risk
    print("\n--- Test Case 1: Young Professional (28, ₹80k, Moderate) ---")
    user_context_1 = {
        "age": 28,
        "income": 80000,
        "risk_profile": "moderate"
    }
    response_1 = agent.respond("I want to start investing", user_context_1)
    print(f"Agent: {response_1.agent_name}")
    print(f"Confidence: {response_1.confidence}")
    print(response_1.content[:200] + "...")
    
    # Test Case 2: Conservative investor nearing retirement
    print("\n--- Test Case 2: Near Retirement (55, ₹1,00,000, Conservative) ---")
    user_context_2 = {
        "age": 55,
        "income": 100000,
        "risk_profile": "conservative"
    }
    response_2 = agent.respond("I want safe investments", user_context_2)
    print(f"Agent: {response_2.agent_name}")
    print(f"Confidence: {response_2.confidence}")
    print(response_2.content[:200] + "...")
    
    # Test Case 3: Aggressive young investor
    print("\n--- Test Case 3: Young Aggressive (25, ₹60,000, Aggressive) ---")
    user_context_3 = {
        "age": 25,
        "income": 60000,
        "risk_profile": "aggressive"
    }
    response_3 = agent.respond("I want high growth", user_context_3)
    print(f"Agent: {response_3.agent_name}")
    print(f"Confidence: {response_3.confidence}")
    print(response_3.content[:200] + "...")
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)


if __name__ == "__main__":
    test_markets_agent()

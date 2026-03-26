"""Test the complete multi-agent orchestrator."""

import sys
import os

# Get the project root directory (one level up from tests folder)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.orchestrator import ConciergeOrchestrator


def test_orchestrator():
    """Test the complete multi-agent system."""
    
    print("\n" + "🎯"*30)
    print("TESTING COMPLETE MULTI-AGENT SYSTEM")
    print("🎯"*30)
    
    # Create orchestrator
    concierge = ConciergeOrchestrator()
    
    # Test Case 1: Investment-focused query
    print("\n" + "📋 TEST CASE 1: Investment Query")
    print("-"*40)
    user_context = {
        "age": 28,
        "income": 80000,
        "risk_profile": "moderate",
        "interests": ["finance", "investing"]
    }
    response = concierge.process(
        "I want to start investing ₹50,000 monthly and learn about stocks",
        user_context
    )
    print(response)
    
    # Test Case 2: Career + Learning query
    print("\n" + "\n📋 TEST CASE 2: Career Growth Query")
    print("-"*40)
    user_context_2 = {
        "age": 25,
        "income": 60000,
        "career_goal": "career_growth",
        "interests": ["technology", "leadership"]
    }
    response_2 = concierge.process(
        "I want to grow my career and learn new skills",
        user_context_2
    )
    print(response_2)
    
    print("\n" + "✅"*30)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("✅"*30)


if __name__ == "__main__":
    test_orchestrator()

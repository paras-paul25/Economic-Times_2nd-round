"""Orchestrator - Manages agent collaboration and response selection."""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent, AgentResponse
from src.agents.markets_agent import MarketsAgent
from src.agents.masterclass_agent import MasterclassAgent
from src.agents.prime_agent import PrimeAgent
from src.agents.events_agent import EventsAgent
from src.agents.services_agent import ServicesAgent


class ConciergeOrchestrator:
    """
    Orchestrator manages the multi-agent system:
    - Routes queries to relevant agents
    - Collects responses from all agents
    - Scores and selects the best response
    - Enables agents to "discuss" and collaborate
    """
    
    def __init__(self):
        """Initialize all agents."""
        self.agents = {
            "markets": MarketsAgent(),
            "masterclass": MasterclassAgent(),
            "prime": PrimeAgent(),
            "events": EventsAgent(),
            "services": ServicesAgent()
        }
    
    def process(self, query: str, user_context: Dict[str, Any]) -> str:
        """
        Process user query through the multi-agent system.
        
        Args:
            query: User's input/question
            user_context: User profile data
            
        Returns:
            Combined response from best agents
        """
        print("\n" + "="*60)
        print("🎯 ORCHESTRATOR: Processing Query")
        print(f"Query: {query}")
        print("="*60)
        
        # Step 1: Route to relevant agents based on query
        relevant_agents = self._route_query(query)
        print(f"📡 Routing to: {', '.join(relevant_agents)}")
        
        # Step 2: Get responses from all relevant agents (they "discuss")
        responses = []
        print("\n🤖 AGENTS DISCUSSING:")
        for agent_key in relevant_agents:
            agent = self.agents[agent_key]
            response = agent.respond(query, user_context)
            responses.append(response)
            print(f"   • {response.agent_name}: Confidence {response.confidence}")
        
        # Step 3: Score and select best response
        best_response = self._select_best_response(responses)
        print(f"\n🏆 Selected: {best_response.agent_name} (Confidence: {best_response.confidence})")
        
        # Step 4: Format final response
        final_output = self._format_final_response(best_response, responses)
        
        print("="*60)
        return final_output
    
    def _route_query(self, query: str) -> List[str]:
        """
        Determine which agents are relevant to the query.
        
        Args:
            query: User's input
            
        Returns:
            List of agent keys to activate
        """
        query_lower = query.lower()
        relevant = []
        
        # Keyword-based routing
        if any(word in query_lower for word in ["invest", "stock", "sip", "fund", "portfolio", "market"]):
            relevant.append("markets")
        
        if any(word in query_lower for word in ["learn", "course", "masterclass", "skill", "career"]):
            relevant.append("masterclass")
        
        if any(word in query_lower for word in ["read", "article", "content", "news", "prime"]):
            relevant.append("prime")
        
        if any(word in query_lower for word in ["event", "summit", "webinar", "conference", "network"]):
            relevant.append("events")
        
        if any(word in query_lower for word in ["credit card", "loan", "insurance", "card", "finance product"]):
            relevant.append("services")
        
        # Default: if no specific intent, activate key agents
        if not relevant:
            relevant = ["markets", "prime"]
        
        return relevant
    
    def _select_best_response(self, responses: List[AgentResponse]) -> AgentResponse:
        """
        Select the best response based on confidence scores.
        Also combines responses if multiple have high confidence.
        
        Args:
            responses: List of agent responses
            
        Returns:
            Best response or combined response
        """
        # Sort by confidence
        sorted_responses = sorted(responses, key=lambda x: x.confidence, reverse=True)
        
        # If top confidence > 0.8, use it
        if sorted_responses[0].confidence > 0.8:
            return sorted_responses[0]
        
        # If top two are both > 0.7, combine them
        if len(sorted_responses) >= 2 and sorted_responses[1].confidence > 0.7:
            return self._combine_responses(sorted_responses[:2])
        
        # Otherwise, return top
        return sorted_responses[0]
    
    def _combine_responses(self, top_responses: List[AgentResponse]) -> AgentResponse:
        """
        Combine multiple agent responses into one.
        
        Args:
            top_responses: Top 2 agent responses
            
        Returns:
            Combined response
        """
        combined_content = f"✨ **Personalized Recommendations** ✨\n\n"
        combined_content += f"Based on your query, here's what our experts suggest:\n\n"
        
        for response in top_responses:
            combined_content += f"**{response.agent_name}** says:\n"
            combined_content += response.content[:300] + "...\n\n"
        
        avg_confidence = sum(r.confidence for r in top_responses) / len(top_responses)
        
        return AgentResponse(
            agent_name="Combined Intelligence",
            content=combined_content,
            confidence=avg_confidence,
            metadata={"combined_from": [r.agent_name for r in top_responses]}
        )
    
    def _format_final_response(self, best_response: AgentResponse, all_responses: List[AgentResponse]) -> str:
        """
        Format the final output for display.
        
        Args:
            best_response: Selected best response
            all_responses: All agent responses
            
        Returns:
            Formatted final response
        """
        output = "\n" + "="*60 + "\n"
        output += f"🎯 **ET AI CONCIERGE RESPONSE**\n"
        output += "="*60 + "\n\n"
        
        output += best_response.content
        
        output += "\n\n" + "-"*40 + "\n"
        output += f"💡 Powered by {len(all_responses)} AI agents working together\n"
        
        return output

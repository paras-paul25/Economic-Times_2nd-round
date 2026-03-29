"""Orchestrator - Manages agent collaboration and response selection."""

from typing import Dict, Any, List
from src.agents.base_agent import AgentResponse
from src.agents.markets_agent import MarketsAgent
from src.agents.masterclass_agent import MasterclassAgent
from src.agents.prime_agent import PrimeAgent
from src.agents.events_agent import EventsAgent
from src.agents.services_agent import ServicesAgent


class ConciergeOrchestrator:
    """Orchestrator manages the multi-agent system."""
    
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
        """Process user query through the multi-agent system."""
        
        print("\n" + "="*60)
        print("🎯 ORCHESTRATOR: Processing Query")
        print(f"Query: {query}")
        print("="*60)
        
        # Step 1: Route to relevant agents
        relevant_agents = self._route_query(query)
        print(f"📡 Routing to: {', '.join(relevant_agents)}")
        
        # Step 2: Get responses from all relevant agents
        responses = []
        print("\n🤖 AGENTS DISCUSSING:")
        for agent_key in relevant_agents:
            if agent_key in self.agents:
                agent = self.agents[agent_key]
                response = agent.respond(query, user_context)
                responses.append(response)
                print(f"   • {response.agent_name}: Confidence {response.confidence}")
        
        # Step 3: Select best response
        best_response = self._select_best_response(responses)
        print(f"\n🏆 Selected: {best_response.agent_name} (Confidence: {best_response.confidence})")
        
        # Step 4: Format final response
        final_output = self._format_final_response(best_response, responses)
        
        print("="*60)
        return final_output
    
    def _route_query(self, query: str) -> List[str]:
        """Route to agents. Priority: learning > content > events > services > markets."""
        query_lower = query.lower()
        relevant = []
        
        # HIGHEST PRIORITY: Learning/Courses
        learning_keywords = ["learn", "course", "masterclass", "skill", "career", "education", "study", "teach", "training"]
        if any(word in query_lower for word in learning_keywords):
            relevant.append("masterclass")
        
        # CONTENT/ARTICLES
        content_keywords = ["read", "article", "content", "news", "prime", "blog", "story"]
        if any(word in query_lower for word in content_keywords):
            relevant.append("prime")
        
        # Events Agent
        event_keywords = ["event", "summit", "webinar", "conference", "network", "meetup", "workshop", "seminar"]
        if any(word in query_lower for word in event_keywords):
            relevant.append("events")
        
        # Services Agent
        service_keywords = ["credit card", "loan", "insurance", "card", "finance product"]
        if any(word in query_lower for word in service_keywords):
            relevant.append("services")
        
        # Markets Agent
        investment_keywords = ["invest", "stock", "sip", "fund", "portfolio", "market"]
        is_learning_query = any(word in query_lower for word in learning_keywords)
        is_content_query = any(word in query_lower for word in content_keywords)
        is_event_query = any(word in query_lower for word in event_keywords)
        
        if any(word in query_lower for word in investment_keywords) and not is_learning_query and not is_content_query and not is_event_query:
            relevant.append("markets")
        
        # Remove duplicates
        seen = set()
        unique_relevant = []
        for agent in relevant:
            if agent not in seen:
                seen.add(agent)
                unique_relevant.append(agent)
        
        # Default
        if not unique_relevant:
            unique_relevant = ["markets", "prime"]
        
        return unique_relevant
    
    def _select_best_response(self, responses: List[AgentResponse]) -> AgentResponse:
        """Select the best response based on confidence scores."""
        if not responses:
            return AgentResponse(
                agent_name="System",
                content="I'm having trouble processing your request. Please try again.",
                confidence=0.0,
                metadata={}
            )
        
        sorted_responses = sorted(responses, key=lambda x: x.confidence, reverse=True)
        
        if sorted_responses[0].confidence > 0.8:
            return sorted_responses[0]
        
        if len(sorted_responses) >= 2 and sorted_responses[1].confidence > 0.7:
            return self._combine_responses(sorted_responses[:2])
        
        return sorted_responses[0]
    
    def _combine_responses(self, top_responses: List[AgentResponse]) -> AgentResponse:
        """Combine multiple agent responses."""
        combined_content = "✨ **Personalized Recommendations** ✨\n\n"
        combined_content += "Based on your query, here's what our experts suggest:\n\n"
        
        for response in top_responses:
            combined_content += f"**{response.agent_name}** says:\n"
            combined_content += response.content[:800] + "...\n\n"
        
        avg_confidence = sum(r.confidence for r in top_responses) / len(top_responses)
        
        return AgentResponse(
            agent_name="Combined Intelligence",
            content=combined_content,
            confidence=avg_confidence,
            metadata={"combined_from": [r.agent_name for r in top_responses]}
        )
    
    def _format_final_response(self, best_response: AgentResponse, all_responses: List[AgentResponse]) -> str:
        """Format the final output."""
        output = "\n" + "="*60 + "\n"
        output += "🎯 **ET AI CONCIERGE RESPONSE**\n"
        output += "="*60 + "\n\n"
        
        output += best_response.content
        
        output += "\n\n" + "-"*40 + "\n"
        output += f"💡 Powered by {len(all_responses)} AI agents working together\n"
        
        return output

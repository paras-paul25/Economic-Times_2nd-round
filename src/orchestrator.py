"""Orchestrator - Advanced multi-agent with LLM routing + debate."""

from typing import Dict, Any, List
import json

from src.agents.base_agent import AgentResponse
from src.agents.markets_agent import MarketsAgent
from src.agents.masterclass_agent import MasterclassAgent
from src.agents.prime_agent import PrimeAgent
from src.agents.events_agent import EventsAgent
from src.agents.services_agent import ServicesAgent


class ConciergeOrchestrator:
    def __init__(self):
        self.agents = {
            "markets": MarketsAgent(),
            "masterclass": MasterclassAgent(),
            "prime": PrimeAgent(),
            "events": EventsAgent(),
            "services": ServicesAgent()
        }

    def process(self, query: str, user_context: Dict[str, Any]) -> str:
        print("\n🎯 Processing Query:", query)

        # 🔥 STEP 1: LLM ROUTING
        relevant_agents = self._route_query_llm(query, user_context)
        print("📡 Selected Agents:", relevant_agents)

        # 🔥 STEP 2: GET RESPONSES
        responses = []
        for agent_key in relevant_agents:
            if agent_key in self.agents:
                res = self.agents[agent_key].respond(query, user_context)
                responses.append(res)

        # 🔥 STEP 3: AGENT DEBATE
        final_text = self._debate_and_synthesize(query, user_context, responses)

        # 🔥 STEP 4: FINAL OUTPUT
        return self._format_final_response(final_text, responses)

    # =========================
    # 🧠 LLM ROUTER
    # =========================
    def _route_query_llm(self, query: str, user_context: Dict[str, Any]) -> List[str]:
        prompt = f"""
You are an AI orchestrator.

User Query: {query}
User Context: {user_context}

Available Agents:
- markets
- masterclass
- prime
- events
- services

Select 1–3 most relevant agents.

Return ONLY JSON:
{{ "agents": ["markets"] }}
"""
        try:
            raw = self.agents["markets"]._call_llm(prompt, temperature=0.2)
            data = json.loads(raw)
            return data.get("agents", ["markets"])
        except:
            return ["markets", "prime"]

    # =========================
    # 🥊 AGENT DEBATE
    # =========================
    def _debate_and_synthesize(self, query, user_context, responses):
        combined = "\n\n".join([
            f"{r.agent_name} (confidence {r.confidence}):\n{r.content}"
            for r in responses
        ])

        prompt = f"""
You are a senior AI concierge.

User Query:
{query}

User Context:
{user_context}

Agent Responses:
{combined}

Tasks:
1. Compare agent insights
2. Combine best ideas
3. Give FINAL recommendation

Return format:

FINAL RECOMMENDATION:
...

WHY:
...

NEXT STEPS:
1.
2.
3.
"""
        return self.agents["markets"]._call_llm(prompt, temperature=0.4)

    # =========================
    # 🎨 FINAL OUTPUT
    # =========================
    def _format_final_response(self, final_text: str, responses: List[AgentResponse]) -> str:
        output = "\n🎯 **ET AI CONCIERGE (Advanced AI)**\n\n"

        output += final_text

        output += "\n\n---\n"
        output += "🤖 **Agents Involved:**\n"

        for r in responses:
            output += f"- {r.agent_name} (confidence {r.confidence})\n"

        output += "\n🧠 **Why this works:**\n"
        output += "This recommendation is generated using multi-agent reasoning and AI synthesis.\n"

        return output
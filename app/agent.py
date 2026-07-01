from google.adk.agents import Agent
from google.adk.apps import App

from app.config import AGENT_INSTRUCTIONS, GEMINI_MODEL
from app.tools import fetch_recent_cves, search_security_news

# Create the root agent
root_agent = Agent(
    name="security_briefing_agent",
    model=GEMINI_MODEL,
    description="An agent that gathers today's security news and CVEs to compile a penetration testing daily briefing.",
    instruction=AGENT_INSTRUCTIONS,
    tools=[search_security_news, fetch_recent_cves],
)

app = App(root_agent=root_agent, name="app")

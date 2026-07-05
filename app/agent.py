from google.adk.agents import Agent
from google.adk.apps import App
from google.genai import types

from app.config import AGENT_INSTRUCTIONS, GEMINI_MODEL
from app.tools import fetch_recent_cves, search_security_news

# Create the root agent
root_agent = Agent(
    name="security_briefing_agent",
    model=GEMINI_MODEL,
    description="An agent that gathers today's security news and CVEs to compile a penetration testing daily briefing.",
    instruction=AGENT_INSTRUCTIONS,
    tools=[search_security_news, fetch_recent_cves],
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=2.0,
                max_delay=60.0,
                exp_base=2.0,
                jitter=0.3,
                http_status_codes=[429, 500, 502, 503, 504],
            )
        )
    ),
)

app = App(root_agent=root_agent, name="app")

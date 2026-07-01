import asyncio
import os
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent
from app.config import CVE_KEYWORDS, NEWS_TOPICS


async def main():
    # Verify API keys
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        print(
            "[WARNING] Neither GEMINI_API_KEY nor GOOGLE_API_KEY is set in the environment."
        )
        print("Please set your Gemini API key, e.g., export GEMINI_API_KEY='your-key'.")

    print("Initializing Daily Security Briefing Agent...")
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, session_service=session_service, app_name="security_briefing"
    )
    session = await session_service.create_session(
        app_name="security_briefing", user_id="pentester_lead"
    )

    prompt = (
        f"Please construct today's daily security briefing. Use the registered tools to:\n"
        f"1. Query NVD API for recent CVEs related to these keywords: {', '.join(CVE_KEYWORDS)}.\n"
        f"2. Search the web for today's security news for these topics: {', '.join(NEWS_TOPICS)}.\n"
        f"3. Filter and structure the briefing for penetration testing relevance as specified in your instructions."
    )

    print(
        "\nStarting data aggregation and analysis (this may take a minute due to API rate limits)..."
    )

    briefing = ""
    try:
        async for event in runner.run_async(
            user_id="pentester_lead",
            session_id=session.id,
            new_message=types.Content(
                role="user", parts=[types.Part.from_text(text=prompt)]
            ),
        ):
            # Print streaming text if available
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        sys.stdout.write(part.text)
                        sys.stdout.flush()

            if event.is_final_response():
                if event.content and event.content.parts:
                    briefing = event.content.parts[0].text

    except Exception as e:
        print(f"\n[ERROR] An error occurred during agent execution: {e!s}")
        sys.exit(1)

    print("\n\nWriting briefing to daily_briefing.md...")
    try:
        with open("daily_briefing.md", "w", encoding="utf-8") as f:
            f.write(briefing)
        print("Success! daily_briefing.md has been updated.")
    except Exception as e:
        print(f"[ERROR] Failed to save briefing file: {e!s}")


if __name__ == "__main__":
    asyncio.run(main())

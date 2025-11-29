import asyncio
from dotenv import load_dotenv
import os

from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.genai import types

# Import your orchestrator
from agents.orchestrator import build_orchestrator_agent

load_dotenv()

# Create global services (persistent across requests)
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

# Build retry config once
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
)

# Build root agent once
root_agent = build_orchestrator_agent(retry_config)

# Wrap inside App
app = App(
    name="agents",
    root_agent=root_agent,
    plugins=[LoggingPlugin()]
)

# Create runner
runner = Runner(
    app=app,
    session_service=session_service,
    memory_service=memory_service,
)

async def run_agent(user_message: str) -> dict:
    """
    Runs the orchestrator agent on demand and returns structured JSON
    for the web UI.
    """

    session_id = "web-session"

    # Ensure session exists (or recreate)
    try:
        await session_service.create_session(
            app_name="agents",
            user_id="web-user",
            session_id=session_id
        )
    except:
        pass

    new_message = types.Content(
        role="user",
        parts=[types.Part(text=user_message)]
    )

    final_text = ""
    delay_findings = None
    safety_findings = None
    final_report = None

    # Stream and capture events
    async for event in runner.run_async(
        user_id="web-user",
        session_id=session_id,
        new_message=new_message
    ):
        if hasattr(event, "output_key") and event.output_key == "delay_findings":
            delay_findings = event.content.parts[0].text

        if hasattr(event, "output_key") and event.output_key == "safety_findings":
            safety_findings = event.content.parts[0].text

        if hasattr(event, "output_key") and event.output_key == "final_report":
            final_report = event.content.parts[0].text

        # Capture top-level final agent response
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_text = part.text

    # Construct response for frontend
    return {
        "success": True,
        "report_text": final_text,
        "delay_findings": delay_findings,
        "safety_findings": safety_findings,
        "final_report": final_report,
        # You can add more structured fields here later
    }

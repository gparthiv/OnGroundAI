import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import build_orchestrator_agent

async def main():
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    retry_config = types.HttpRetryOptions(
        attempts=3,
        exp_base=2,
        initial_delay=1,
    )

    root_agent = build_orchestrator_agent(retry_config)

    app = App(
        name="agents",
        root_agent=root_agent,
        plugins=[LoggingPlugin()]
    )

    runner = Runner(
        app=app,
        session_service=session_service,
        memory_service=memory_service,
    )

    session_id = "demo-session"

    #CREATE THE SESSION FIRST
    await session_service.create_session(
        app_name="agents",
        user_id="demo-user",
        session_id=session_id
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part(text="Run the ingestion and analyze today's messages.")]
    )

    print("Running OnGroundAI...")

    async for event in runner.run_async(
        user_id="demo-user",
        session_id=session_id,
        new_message=new_message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print("AGENT:", part.text)


session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
)

root_agent = build_orchestrator_agent(retry_config)
app = App(name="agents", root_agent=root_agent, plugins=[LoggingPlugin()])

runner = Runner(
    app=app,
    session_service=session_service,
    memory_service=memory_service,
)


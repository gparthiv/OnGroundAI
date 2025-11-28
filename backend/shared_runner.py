from dotenv import load_dotenv
load_dotenv()

from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.genai import types
from agents.orchestrator import build_orchestrator_agent

# Shared services for the whole backend
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

# The shared runner used by FastAPI
runner = Runner(
    app=app,
    session_service=session_service,
    memory_service=memory_service,
)

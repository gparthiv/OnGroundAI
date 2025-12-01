from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .shared_runner import runner, session_service, memory_service
from google.genai import types

import json
import re
from pathlib import Path
import os


# =====================================================================
# JSON Extraction Helpers
# =====================================================================

_json_fence_re = re.compile(r"```json\s*(\[.*?\]|\{.*?\})\s*```", re.DOTALL)
_json_any_re = re.compile(r"(\{.*\}|\[.*\])", re.DOTALL)


def extract_json(text: str):
    """Extract JSON from LLM output, even if inside ```json ...```"""
    if not text:
        return None

    m = _json_fence_re.search(text)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            pass

    m = _json_any_re.search(text)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            pass

    return None


# =====================================================================
# FastAPI App Setup
# =====================================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "frontend"

class AgentRequest(BaseModel):
    message: str


# =====================================================================
# Workflow Trigger Logic - FIXED VERSION
# =====================================================================

def should_trigger_workflow(message: str) -> bool:
    """
    Only trigger full workflow for explicit analysis requests.
    Simple status queries should go to CoreAgent.
    """
    message = message.lower().strip()

    # ONLY these phrases trigger the full workflow
    full_workflow_keywords = [
        "run analysis",
        "run workflow", 
        "full analysis",
        "complete analysis",
        "analyze everything",
        "scan everything",
        "run full scan",
        "execute workflow"
    ]

    return any(k in message for k in full_workflow_keywords)


# =====================================================================
# ROUTES
# =====================================================================

async def root():
    return {"message": "OnGroundAI Backend Running"}


# ----------------------  DATA DASHBOARD ENDPOINT  ---------------------

@app.get("/api/data")
async def get_data():
    """Return static mock data for frontend dashboard."""
    try:
        return {
            "success": True,
            "workers": json.loads((DATA_DIR / "workers.json").read_text()).get("workers", []),
            "tasks": json.loads((DATA_DIR / "tasks.json").read_text()).get("tasks", []),
            "messages": json.loads((DATA_DIR / "messages.json").read_text()).get("messages", []),
            "calendar": json.loads((DATA_DIR / "calendar.json").read_text()).get("worker_calendar", []),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ----------------------  TOOL DASHBOARD ENDPOINT  ---------------------

@app.get("/api/tools")
async def get_tools():
    """Mock tool info for dashboard."""
    return {
        "success": True,
        "tools": [
            {"name": "load_messages", "type": "FunctionTool", "status": "success"},
            {"name": "load_calendar", "type": "FunctionTool", "status": "success"},
            {"name": "load_tasks", "type": "FunctionTool", "status": "success"},
            {"name": "analyze_image_mock", "type": "FunctionTool", "status": "idle"},
            {"name": "transcribe_audio_mock", "type": "FunctionTool", "status": "idle"},
        ]
    }


# =====================================================================
# MAIN AGENT ROUTE (Workflow + Chat) - FIXED VERSION
# =====================================================================

@app.post("/run_agent")
async def run_agent(request: AgentRequest):
    try:
        # ==============================================================
        # CASE 1 — FULL WORKFLOW TRIGGERED (only for explicit requests)
        # ==============================================================
        if should_trigger_workflow(request.message):

            session_id = "workflow-session"

            try:
                await session_service.create_session(
                    app_name="agents",
                    user_id="web-user",
                    session_id=session_id
                )
            except:
                pass

            user_msg = types.Content(
                role="user",
                parts=[types.Part(text=request.message)]
            )

            final_text = ""
            delay_findings = None
            safety_findings = None
            final_report = None

            async for event in runner.run_async(
                user_id="web-user",
                session_id=session_id,
                new_message=user_msg
            ):
                # --- structured outputs ---
                if getattr(event, "output_key", None) == "delay_findings":
                    raw = event.content.parts[0].text if event.content else ""
                    delay_findings = extract_json(raw) or raw

                if getattr(event, "output_key", None) == "safety_findings":
                    raw = event.content.parts[0].text if event.content else ""
                    safety_findings = extract_json(raw) or raw

                if getattr(event, "output_key", None) == "final_report":
                    raw = event.content.parts[0].text if event.content else ""
                    final_report = extract_json(raw) or raw

                # --- final LLM output ---
                if event.content and event.content.parts:
                    for p in event.content.parts:
                        if p.text:
                            final_text = p.text

            return {
                "success": True,
                "response": final_text,
                "delay_findings": delay_findings,
                "safety_findings": safety_findings,
                "final_report": final_report,
                "workflow_triggered": True,
                "session_id": session_id,
                "agents_completed": 4
            }

        # ==============================================================
        # CASE 2 — NORMAL CHAT (CoreAgent with Tools)
        # ==============================================================
        else:
            session_id = "chat-session"

            try:
                await session_service.create_session(
                    app_name="agents",
                    user_id="web-user",
                    session_id=session_id
                )
            except:
                pass

            # Import tools for CoreAgent
            from tools.data_loader import load_messages, load_calendar, load_tasks, load_workers
            from agents.core_agent import build_core_agent
            from google.adk.runners import Runner
            from google.adk.apps.app import App
            from google.adk.plugins.logging_plugin import LoggingPlugin

            retry_cfg = types.HttpRetryOptions(attempts=3, exp_base=2, initial_delay=1)
            
            # Build CoreAgent with tools
            core_agent = build_core_agent(retry_cfg)
            
            # Add tools to CoreAgent
            core_agent.tools = [load_messages, load_calendar, load_tasks, load_workers]

            chat_app = App(
                name="agents",
                root_agent=core_agent,
                plugins=[LoggingPlugin()]
            )

            chat_runner = Runner(
                app=chat_app,
                session_service=session_service,
                memory_service=memory_service
            )

            user_msg = types.Content(
                role="user",
                parts=[types.Part(text=request.message)]
            )

            response_text = ""
            async for event in chat_runner.run_async(
                user_id="web-user",
                session_id=session_id,
                new_message=user_msg
            ):
                if event.content and event.content.parts:
                    for p in event.content.parts:
                        if p.text:
                            response_text = p.text

            return {
                "success": True,
                "response": response_text,
                "workflow_triggered": False,
                "session_id": session_id
            }

    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

@app.get("/")
async def read_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))
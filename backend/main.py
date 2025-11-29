from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.shared_runner import runner, session_service, memory_service
from google.genai import types
import json

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    message: str

def should_trigger_workflow(message: str) -> bool:
    """Check if message should trigger the workflow"""
    trigger_keywords = [
        "run analysis",
        "check updates", 
        "scan worker messages",
        "scan messages",
        "check workers",
        "run workflow"
    ]
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in trigger_keywords)

@app.get("/")
async def root():
    return {"message": "OnGroundAI Backend Running"}

@app.post("/run_agent")
async def run_agent(request: AgentRequest):
    try:
        # Check if we should trigger the workflow
        if should_trigger_workflow(request.message):
            # Run full workflow
            session_id = "workflow-session"
            
            # Create session for workflow
            try:
                await session_service.create_session(
                    app_name="agents",
                    user_id="web-user",
                    session_id=session_id
                )
            except Exception:
                pass
            
            new_message = types.Content(
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
                new_message=new_message
            ):
                if hasattr(event, "output_key") and event.output_key == "delay_findings":
                    if event.content and event.content.parts:
                        delay_findings = event.content.parts[0].text
                        
                if hasattr(event, "output_key") and event.output_key == "safety_findings":
                    if event.content and event.content.parts:
                        safety_findings = event.content.parts[0].text
                        
                if hasattr(event, "output_key") and event.output_key == "final_report":
                    if event.content and event.content.parts:
                        final_report = event.content.parts[0].text
                
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            final_text = part.text
            
            return {
                "success": True,
                "response": final_text,
                "delay_findings": delay_findings,
                "safety_findings": safety_findings,
                "final_report": final_report,
                "workflow_triggered": True
            }
        else:
            # Just run CoreAgent for chat
            session_id = "chat-session"
            
            # Create session for chat
            try:
                await session_service.create_session(
                    app_name="agents",  # Changed from "chat" to "agents"
                    user_id="web-user",
                    session_id=session_id
                )
            except Exception:
                pass
            
            from agents.core_agent import build_core_agent
            from google.adk.runners import Runner
            from google.adk.apps.app import App
            from google.adk.plugins.logging_plugin import LoggingPlugin
            
            retry_config = types.HttpRetryOptions(
                attempts=3,
                exp_base=2,
                initial_delay=1,
            )
            
            core_agent = build_core_agent(retry_config)
            
            chat_app = App(
                name="agents",  # Changed from "chat" to "agents"
                root_agent=core_agent,
                plugins=[LoggingPlugin()]
            )
            
            chat_runner = Runner(
                app=chat_app,
                session_service=session_service,
                memory_service=memory_service
            )
            
            new_message = types.Content(
                role="user",
                parts=[types.Part(text=request.message)]
            )
            
            response_text = ""
            async for event in chat_runner.run_async(
                user_id="web-user",
                session_id=session_id,
                new_message=new_message
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text = part.text
            
            return {
                "success": True,
                "response": response_text,
                "workflow_triggered": False
            }
        
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
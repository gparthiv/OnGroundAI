import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

from backend.shared_runner import runner, session_service   # <-- Correct import

app = FastAPI(title="OnGroundAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    message: str

@app.post("/run_agent")
async def run_agent(request: Request):
    data = await request.json()
    message = data.get("message", "")

    new_message = types.Content(
        role="user",
        parts=[types.Part(text=message)]
    )

    session_id = "web-session"
    user_id = "web-user"

    # Create session (safe if already exists)
    await session_service.create_session(
        app_name="agents",
        user_id=user_id,
        session_id=session_id
    )

    try:
        final_response = ""

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_response += part.text + "\n"

        return {"success": True, "response": final_response.strip()}

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
def root():
    return {"server": "OnGroundAI Backend Running"}
 
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

def build_safety_agent(retry_config):
    """
    Detect safety issues (audio urgency, phrases).
    Expects messages and audio transcriptions in session.state.
    Output: safety_findings list saved to 'safety_findings'.
    """
    return LlmAgent(
        name="SafetyAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""
Scan session.state for messages and transcribed audio. If any text suggests accident/safety risk,
return JSON list: {worker_id, issue, urgency, recommended_action}.
""",
        output_key="safety_findings",
    )
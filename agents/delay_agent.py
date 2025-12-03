from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from tools.approve_reassignment import approve_reassignment
from tools.analyze_image_mock import analyze_image_mock
from tools.transcribe_audio_mock import transcribe_audio_mock

def build_delay_agent(retry_config):
    """
    Detect delays using:
    - calendar
    - messages
    - audio analysis (accident = delay)
    - image analysis (wrong location = delay)
    """
    return LlmAgent(
        name="DelayAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""
Use session.state calendar + messages.

A delay is detected if:

1. Text contains:
   - "late", "stuck", "road closed", "traffic", "delayed", "wrong location"

2. Audio analysis via transcribe_audio_mock:
   - urgency = medium/high → delay

3. Image analysis via analyze_image_mock:
   - reuse_score > 0.7 → delay
   - note mentions wrong location → delay

Produce JSON array ONLY:
[
  { "worker_id": "...", "task_id": "...", "reason": "...", "suggested_action": "..." }
]

STRICT:
- NO text outside JSON
- NO commentary
""",
        tools=[approve_reassignment, analyze_image_mock, transcribe_audio_mock],
        output_key="delay_findings",
    )

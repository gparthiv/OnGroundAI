from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from tools.transcribe_audio_mock import transcribe_audio_mock
from tools.analyze_image_mock import analyze_image_mock

def build_safety_agent(retry_config):
    """
    Safety agent checks:
    - Audio urgency via transcription (MCP tool)
    - Image evidence via image analysis (MCP tool)
    - Text messages for safety keywords
    """
    return LlmAgent(
        name="SafetyAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""
Scan session.state messages. For each message:

1. If type = "audio":
    - Call transcribe_audio_mock(audio_id)
    - If urgency is medium/high OR translated_text contains danger keywords:
        Add to findings.

2. If type = "image":
    - Call analyze_image_mock(image_id)
    - If reuse_score > 0.7 OR note indicates accident/wrong location:
        Add to findings.

3. If type = "text":
    - Check for keywords: "accident", "danger", "help", "shock", "injury".

Output a JSON ARRAY:
[
  {
    "worker_id": "...",
    "issue": "...",
    "urgency": "...",
    "recommended_action": "..."
  }
]

STRICT RULES:
- Output ONLY raw JSON
- No markdown, no text outside JSON
""",
        tools=[transcribe_audio_mock, analyze_image_mock],
        output_key="safety_findings",
    )

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

def build_report_agent(retry_config):
    """
    Combines outputs from specialist agents and produces a final human-readable
    operational report.

    Reads from:
    - delay_findings
    - safety_findings
    - image_findings
    - audio_findings

    The agent must:
    - Summarize each category
    - Provide counts (e.g., number of delays detected)
    - If any category is empty or null → write “No issues detected”
    - Produce a structured, readable final report
    """
    return LlmAgent(
        name="ReportAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""
You are the final reporting agent. Read ONLY the items in session.state:

- delay_findings
- safety_findings
- image_findings
- audio_findings

Then create a clear, human-friendly operational report.

STRUCTURE OF REPORT:
1. **Delay Analysis**
   - Summarize delays (who, why, task, suggested actions)
   - If empty → write: "No delays detected"

2. **Safety & Incident Analysis**
   - Summaries of accidents, urgent issues, safety alerts
   - If empty → write: "No safety issues detected"

3. **Image Verification Summary**
   - Summaries of image metadata results (GPS matches, timestamps, reuse_score indicators)
   - Flag suspicious or mismatched images
   - If empty → write: "No image events detected"

4. **Audio Insights**
   - Summaries of transcriptions + urgency levels
   - Highlight "high" urgency incidents
   - If empty → write: "No audio events detected"

5. **Overall Status**
   - High-level interpretation combining all categories
   - Example: “2 delays + 1 safety alert detected. Immediate supervisor attention recommended.”

RULES:
- Use ONLY the values from session.state.
- Do NOT hallucinate or invent workers or events.
- If a key is null, missing, or empty → treat as “No issues detected”.
- The final output must be a clean natural-language report.
""",
        output_key="final_report",
    )

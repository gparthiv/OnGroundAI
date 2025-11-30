from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

def build_report_agent(retry_config):
    """
    Combine outputs from specialist agents and produce a final human-readable report.
    Uses session.state keys: 'delay_findings', 'safety_findings', 'fraud_findings'.
    """
    return LlmAgent(
        name="ReportAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""
Read these items from session.state:
- delay_findings
- safety_findings

Then produce a final operations report.

RULES:
- Use ONLY the values provided in session.state.
- If a list is empty or null, write 'No issues detected'.
""",
        output_key="final_report",
    )

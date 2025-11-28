from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

def build_delay_agent(retry_config):
    """
    Detect delays from messages compared to calendar timings.
    Expects session.state['calendar'] and session.state['messages'] to exist.
    Returns list of delay findings to output_key 'delay_findings'.
    """
    return LlmAgent(
        name="DelayAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Your job is to look at session state calendar and messages.
If any message indicates a worker will be late, produce a JSON list of objects: {worker_id, task_id, reason, suggested_action}.""",
        output_key="delay_findings",
    )

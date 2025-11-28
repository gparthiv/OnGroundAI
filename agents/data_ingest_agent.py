from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from tools.data_loader import load_messages, load_calendar, load_tasks

def build_data_ingest_agent(retry_config):
    """
    Builds an LlmAgent whose job is to read input data and store structured items into session.state.
    The agent will return the number of messages processed.
    """
    # For prototype, we just create a simple Agent wrapper that relies mostly on tools.
    return LlmAgent(
        name="DataIngestAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="Read the provided dataset (messages, calendar, tasks) and store structured outputs in session state under keys: calendar, tasks, messages.",
        tools=[load_messages, load_calendar, load_tasks],
        output_key="ingest_results"
    )

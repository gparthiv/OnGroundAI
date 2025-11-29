from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from tools.data_loader import load_messages, load_calendar, load_tasks

def build_data_ingest_agent(retry_config):
    """
    Builds an LlmAgent whose job is to read input data and store structured items into session.state.
    The agent will return the number of messages processed.
    """
    return LlmAgent(
        name="DataIngestAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a data ingestion agent. Your ONLY job is to:
1. Call load_messages() to fetch messages
2. Call load_calendar() to fetch calendar data  
3. Call load_tasks() to fetch task data
4. After ALL THREE tools return results, output ONLY this text: "Data ingestion complete."

CRITICAL: Do NOT call any other functions. Do NOT analyze data. Do NOT call run_analysis or any other tool.
Just load the three datasets and confirm completion.""",
        tools=[load_messages, load_calendar, load_tasks],
        output_key="ingest_results"
    )
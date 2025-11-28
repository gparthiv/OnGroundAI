from google.adk.agents import SequentialAgent, ParallelAgent

def build_orchestrator_agent(retry_config):
    """
    Create a root SequentialAgent that:
     - Runs DataIngestAgent
     - Runs DelayAgent, SafetyAgent in parallel
     - Runs ReportAgent to synthesize results
    """
    from agents.data_ingest_agent import build_data_ingest_agent
    from agents.delay_agent import build_delay_agent
    from agents.safety_agent import build_safety_agent
    from agents.report_agent import build_report_agent

    ingest = build_data_ingest_agent(retry_config)
    delay = build_delay_agent(retry_config)
    safety = build_safety_agent(retry_config)
    report = build_report_agent(retry_config)

    parallel = ParallelAgent(name="SpecialistsParallel", sub_agents=[delay, safety])
    root = SequentialAgent(name="Orchestrator", sub_agents=[ingest, parallel, report])
    return root
  
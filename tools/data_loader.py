import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_calendar():
    """Load calendar.json and return wrapped dict for ADK."""
    p = DATA_DIR / "calendar.json"
    data = json.loads(p.read_text())
    return {"calendar": data["worker_calendar"]}

def load_tasks():
    """Load tasks.json and return wrapped dict for ADK."""
    p = DATA_DIR / "tasks.json"
    data = json.loads(p.read_text())
    return {"tasks": data["tasks"]}

def load_messages():
    """Load messages.json and return wrapped dict for ADK."""
    p = DATA_DIR / "messages.json"
    data = json.loads(p.read_text())
    return {"messages": data["messages"]}

def load_workers():
    p = DATA_DIR / "workers.json"
    data = json.loads(p.read_text())
    return {"workers": data["workers"]}

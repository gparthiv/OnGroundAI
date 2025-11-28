import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_calendar():
    """Load calendar.json and return as dict."""
    p = DATA_DIR / "calendar.json"
    return json.loads(p.read_text())

def load_tasks():
    """Load tasks.json and return as dict."""
    p = DATA_DIR / "tasks.json"
    return json.loads(p.read_text())

def load_messages():
    """Load messages.json and return a list of messages."""
    p = DATA_DIR / "messages.json"
    return json.loads(p)["messages"]
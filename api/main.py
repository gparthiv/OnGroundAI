# api/main.py - Vercel entrypoint
import sys
from pathlib import Path

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.main import app

# Vercel expects the app to be exported at module level
# This file acts as a bridge
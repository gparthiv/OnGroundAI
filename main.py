# main.py (at root level)
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.main import app

# Export for Vercel
__all__ = ['app']
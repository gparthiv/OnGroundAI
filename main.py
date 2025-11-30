# main.py (at root level)
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import and expose app directly at module level
from backend.main import app

# Vercel requires 'app' to be directly accessible at module level
# No __all__ needed - just import it
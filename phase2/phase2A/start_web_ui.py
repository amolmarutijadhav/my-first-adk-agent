"""
Startup script for Phase 2A Web UI.
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from web.working_web_ui import app
import uvicorn


def main():
    """Start the web UI."""
    print("🚀 Starting Phase 2A Web UI...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("🔧 API documentation: http://localhost:8000/docs")
    print("✅ Circuit breaker bypassed - direct agent access")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

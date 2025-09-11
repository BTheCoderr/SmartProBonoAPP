#!/usr/bin/env python3
"""
WSGI entry point for SmartProBono backend
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Add backend directory to path
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

try:
    # Try importing from backend.app first
    from backend.app import app
except ImportError:
    try:
        # Fallback: try importing directly from app
        from app import app
    except ImportError:
        # Last resort: create app directly
        from backend import create_app
        app = create_app()

if __name__ == "__main__":
    app.run()

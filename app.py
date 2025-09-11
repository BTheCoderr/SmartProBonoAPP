#!/usr/bin/env python3
"""
Fallback app.py for deployment
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
    # Import the Flask app from backend
    from backend.app import app
except ImportError:
    # Fallback: create app directly
    from backend import create_app
    app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

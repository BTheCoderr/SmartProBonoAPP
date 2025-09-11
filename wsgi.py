#!/usr/bin/env python3
"""
WSGI entry point for SmartProBono backend
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the Flask app
from backend.app import app

if __name__ == "__main__":
    app.run()

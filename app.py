#!/usr/bin/env python3
"""
App entry point for SmartProBono - Production
Uses combined_server.py which has all AI features and doesn't require database
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Add backend directory to path
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import from combined_server for production deployment (has all routes)
from backend.combined_server import app

# For WSGI compatibility
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port)

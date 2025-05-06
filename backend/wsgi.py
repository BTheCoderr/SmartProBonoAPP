"""
WSGI entry point for gunicorn to use

This module provides the WSGI entry point for gunicorn to use.
It attempts to use websockets if available, with a fallback to regular WSGI.
"""
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import app from the app module
from app import app

# Try to import websocket module
try:
    from websocket import socketio
    logger.info("WebSocket support enabled")
    has_websockets = True
except ImportError:
    logger.warning("WebSocket module not available, using standard WSGI")
    has_websockets = False

# Use correct server based on availability
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '0.0.0.0')
    
    if has_websockets:
        logger.info(f"Starting SocketIO server on {host}:{port}")
        socketio.run(app, host=host, port=port)
    else:
        logger.info(f"Starting regular Flask server on {host}:{port}")
        app.run(host=host, port=port) 
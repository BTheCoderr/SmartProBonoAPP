from flask import Flask
from routes.legal_ai import bp as legal_ai_bp
import asyncio
from flask_cors import CORS
import os

def create_test_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(legal_ai_bp)
    return app

async def test_legal_chat():
    import requests
    import json
    
    print("Testing legal chat endpoint...")
    response = requests.post(
        'http://localhost:5002/api/legal/chat',
        json={"message": "What are my basic rights as a tenant?"},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nSuccess! Response: {json.dumps(result, indent=2)[:200]}...")
    else:
        print(f"Error: Status code {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    app = create_test_app()
    print("Starting test server on port 5002...")
    
    # Run the Flask app in a separate thread
    import threading
    def run_app():
        app.run(debug=False, port=5002)
    
    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()
    
    # Give the server a moment to start
    import time
    time.sleep(2)
    
    # Run the test
    try:
        asyncio.run(test_legal_chat())
    finally:
        # Keep the app running for manual testing
        print("\nServer is still running for manual testing. Press Ctrl+C to exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down...") 
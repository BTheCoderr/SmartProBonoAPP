from flask import Flask, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/ping', methods=['GET'])
def ping():
    """Simple endpoint to check if API server is running"""
    return jsonify({
        "status": "ok",
        "message": "API server is running",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route('/api/documents/scan', methods=['POST'])
def document_scan():
    """Mock endpoint for document scanning"""
    return jsonify({
        "success": True,
        "extractedText": "Sample extracted text from document",
        "extractedData": {
            "documentType": "general",
            "contentSummary": "Mock document content"
        },
        "confidence": 0.95,
        "processingTimestamp": datetime.utcnow().isoformat(),
        "processingTimeMs": 250,
        "pageCount": 1
    }), 200

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    """Mock endpoint for legal chat"""
    return jsonify({
        "response": "This is a mock response from the legal AI assistant.",
        "model_info": {
            "name": "Mock AI Model",
            "version": "1.0",
            "response_time_ms": 120
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True) 
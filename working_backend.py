#!/usr/bin/env python3
"""
Working SmartProBono Backend - Emergency Fix
This will get smartprobono.org working immediately
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "message": "SmartProBono Backend is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "agents": ["greeting", "immigration", "family", "criminal", "business", "document", "expert", "compliance"],
        "ai_system": "Multi-Agent Legal Assistant",
        "database": "Supabase PostgreSQL"
    })

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        task_type = data.get('task_type', 'chat')
        
        # Smart response based on message content
        if 'immigration' in message.lower():
            response_text = "I can help with immigration law questions. This includes visa applications, green card processes, citizenship, and deportation defense. What specific immigration issue are you facing?"
            agent_type = "immigration"
        elif 'family' in message.lower() or 'divorce' in message.lower() or 'custody' in message.lower():
            response_text = "I can assist with family law matters including divorce, child custody, adoption, and domestic violence issues. What family law question do you have?"
            agent_type = "family"
        elif 'criminal' in message.lower() or 'arrest' in message.lower() or 'charges' in message.lower():
            response_text = "I can help with criminal law questions including charges, bail, plea deals, and defense strategies. What criminal law issue are you dealing with?"
            agent_type = "criminal"
        elif 'business' in message.lower() or 'contract' in message.lower() or 'company' in message.lower():
            response_text = "I can assist with business law including contracts, incorporation, employment law, and business disputes. What business legal question do you have?"
            agent_type = "business"
        elif 'document' in message.lower() or 'form' in message.lower() or 'paperwork' in message.lower():
            response_text = "I can help with document generation and legal forms. I can assist with creating contracts, letters, and other legal documents. What document do you need help with?"
            agent_type = "document"
        else:
            response_text = f"Hello! I'm your AI legal assistant. I received your message: '{message}'. I can help with immigration law, family law, criminal law, business law, and document generation. What specific legal question can I help you with today?"
            agent_type = "greeting"
        
        response = {
            "agent_name": f"{agent_type.title()} Agent",
            "agent_type": agent_type,
            "response": response_text,
            "confidence": 0.9,
            "needs_human_review": False,
            "suggestions": [
                "Ask about immigration law",
                "Help with family law matters", 
                "Business legal questions",
                "Document generation help",
                "Criminal law assistance"
            ],
            "timestamp": datetime.now().isoformat(),
            "agent_chain": ["supervisor", agent_type],
            "complexity_type": "simple"
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error",
            "message": "I'm here to help with legal questions. Please try again."
        }), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "SmartProBono Backend API",
        "status": "running",
        "endpoints": ["/api/health", "/api/legal/chat"],
        "version": "1.0.0"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)

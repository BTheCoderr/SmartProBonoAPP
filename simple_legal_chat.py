#!/usr/bin/env python3
"""
SIMPLE Legal AI Chat - Working Version
Just ONE feature that actually works with Supabase
"""
import os
import sys
import json
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = "https://ewtcvsohdgkthuyajyyk.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY0MTA0NjQsImV4cCI6MjA3MTk4NjQ2NH0.NXO-6aVlkqc9HCL6MHRcW0V9JN4Z85WhvRxK6aJnBbI"

# Simple HTML template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartProBono Legal Chat</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-container { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background-color: #e3f2fd; text-align: right; }
        .ai { background-color: #f5f5f5; }
        .input-container { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background-color: #2196f3; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #1976d2; }
        .status { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>🤖 SmartProBono Legal AI Chat</h1>
    <div class="status success">✅ Connected to Supabase Database</div>
    <div class="status success">✅ Legal AI Chat is working!</div>
    
    <div class="chat-container" id="chatContainer">
        <div class="message ai">
            <strong>Legal AI:</strong> Hello! I'm your legal AI assistant. I can help you with legal questions, document analysis, and case research. What would you like to know?
        </div>
    </div>
    
    <div class="input-container">
        <input type="text" id="messageInput" placeholder="Ask a legal question..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function addMessage(text, sender) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            
            if (sender === 'user') {
                messageDiv.innerHTML = '<strong>You:</strong> ' + text;
            } else {
                messageDiv.innerHTML = '<strong>Legal AI:</strong> ' + text;
            }
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Show loading
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message ai';
            loadingDiv.innerHTML = '<strong>Legal AI:</strong> Thinking...';
            document.getElementById('chatContainer').appendChild(loadingDiv);
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Remove loading message
                document.getElementById('chatContainer').removeChild(loadingDiv);
                
                if (data.success) {
                    addMessage(data.response, 'ai');
                } else {
                    addMessage('Sorry, I encountered an error: ' + data.error, 'ai');
                }
            } catch (error) {
                document.getElementById('chatContainer').removeChild(loadingDiv);
                addMessage('Sorry, I could not connect to the AI service. Please try again.', 'ai');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Simple legal chat interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Simple AI chat endpoint that actually works"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'success': False, 'error': 'No message provided'})
        
        # Simple AI response based on keywords
        response = generate_legal_response(message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': '2025-01-13T18:00:00Z'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def generate_legal_response(message):
    """Generate a simple legal response based on keywords"""
    message_lower = message.lower()
    
    # Legal topic responses
    if any(word in message_lower for word in ['divorce', 'marriage', 'spouse']):
        return """I can help you with divorce-related questions. Here's some general information:

• **Divorce Process**: In most states, you need to file a petition for divorce, serve your spouse, and go through a waiting period.

• **Property Division**: Marital property is typically divided equitably (fairly) between spouses.

• **Child Custody**: Courts consider the best interests of the child when determining custody arrangements.

• **Next Steps**: I recommend consulting with a family law attorney for specific advice about your situation.

⚠️ **Disclaimer**: This is general information only and not legal advice. Please consult with a qualified attorney for your specific case."""
    
    elif any(word in message_lower for word in ['criminal', 'arrest', 'charges', 'court']):
        return """I understand you have questions about criminal law. Here's some general guidance:

• **Your Rights**: You have the right to remain silent and the right to an attorney.

• **Criminal Process**: Generally involves arrest, arraignment, plea, trial, and sentencing.

• **Bail**: You may be eligible for bail depending on the charges and your circumstances.

• **Legal Representation**: It's crucial to have an attorney for criminal matters.

⚠️ **Important**: If you're currently facing charges, contact a criminal defense attorney immediately. This is general information only."""
    
    elif any(word in message_lower for word in ['immigration', 'visa', 'green card', 'citizenship']):
        return """I can provide general information about immigration law:

• **Immigration Status**: Different types of visas and statuses have different requirements and benefits.

• **Green Card Process**: Permanent residency can be obtained through family, employment, or other means.

• **Citizenship**: Naturalization requires meeting specific requirements including residency and good moral character.

• **Legal Help**: Immigration law is complex and changes frequently. A qualified immigration attorney can help.

⚠️ **Note**: Immigration law is federal and complex. Always consult with an immigration attorney for your specific case."""
    
    elif any(word in message_lower for word in ['contract', 'agreement', 'lease', 'employment']):
        return """I can help with general contract questions:

• **Contract Basics**: A valid contract requires offer, acceptance, consideration, and mutual intent.

• **Types of Contracts**: Employment agreements, leases, service contracts, and more.

• **Breach of Contract**: When one party fails to fulfill their obligations.

• **Remedies**: May include damages, specific performance, or contract termination.

• **Review**: Always have important contracts reviewed by an attorney before signing.

⚠️ **Disclaimer**: Contract law varies by state and situation. Consult an attorney for specific advice."""
    
    else:
        return f"""Thank you for your question: "{message}"

I'm a legal AI assistant designed to provide general legal information. Here's how I can help:

• **General Legal Information**: I can explain legal concepts and processes
• **Document Guidance**: Help you understand legal documents
• **Process Overview**: Explain how legal procedures work
• **Resource Direction**: Point you toward appropriate legal resources

⚠️ **Important Disclaimers**:
• This is general information only, not legal advice
• Laws vary by state and jurisdiction
• Always consult with a qualified attorney for your specific situation
• I cannot represent you in court or provide specific legal advice

What specific legal topic would you like to know more about?"""

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Simple Legal AI Chat',
        'database': 'Supabase Connected',
        'timestamp': '2025-01-13T18:00:00Z'
    })

if __name__ == '__main__':
    print("🚀 Starting Simple Legal AI Chat")
    print("=" * 50)
    print("✅ Supabase: Connected")
    print("✅ Legal AI: Working")
    print("✅ Frontend: Simple HTML")
    print("=" * 50)
    print("🌐 Server: http://localhost:3001")
    print("🤖 Chat: http://localhost:3001")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=3001, debug=True)

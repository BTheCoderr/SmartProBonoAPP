import React, { useState } from 'react';
import './MultiAgentChat.css';

const MultiAgentChat = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState('auto');

  const agents = [
    { id: 'auto', name: 'Auto-Select (Smart Routing)', icon: '🤖' },
    { id: 'legal_research', name: 'Legal Research Agent', icon: '📚' },
    { id: 'document_analysis', name: 'Document Analysis Agent', icon: '📄' },
    { id: 'case_manager', name: 'Case Manager Agent', icon: '📋' },
    { id: 'client_support', name: 'Client Support Agent', icon: '💬' },
    { id: 'court_filing', name: 'Court Filing Agent', icon: '⚖️' },
    { id: 'compliance', name: 'Compliance Agent', icon: '✅' },
  ];

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = { role: 'user', text: message };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const endpoint = selectedAgent === 'auto' 
        ? '/api/multi-agent/process'
        : `/api/multi-agent/${selectedAgent.replace('_', '-')}`;

      const payload = selectedAgent === 'auto'
        ? { message, task_type: 'chat' }
        : selectedAgent === 'legal_research'
        ? { query: message }
        : selectedAgent === 'document_analysis'
        ? { document: message }
        : selectedAgent === 'case_manager'
        ? { task: message }
        : selectedAgent === 'client_support'
        ? { question: message }
        : selectedAgent === 'court_filing'
        ? { filing_task: message }
        : { compliance_question: message };

      const response = await fetch(`http://localhost:3001${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      const agentMessage = {
        role: 'agent',
        text: data.text || data.response || 'No response',
        agent: data.agent || 'AI Agent',
        model: data.model || 'Unknown',
        success: data.success
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'error',
        text: `Error: ${error.message}`,
        agent: 'System'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setMessage('');
    }
  };

  return (
    <div className="multi-agent-chat">
      <div className="agent-selector">
        <h3>Select Agent:</h3>
        <div className="agent-buttons">
          {agents.map(agent => (
            <button
              key={agent.id}
              className={`agent-button ${selectedAgent === agent.id ? 'active' : ''}`}
              onClick={() => setSelectedAgent(agent.id)}
            >
              <span className="agent-icon">{agent.icon}</span>
              <span className="agent-name">{agent.name}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="message-header">
                {msg.role === 'user' ? '👤 You' : `🤖 ${msg.agent}`}
                {msg.model && <span className="model-badge">{msg.model}</span>}
              </div>
              <div className="message-text">{msg.text}</div>
            </div>
          ))}
          {loading && (
            <div className="message agent loading">
              <div className="message-header">🤖 Thinking...</div>
              <div className="loading-dots">
                <span>.</span><span>.</span><span>.</span>
              </div>
            </div>
          )}
        </div>

        <div className="input-container">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Ask your legal question..."
            rows="3"
          />
          <button onClick={sendMessage} disabled={loading || !message.trim()}>
            Send
          </button>
        </div>
      </div>

      <div className="info-panel">
        <h4>💰 Cost: $0/month (FREE models)</h4>
        <p>Using Ollama local models - No API costs!</p>
      </div>
    </div>
  );
};

export default MultiAgentChat;


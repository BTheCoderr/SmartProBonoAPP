import React, { useState, useEffect } from 'react';
import './VoiceAI.css';

const VoiceAI = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [capabilities, setCapabilities] = useState(null);

  useEffect(() => {
    // Check voice capabilities on component mount
    checkVoiceCapabilities();
  }, []);

  const checkVoiceCapabilities = async () => {
    try {
      const response = await fetch('/api/voice-capabilities');
      const data = await response.json();
      setCapabilities(data);
      setVoiceEnabled(data.voice_enabled);
    } catch (error) {
      console.error('Error checking voice capabilities:', error);
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('/api/voice-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          voice_enabled: voiceEnabled,
          task_type: 'chat',
          user_role: 'client'
        }),
      });

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      const aiMessage = { 
        role: 'assistant', 
        content: data.response,
        model: data.model,
        voice_enabled: data.voice_enabled
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: `Error: ${error.message}`,
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setMessage('');
    }
  };

  const transferToSpecialist = async (specialist) => {
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/voice-transfer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          specialist: specialist,
          user_role: 'client'
        }),
      });

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      const transferMessage = { 
        role: 'assistant', 
        content: data.response,
        model: 'voice-transfer',
        specialist: specialist
      };
      
      setMessages(prev => [...prev, transferMessage]);
    } catch (error) {
      console.error('Error transferring:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: `Transfer error: ${error.message}`,
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="voice-ai-container">
      <div className="voice-ai-header">
        <h2>🎤 Voice AI Assistant</h2>
        <div className="voice-status">
          <span className={`status-indicator ${voiceEnabled ? 'active' : 'inactive'}`}>
            {voiceEnabled ? '🎤 Voice Enabled' : '🔇 Voice Disabled'}
          </span>
          {capabilities && (
            <div className="capabilities">
              <span>Models: {capabilities.models.voice_ai?.length > 0 ? 'Cerebras' : 'None'}</span>
            </div>
          )}
        </div>
      </div>

      <div className="voice-ai-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content}
            </div>
            <div className="message-meta">
              {msg.model && <span className="model">Model: {msg.model}</span>}
              {msg.voice_enabled && <span className="voice">🎤 Voice</span>}
              {msg.specialist && <span className="specialist">Specialist: {msg.specialist}</span>}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="voice-ai-input">
        <div className="input-container">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={voiceEnabled ? "Type your message or use voice..." : "Type your message..."}
            rows="3"
            disabled={loading}
          />
          <button 
            onClick={sendMessage} 
            disabled={loading || !message.trim()}
            className="send-button"
          >
            {loading ? '⏳' : '📤'}
          </button>
        </div>
        
        {voiceEnabled && (
          <div className="specialist-buttons">
            <button 
              onClick={() => transferToSpecialist('technical')}
              disabled={loading}
              className="specialist-btn technical"
            >
              💻 Technical Support
            </button>
            <button 
              onClick={() => transferToSpecialist('pricing')}
              disabled={loading}
              className="specialist-btn pricing"
            >
              💰 Pricing Specialist
            </button>
            <button 
              onClick={() => transferToSpecialist('sales')}
              disabled={loading}
              className="specialist-btn sales"
            >
              🏷️ Sales Representative
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default VoiceAI;

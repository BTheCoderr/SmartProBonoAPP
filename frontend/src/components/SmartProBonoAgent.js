import React, { useState, useEffect, useRef } from 'react';
import { Card, Button, Input, Badge, Alert, Spinner, Tabs, Tab } from 'react-bootstrap';
import { 
  Send, 
  Bot, 
  User, 
  Case, 
  Document, 
  Search, 
  Bell, 
  Calendar,
  FileText,
  Shield,
  Activity,
  InfoCircle,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react';
import './SmartProBonoAgent.css';

const SmartProBonoAgent = ({ user, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [agentStatus, setAgentStatus] = useState('connecting');
  const [capabilities, setCapabilities] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  // Initialize agent
  useEffect(() => {
    initializeAgent();
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initializeAgent = async () => {
    try {
      // Check agent status
      const statusResponse = await fetch('/api/agent/status');
      const statusData = await statusResponse.json();
      setAgentStatus(statusData.status);

      // Get agent capabilities
      const capabilitiesResponse = await fetch('/api/agent/capabilities', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const capabilitiesData = await capabilitiesResponse.json();
      setCapabilities(capabilitiesData.capabilities);

      // Add welcome message
      if (messages.length === 0) {
        const welcomeMessage = {
          id: Date.now(),
          type: 'agent',
          content: `Hello! I'm your SmartProBono AI Agent. I can help you with:

• **Case Management**: Create cases, update status, search cases
• **Document Analysis**: Analyze legal documents for compliance and insights  
• **Legal Research**: Search case law and legal precedents
• **Client Management**: Add clients, schedule meetings, send notifications
• **Document Generation**: Create legal documents from templates

What would you like to do today?`,
          timestamp: new Date(),
          capabilities: capabilitiesData.capabilities
        };
        setMessages([welcomeMessage]);
      }
    } catch (error) {
      console.error('Error initializing agent:', error);
      setAgentStatus('error');
    }
  };

  const sendMessage = async (message = input) => {
    if (!message.trim() || isProcessing) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          message: message,
          context: { 
            user_role: user?.role || 'client',
            user_id: user?.id,
            conversation_id: conversationId
          },
          user_role: user?.role || 'client',
          verbose: true
        })
      });

      const data = await response.json();

      if (response.ok) {
        const agentMessage = {
          id: Date.now() + 1,
          type: 'agent',
          content: data.response,
          timestamp: new Date(),
          metadata: {
            service: data.agent_version,
            user_role: data.user_role
          }
        };

        setMessages(prev => [...prev, agentMessage]);
        
        if (!conversationId) {
          setConversationId(data.conversation_id);
        }
      } else {
        throw new Error(data.error || 'Failed to get response');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const executeQuickTask = async (task) => {
    setInput(task);
    await sendMessage(task);
  };

  const getMessageIcon = (type) => {
    switch (type) {
      case 'user': return <User size={16} />;
      case 'agent': return <Bot size={16} />;
      case 'function_call': return <Activity size={16} />;
      case 'error': return <AlertCircle size={16} />;
      default: return <Bot size={16} />;
    }
  };

  const getMessageClass = (type) => {
    switch (type) {
      case 'user': return 'user-message';
      case 'agent': return 'agent-message';
      case 'function_call': return 'function-message';
      case 'error': return 'error-message';
      default: return 'agent-message';
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const quickActions = [
    {
      title: 'Create Case',
      description: 'Start a new legal case',
      icon: <Case size={20} />,
      action: 'Create a new immigration case for John Smith with high priority'
    },
    {
      title: 'Analyze Document',
      description: 'Review legal documents',
      icon: <Document size={20} />,
      action: 'Analyze the contract document for compliance issues'
    },
    {
      title: 'Search Case Law',
      description: 'Research legal precedents',
      icon: <Search size={20} />,
      action: 'Search case law for contract dispute liability in federal jurisdiction'
    },
    {
      title: 'Send Notification',
      description: 'Notify clients or lawyers',
      icon: <Bell size={20} />,
      action: 'Send an email notification to client about case status update'
    }
  ];

  return (
    <div className="smartprobono-agent">
      {/* Header */}
      <div className="agent-header">
        <div className="agent-title">
          <Bot size={24} className="agent-icon" />
          <div>
            <h3>SmartProBono AI Agent</h3>
            <div className="agent-status">
              <Badge 
                variant={agentStatus === 'healthy' ? 'success' : 
                        agentStatus === 'mock_mode' ? 'warning' : 'danger'}
                className="status-badge"
              >
                {agentStatus === 'healthy' ? 'Online' : 
                 agentStatus === 'mock_mode' ? 'Demo Mode' : 'Offline'}
              </Badge>
              {user?.role && (
                <Badge variant="info" className="role-badge">
                  {user.role}
                </Badge>
              )}
            </div>
          </div>
        </div>
        {onClose && (
          <Button variant="outline-secondary" size="sm" onClick={onClose}>
            ×
          </Button>
        )}
      </div>

      {/* Tabs */}
      <Tabs 
        activeKey={activeTab} 
        onSelect={setActiveTab}
        className="agent-tabs"
      >
        <Tab eventKey="chat" title="Chat">
          <div className="chat-container">
            {/* Messages */}
            <div className="messages-container">
              {messages.map((message) => (
                <div 
                  key={message.id} 
                  className={`message ${getMessageClass(message.type)}`}
                >
                  <div className="message-header">
                    <div className="message-icon">
                      {getMessageIcon(message.type)}
                    </div>
                    <div className="message-meta">
                      <span className="message-type">
                        {message.type === 'user' ? 'You' : 
                         message.type === 'agent' ? 'SmartProBono Agent' :
                         message.type === 'function_call' ? 'Function Call' :
                         'System'}
                      </span>
                      <span className="message-time">
                        {formatTimestamp(message.timestamp)}
                      </span>
                    </div>
                  </div>
                  <div className="message-content">
                    {message.content}
                  </div>
                  {message.metadata && (
                    <div className="message-metadata">
                      <small className="text-muted">
                        Service: {message.metadata.service || 'SmartProBono Agent'}
                      </small>
                    </div>
                  )}
                </div>
              ))}
              
              {isProcessing && (
                <div className="message agent-message processing">
                  <div className="message-header">
                    <div className="message-icon">
                      <Bot size={16} />
                    </div>
                    <span className="message-type">SmartProBono Agent</span>
                  </div>
                  <div className="message-content">
                    <Spinner animation="border" size="sm" className="me-2" />
                    Processing your request...
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="input-area">
              <div className="input-group">
                <Input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Ask me to create a case, analyze documents, or research case law..."
                  disabled={isProcessing}
                  className="message-input"
                />
                <Button 
                  variant="primary" 
                  onClick={() => sendMessage()}
                  disabled={isProcessing || !input.trim()}
                  className="send-button"
                >
                  <Send size={16} />
                </Button>
              </div>
            </div>
          </div>
        </Tab>

        <Tab eventKey="actions" title="Quick Actions">
          <div className="quick-actions-container">
            <Alert variant="info" className="mb-3">
              <InfoCircle size={16} className="me-2" />
              Click any action below to quickly execute common legal tasks.
            </Alert>
            
            <div className="quick-actions-grid">
              {quickActions.map((action, index) => (
                <Card key={index} className="quick-action-card">
                  <Card.Body>
                    <div className="action-header">
                      <div className="action-icon">
                        {action.icon}
                      </div>
                      <h5 className="action-title">{action.title}</h5>
                    </div>
                    <p className="action-description">{action.description}</p>
                    <Button 
                      variant="outline-primary" 
                      size="sm"
                      onClick={() => executeQuickTask(action.action)}
                      disabled={isProcessing}
                      className="action-button"
                    >
                      Execute
                    </Button>
                  </Card.Body>
                </Card>
              ))}
            </div>
          </div>
        </Tab>

        <Tab eventKey="capabilities" title="Capabilities">
          <div className="capabilities-container">
            <Alert variant="success" className="mb-3">
              <CheckCircle size={16} className="me-2" />
              SmartProBono AI Agent is equipped with comprehensive legal platform capabilities.
            </Alert>
            
            {Object.entries(capabilities).map(([category, functions]) => (
              <Card key={category} className="capability-card mb-3">
                <Card.Header>
                  <h5 className="capability-category">
                    {category.replace('_', ' ').toUpperCase()}
                  </h5>
                </Card.Header>
                <Card.Body>
                  <div className="capability-functions">
                    {functions.map((func, index) => (
                      <Badge 
                        key={index} 
                        variant="secondary" 
                        className="function-badge me-2 mb-2"
                      >
                        {func.replace('_', ' ')}
                      </Badge>
                    ))}
                  </div>
                </Card.Body>
              </Card>
            ))}
          </div>
        </Tab>
      </Tabs>
    </div>
  );
};

export default SmartProBonoAgent;

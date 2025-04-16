# Legal AI Assistant Documentation

The Smart Pro Bono application includes an AI-powered legal assistant that provides automated responses to common legal questions, preliminary case analysis, and document drafting assistance. This document outlines the functionality and implementation of the Legal AI Assistant feature.

## Feature Overview

The Legal AI Assistant provides the following capabilities:

1. **Legal Question Answering**: Automated responses to common legal questions
2. **Document Analysis**: Review of legal documents with explanations in plain language
3. **Form Generation**: Assistance with filling out common legal forms
4. **Case Assessment**: Preliminary analysis of case viability and resource requirements
5. **Legal Research**: Access to relevant case law, statutes, and legal resources

## Implementation Details

### Architecture

The Legal AI Assistant is built using a combination of:

1. **Large Language Model (LLM)**: Powers the natural language understanding and generation
2. **Legal Knowledge Base**: Contains jurisdiction-specific legal information
3. **Document Processing**: For handling document uploads and analysis
4. **Vector Database**: For efficient retrieval of relevant legal information
5. **WebSocket Integration**: For real-time interaction with users

### Backend Components

```python
from flask import request, jsonify
from llm_service import LegalLLM
from document_processor import DocumentProcessor
from knowledge_base import LegalKnowledgeBase

# Initialize components
legal_llm = LegalLLM()
doc_processor = DocumentProcessor()
knowledge_base = LegalKnowledgeBase()

@app.route('/api/legal-ai/query', methods=['POST'])
@jwt_required()
def legal_ai_query():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    query = data.get('query')
    context = data.get('context', [])
    jurisdiction = data.get('jurisdiction', 'general')
    
    # Get relevant knowledge base entries
    kb_results = knowledge_base.search(query, jurisdiction=jurisdiction)
    
    # Generate response using LLM
    response = legal_llm.generate_response(
        query=query,
        context=context + kb_results,
        user_id=user_id
    )
    
    # Log the interaction for future training
    log_interaction(user_id, query, response)
    
    return jsonify({
        'response': response,
        'sources': kb_results.get_sources()
    })

@app.route('/api/legal-ai/document-analysis', methods=['POST'])
@jwt_required()
def analyze_document():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    
    # Process the document
    doc_text = doc_processor.extract_text(file)
    doc_type = doc_processor.identify_document_type(doc_text)
    
    # Analyze the document
    analysis = legal_llm.analyze_document(
        document_text=doc_text,
        document_type=doc_type,
        user_id=user_id
    )
    
    return jsonify({
        'analysis': analysis,
        'document_type': doc_type
    })

@socketio.on('legal_ai_message')
def handle_legal_ai_message(data):
    sid = get_sid()
    user_id = session.get('user_id')
    query = data.get('message')
    
    if not user_id or not query:
        return
    
    # Initial acknowledgment
    emit('legal_ai_typing', {'status': True}, room=sid)
    
    # Get response from Legal AI
    kb_results = knowledge_base.search(query)
    response = legal_llm.generate_response(
        query=query,
        context=kb_results,
        user_id=user_id
    )
    
    # Send response
    emit('legal_ai_typing', {'status': False}, room=sid)
    emit('legal_ai_response', {
        'message': response,
        'sources': kb_results.get_sources()
    }, room=sid)
    
    # Create notification for the user
    notification_service = get_notification_service()
    notification_data = create_legal_response_notification(
        user_id=user_id,
        query_id=str(uuid.uuid4()),
        preview_text=query[:50] + '...' if len(query) > 50 else query
    )
    notification_service.send_notification(user_id, notification_data)
```

### Frontend Implementation

#### Legal AI Chat Component

```jsx
import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';
import { useAuth } from '../contexts/AuthContext';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar
} from '@mui/material';
import {
  Send as SendIcon,
  AttachFile as AttachFileIcon,
  Save as SaveIcon
} from '@mui/icons-material';

const LegalAIChat = () => {
  const { user } = useAuth();
  const { emit, on, off, isConnected } = useWebSocket();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [files, setFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isAITyping, setIsAITyping] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);
  
  // Set up event listeners for WebSocket
  useEffect(() => {
    if (isConnected) {
      // AI typing indicator
      const handleAITyping = (data) => {
        setIsAITyping(data.status);
      };
      
      // AI response
      const handleAIResponse = (data) => {
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          sender: 'ai',
          message: data.message,
          timestamp: new Date().toISOString(),
          sources: data.sources || []
        }]);
        setIsLoading(false);
      };
      
      // Error handling
      const handleError = (data) => {
        setError(data.message);
        setIsLoading(false);
        setIsAITyping(false);
      };
      
      // Register listeners
      on('legal_ai_typing', handleAITyping);
      on('legal_ai_response', handleAIResponse);
      on('error', handleError);
      
      // Clean up
      return () => {
        off('legal_ai_typing', handleAITyping);
        off('legal_ai_response', handleAIResponse);
        off('error', handleError);
      };
    }
  }, [isConnected, on, off]);
  
  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Send message to AI
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim() === '' && files.length === 0) return;
    
    // Add user message to chat
    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      message: newMessage.trim(),
      timestamp: new Date().toISOString(),
      files: files.map(f => f.name)
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    // Send message to AI
    emit('legal_ai_message', {
      message: newMessage.trim(),
      files: files.length > 0
    });
    
    // Reset state
    setNewMessage('');
    setFiles([]);
  };
  
  // Handle file selection
  const handleFileSelect = (e) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };
  
  // Trigger file input click
  const handleFileButtonClick = () => {
    fileInputRef.current?.click();
  };
  
  // Handle file upload
  const handleFileUpload = async () => {
    if (files.length === 0) return;
    
    setIsLoading(true);
    
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    
    try {
      const response = await fetch('/api/legal-ai/document-analysis', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload files');
      }
      
      const data = await response.json();
      
      // Add AI message with document analysis
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        sender: 'ai',
        message: `Document Analysis: ${data.analysis}`,
        timestamp: new Date().toISOString(),
        documentType: data.document_type
      }]);
      
      setFiles([]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Export chat history
  const exportChatHistory = () => {
    const chatText = messages.map(msg => 
      `${new Date(msg.timestamp).toLocaleString()} - ${msg.sender === 'user' ? user.name : 'Legal AI'}: ${msg.message}`
    ).join('\n\n');
    
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `legal-ai-chat-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 2, 
          display: 'flex', 
          flexDirection: 'column',
          height: '100%',
          maxHeight: '80vh'
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h5">Legal AI Assistant</Typography>
          <IconButton onClick={exportChatHistory} title="Export Chat History">
            <SaveIcon />
          </IconButton>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        {/* Messages */}
        <List sx={{ flexGrow: 1, overflow: 'auto', mb: 2 }}>
          {messages.length === 0 && (
            <Typography variant="body1" sx={{ p: 2, textAlign: 'center', color: 'text.secondary' }}>
              Ask me any legal question or upload a document for analysis.
            </Typography>
          )}
          
          {messages.map(message => (
            <ListItem 
              key={message.id} 
              alignItems="flex-start"
              sx={{ 
                flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
                mb: 1
              }}
            >
              <ListItemAvatar>
                <Avatar 
                  src={message.sender === 'user' ? user.profile_pic : '/legal-ai-avatar.png'} 
                  alt={message.sender === 'user' ? user.name : 'Legal AI'}
                  sx={{ 
                    bgcolor: message.sender === 'ai' ? 'primary.main' : 'secondary.main'
                  }}
                >
                  {message.sender === 'user' ? user.name[0] : 'AI'}
                </Avatar>
              </ListItemAvatar>
              
              <ListItemText 
                primary={message.sender === 'user' ? user.name : 'Legal AI'}
                secondary={
                  <React.Fragment>
                    <Typography component="span" variant="body2" color="text.primary">
                      {message.message}
                    </Typography>
                    
                    {message.files && message.files.length > 0 && (
                      <Typography component="div" variant="body2" sx={{ mt: 1 }}>
                        Files: {message.files.join(', ')}
                      </Typography>
                    )}
                    
                    {message.sources && message.sources.length > 0 && (
                      <Typography component="div" variant="body2" sx={{ mt: 1 }}>
                        Sources:
                        <ul style={{ margin: '4px 0', paddingLeft: 20 }}>
                          {message.sources.map((source, idx) => (
                            <li key={idx}>{source}</li>
                          ))}
                        </ul>
                      </Typography>
                    )}
                    
                    <Typography variant="caption" color="text.secondary" display="block">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </Typography>
                  </React.Fragment>
                }
                sx={{ 
                  bgcolor: message.sender === 'user' ? 'grey.100' : 'info.light',
                  p: 1,
                  borderRadius: 2,
                  mx: 1
                }}
              />
            </ListItem>
          ))}
          
          {isAITyping && (
            <Box sx={{ display: 'flex', alignItems: 'center', p: 1 }}>
              <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>AI</Avatar>
              <Typography variant="body2">Legal AI is typing...</Typography>
            </Box>
          )}
          
          <div ref={messagesEndRef} />
        </List>
        
        {/* File attachments */}
        {files.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>Selected files:</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {files.map((file, index) => (
                <Chip
                  key={index}
                  label={file.name}
                  onDelete={() => setFiles(files.filter((_, i) => i !== index))}
                  variant="outlined"
                />
              ))}
            </Box>
            <Button 
              variant="contained" 
              onClick={handleFileUpload} 
              disabled={isLoading}
              sx={{ mt: 1 }}
              size="small"
            >
              Analyze Documents
            </Button>
          </Box>
        )}
        
        {/* Input box */}
        <form onSubmit={handleSendMessage}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <IconButton 
              onClick={handleFileButtonClick}
              disabled={isLoading}
            >
              <AttachFileIcon />
            </IconButton>
            
            <input
              type="file"
              multiple
              ref={fileInputRef}
              onChange={handleFileSelect}
              style={{ display: 'none' }}
              accept=".pdf,.doc,.docx,.txt"
            />
            
            <TextField
              fullWidth
              placeholder="Ask a legal question..."
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              disabled={isLoading}
              variant="outlined"
              multiline
              maxRows={3}
              sx={{ mr: 1 }}
            />
            
            <Button
              type="submit"
              variant="contained"
              color="primary"
              endIcon={isLoading ? <CircularProgress size={20} /> : <SendIcon />}
              disabled={isLoading || (newMessage.trim() === '' && files.length === 0)}
            >
              Send
            </Button>
          </Box>
        </form>
        
        {error && (
          <Typography color="error" variant="body2" sx={{ mt: 1 }}>
            Error: {error}
          </Typography>
        )}
      </Paper>
    </Box>
  );
};

export default LegalAIChat;
```

## Capabilities and Limitations

### What the Legal AI Can Do

1. **Answer common legal questions** in plain language
2. **Provide general legal information** based on a knowledge base of legal resources
3. **Analyze simple legal documents** and explain key terms and clauses
4. **Help draft basic legal documents** like demand letters or simple contracts
5. **Suggest relevant legal resources** for further research

### Limitations

1. **Not a substitute for legal advice**: The AI provides information, not personalized legal advice
2. **Jurisdiction limitations**: May not have complete information for all jurisdictions
3. **Complex case handling**: Not equipped to handle complex or nuanced legal scenarios
4. **No representation**: Cannot represent users in legal proceedings
5. **Legal updates**: May not reflect very recent changes in law or precedent

## User Guidelines

### Best Practices

1. **Be specific**: Provide clear, specific questions for better results
2. **Include context**: Mention relevant details like jurisdiction and case type
3. **Verify information**: Always verify AI responses with official legal sources
4. **Review documents**: Carefully review any AI-generated documents before use
5. **Seek professional advice**: Consult with a qualified attorney for complex matters

### Common Use Cases

1. **Understanding legal terminology**: Explaining legal jargon in plain language
2. **Initial case assessment**: Getting a basic understanding of legal situation
3. **Document review assistance**: Help understanding contracts or legal notices
4. **Form completion guidance**: Assistance with filling out standard legal forms
5. **Legal research starting points**: Finding relevant statutes or case law

## Safety and Ethical Guidelines

1. **Disclaimer**: All AI interactions include clear disclaimers about not providing legal advice
2. **Confidentiality**: User queries are handled confidentially but may be used for training
3. **Verification**: Responses are verified against reliable legal sources
4. **Bias mitigation**: Regular auditing to detect and address potential biases
5. **Referral to attorneys**: The system recommends professional legal help when appropriate

## Future Enhancements

1. **Enhanced document analysis** with more complex document understanding
2. **Multi-jurisdictional knowledge** expansion to cover more legal systems
3. **Personalized learning** to adapt to specific user needs and areas of interest
4. **Integration with legal databases** for more up-to-date research capabilities
5. **Multi-language support** for legal assistance in multiple languages

## Integration with Other Systems

The Legal AI Assistant integrates with several other components:

1. **Notification System**: Alerts users when AI responses are ready
2. **Document Management**: Connects with the document system for analysis
3. **Case Management**: Provides insights that can be attached to case records
4. **WebSocket System**: Delivers real-time responses and typing indicators

## Performance Monitoring

To ensure quality and reliability, the Legal AI system includes:

1. **Response quality tracking**: User feedback on AI responses
2. **Accuracy monitoring**: Regular audits against expert legal analysis
3. **Response time metrics**: Monitoring and optimizing response speed
4. **Usage analytics**: Tracking common questions and user patterns
5. **Error logging**: Capturing and addressing system failures 
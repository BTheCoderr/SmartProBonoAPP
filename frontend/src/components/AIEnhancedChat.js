import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, 
  TextField, 
  IconButton, 
  Avatar, 
  Typography,
  Divider,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { 
  Send as SendIcon, 
  SmartToy as AIIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  Feedback as FeedbackIcon
} from '@mui/icons-material';

const AIEnhancedChat = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [feedbackDialog, setFeedbackDialog] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [feedback, setFeedback] = useState('');
  const messagesEndRef = useRef(null);

  // AI Knowledge Base - This would normally be stored in a database
  const [knowledgeBase, setKnowledgeBase] = useState({
    legalTopics: {
      'eviction': {
        responses: [
          "Eviction laws vary by state, but generally landlords must provide proper notice before filing for eviction.",
          "If you're facing eviction, you may have rights to contest it in court. Document everything.",
          "Many states have tenant protection programs that can help with eviction defense."
        ],
        confidence: 0.8,
        feedback: { positive: 0, negative: 0 }
      },
      'small claims': {
        responses: [
          "Small claims court handles disputes under a certain dollar amount (varies by state).",
          "You can represent yourself in small claims court without an attorney.",
          "Gather all evidence, receipts, and documentation before filing your claim."
        ],
        confidence: 0.9,
        feedback: { positive: 0, negative: 0 }
      },
      'fee waiver': {
        responses: [
          "Fee waivers allow you to file court documents without paying fees if you meet income requirements.",
          "You'll need to provide proof of income and complete a fee waiver application.",
          "Each court has different requirements for fee waivers - check your local court's website."
        ],
        confidence: 0.85,
        feedback: { positive: 0, negative: 0 }
      }
    },
    generalResponses: [
      "I can help you with general legal information. For specific advice, please consult an attorney.",
      "That's a great question. Let me provide some general guidance on this topic.",
      "I understand your concern. Here's some information that might help you understand your options."
    ]
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize with welcome message
  useEffect(() => {
    setMessages([
      {
        id: 1,
        text: "Hello! I'm your AI Legal Assistant. I can help with general legal questions and provide guidance on common legal topics. How can I assist you today?",
        sender: 'ai',
        timestamp: new Date(),
        confidence: 0.9,
        topic: 'greeting'
      }
    ]);
  }, []);

  const analyzeMessage = (message) => {
    const lowerMessage = message.toLowerCase();
    
    // Simple keyword matching - in a real system, this would use NLP
    if (lowerMessage.includes('eviction') || lowerMessage.includes('evict')) {
      return { topic: 'eviction', confidence: 0.8 };
    } else if (lowerMessage.includes('small claims') || lowerMessage.includes('sue')) {
      return { topic: 'small claims', confidence: 0.8 };
    } else if (lowerMessage.includes('fee waiver') || lowerMessage.includes('court fees')) {
      return { topic: 'fee waiver', confidence: 0.8 };
    } else if (lowerMessage.includes('legal') || lowerMessage.includes('law')) {
      return { topic: 'general', confidence: 0.6 };
    }
    
    return { topic: 'general', confidence: 0.5 };
  };

  const generateResponse = (userMessage, analysis) => {
    const { topic, confidence } = analysis;
    
    if (knowledgeBase.legalTopics[topic]) {
      const topicData = knowledgeBase.legalTopics[topic];
      const responses = topicData.responses;
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      
      return {
        text: randomResponse,
        confidence: confidence * topicData.confidence,
        topic: topic,
        source: 'knowledge_base'
      };
    } else {
      const generalResponses = knowledgeBase.generalResponses;
      const randomResponse = generalResponses[Math.floor(Math.random() * generalResponses.length)];
      
      return {
        text: randomResponse,
        confidence: confidence * 0.7,
        topic: 'general',
        source: 'general'
      };
    }
  };

  const handleSendMessage = () => {
    if (!newMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: newMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setNewMessage('');
    setIsTyping(true);

    // Simulate AI thinking time
    setTimeout(() => {
      const analysis = analyzeMessage(newMessage);
      const aiResponse = generateResponse(newMessage, analysis);
      
      const aiMessage = {
        id: messages.length + 2,
        text: aiResponse.text,
        sender: 'ai',
        timestamp: new Date(),
        confidence: aiResponse.confidence,
        topic: aiResponse.topic,
        source: aiResponse.source
      };
      
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500 + Math.random() * 1000); // Random delay to simulate thinking
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFeedback = (messageId, isPositive) => {
    setSelectedMessage(messageId);
    setFeedbackDialog(true);
  };

  const submitFeedback = () => {
    if (selectedMessage && feedback) {
      // In a real system, this would send feedback to improve the AI
      console.log('Feedback submitted:', {
        messageId: selectedMessage,
        feedback: feedback,
        timestamp: new Date()
      });
      
      // Update knowledge base confidence based on feedback
      const message = messages.find(m => m.id === selectedMessage);
      if (message && message.topic && knowledgeBase.legalTopics[message.topic]) {
        const topicData = knowledgeBase.legalTopics[message.topic];
        if (feedback === 'positive') {
          topicData.feedback.positive += 1;
          topicData.confidence = Math.min(1.0, topicData.confidence + 0.05);
        } else {
          topicData.feedback.negative += 1;
          topicData.confidence = Math.max(0.1, topicData.confidence - 0.05);
        }
        setKnowledgeBase({...knowledgeBase});
      }
      
      setFeedbackDialog(false);
      setFeedback('');
      setSelectedMessage(null);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Chat Messages */}
      <Box
        sx={{
          flex: 1,
          overflow: 'auto',
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          gap: 2
        }}
      >
        {messages.map((message) => (
          <Box
            key={message.id}
            sx={{
              display: 'flex',
              justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
              alignItems: 'flex-start',
              gap: 1
            }}
          >
            {message.sender === 'ai' && (
              <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                <AIIcon sx={{ fontSize: 18 }} />
              </Avatar>
            )}
            <Box
              sx={{
                maxWidth: '70%',
                p: 2,
                borderRadius: 2,
                bgcolor: message.sender === 'user' ? 'primary.main' : 'grey.100',
                color: message.sender === 'user' ? 'white' : 'text.primary'
              }}
            >
              <Typography variant="body1">
                {message.text}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                <Typography
                  variant="caption"
                  sx={{
                    opacity: 0.7,
                    fontSize: '0.75rem'
                  }}
                >
                  {formatTime(message.timestamp)}
                </Typography>
                {message.sender === 'ai' && message.confidence && (
                  <Chip
                    label={`${Math.round(message.confidence * 100)}% confident`}
                    size="small"
                    color={getConfidenceColor(message.confidence)}
                    sx={{ height: 16, fontSize: '0.7rem' }}
                  />
                )}
              </Box>
              {message.sender === 'ai' && (
                <Box sx={{ display: 'flex', gap: 0.5, mt: 1 }}>
                  <IconButton
                    size="small"
                    onClick={() => handleFeedback(message.id, true)}
                    sx={{ p: 0.5 }}
                  >
                    <ThumbUpIcon sx={{ fontSize: 16 }} />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleFeedback(message.id, false)}
                    sx={{ p: 0.5 }}
                  >
                    <ThumbDownIcon sx={{ fontSize: 16 }} />
                  </IconButton>
                </Box>
              )}
            </Box>
            {message.sender === 'user' && (
              <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32, fontSize: '0.875rem' }}>
                U
              </Avatar>
            )}
          </Box>
        ))}
        
        {isTyping && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
              <AIIcon sx={{ fontSize: 18 }} />
            </Avatar>
            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                bgcolor: 'grey.100',
                display: 'flex',
                alignItems: 'center',
                gap: 1
              }}
            >
              <Typography variant="body2" color="text.secondary">
                AI is thinking
              </Typography>
              <Box sx={{ display: 'flex', gap: 0.5 }}>
                {[0, 1, 2].map((i) => (
                  <Box
                    key={i}
                    sx={{
                      width: 4,
                      height: 4,
                      borderRadius: '50%',
                      bgcolor: 'text.secondary',
                      animation: 'pulse 1.4s ease-in-out infinite both',
                      animationDelay: `${i * 0.2}s`
                    }}
                  />
                ))}
              </Box>
            </Box>
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>

      <Divider />
      
      {/* Message Input */}
      <Box sx={{ p: 2, display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          placeholder="Ask me about legal topics..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          variant="outlined"
          size="small"
          multiline
          maxRows={3}
        />
        <IconButton
          color="primary"
          onClick={handleSendMessage}
          disabled={!newMessage.trim()}
          sx={{ alignSelf: 'flex-end' }}
        >
          <SendIcon />
        </IconButton>
      </Box>

      {/* Feedback Dialog */}
      <Dialog open={feedbackDialog} onClose={() => setFeedbackDialog(false)}>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <FeedbackIcon />
            Provide Feedback
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Your feedback helps improve the AI's responses. Please tell us how we can do better:
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={3}
            placeholder="What could be improved about this response?"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFeedbackDialog(false)}>Cancel</Button>
          <Button onClick={submitFeedback} variant="contained" disabled={!feedback.trim()}>
            Submit Feedback
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AIEnhancedChat;

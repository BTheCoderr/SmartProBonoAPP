import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
  Container,
  Chip,
  IconButton,
  Tooltip,
  Avatar,
  Divider
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import { aiAgents, routeToAgent } from '../lib/aiAgents';

const ImprovedLegalAIChat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: input,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Route to appropriate agent
      const agentType = routeToAgent(input, { conversationLength: messages.length });
      const agent = aiAgents[agentType];
      setCurrentAgent(agent);

      // Simulate API call (replace with actual Supabase call)
      const response = await simulateAIResponse(input, agent);
      
      const aiMessage = {
        id: Date.now() + 1,
        text: response,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        agent: agent.name,
        agentType: agentType
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm sorry, I encountered an error. Please try again.",
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Simulate AI response based on agent type
  const simulateAIResponse = async (message, agent) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

    const lowerMessage = message.toLowerCase();

    // Greeting Agent - Keep it simple!
    if (agent.name === "Greeting Agent") {
      if (lowerMessage.match(/^(hello|hi|hey|good morning|good afternoon|good evening)$/)) {
        return "Hello! I'm your AI legal assistant. I can help with compliance, business law, document analysis, and more. What specific legal question can I help you with today?";
      }
      if (lowerMessage.includes('what can you do')) {
        return "I can help with:\n• Legal compliance (GDPR, SOC 2, privacy policies)\n• Business law (incorporation, fundraising, contracts)\n• Document analysis and generation\n• Expert referrals for complex matters\n\nWhat would you like to explore?";
      }
      return "I'm here to help with your legal questions! What specific area would you like assistance with?";
    }

    // Compliance Agent
    if (agent.name === "Compliance Agent") {
      if (lowerMessage.includes('gdpr')) {
        return "**GDPR Compliance Overview:**\n\nGDPR applies if you process personal data of EU residents. Key requirements:\n\n1. **Legal Basis**: Identify lawful basis (consent, contract, legitimate interest)\n2. **Privacy Policy**: Clear, accessible policy explaining data use\n3. **Data Rights**: Implement processes for access, rectification, erasure\n4. **Breach Notification**: Report breaches within 72 hours\n5. **Privacy by Design**: Build data protection into systems\n\n**Risk**: Fines up to €20M or 4% of annual revenue\n\nWould you like me to help you create a compliance checklist for your specific situation?";
      }
      if (lowerMessage.includes('soc 2')) {
        return "**SOC 2 Compliance Guide:**\n\nSOC 2 is essential for enterprise sales and customer trust.\n\n**Five Trust Principles:**\n1. **Security**: Protection against unauthorized access\n2. **Availability**: System operational availability\n3. **Processing Integrity**: System processing completeness/accuracy\n4. **Confidentiality**: Information designated confidential is protected\n5. **Privacy**: Personal information collection/use/disposal\n\n**Implementation Timeline:**\n• Type I: 3-6 months\n• Type II: 12+ months\n\n**Investment:** $15k-$50k for initial compliance\n\nReady to start your SOC 2 journey? I can help create your control framework.";
      }
      return "I specialize in compliance matters including GDPR, SOC 2, privacy policies, and regulatory requirements. What specific compliance question do you have?";
    }

    // Business Agent
    if (agent.name === "Business Agent") {
      if (lowerMessage.includes('incorporat') || lowerMessage.includes('llc') || lowerMessage.includes('corporation')) {
        return "**Entity Formation Guide:**\n\n**Delaware C-Corporation** (Recommended for VC-backed startups):\n✅ Pros: Investor-friendly, stock options, global recognition\n❌ Cons: Double taxation, more compliance\n\n**LLC** (Good for bootstrapped/small teams):\n✅ Pros: Tax flexibility, simple structure, liability protection\n❌ Cons: Harder to raise VC funding, no stock options\n\n**Formation Checklist:**\n1. Choose state (Delaware for corp, home state for LLC)\n2. Reserve name\n3. File articles\n4. Get EIN\n5. Open business bank account\n6. Create operating agreement\n7. Set up equity structure\n\n**Costs:** Delaware Corp: ~$400, LLC: $50-$500\n\nNeed help choosing the right structure for your startup?";
      }
      if (lowerMessage.includes('fundraising')) {
        return "**Startup Fundraising Legal Framework:**\n\n**Funding Stages:**\n• **Pre-Seed/F&F**: SAFE, convertible notes ($25K-$250K)\n• **Seed**: Series Seed docs or equity ($250K-$2M)\n• **Series A+**: Full equity rounds with extensive docs ($2M+)\n\n**Essential Legal Documents:**\n1. Term Sheet (non-binding overview)\n2. Stock Purchase Agreement (main contract)\n3. Investors' Rights Agreement\n4. Voting Agreement\n5. Right of First Refusal\n6. Drag-Along/Tag-Along rights\n\n**Key Considerations:**\n• Anti-dilution provisions\n• Liquidation preferences\n• Board composition\n• Option pool sizing\n\n**Legal Costs:** Seed: $5K-$15K, Series A: $15K-$40K\n\nReady to review your term sheet or generate fundraising docs?";
      }
      return "I specialize in business law including entity formation, fundraising, employment agreements, and intellectual property. What business legal question can I help you with?";
    }

    // Document Agent
    if (agent.name === "Document Agent") {
      return "I specialize in document analysis and generation. I can help you:\n\n• **Analyze Documents**: Review contracts, agreements, legal forms\n• **Generate Documents**: Create privacy policies, terms of service, contracts\n• **Explain Legal Language**: Break down complex legal terms\n• **Identify Key Terms**: Highlight important clauses and implications\n\nDo you have a document you'd like me to analyze, or would you like me to help generate a specific legal document?";
    }

    // Expert Agent
    if (agent.name === "Expert Agent") {
      return "For complex legal matters, I recommend connecting with a qualified attorney. I can help you:\n\n• **Identify the Right Expert**: Match you with attorneys specializing in your area\n• **Prepare for Consultation**: Help you organize your questions and documents\n• **Understand Legal Issues**: Break down complex legal concepts\n• **Find Pro Bono Resources**: Connect you with legal aid organizations\n\nWhat type of legal expert are you looking for? I can help match you with the right professional.";
    }

    // Default response
    return "I'm here to help with your legal questions. Could you be more specific about what you need assistance with?";
  };

  const getAgentColor = (agentType) => {
    const colors = {
      greeting: 'primary',
      compliance: 'success',
      business: 'warning',
      document: 'info',
      expert: 'error'
    };
    return colors[agentType] || 'default';
  };

  const getAgentIcon = (agentType) => {
    const icons = {
      greeting: '👋',
      compliance: '🛡️',
      business: '💼',
      document: '📄',
      expert: '⚖️'
    };
    return icons[agentType] || '🤖';
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ height: '80vh', display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Box sx={{ mb: 2, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
            AI Legal Assistant
          </Typography>
          {currentAgent && (
            <Chip
              icon={<span>{getAgentIcon(currentAgent.agentType)}</span>}
              label={`${currentAgent.name} is helping you`}
              color={getAgentColor(currentAgent.agentType)}
              variant="outlined"
              sx={{ mb: 2 }}
            />
          )}
        </Box>

        {/* Messages */}
        <Paper 
          elevation={2} 
          sx={{ 
            flex: 1, 
            overflow: 'auto', 
            p: 2, 
            mb: 2,
            backgroundColor: '#fafafa'
          }}
        >
          {messages.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <SmartToyIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Welcome to SmartProBono AI Assistant
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                I can help with legal compliance, business law, document analysis, and more.
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Chip label="GDPR Compliance" onClick={() => setInput("What is GDPR compliance?")} />
                <Chip label="Entity Formation" onClick={() => setInput("Should I form an LLC or Corporation?")} />
                <Chip label="Privacy Policy" onClick={() => setInput("Help me create a privacy policy")} />
                <Chip label="Document Review" onClick={() => setInput("I need help analyzing a contract")} />
              </Box>
            </Box>
          ) : (
            <List>
              {messages.map((message) => (
                <ListItem key={message.id} sx={{ flexDirection: 'column', alignItems: 'flex-start', py: 2 }}>
                  <Box sx={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    mb: 1,
                    alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start'
                  }}>
                    <Avatar sx={{ 
                      width: 32, 
                      height: 32, 
                      mr: 1,
                      bgcolor: message.sender === 'user' ? 'primary.main' : 'secondary.main'
                    }}>
                      {message.sender === 'user' ? <PersonIcon /> : <SmartToyIcon />}
                    </Avatar>
                    <Typography variant="caption" color="text.secondary">
                      {message.sender === 'user' ? 'You' : (message.agent || 'AI Assistant')}
                    </Typography>
                  </Box>
                  <Paper
                    elevation={1}
                    sx={{
                      p: 2,
                      maxWidth: '80%',
                      backgroundColor: message.sender === 'user' ? 'primary.light' : 'white',
                      color: message.sender === 'user' ? 'primary.contrastText' : 'text.primary',
                      alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start'
                    }}
                  >
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                      {message.text}
                    </Typography>
                    {message.isError && (
                      <Alert severity="error" sx={{ mt: 1 }}>
                        There was an error processing your request.
                      </Alert>
                    )}
                  </Paper>
                </ListItem>
              ))}
              {isLoading && (
                <ListItem sx={{ justifyContent: 'center' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <CircularProgress size={24} />
                    <Typography variant="body2" color="text.secondary">
                      AI is thinking...
                    </Typography>
                  </Box>
                </ListItem>
              )}
              <div ref={messagesEndRef} />
            </List>
          )}
        </Paper>

        {/* Input */}
        <Paper elevation={2} sx={{ p: 2 }}>
          <form onSubmit={handleSubmit}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me about legal compliance, business law, documents, or anything else..."
                disabled={isLoading}
                multiline
                maxRows={3}
                variant="outlined"
                size="small"
              />
              <Button
                type="submit"
                variant="contained"
                disabled={!input.trim() || isLoading}
                sx={{ minWidth: 'auto', px: 2 }}
              >
                <SendIcon />
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default ImprovedLegalAIChat;

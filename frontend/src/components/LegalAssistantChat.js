import React, { useState, useEffect, useRef } from 'react';
import {
  Box, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Link,
  IconButton,
  Tooltip,
  Grid,
  Card,
  CardContent
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import InfoIcon from '@mui/icons-material/Info';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import CloseIcon from '@mui/icons-material/Close';
import { styled } from '@mui/material/styles';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

// Styled components
const ChatContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  height: 'calc(100vh - 200px)',
  display: 'flex',
  flexDirection: 'column',
  overflow: 'hidden',
  border: `1px solid ${theme.palette.divider}`,
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[3]
}));

const MessageList = styled(Box)(({ theme }) => ({
  flexGrow: 1,
  overflowY: 'auto',
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  '&::-webkit-scrollbar': {
    width: '0.4em',
  },
  '&::-webkit-scrollbar-track': {
    boxShadow: 'inset 0 0 6px rgba(0,0,0,0.1)',
  },
  '&::-webkit-scrollbar-thumb': {
    backgroundColor: 'rgba(0,0,0,.2)',
    borderRadius: '4px',
  }
}));

const UserMessage = styled(Box)(({ theme }) => ({
  background: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  padding: theme.spacing(1.5),
  borderRadius: '18px 18px 0 18px',
  maxWidth: '80%',
  alignSelf: 'flex-end',
  marginBottom: theme.spacing(1),
  wordBreak: 'break-word'
}));

const BotMessage = styled(Box)(({ theme }) => ({
  background: theme.palette.background.default,
  color: theme.palette.text.primary,
  padding: theme.spacing(1.5),
  borderRadius: '18px 18px 18px 0',
  maxWidth: '80%',
  alignSelf: 'flex-start',
  marginBottom: theme.spacing(1),
  wordBreak: 'break-word',
  border: `1px solid ${theme.palette.divider}`
}));

const CitationChip = styled(Chip)(({ theme }) => ({
  margin: theme.spacing(0.5),
  cursor: 'pointer'
}));

const MessageInputContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  padding: theme.spacing(1),
  borderTop: `1px solid ${theme.palette.divider}`,
  background: theme.palette.background.paper
}));

const ResourceCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(1),
  '&:hover': {
    boxShadow: theme.shadows[4],
    transform: 'translateY(-2px)',
    transition: 'transform 0.3s ease-in-out'
  }
}));

const LegalAssistantChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [jurisdictions, setJurisdictions] = useState([]);
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('');
  const [domains, setDomains] = useState([]);
  const [detectedDomain, setDetectedDomain] = useState('');
  const [availableModels, setAvailableModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [resources, setResources] = useState([]);
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [citationDetails, setCitationDetails] = useState(null);
  
  const messagesEndRef = useRef(null);
  const messageListRef = useRef(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Fetch jurisdictions and domains on component mount
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        // Fetch jurisdictions
        const jurisdictionsResponse = await axios.get('/api/legal/jurisdictions');
        setJurisdictions(jurisdictionsResponse.data.jurisdictions || []);
        setSelectedJurisdiction(jurisdictionsResponse.data.default || '');

        // Fetch legal domains
        const domainsResponse = await axios.get('/api/legal/domains');
        setDomains(domainsResponse.data.domains || []);

        // Fetch available models
        const modelsResponse = await axios.get('/api/legal/models');
        setAvailableModels(modelsResponse.data.models || []);
        setSelectedModel(modelsResponse.data.default || '');
      } catch (error) {
        console.error('Error fetching initial data:', error);
      }
    };

    fetchInitialData();
  }, []);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      sender: 'user',
      text: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      // Analyze the message to detect domain
      const analysisResponse = await axios.post('/api/legal/analyze', {
        query: userMessage.text
      });

      const detectedDomain = analysisResponse.data.domain || 'general';
      setDetectedDomain(detectedDomain);

      // Get legal assistant response
      const response = await axios.post('/api/legal/chat', {
        message: userMessage.text,
        jurisdiction: selectedJurisdiction,
        model_id: selectedModel
      });

      // Update resources
      setResources(response.data.resources || []);

      const botMessage = {
        sender: 'assistant',
        text: response.data.response,
        citations: response.data.citations || [],
        domain: response.data.domain,
        jurisdiction: response.data.jurisdiction,
        model_used: response.data.model_used,
        timestamp: response.data.timestamp
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        sender: 'assistant',
        text: 'I'm sorry, I encountered an error processing your request. Please try again later.',
        error: true,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleJurisdictionChange = (e) => {
    setSelectedJurisdiction(e.target.value);
  };
  
  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
  };

  const handleCitationClick = async (citation) => {
    setSelectedCitation(citation);
    
    try {
      // Fetch citation details if there's an ID
      if (citation.id) {
        const response = await axios.get(`/api/legal/citations/${citation.id}`);
        setCitationDetails(response.data);
      } else {
        setCitationDetails(citation);
      }
    } catch (error) {
      console.error('Error fetching citation details:', error);
      setCitationDetails({
        ...citation,
        error: 'Unable to fetch detailed information'
      });
    }
  };

  const handleCloseCitationDetails = () => {
    setSelectedCitation(null);
    setCitationDetails(null);
  };

  const renderMessage = (message, index) => {
    if (message.sender === 'user') {
      return (
        <Box display="flex" justifyContent="flex-end" mb={2} key={index}>
          <UserMessage>
            <Typography variant="body1">{message.text}</Typography>
          </UserMessage>
        </Box>
      );
    } else {
      return (
        <Box display="flex" justifyContent="flex-start" flexDirection="column" mb={2} key={index}>
          <BotMessage>
            <ReactMarkdown>{message.text}</ReactMarkdown>
            
            {message.citations && message.citations.length > 0 && (
              <Box mt={1}>
                <Typography variant="subtitle2" color="textSecondary">
                  Citations:
                </Typography>
                <Box display="flex" flexWrap="wrap">
                  {message.citations.map((citation, citIndex) => (
                    <CitationChip
                      key={citIndex}
                      label={citation.text.length > 40 ? `${citation.text.substring(0, 40)}...` : citation.text}
                      onClick={() => handleCitationClick(citation)}
                      size="small"
                      icon={<MenuBookIcon />}
                    />
                  ))}
                </Box>
              </Box>
            )}
            
            {message.jurisdiction && (
              <Box mt={1} display="flex" alignItems="center">
                <LocationOnIcon fontSize="small" color="action" />
                <Typography variant="caption" color="textSecondary" ml={0.5}>
                  Jurisdiction: {message.jurisdiction}
                </Typography>
              </Box>
            )}
            
            {message.model_used && (
              <Box mt={0.5}>
                <Typography variant="caption" color="textSecondary">
                  Model: {message.model_used}
                </Typography>
              </Box>
            )}
          </BotMessage>
        </Box>
      );
    }
  };

  const renderCitationDetails = () => {
    if (!selectedCitation || !citationDetails) return null;
    
    return (
      <Paper 
        elevation={3} 
        sx={{ 
          position: 'absolute', 
          bottom: '80px', 
          right: '20px', 
          width: '400px',
          maxHeight: '400px',
          overflow: 'auto',
          zIndex: 1000,
          p: 2 
        }}
      >
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h6">Citation Details</Typography>
          <IconButton size="small" onClick={handleCloseCitationDetails}>
            <CloseIcon />
          </IconButton>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        {citationDetails.error ? (
          <Typography color="error">{citationDetails.error}</Typography>
        ) : (
          <>
            <Typography variant="subtitle1">{citationDetails.text}</Typography>
            
            <Box mt={2}>
              <Typography variant="subtitle2">Type:</Typography>
              <Typography variant="body2">{citationDetails.type || 'Unknown'}</Typography>
            </Box>
            
            {citationDetails.source && (
              <Box mt={1}>
                <Typography variant="subtitle2">Source:</Typography>
                <Typography variant="body2">{citationDetails.source}</Typography>
              </Box>
            )}
            
            {citationDetails.jurisdiction && (
              <Box mt={1}>
                <Typography variant="subtitle2">Jurisdiction:</Typography>
                <Typography variant="body2">{citationDetails.jurisdiction}</Typography>
              </Box>
            )}
            
            {citationDetails.url && (
              <Box mt={2}>
                <Button 
                  variant="outlined" 
                  size="small" 
                  component="a" 
                  href={citationDetails.url} 
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View Source
                </Button>
              </Box>
            )}
          </>
        )}
      </Paper>
    );
  };

  const renderResources = () => {
    if (!resources || resources.length === 0) return null;
    
    return (
      <Box mt={2}>
        <Typography variant="h6" gutterBottom>
          Helpful Resources
        </Typography>
        <Grid container spacing={2}>
          {resources.map((resource, index) => (
            <Grid item xs={12} md={6} key={index}>
              <ResourceCard>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    {resource.name}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    {resource.description}
                  </Typography>
                  <Button 
                    variant="outlined" 
                    size="small" 
                    component="a" 
                    href={resource.url} 
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Visit Resource
                  </Button>
                </CardContent>
              </ResourceCard>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Legal Assistant
        <Tooltip title="This AI legal assistant provides information about legal matters across various domains and jurisdictions. It can answer questions about tenant rights, employment law, and more.">
          <IconButton size="small" sx={{ ml: 1 }}>
            <InfoIcon />
          </IconButton>
        </Tooltip>
      </Typography>
      
      <Box mb={3}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth variant="outlined" size="small">
              <InputLabel id="jurisdiction-select-label">Jurisdiction</InputLabel>
              <Select
                labelId="jurisdiction-select-label"
                id="jurisdiction-select"
                value={selectedJurisdiction}
                onChange={handleJurisdictionChange}
                label="Jurisdiction"
              >
                {jurisdictions.map((jurisdiction) => (
                  <MenuItem key={jurisdiction.id} value={jurisdiction.id}>
                    {jurisdiction.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <FormControl fullWidth variant="outlined" size="small">
              <InputLabel id="model-select-label">AI Model</InputLabel>
              <Select
                labelId="model-select-label"
                id="model-select"
                value={selectedModel}
                onChange={handleModelChange}
                label="AI Model"
              >
                {availableModels.map((model) => (
                  <MenuItem key={model.id} value={model.id}>
                    {model.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>
      
      {detectedDomain && (
        <Box mb={2} display="flex" alignItems="center">
          <Typography variant="body2" mr={1}>
            Detected domain:
          </Typography>
          <Chip 
            label={detectedDomain.replace('_', ' ').toUpperCase()} 
            size="small" 
            color="primary" 
            variant="outlined" 
          />
        </Box>
      )}
      
      <ChatContainer>
        <MessageList ref={messageListRef}>
          {messages.length === 0 ? (
            <Box 
              display="flex" 
              justifyContent="center" 
              alignItems="center" 
              height="100%"
              flexDirection="column"
              textAlign="center"
            >
              <Typography variant="h6" color="textSecondary" gutterBottom>
                Welcome to the Legal Assistant
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                Ask me anything about legal rights, procedures, or information.
              </Typography>
              <Box mt={2}>
                <Typography variant="subtitle2" gutterBottom>
                  Example questions:
                </Typography>
                <List>
                  <ListItem button onClick={() => setInputValue("What are my rights as a tenant in California?")}>
                    <ListItemText primary="What are my rights as a tenant in California?" />
                  </ListItem>
                  <ListItem button onClick={() => setInputValue("How do I file for unemployment benefits?")}>
                    <ListItemText primary="How do I file for unemployment benefits?" />
                  </ListItem>
                  <ListItem button onClick={() => setInputValue("What is the process for applying for asylum?")}>
                    <ListItemText primary="What is the process for applying for asylum?" />
                  </ListItem>
                </List>
              </Box>
            </Box>
          ) : (
            <>
              {messages.map(renderMessage)}
              <div ref={messagesEndRef} />
            </>
          )}
        </MessageList>
        
        <MessageInputContainer>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your legal question..."
            value={inputValue}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            multiline
            maxRows={3}
            disabled={loading}
            size="small"
            sx={{ mr: 1 }}
          />
          <Button 
            variant="contained" 
            color="primary" 
            endIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
            onClick={handleSendMessage}
            disabled={loading || !inputValue.trim()}
          >
            Send
          </Button>
        </MessageInputContainer>
      </ChatContainer>
      
      {renderResources()}
      {renderCitationDetails()}
    </Box>
  );
};

export default LegalAssistantChat; 
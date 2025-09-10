import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Send as SendIcon,
  Upload as UploadIcon,
  Description as DocumentIcon,
  Chat as ChatIcon,
  ExpandMore as ExpandMoreIcon
} from '@mui/icons-material';

const UnifiedLegalAssistant = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  
  // Chat state
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  
  // Document state
  const [selectedFile, setSelectedFile] = useState(null);
  const [documentType, setDocumentType] = useState('generic');
  
  // Legal analysis state
  const [legalQuery, setLegalQuery] = useState('');
  const [jurisdiction, setJurisdiction] = useState('ri');
  const [caseType, setCaseType] = useState('');

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setError(null);
    setResult(null);
  };

  // ============================================================================
  // CHAT FUNCTIONALITY
  // ============================================================================
  
  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/v1/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: chatMessage,
          task_type: 'chat',
          conversation_id: conversationId,
          history: chatHistory,
          model: 'auto'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        const newMessage = {
          id: Date.now(),
          text: data.text,
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString(),
          model: data.model
        };
        
        setChatHistory(prev => [...prev, 
          { id: Date.now() - 1, text: chatMessage, sender: 'user', timestamp: new Date().toLocaleTimeString() },
          newMessage
        ]);
        
        if (!conversationId) {
          setConversationId(data.id);
        }
        
        setChatMessage('');
      } else {
        setError(data.error || 'Chat failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  // ============================================================================
  // DOCUMENT FUNCTIONALITY
  // ============================================================================
  
  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('document_type', documentType);

      const response = await fetch('/api/v1/documents/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      
      if (data.success) {
        setResult({
          type: 'document',
          data: data.analysis,
          documentType: data.document_type
        });
      } else {
        setError(data.error || 'Document analysis failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to analyze document');
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  // ============================================================================
  // LEGAL ANALYSIS FUNCTIONALITY
  // ============================================================================
  
  const handleLegalAnalysis = async (e) => {
    e.preventDefault();
    if (!legalQuery.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/v1/legal/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: legalQuery,
          jurisdiction: jurisdiction,
          case_type: caseType
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setResult({
          type: 'legal',
          data: data.analysis,
          disclaimers: data.disclaimers,
          warnings: data.warnings,
          recommendations: data.recommendations,
          jurisdiction: data.jurisdiction
        });
      } else {
        setError(data.error || 'Legal analysis failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to analyze legal question');
    } finally {
      setLoading(false);
    }
  };

  // ============================================================================
  // RENDER FUNCTIONS
  // ============================================================================
  
  const renderChatTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        AI Legal Chat Assistant
      </Typography>
      
      {/* Chat History */}
      <Paper sx={{ height: 400, overflow: 'auto', mb: 2, p: 2 }}>
        {chatHistory.length === 0 ? (
          <Typography color="text.secondary" align="center">
            Start a conversation with the AI legal assistant
          </Typography>
        ) : (
          chatHistory.map((message) => (
            <Box key={message.id} sx={{ mb: 2 }}>
              <Box sx={{ 
                display: 'flex', 
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                mb: 1
              }}>
                <Chip 
                  label={message.sender === 'user' ? 'You' : 'AI Assistant'} 
                  color={message.sender === 'user' ? 'primary' : 'secondary'}
                  size="small"
                />
                {message.model && (
                  <Chip label={message.model} size="small" sx={{ ml: 1 }} />
                )}
              </Box>
              <Paper sx={{ 
                p: 2, 
                bgcolor: message.sender === 'user' ? 'primary.light' : 'grey.100',
                maxWidth: '80%',
                ml: message.sender === 'user' ? 'auto' : 0
              }}>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                  {message.text}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {message.timestamp}
                </Typography>
              </Paper>
            </Box>
          ))
        )}
      </Paper>
      
      {/* Chat Input */}
      <Box component="form" onSubmit={handleChatSubmit} sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          value={chatMessage}
          onChange={(e) => setChatMessage(e.target.value)}
          placeholder="Ask a legal question..."
          disabled={loading}
        />
        <Button
          type="submit"
          variant="contained"
          endIcon={<SendIcon />}
          disabled={loading || !chatMessage.trim()}
        >
          {loading ? <CircularProgress size={20} /> : 'Send'}
        </Button>
      </Box>
    </Box>
  );

  const renderDocumentTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Document Analysis
      </Typography>
      
      <Box component="form" onSubmit={handleFileUpload} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          type="file"
          onChange={handleFileChange}
          inputProps={{ accept: '.pdf,.doc,.docx,.txt' }}
          disabled={loading}
        />
        
        <FormControl fullWidth>
          <InputLabel>Document Type</InputLabel>
          <Select
            value={documentType}
            onChange={(e) => setDocumentType(e.target.value)}
            label="Document Type"
            disabled={loading}
          >
            <MenuItem value="generic">Generic</MenuItem>
            <MenuItem value="contract">Contract</MenuItem>
            <MenuItem value="lease">Lease</MenuItem>
            <MenuItem value="agreement">Agreement</MenuItem>
            <MenuItem value="legal_document">Legal Document</MenuItem>
            <MenuItem value="court_filing">Court Filing</MenuItem>
          </Select>
        </FormControl>
        
        <Button
          type="submit"
          variant="contained"
          startIcon={<UploadIcon />}
          disabled={loading || !selectedFile}
        >
          {loading ? <CircularProgress size={20} /> : 'Analyze Document'}
        </Button>
      </Box>
    </Box>
  );

  const renderLegalAnalysisTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Legal Case Analysis
      </Typography>
      
      <Box component="form" onSubmit={handleLegalAnalysis} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          multiline
          rows={4}
          fullWidth
          value={legalQuery}
          onChange={(e) => setLegalQuery(e.target.value)}
          placeholder="Describe your legal situation..."
          disabled={loading}
        />
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Jurisdiction</InputLabel>
            <Select
              value={jurisdiction}
              onChange={(e) => setJurisdiction(e.target.value)}
              label="Jurisdiction"
              disabled={loading}
            >
              <MenuItem value="ri">Rhode Island</MenuItem>
              <MenuItem value="ma">Massachusetts</MenuItem>
              <MenuItem value="fed">Federal</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Case Type</InputLabel>
            <Select
              value={caseType}
              onChange={(e) => setCaseType(e.target.value)}
              label="Case Type"
              disabled={loading}
            >
              <MenuItem value="">Any</MenuItem>
              <MenuItem value="criminal">Criminal</MenuItem>
              <MenuItem value="civil">Civil</MenuItem>
              <MenuItem value="family">Family</MenuItem>
              <MenuItem value="housing">Housing</MenuItem>
            </Select>
          </FormControl>
        </Box>
        
        <Button
          type="submit"
          variant="contained"
          startIcon={<DocumentIcon />}
          disabled={loading || !legalQuery.trim()}
        >
          {loading ? <CircularProgress size={20} /> : 'Analyze Legal Case'}
        </Button>
      </Box>
    </Box>
  );

  const renderResults = () => {
    if (!result) return null;

    if (result.type === 'document') {
      return (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Document Analysis Results
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ whiteSpace: 'pre-wrap' }}>
              <Typography variant="body1">
                <strong>Document Type:</strong> {result.documentType}
              </Typography>
              <Typography variant="body1">
                <strong>Word Count:</strong> {result.data.word_count}
              </Typography>
              <Typography variant="body1">
                <strong>Summary:</strong> {result.data.client_summary}
              </Typography>
              
              {result.data.key_terms && result.data.key_terms.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Key Terms:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {result.data.key_terms.map((term, index) => (
                      <Chip key={index} label={term} size="small" />
                    ))}
                  </Box>
                </Box>
              )}
            </Box>
          </CardContent>
        </Card>
      );
    }

    if (result.type === 'legal') {
      return (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                Legal Analysis Results
              </Typography>
              <Chip label={result.jurisdiction?.toUpperCase() || 'RI'} color="primary" variant="outlined" />
            </Box>
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ whiteSpace: 'pre-wrap' }}>
              {result.data.case_summary && (
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1">Case Summary</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography>{Array.isArray(result.data.case_summary) ? result.data.case_summary[0] : result.data.case_summary}</Typography>
                  </AccordionDetails>
                </Accordion>
              )}
              
              {result.data.legal_rules && result.data.legal_rules.length > 0 && (
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1">Legal Rules</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <ul>
                      {result.data.legal_rules.map((rule, index) => (
                        <li key={index}>{rule}</li>
                      ))}
                    </ul>
                  </AccordionDetails>
                </Accordion>
              )}
              
              {result.data.practical_advice && result.data.practical_advice.length > 0 && (
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1">Practical Advice</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <ul>
                      {result.data.practical_advice.map((advice, index) => (
                        <li key={index}>{advice}</li>
                      ))}
                    </ul>
                  </AccordionDetails>
                </Accordion>
              )}
            </Box>
          </CardContent>
        </Card>
      );
    }

    return null;
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          SmartProBono Legal Assistant
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Unified AI-powered legal assistance platform
        </Typography>
      </Box>

      <Paper elevation={2}>
        <Tabs value={activeTab} onChange={handleTabChange} sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tab icon={<ChatIcon />} label="AI Chat" />
          <Tab icon={<DocumentIcon />} label="Document Analysis" />
          <Tab icon={<UploadIcon />} label="Legal Analysis" />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {activeTab === 0 && renderChatTab()}
          {activeTab === 1 && renderDocumentTab()}
          {activeTab === 2 && renderLegalAnalysisTab()}
        </Box>
      </Paper>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ ml: 2, alignSelf: 'center' }}>
            Processing...
          </Typography>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      )}

      {renderResults()}

      {result?.disclaimers && result.disclaimers.length > 0 && (
        <Alert severity="info" sx={{ mt: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Important Legal Disclaimers:
          </Typography>
          {result.disclaimers.map((disclaimer, index) => (
            <Typography key={index} variant="body2" sx={{ mb: 1 }}>
              • {disclaimer}
            </Typography>
          ))}
        </Alert>
      )}
    </Container>
  );
};

export default UnifiedLegalAssistant;

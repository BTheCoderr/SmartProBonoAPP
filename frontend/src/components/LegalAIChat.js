import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
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
  Divider,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  ListItemIcon,
  Tabs,
  Tab,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import FeedbackIcon from '@mui/icons-material/Feedback';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DescriptionIcon from '@mui/icons-material/Description';
import GavelIcon from '@mui/icons-material/Gavel';
import SearchIcon from '@mui/icons-material/Search';
import ChatIcon from '@mui/icons-material/Chat';
import CategoryIcon from '@mui/icons-material/Category';
import { jsPDF } from 'jspdf';
import { legalChatApi, feedbackApi, conversationApi } from '../services/api';
import useApi from '../hooks/useApi';
import FeedbackForm from './FeedbackForm';
import ModelSelector from './ModelSelector';
import LegalCategories from './LegalCategories';
import ContractForm from './ContractForm';
import AIResponseMetadata from './AIResponseMetadata';
const LegalAIChat = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentModel, setCurrentModel] = useState('mistral');
  const [interfaceMode, setInterfaceMode] = useState('categories'); // 'categories' or 'chat'
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [pdfDialogOpen, setPdfDialogOpen] = useState(false);
  const [feedbackDialogOpen, setFeedbackDialogOpen] = useState(false);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [pdfGenerating, setPdfGenerating] = useState(false);
  const [savingConversation, setSavingConversation] = useState(false);
  const [taskType, setTaskType] = useState('chat');
  const messagesEndRef = useRef(null);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [contractFormOpen, setContractFormOpen] = useState(false);
  const { loading, error, execute: sendMessage } = useApi(legalChatApi.sendMessage);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  const handleSubmit = async e => {
    e.preventDefault();
    if (!input.trim()) return;
    // Detect task type from input
    const detectedTaskType = detectTaskType(input);
    setTaskType(detectedTaskType);
    const userMessage = {
      text: input,
      sender: 'user',
      timestamp: new Date().toISOString(),
      category: selectedCategory?.name,
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    try {
      const response = await sendMessage(input, detectedTaskType);
      const aiMessage = {
        text: response.response,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        model: response.model,
        category: selectedCategory?.name,
        confidenceScore: response.confidenceScore,
        confidenceFactors: response.confidenceFactors,
        reasoningDetails: response.reasoningDetails,
        citations: response.citations,
        jurisdictions: response.jurisdictions,
        lastUpdated: response.lastUpdated,
      };
      setMessages(prev => [...prev, aiMessage]);
      setCurrentModel(response.model || currentModel);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        text: 'Sorry, there was an error processing your request. Please try again.',
        sender: 'ai',
        timestamp: new Date().toISOString(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  const handleCategorySelect = category => {
    setSelectedCategory(category);
    setInput(`Ask about ${category.name.toLowerCase()}...`);
  };
  const handleQuestionSelect = question => {
    setInput(question);
  };
  const generatePDF = async () => {
    setPdfGenerating(true);
    try {
      const doc = new jsPDF();
      // Add title and branding
      doc.setFontSize(24);
      doc.setTextColor(25, 118, 210); // Primary blue color
      doc.text('SmartProBono Legal Document', 20, 20);
      // Add document type and timestamp
      doc.setFontSize(12);
      doc.setTextColor(0, 0, 0);
      doc.text(`Document Type: ${taskType.replace(/_/g, ' ').toUpperCase()}`, 20, 35);
      doc.text(`Generated on: ${new Date().toLocaleString()}`, 20, 45);
      // Add disclaimer
      doc.setFontSize(10);
      doc.setTextColor(128, 128, 128);
      doc.text(t('legalChat.disclaimer'), 20, 55, { maxWidth: 170 });
      let yPosition = 70;
      // Format content based on task type
      if (taskType === 'document_drafting') {
        // For legal documents, use proper formatting
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        const lastResponse = messages[messages.length - 1]?.text;
        if (lastResponse) {
          const sections = lastResponse.split('\n\n');
          sections.forEach(section => {
            const lines = doc.splitTextToSize(section, 170);
            // Check for page overflow
            if (yPosition + lines.length * 7 > 280) {
              doc.addPage();
              yPosition = 20;
            }
            doc.text(lines, 20, yPosition);
            yPosition += lines.length * 7 + 5;
          });
        }
      } else if (taskType === 'rights_research' || taskType === 'complex_analysis') {
        // For research and analysis, use structured format
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        messages.forEach(msg => {
          const prefix = msg.sender === 'user' ? 'Question: ' : 'Analysis: ';
          const text = prefix + msg.text;
          // Add section headers
          if (msg.sender === 'ai') {
            doc.setFontSize(14);
            doc.setTextColor(25, 118, 210);
            doc.text(prefix, 20, yPosition);
            yPosition += 10;
            doc.setFontSize(12);
            doc.setTextColor(0, 0, 0);
          }
          const lines = doc.splitTextToSize(msg.text, 170);
          // Check for page overflow
          if (yPosition + lines.length * 7 > 280) {
            doc.addPage();
            yPosition = 20;
          }
          doc.text(lines, 20, yPosition);
          yPosition += lines.length * 7 + 10;
        });
      } else {
        // For general chat, use Q&A format
        messages.forEach(msg => {
          const prefix = msg.sender === 'user' ? 'Q: ' : 'A: ';
          const text = prefix + msg.text;
          const lines = doc.splitTextToSize(text, 170);
          // Check for page overflow
          if (yPosition + lines.length * 7 > 280) {
            doc.addPage();
            yPosition = 20;
          }
          doc.text(lines, 20, yPosition);
          yPosition += lines.length * 7 + 5;
        });
      }
      // Add footer
      doc.setFontSize(10);
      doc.setTextColor(128, 128, 128);
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.text(`Generated by SmartProBono Legal Assistant - Page ${i} of ${pageCount}`, 20, 290);
      }
      // Save the PDF with appropriate name
      const filename = `legal-${taskType}-${new Date().toISOString().split('T')[0]}.pdf`;
      doc.save(filename);
    } catch (err) {
      console.error('PDF generation error:', err);
    } finally {
      setPdfGenerating(false);
      setPdfDialogOpen(false);
    }
  };
  const handleSaveConversation = async () => {
    setSavingConversation(true);
    try {
      const conversation = {
        timestamp: new Date().toISOString(),
        messages: messages,
        // TODO: Add user ID when authentication is implemented
        user_id: 'temp_user_id',
      };
      await conversationApi.save(conversation);
      setSelectedConversation(conversation);
    } catch (error) {
      console.error('Error saving conversation:', error);
    } finally {
      setSavingConversation(false);
    }
  };
  const handleFeedbackSubmit = async feedbackData => {
    try {
      await feedbackApi.submit(feedbackData);
      setFeedbackDialogOpen(false);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };
  const detectTaskType = message => {
    const lowerMessage = message.toLowerCase();
    // Define task patterns
    const patterns = {
      document_drafting: {
        keywords: ['create', 'draft', 'write', 'generate', 'prepare'],
        documents: [
          'contract',
          'agreement',
          'document',
          'form',
          'letter',
          'template',
          'nda',
          'lease',
        ],
        weight: 0,
      },
      rights_research: {
        keywords: ['right', 'entitled', 'allowed', 'legal', 'law', 'statute'],
        contexts: ['tenant', 'employee', 'worker', 'consumer', 'citizen', 'immigrant'],
        weight: 0,
      },
      complex_analysis: {
        keywords: ['analyze', 'interpret', 'explain', 'understand', 'review'],
        contexts: ['law', 'regulation', 'statute', 'legislation', 'precedent', 'case'],
        weight: 0,
      },
      chat: {
        keywords: ['help', 'how', 'what', 'when', 'where', 'why', 'can', 'should'],
        weight: 0,
      },
    };
    // Calculate weights for each task type
    for (const [task, pattern] of Object.entries(patterns)) {
      // Check for keywords
      if (pattern.keywords) {
        pattern.weight += pattern.keywords.filter(word => lowerMessage.includes(word)).length * 2;
      }
      // Check for document types
      if (pattern.documents) {
        pattern.weight += pattern.documents.filter(doc => lowerMessage.includes(doc)).length * 3;
      }
      // Check for context
      if (pattern.contexts) {
        pattern.weight +=
          pattern.contexts.filter(context => lowerMessage.includes(context)).length * 2;
      }
    }
    // Get task type with highest weight
    const sortedTasks = Object.entries(patterns).sort(([, a], [, b]) => b.weight - a.weight);
    return sortedTasks[0][0]; // Return the task type with highest weight
  };
  const getSuggestedPrompts = () => {
    switch (taskType) {
      case 'document_drafting':
        return [
          'Create a rental agreement for a residential property',
          'Draft an NDA for a freelance project',
          'Generate an employment contract template',
          'Write a demand letter for unpaid services',
          'Prepare a simple will document',
        ];
      case 'rights_research':
        return [
          'What are my rights as a tenant during eviction?',
          'Explain employee rights in workplace discrimination',
          'What are my rights in a police interaction?',
          'Consumer rights for defective products',
          'Immigration rights during visa application',
        ];
      case 'complex_analysis':
        return [
          'Analyze recent changes to privacy laws in tech',
          'Interpret fair use in digital content creation',
          'Explain implications of new employment regulations',
          'Review changes in immigration policy',
          'Analyze landlord-tenant law updates',
        ];
      default:
        return [
          'How do I respond to a court summons?',
          'What steps should I take after a car accident?',
          'How can I dispute a credit report error?',
          "What's the process for small claims court?",
          'How do I file for unemployment benefits?',
        ];
    }
  };
  const TaskSpecificComponents = ({ taskType, response }) => {
    if (!response) return null;
    const handleCopyToClipboard = () => {
      navigator.clipboard.writeText(response);
    };
    switch (taskType) {
      case 'document_drafting':
        return (
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Document Preview
              </Typography>
              <Box sx={{ bgcolor: 'background.paper', p: 2, borderRadius: 1 }}>
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>{response}</pre>
              </Box>
              <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                <span>
                  <Button
                    variant="outlined"
                    startIcon={<DescriptionIcon />}
                    onClick={() => setPdfDialogOpen(true)}
                  >
                    Download as PDF
                  </Button>
                </span>
                <span>
                  <Button variant="outlined" onClick={handleCopyToClipboard}>
                    Copy to Clipboard
                  </Button>
                </span>
              </Box>
            </CardContent>
          </Card>
        );
      case 'rights_research':
        return (
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Rights Summary
              </Typography>
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography>Key Rights</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <List>
                    {response.split('\n').map((line, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <GavelIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={line} />
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography>Legal Resources</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <List>
                    <ListItem>
                      <ListItemIcon>
                        <SearchIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary="Legal Aid Organizations"
                        secondary="Find free legal assistance in your area"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <DescriptionIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary="Related Forms"
                        secondary="Download relevant legal forms"
                      />
                    </ListItem>
                  </List>
                </AccordionDetails>
              </Accordion>
            </CardContent>
          </Card>
        );
      case 'complex_analysis':
        return (
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Legal Analysis
              </Typography>
              <Stepper activeStep={-1} orientation="vertical">
                <Step>
                  <StepLabel>Issue Identification</StepLabel>
                </Step>
                <Step>
                  <StepLabel>Legal Framework</StepLabel>
                </Step>
                <Step>
                  <StepLabel>Analysis</StepLabel>
                </Step>
                <Step>
                  <StepLabel>Implications</StepLabel>
                </Step>
                <Step>
                  <StepLabel>Recommendations</StepLabel>
                </Step>
              </Stepper>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                  {response}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        );
      default:
        return null;
    }
  };
  const handleModelChange = model => {
    setCurrentModel(model);
    // Add a system message to indicate model change
    setMessages(prev => [
      ...prev,
      {
        text: `Switched to ${model} model`,
        sender: 'system',
        timestamp: new Date().toISOString(),
        isSystemMessage: true,
      },
    ]);
  };
  const handleGenerateContract = async (templateName, formData) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/contracts/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template: templateName,
          formData: formData,
          model: currentModel,
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to generate contract');
      }
      // Create blob from response
      const blob = await response.blob();
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${templateName.toLowerCase().replace(/\s+/g, '-')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      // Add success message to chat
      setMessages(prev => [
        ...prev,
        {
          text: `Successfully generated ${templateName}. Check your downloads folder.`,
          sender: 'system',
          timestamp: new Date().toISOString(),
          isSystemMessage: true,
        },
      ]);
    } catch (error) {
      console.error('Error generating contract:', error);
      setMessages(prev => [
        ...prev,
        {
          text: `Error generating contract: ${error.message}`,
          sender: 'system',
          timestamp: new Date().toISOString(),
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };
  const handleGenerateClick = template => {
    setSelectedTemplate(template);
    setContractFormOpen(true);
  };
  const handleCloseContractForm = () => {
    setContractFormOpen(false);
    setSelectedTemplate(null);
  };
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 3 }}>
          <Box
            sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}
          >
            <Typography variant="h4" gutterBottom>
              {t('legalChat.title')}
            </Typography>
            <Tooltip title="Share Feedback">
              <IconButton onClick={() => setFeedbackDialogOpen(true)} color="primary">
                <FeedbackIcon />
              </IconButton>
            </Tooltip>
          </Box>
          <Alert severity="info" sx={{ mb: 3 }}>
            {t('legalChat.disclaimer')}
          </Alert>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle2" gutterBottom>
              Current Mode: {taskType.replace(/_/g, ' ').toUpperCase()}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Using specialized model for {taskType} tasks
            </Typography>
          </Box>
          <Tabs
            value={interfaceMode}
            onChange={(e, newValue) => setInterfaceMode(newValue)}
            centered
          >
            <Tab icon={<CategoryIcon />} label="Categories" value="categories" />
            <Tab icon={<ChatIcon />} label="Direct Chat" value="chat" />
          </Tabs>
          {interfaceMode === 'chat' && (
            <Box sx={{ p: 2 }}>
              <ModelSelector
                currentModel={currentModel}
                onModelChange={handleModelChange}
                isLoading={loading}
              />
            </Box>
          )}
          {interfaceMode === 'categories' && (
            <Box sx={{ p: 2 }}>
              <LegalCategories
                onCategorySelect={handleCategorySelect}
                onQuestionSelect={handleQuestionSelect}
                selectedCategory={selectedCategory}
              />
            </Box>
          )}
          <Paper
            sx={{
              height: 400,
              overflow: 'auto',
              mb: 2,
              p: 2,
              backgroundColor: '#f5f5f5',
              borderRadius: 2,
            }}
          >
            <List>
              {messages.map((msg, index) => (
                <ListItem
                  key={index}
                  sx={{
                    flexDirection: 'column',
                    alignItems: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                    mb: 2,
                  }}
                >
                  <Box
                    sx={{
                      maxWidth: '80%',
                      bgcolor:
                        msg.sender === 'user'
                          ? 'primary.light'
                          : msg.isError
                            ? 'error.light'
                            : 'background.paper',
                      color:
                        msg.sender === 'user' ? 'white' : msg.isError ? 'white' : 'text.primary',
                      borderRadius: 2,
                      p: 2,
                      boxShadow: 1,
                      position: 'relative',
                    }}
                  >
                    {msg.sender === 'ai' && !msg.isError && (
                      <Typography
                        variant="caption"
                        component="div"
                        sx={{ mb: 1, color: 'text.secondary' }}
                      >
                        {msg.model || 'AI Assistant'}
                      </Typography>
                    )}
                    <Typography variant="body1" component="div" sx={{ whiteSpace: 'pre-wrap' }}>
                      {msg.text}
                    </Typography>
                    {msg.sender === 'ai' && !msg.isError && msg.confidenceScore && (
                      <AIResponseMetadata
                        confidenceScore={msg.confidenceScore}
                        citations={msg.citations}
                        reasoningDetails={msg.reasoningDetails}
                        jurisdictions={msg.jurisdictions}
                        lastUpdated={msg.lastUpdated}
                      />
                    )}
                    {msg.sender === 'ai' && !msg.isError && (
                      <TaskSpecificComponents taskType={taskType} response={msg.text} />
                    )}
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{
                        display: 'block',
                        mt: 1,
                        textAlign: msg.sender === 'user' ? 'right' : 'left',
                      }}
                    >
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </Typography>
                  </Box>
                  {msg.sender === 'user' && (
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                      You
                    </Typography>
                  )}
                </ListItem>
              ))}
              {loading && (
                <ListItem>
                  <Paper sx={{ p: 2, bgcolor: 'white', borderRadius: '20px' }}>
                    <CircularProgress size={20} sx={{ mr: 1 }} />
                    <Typography variant="body2" component="span">
                      {t('common.loading')}
                    </Typography>
                  </Paper>
                </ListItem>
              )}
            </List>
          </Paper>
          <TaskSpecificComponents
            taskType={taskType}
            response={messages[messages.length - 1]?.text}
          />
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 2 }}>
            <Tooltip title={pdfGenerating ? 'Generating PDF...' : 'Generate PDF'}>
              <span>
                <Button
                  variant="outlined"
                  startIcon={<PictureAsPdfIcon />}
                  onClick={() => setPdfDialogOpen(true)}
                  disabled={pdfGenerating || messages.length === 0}
                >
                  Export PDF
                </Button>
              </span>
            </Tooltip>
            <Tooltip title={savingConversation ? 'Saving...' : 'Save Conversation'}>
              <span>
                <Button
                  variant="outlined"
                  startIcon={<SaveAltIcon />}
                  onClick={handleSaveConversation}
                  disabled={savingConversation || messages.length === 0}
                >
                  Save
                </Button>
              </span>
            </Tooltip>
          </Box>
          <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{
              display: 'flex',
              gap: 1,
              p: 2,
              backgroundColor: 'background.paper',
              borderTop: 1,
              borderColor: 'divider',
            }}
          >
            <TextField
              fullWidth
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder={
                selectedCategory
                  ? `Ask about ${selectedCategory.name.toLowerCase()}...`
                  : 'Type your message...'
              }
              disabled={loading}
              variant="outlined"
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: '30px',
                },
              }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={loading || !input.trim()}
              endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
              sx={{
                borderRadius: '30px',
                px: 3,
              }}
            >
              {t('common.submit')}
            </Button>
          </Box>
          <Box sx={{ mt: 3 }}>
            <Typography variant="subtitle2" gutterBottom>
              Suggested Questions
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {getSuggestedPrompts().map((suggestion, index) => (
                <Chip
                  key={index}
                  label={suggestion}
                  onClick={() => setInput(suggestion)}
                  disabled={loading}
                  sx={{ my: 0.5 }}
                />
              ))}
            </Box>
          </Box>
        </Paper>
      </Box>
      <Dialog open={pdfDialogOpen} onClose={() => setPdfDialogOpen(false)}>
        <DialogTitle>Generate PDF Summary</DialogTitle>
        <DialogContent>
          <Typography>
            Your {taskType.replace(/_/g, ' ')} will be formatted into a PDF document that you can
            download and save for your records.
          </Typography>
        </DialogContent>
        <DialogActions>
          <span>
            <Button onClick={() => setPdfDialogOpen(false)} disabled={pdfGenerating}>
              Cancel
            </Button>
          </span>
          <span>
            <Button
              variant="contained"
              onClick={generatePDF}
              disabled={pdfGenerating}
              startIcon={pdfGenerating ? <CircularProgress size={20} /> : <PictureAsPdfIcon />}
            >
              {pdfGenerating ? 'Generating...' : 'Generate PDF'}
            </Button>
          </span>
        </DialogActions>
      </Dialog>
      <Dialog
        open={feedbackDialogOpen}
        onClose={() => setFeedbackDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>{t('feedback.title')}</DialogTitle>
        <DialogContent>
          <FeedbackForm onSubmit={handleFeedbackSubmit} />
        </DialogContent>
      </Dialog>
      <ContractForm
        open={contractFormOpen}
        onClose={handleCloseContractForm}
        onGenerate={handleGenerateContract}
        template={selectedTemplate}
        loading={isLoading}
      />
    </Container>
  );
};
export default LegalAIChat;
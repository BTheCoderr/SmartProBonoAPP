import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Button, 
  Container,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Stepper,
  Step,
  StepLabel,
  TextField,
  MenuItem,
  FormControl,
  RadioGroup,
  Radio,
  FormControlLabel,
  Tabs,
  Tab,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  CircularProgress,
  Tooltip
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import DescriptionIcon from '@mui/icons-material/Description';
import EventNoteIcon from '@mui/icons-material/EventNote';
import AssignmentIcon from '@mui/icons-material/Assignment';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import WifiIcon from '@mui/icons-material/Wifi';
import WifiOffIcon from '@mui/icons-material/WifiOff';
import PageLayout from '../components/PageLayout';
import { useAuth } from '../context/AuthContext';
import paralegalService from '../services/paralegalService';
import { useSnackbar } from 'notistack';
import { API_BASE_URL } from '../config';

// Case types for the intake form
const caseTypes = [
  'Tenant Rights',
  'Immigration',
  'Employment',
  'Family Law',
  'Criminal Defense',
  'Consumer Protection',
  'Expungement',
  'Other'
];

// Mock data for demonstration
const mockDocumentTemplates = [
  { id: 1, name: 'Client Intake Form', category: 'General', format: 'PDF' },
  { id: 2, name: 'Fee Waiver Request', category: 'Court', format: 'DOCX' },
  { id: 3, name: 'Client Representation Agreement', category: 'Contracts', format: 'PDF' },
  { id: 4, name: 'Tenant Complaint Letter', category: 'Housing', format: 'DOCX' },
  { id: 5, name: 'Employment Discrimination Complaint', category: 'Employment', format: 'PDF' },
];

const mockScreeningQuestions = [
  { id: 1, question: 'Have you sought legal help for this issue before?', type: 'boolean' },
  { id: 2, question: 'When did this issue first occur?', type: 'date' },
  { id: 3, question: 'Please describe your current financial situation', type: 'text' },
  { id: 4, question: 'Do you have any deadlines or court dates approaching?', type: 'boolean' },
  { id: 5, question: 'What is your preferred language for communication?', type: 'select', options: ['English', 'Spanish', 'Mandarin', 'Vietnamese', 'Other'] }
];

function VirtualParalegalPage() {
  const { isAuthenticated } = useAuth();
  const { enqueueSnackbar } = useSnackbar();
  const [activeTab, setActiveTab] = useState(0);
  const [activeStep, setActiveStep] = useState(0);
  const [caseInfo, setCaseInfo] = useState({
    caseType: '',
    clientName: '',
    clientEmail: '',
    clientPhone: '',
    description: '',
    urgency: 'medium',
    initialConsultDate: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [documentTemplates, setDocumentTemplates] = useState([]);
  const [screeningQuestions, setScreeningQuestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('unknown'); // 'connected', 'disconnected', 'unknown'

  // Steps for the case intake process
  const steps = ['Basic Information', 'Case Details', 'Review & Submit'];

  // Check backend connection status
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await fetch(`${API_BASE_URL}/ping`, { 
          method: 'GET',
          headers: { 'Accept': 'application/json' },
          // Set a timeout for the connection test
          signal: AbortSignal.timeout(5000)
        });
        setConnectionStatus('connected');
      } catch (error) {
        console.warn('Backend connection failed:', error);
        setConnectionStatus('disconnected');
        enqueueSnackbar('Could not connect to backend server. Using demo mode.', { 
          variant: 'warning',
          autoHideDuration: 5000
        });
      }
    };
    
    checkConnection();
  }, [enqueueSnackbar]);

  // Load data from API on component mount
  useEffect(() => {
    const fetchTemplatesAndQuestions = async () => {
      if (isAuthenticated) {
        setIsLoading(true);
        try {
          // Fetch document templates
          const templatesResponse = await paralegalService.getDocumentTemplates();
          if (templatesResponse.success) {
            setDocumentTemplates(templatesResponse.templates);
          }
          
          // Fetch screening questions
          const questionsResponse = await paralegalService.getScreeningQuestions();
          if (questionsResponse.success) {
            setScreeningQuestions(questionsResponse.questions);
          }
        } catch (error) {
          console.error('Error fetching data:', error);
          enqueueSnackbar('Failed to load data. Using demo data instead.', { 
            variant: 'warning',
            autoHideDuration: 4000
          });
          // Use mock data if API fails
          setDocumentTemplates(mockDocumentTemplates);
          setScreeningQuestions(mockScreeningQuestions);
        } finally {
          setIsLoading(false);
        }
      } else {
        // Use mock data if user is not authenticated
        setDocumentTemplates(mockDocumentTemplates);
        setScreeningQuestions(mockScreeningQuestions);
      }
    };
    
    fetchTemplatesAndQuestions();
  }, [isAuthenticated, enqueueSnackbar]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleNextStep = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBackStep = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCaseInfo({
      ...caseInfo,
      [name]: value
    });
  };

  const handleSubmit = async () => {
    if (!isAuthenticated && connectionStatus === 'connected') {
      enqueueSnackbar('Please login to submit a case', { 
        variant: 'warning',
        autoHideDuration: 4000
      });
      return;
    }
    
    setIsSubmitting(true);
    try {
      const response = await paralegalService.createCase(caseInfo);
      if (response.success) {
        enqueueSnackbar('Case submitted successfully!', { 
          variant: 'success',
          autoHideDuration: 4000
        });
        // Reset form and show success message
        setActiveStep(0);
        setCaseInfo({
          caseType: '',
          clientName: '',
          clientEmail: '',
          clientPhone: '',
          description: '',
          urgency: 'medium',
          initialConsultDate: ''
        });
      } else {
        throw new Error(response.message || 'Failed to submit case');
      }
    } catch (error) {
      console.error('Error submitting case:', error);
      enqueueSnackbar(error.message || 'Failed to submit case', { 
        variant: 'error',
        autoHideDuration: 4000
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUseTemplate = async (templateId) => {
    if (!isAuthenticated && connectionStatus === 'connected') {
      enqueueSnackbar('Please login to use templates', { 
        variant: 'warning',
        autoHideDuration: 4000
      });
      return;
    }
    
    try {
      const response = await paralegalService.generateDocument(templateId, {
        // Add any data needed for the template
        clientName: caseInfo.clientName || 'Client Name',
        date: new Date().toISOString()
      });
      
      if (response.success) {
        enqueueSnackbar('Document generated successfully!', { 
          variant: 'success',
          autoHideDuration: 4000
        });
        // Handle successful document generation
        // e.g., redirect to document viewer or download
      } else {
        throw new Error(response.message || 'Failed to generate document');
      }
    } catch (error) {
      console.error('Error generating document:', error);
      enqueueSnackbar(error.message || 'Failed to generate document', { 
        variant: 'error',
        autoHideDuration: 4000
      });
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Client Name"
                name="clientName"
                value={caseInfo.clientName}
                onChange={handleInputChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                label="Client Email"
                name="clientEmail"
                type="email"
                value={caseInfo.clientEmail}
                onChange={handleInputChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                label="Client Phone"
                name="clientPhone"
                value={caseInfo.clientPhone}
                onChange={handleInputChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                select
                required
                fullWidth
                label="Case Type"
                name="caseType"
                value={caseInfo.caseType}
                onChange={handleInputChange}
              >
                {caseTypes.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          </Grid>
        );
      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                multiline
                rows={4}
                label="Case Description"
                name="description"
                value={caseInfo.description}
                onChange={handleInputChange}
                placeholder="Please provide a brief description of the legal issue..."
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom>Urgency Level</Typography>
              <FormControl component="fieldset">
                <RadioGroup
                  row
                  name="urgency"
                  value={caseInfo.urgency}
                  onChange={handleInputChange}
                >
                  <FormControlLabel value="low" control={<Radio />} label="Low" />
                  <FormControlLabel value="medium" control={<Radio />} label="Medium" />
                  <FormControlLabel value="high" control={<Radio />} label="High" />
                  <FormControlLabel value="urgent" control={<Radio />} label="Urgent" />
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Initial Consultation Date"
                name="initialConsultDate"
                type="date"
                value={caseInfo.initialConsultDate}
                onChange={handleInputChange}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper variant="outlined" sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>Case Summary</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2">Client Name</Typography>
                    <Typography variant="body1" gutterBottom>{caseInfo.clientName || 'Not provided'}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2">Case Type</Typography>
                    <Typography variant="body1" gutterBottom>{caseInfo.caseType || 'Not selected'}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2">Email</Typography>
                    <Typography variant="body1" gutterBottom>{caseInfo.clientEmail || 'Not provided'}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2">Phone</Typography>
                    <Typography variant="body1" gutterBottom>{caseInfo.clientPhone || 'Not provided'}</Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="subtitle2">Case Description</Typography>
                    <Typography variant="body1" gutterBottom>{caseInfo.description || 'Not provided'}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2">Urgency</Typography>
                    <Chip 
                      label={caseInfo.urgency.charAt(0).toUpperCase() + caseInfo.urgency.slice(1)} 
                      color={caseInfo.urgency === 'urgent' || caseInfo.urgency === 'high' ? 'error' : 'default'}
                      size="small"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2">Initial Consultation</Typography>
                    <Typography variant="body1">{caseInfo.initialConsultDate || 'Not scheduled'}</Typography>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
            <Grid item xs={12}>
              <Alert severity="info">
                Please review the information above before submitting. Once submitted, you'll be able to track this case and receive automated document suggestions.
              </Alert>
            </Grid>
          </Grid>
        );
      default:
        return null;
    }
  };

  // Tab panel for Document Automation
  const DocumentAutomationPanel = () => (
    <Box sx={{ py: 3 }}>
      <Typography variant="h6" gutterBottom>Document Templates</Typography>
      <Typography variant="body2" paragraph>
        Generate professional legal documents quickly using our automated templates. Select a template to get started.
      </Typography>
      
      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {(documentTemplates.length > 0 ? documentTemplates : mockDocumentTemplates).map((template) => (
            <Grid item xs={12} sm={6} md={4} key={template.id}>
              <Card sx={{ 
                transition: 'all 0.3s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}>
                <CardHeader
                  avatar={<InsertDriveFileIcon color="primary" />}
                  title={template.name}
                  subheader={`Category: ${template.category} • Format: ${template.format}`}
                />
                <CardContent sx={{ pt: 0 }}>
                  <Button 
                    variant="contained" 
                    color="primary" 
                    fullWidth
                    startIcon={<DescriptionIcon />}
                    onClick={() => handleUseTemplate(template.id)}
                    sx={{ 
                      py: 1.2,
                      fontSize: '1rem',
                      boxShadow: 2,
                      '&:hover': {
                        boxShadow: 4,
                        bgcolor: 'primary.dark'
                      }
                    }}
                  >
                    Use Template
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );

  // Tab panel for Screening Questions
  const ScreeningQuestionsPanel = () => (
    <Box sx={{ py: 3 }}>
      <Typography variant="h6" gutterBottom>Client Screening Questions</Typography>
      <Typography variant="body2" paragraph>
        Use these standard questions to screen potential clients and determine eligibility for services.
      </Typography>
      
      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <List>
          {(screeningQuestions.length > 0 ? screeningQuestions : mockScreeningQuestions).map((q) => (
            <ListItem key={q.id} divider>
              <ListItemIcon>
                <AssignmentIcon color="primary" />
              </ListItemIcon>
              <ListItemText
                primary={q.question}
                secondary={`Question type: ${q.type}`}
              />
              <Button size="small" variant="outlined">
                Add to Form
              </Button>
            </ListItem>
          ))}
        </List>
      )}
      
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<EventNoteIcon />}
        >
          Create Custom Screening Form
        </Button>
      </Box>
    </Box>
  );

  return (
    <PageLayout
      title="Virtual Paralegal Assistant"
      description="Streamline client intake, document preparation, and case management"
      sx={{
        background: 'linear-gradient(45deg, #004D40 30%, #00796B 90%)',
      }}
    >
      <Container maxWidth="lg">
        {/* Connection Status Indicator */}
        <Box sx={{ position: 'absolute', top: 16, right: 16, display: 'flex', alignItems: 'center' }}>
          <Tooltip title={connectionStatus === 'connected' 
            ? 'Connected to backend server' 
            : connectionStatus === 'disconnected' 
              ? 'Not connected to backend server. Using demo mode.' 
              : 'Checking...'
          }>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {connectionStatus === 'unknown' && <CircularProgress size={16} sx={{ mr: 1 }} />}
              {connectionStatus === 'connected' && <WifiIcon color="success" />}
              {connectionStatus === 'disconnected' && <WifiOffIcon color="error" />}
              <Typography variant="caption" sx={{ ml: 0.5 }}>
                {connectionStatus === 'connected' ? 'Online' : connectionStatus === 'disconnected' ? 'Offline' : 'Checking...'}
              </Typography>
            </Box>
          </Tooltip>
        </Box>

        {/* Show explicit demo mode warning if disconnected */}
        {connectionStatus === 'disconnected' && (
          <Paper sx={{ p: 2, mb: 4, bgcolor: 'warning.light', color: 'warning.contrastText' }}>
            <Typography variant="body2">
              <strong>Demo Mode:</strong> You're currently viewing this page in demo mode. 
              The form submissions and document generation will simulate API calls without actually connecting to the backend.
            </Typography>
          </Paper>
        )}

        {/* Main action buttons */}
        <Box sx={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: 2, 
          justifyContent: 'center',
          mb: 4
        }}>
          <Button 
            variant="contained" 
            color="primary"
            size="large"
            onClick={() => setActiveTab(0)}
            startIcon={<PersonIcon />}
            sx={{ 
              px: 4, 
              py: 1.5, 
              fontSize: '1.1rem',
              fontWeight: 'bold',
              boxShadow: 3,
              '&:hover': {
                boxShadow: 5,
                transform: 'translateY(-3px)'
              },
              transition: 'all 0.2s'
            }}
          >
            Client Intake
          </Button>
          
          <Button 
            variant="contained" 
            color="secondary"
            size="large"
            onClick={() => setActiveTab(1)}
            startIcon={<DescriptionIcon />}
            sx={{ 
              px: 4, 
              py: 1.5, 
              fontSize: '1.1rem',
              fontWeight: 'bold',
              boxShadow: 3,
              '&:hover': {
                boxShadow: 5,
                transform: 'translateY(-3px)'
              },
              transition: 'all 0.2s'
            }}
          >
            Document Automation
          </Button>
          
          <Button 
            variant="contained" 
            color="info"
            size="large"
            onClick={() => setActiveTab(2)}
            startIcon={<AssignmentIcon />}
            sx={{ 
              px: 4, 
              py: 1.5, 
              fontSize: '1.1rem',
              fontWeight: 'bold',
              boxShadow: 3,
              '&:hover': {
                boxShadow: 5,
                transform: 'translateY(-3px)'
              },
              transition: 'all 0.2s'
            }}
          >
            Case Screening
          </Button>
          
          <Button 
            variant="outlined" 
            color="primary"
            size="large"
            startIcon={<AutorenewIcon />}
            sx={{ 
              px: 4, 
              py: 1.5, 
              fontSize: '1.1rem',
              fontWeight: 'bold',
              bgcolor: 'rgba(255, 255, 255, 0.9)',
              borderWidth: 2,
              '&:hover': {
                borderWidth: 2,
                bgcolor: 'white'
              },
              transition: 'all 0.2s'
            }}
          >
            Self-Service Legal Help
          </Button>
        </Box>

        {/* Overview Section */}
        <Paper sx={{ p: 4, mb: 4 }}>
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography variant="h5" component="h2" gutterBottom>
                Your AI-Powered Legal Assistant
              </Typography>
              <Typography variant="body1" paragraph>
                Smart Pro Bono's Virtual Paralegal Assistant helps law firms and solo practitioners streamline client intake, 
                automate document preparation, and manage cases more efficiently.
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary="Reduce administrative workload with automated client intake" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary="Generate legal documents from templates in seconds" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary="Screen potential clients with customizable questionnaires" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary="Provide self-service resources for clients you can't take on" />
                </ListItem>
              </List>
            </Grid>
            <Grid item xs={12} md={5}>
              <Box sx={{ 
                bgcolor: 'primary.main', 
                color: 'white', 
                p: 3, 
                borderRadius: 2,
                boxShadow: 3
              }}>
                <Typography variant="h6" gutterBottom>
                  Virtual Paralegal Assistant Benefits:
                </Typography>
                <Box component="ul" sx={{ pl: 2 }}>
                  <Typography component="li" sx={{ mb: 1 }}>Save 15+ hours weekly on administrative tasks</Typography>
                  <Typography component="li" sx={{ mb: 1 }}>Reduce client intake time by up to 70%</Typography>
                  <Typography component="li" sx={{ mb: 1 }}>Decrease document preparation errors</Typography>
                  <Typography component="li">Serve more clients without increasing staff</Typography>
                </Box>
                <Box sx={{ mt: 3 }}>
                  <Button 
                    variant="contained" 
                    color="secondary"
                    fullWidth
                    size="large"
                  >
                    Schedule a Demo
                  </Button>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Paper>

        {/* Main Functionality Tabs */}
        <Paper sx={{ mb: 4 }}>
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            variant="fullWidth"
            indicatorColor="primary"
            textColor="primary"
          >
            <Tab icon={<PersonIcon />} label="Case Intake" />
            <Tab icon={<DescriptionIcon />} label="Document Automation" />
            <Tab icon={<AssignmentIcon />} label="Screening Questions" />
          </Tabs>
          
          <Box sx={{ p: 3 }}>
            {activeTab === 0 && (
              <Box>
                <Typography variant="h6" gutterBottom>New Client Intake</Typography>
                <Typography variant="body2" paragraph>
                  Streamline your client onboarding process with our digital intake form. 
                  Complete the steps below to create a new case.
                </Typography>
                
                <Stepper activeStep={activeStep} sx={{ mb: 3 }}>
                  {steps.map((label) => (
                    <Step key={label}>
                      <StepLabel>{label}</StepLabel>
                    </Step>
                  ))}
                </Stepper>
                
                <Box sx={{ mt: 3 }}>
                  {renderStepContent(activeStep)}
                  
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3 }}>
                    {activeStep > 0 && (
                      <Button 
                        onClick={handleBackStep} 
                        sx={{ 
                          mr: 1,
                          px: 3,
                          py: 1,
                          fontSize: '1rem'
                        }}
                      >
                        Back
                      </Button>
                    )}
                    {activeStep < steps.length - 1 ? (
                      <Button
                        variant="contained"
                        color="primary"
                        onClick={handleNextStep}
                        sx={{ 
                          px: 3,
                          py: 1,
                          fontSize: '1rem',
                          boxShadow: 3,
                          '&:hover': {
                            boxShadow: 5,
                            transform: 'translateY(-2px)'
                          },
                          transition: 'all 0.2s'
                        }}
                      >
                        Next
                      </Button>
                    ) : (
                      <Button
                        variant="contained"
                        color="primary"
                        onClick={handleSubmit}
                        disabled={isSubmitting}
                        sx={{ 
                          px: 3,
                          py: 1,
                          fontSize: '1rem',
                          boxShadow: 3,
                          '&:hover': {
                            boxShadow: 5,
                            transform: 'translateY(-2px)'
                          },
                          transition: 'all 0.2s'
                        }}
                      >
                        {isSubmitting ? 'Submitting...' : 'Submit'}
                      </Button>
                    )}
                  </Box>
                </Box>
              </Box>
            )}
            
            {activeTab === 1 && <DocumentAutomationPanel />}
            
            {activeTab === 2 && <ScreeningQuestionsPanel />}
          </Box>
        </Paper>
        
        {/* Law Firm Use Cases */}
        <Paper sx={{ p: 4, mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            Use Cases for Law Firms
          </Typography>
          <Typography variant="body2" paragraph>
            See how different legal practices benefit from our Virtual Paralegal Assistant.
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%' }}>
                <CardHeader
                  title="Solo Practitioners"
                  titleTypographyProps={{ variant: 'h6' }}
                />
                <CardContent>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Work more efficiently without the cost of full-time support staff.
                  </Typography>
                  <List dense disablePadding>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Handle more client inquiries" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Automated document generation" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Client screening tools" />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%' }}>
                <CardHeader
                  title="Small Law Firms"
                  titleTypographyProps={{ variant: 'h6' }}
                />
                <CardContent>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Scale your practice without proportionally increasing staff costs.
                  </Typography>
                  <List dense disablePadding>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Standardized client intake" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Consistent document preparation" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Efficient case management" />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%' }}>
                <CardHeader
                  title="Legal Aid Organizations"
                  titleTypographyProps={{ variant: 'h6' }}
                />
                <CardContent>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Serve more clients with limited resources and staff.
                  </Typography>
                  <List dense disablePadding>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Automated eligibility screening" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Self-service resources for clients" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon sx={{ minWidth: '30px' }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary="Case prioritization tools" />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Paper>
        
        {/* Call to Action */}
        <Paper sx={{ p: 4, textAlign: 'center', bgcolor: 'secondary.light' }}>
          <Typography variant="h5" gutterBottom>
            Ready to Transform Your Legal Practice?
          </Typography>
          <Typography variant="body1" paragraph sx={{ maxWidth: '700px', mx: 'auto' }}>
            Join the growing number of legal professionals using Smart Pro Bono's Virtual Paralegal Assistant to streamline their practice.
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Button 
              variant="contained" 
              color="primary" 
              size="large"
              sx={{ 
                mx: 1, 
                mb: { xs: 2, sm: 0 },
                px: 4,
                py: 1.5,
                fontSize: '1.1rem',
                fontWeight: 'bold',
                boxShadow: 3,
                '&:hover': {
                  boxShadow: 5,
                  transform: 'translateY(-3px)'
                },
                transition: 'all 0.2s'
              }}
            >
              Get Started
            </Button>
            <Button 
              variant="outlined" 
              color="primary" 
              size="large"
              sx={{ 
                mx: 1,
                px: 4,
                py: 1.5,
                fontSize: '1.1rem',
                fontWeight: 'bold',
                bgcolor: 'rgba(255, 255, 255, 0.9)',
                borderWidth: 2,
                '&:hover': {
                  borderWidth: 2,
                  bgcolor: 'white',
                  transform: 'translateY(-2px)'
                },
                transition: 'all 0.2s'
              }}
              startIcon={<AutorenewIcon />}
            >
              Request Demo
            </Button>
          </Box>
        </Paper>
      </Container>
    </PageLayout>
  );
}

export default VirtualParalegalPage; 
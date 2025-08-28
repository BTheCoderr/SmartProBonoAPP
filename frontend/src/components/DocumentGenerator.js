import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stepper,
  Step,
  StepLabel,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  FormControlLabel,
  Switch,
  Tooltip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Card,
  CardContent,
  Divider,
  Chip,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import { useTheme } from '@mui/material/styles';
import { useTranslation } from 'react-i18next';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import EditIcon from '@mui/icons-material/Edit';
import DragIndicatorIcon from '@mui/icons-material/DragIndicator';
import MicIcon from '@mui/icons-material/Mic';
import VoiceInput from './VoiceInput';
import { toast } from 'react-hot-toast';
import documentsApi from '../services/documentsApi';
import AssignmentIcon from '@mui/icons-material/Assignment';
import DescriptionIcon from '@mui/icons-material/Description';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import CloseIcon from '@mui/icons-material/Close';
import PreviewIcon from '@mui/icons-material/Preview';
import DocumentPreview from './DocumentPreview';
import { useAuth } from '../context/AuthContext';

const DocumentGenerator = ({ 
  documentType,
  initialValues = {},
  onSubmit,
  onSave 
}) => {
  const theme = useTheme();
  const { t } = useTranslation();
  const { currentUser } = useAuth();
  const [activeStep, setActiveStep] = useState(0);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [formData, setFormData] = useState(initialValues);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [templateMetadata, setTemplateMetadata] = useState({});
  const [accessibilityMode, setAccessibilityMode] = useState(false);
  const [fontSize, setFontSize] = useState('medium');
  const [sections, setSections] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editingContent, setEditingContent] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [progress, setProgress] = useState(() => {
    const saved = localStorage.getItem('documentProgress');
    return saved ? JSON.parse(saved) : {};
  });
  const [isListening, setIsListening] = useState(false);
  const [isAIHelping, setIsAIHelping] = useState(false);
  const [aiStatus, setAiStatus] = useState('');
  const [previewOpen, setPreviewOpen] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Document templates based on document type
  const documentTemplates = {
    expungement: {
      title: 'Expungement Request Form',
      steps: [
        { label: 'Personal Information', fields: ['fullName', 'dateOfBirth', 'address', 'phoneNumber', 'email'] },
        { label: 'Case Information', fields: ['caseNumber', 'courtName', 'convictionDate', 'offenseDescription'] },
        { label: 'Eligibility Information', fields: ['completedSentence', 'timeSinceConviction', 'otherConvictions'] },
        { label: 'Supporting Documents', fields: ['documentsAttached', 'additionalStatements'] },
        { label: 'Review & Submit', fields: [] }
      ],
    },
    housing: {
      title: 'Housing Defense Letter',
      steps: [
        { label: 'Personal Information', fields: ['fullName', 'address', 'email', 'phoneNumber'] },
        { label: 'Landlord Information', fields: ['landlordName', 'landlordAddress'] },
        { label: 'Tenancy Details', fields: ['leaseStartDate', 'monthlyRent', 'unitDetails'] },
        { label: 'Defense Details', fields: ['issueDescription', 'issueStartDate', 'attemptedResolution'] },
        { label: 'Review & Submit', fields: [] }
      ],
    },
    fee_waiver: {
      title: 'Fee Waiver Application',
      steps: [
        { label: 'Personal Information', fields: ['fullName', 'address', 'phoneNumber', 'email'] },
        { label: 'Financial Information', fields: ['monthlyIncome', 'householdSize', 'publicBenefits'] },
        { label: 'Case Information', fields: ['caseNumber', 'courtName', 'caseType'] },
        { label: 'Review & Submit', fields: [] }
      ],
    },
  };

  // Field definitions for each document type
  const fieldDefinitions = {
    expungement: {
      fullName: { label: 'Full Legal Name', type: 'text', required: true },
      dateOfBirth: { label: 'Date of Birth', type: 'date', required: true },
      address: { label: 'Current Address', type: 'text', required: true },
      phoneNumber: { label: 'Phone Number', type: 'tel', required: true },
      email: { label: 'Email Address', type: 'email', required: true },
      caseNumber: { label: 'Case Number', type: 'text', required: true },
      courtName: { label: 'Court Name', type: 'text', required: true },
      convictionDate: { label: 'Date of Conviction', type: 'date', required: true },
      offenseDescription: { label: 'Description of Offense', type: 'textarea', required: true },
      completedSentence: { label: 'Have you completed all terms of your sentence?', type: 'select', options: ['Yes', 'No'], required: true },
      timeSinceConviction: { label: 'Time since conviction (years)', type: 'number', required: true },
      otherConvictions: { label: 'Do you have other convictions?', type: 'select', options: ['Yes', 'No'], required: true },
      documentsAttached: { label: 'List of documents attached', type: 'textarea', required: false },
      additionalStatements: { label: 'Additional statements', type: 'textarea', required: false },
    },
    housing: {
      fullName: { label: 'Full Legal Name', type: 'text', required: true },
      address: { label: 'Current Address', type: 'text', required: true },
      email: { label: 'Email Address', type: 'email', required: true },
      phoneNumber: { label: 'Phone Number', type: 'tel', required: true },
      landlordName: { label: 'Landlord Name', type: 'text', required: true },
      landlordAddress: { label: 'Landlord Address', type: 'text', required: true },
      leaseStartDate: { label: 'Lease Start Date', type: 'date', required: true },
      monthlyRent: { label: 'Monthly Rent', type: 'number', required: true },
      unitDetails: { label: 'Unit Details', type: 'textarea', required: false },
      issueDescription: { label: 'Description of Issue', type: 'textarea', required: true },
      issueStartDate: { label: 'Date Issue Began', type: 'date', required: true },
      attemptedResolution: { label: 'Steps Taken to Resolve Issue', type: 'textarea', required: true },
    },
    fee_waiver: {
      fullName: { label: 'Full Legal Name', type: 'text', required: true },
      address: { label: 'Current Address', type: 'text', required: true },
      phoneNumber: { label: 'Phone Number', type: 'tel', required: true },
      email: { label: 'Email Address', type: 'email', required: true },
      monthlyIncome: { label: 'Monthly Income', type: 'number', required: true },
      householdSize: { label: 'Number of People in Household', type: 'number', required: true },
      publicBenefits: { label: 'Do you receive public benefits?', type: 'select', options: ['Yes', 'No'], required: true },
      caseNumber: { label: 'Case Number', type: 'text', required: false },
      courtName: { label: 'Court Name', type: 'text', required: true },
      caseType: { label: 'Type of Case', type: 'text', required: true },
    }
  };

  // Fetch available templates and their metadata
  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const templates = await documentsApi.getTemplates();
        // Extract template names from the response
        const templateNames = templates.map(template => template.id);
        setTemplates(templateNames);
        
        // Create metadata object
        const metadata = {};
        templates.forEach(template => {
          metadata[template.id] = {
            name: template.name,
            description: template.description,
            required_fields: template.fields.filter(field => field.required).map(field => field.name)
          };
        });
        setTemplateMetadata(metadata);
      } catch (err) {
        setError('Failed to load templates');
      }
    };
    fetchTemplates();
  }, []);

  useEffect(() => {
    // Initialize Web Speech API
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');
        setEditingContent(prev => prev + ' ' + transcript);
      };
      setRecognition(recognition);
    }
  }, []);

  useEffect(() => {
    // Save progress to localStorage
    if (Object.keys(formData).length > 0) {
      localStorage.setItem('documentProgress', JSON.stringify({
        template: selectedTemplate,
        formData,
        step: activeStep
      }));
    }
  }, [formData, selectedTemplate, activeStep]);

  useEffect(() => {
    // Load any saved draft from localStorage
    const savedDraft = localStorage.getItem(`${documentType}FormDraft`);
    if (savedDraft && Object.keys(initialValues).length === 0) {
      try {
        const parsed = JSON.parse(savedDraft);
        setFormData(parsed.values || {});
      } catch (e) {
        console.error('Error loading saved draft:', e);
      }
    }
  }, [documentType, initialValues]);

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    
    // Find the template in the metadata
    const metadata = templateMetadata[template] || {};
    
    // Initialize form data with required fields
    const requiredFields = metadata.required_fields || [];
    const initialData = {};
    requiredFields.forEach(field => {
      initialData[field] = '';
    });
    setFormData(initialData);
  };

  const handleInputChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleAccessibilityToggle = () => {
    setAccessibilityMode(!accessibilityMode);
  };

  const handleFontSizeChange = (event) => {
    setFontSize(event.target.value);
  };

  const validateForm = () => {
    if (!selectedTemplate) return false;
    const requiredFields = templateMetadata[selectedTemplate]?.required_fields || [];
    return requiredFields.every(field => formData[field] && formData[field].trim() !== '');
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      // Use the documentsApi service with direct method
      await documentsApi.generateDocumentDirect(selectedTemplate, formData);

      // Success notification
      setActiveStep(0);
      setSelectedTemplate('');
      setFormData({});
      toast.success("Document generated successfully!");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => {
      const newData = { ...prev, [field]: value };
      
      // Save to localStorage as draft
      localStorage.setItem(`${documentType}FormDraft`, JSON.stringify({ 
        values: newData, 
        timestamp: new Date().toISOString(),
        userId: currentUser?.id
      }));
      
      return newData;
    });
  };

  const handleNext = () => {
    const template = documentTemplates[documentType];
    if (activeStep < template.steps.length - 1) {
      setActiveStep(prev => prev + 1);
    } else {
      handleSubmitDocument();
    }
  };

  const handleBack = () => {
    setActiveStep(prev => Math.max(0, prev - 1));
  };

  const handleSubmitDocument = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await onSubmit(formData, documentType);
      
      // Clear draft from localStorage on successful submission
      localStorage.removeItem(`${documentType}FormDraft`);
      
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      setError('Error submitting document. Please try again.');
      console.error('Error submitting document:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveDraft = async () => {
    setLoading(true);
    
    try {
      if (onSave) {
        await onSave(formData, documentType);
      }
      
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      console.error('Error saving draft:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestAIHelp = async () => {
    setIsAIHelping(true);
    setAiStatus('Analyzing form...');
    
    try {
      // Simulate AI processing
      await new Promise(resolve => setTimeout(resolve, 1500));
      setAiStatus('Generating suggestions...');
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Get current step fields
      const currentTemplate = documentTemplates[documentType];
      const currentStepFields = currentTemplate.steps[activeStep].fields;
      
      // Simulate AI suggestions for empty fields
      const updatedFormData = { ...formData };
      let changesMade = false;
      
      currentStepFields.forEach(field => {
        if (!formData[field] && fieldDefinitions[documentType][field]) {
          // Generate mock data based on field type
          const fieldDef = fieldDefinitions[documentType][field];
          
          if (fieldDef.type === 'text' && field.includes('Name')) {
            updatedFormData[field] = currentUser?.name || 'John Doe';
            changesMade = true;
          } else if (field === 'address') {
            updatedFormData[field] = '123 Legal Street, Anytown, ST 12345';
            changesMade = true;
          } else if (field === 'email') {
            updatedFormData[field] = currentUser?.email || 'user@example.com';
            changesMade = true;
          } else if (field === 'phoneNumber') {
            updatedFormData[field] = '(555) 123-4567';
            changesMade = true;
          } else if (fieldDef.type === 'textarea') {
            if (field === 'offenseDescription') {
              updatedFormData[field] = 'Minor misdemeanor offense from 2018.';
              changesMade = true;
            } else if (field === 'issueDescription') {
              updatedFormData[field] = 'Ongoing maintenance issues with plumbing that have not been addressed despite multiple requests.';
              changesMade = true;
            }
          }
        }
      });
      
      if (changesMade) {
        setFormData(updatedFormData);
        localStorage.setItem(`${documentType}FormDraft`, JSON.stringify({ 
          values: updatedFormData, 
          timestamp: new Date().toISOString(),
          userId: currentUser?.id
        }));
      }
      
      setAiStatus('Suggestions applied!');
      setTimeout(() => {
        setIsAIHelping(false);
        setAiStatus('');
      }, 2000);
      
    } catch (err) {
      setAiStatus('Error generating suggestions');
      console.error('Error with AI assistance:', err);
      setTimeout(() => {
        setIsAIHelping(false);
        setAiStatus('');
      }, 2000);
    }
  };

  const validateStep = () => {
    const template = documentTemplates[documentType];
    const currentStepFields = template.steps[activeStep].fields;
    
    // Skip validation for review step
    if (activeStep === template.steps.length - 1) {
      return true;
    }
    
    for (const field of currentStepFields) {
      const fieldDef = fieldDefinitions[documentType][field];
      if (fieldDef && fieldDef.required && !formData[field]) {
        return false;
      }
    }
    
    return true;
  };

  const handleOpenPreview = () => {
    setPreviewOpen(true);
  };

  const handleClosePreview = () => {
    setPreviewOpen(false);
  };

  // If document type is not valid
  if (!documentTemplates[documentType]) {
    return (
      <Alert severity="error">Invalid document type specified.</Alert>
    );
  }

  const template = documentTemplates[documentType];
  const currentStep = template.steps[activeStep];
  const currentFields = currentStep.fields;
  const isLastStep = activeStep === template.steps.length - 1;
  const canProceed = validateStep();

  return (
    <Box sx={{ mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <AssignmentIcon fontSize="large" color="primary" sx={{ mr: 2 }} />
          <Typography variant="h5">{template.title}</Typography>
          
          <Box ml="auto" display="flex" alignItems="center">
            <Button 
              startIcon={<PreviewIcon />} 
              onClick={handleOpenPreview}
              sx={{ mr: 1 }}
            >
              Preview
            </Button>
            
            <Button
              variant="outlined"
              onClick={handleSaveDraft}
              disabled={loading}
            >
              Save Draft
            </Button>
          </Box>
        </Box>
        
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {template.steps.map((step, index) => (
            <Step key={index}>
              <StepLabel>{step.label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        
        {saveSuccess && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Document saved successfully!
          </Alert>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {isAIHelping && (
          <Alert 
            severity="info" 
            sx={{ mb: 2, display: 'flex', alignItems: 'center' }}
            icon={<SmartToyIcon />}
          >
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Typography sx={{ mr: 2 }}>{aiStatus}</Typography>
              {aiStatus !== 'Suggestions applied!' && <CircularProgress size={20} />}
            </Box>
          </Alert>
        )}
        
        {isLastStep ? (
          <Box>
            <Typography variant="h6" gutterBottom>
              Review Your Information
            </Typography>
            
            {template.steps.slice(0, -1).map((step, stepIndex) => (
              <Card key={stepIndex} sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {step.label}
                  </Typography>
                  
                  <Grid container spacing={2}>
                    {step.fields.map(field => (
                      <Grid item xs={12} sm={6} key={field}>
                        <Box>
                          <Typography variant="subtitle2" color="text.secondary">
                            {fieldDefinitions[documentType][field]?.label}:
                          </Typography>
                          <Typography variant="body1">
                            {formData[field] || 'Not provided'}
                          </Typography>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>
                  
                  <Box display="flex" justifyContent="flex-end" mt={1}>
                    <Button 
                      size="small"
                      onClick={() => setActiveStep(stepIndex)}
                    >
                      Edit
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        ) : (
          <Grid container spacing={3}>
            {currentFields.map(field => {
              const fieldDef = fieldDefinitions[documentType][field];
              
              if (!fieldDef) return null;
              
              return (
                <Grid item xs={12} sm={fieldDef.type === 'textarea' ? 12 : 6} key={field}>
                  {fieldDef.type === 'select' ? (
                    <FormControl fullWidth required={fieldDef.required}>
                      <InputLabel id={`label-${field}`}>{fieldDef.label}</InputLabel>
                      <Select
                        labelId={`label-${field}`}
                        id={field}
                        value={formData[field] || ''}
                        label={fieldDef.label}
                        onChange={(e) => handleChange(field, e.target.value)}
                      >
                        {fieldDef.options.map(option => (
                          <MenuItem key={option} value={option}>{option}</MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  ) : (
                    <TextField
                      id={field}
                      label={fieldDef.label}
                      type={fieldDef.type}
                      value={formData[field] || ''}
                      onChange={(e) => handleChange(field, e.target.value)}
                      required={fieldDef.required}
                      fullWidth
                      multiline={fieldDef.type === 'textarea'}
                      rows={fieldDef.type === 'textarea' ? 4 : 1}
                    />
                  )}
                </Grid>
              );
            })}
          </Grid>
        )}
        
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
          <Box>
            <Button
              color="primary"
              variant="outlined"
              startIcon={<SmartToyIcon />}
              onClick={handleRequestAIHelp}
              disabled={isAIHelping || isLastStep}
            >
              AI Assist
            </Button>
          </Box>
          
          <Box>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
              sx={{ mr: 1 }}
            >
              Back
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={handleNext}
              disabled={loading || !canProceed}
            >
              {isLastStep ? 'Submit' : 'Next'}
            </Button>
          </Box>
        </Box>
      </Paper>
      
      <Dialog 
        open={previewOpen} 
        onClose={handleClosePreview}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            Document Preview
            <IconButton onClick={handleClosePreview}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <DocumentPreview 
            formData={formData}
            formType={documentType}
            autoUpdate={true}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePreview}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DocumentGenerator;
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

const DocumentGenerator = () => {
  const theme = useTheme();
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [formData, setFormData] = useState({});
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

  const renderFieldHelp = (field) => {
    const validationRule = templateMetadata[selectedTemplate]?.validation_rules?.[field];
    if (!validationRule) return null;

    let helpText = '';
    if (typeof validationRule === 'string') {
      helpText = 'Please enter a valid value';
    } else if (validationRule.min_length) {
      helpText = `At least ${validationRule.min_length} item(s) required`;
    }

    return (
      <Tooltip title={helpText}>
        <IconButton size="small" aria-label="help">
          <HelpOutlineIcon />
        </IconButton>
      </Tooltip>
    );
  };

  const handleDragEnd = (result) => {
    if (!result.destination) return;
    const items = Array.from(sections);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    setSections(items);
  };

  const toggleVoiceInput = () => {
    if (isRecording) {
      recognition?.stop();
    } else {
      recognition?.start();
    }
    setIsRecording(!isRecording);
  };

  const handleVoiceTranscript = (transcript) => {
    if (isEditing) {
      setEditingContent(prev => prev + ' ' + transcript);
    } else {
      // Add transcript to the currently selected field
      const currentField = Object.keys(formData)[0]; // You might want to track the current field
      if (currentField) {
        setFormData(prev => ({
          ...prev,
          [currentField]: prev[currentField] + ' ' + transcript
        }));
      }
    }
  };

  const renderDraggableSections = () => (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="sections">
        {(provided) => (
          <div {...provided.droppableProps} ref={provided.innerRef}>
            {sections.map((section, index) => (
              <Draggable key={section.id} draggableId={section.id} index={index}>
                {(provided) => (
                  <Paper
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    sx={{ mb: 2, p: 2 }}
                  >
                    <Grid container alignItems="center" spacing={2}>
                      <Grid item {...provided.dragHandleProps}>
                        <DragIndicatorIcon />
                      </Grid>
                      <Grid item xs>
                        <Typography variant="h6">{section.title}</Typography>
                        <Typography>{section.content}</Typography>
                      </Grid>
                      <Grid item>
                        <IconButton onClick={() => {
                          setIsEditing(true);
                          setEditingContent(section.content);
                        }}>
                          <EditIcon />
                        </IconButton>
                      </Grid>
                    </Grid>
                  </Paper>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 4,
          fontSize: accessibilityMode ? theme.typography[fontSize].fontSize : 'inherit'
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            {t('documents.title')}
          </Typography>
          <Box>
            <FormControlLabel
              control={
                <Switch
                  checked={accessibilityMode}
                  onChange={handleAccessibilityToggle}
                  icon={<AccessibilityNewIcon />}
                />
              }
              label={t('accessibility.mode')}
            />
            {accessibilityMode && (
              <FormControl size="small" sx={{ ml: 2 }}>
                <Select
                  value={fontSize}
                  onChange={handleFontSizeChange}
                  aria-label="Font size"
                >
                  <MenuItem value="small">Small</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="large">Large</MenuItem>
                </Select>
              </FormControl>
            )}
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          <Step>
            <StepLabel>{t('documents.steps.selectTemplate')}</StepLabel>
          </Step>
          <Step>
            <StepLabel>{t('documents.steps.fillDetails')}</StepLabel>
          </Step>
          <Step>
            <StepLabel>{t('documents.steps.review')}</StepLabel>
          </Step>
        </Stepper>

        {activeStep === 0 && (
          <Box>
            <FormControl fullWidth>
              <InputLabel>{t('documents.selectTemplate')}</InputLabel>
              <Select
                value={selectedTemplate}
                onChange={(e) => handleTemplateSelect(e.target.value)}
                label={t('documents.selectTemplate')}
              >
                {templates.map((template) => (
                  <MenuItem key={template} value={template}>
                    {templateMetadata[template]?.name || template}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        )}

        {activeStep === 1 && selectedTemplate && (
          <Box>
            <Typography variant="h6" gutterBottom>
              {templateMetadata[selectedTemplate]?.name || selectedTemplate}
            </Typography>
            <Typography variant="body2" gutterBottom sx={{ mb: 3 }}>
              {templateMetadata[selectedTemplate]?.description || ''}
            </Typography>
            
            {templateMetadata[selectedTemplate]?.required_fields && (
              <Grid container spacing={2}>
                {Object.entries(templateMetadata[selectedTemplate].required_fields).map(([field, required]) => (
                  <Grid item xs={12} md={6} key={field}>
                    <TextField
                      fullWidth
                      label={field.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                      value={formData[field] || ''}
                      onChange={handleInputChange(field)}
                      required={required}
                      margin="normal"
                      error={required && (!formData[field] || formData[field].trim() === '')}
                      helperText={required && (!formData[field] || formData[field].trim() === '') ? 'This field is required' : ''}
                    />
                  </Grid>
                ))}
              </Grid>
            )}
            
            <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
              <VoiceInput
                onTranscript={handleVoiceTranscript}
                isListening={isListening}
                setIsListening={setIsListening}
              />
            </Box>
          </Box>
        )}

        {activeStep === 2 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              {t('documents.review.title')}
            </Typography>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>{t('documents.review.details')}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                {Object.entries(formData).map(([key, value]) => (
                  <Box key={key} sx={{ mb: 1 }}>
                    <Typography variant="subtitle2">{key}:</Typography>
                    <Typography>{value}</Typography>
                  </Box>
                ))}
              </AccordionDetails>
            </Accordion>
          </Box>
        )}

        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
          <Button
            onClick={() => setActiveStep((prev) => Math.max(0, prev - 1))}
            disabled={activeStep === 0 || loading}
          >
            {t('common.back')}
          </Button>
          {activeStep === 2 ? (
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={!validateForm() || loading}
              endIcon={loading ? <CircularProgress size={20} /> : null}
            >
              {t('documents.generate')}
            </Button>
          ) : (
            <Button
              variant="contained"
              onClick={() => setActiveStep((prev) => prev + 1)}
              disabled={
                (activeStep === 0 && !selectedTemplate) ||
                (activeStep === 1 && !validateForm())
              }
            >
              {t('common.next')}
            </Button>
          )}
        </Box>
      </Paper>

      <Dialog open={isEditing} onClose={() => setIsEditing(false)}>
        <DialogTitle>Edit Section Content</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={4}
            value={editingContent}
            onChange={(e) => setEditingContent(e.target.value)}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsEditing(false)}>Cancel</Button>
          <Button onClick={() => {
            // Update section content
            setSections(prev => prev.map(section => 
              section.content === editingContent ? { ...section, content: editingContent } : section
            ));
            setIsEditing(false);
          }} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DocumentGenerator;
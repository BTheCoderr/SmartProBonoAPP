import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Button, 
  Stepper, 
  Step, 
  StepLabel, 
  StepContent, 
  Paper, 
  CircularProgress,
  Chip,
  Alert,
  Grid,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { Gavel as RightsIcon } from '@mui/icons-material';
import axios from 'axios';

// Common legal process workflows
const WORKFLOWS = {
  'eviction': {
    title: 'Eviction Process',
    description: 'Learn about the eviction process and your rights as a tenant',
    domains: ['tenant_rights'],
    steps: ['notice', 'response', 'court', 'decision', 'appeal']
  },
  'divorce': {
    title: 'Divorce Process',
    description: 'Navigate the divorce process step by step',
    domains: ['family'],
    steps: ['petition', 'response', 'discovery', 'mediation', 'trial', 'finalization']
  },
  'immigration': {
    title: 'Immigration Application',
    description: 'Understand the immigration application process',
    domains: ['immigration'],
    steps: ['eligibility', 'forms', 'documentation', 'filing', 'interview', 'decision']
  },
  'employment_discrimination': {
    title: 'Employment Discrimination',
    description: 'Steps to address workplace discrimination',
    domains: ['employment'],
    steps: ['internal_complaint', 'eeoc_filing', 'investigation', 'mediation', 'litigation']
  }
};

const LegalRightsVisualizer = () => {
  const [workflow, setWorkflow] = useState('');
  const [activeStep, setActiveStep] = useState(0);
  const [jurisdiction, setJurisdiction] = useState('');
  const [loading, setLoading] = useState(false);
  const [stepContent, setStepContent] = useState({});
  const [jurisdictions, setJurisdictions] = useState([]);
  const [error, setError] = useState(null);

  // Fetch available jurisdictions
  useEffect(() => {
    const fetchJurisdictions = async () => {
      try {
        const response = await axios.get('/api/legal/jurisdictions');
        setJurisdictions(response.data.jurisdictions || []);
      } catch (err) {
        console.error('Error fetching jurisdictions:', err);
        setJurisdictions(['federal', 'california', 'new_york', 'texas']);
      }
    };
    
    fetchJurisdictions();
  }, []);

  // Handle workflow selection
  const handleWorkflowChange = (event) => {
    const selectedWorkflow = event.target.value;
    setWorkflow(selectedWorkflow);
    setActiveStep(0);
    setStepContent({});
    
    if (selectedWorkflow) {
      fetchStepContent(selectedWorkflow, 0);
    }
  };

  // Handle jurisdiction change
  const handleJurisdictionChange = (event) => {
    setJurisdiction(event.target.value);
    
    if (workflow) {
      fetchStepContent(workflow, activeStep);
    }
  };

  // Handle step navigation
  const handleNext = () => {
    const nextStep = activeStep + 1;
    setActiveStep(nextStep);
    
    if (workflow && nextStep < WORKFLOWS[workflow].steps.length) {
      fetchStepContent(workflow, nextStep);
    }
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    fetchStepContent(workflow, 0);
  };

  // Fetch step content from the API
  const fetchStepContent = async (workflowId, stepIndex) => {
    if (!workflowId || stepIndex < 0 || !WORKFLOWS[workflowId]) return;
    
    const steps = WORKFLOWS[workflowId].steps;
    if (stepIndex >= steps.length) return;
    
    const stepName = steps[stepIndex];
    if (stepContent[stepName]) {
      // Content already loaded
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const domain = WORKFLOWS[workflowId].domains[0];
      
      const query = `Explain the ${stepName} stage of the ${WORKFLOWS[workflowId].title} procedure`;
      
      const response = await axios.post('/api/legal/chat/specialized', {
        message: query,
        domain: domain,
        jurisdiction: jurisdiction || undefined
      });
      
      const result = response.data.response || {};
      
      setStepContent(prevContent => ({
        ...prevContent,
        [stepName]: {
          text: result.text || 'Information not available.',
          citations: result.citations || [],
          resources: result.resources || []
        }
      }));
      
    } catch (err) {
      console.error('Error fetching step content:', err);
      setError('Failed to load information. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Render the currently active step content
  const renderStepContent = () => {
    if (!workflow || activeStep < 0 || activeStep >= WORKFLOWS[workflow].steps.length) {
      return <Typography>Please select a legal process to visualize.</Typography>;
    }
    
    const stepName = WORKFLOWS[workflow].steps[activeStep];
    const content = stepContent[stepName];
    
    if (loading) {
      return (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      );
    }
    
    if (!content) {
      return <Typography>Loading content...</Typography>;
    }
    
    return (
      <Box>
        <Typography variant="body1" paragraph>
          {content.text}
        </Typography>
        
        {content.citations && content.citations.length > 0 && (
          <Box mt={2}>
            <Typography variant="subtitle1" gutterBottom>
              Relevant Laws & Citations:
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {content.citations.map((citation, index) => (
                <Chip 
                  key={index}
                  label={citation.text}
                  color="primary"
                  variant="outlined"
                  size="small"
                />
              ))}
            </Box>
          </Box>
        )}
        
        {content.resources && content.resources.length > 0 && (
          <Box mt={3}>
            <Typography variant="subtitle1" gutterBottom>
              Helpful Resources:
            </Typography>
            <ul>
              {content.resources.map((resource, index) => (
                <li key={index}>
                  <Typography>
                    <strong>{resource.name}</strong>: {resource.description}
                    {resource.url && (
                      <Button
                        href={resource.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        size="small"
                        sx={{ ml: 1 }}
                      >
                        Visit
                      </Button>
                    )}
                  </Typography>
                </li>
              ))}
            </ul>
          </Box>
        )}
      </Box>
    );
  };

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto', p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        <RightsIcon sx={{ mr: 1, verticalAlign: 'top' }} />
        Legal Rights & Procedures Visualizer
      </Typography>
      
      <Typography variant="body1" paragraph>
        This tool helps you understand common legal processes step by step, with information specific to your jurisdiction.
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel id="workflow-select-label">Select Legal Process</InputLabel>
            <Select
              labelId="workflow-select-label"
              value={workflow}
              label="Select Legal Process"
              onChange={handleWorkflowChange}
            >
              <MenuItem value="">
                <em>Select a process</em>
              </MenuItem>
              {Object.entries(WORKFLOWS).map(([id, data]) => (
                <MenuItem key={id} value={id}>{data.title}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel id="jurisdiction-select-label">Jurisdiction (Optional)</InputLabel>
            <Select
              labelId="jurisdiction-select-label"
              value={jurisdiction}
              label="Jurisdiction (Optional)"
              onChange={handleJurisdictionChange}
            >
              <MenuItem value="">
                <em>General (Federal)</em>
              </MenuItem>
              {jurisdictions.map((j) => (
                <MenuItem key={j} value={j}>{j.replace('_', ' ')}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>
      
      {workflow && (
        <Card variant="outlined" sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              {WORKFLOWS[workflow].title}
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              {WORKFLOWS[workflow].description}
            </Typography>
            <Divider sx={{ my: 2 }} />
            
            <Stepper activeStep={activeStep} orientation="vertical">
              {WORKFLOWS[workflow].steps.map((step, index) => (
                <Step key={step}>
                  <StepLabel>
                    {step.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}
                  </StepLabel>
                  <StepContent>
                    {error ? (
                      <Alert severity="error" sx={{ mb: 2 }}>
                        {error}
                      </Alert>
                    ) : (
                      renderStepContent()
                    )}
                    <Box sx={{ mb: 2 }}>
                      <div>
                        <Button
                          variant="contained"
                          onClick={handleNext}
                          sx={{ mt: 1, mr: 1 }}
                          disabled={loading}
                        >
                          {index === WORKFLOWS[workflow].steps.length - 1 ? 'Finish' : 'Continue'}
                        </Button>
                        <Button
                          disabled={index === 0 || loading}
                          onClick={handleBack}
                          sx={{ mt: 1, mr: 1 }}
                        >
                          Back
                        </Button>
                      </div>
                    </Box>
                  </StepContent>
                </Step>
              ))}
            </Stepper>
            
            {activeStep === WORKFLOWS[workflow].steps.length && (
              <Paper square elevation={0} sx={{ p: 3 }}>
                <Typography>All steps completed - you've finished this guide.</Typography>
                <Button onClick={handleReset} sx={{ mt: 1, mr: 1 }}>
                  Start Over
                </Button>
              </Paper>
            )}
          </CardContent>
        </Card>
      )}
      
      {!workflow && (
        <Paper sx={{ p: 3, mt: 2 }}>
          <Typography align="center" color="textSecondary">
            Please select a legal process from the dropdown above to get started.
          </Typography>
        </Paper>
      )}
      
      <Alert severity="info" sx={{ mt: 3 }}>
        This information is for educational purposes only and should not be considered legal advice. 
        For specific guidance on your legal situation, please consult with a qualified attorney.
      </Alert>
    </Box>
  );
};

export default LegalRightsVisualizer; 
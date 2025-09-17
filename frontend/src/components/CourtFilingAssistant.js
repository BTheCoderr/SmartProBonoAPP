/**
 * Court Filing Assistant Component
 * Comprehensive court document preparation and filing interface
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Card,
  CardContent,
  CardActions,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Chip,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
  Badge
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  FileDownload as DownloadIcon,
  FileUpload as UploadIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Gavel as GavelIcon,
  Description as DocumentIcon,
  Schedule as ScheduleIcon,
  AttachMoney as MoneyIcon,
  Rule as RuleIcon,
  Template as TemplateIcon
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const CourtFilingAssistant = () => {
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  // Data states
  const [courtRules, setCourtRules] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [filings, setFilings] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [filingData, setFilingData] = useState({});
  const [generatedDocument, setGeneratedDocument] = useState('');
  
  // Form states
  const [jurisdiction, setJurisdiction] = useState('Rhode Island');
  const [court, setCourt] = useState('');
  const [documentType, setDocumentType] = useState('');
  const [filingTitle, setFilingTitle] = useState('');
  const [filingDescription, setFilingDescription] = useState('');
  
  // Dialog states
  const [templateDialogOpen, setTemplateDialogOpen] = useState(false);
  const [filingDialogOpen, setFilingDialogOpen] = useState(false);
  const [previewDialogOpen, setPreviewDialogOpen] = useState(false);

  const steps = [
    'Select Court & Document Type',
    'Choose Template',
    'Fill Document Data',
    'Review & Generate',
    'File with Court'
  ];

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      // Load court rules
      const rulesResponse = await fetch('http://localhost:3001/api/court-filing/rules');
      if (rulesResponse.ok) {
        const rulesData = await rulesResponse.json();
        setCourtRules(rulesData.rules || []);
      }

      // Load templates
      const templatesResponse = await fetch('http://localhost:3001/api/court-filing/templates');
      if (templatesResponse.ok) {
        const templatesData = await templatesResponse.json();
        setTemplates(templatesData.templates || []);
      }

      // Load existing filings
      const filingsResponse = await fetch('http://localhost:3001/api/court-filing/filings');
      if (filingsResponse.ok) {
        const filingsData = await filingsResponse.json();
        setFilings(filingsData.filings || []);
      }

    } catch (err) {
      console.error('Error loading initial data:', err);
      setError('Failed to load court filing data');
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setFilingData({});
    setGeneratedDocument('');
    setSelectedTemplate(null);
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setTemplateDialogOpen(false);
    handleNext();
  };

  const handleGenerateDocument = async () => {
    if (!selectedTemplate) {
      setError('Please select a template');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:3001/api/court-filing/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_id: selectedTemplate.id,
          data: filingData
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setGeneratedDocument(data.document_content);
      setSuccess('Document generated successfully');
      handleNext();

    } catch (err) {
      console.error('Error generating document:', err);
      setError('Failed to generate document');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFiling = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:3001/api/court-filing/filings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          case_id: filingData.case_id || 'CASE-001',
          document_type: documentType,
          title: filingTitle,
          description: filingDescription,
          court: court,
          jurisdiction: jurisdiction,
          filed_by: 'Current User',
          file_path: 'generated_document.pdf'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSuccess('Filing created successfully');
      setFilingDialogOpen(false);
      loadInitialData(); // Reload filings
      handleNext();

    } catch (err) {
      console.error('Error creating filing:', err);
      setError('Failed to create filing');
    } finally {
      setLoading(false);
    }
  };

  const handleFileDocument = async (filingId) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:3001/api/court-filing/filings/${filingId}/file`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          court_system: 'efiling'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSuccess('Document filed successfully');
      loadInitialData(); // Reload filings

    } catch (err) {
      console.error('Error filing document:', err);
      setError('Failed to file document');
    } finally {
      setLoading(false);
    }
  };

  const calculateFees = async () => {
    if (!documentType || !jurisdiction || !court) return;

    try {
      const response = await fetch('http://localhost:3001/api/court-filing/fees', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_type: documentType,
          jurisdiction: jurisdiction,
          court: court
        })
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(`Filing fee: $${data.fees}`);
      }
    } catch (err) {
      console.error('Error calculating fees:', err);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'draft': return 'default';
      case 'ready_to_file': return 'primary';
      case 'filed': return 'success';
      case 'accepted': return 'success';
      case 'rejected': return 'error';
      case 'amended': return 'warning';
      case 'withdrawn': return 'default';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'draft': return <EditIcon />;
      case 'ready_to_file': return <ScheduleIcon />;
      case 'filed': return <CheckIcon />;
      case 'accepted': return <CheckIcon />;
      case 'rejected': return <ErrorIcon />;
      case 'amended': return <WarningIcon />;
      case 'withdrawn': return <InfoIcon />;
      default: return <InfoIcon />;
    }
  };

  return (
    <Box sx={{ maxWidth: 1200, margin: '0 auto', p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <GavelIcon color="primary" />
        Court Filing Assistant
      </Typography>

      {/* Error/Success Messages */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Main Stepper */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stepper activeStep={activeStep} orientation="horizontal">
          {steps.map((label, index) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {/* Step Content */}
        <Box sx={{ mt: 3 }}>
          {/* Step 0: Select Court & Document Type */}
          {activeStep === 0 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Select Court and Document Type
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Jurisdiction</InputLabel>
                    <Select
                      value={jurisdiction}
                      onChange={(e) => setJurisdiction(e.target.value)}
                    >
                      <MenuItem value="Rhode Island">Rhode Island</MenuItem>
                      <MenuItem value="Massachusetts">Massachusetts</MenuItem>
                      <MenuItem value="Connecticut">Connecticut</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Court</InputLabel>
                    <Select
                      value={court}
                      onChange={(e) => setCourt(e.target.value)}
                    >
                      <MenuItem value="Superior Court">Superior Court</MenuItem>
                      <MenuItem value="District Court">District Court</MenuItem>
                      <MenuItem value="Family Court">Family Court</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Document Type</InputLabel>
                    <Select
                      value={documentType}
                      onChange={(e) => setDocumentType(e.target.value)}
                    >
                      <MenuItem value="complaint">Complaint</MenuItem>
                      <MenuItem value="motion">Motion</MenuItem>
                      <MenuItem value="answer">Answer</MenuItem>
                      <MenuItem value="brief">Brief</MenuItem>
                      <MenuItem value="notice">Notice</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
              <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  onClick={handleNext}
                  disabled={!jurisdiction || !court || !documentType}
                >
                  Next
                </Button>
                <Button onClick={calculateFees} disabled={!documentType || !jurisdiction || !court}>
                  Calculate Fees
                </Button>
              </Box>
            </Box>
          )}

          {/* Step 1: Choose Template */}
          {activeStep === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Choose Document Template
              </Typography>
              <Grid container spacing={2}>
                {templates
                  .filter(t => t.document_type === documentType && t.jurisdiction === jurisdiction)
                  .map((template) => (
                    <Grid item xs={12} md={6} key={template.id}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6">{template.name}</Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {template.description}
                          </Typography>
                          <Typography variant="body2" sx={{ mb: 1 }}>
                            <strong>Required Fields:</strong> {template.required_fields.join(', ')}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Instructions:</strong> {template.instructions}
                          </Typography>
                        </CardContent>
                        <CardActions>
                          <Button
                            variant="contained"
                            onClick={() => handleTemplateSelect(template)}
                            startIcon={<TemplateIcon />}
                          >
                            Use Template
                          </Button>
                        </CardActions>
                      </Card>
                    </Grid>
                  ))}
              </Grid>
              <Box sx={{ mt: 3 }}>
                <Button onClick={handleBack}>Back</Button>
              </Box>
            </Box>
          )}

          {/* Step 2: Fill Document Data */}
          {activeStep === 2 && selectedTemplate && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Fill Document Data
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Template: {selectedTemplate.name}
              </Typography>
              
              <Grid container spacing={3}>
                {selectedTemplate.required_fields.map((field) => (
                  <Grid item xs={12} md={6} key={field}>
                    <TextField
                      fullWidth
                      label={field.replace(/_/g, ' ').toUpperCase()}
                      value={filingData[field] || ''}
                      onChange={(e) => setFilingData(prev => ({
                        ...prev,
                        [field]: e.target.value
                      }))}
                      required
                    />
                  </Grid>
                ))}
                {selectedTemplate.optional_fields.map((field) => (
                  <Grid item xs={12} md={6} key={field}>
                    <TextField
                      fullWidth
                      label={field.replace(/_/g, ' ').toUpperCase()}
                      value={filingData[field] || ''}
                      onChange={(e) => setFilingData(prev => ({
                        ...prev,
                        [field]: e.target.value
                      }))}
                    />
                  </Grid>
                ))}
              </Grid>
              
              <Box sx={{ mt: 3 }}>
                <TextField
                  fullWidth
                  label="Filing Title"
                  value={filingTitle}
                  onChange={(e) => setFilingTitle(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Filing Description"
                  value={filingDescription}
                  onChange={(e) => setFilingDescription(e.target.value)}
                />
              </Box>
              
              <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                <Button onClick={handleBack}>Back</Button>
                <Button
                  variant="contained"
                  onClick={handleGenerateDocument}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <DocumentIcon />}
                >
                  {loading ? 'Generating...' : 'Generate Document'}
                </Button>
              </Box>
            </Box>
          )}

          {/* Step 3: Review & Generate */}
          {activeStep === 3 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Review Generated Document
              </Typography>
              
              <Paper sx={{ p: 2, mb: 3, maxHeight: 400, overflow: 'auto' }}>
                <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                  {generatedDocument}
                </Typography>
              </Paper>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  variant="outlined"
                  onClick={() => setPreviewDialogOpen(true)}
                  startIcon={<DocumentIcon />}
                >
                  Preview Full Document
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => {
                    const blob = new Blob([generatedDocument], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${filingTitle || 'document'}.txt`;
                    a.click();
                    URL.revokeObjectURL(url);
                  }}
                  startIcon={<DownloadIcon />}
                >
                  Download
                </Button>
              </Box>
              
              <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                <Button onClick={handleBack}>Back</Button>
                <Button
                  variant="contained"
                  onClick={() => setFilingDialogOpen(true)}
                  startIcon={<GavelIcon />}
                >
                  Create Filing
                </Button>
              </Box>
            </Box>
          )}

          {/* Step 4: File with Court */}
          {activeStep === 4 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                File with Court
              </Typography>
              
              <Alert severity="info" sx={{ mb: 3 }}>
                Your document has been prepared and is ready for filing. Review the filing details below and proceed with court submission.
              </Alert>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button onClick={handleBack}>Back</Button>
                <Button
                  variant="contained"
                  onClick={handleReset}
                  startIcon={<CheckIcon />}
                >
                  Complete Process
                </Button>
              </Box>
            </Box>
          )}
        </Box>
      </Paper>

      {/* Existing Filings */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <DocumentIcon color="primary" />
          Existing Filings
        </Typography>
        
        {filings.length === 0 ? (
          <Typography color="text.secondary">No filings found</Typography>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Court</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filings.map((filing) => (
                  <TableRow key={filing.id}>
                    <TableCell>{filing.title}</TableCell>
                    <TableCell>{filing.document_type}</TableCell>
                    <TableCell>{filing.court}</TableCell>
                    <TableCell>
                      <Chip
                        label={filing.status}
                        color={getStatusColor(filing.status)}
                        icon={getStatusIcon(filing.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {new Date(filing.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <Tooltip title="View Details">
                          <IconButton size="small">
                            <InfoIcon />
                          </IconButton>
                        </Tooltip>
                        {filing.status === 'ready_to_file' && (
                          <Tooltip title="File Document">
                            <IconButton
                              size="small"
                              onClick={() => handleFileDocument(filing.id)}
                              disabled={loading}
                            >
                              <GavelIcon />
                            </IconButton>
                          </Tooltip>
                        )}
                        <Tooltip title="Download">
                          <IconButton size="small">
                            <DownloadIcon />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      {/* Template Selection Dialog */}
      <Dialog
        open={templateDialogOpen}
        onClose={() => setTemplateDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Select Template</DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            {templates.map((template) => (
              <Grid item xs={12} md={6} key={template.id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">{template.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {template.description}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button onClick={() => handleTemplateSelect(template)}>
                      Select
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
      </Dialog>

      {/* Filing Creation Dialog */}
      <Dialog
        open={filingDialogOpen}
        onClose={() => setFilingDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create Court Filing</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Filing Title"
            value={filingTitle}
            onChange={(e) => setFilingTitle(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Description"
            value={filingDescription}
            onChange={(e) => setFilingDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFilingDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleCreateFiling}
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Create Filing'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Document Preview Dialog */}
      <Dialog
        open={previewDialogOpen}
        onClose={() => setPreviewDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>Document Preview</DialogTitle>
        <DialogContent>
          <Paper sx={{ p: 2, maxHeight: 600, overflow: 'auto' }}>
            <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
              {generatedDocument}
            </Typography>
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewDialogOpen(false)}>Close</Button>
          <Button
            variant="contained"
            onClick={() => {
              const blob = new Blob([generatedDocument], { type: 'text/plain' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `${filingTitle || 'document'}.txt`;
              a.click();
              URL.revokeObjectURL(url);
            }}
          >
            Download
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CourtFilingAssistant;

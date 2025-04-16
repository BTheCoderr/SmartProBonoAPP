import React, { useState, useCallback } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  TextField, 
  Divider, 
  Grid, 
  LinearProgress, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Card, 
  CardHeader, 
  CardContent, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon, 
  Tab, 
  Tabs, 
  IconButton,
  Alert,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { 
  CloudUpload as CloudUploadIcon, 
  DescriptionOutlined as DocumentIcon, 
  DeleteOutline as DeleteIcon, 
  InfoOutlined as InfoIcon,
  AccessTime as TimeIcon,
  Language as JurisdictionIcon,
  Gavel as LegalIcon,
  Article as ArticleIcon,
  Person as PersonIcon,
  Description as DescriptionIcon,
  Event as EventIcon,
  ExpandMore as ExpandMoreIcon,
  AttachMoney as MoneyIcon
} from '@mui/icons-material';
import axios from 'axios';

// Styled components
const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const DocTypeChip = styled(Chip)(({ theme, doctype }) => ({
  backgroundColor: 
    doctype === 'contract' ? theme.palette.primary.light : 
    doctype === 'lease' ? theme.palette.secondary.light :
    doctype === 'legal_brief' ? theme.palette.info.light :
    doctype === 'immigration_form' ? theme.palette.warning.light :
    theme.palette.grey[300],
  color: 
    doctype === 'contract' ? theme.palette.primary.contrastText : 
    doctype === 'lease' ? theme.palette.secondary.contrastText :
    doctype === 'legal_brief' ? theme.palette.info.contrastText :
    doctype === 'immigration_form' ? theme.palette.warning.contrastText :
    theme.palette.text.primary,
  fontWeight: 'bold'
}));

const LegalDocumentAnalyzer = () => {
  // State
  const [file, setFile] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [documentType, setDocumentType] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  
  // Document type options
  const docTypes = [
    { value: 'contract', label: 'Contract' },
    { value: 'lease', label: 'Lease Agreement' },
    { value: 'legal_brief', label: 'Legal Brief' },
    { value: 'immigration_form', label: 'Immigration Form' },
    { value: 'other', label: 'Other Document' }
  ];
  
  // Handle file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setTextInput(''); // Clear text input when file is selected
      
      // Try to guess document type from filename
      if (!documentType) {
        const fileName = selectedFile.name.toLowerCase();
        if (fileName.includes('lease') || fileName.includes('rental')) {
          setDocumentType('lease');
        } else if (fileName.includes('contract') || fileName.includes('agreement')) {
          setDocumentType('contract');
        } else if (fileName.includes('brief') || fileName.includes('motion')) {
          setDocumentType('legal_brief');
        } else if (fileName.includes('immigration') || fileName.includes('form')) {
          setDocumentType('immigration_form');
        }
      }
    }
  };
  
  // Handle text input change
  const handleTextChange = (event) => {
    setTextInput(event.target.value);
    setFile(null); // Clear file when text is entered
  };
  
  // Handle document type selection
  const handleDocTypeChange = (event) => {
    setDocumentType(event.target.value);
  };
  
  // Handle tab change (File/Text)
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    if (newValue === 0) {
      setTextInput('');
    } else {
      setFile(null);
    }
  };
  
  // Reset everything
  const handleReset = () => {
    setFile(null);
    setTextInput('');
    setDocumentType('');
    setAnalysisResults(null);
    setError(null);
  };
  
  // Analyze document
  const analyzeDocument = useCallback(async () => {
    setError(null);
    setIsAnalyzing(true);
    setUploadProgress(0);
    
    try {
      let response;
      
      if (file) {
        // File upload approach
        const formData = new FormData();
        formData.append('file', file);
        if (documentType) {
          formData.append('document_type', documentType);
        }
        
        response = await axios.post(
          '/api/legal/analyze/document', 
          formData, 
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              setUploadProgress(percentCompleted);
            }
          }
        );
      } else if (textInput) {
        // Text input approach
        response = await axios.post('/api/legal/analyze/document', {
          text: textInput,
          document_type: documentType || undefined
        });
      } else {
        throw new Error('Please provide either a file or text to analyze');
      }
      
      setAnalysisResults(response.data);
    } catch (err) {
      console.error('Error analyzing document:', err);
      setError(err.response?.data?.error || err.message || 'An unknown error occurred');
    } finally {
      setIsAnalyzing(false);
      setUploadProgress(0);
    }
  }, [file, textInput, documentType]);
  
  // Render analysis results
  const renderAnalysisResults = () => {
    if (!analysisResults) return null;
    
    return (
      <Box mt={4}>
        <Typography variant="h5" gutterBottom>
          Analysis Results
        </Typography>
        
        <Grid container spacing={3}>
          {/* Document overview */}
          <Grid item xs={12} md={6}>
            <Card variant="outlined">
              <CardHeader 
                title="Document Overview" 
                avatar={<DocumentIcon color="primary" />}
              />
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Typography variant="subtitle1" component="span">
                      Document Type: 
                    </Typography>
                    <DocTypeChip 
                      label={analysisResults.document_type || 'General Document'}
                      doctype={analysisResults.document_type}
                      icon={<DescriptionIcon />}
                    />
                  </Grid>
                  
                  {analysisResults.complexity && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle1">
                        Complexity Level: {analysisResults.complexity.level || 'N/A'}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Readability score: {analysisResults.complexity.readability_score?.toFixed(1) || 'N/A'}
                      </Typography>
                    </Grid>
                  )}
                  
                  {analysisResults.jurisdiction && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle1">
                        <JurisdictionIcon fontSize="small" sx={{ mr: 1 }} />
                        Jurisdiction: {analysisResults.jurisdiction.name || 'N/A'}
                      </Typography>
                    </Grid>
                  )}
                  
                  {analysisResults.dates && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle1">
                        <EventIcon fontSize="small" sx={{ mr: 1 }} />
                        Key Dates:
                      </Typography>
                      <List dense>
                        {Object.entries(analysisResults.dates).map(([key, value]) => (
                          <ListItem key={key}>
                            <ListItemText 
                              primary={`${key.replace('_', ' ')}: ${value}`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                  )}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Entities & Parties */}
          <Grid item xs={12} md={6}>
            <Card variant="outlined">
              <CardHeader 
                title="Parties & Entities" 
                avatar={<PersonIcon color="primary" />}
              />
              <CardContent>
                {analysisResults.parties ? (
                  <List dense>
                    {analysisResults.parties.map((party, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <PersonIcon />
                        </ListItemIcon>
                        <ListItemText 
                          primary={party.name || 'Unnamed Party'} 
                          secondary={party.role || 'Unknown Role'}
                        />
                      </ListItem>
                    ))}
                  </List>
                ) : analysisResults.entities ? (
                  <Box>
                    {Object.entries(analysisResults.entities).map(([category, items]) => (
                      <Box key={category} mb={2}>
                        <Typography variant="subtitle1">
                          {category.replace('_', ' ')}:
                        </Typography>
                        <Box display="flex" flexWrap="wrap" gap={1} mt={1}>
                          {items.map((item, i) => (
                            <Chip key={i} label={item} size="small" />
                          ))}
                        </Box>
                      </Box>
                    ))}
                  </Box>
                ) : (
                  <Typography variant="body2" color="textSecondary">
                    No party or entity information detected
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          
          {/* Key Terms & Provisions */}
          {(analysisResults.clauses || analysisResults.key_terms || analysisResults.obligations) && (
            <Grid item xs={12}>
              <Card variant="outlined">
                <CardHeader 
                  title="Key Terms & Provisions" 
                  avatar={<ArticleIcon color="primary" />}
                />
                <CardContent>
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography>Key Clauses and Terms</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      {analysisResults.clauses ? (
                        <Grid container spacing={2}>
                          {Object.entries(analysisResults.clauses).map(([clause, text]) => (
                            <Grid item xs={12} key={clause}>
                              <Typography variant="subtitle2">{clause.replace('_', ' ')}:</Typography>
                              <Typography variant="body2">{text}</Typography>
                            </Grid>
                          ))}
                        </Grid>
                      ) : analysisResults.key_terms ? (
                        <List dense>
                          {analysisResults.key_terms.map((term, index) => (
                            <ListItem key={index}>
                              <ListItemText primary={term} />
                            </ListItem>
                          ))}
                        </List>
                      ) : (
                        <Typography>No key terms identified</Typography>
                      )}
                    </AccordionDetails>
                  </Accordion>
                  
                  {analysisResults.obligations && (
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography>Obligations & Requirements</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <List dense>
                          {analysisResults.obligations.map((obligation, index) => (
                            <ListItem key={index}>
                              <ListItemText primary={obligation} />
                            </ListItem>
                          ))}
                        </List>
                      </AccordionDetails>
                    </Accordion>
                  )}
                  
                  {analysisResults.financial_terms && (
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography>
                          <MoneyIcon fontSize="small" sx={{ mr: 1, verticalAlign: 'middle' }} />
                          Financial Terms
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <List dense>
                          {Object.entries(analysisResults.financial_terms).map(([term, value]) => (
                            <ListItem key={term}>
                              <ListItemText 
                                primary={`${term.replace('_', ' ')}: ${value}`}
                              />
                            </ListItem>
                          ))}
                        </List>
                      </AccordionDetails>
                    </Accordion>
                  )}
                </CardContent>
              </Card>
            </Grid>
          )}
          
          {/* Legal Implications */}
          {analysisResults.legal_issues && (
            <Grid item xs={12}>
              <Card variant="outlined">
                <CardHeader 
                  title="Legal Implications & Issues" 
                  avatar={<LegalIcon color="primary" />}
                />
                <CardContent>
                  <List dense>
                    {analysisResults.legal_issues.map((issue, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <InfoIcon color={issue.severity === 'high' ? 'error' : issue.severity === 'medium' ? 'warning' : 'info'} />
                        </ListItemIcon>
                        <ListItemText 
                          primary={issue.description} 
                          secondary={issue.recommendation || ''}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          )}
          
          {/* Disclaimer */}
          <Grid item xs={12}>
            <Alert severity="info">
              {analysisResults.disclaimer || 
                'This document analysis is provided for informational purposes only and should not be considered legal advice.'}
            </Alert>
          </Grid>
        </Grid>
      </Box>
    );
  };
  
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Legal Document Analyzer
      </Typography>
      
      <Typography variant="body1" paragraph>
        Upload a legal document or paste text to analyze its structure, extract key information, and identify important legal provisions.
      </Typography>
      
      <Paper sx={{ p: 3, mt: 3 }}>
        {/* Input Tabs (File/Text) */}
        <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 2 }}>
          <Tab label="Upload Document" />
          <Tab label="Paste Text" />
        </Tabs>
        
        {/* File Upload */}
        {activeTab === 0 && (
          <Box>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
              <Button
                component="label"
                variant="contained"
                startIcon={<CloudUploadIcon />}
                sx={{ mb: 2 }}
              >
                Select Document
                <VisuallyHiddenInput 
                  type="file" 
                  accept=".pdf,.docx,.doc,.txt,.rtf" 
                  onChange={handleFileChange}
                />
              </Button>
              
              {file && (
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
                  <DocumentIcon sx={{ mr: 1 }} />
                  <Typography variant="body1">{file.name}</Typography>
                  <IconButton 
                    size="small" 
                    onClick={() => setFile(null)}
                    sx={{ ml: 1 }}
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </Box>
              )}
            </Box>
          </Box>
        )}
        
        {/* Text Input */}
        {activeTab === 1 && (
          <TextField
            fullWidth
            multiline
            rows={10}
            variant="outlined"
            label="Paste document text here"
            value={textInput}
            onChange={handleTextChange}
          />
        )}
        
        {/* Document Type Selection */}
        <FormControl fullWidth sx={{ mt: 3 }}>
          <InputLabel id="document-type-label">Document Type (Optional)</InputLabel>
          <Select
            labelId="document-type-label"
            id="document-type"
            value={documentType}
            label="Document Type (Optional)"
            onChange={handleDocTypeChange}
          >
            <MenuItem value="">
              <em>Auto-detect</em>
            </MenuItem>
            {docTypes.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        
        {/* Error messages */}
        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {error}
          </Alert>
        )}
        
        {/* Upload Progress */}
        {uploadProgress > 0 && (
          <Box sx={{ width: '100%', mt: 3 }}>
            <LinearProgress 
              variant="determinate" 
              value={uploadProgress} 
            />
            <Typography variant="body2" align="center" sx={{ mt: 1 }}>
              {uploadProgress}% uploaded
            </Typography>
          </Box>
        )}
        
        {/* Actions */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
          <Button 
            variant="outlined" 
            onClick={handleReset}
            disabled={isAnalyzing}
          >
            Reset
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={analyzeDocument}
            disabled={isAnalyzing || (!file && !textInput)}
            startIcon={isAnalyzing ? null : <LegalIcon />}
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze Document'}
          </Button>
        </Box>
        
        {/* Loading indicator */}
        {isAnalyzing && (
          <Box sx={{ mt: 3 }}>
            <LinearProgress />
            <Typography variant="body2" align="center" sx={{ mt: 1 }}>
              Analyzing document... This may take a moment.
            </Typography>
          </Box>
        )}
      </Paper>
      
      {/* Analysis Results Section */}
      {renderAnalysisResults()}
    </Box>
  );
};

export default LegalDocumentAnalyzer; 
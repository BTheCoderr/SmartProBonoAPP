import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Divider,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Tab,
  Tabs,
  TextField,
  Typography,
  Alert,
  IconButton,
  Tooltip,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Upload as UploadIcon,
  ContentPaste as PasteIcon,
  Help as HelpIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const VisuallyHiddenInput = styled('input')`
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  bottom: 0;
  left: 0;
  white-space: nowrap;
  width: 1px;
`;

const DocumentAnalyzer = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState(0);
  const [documentText, setDocumentText] = useState('');
  const [documentType, setDocumentType] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [supportedTypes, setSupportedTypes] = useState([]);

  // Fetch supported document types on component mount
  useEffect(() => {
    fetchSupportedTypes();
  }, []);

  const fetchSupportedTypes = async () => {
    try {
      const response = await fetch('/api/document-analysis/supported-types');
      const data = await response.json();
      setSupportedTypes(data.supported_types);
    } catch (err) {
      setError('Failed to fetch supported document types');
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setError(null);
    setAnalysis(null);
  };

  const handleFileUpload = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      if (uploadedFile.size > 10 * 1024 * 1024) { // 10MB limit
        setError('File size exceeds 10MB limit');
        return;
      }
      setFile(uploadedFile);
      setError(null);
    }
  };

  const handleTextInput = (event) => {
    setDocumentText(event.target.value);
    setError(null);
  };

  const handleTypeChange = (event) => {
    setDocumentType(event.target.value);
  };

  const analyzeDocument = async () => {
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const formData = new FormData();
      if (activeTab === 0 && file) {
        formData.append('file', file);
      } else if (activeTab === 1 && documentText) {
        formData.append('document_text', documentText);
      } else {
        setError('Please provide a document to analyze');
        setLoading(false);
        return;
      }

      if (documentType) {
        formData.append('document_type', documentType);
      }

      const response = await fetch('/api/document-analysis/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Analysis failed');
      }

      setAnalysis(data.analysis);
    } catch (err) {
      setError(err.message || 'Failed to analyze document');
    } finally {
      setLoading(false);
    }
  };

  const renderAnalysisResults = () => {
    if (!analysis) return null;

    return (
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Analysis Results
          </Typography>
          
          {/* Basic Analysis */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" color="primary">
              Basic Analysis
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="body2">
                    Document Type: {analysis.document_type}
                  </Typography>
                  <Typography variant="body2">
                    Length: {analysis.basic_analysis.length} characters
                  </Typography>
                  <Typography variant="body2">
                    Reading Ease: {analysis.basic_analysis.complexity_metrics.flesch_reading_ease.toFixed(2)}
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Box>

          {/* Named Entities */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" color="primary">
              Named Entities
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(analysis.basic_analysis.named_entities).map(([type, entities]) => (
                <Grid item xs={12} md={6} key={type}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      {type.replace('_', ' ').toUpperCase()}
                    </Typography>
                    {entities.map((entity, index) => (
                      <Typography key={index} variant="body2">
                        • {entity}
                      </Typography>
                    ))}
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Box>

          {/* Document-Specific Analysis */}
          {analysis.contract_analysis && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" color="primary">
                Contract Analysis
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Parties
                    </Typography>
                    {analysis.contract_analysis.parties.map((party, index) => (
                      <Typography key={index} variant="body2">
                        • {party}
                      </Typography>
                    ))}
                  </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Key Dates
                    </Typography>
                    {Object.entries(analysis.contract_analysis.dates).map(([type, date]) => (
                      <Typography key={type} variant="body2">
                        • {type}: {date}
                      </Typography>
                    ))}
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Document Analysis
      </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload or paste your legal document for AI-powered analysis
      </Typography>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs value={activeTab} onChange={handleTabChange}>
          <Tab label="Upload File" icon={<UploadIcon />} />
          <Tab label="Paste Text" icon={<PasteIcon />} />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {activeTab === 0 ? (
            <Box sx={{ textAlign: 'center' }}>
              <Button
                component="label"
                variant="contained"
                startIcon={<UploadIcon />}
              >
                Upload Document
                <VisuallyHiddenInput
                  type="file"
                  onChange={handleFileUpload}
                  accept=".txt,.pdf,.doc,.docx"
                />
              </Button>
              {file && (
                <Typography variant="body2" sx={{ mt: 2 }}>
                  Selected file: {file.name}
                </Typography>
              )}
            </Box>
          ) : (
            <TextField
              fullWidth
              multiline
              rows={6}
              value={documentText}
              onChange={handleTextInput}
              placeholder="Paste your document text here..."
            />
          )}

          <FormControl fullWidth sx={{ mt: 3 }}>
            <InputLabel>Document Type (Optional)</InputLabel>
            <Select
              value={documentType}
              onChange={handleTypeChange}
              label="Document Type (Optional)"
            >
              <MenuItem value="">
                <em>Auto-detect</em>
              </MenuItem>
              {Object.entries(supportedTypes).map(([type, info]) => (
                <MenuItem key={type} value={type}>
                  {info.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
              <Button
                variant="contained"
              onClick={analyzeDocument}
              disabled={loading || (!file && !documentText)}
              startIcon={loading ? <CircularProgress size={20} /> : null}
            >
              {loading ? 'Analyzing...' : 'Analyze Document'}
              </Button>
            </Box>
        </Box>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {renderAnalysisResults()}
    </Container>
  );
};

export default DocumentAnalyzer;
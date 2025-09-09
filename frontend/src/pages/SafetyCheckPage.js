import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Button,
  TextField,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import {
  Security as SecurityIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Info as InfoIcon
} from '@mui/icons-material';

const SafetyCheckPage = () => {
  const [text, setText] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;

    setAnalyzing(true);
    setError(null);
    setResults(null);

    try {
      // Create a temporary file for the API call
      const formData = new FormData();
      const blob = new Blob([text], { type: 'text/plain' });
      formData.append('file', blob, 'safety-check.txt');
      formData.append('document_type', 'safety_check');

      const response = await fetch('http://localhost:3001/api/scanner/analyze-safe', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        setResults(data.analysis);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Failed to analyze text. Please try again.');
      console.error('Safety check error:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const renderResults = () => {
    if (!results) return null;

    return (
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <SecurityIcon sx={{ mr: 1 }} />
            Safety Analysis Results
          </Typography>

          {results.escalation_needed && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              <strong>Escalation Recommended:</strong> This content may require professional legal review.
            </Alert>
          )}

          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <strong>Summary:</strong>
            </Typography>
            <Typography variant="body2" paragraph>
              {results.client_summary || 'No summary available'}
            </Typography>
          </Box>

          {results.recommendations && results.recommendations.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Recommendations:</strong>
              </Typography>
              <List dense>
                {results.recommendations.map((rec, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <InfoIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={rec} />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}

          {results.risk_level && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Risk Level:</strong>
              </Typography>
              <Chip
                label={results.risk_level}
                color={
                  results.risk_level.toLowerCase().includes('high') ? 'error' :
                  results.risk_level.toLowerCase().includes('medium') ? 'warning' : 'success'
                }
                icon={
                  results.risk_level.toLowerCase().includes('high') ? <WarningIcon /> :
                  results.risk_level.toLowerCase().includes('medium') ? <WarningIcon /> : <CheckIcon />
                }
              />
            </Box>
          )}

          {results.safety_checked && (
            <Alert severity="success" sx={{ mt: 2 }}>
              <strong>Safety Check Complete:</strong> This analysis has been reviewed for compliance and safety.
            </Alert>
          )}
        </CardContent>
      </Card>
    );
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <SecurityIcon color="primary" sx={{ mr: 2, fontSize: 32 }} />
          <Typography variant="h4" component="h1">
            Legal Safety Check
          </Typography>
        </Box>

        <Typography variant="body1" paragraph>
          Use this tool to analyze your legal content for compliance, safety, and potential issues. 
          Our AI will review your text and provide recommendations for improvement.
        </Typography>

        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={6}
            variant="outlined"
            label="Enter text to analyze"
            placeholder="Paste your legal document, contract, or any text you'd like to check for legal compliance and safety..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            sx={{ mb: 2 }}
          />

          <Button
            variant="contained"
            size="large"
            onClick={handleAnalyze}
            disabled={!text.trim() || analyzing}
            startIcon={analyzing ? <CircularProgress size={20} /> : <SecurityIcon />}
            sx={{ minWidth: 200 }}
          >
            {analyzing ? 'Analyzing...' : 'Check Safety'}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {renderResults()}
      </Paper>
    </Container>
  );
};

export default SafetyCheckPage;

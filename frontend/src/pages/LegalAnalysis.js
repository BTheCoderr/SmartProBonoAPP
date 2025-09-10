import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Alert, 
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Divider
} from '@mui/material';
import CaseInputForm from '../components/CaseInputForm';
import { formatAIResponse } from '../components/ImprovedLegalAIChat';

const LegalAnalysis = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async ({ text, jurisdiction }) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Call the search API
      const searchResponse = await fetch('/api/searchCase', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, jurisdiction })
      });

      const searchData = await searchResponse.json();
      
      if (searchData.success) {
        setResult(searchData);
        
        // Save to Supabase
        try {
          await fetch('/api/saveQuery', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              text, 
              jurisdiction, 
              results: searchData 
            })
          });
        } catch (saveError) {
          console.warn('Failed to save query:', saveError);
          // Don't fail the whole request if save fails
        }
      } else {
        setError(searchData.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to analyze your case');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          SmartProBono Legal Analysis
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Get AI-powered legal research and case analysis
        </Typography>
      </Box>

      <CaseInputForm onSubmit={handleSubmit} loading={loading} />

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ ml: 2, alignSelf: 'center' }}>
            Analyzing your case...
          </Typography>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" component="h2" sx={{ flexGrow: 1 }}>
                Legal Analysis Results
              </Typography>
              <Chip 
                label={result.jurisdiction?.toUpperCase() || 'RI'} 
                color="primary" 
                variant="outlined" 
              />
            </Box>
            
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ whiteSpace: 'pre-wrap' }}>
              {formatAIResponse(result)}
            </Box>
          </CardContent>
        </Card>
      )}

      {result?.disclaimers && result.disclaimers.length > 0 && (
        <Alert severity="info" sx={{ mt: 2 }}>
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

export default LegalAnalysis;

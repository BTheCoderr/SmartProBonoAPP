import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Chip,
  Collapse,
  IconButton,
  LinearProgress
} from '@mui/material';
import { 
  FindInPage as ScanIcon, 
  Description as DocumentIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckCircleIcon,
  FormatQuote as QuoteIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

// Styled component for expandable sections
const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

const DocumentScanner = ({ document, onAnalysisComplete }) => {
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState({});

  // Toggle expansion of sections
  const handleExpandClick = (section) => {
    setExpanded({
      ...expanded,
      [section]: !expanded[section]
    });
  };

  // Mock document scanning function
  const scanDocument = async () => {
    setScanning(true);
    setProgress(0);
    setResult(null);
    setError(null);
    
    try {
      // Simulate scanning progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 95) {
            clearInterval(progressInterval);
            return 95;
          }
          return prev + Math.floor(Math.random() * 10);
        });
      }, 500);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      clearInterval(progressInterval);
      setProgress(100);
      
      // Mock scan result
      const scanResult = {
        documentType: 'Legal Contract',
        confidence: 92,
        pageCount: 5,
        wordCount: 2458,
        language: 'English',
        hasSignatures: true,
        dateIdentified: '2023-06-15',
        parties: [
          { name: 'ABC Corporation', type: 'Company', role: 'Provider' },
          { name: 'John Smith', type: 'Individual', role: 'Client' }
        ],
        keyTerms: [
          { term: 'Payment Terms', description: 'Net 30 days from invoice date', risk: 'low' },
          { term: 'Termination Clause', description: '30 day written notice required', risk: 'medium' },
          { term: 'Liability Limitation', description: 'Capped at contract value', risk: 'high' },
          { term: 'Governing Law', description: 'State of California', risk: 'low' }
        ],
        potentialIssues: [
          { issue: 'Ambiguous renewal terms', severity: 'medium', explanation: 'Section 8.3 contains contradictory statements about automatic renewal' },
          { issue: 'Unbalanced liability provisions', severity: 'high', explanation: 'One-sided indemnification may be unenforceable' }
        ],
        keyExcerpts: [
          { text: 'Provider shall not be liable for any indirect, special, or consequential damages.', section: 'Liability', page: 3 },
          { text: 'This Agreement shall automatically renew for successive one-year terms unless terminated by either party.', section: 'Term', page: 2 },
        ],
        recommendations: [
          'Review liability cap and consider negotiating higher limit',
          'Clarify renewal terms to avoid unintended auto-renewal',
          'Ensure indemnification provisions are mutual where appropriate'
        ]
      };
      
      setResult(scanResult);
      
      // Call the callback if provided
      if (onAnalysisComplete) {
        onAnalysisComplete(scanResult);
      }
    } catch (err) {
      setError('Failed to analyze document. Please try again.');
      console.error('Document scanning error:', err);
    } finally {
      setScanning(false);
    }
  };

  const renderScanResults = () => {
    if (!result) return null;
    
    return (
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Document Analysis Results
        </Typography>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          <Chip icon={<DocumentIcon />} label={`Type: ${result.documentType}`} />
          <Chip icon={<InfoIcon />} label={`Pages: ${result.pageCount}`} />
          <Chip icon={<InfoIcon />} label={`Words: ${result.wordCount}`} />
          <Chip 
            icon={<CheckCircleIcon />} 
            label={`Confidence: ${result.confidence}%`}
            color={result.confidence > 85 ? 'success' : 'warning'}
          />
        </Box>
        
        {/* Parties */}
        <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }} onClick={() => handleExpandClick('parties')}>
            <Typography variant="subtitle1" fontWeight="bold">
              Identified Parties
            </Typography>
            <ExpandMore
              expand={expanded.parties}
              onClick={() => handleExpandClick('parties')}
              aria-label="show more"
            >
              <ExpandMoreIcon />
            </ExpandMore>
          </Box>
          
          <Collapse in={expanded.parties || false} timeout="auto" unmountOnExit>
            <List dense>
              {result.parties.map((party, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={party.name}
                    secondary={`${party.type} • ${party.role}`}
                  />
                </ListItem>
              ))}
            </List>
          </Collapse>
        </Paper>
        
        {/* Key Terms */}
        <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }} onClick={() => handleExpandClick('terms')}>
            <Typography variant="subtitle1" fontWeight="bold">
              Key Terms & Provisions
            </Typography>
            <ExpandMore
              expand={expanded.terms}
              onClick={() => handleExpandClick('terms')}
              aria-label="show more"
            >
              <ExpandMoreIcon />
            </ExpandMore>
          </Box>
          
          <Collapse in={expanded.terms || false} timeout="auto" unmountOnExit>
            <List dense>
              {result.keyTerms.map((term, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    {term.risk === 'high' ? (
                      <WarningIcon color="error" />
                    ) : term.risk === 'medium' ? (
                      <WarningIcon color="warning" />
                    ) : (
                      <InfoIcon color="success" />
                    )}
                  </ListItemIcon>
                  <ListItemText 
                    primary={term.term}
                    secondary={term.description}
                  />
                  <Chip 
                    size="small" 
                    label={term.risk.toUpperCase()} 
                    color={
                      term.risk === 'high' ? 'error' : 
                      term.risk === 'medium' ? 'warning' : 
                      'success'
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Collapse>
        </Paper>
        
        {/* Potential Issues */}
        <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }} onClick={() => handleExpandClick('issues')}>
            <Typography variant="subtitle1" fontWeight="bold" color="error">
              Potential Issues
            </Typography>
            <ExpandMore
              expand={expanded.issues}
              onClick={() => handleExpandClick('issues')}
              aria-label="show more"
            >
              <ExpandMoreIcon />
            </ExpandMore>
          </Box>
          
          <Collapse in={expanded.issues || false} timeout="auto" unmountOnExit>
            {result.potentialIssues.length > 0 ? (
              <List dense>
                {result.potentialIssues.map((issue, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <WarningIcon color={issue.severity === 'high' ? 'error' : 'warning'} />
                    </ListItemIcon>
                    <ListItemText 
                      primary={issue.issue}
                      secondary={issue.explanation}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Alert severity="success">No significant issues detected</Alert>
            )}
          </Collapse>
        </Paper>
        
        {/* Key Excerpts */}
        <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }} onClick={() => handleExpandClick('excerpts')}>
            <Typography variant="subtitle1" fontWeight="bold">
              Important Excerpts
            </Typography>
            <ExpandMore
              expand={expanded.excerpts}
              onClick={() => handleExpandClick('excerpts')}
              aria-label="show more"
            >
              <ExpandMoreIcon />
            </ExpandMore>
          </Box>
          
          <Collapse in={expanded.excerpts || false} timeout="auto" unmountOnExit>
            <List dense>
              {result.keyExcerpts.map((excerpt, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <QuoteIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={excerpt.text}
                    secondary={`${excerpt.section} - Page ${excerpt.page}`}
                  />
                </ListItem>
              ))}
            </List>
          </Collapse>
        </Paper>
        
        {/* Recommendations */}
        <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#f9f9ff' }}>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            Recommendations
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <List dense>
            {result.recommendations.map((rec, index) => (
              <ListItem key={index}>
                <ListItemIcon>
                  <CheckCircleIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary={rec} />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Box>
    );
  };

  return (
    <Box>
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ScanIcon sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6">
            Document Scanner
          </Typography>
        </Box>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          Our AI-powered document scanner will analyze your document for key legal terms, potential issues, and provide recommendations.
        </Typography>
        
        {document && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Selected Document:
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', p: 1, bgcolor: 'background.paper', borderRadius: 1 }}>
              <DocumentIcon color="action" sx={{ mr: 1 }} />
              <Typography variant="body2" sx={{ flexGrow: 1, fontWeight: 'medium' }}>
                {document.name || 'Unnamed Document'}
              </Typography>
              <Chip label={document.type || 'Document'} size="small" />
            </Box>
          </Box>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {scanning && (
          <Box sx={{ width: '100%', mb: 2 }}>
            <LinearProgress variant="determinate" value={progress} sx={{ mb: 1 }} />
            <Typography variant="caption" color="text.secondary">
              {progress < 100 ? 'Analyzing document...' : 'Analysis complete'}
            </Typography>
          </Box>
        )}
        
        <Button
          variant="contained"
          color="primary"
          startIcon={scanning ? <CircularProgress size={20} color="inherit" /> : <ScanIcon />}
          onClick={scanDocument}
          disabled={scanning || !document}
          fullWidth
        >
          {scanning ? 'Analyzing...' : 'Analyze Document'}
        </Button>
      </Paper>
      
      {renderScanResults()}
    </Box>
  );
};

export default DocumentScanner; 
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

  // Real document scanning function
  const scanDocument = async () => {
    if (!document || !document.file) {
      setError('Please select a document file first.');
      return;
    }

    setScanning(true);
    setProgress(0);
    setResult(null);
    setError(null);
    
    try {
      // Simulate scanning progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + Math.floor(Math.random() * 15);
        });
      }, 300);
      
      // Prepare form data for file upload
      const formData = new FormData();
      formData.append('file', document.file);
      formData.append('document_type', document.type?.toLowerCase() || 'generic');
      
      // Call the real backend API
      const response = await fetch('http://localhost:3001/api/scanner/analyze', {
        method: 'POST',
        body: formData,
      });
      
      clearInterval(progressInterval);
      setProgress(100);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Analysis failed');
      }
      
      // Transform backend response to frontend format
      const analysis = data.analysis;
      const scanResult = {
        documentType: analysis.document_type || 'Legal Document',
        confidence: Math.round((analysis.confidence || 0.85) * 100),
        pageCount: analysis.page_count || 1,
        wordCount: analysis.word_count || 0,
        language: 'English',
        hasSignatures: analysis.has_signatures || false,
        dateIdentified: analysis.analysis_date || new Date().toISOString().split('T')[0],
        // Enhanced fields from our improved backend
        clientSummary: analysis.client_summary || '',
        riskLevel: analysis.risk_level || 'medium',
        actionItems: analysis.action_items || [],
        parties: analysis.parties?.map((party, index) => ({
          name: party,
          type: 'Unknown',
          role: index === 0 ? 'Primary' : 'Secondary'
        })) || [],
        keyTerms: analysis.legal_terms?.map(term => ({
          term: term.charAt(0).toUpperCase() + term.slice(1),
          description: `Found in document: ${term}`,
          risk: 'medium'
        })) || [],
        potentialIssues: analysis.potential_issues?.map((issue, index) => ({
          issue: issue,
          severity: 'medium',
          explanation: 'Identified through document analysis'
        })) || [],
        keyExcerpts: analysis.key_dates?.map(date => ({
          text: `Date found: ${date}`,
          section: 'Timeline',
          page: 1
        })) || [],
        recommendations: analysis.recommendations || [],
        extractedText: analysis.extracted_text,
        monetaryAmounts: analysis.monetary_amounts || []
      };
      
      setResult(scanResult);
      
      // Call the callback if provided
      if (onAnalysisComplete) {
        onAnalysisComplete(scanResult);
      }
    } catch (err) {
      setError(`Failed to analyze document: ${err.message}`);
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
          <Chip 
            icon={<InfoIcon />} 
            label={`Risk: ${result.riskLevel?.toUpperCase() || 'MEDIUM'}`}
            color={result.riskLevel === 'high' ? 'error' : result.riskLevel === 'low' ? 'success' : 'warning'}
          />
        </Box>

        {/* Client Summary - Most Important Section */}
        {result.clientSummary && (
          <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: 'primary.50', border: '1px solid', borderColor: 'primary.200' }}>
            <Typography variant="h6" gutterBottom color="primary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <InfoIcon />
              What This Document Means
            </Typography>
            <Typography variant="body1" sx={{ lineHeight: 1.6 }}>
              {result.clientSummary}
            </Typography>
          </Paper>
        )}

        {/* Action Items - Second Most Important */}
        {result.actionItems && result.actionItems.length > 0 && (
          <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: 'warning.50', border: '1px solid', borderColor: 'warning.200' }}>
            <Typography variant="h6" gutterBottom color="warning.dark" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CheckCircleIcon />
              What You Should Do Next
            </Typography>
            <List dense>
              {result.actionItems.map((item, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    <Typography variant="body2" color="warning.dark" fontWeight="bold">
                      {index + 1}.
                    </Typography>
                  </ListItemIcon>
                  <ListItemText 
                    primary={item}
                    primaryTypographyProps={{ variant: 'body2' }}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        )}
        
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
          Your personal legal assistant is ready! We'll analyze your document to give you the knowledge and confidence to handle it like a pro.
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
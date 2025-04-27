import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  CircularProgress,
  Alert,
  Grid,
  Paper,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tabs,
  Tab
} from '@mui/material';
import { 
  CompareArrows as CompareIcon,
  ContentCopy as CopyIcon 
} from '@mui/icons-material';
import { documentsApi } from '../services/api';
import * as DiffLib from 'diff';

const DocumentComparisonTool = ({ open, onClose, documents = [] }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedDocuments, setSelectedDocuments] = useState({
    left: null,
    right: null
  });
  const [documentContents, setDocumentContents] = useState({
    left: '',
    right: ''
  });
  const [comparisonResult, setComparisonResult] = useState([]);
  const [viewMode, setViewMode] = useState('side-by-side');
  const [comparisonStats, setComparisonStats] = useState({
    additions: 0,
    deletions: 0,
    unchanged: 0
  });

  useEffect(() => {
    if (selectedDocuments.left && selectedDocuments.right) {
      fetchDocumentContents();
    }
  }, [selectedDocuments]);

  const fetchDocumentContents = async () => {
    try {
      setLoading(true);
      
      // In a real implementation, you would fetch the document contents
      // For now, we'll use the content property assuming it's already loaded
      const leftDoc = documents.find(doc => doc._id === selectedDocuments.left);
      const rightDoc = documents.find(doc => doc._id === selectedDocuments.right);
      
      if (leftDoc && rightDoc) {
        setDocumentContents({
          left: leftDoc.content || '',
          right: rightDoc.content || ''
        });
        
        // Compare documents
        compareDocuments(leftDoc.content || '', rightDoc.content || '');
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching document contents:', error);
      setError('Failed to load document contents');
      setLoading(false);
    }
  };

  const compareDocuments = (leftContent, rightContent) => {
    // Basic text diffing using diff library
    try {
      // Strip HTML tags if content is HTML
      const leftText = stripHtml(leftContent);
      const rightText = stripHtml(rightContent);
      
      // Split by words for better comparison
      const diff = DiffLib.diffWords(leftText, rightText);
      
      // Calculate stats
      const stats = {
        additions: 0,
        deletions: 0,
        unchanged: 0
      };
      
      diff.forEach(part => {
        if (part.added) {
          stats.additions += part.value.length;
        } else if (part.removed) {
          stats.deletions += part.value.length;
        } else {
          stats.unchanged += part.value.length;
        }
      });
      
      setComparisonResult(diff);
      setComparisonStats(stats);
    } catch (error) {
      console.error('Error comparing documents:', error);
      setError('Failed to compare documents');
    }
  };

  const stripHtml = (html) => {
    // Simple function to strip HTML tags
    if (!html) return '';
    return html.replace(/<[^>]*>/g, '');
  };

  const handleDocumentSelect = (side, documentId) => {
    setSelectedDocuments(prev => ({
      ...prev,
      [side]: documentId
    }));
  };

  const handleViewModeChange = (event, newValue) => {
    setViewMode(newValue);
  };

  const renderDiff = () => {
    if (!comparisonResult.length) {
      return (
        <Typography variant="body1" align="center" sx={{ my: 4 }}>
          Select two documents to compare
        </Typography>
      );
    }
    
    if (viewMode === 'side-by-side') {
      return (
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
              <Typography variant="subtitle1" gutterBottom>
                {documents.find(doc => doc._id === selectedDocuments.left)?.title || 'Document 1'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box>
                {comparisonResult.map((part, index) => (
                  <span 
                    key={index}
                    style={{
                      backgroundColor: part.removed ? '#ffecec' : 'transparent',
                      textDecoration: part.removed ? 'line-through' : 'none',
                      color: part.removed ? '#ff0000' : 'inherit'
                    }}
                  >
                    {part.removed ? part.value : part.added ? '' : part.value}
                  </span>
                ))}
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={6}>
            <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
              <Typography variant="subtitle1" gutterBottom>
                {documents.find(doc => doc._id === selectedDocuments.right)?.title || 'Document 2'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box>
                {comparisonResult.map((part, index) => (
                  <span 
                    key={index}
                    style={{
                      backgroundColor: part.added ? '#eaffea' : 'transparent',
                      color: part.added ? '#00cc00' : 'inherit'
                    }}
                  >
                    {part.added ? part.value : part.removed ? '' : part.value}
                  </span>
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      );
    } else {
      // Unified view
      return (
        <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
          <Typography variant="subtitle1" gutterBottom>
            Unified View
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <Box>
            {comparisonResult.map((part, index) => (
              <span 
                key={index}
                style={{
                  backgroundColor: part.added 
                    ? '#eaffea' 
                    : part.removed 
                      ? '#ffecec' 
                      : 'transparent',
                  textDecoration: part.removed ? 'line-through' : 'none',
                  color: part.added 
                    ? '#00cc00' 
                    : part.removed 
                      ? '#ff0000' 
                      : 'inherit'
                }}
              >
                {part.value}
              </span>
            ))}
          </Box>
        </Paper>
      );
    }
  };

  const renderStatistics = () => {
    if (!comparisonResult.length) return null;
    
    const totalChanges = comparisonStats.additions + comparisonStats.deletions;
    const totalLength = totalChanges + comparisonStats.unchanged;
    const changePercentage = totalLength === 0 ? 0 : Math.round((totalChanges / totalLength) * 100);
    
    return (
      <Paper sx={{ p: 2, mt: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Comparison Statistics
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Typography variant="body2" color="success.main">
              Additions: {comparisonStats.additions} characters
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography variant="body2" color="error.main">
              Deletions: {comparisonStats.deletions} characters
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography variant="body2">
              Similarity: {100 - changePercentage}%
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    );
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="lg" 
      fullWidth
      PaperProps={{ sx: { height: '80vh' } }}
    >
      <DialogTitle>Compare Documents</DialogTitle>
      
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel>First Document</InputLabel>
              <Select
                value={selectedDocuments.left || ''}
                onChange={(e) => handleDocumentSelect('left', e.target.value)}
                label="First Document"
              >
                {documents.map(doc => (
                  <MenuItem 
                    key={doc._id} 
                    value={doc._id}
                    disabled={doc._id === selectedDocuments.right}
                  >
                    {doc.title}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel>Second Document</InputLabel>
              <Select
                value={selectedDocuments.right || ''}
                onChange={(e) => handleDocumentSelect('right', e.target.value)}
                label="Second Document"
              >
                {documents.map(doc => (
                  <MenuItem 
                    key={doc._id} 
                    value={doc._id}
                    disabled={doc._id === selectedDocuments.left}
                  >
                    {doc.title}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={viewMode} onChange={handleViewModeChange}>
            <Tab value="side-by-side" label="Side-by-Side View" />
            <Tab value="unified" label="Unified View" />
          </Tabs>
        </Box>
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            {renderDiff()}
            {renderStatistics()}
          </>
        )}
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose}>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DocumentComparisonTool; 
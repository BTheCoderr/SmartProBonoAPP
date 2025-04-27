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
  List,
  ListItem,
  ListItemText,
  Paper,
  Divider,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Restore as RestoreIcon,
  Visibility as VisibilityIcon,
  Compare as CompareIcon,
  GetApp as DownloadIcon
} from '@mui/icons-material';
import { documentsApi } from '../services/api';

const DocumentVersionHistoryDialog = ({ open, onClose, document, onRevertToVersion }) => {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [previewVersion, setPreviewVersion] = useState(null);
  const [compareMode, setCompareMode] = useState(false);
  const [versionToCompare, setVersionToCompare] = useState(null);

  useEffect(() => {
    if (open && document) {
      loadVersions();
    }
  }, [open, document]);

  const loadVersions = async () => {
    if (!document || !document._id) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentsApi.getDocumentVersions(document._id);
      setVersions(result || []);
    } catch (err) {
      console.error('Error loading document versions:', err);
      setError('Failed to load version history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRevert = async (version) => {
    try {
      setLoading(true);
      await documentsApi.revertToVersion(document._id, version.version);
      
      // Notify parent component
      if (onRevertToVersion) {
        onRevertToVersion(version);
      }
      
      // Close dialog
      onClose();
    } catch (err) {
      console.error('Error reverting to version:', err);
      setError('Failed to revert to this version. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = (version) => {
    setPreviewVersion(version);
    setCompareMode(false);
  };

  const handleCompare = (version) => {
    setVersionToCompare(version);
    setCompareMode(true);
  };

  const handleDownload = (version) => {
    // Create a blob from the content
    const blob = new Blob([version.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    // Create a download link
    const a = document.createElement('a');
    a.href = url;
    a.download = `${document.title}-v${version.version}.txt`;
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'Unknown';
    
    const date = new Date(timestamp);
    return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
  };

  const renderContent = (content) => {
    // If content is HTML, render it safely
    if (content && content.startsWith('<') && content.includes('</')) {
      return <div dangerouslySetInnerHTML={{ __html: content }} />;
    }
    
    // Otherwise render as plain text
    return <Typography variant="body2">{content}</Typography>;
  };

  const renderCompareView = () => {
    if (!versionToCompare || !previewVersion) return null;
    
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Compare Versions
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Paper sx={{ flex: 1, p: 2, bgcolor: '#f5f5f5', maxHeight: '400px', overflow: 'auto' }}>
            <Typography variant="subtitle2">
              Version {versionToCompare.version} - {formatDate(versionToCompare.timestamp)}
            </Typography>
            <Divider sx={{ my: 1 }} />
            {renderContent(versionToCompare.content)}
          </Paper>
          
          <Paper sx={{ flex: 1, p: 2, bgcolor: '#f5f5f5', maxHeight: '400px', overflow: 'auto' }}>
            <Typography variant="subtitle2">
              Version {previewVersion.version} - {formatDate(previewVersion.timestamp)}
            </Typography>
            <Divider sx={{ my: 1 }} />
            {renderContent(previewVersion.content)}
          </Paper>
        </Box>
      </Box>
    );
  };

  const renderPreview = () => {
    if (!previewVersion) return null;
    
    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Preview of Version {previewVersion.version}
        </Typography>
        <Paper sx={{ p: 2, bgcolor: '#f5f5f5', maxHeight: '400px', overflow: 'auto' }}>
          {renderContent(previewVersion.content)}
        </Paper>
      </Box>
    );
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="md" 
      fullWidth 
      PaperProps={{ sx: { maxHeight: '80vh' } }}
    >
      <DialogTitle>Version History - {document?.title}</DialogTitle>
      
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Box>
            {versions.length === 0 ? (
              <Typography>No version history available for this document.</Typography>
            ) : (
              <>
                <List>
                  {versions.map((version) => (
                    <Paper
                      key={version.version}
                      elevation={version.isCurrent ? 3 : 1}
                      sx={{ 
                        mb: 2, 
                        border: version.isCurrent ? '1px solid #3f51b5' : 'none',
                        bgcolor: version.isCurrent ? 'rgba(63, 81, 181, 0.08)' : 'white' 
                      }}
                    >
                      <ListItem 
                        secondaryAction={
                          <Box>
                            <Tooltip title="Preview">
                              <IconButton 
                                edge="end" 
                                onClick={() => handlePreview(version)}
                                sx={{ mr: 1 }}
                              >
                                <VisibilityIcon />
                              </IconButton>
                            </Tooltip>
                            
                            <Tooltip title="Compare">
                              <IconButton 
                                edge="end" 
                                onClick={() => handleCompare(version)}
                                sx={{ mr: 1 }}
                                disabled={!previewVersion || previewVersion.version === version.version}
                              >
                                <CompareIcon />
                              </IconButton>
                            </Tooltip>
                            
                            <Tooltip title="Download">
                              <IconButton 
                                edge="end" 
                                onClick={() => handleDownload(version)}
                                sx={{ mr: 1 }}
                              >
                                <DownloadIcon />
                              </IconButton>
                            </Tooltip>
                            
                            {!version.isCurrent && (
                              <Tooltip title="Revert to this version">
                                <IconButton 
                                  edge="end" 
                                  color="primary"
                                  onClick={() => handleRevert(version)}
                                >
                                  <RestoreIcon />
                                </IconButton>
                              </Tooltip>
                            )}
                          </Box>
                        }
                      >
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Typography variant="subtitle1">
                                Version {version.version}
                              </Typography>
                              {version.isCurrent && (
                                <Chip 
                                  label="Current" 
                                  size="small" 
                                  color="primary" 
                                  sx={{ ml: 1 }} 
                                />
                              )}
                            </Box>
                          }
                          secondary={
                            <>
                              <Typography variant="body2">
                                Last modified: {formatDate(version.timestamp)}
                              </Typography>
                              {version.modifiedBy && (
                                <Typography variant="body2">
                                  Modified by: {version.modifiedBy}
                                </Typography>
                              )}
                            </>
                          }
                        />
                      </ListItem>
                    </Paper>
                  ))}
                </List>
                
                {compareMode ? renderCompareView() : renderPreview()}
              </>
            )}
          </Box>
        )}
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DocumentVersionHistoryDialog; 
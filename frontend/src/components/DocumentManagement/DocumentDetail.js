import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Paper, Grid, Chip, Button, IconButton, Divider,
  Dialog, DialogTitle, DialogContent, DialogActions, CircularProgress,
  Alert, Card, CardContent, Tooltip, List, ListItem, ListItemText,
  ListItemIcon, ListItemSecondaryAction
} from '@mui/material';
import {
  GetApp, Edit, Delete, Share, History, InsertDriveFile, Description,
  Image, PictureAsPdf, Archive, Code, Movie, AudioFile, Visibility,
  Business, Lock, LockOpen, Public, Security, Person, Group, CalendarToday,
  Update, Storage, Label
} from '@mui/icons-material';
import PropTypes from 'prop-types';
import ApiService from '../../services/ApiService';
import DocumentPreviewComponent from '../DocumentPreview';

const getFileIcon = (fileType, size = 'medium') => {
  if (!fileType) return <InsertDriveFile fontSize={size} />;
  
  if (fileType.includes('pdf')) return <PictureAsPdf color="error" fontSize={size} />;
  if (fileType.includes('image')) return <Image color="primary" fontSize={size} />;
  if (fileType.includes('word') || fileType.includes('document')) return <Description color="primary" fontSize={size} />;
  if (fileType.includes('zip') || fileType.includes('rar')) return <Archive color="warning" fontSize={size} />;
  if (fileType.includes('text')) return <Code color="info" fontSize={size} />;
  if (fileType.includes('video')) return <Movie color="secondary" fontSize={size} />;
  if (fileType.includes('audio')) return <AudioFile color="success" fontSize={size} />;
  
  return <InsertDriveFile fontSize={size} />;
};

const getAccessLevelInfo = (level) => {
  switch (level) {
    case 'public':
      return { 
        icon: <Public color="success" />, 
        color: 'success',
        description: 'Visible to anyone' 
      };
    case 'internal':
      return { 
        icon: <Business color="info" />, 
        color: 'info',
        description: 'Visible to organization members' 
      };
    case 'confidential':
      return { 
        icon: <Lock color="warning" />, 
        color: 'warning',
        description: 'Visible to specific users only' 
      };
    case 'restricted':
      return { 
        icon: <Security color="error" />, 
        color: 'error',
        description: 'Visible only to owner and admins' 
      };
    default:
      return { 
        icon: <LockOpen />, 
        color: 'default',
        description: 'Unknown access level' 
      };
  }
};

const formatFileSize = (bytes) => {
  if (!bytes) return 'Unknown';
  
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`;
};

const DocumentDetail = ({ 
  documentId, 
  onEdit, 
  onDelete, 
  onShare, 
  onViewHistory,
  onClose
}) => {
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  
  // Load document details
  useEffect(() => {
    if (documentId) {
      fetchDocumentDetails();
    }
  }, [documentId]);
  
  // Cleanup preview URL on unmount
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  // Fetch document details
  const fetchDocumentDetails = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await ApiService.get(`/api/documents/${documentId}`);
      setDocument(response.data.document);
    } catch (err) {
      console.error('Error fetching document details:', err);
      setError('Failed to load document details. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Handle download document
  const handleDownload = async () => {
    try {
      const response = await ApiService.getFile(`/api/documents/${documentId}/file`);
      
      // Create blob URL and trigger download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', document.original_filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Error downloading document:', err);
      setError('Failed to download document. Please try again later.');
    }
  };

  // Handle preview document
  const handlePreview = async () => {
    try {
      // Check if document type is previewable
      const previewableTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
      
      if (!previewableTypes.includes(document.file_type)) {
        setError('Preview not available for this document type. Please download the file to view it.');
        return;
      }
      
      // Load file for preview
      const response = await ApiService.getFile(`/api/documents/${documentId}/file`, { responseType: 'blob' });
      
      // Create URL for preview
      const url = URL.createObjectURL(response.data);
      setPreviewUrl(url);
      setShowPreview(true);
    } catch (err) {
      console.error('Error preparing document preview:', err);
      setError('Failed to prepare document preview. Please try again later.');
    }
  };

  // Handle close preview
  const handleClosePreview = () => {
    setShowPreview(false);
    // Wait for dialog to close before revoking URL
    setTimeout(() => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
        setPreviewUrl(null);
      }
    }, 300);
  };

  // Render content
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 2 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!document) {
    return (
      <Box sx={{ p: 2 }}>
        <Alert severity="warning">Document not found or you don't have permission to access it.</Alert>
      </Box>
    );
  }

  // Get access level information
  const accessLevelInfo = getAccessLevelInfo(document.access_level);

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {getFileIcon(document.file_type, 'large')}
            <Box sx={{ ml: 2 }}>
              <Typography variant="h5" component="h1">
                {document.metadata?.title || document.original_filename || 'Untitled Document'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {document.original_filename}
              </Typography>
            </Box>
          </Box>
          
          <Box>
            <Tooltip title="View">
              <IconButton onClick={handlePreview}>
                <Visibility />
              </IconButton>
            </Tooltip>
            <Tooltip title="Download">
              <IconButton onClick={handleDownload}>
                <GetApp />
              </IconButton>
            </Tooltip>
            <Tooltip title="Edit">
              <IconButton onClick={() => onEdit(document)}>
                <Edit />
              </IconButton>
            </Tooltip>
            <Tooltip title="Share">
              <IconButton onClick={() => onShare(document)}>
                <Share />
              </IconButton>
            </Tooltip>
            <Tooltip title="Version History">
              <IconButton onClick={() => onViewHistory(document)}>
                <History />
              </IconButton>
            </Tooltip>
            <Tooltip title="Delete">
              <IconButton color="error" onClick={() => onDelete(document)}>
                <Delete />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card variant="outlined" sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Document Information
                </Typography>
                
                <List dense disablePadding>
                  <ListItem>
                    <ListItemIcon>
                      <Label />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Document Type" 
                      secondary={document.metadata?.document_type || 'Not specified'} 
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      {accessLevelInfo.icon}
                    </ListItemIcon>
                    <ListItemText 
                      primary="Access Level" 
                      secondary={accessLevelInfo.description} 
                    />
                    <ListItemSecondaryAction>
                      <Chip 
                        label={document.access_level} 
                        color={accessLevelInfo.color}
                        size="small"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <Storage />
                    </ListItemIcon>
                    <ListItemText 
                      primary="File Size" 
                      secondary={formatFileSize(document.file_size)} 
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <CalendarToday />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Created" 
                      secondary={new Date(document.created_at).toLocaleString()} 
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <Update />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Last Updated" 
                      secondary={new Date(document.updated_at).toLocaleString()} 
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <Person />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Owner" 
                      secondary={document.owner_name || document.owner_id || 'Unknown'} 
                    />
                  </ListItem>
                  
                  {document.version > 1 && (
                    <ListItem>
                      <ListItemIcon>
                        <History />
                      </ListItemIcon>
                      <ListItemText 
                        primary="Version" 
                        secondary={document.version} 
                      />
                    </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
            
            {document.shared_with && document.shared_with.length > 0 && (
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Shared With
                  </Typography>
                  
                  <List dense disablePadding>
                    {document.shared_with.map((user, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <Group />
                        </ListItemIcon>
                        <ListItemText 
                          primary={user.name || user} 
                          secondary={user.email || ''} 
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            )}
          </Grid>
          
          <Grid item xs={12} md={6}>
            {document.metadata?.description && (
              <Card variant="outlined" sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Description
                  </Typography>
                  <Typography variant="body1">
                    {document.metadata.description}
                  </Typography>
                </CardContent>
              </Card>
            )}
            
            {document.metadata?.tags && document.metadata.tags.length > 0 && (
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Tags
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {document.metadata.tags.map((tag, index) => (
                      <Chip key={index} label={tag} size="small" />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            )}
            
            {/* Add additional metadata cards as needed */}
          </Grid>
        </Grid>
      </Paper>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
        <Button onClick={onClose} sx={{ mr: 1 }}>
          Close
        </Button>
        <Button variant="contained" onClick={handlePreview}>
          Preview Document
        </Button>
      </Box>

      {/* Document Preview Dialog */}
      <Dialog
        open={showPreview}
        onClose={handleClosePreview}
        maxWidth="lg"
        fullWidth
      >
        {previewUrl && (
          <DocumentPreviewComponent
            documentUrl={previewUrl}
            documentType={document.file_type.split('/')[1]}
            previewTitle={document.metadata?.title || document.original_filename}
            onClose={handleClosePreview}
          />
        )}
      </Dialog>
    </Box>
  );
};

DocumentDetail.propTypes = {
  documentId: PropTypes.string.isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onShare: PropTypes.func.isRequired,
  onViewHistory: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired
};

export default DocumentDetail; 
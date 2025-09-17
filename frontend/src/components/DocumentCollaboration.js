/**
 * Document Collaboration Component
 * Provides real-time document editing and collaboration features
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  IconButton,
  Toolbar,
  Divider,
  Chip,
  Avatar,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Alert,
  CircularProgress,
  Badge
} from '@mui/material';
import {
  Edit as EditIcon,
  Save as SaveIcon,
  Share as ShareIcon,
  People as PeopleIcon,
  Chat as ChatIcon,
  History as HistoryIcon,
  Download as DownloadIcon,
  Upload as UploadIcon,
  Lock as LockIcon,
  LockOpen as LockOpenIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  Add as AddIcon,
  Remove as RemoveIcon
} from '@mui/icons-material';
import { useDocumentCollaboration } from '../hooks/useWebSocket';
import RealtimeChat from './RealtimeChat';

const DocumentCollaboration = ({ 
  documentId, 
  documentTitle = "Untitled Document",
  initialContent = "",
  readOnly = false 
}) => {
  const [content, setContent] = useState(initialContent);
  const [isEditing, setIsEditing] = useState(false);
  const [collaborators, setCollaborators] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showShareDialog, setShowShareDialog] = useState(false);
  const [shareEmail, setShareEmail] = useState('');
  const [permissions, setPermissions] = useState('view');
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);
  const [version, setVersion] = useState(1);
  const [documentHistory, setDocumentHistory] = useState([]);
  
  const editorRef = useRef(null);
  const roomId = `document_${documentId}`;
  
  const {
    isConnected,
    isCollaborating,
    documentChanges,
    sendChanges,
    startCollaboration,
    stopCollaboration
  } = useDocumentCollaboration(documentId, roomId);

  // Handle document changes from other collaborators
  useEffect(() => {
    if (documentChanges.length > 0) {
      const latestChange = documentChanges[documentChanges.length - 1];
      if (latestChange.document_id === documentId) {
        // Apply changes to document
        setContent(prevContent => {
          // Simple merge strategy - in production, use operational transforms
          return latestChange.changes.content || prevContent;
        });
        setVersion(prev => prev + 1);
      }
    }
  }, [documentChanges, documentId]);

  // Auto-save functionality
  useEffect(() => {
    if (isEditing && content !== initialContent) {
      const autoSaveTimer = setTimeout(() => {
        handleSave();
      }, 2000); // Auto-save every 2 seconds

      return () => clearTimeout(autoSaveTimer);
    }
  }, [content, isEditing, initialContent]);

  const handleEdit = () => {
    if (readOnly) return;
    
    setIsEditing(true);
    startCollaboration();
  };

  const handleSave = useCallback(async () => {
    if (!isEditing) return;
    
    setIsSaving(true);
    
    try {
      // Send changes to other collaborators
      if (isConnected) {
        sendChanges({
          content,
          timestamp: new Date().toISOString(),
          version: version + 1
        });
      }
      
      // Save to backend
      const response = await fetch(`http://localhost:3001/api/documents/${documentId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          version: version + 1,
          last_modified: new Date().toISOString()
        })
      });
      
      if (response.ok) {
        setVersion(prev => prev + 1);
        setLastSaved(new Date());
        
        // Add to history
        setDocumentHistory(prev => [...prev, {
          id: Date.now(),
          content,
          version: version + 1,
          timestamp: new Date(),
          author: 'You'
        }]);
      }
    } catch (error) {
      console.error('Error saving document:', error);
    } finally {
      setIsSaving(false);
    }
  }, [content, isEditing, isConnected, sendChanges, documentId, version]);

  const handleStopEditing = () => {
    setIsEditing(false);
    stopCollaboration();
  };

  const handleContentChange = (event) => {
    if (!isEditing) return;
    
    const newContent = event.target.value;
    setContent(newContent);
    
    // Send real-time changes to collaborators
    if (isConnected) {
      sendChanges({
        content: newContent,
        timestamp: new Date().toISOString(),
        version: version + 1
      });
    }
  };

  const handleShare = async () => {
    if (!shareEmail) return;
    
    try {
      const response = await fetch(`http://localhost:3001/api/documents/${documentId}/share`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: shareEmail,
          permissions: permissions
        })
      });
      
      if (response.ok) {
        setShowShareDialog(false);
        setShareEmail('');
        // Add to collaborators list
        setCollaborators(prev => [...prev, {
          id: Date.now(),
          email: shareEmail,
          permissions: permissions,
          avatar: shareEmail.charAt(0).toUpperCase()
        }]);
      }
    } catch (error) {
      console.error('Error sharing document:', error);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${documentTitle}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      setContent(e.target.result);
    };
    reader.readAsText(file);
  };

  const getCollaboratorColor = (index) => {
    const colors = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#00bcd4', '#009688'];
    return colors[index % colors.length];
  };

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper elevation={1} sx={{ p: 2, borderRadius: 0 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="h6">{documentTitle}</Typography>
            <Chip 
              label={isEditing ? "Editing" : "Viewing"} 
              color={isEditing ? "primary" : "default"}
              size="small"
            />
            {isSaving && (
              <Chip 
                label="Saving..." 
                color="warning"
                size="small"
                icon={<CircularProgress size={16} />}
              />
            )}
            {lastSaved && (
              <Typography variant="caption" color="text.secondary">
                Last saved: {lastSaved.toLocaleTimeString()}
              </Typography>
            )}
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {/* Collaborators */}
            <Tooltip title="Active Collaborators">
              <Badge badgeContent={collaborators.length} color="primary">
                <IconButton onClick={() => setShowChat(!showChat)}>
                  <PeopleIcon />
                </IconButton>
              </Badge>
            </Tooltip>
            
            {/* Chat */}
            <Tooltip title="Document Chat">
              <IconButton onClick={() => setShowChat(!showChat)}>
                <ChatIcon />
              </IconButton>
            </Tooltip>
            
            {/* History */}
            <Tooltip title="Document History">
              <IconButton onClick={() => setShowHistory(!showHistory)}>
                <HistoryIcon />
              </IconButton>
            </Tooltip>
            
            {/* Share */}
            <Tooltip title="Share Document">
              <IconButton onClick={() => setShowShareDialog(true)}>
                <ShareIcon />
              </IconButton>
            </Tooltip>
            
            {/* Download */}
            <Tooltip title="Download Document">
              <IconButton onClick={handleDownload}>
                <DownloadIcon />
              </IconButton>
            </Tooltip>
            
            {/* Upload */}
            <Tooltip title="Upload Document">
              <IconButton component="label">
                <UploadIcon />
                <input
                  type="file"
                  hidden
                  accept=".txt,.md,.doc,.docx"
                  onChange={handleUpload}
                />
              </IconButton>
            </Tooltip>
            
            {/* Edit/Save */}
            {!readOnly && (
              <>
                {isEditing ? (
                  <Button
                    variant="contained"
                    startIcon={<SaveIcon />}
                    onClick={handleSave}
                    disabled={isSaving}
                  >
                    Save
                  </Button>
                ) : (
                  <Button
                    variant="outlined"
                    startIcon={<EditIcon />}
                    onClick={handleEdit}
                  >
                    Edit
                  </Button>
                )}
              </>
            )}
          </Box>
        </Box>
        
        {/* Collaborators List */}
        {collaborators.length > 0 && (
          <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {collaborators.map((collaborator, index) => (
              <Chip
                key={collaborator.id}
                avatar={
                  <Avatar sx={{ 
                    bgcolor: getCollaboratorColor(index),
                    width: 24,
                    height: 24,
                    fontSize: '0.75rem'
                  }}>
                    {collaborator.avatar}
                  </Avatar>
                }
                label={collaborator.email}
                size="small"
                color={collaborator.permissions === 'edit' ? 'primary' : 'default'}
              />
            ))}
          </Box>
        )}
      </Paper>

      {/* Main Content */}
      <Box sx={{ flex: 1, display: 'flex' }}>
        {/* Document Editor */}
        <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <Paper elevation={1} sx={{ flex: 1, m: 1, display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
              <Typography variant="subtitle2" color="text.secondary">
                Document Content {isConnected && isCollaborating && (
                  <Chip label="Live Collaboration" color="success" size="small" sx={{ ml: 1 }} />
                )}
              </Typography>
            </Box>
            
            <Box sx={{ flex: 1, p: 2 }}>
              <TextField
                ref={editorRef}
                fullWidth
                multiline
                value={content}
                onChange={handleContentChange}
                disabled={!isEditing}
                placeholder="Start typing your document..."
                variant="outlined"
                sx={{
                  '& .MuiInputBase-root': {
                    height: '100%',
                    alignItems: 'flex-start'
                  },
                  '& .MuiInputBase-input': {
                    height: '100% !important',
                    overflow: 'auto !important'
                  }
                }}
              />
            </Box>
          </Paper>
        </Box>

        {/* Sidebar */}
        {(showChat || showHistory) && (
          <Box sx={{ width: 300, borderLeft: 1, borderColor: 'divider' }}>
            {showChat && (
              <Box sx={{ height: '100%' }}>
                <RealtimeChat
                  roomId={roomId}
                  currentUser="You"
                  showUserAvatars={true}
                />
              </Box>
            )}
            
            {showHistory && (
              <Box sx={{ height: '100%', overflow: 'auto' }}>
                <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                  <Typography variant="h6">Document History</Typography>
                </Box>
                <List>
                  {documentHistory.map((entry) => (
                    <ListItem key={entry.id}>
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                          {entry.author.charAt(0)}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={`Version ${entry.version}`}
                        secondary={`${entry.author} - ${entry.timestamp.toLocaleString()}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}
          </Box>
        )}
      </Box>

      {/* Share Dialog */}
      <Dialog open={showShareDialog} onClose={() => setShowShareDialog(false)}>
        <DialogTitle>Share Document</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Email Address"
            fullWidth
            variant="outlined"
            value={shareEmail}
            onChange={(e) => setShareEmail(e.target.value)}
            sx={{ mb: 2 }}
          />
          <FormControl fullWidth>
            <InputLabel>Permissions</InputLabel>
            <Select
              value={permissions}
              onChange={(e) => setPermissions(e.target.value)}
              label="Permissions"
            >
              <MenuItem value="view">View Only</MenuItem>
              <MenuItem value="edit">Edit</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowShareDialog(false)}>Cancel</Button>
          <Button onClick={handleShare} variant="contained">Share</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DocumentCollaboration;

import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Autocomplete,
  Box,
  Chip,
  Typography,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Divider,
  Tab,
  Tabs,
  Paper
} from '@mui/material';
import { 
  PersonAdd as PersonAddIcon, 
  Email as EmailIcon,
  Send as SendIcon 
} from '@mui/icons-material';
import axios from 'axios';
import config from '../config';

const ShareDocumentDialog = ({ open, onClose, document, onShareComplete }) => {
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [currentlySharedWith, setCurrentlySharedWith] = useState([]);
  const [tabValue, setTabValue] = useState(0);
  const [emailData, setEmailData] = useState({
    recipientEmail: '',
    subject: '',
    message: ''
  });

  // Load users for sharing
  useEffect(() => {
    if (open) {
      fetchUsers();
      if (document && document.sharedWith) {
        setCurrentlySharedWith(document.sharedWith);
      } else {
        setCurrentlySharedWith([]);
      }
      
      // Set default email subject if document is available
      if (document) {
        setEmailData(prev => ({
          ...prev,
          subject: `Shared Document: ${document.title}`,
          message: `I'd like to share this document with you: ${document.title}\n\nYou can access it using the link below.`
        }));
      }
    }
  }, [open, document]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      // In a real app, this would call a backend API to get users
      const response = await axios.get(`${config.apiUrl}/api/users`);
      setUsers(response.data || []);
    } catch (error) {
      console.error('Error fetching users:', error);
      // Mock users for demo purposes
      setUsers([
        { _id: '1', name: 'John Doe', email: 'john@example.com', role: 'lawyer' },
        { _id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'client' },
        { _id: '3', name: 'Robert Brown', email: 'robert@example.com', role: 'admin' },
        { _id: '4', name: 'Sarah Johnson', email: 'sarah@example.com', role: 'client' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleShare = async () => {
    if (selectedUsers.length === 0) {
      setError('Please select at least one user to share with');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const userIds = selectedUsers.map(user => user._id);
      
      await axios.post(`${config.apiUrl}/api/documents/${document._id}/share`, {
        users: userIds
      });
      
      setSuccess(true);
      setCurrentlySharedWith([...currentlySharedWith, ...selectedUsers]);
      
      // Notify parent component
      if (onShareComplete) {
        onShareComplete(userIds);
      }
      
      // Reset selection
      setSelectedUsers([]);
      
      // Close dialog after 2 seconds
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 2000);
    } catch (error) {
      console.error('Error sharing document:', error);
      setError('Failed to share document. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyLink = () => {
    const shareLink = `${window.location.origin}/documents/shared/${document._id}`;
    navigator.clipboard.writeText(shareLink)
      .then(() => {
        setSuccess('Link copied to clipboard');
        setTimeout(() => setSuccess(false), 2000);
      })
      .catch(err => {
        console.error('Failed to copy link:', err);
        setError('Failed to copy link');
      });
  };

  const handleUserChange = (event, newValue) => {
    setSelectedUsers(newValue);
  };

  const handleEmailInputChange = (e) => {
    const { name, value } = e.target;
    setEmailData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSendEmail = async () => {
    if (!emailData.recipientEmail) {
      setError('Please enter a recipient email address');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const shareLink = `${window.location.origin}/documents/shared/${document._id}`;
      
      // In a real app, this would call a backend API to send the email
      await axios.post(`${config.apiUrl}/api/documents/${document._id}/share-via-email`, {
        recipientEmail: emailData.recipientEmail,
        subject: emailData.subject,
        message: emailData.message,
        shareLink: shareLink
      });
      
      setSuccess('Email sent successfully!');
      
      // Reset form
      setEmailData(prev => ({
        ...prev,
        recipientEmail: ''
      }));
      
      // Close dialog after 2 seconds
      setTimeout(() => {
        setSuccess(false);
      }, 2000);
    } catch (error) {
      console.error('Error sending email:', error);
      setError('Failed to send email. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  // Filter out users that are already shared with
  const filteredUsers = users.filter(user => 
    !currentlySharedWith.some(shared => shared._id === user._id)
  );

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Share Document</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>
          {typeof success === 'string' ? success : 'Document shared successfully!'}
        </Alert>}
        
        <Typography variant="subtitle1" gutterBottom>
          Document: {document?.title}
        </Typography>
        
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="share options tabs">
            <Tab label="Share with Users" />
            <Tab label="Share via Email" />
          </Tabs>
        </Box>

        {tabValue === 0 ? (
          <Box sx={{ mt: 3, mb: 4 }}>
            <Autocomplete
              multiple
              options={filteredUsers}
              getOptionLabel={(option) => `${option.name} (${option.email})`}
              onChange={handleUserChange}
              value={selectedUsers}
              filterSelectedOptions
              renderInput={(params) => (
                <TextField
                  {...params}
                  variant="outlined"
                  label="Add people"
                  placeholder="Search by name or email"
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              )}
              renderTags={(tagValue, getTagProps) =>
                tagValue.map((option, index) => (
                  <Chip
                    avatar={<Avatar>{option.name[0]}</Avatar>}
                    label={option.name}
                    {...getTagProps({ index })}
                  />
                ))
              }
            />
            
            <Button
              variant="outlined"
              startIcon={<EmailIcon />}
              onClick={handleCopyLink}
              sx={{ mt: 2 }}
            >
              Copy Shareable Link
            </Button>
          </Box>
        ) : (
          <Box sx={{ mt: 3, mb: 4 }}>
            <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Share this document directly via email. The recipient will receive a link to access the document.
              </Typography>
            </Paper>
            
            <TextField
              fullWidth
              label="Recipient Email"
              name="recipientEmail"
              value={emailData.recipientEmail}
              onChange={handleEmailInputChange}
              margin="normal"
              required
              placeholder="email@example.com"
            />
            
            <TextField
              fullWidth
              label="Subject"
              name="subject"
              value={emailData.subject}
              onChange={handleEmailInputChange}
              margin="normal"
            />
            
            <TextField
              fullWidth
              label="Message"
              name="message"
              value={emailData.message}
              onChange={handleEmailInputChange}
              margin="normal"
              multiline
              rows={4}
            />
            
            <Button
              variant="contained"
              color="primary"
              startIcon={<SendIcon />}
              onClick={handleSendEmail}
              sx={{ mt: 2 }}
              disabled={!emailData.recipientEmail || loading}
            >
              Send Email
            </Button>
          </Box>
        )}
        
        {currentlySharedWith.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="subtitle1" gutterBottom>
              Currently shared with:
            </Typography>
            <List>
              {currentlySharedWith.map((user) => (
                <React.Fragment key={user._id}>
                  <ListItem>
                    <ListItemAvatar>
                      <Avatar>{user.name ? user.name[0] : '?'}</Avatar>
                    </ListItemAvatar>
                    <ListItemText 
                      primary={user.name} 
                      secondary={user.email} 
                    />
                  </ListItem>
                  <Divider variant="inset" component="li" />
                </React.Fragment>
              ))}
            </List>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        {tabValue === 0 && (
          <Button 
            onClick={handleShare} 
            color="primary" 
            variant="contained"
            disabled={selectedUsers.length === 0 || loading}
            startIcon={loading ? <CircularProgress size={20} /> : <PersonAddIcon />}
          >
            Share
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default ShareDocumentDialog; 
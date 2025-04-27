import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Chip,
  Typography,
  CircularProgress,
  Alert,
  Autocomplete
} from '@mui/material';
import { 
  LocalOffer as TagIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { documentsApi } from '../services/api';

const TagManagerDialog = ({ open, onClose, document, onTagsUpdated }) => {
  const [tags, setTags] = useState([]);
  const [availableTags, setAvailableTags] = useState([]);
  const [newTag, setNewTag] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (open && document) {
      // Initialize with document's existing tags
      setTags(document.tags || []);
      fetchAvailableTags();
    }
  }, [open, document]);

  const fetchAvailableTags = async () => {
    try {
      setLoading(true);
      // Fetch common tags from the backend
      const response = await documentsApi.getCommonTags();
      const commonTags = response.tags.map(tag => tag.tag);
      setAvailableTags(commonTags);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching available tags:', error);
      
      // Fallback to default tags if API fails
      const defaultTags = [
        'important', 'urgent', 'draft', 'final', 'reviewed',
        'pending', 'archived', 'legal', 'contract', 'personal'
      ];
      setAvailableTags(defaultTags);
      setLoading(false);
    }
  };

  const handleAddTag = () => {
    if (newTag && !tags.includes(newTag)) {
      setTags([...tags, newTag]);
      setNewTag('');
    }
  };

  const handleDeleteTag = (tagToDelete) => {
    setTags(tags.filter(tag => tag !== tagToDelete));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && newTag) {
      e.preventDefault();
      handleAddTag();
    }
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      setError(null);
      
      await documentsApi.updateDocumentTags(document._id, tags);
      
      setSuccess(true);
      
      // Notify parent component
      if (onTagsUpdated) {
        onTagsUpdated(tags);
      }
      
      // Close dialog after 1.5 seconds
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 1500);
    } catch (error) {
      console.error('Error updating tags:', error);
      setError('Failed to update tags. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTagSelect = (event, value) => {
    setTags(value);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Manage Tags</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>Tags updated successfully!</Alert>}
        
        <Typography variant="subtitle1" gutterBottom>
          Document: {document?.title}
        </Typography>
        
        <Box sx={{ mt: 3 }}>
          <Typography variant="body2" color="textSecondary" gutterBottom>
            Add tags to categorize and easily find your documents later.
          </Typography>
          
          <Autocomplete
            multiple
            freeSolo
            options={availableTags.filter(tag => !tags.includes(tag))}
            value={tags}
            onChange={handleTagSelect}
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip
                  variant="outlined"
                  label={option}
                  {...getTagProps({ index })}
                  icon={<TagIcon />}
                />
              ))
            }
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                label="Document Tags"
                placeholder="Add a tag"
                helperText="Press Enter to add a new tag"
                fullWidth
                margin="normal"
              />
            )}
          />
          
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
            <TextField
              label="New Tag"
              variant="outlined"
              size="small"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              onKeyPress={handleKeyPress}
              sx={{ flexGrow: 1 }}
            />
            <Button
              variant="contained"
              color="primary"
              startIcon={<AddIcon />}
              onClick={handleAddTag}
              disabled={!newTag}
              sx={{ ml: 1 }}
            >
              Add
            </Button>
          </Box>
          
          <Box sx={{ mt: 3 }}>
            <Typography variant="subtitle2" gutterBottom>
              Current Tags:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {tags.length > 0 ? (
                tags.map((tag) => (
                  <Chip
                    key={tag}
                    label={tag}
                    variant="filled"
                    color="primary"
                    onDelete={() => handleDeleteTag(tag)}
                    icon={<TagIcon />}
                  />
                ))
              ) : (
                <Typography variant="body2" color="textSecondary">
                  No tags added yet
                </Typography>
              )}
            </Box>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          onClick={handleSave}
          color="primary"
          variant="contained"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : null}
        >
          Save Tags
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default TagManagerDialog; 
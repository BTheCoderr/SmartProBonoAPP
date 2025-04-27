import React, { useState, useEffect, useRef } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Chip,
  Paper,
  Divider,
  IconButton
} from '@mui/material';
import {
  Save as SaveIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  ContentCopy as ContentCopyIcon
} from '@mui/icons-material';
import { Editor } from '@tinymce/tinymce-react';
import { documentsApi } from '../services/api';

const DocumentTemplateDialog = ({ open, onClose, onSave, initialTemplate = null }) => {
  const [template, setTemplate] = useState({
    title: '',
    description: '',
    content: '',
    category: 'legal',
    tags: []
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [newTag, setNewTag] = useState('');
  const [templateVariables, setTemplateVariables] = useState([]);
  const editorRef = useRef(null);

  useEffect(() => {
    if (initialTemplate) {
      setTemplate({
        ...initialTemplate,
        tags: initialTemplate.tags || []
      });
      
      // Extract variables from content using {{variable}} pattern
      if (initialTemplate.content) {
        extractVariables(initialTemplate.content);
      }
    } else {
      resetForm();
    }
  }, [initialTemplate, open]);

  const resetForm = () => {
    setTemplate({
      title: '',
      description: '',
      content: '',
      category: 'legal',
      tags: []
    });
    setTemplateVariables([]);
    setError(null);
    setSuccess(false);
  };

  const extractVariables = (content) => {
    const regex = /{{([^}]+)}}/g;
    const matches = [...content.matchAll(regex)];
    const variables = matches.map(match => match[1].trim());
    
    // Remove duplicates
    setTemplateVariables([...new Set(variables)]);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setTemplate(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleEditorChange = (content) => {
    setTemplate(prev => ({
      ...prev,
      content
    }));
    
    // Extract variables when content changes
    extractVariables(content);
  };

  const handleAddTag = () => {
    if (newTag && !template.tags.includes(newTag)) {
      setTemplate(prev => ({
        ...prev,
        tags: [...prev.tags, newTag]
      }));
      setNewTag('');
    }
  };

  const handleDeleteTag = (tagToDelete) => {
    setTemplate(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToDelete)
    }));
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && newTag) {
      e.preventDefault();
      handleAddTag();
    }
  };

  const handleSave = async () => {
    // Validate required fields
    if (!template.title || !template.content) {
      setError('Title and content are required');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const savedTemplate = await documentsApi.saveTemplate({
        ...template,
        type: 'template',
        variables: templateVariables
      });
      
      setSuccess(true);
      
      // Notify parent component
      if (onSave) {
        onSave(savedTemplate);
      }
      
      // Close dialog after 1.5 seconds
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 1500);
    } catch (err) {
      console.error('Error saving template:', err);
      setError('Failed to save template. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddVariable = (variable) => {
    if (!editorRef.current) return;
    
    // Insert the variable at cursor position
    editorRef.current.insertContent(`{{${variable}}}`);
  };

  const handleVariableClick = (variable) => {
    handleAddVariable(variable);
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="md" 
      fullWidth
      PaperProps={{ sx: { height: '90vh' } }}
    >
      <DialogTitle>
        {initialTemplate ? 'Edit Template' : 'Create New Template'}
      </DialogTitle>
      
      <DialogContent dividers>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>Template saved successfully!</Alert>}
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              label="Template Title"
              name="title"
              value={template.title}
              onChange={handleInputChange}
              margin="normal"
              required
              error={!template.title && error}
              helperText={!template.title && error ? 'Title is required' : ''}
            />
          </Grid>
          
          <Grid item xs={12} md={4}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Category</InputLabel>
              <Select
                name="category"
                value={template.category}
                onChange={handleInputChange}
                label="Category"
              >
                <MenuItem value="legal">Legal</MenuItem>
                <MenuItem value="contract">Contract</MenuItem>
                <MenuItem value="letter">Letter</MenuItem>
                <MenuItem value="form">Form</MenuItem>
                <MenuItem value="other">Other</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Description"
              name="description"
              value={template.description}
              onChange={handleInputChange}
              margin="normal"
              multiline
              rows={2}
            />
          </Grid>
          
          <Grid item xs={12}>
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Template Content
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Use {{variable_name}} syntax to add placeholders that can be replaced when using the template.
              </Typography>
            </Box>
            
            <Editor
              onInit={(evt, editor) => editorRef.current = editor}
              apiKey={process.env.REACT_APP_TINYMCE_API_KEY || 'no-api-key'}
              value={template.content}
              onEditorChange={handleEditorChange}
              init={{
                height: 350,
                menubar: true,
                plugins: [
                  'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
                  'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
                  'insertdatetime', 'media', 'table', 'help', 'wordcount'
                ],
                toolbar: 'undo redo | blocks | ' +
                  'bold italic forecolor | alignleft aligncenter ' +
                  'alignright alignjustify | bullist numlist outdent indent | ' +
                  'removeformat | help',
                content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
              }}
            />
          </Grid>
          
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              Tags
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <TextField
                label="Add tag"
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                onKeyDown={handleKeyDown}
                size="small"
                sx={{ width: 200 }}
              />
              <Button 
                onClick={handleAddTag} 
                disabled={!newTag}
                startIcon={<AddIcon />}
                sx={{ ml: 1 }}
              >
                Add
              </Button>
            </Box>
            
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 2 }}>
              {template.tags.map((tag) => (
                <Chip
                  key={tag}
                  label={tag}
                  onDelete={() => handleDeleteTag(tag)}
                  size="small"
                />
              ))}
              {template.tags.length === 0 && (
                <Typography variant="body2" color="textSecondary">
                  No tags added yet
                </Typography>
              )}
            </Box>
          </Grid>
          
          {templateVariables.length > 0 && (
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle1" gutterBottom>
                Template Variables
              </Typography>
              <Typography variant="caption" color="textSecondary" paragraph>
                Click on a variable to insert it at the cursor position
              </Typography>
              
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {templateVariables.map((variable) => (
                  <Chip
                    key={variable}
                    label={variable}
                    onClick={() => handleVariableClick(variable)}
                    clickable
                    color="primary"
                    variant="outlined"
                    size="small"
                  />
                ))}
              </Box>
            </Grid>
          )}
          
          <Grid item xs={12}>
            <Paper variant="outlined" sx={{ p: 2, mt: 2, bgcolor: '#f8f9fa' }}>
              <Typography variant="subtitle2" gutterBottom>
                Common Variables
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {[
                  'client_name', 'client_address', 'client_email', 'client_phone',
                  'date', 'company_name', 'signature', 'lawyer_name', 'case_number'
                ].map((variable) => (
                  <Chip
                    key={variable}
                    label={variable}
                    onClick={() => handleAddVariable(variable)}
                    clickable
                    size="small"
                    sx={{ mb: 1 }}
                  />
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button 
          onClick={handleSave} 
          color="primary" 
          variant="contained"
          disabled={loading || !template.title || !template.content}
          startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
        >
          Save Template
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DocumentTemplateDialog; 
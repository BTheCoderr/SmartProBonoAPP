import React, { useState, useRef } from 'react';
import { 
  Box, Button, Typography, LinearProgress, Alert, 
  Paper, IconButton, List, ListItem, ListItemText, 
  ListItemSecondaryAction, Dialog, DialogTitle, DialogContent,
  DialogActions, TextField, FormHelperText
} from '@mui/material';
import { 
  CloudUpload, Delete, CheckCircle, Error as ErrorIcon, 
  Visibility, Description 
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import PropTypes from 'prop-types';
import DocumentPreviewComponent from './DocumentPreview';

// Styled components
const UploadBox = styled(Paper)(({ theme, isDragActive, isError }) => ({
  padding: theme.spacing(3),
  textAlign: 'center',
  cursor: 'pointer',
  border: `2px dashed ${isError ? theme.palette.error.main : 
    isDragActive ? theme.palette.primary.main : theme.palette.divider}`,
  backgroundColor: isDragActive ? theme.palette.action.hover : theme.palette.background.paper,
  transition: 'all 0.3s ease',
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
  },
}));

const HiddenInput = styled('input')({
  display: 'none',
});

// Max file size in bytes (10MB)
const MAX_FILE_SIZE = 10 * 1024 * 1024;

// Allowed file types
const ALLOWED_FILE_TYPES = {
  'application/pdf': 'pdf',
  'image/jpeg': 'jpeg',
  'image/jpg': 'jpg',
  'image/png': 'png',
  'application/msword': 'doc',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
  'text/plain': 'txt'
};

const DocumentUploadWithValidation = ({ 
  onUpload, 
  maxFiles = 5,
  allowedFileTypes = Object.keys(ALLOWED_FILE_TYPES),
  maxFileSize = MAX_FILE_SIZE,
  showPreview = true
}) => {
  const [files, setFiles] = useState([]);
  const [isDragActive, setIsDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({});
  const [uploadErrors, setUploadErrors] = useState({});
  const [previewFile, setPreviewFile] = useState(null);
  const [showFileInfoDialog, setShowFileInfoDialog] = useState(false);
  const [currentFile, setCurrentFile] = useState(null);
  const [fileInfo, setFileInfo] = useState({ description: '' });
  const [fileInfoErrors, setFileInfoErrors] = useState({});
  
  const fileInputRef = useRef(null);

  // Handle file selection
  const handleFileSelect = (event) => {
    event.preventDefault();
    const selectedFiles = event.target.files || event.dataTransfer.files;
    
    if (!selectedFiles || selectedFiles.length === 0) return;
    
    // Check if max files would be exceeded
    if (files.length + selectedFiles.length > maxFiles) {
      setUploadErrors({ general: `Maximum of ${maxFiles} files allowed` });
      return;
    }
    
    // Process each file
    Array.from(selectedFiles).forEach(file => {
      validateAndAddFile(file);
    });
    
    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
  };

  // Validate and add file
  const validateAndAddFile = (file) => {
    const newErrors = { ...uploadErrors };
    
    // Check file type
    if (!allowedFileTypes.includes(file.type)) {
      newErrors[file.name] = `Invalid file type. Allowed types: ${allowedFileTypes.map(
        type => ALLOWED_FILE_TYPES[type] || type
      ).join(', ')}`;
      setUploadErrors(newErrors);
      return;
    }
    
    // Check file size
    if (file.size > maxFileSize) {
      newErrors[file.name] = `File is too large. Maximum size is ${maxFileSize / (1024 * 1024)}MB`;
      setUploadErrors(newErrors);
      return;
    }
    
    // Add file to list
    setFiles(prevFiles => {
      // Check if file with same name already exists
      const fileExists = prevFiles.some(f => f.name === file.name);
      if (fileExists) {
        newErrors[file.name] = 'A file with this name already exists';
        setUploadErrors(newErrors);
        return prevFiles;
      }
      
      // Add file with status
      const newFile = {
        file,
        id: `file-${Date.now()}-${prevFiles.length}`,
        status: 'ready', // ready, uploading, success, error
        progress: 0,
        description: ''
      };
      
      return [...prevFiles, newFile];
    });
  };

  // Handle drag events
  const handleDragEnter = (event) => {
    event.preventDefault();
    setIsDragActive(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsDragActive(false);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragActive(true);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragActive(false);
    handleFileSelect(event);
  };

  // Trigger file input click
  const handleBoxClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // Remove a file from the list
  const handleRemoveFile = (id) => {
    setFiles(prevFiles => prevFiles.filter(file => file.id !== id));
    
    // Clear any errors associated with this file
    const fileToRemove = files.find(file => file.id === id);
    if (fileToRemove) {
      const newErrors = { ...uploadErrors };
      delete newErrors[fileToRemove.file.name];
      setUploadErrors(newErrors);
    }
  };

  // Preview a file
  const handlePreviewFile = (file) => {
    // Only allow preview for certain file types
    const previewableTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    
    if (previewableTypes.includes(file.type)) {
      setPreviewFile({
        url: URL.createObjectURL(file),
        type: ALLOWED_FILE_TYPES[file.type],
        name: file.name
      });
    } else {
      // For non-previewable files, just show an error
      alert('Preview not available for this file type');
    }
  };

  // Close preview
  const handleClosePreview = () => {
    if (previewFile && previewFile.url) {
      URL.revokeObjectURL(previewFile.url);
    }
    setPreviewFile(null);
  };

  // Show file info dialog
  const handleShowFileInfo = (fileObj) => {
    setCurrentFile(fileObj);
    setFileInfo({ description: fileObj.description || '' });
    setFileInfoErrors({});
    setShowFileInfoDialog(true);
  };

  // Save file info
  const handleSaveFileInfo = () => {
    const errors = {};
    
    // Validate description (optional validation rules could go here)
    if (fileInfo.description.length > 500) {
      errors.description = 'Description is too long (maximum 500 characters)';
    }
    
    if (Object.keys(errors).length > 0) {
      setFileInfoErrors(errors);
      return;
    }
    
    // Update file in list
    setFiles(prevFiles => prevFiles.map(f => 
      f.id === currentFile.id ? { ...f, description: fileInfo.description } : f
    ));
    
    setShowFileInfoDialog(false);
  };

  // Upload all files
  const handleUploadFiles = async () => {
    if (files.length === 0) return;
    
    // Reset any previous errors
    setUploadErrors({});
    
    // Mark all files as uploading
    setFiles(prevFiles => prevFiles.map(f => ({ ...f, status: 'uploading', progress: 0 })));
    
    // Track progress for all files
    const newProgress = {};
    files.forEach(f => {
      newProgress[f.id] = 0;
    });
    setUploadProgress(newProgress);
    
    // Upload each file
    for (const fileObj of files) {
      try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', fileObj.file);
        formData.append('description', fileObj.description || '');
        
        // Call the onUpload callback with progress tracking
        if (onUpload) {
          await onUpload(formData, {
            onProgress: (progress) => {
              setUploadProgress(prev => ({ ...prev, [fileObj.id]: progress }));
              setFiles(prevFiles => prevFiles.map(f => 
                f.id === fileObj.id ? { ...f, progress } : f
              ));
            },
            fileObj
          });
          
          // Mark as success
          setFiles(prevFiles => prevFiles.map(f => 
            f.id === fileObj.id ? { ...f, status: 'success', progress: 100 } : f
          ));
        }
      } catch (error) {
        console.error('Upload error:', error);
        
        // Mark as error
        setFiles(prevFiles => prevFiles.map(f => 
          f.id === fileObj.id ? { ...f, status: 'error' } : f
        ));
        
        // Set error message
        setUploadErrors(prev => ({ 
          ...prev, 
          [fileObj.file.name]: error.message || 'Upload failed' 
        }));
      }
    }
  };

  // Get file status icon
  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle color="success" />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return null;
    }
  };

  // Render file list
  const renderFileList = () => {
    if (files.length === 0) return null;
    
    return (
      <List>
        {files.map((fileObj) => (
          <ListItem key={fileObj.id}>
            <ListItemText 
              primary={fileObj.file.name} 
              secondary={
                fileObj.status === 'uploading' ? (
                  <LinearProgress 
                    variant="determinate" 
                    value={fileObj.progress} 
                    sx={{ my: 1, height: 5 }}
                  />
                ) : fileObj.description || (
                  fileObj.status === 'success' ? 'Uploaded successfully' : 
                  fileObj.status === 'error' ? 'Upload failed' : 
                  'Ready to upload'
                )
              }
            />
            <ListItemSecondaryAction>
              {getStatusIcon(fileObj.status)}
              {showPreview && (
                <IconButton 
                  edge="end" 
                  aria-label="preview" 
                  onClick={() => handlePreviewFile(fileObj.file)}
                  disabled={fileObj.status === 'uploading'}
                >
                  <Visibility />
                </IconButton>
              )}
              <IconButton 
                edge="end" 
                aria-label="info" 
                onClick={() => handleShowFileInfo(fileObj)}
                disabled={fileObj.status === 'uploading'}
              >
                <Description />
              </IconButton>
              <IconButton 
                edge="end" 
                aria-label="delete" 
                onClick={() => handleRemoveFile(fileObj.id)}
                disabled={fileObj.status === 'uploading'}
              >
                <Delete />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    );
  };

  // Render errors
  const renderErrors = () => {
    const errorMessages = Object.values(uploadErrors);
    if (errorMessages.length === 0) return null;
    
    return (
      <Box sx={{ mt: 2 }}>
        {errorMessages.map((error, index) => (
          <Alert key={index} severity="error" sx={{ mb: 1 }}>
            {error}
          </Alert>
        ))}
      </Box>
    );
  };

  return (
    <Box>
      {/* Upload area */}
      <UploadBox
        isDragActive={isDragActive}
        isError={Object.keys(uploadErrors).length > 0}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleBoxClick}
      >
        <CloudUpload fontSize="large" color="primary" />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Drag & Drop Files Here
        </Typography>
        <Typography variant="body2" color="textSecondary">
          or click to browse
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          Allowed file types: {Object.values(ALLOWED_FILE_TYPES).join(', ')}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Maximum file size: {maxFileSize / (1024 * 1024)}MB
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Maximum files: {maxFiles}
        </Typography>
        <HiddenInput
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleFileSelect}
          accept={allowedFileTypes.join(',')}
        />
      </UploadBox>
      
      {/* File list */}
      {renderFileList()}
      
      {/* Errors */}
      {renderErrors()}
      
      {/* Upload button */}
      {files.length > 0 && (
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleUploadFiles}
            disabled={files.some(f => f.status === 'uploading')}
          >
            Upload {files.length} {files.length === 1 ? 'File' : 'Files'}
          </Button>
        </Box>
      )}
      
      {/* File preview dialog */}
      {previewFile && (
        <Dialog
          open={Boolean(previewFile)}
          onClose={handleClosePreview}
          fullWidth
          maxWidth="md"
        >
          <DocumentPreviewComponent
            documentUrl={previewFile.url}
            documentType={previewFile.type}
            previewTitle={previewFile.name}
            onClose={handleClosePreview}
          />
        </Dialog>
      )}
      
      {/* File info dialog */}
      <Dialog
        open={showFileInfoDialog}
        onClose={() => setShowFileInfoDialog(false)}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>File Information</DialogTitle>
        <DialogContent>
          <Typography variant="subtitle1" sx={{ mb: 2 }}>
            {currentFile?.file.name}
          </Typography>
          <TextField
            label="Description"
            multiline
            rows={4}
            fullWidth
            value={fileInfo.description}
            onChange={(e) => setFileInfo({ ...fileInfo, description: e.target.value })}
            error={Boolean(fileInfoErrors.description)}
            helperText={fileInfoErrors.description}
            variant="outlined"
            margin="normal"
          />
          <FormHelperText>
            Add a description for this file (optional)
          </FormHelperText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowFileInfoDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveFileInfo} color="primary">Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

DocumentUploadWithValidation.propTypes = {
  onUpload: PropTypes.func.isRequired,
  maxFiles: PropTypes.number,
  allowedFileTypes: PropTypes.arrayOf(PropTypes.string),
  maxFileSize: PropTypes.number,
  showPreview: PropTypes.bool
};

export default DocumentUploadWithValidation; 
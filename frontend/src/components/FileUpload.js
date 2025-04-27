import React, { useState, useCallback } from 'react';
import { Box, Button, Typography, CircularProgress, Alert, AlertTitle, FormHelperText, Paper } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DoneIcon from '@mui/icons-material/Done';
import InfoIcon from '@mui/icons-material/Info';
import axios from 'axios';
import config from '../config';

const FileUpload = ({ 
  onUploadComplete, 
  uploadType = 'user', 
  buttonText = 'Upload File',
  allowedFormats = ['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png'],
  maxFileSize = 10 * 1024 * 1024, // 10MB
  multipleFiles = false
}) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [files, setFiles] = useState([]);
  const [progress, setProgress] = useState(0);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const getUploadSignature = async () => {
    try {
      const response = await axios.get(`${config.apiUrl}/api/uploads/signature?type=${uploadType}`);
      return response.data;
    } catch (error) {
      console.error('Error getting upload signature:', error);
      if (error.response) {
        throw new Error(`Server error: ${error.response.data.error || error.response.statusText}`);
      } else if (error.request) {
        throw new Error('Network error: Unable to connect to the server');
      } else {
        throw new Error('Error preparing upload: ' + error.message);
      }
    }
  };

  const validateFile = (file) => {
    // Check file size
    if (file.size > maxFileSize) {
      throw new Error(`File size exceeds the maximum allowed (${(maxFileSize / (1024 * 1024)).toFixed(1)}MB)`);
    }

    // Check file format
    const extension = file.name.split('.').pop().toLowerCase();
    if (!allowedFormats.includes(extension)) {
      throw new Error(`Invalid file format. Allowed formats: ${allowedFormats.join(', ')}`);
    }
    
    // Check if file is empty
    if (file.size === 0) {
      throw new Error('File is empty');
    }

    return true;
  };

  const uploadToCloudinary = async (file, uploadSignature) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('api_key', uploadSignature.apiKey);
    formData.append('timestamp', uploadSignature.timestamp);
    formData.append('signature', uploadSignature.signature);
    formData.append('upload_preset', uploadSignature.uploadPreset);

    try {
      const response = await axios.post(
        `https://api.cloudinary.com/v1_1/${uploadSignature.cloudName}/auto/upload`,
        formData,
        {
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(percentCompleted);
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error uploading to Cloudinary:', error);
      if (error.response) {
        throw new Error(`Upload failed: ${error.response.data.error?.message || 'Server error'}`);
      } else if (error.request) {
        throw new Error('Network error: Unable to upload file');
      } else {
        throw new Error('Failed to upload file: ' + error.message);
      }
    }
  };

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);
    setFiles(selectedFiles);
    setError(null);
    setUploadSuccess(false);
    
    // Early validation to show errors before upload
    try {
      if (selectedFiles.length === 0) {
        return;
      }
      
      selectedFiles.forEach(validateFile);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleSubmit = useCallback(async (event) => {
    event.preventDefault();
    
    if (files.length === 0) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError(null);
    setProgress(0);
    setUploadSuccess(false);
    
    try {
      // Validate files
      for (const file of files) {
        validateFile(file);
      }
      
      // Get upload signature
      const uploadSignature = await getUploadSignature();
      
      // Upload files
      const uploadResults = [];
      for (const file of files) {
        const result = await uploadToCloudinary(file, uploadSignature);
        uploadResults.push(result);
      }
      
      // Call the callback with results
      if (multipleFiles) {
        onUploadComplete(uploadResults);
      } else {
        onUploadComplete(uploadResults[0]);
      }
      
      // Reset the file input and show success
      setFiles([]);
      setUploadSuccess(true);
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setUploadSuccess(false);
      }, 3000);
    } catch (error) {
      setError(error.message || 'An error occurred during upload');
    } finally {
      setUploading(false);
    }
  }, [files, onUploadComplete, multipleFiles, uploadType]);

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  return (
    <Box sx={{ mt: 2, mb: 2 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          <AlertTitle>Upload Error</AlertTitle>
          {error}
        </Alert>
      )}
      
      {uploadSuccess && (
        <Alert severity="success" sx={{ mb: 2 }}>
          <AlertTitle>Success!</AlertTitle>
          File uploaded successfully.
        </Alert>
      )}
      
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          id="fileUpload"
          multiple={multipleFiles}
          onChange={handleFileChange}
          style={{ display: 'none' }}
          accept={allowedFormats.map(format => `.${format}`).join(',')}
        />
        
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center',
          padding: 2,
          border: '1px dashed',
          borderColor: 'divider',
          borderRadius: 1,
          backgroundColor: 'background.paper'
        }}>
          <label htmlFor="fileUpload">
            <Button
              variant="outlined"
              component="span"
              startIcon={files.length > 0 ? <DoneIcon /> : <CloudUploadIcon />}
              disabled={uploading}
              sx={{ mb: 2 }}
              fullWidth
            >
              {files.length > 0 ? 'Change File' : buttonText}
            </Button>
          </label>
          
          {files.length > 0 && (
            <Paper 
              elevation={0} 
              sx={{ 
                p: 1, 
                mb: 2, 
                width: '100%', 
                backgroundColor: 'background.default',
                border: '1px solid',
                borderColor: 'divider'
              }}
            >
              {files.map((file, index) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: index < files.length - 1 ? 1 : 0 }}>
                  <UploadFileIcon sx={{ mr: 1, fontSize: 20, color: 'primary.main' }} />
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="body2" sx={{ 
                      overflow: 'hidden', 
                      textOverflow: 'ellipsis', 
                      whiteSpace: 'nowrap'
                    }}>
                      {file.name}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {formatFileSize(file.size)}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Paper>
          )}
          
          <FormHelperText sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
            <InfoIcon sx={{ fontSize: 16, mr: 0.5, color: 'info.main' }} /> 
            Accepted formats: {allowedFormats.join(', ')} (Max size: {(maxFileSize / (1024 * 1024)).toFixed(1)}MB)
          </FormHelperText>
          
          <Button
            variant="contained"
            color="primary"
            type="submit"
            disabled={uploading || files.length === 0 || error !== null}
            sx={{ mt: 1 }}
            fullWidth
          >
            {uploading ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} />
                Uploading {progress}%
              </>
            ) : (
              'Upload'
            )}
          </Button>
        </Box>
      </form>
    </Box>
  );
};

export default FileUpload; 
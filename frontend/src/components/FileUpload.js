import React, { useState, useCallback } from 'react';
import { Box, Button, Typography, CircularProgress, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';
import { API_URL } from '../config';

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

  const getUploadSignature = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/uploads/signature?type=${uploadType}`);
      return response.data;
    } catch (error) {
      console.error('Error getting upload signature:', error);
      throw new Error('Failed to get upload credentials');
    }
  };

  const validateFile = (file) => {
    // Check file size
    if (file.size > maxFileSize) {
      throw new Error(`File size exceeds the maximum allowed (${maxFileSize / (1024 * 1024)}MB)`);
    }

    // Check file format
    const extension = file.name.split('.').pop().toLowerCase();
    if (!allowedFormats.includes(extension)) {
      throw new Error(`Invalid file format. Allowed formats: ${allowedFormats.join(', ')}`);
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
      throw new Error('Failed to upload file to cloud storage');
    }
  };

  const handleFileChange = (event) => {
    setFiles(Array.from(event.target.files));
    setError(null);
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
      
      // Reset the file input
      setFiles([]);
    } catch (error) {
      setError(error.message || 'An error occurred during upload');
    } finally {
      setUploading(false);
    }
  }, [files, onUploadComplete, multipleFiles, uploadType]);

  return (
    <Box sx={{ mt: 2, mb: 2 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          id="fileUpload"
          multiple={multipleFiles}
          onChange={handleFileChange}
          style={{ display: 'none' }}
          accept={allowedFormats.map(format => `.${format}`).join(',')}
        />
        
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <label htmlFor="fileUpload">
            <Button
              variant="outlined"
              component="span"
              startIcon={<CloudUploadIcon />}
              disabled={uploading}
              sx={{ mb: 2 }}
            >
              {buttonText}
            </Button>
          </label>
          
          {files.length > 0 && (
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {files.length} file(s) selected: {files.map(f => f.name).join(', ')}
            </Typography>
          )}
          
          <Button
            variant="contained"
            color="primary"
            type="submit"
            disabled={uploading || files.length === 0}
            sx={{ mt: 1 }}
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
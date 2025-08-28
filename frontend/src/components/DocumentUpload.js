import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Alert,
  Paper,
  IconButton,
  Chip,
  useTheme,
  Fade,
  Zoom
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Description as DocumentIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const DocumentUpload = ({ onUploaded, onError }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const theme = useTheme();

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setUploadStatus('uploading');

    try {
      // For now, we'll use a mock user ID - you'll need to integrate with your auth system
      const mockUserId = 'mock-user-id';
      
      // Import the service dynamically to avoid issues during build
      const { default: documentAIService } = await import('../services/documentAI');
      
      // Upload document
      setUploadStatus('uploading');
      const uploadResult = await documentAIService.uploadDocument(selectedFile, mockUserId);
      setUploadStatus('uploaded');

      // Process document
      setUploadStatus('processing');
      await documentAIService.processDocument(uploadResult.id);
      
      setUploadStatus('success');
      onUploaded?.(uploadResult.id);
      
      // Reset after success
      setTimeout(() => {
        setSelectedFile(null);
        setUploadStatus(null);
      }, 3000);

    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('error');
      onError?.(error.message);
    } finally {
      setIsUploading(false);
    }
  };

  const getStatusColor = () => {
    switch (uploadStatus) {
      case 'uploading': return 'info';
      case 'uploaded': return 'warning';
      case 'processing': return 'warning';
      case 'success': return 'success';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const getStatusText = () => {
    switch (uploadStatus) {
      case 'uploading': return 'Uploading...';
      case 'uploaded': return 'Uploaded, processing...';
      case 'processing': return 'Processing document...';
      case 'success': return 'Document ready!';
      case 'error': return 'Upload failed';
      default: return '';
    }
  };

  const getStatusIcon = () => {
    switch (uploadStatus) {
      case 'uploading': return <CircularProgress size={20} />;
      case 'uploaded': return <CircularProgress size={20} />;
      case 'processing': return <CircularProgress size={20} />;
      case 'success': return <SuccessIcon />;
      case 'error': return <ErrorIcon />;
      default: return null;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box
        sx={{
          p: 4,
          borderRadius: 3,
          backgroundColor: '#ffffff',
          border: '2px dashed',
          borderColor: selectedFile ? '#2563eb' : '#cbd5e1',
          transition: 'all 0.3s ease',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          '&:hover': {
            borderColor: '#2563eb',
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 32px rgba(37, 99, 235, 0.15)',
          }
        }}
      >
        <Box sx={{ textAlign: 'center' }}>
          <motion.div
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            <IconButton
              component="label"
              sx={{
                width: 80,
                height: 80,
                backgroundColor: '#2563eb',
                color: 'white',
                '&:hover': {
                  backgroundColor: '#1d4ed8',
                  transform: 'scale(1.05)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              <UploadIcon sx={{ fontSize: 40 }} />
              <input
                type="file"
                hidden
                accept=".pdf,.doc,.docx,.txt"
                onChange={handleFileSelect}
                disabled={isUploading}
              />
            </IconButton>
          </motion.div>

          <Typography
            variant="h6"
            sx={{
              mt: 2,
              mb: 1,
              color: '#1e293b',
              fontWeight: 600,
            }}
          >
            Upload Legal Document
          </Typography>

          <Typography
            variant="body2"
            sx={{
              color: '#475569',
              mb: 3,
            }}
          >
            Upload PDFs, Word documents, or text files for AI analysis
          </Typography>

          {selectedFile && (
            <Fade in={true}>
              <Box sx={{ mb: 3 }}>
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    border: `1px solid ${theme.palette.primary.light}`,
                    borderRadius: 2,
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <DocumentIcon color="primary" />
                    <Typography variant="body2" sx={{ flex: 1 }}>
                      {selectedFile.name}
                    </Typography>
                    <Chip
                      label={`${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  </Box>
                </Paper>
              </Box>
            </Fade>
          )}

          {uploadStatus && (
            <Zoom in={true}>
              <Alert
                severity={getStatusColor()}
                icon={getStatusIcon()}
                sx={{ mb: 3 }}
              >
                {getStatusText()}
              </Alert>
            </Zoom>
          )}

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!selectedFile || isUploading}
              startIcon={isUploading ? <CircularProgress size={20} /> : <UploadIcon />}
              sx={{
                borderRadius: 12,
                px: 4,
                py: 1.5,
                fontWeight: 600,
                textTransform: 'none',
                boxShadow: '0 4px 12px rgba(37, 99, 235, 0.2)',
                '&:hover': {
                  boxShadow: '0 8px 24px rgba(37, 99, 235, 0.3)',
                  transform: 'translateY(-1px)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              {isUploading ? 'Processing...' : 'Upload & Process'}
            </Button>

            {selectedFile && (
              <Button
                variant="outlined"
                onClick={() => {
                  setSelectedFile(null);
                  setUploadStatus(null);
                }}
                disabled={isUploading}
                sx={{
                  borderRadius: 2,
                  px: 4,
                  py: 1.5,
                  fontWeight: 600,
                  textTransform: 'none',
                }}
              >
                Clear
              </Button>
            )}
          </Box>

          <Typography
            variant="caption"
            sx={{
              display: 'block',
              mt: 2,
              color: '#64748b',
            }}
          >
            Supported formats: PDF, DOC, DOCX, TXT (Max 50MB)
          </Typography>
        </Box>
      </Box>
    </motion.div>
  );
};

export default DocumentUpload; 
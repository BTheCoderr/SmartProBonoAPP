import React, { useState, useRef } from 'react';
import { 
  Box, 
  Button, 
  Typography, 
  Paper, 
  CircularProgress, 
  Snackbar, 
  Alert,
  IconButton
} from '@mui/material';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import CloseIcon from '@mui/icons-material/Close';
import DocumentScannerIcon from '@mui/icons-material/DocumentScanner';
import { useAuth } from '../context/AuthContext';
import { documentsApi } from '../services/api';

const MobileFileScanner = ({ onScanComplete, documentType = 'general' }) => {
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' });
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);
  const { currentUser } = useAuth();

  const isMobileDevice = () => {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  };

  const handleCameraCapture = () => {
    console.log('Camera capture triggered');
    if (cameraInputRef.current) {
      // Log the current environment
      console.log('User agent:', navigator.userAgent);
      console.log('Is mobile device:', isMobileDevice());
      
      // Always try to use the camera directly
      cameraInputRef.current.click();
    }
  };

  const handleFileUpload = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const processImage = async (file) => {
    setScanning(true);
    setError(null);
    
    try {
      // Create preview URL
      const previewUrl = URL.createObjectURL(file);
      setPreviewUrl(previewUrl);
      
      // Call the documents API to scan the document
      const result = await documentsApi.scanDocument(file, documentType);
      setScanResult(result);
      
      // Notify parent component
      if (onScanComplete) {
        onScanComplete(result);
      }
      
      setNotification({
        open: true,
        message: 'Document successfully scanned and processed',
        severity: 'success'
      });
    } catch (err) {
      console.error('Error processing document:', err);
      setError(err.message || 'Failed to process document');
      setNotification({
        open: true,
        message: 'Error processing document: ' + (err.message || 'Unknown error'),
        severity: 'error'
      });
    } finally {
      setScanning(false);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      processImage(file);
    }
  };

  const resetScan = () => {
    setScanResult(null);
    setPreviewUrl(null);
    setError(null);
  };

  const closeNotification = () => {
    setNotification({ ...notification, open: false });
  };

  return (
    <Paper elevation={3} sx={{ p: 3, borderRadius: 2, mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <DocumentScannerIcon color="primary" sx={{ mr: 1 }} />
        <Typography variant="h6" component="h2">
          Scan & Upload Document
        </Typography>
      </Box>
      
      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary">
          Take a photo of your document or upload an existing image. 
          We'll process it automatically to extract the information.
        </Typography>
      </Box>
      
      {/* Hidden file inputs */}
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      
      {/* Separate input specifically for camera capture */}
      <input
        type="file"
        accept="image/*"
        capture="environment"
        ref={cameraInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      
      {!scanResult && !scanning && !previewUrl && (
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, my: 3 }}>
          <Button
            variant="contained"
            startIcon={<CameraAltIcon />}
            onClick={handleCameraCapture}
          >
            {isMobileDevice() ? "Take Photo" : "Capture Image"}
          </Button>
          <Button
            variant="outlined"
            startIcon={<FileUploadIcon />}
            onClick={handleFileUpload}
          >
            Choose Image File
          </Button>
        </Box>
      )}
      
      {scanning && (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', my: 3 }}>
          <CircularProgress size={40} />
          <Typography variant="body2" sx={{ mt: 2 }}>
            Processing document...
          </Typography>
        </Box>
      )}
      
      {previewUrl && !scanning && (
        <Box sx={{ position: 'relative', my: 2 }}>
          <IconButton
            sx={{ position: 'absolute', top: 5, right: 5, bgcolor: 'rgba(255,255,255,0.7)' }}
            onClick={resetScan}
          >
            <CloseIcon />
          </IconButton>
          
          <img
            src={previewUrl}
            alt="Document preview"
            style={{ 
              width: '100%', 
              maxHeight: '300px', 
              objectFit: 'contain',
              borderRadius: '4px'
            }}
          />
          
          {scanResult && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle1" fontWeight="bold">
                Detected Information:
              </Typography>
              <Box component="pre" sx={{ 
                p: 2, 
                bgcolor: 'grey.100', 
                borderRadius: 1,
                overflow: 'auto',
                fontSize: '0.875rem',
                maxHeight: '150px'
              }}>
                {JSON.stringify(scanResult.extractedData || {}, null, 2)}
              </Box>
            </Box>
          )}
          
          {!scanResult && !scanning && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <Button
                variant="contained"
                onClick={resetScan}
              >
                Retry Scan
              </Button>
            </Box>
          )}
        </Box>
      )}
      
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={closeNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={closeNotification} severity={notification.severity} sx={{ width: '100%' }}>
          {notification.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default MobileFileScanner; 
import React, { useRef, useState } from 'react';
import SignatureCanvas from 'react-signature-canvas';
import {
  Box,
  Button,
  Typography,
  Alert,
  Card,
  CardContent,
  Stack,
  IconButton,
} from '@mui/material';
import { Save as SaveIcon, Clear as ClearIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';
import PdfService from '../services/PdfService';

const SignatureCapture = ({ caseNumber, onUploaded, onClear }) => {
  const sigRef = useRef(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [uploadedPath, setUploadedPath] = useState(null);

  const handleSave = async () => {
    try {
      setBusy(true);
      setError(null);
      setSuccess(false);

      if (!sigRef.current || sigRef.current.isEmpty()) {
        setError('Please add a signature first.');
        return;
      }

      // Trim transparent edges and export as PNG
      const dataUrl = sigRef.current.getTrimmedCanvas().toDataURL('image/png');
      const response = await fetch(dataUrl);
      const blob = await response.blob();
      const file = new File([blob], 'signature.png', { type: 'image/png' });

      const form = new FormData();
      form.append('file', file);
      form.append('caseNumber', caseNumber);

      // Upload to Supabase Storage
      const result = await PdfService.uploadSignature(file, caseNumber);
      
      if (result.success) {
        setUploadedPath(result.path);
        setSuccess(true);
        onUploaded?.(result.path);
      } else {
        throw new Error(result.message || 'Upload failed');
      }

    } catch (err) {
      setError(err?.message || 'Upload failed');
    } finally {
      setBusy(false);
    }
  };

  const handleClear = () => {
    sigRef.current?.clear();
    setError(null);
    setSuccess(false);
    setUploadedPath(null);
    onClear?.();
  };

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ textAlign: 'center' }}>
          Digital Signature Capture
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
          Sign with your finger, mouse, or stylus. Your signature will be securely stored and can be added to legal documents.
        </Typography>

        {/* Signature Canvas */}
        <Box
          sx={{
            border: '2px solid #e0e0e0',
            borderRadius: 2,
            backgroundColor: '#ffffff',
            p: 1,
            mb: 2,
            '& canvas': {
              borderRadius: 1,
              width: '100%',
              height: 'auto',
            },
          }}
        >
          <SignatureCanvas
            ref={sigRef}
            penColor="black"
            canvasProps={{
              width: 640,
              height: 220,
              className: 'signature-canvas',
            }}
          />
        </Box>

        {/* Action Buttons */}
        <Stack direction="row" spacing={2} justifyContent="center" sx={{ mb: 2 }}>
          <Button
            variant="contained"
            startIcon={busy ? <SaveIcon /> : <SaveIcon />}
            onClick={handleSave}
            disabled={busy}
            sx={{
              backgroundColor: '#1565C0',
              '&:hover': {
                backgroundColor: '#0D47A1',
              },
            }}
          >
            {busy ? 'Saving...' : 'Save Signature'}
          </Button>
          
          <Button
            variant="outlined"
            startIcon={<ClearIcon />}
            onClick={handleClear}
            sx={{
              borderColor: '#1565C0',
              color: '#1565C0',
              '&:hover': {
                borderColor: '#0D47A1',
                backgroundColor: 'rgba(21, 101, 192, 0.04)',
              },
            }}
          >
            Clear
          </Button>
        </Stack>

        {/* Status Messages */}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert 
            severity="success" 
            icon={<CheckCircleIcon />}
            sx={{ mb: 2 }}
          >
            Signature saved successfully! Path: {uploadedPath}
          </Alert>
        )}

        {/* Instructions */}
        <Box sx={{ mt: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
          <Typography variant="body2" color="text.secondary">
            <strong>Instructions:</strong>
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            • Use your finger, mouse, or stylus to sign in the box above
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • Click "Save Signature" to store it securely
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • Click "Clear" to start over
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • Your signature will be automatically added to generated PDFs
          </Typography>
        </Box>

        {/* Case Info */}
        {caseNumber && (
          <Box sx={{ mt: 2, p: 1, backgroundColor: '#e3f2fd', borderRadius: 1 }}>
            <Typography variant="caption" color="primary">
              Case Number: {caseNumber}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default SignatureCapture;

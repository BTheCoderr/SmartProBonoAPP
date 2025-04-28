import React, { useState, useEffect, useRef } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { Box, Button, CircularProgress, Typography, Paper } from '@mui/material';
import SignatureCanvas from 'react-signature-canvas';
import { validateSignature } from '../../utils/validation';

// Set pdf.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const DocumentPreview = ({ 
  documentUrl, 
  onSignatureComplete, 
  allowSignature = false,
  showToolbar = true 
}) => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [scale, setScale] = useState(1.0);
  const [signature, setSignature] = useState(null);
  
  const signatureRef = useRef();

  useEffect(() => {
    setLoading(true);
    setError(null);
  }, [documentUrl]);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setLoading(false);
  };

  const onDocumentLoadError = (error) => {
    console.error('Error loading document:', error);
    setError('Failed to load document. Please try again.');
    setLoading(false);
  };

  const handlePrevPage = () => {
    setPageNumber(page => Math.max(page - 1, 1));
  };

  const handleNextPage = () => {
    setPageNumber(page => Math.min(page + 1, numPages));
  };

  const handleZoomIn = () => {
    setScale(scale => Math.min(scale + 0.2, 2.0));
  };

  const handleZoomOut = () => {
    setScale(scale => Math.max(scale - 0.2, 0.6));
  };

  const handleSignatureComplete = async () => {
    if (!signatureRef.current) return;

    const signatureData = {
      signatureType: 'drawn',
      signatureData: signatureRef.current.toDataURL(),
      dateTime: new Date(),
      ipAddress: await fetch('https://api.ipify.org?format=json')
        .then(res => res.json())
        .then(data => data.ip),
      consent: true
    };

    const validation = await validateSignature(signatureData);
    if (validation.isValid) {
      setSignature(signatureData);
      onSignatureComplete?.(signatureData);
    } else {
      setError('Invalid signature. Please try again.');
    }
  };

  const clearSignature = () => {
    if (signatureRef.current) {
      signatureRef.current.clear();
      setSignature(null);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', maxWidth: 1200, mx: 'auto' }}>
      {showToolbar && (
        <Paper sx={{ mb: 2, p: 1, display: 'flex', justifyContent: 'space-between' }}>
          <Box>
            <Button onClick={handlePrevPage} disabled={pageNumber <= 1}>
              Previous
            </Button>
            <Button onClick={handleNextPage} disabled={pageNumber >= numPages}>
              Next
            </Button>
            <Typography component="span" sx={{ mx: 2 }}>
              Page {pageNumber} of {numPages}
            </Typography>
          </Box>
          <Box>
            <Button onClick={handleZoomOut}>Zoom Out</Button>
            <Button onClick={handleZoomIn}>Zoom In</Button>
          </Box>
        </Paper>
      )}

      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center',
        boxShadow: 3,
        bgcolor: 'background.paper',
        borderRadius: 1,
        overflow: 'hidden'
      }}>
        <Document
          file={documentUrl}
          onLoadSuccess={onDocumentLoadSuccess}
          onLoadError={onDocumentLoadError}
          loading={
            <Box display="flex" justifyContent="center" p={2}>
              <CircularProgress />
            </Box>
          }
        >
          <Page 
            pageNumber={pageNumber} 
            scale={scale}
            renderTextLayer={false}
            renderAnnotationLayer={false}
          />
        </Document>
      </Box>

      {allowSignature && (
        <Box sx={{ mt: 3, p: 2, border: '1px solid', borderColor: 'divider' }}>
          <Typography variant="h6" gutterBottom>
            Digital Signature
          </Typography>
          <Box sx={{ 
            border: '1px solid', 
            borderColor: 'divider',
            bgcolor: 'background.paper',
            height: 200 
          }}>
            <SignatureCanvas
              ref={signatureRef}
              canvasProps={{
                width: 500,
                height: 200,
                className: 'signature-canvas'
              }}
            />
          </Box>
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            <Button 
              variant="contained" 
              color="primary"
              onClick={handleSignatureComplete}
              disabled={!signatureRef.current || !signatureRef.current.toData().length}
            >
              Apply Signature
            </Button>
            <Button 
              variant="outlined"
              onClick={clearSignature}
            >
              Clear
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default DocumentPreview; 
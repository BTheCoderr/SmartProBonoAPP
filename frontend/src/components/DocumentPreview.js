import React, { useState, useEffect } from 'react';
import { Button, CircularProgress, Paper, Typography, Box, IconButton, Tooltip } from '@mui/material';
import { Download, Print, ZoomIn, ZoomOut, RotateLeft, RotateRight, Lock } from '@mui/icons-material';
import { Document, Page, pdfjs } from 'react-pdf';
import ApiService from '../services/ApiService';

// Set PDF worker source
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const DocumentPreview = ({ documentId, templateId, data, documentUrl, title }) => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState(1.0);
  const [rotation, setRotation] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(documentUrl || null);
  
  useEffect(() => {
    if (!pdfUrl && (documentId || (templateId && data))) {
      generatePreview();
    }
  }, [documentId, templateId, data, pdfUrl]);
  
  const generatePreview = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let response;
      
      if (documentId) {
        // Fetch existing document
        response = await ApiService.get(`/api/documents/${documentId}`, { responseType: 'blob' });
      } else if (templateId && data) {
        // Generate document preview
        response = await ApiService.post('/api/templates/preview', {
          template_id: templateId,
          data: data
        }, { responseType: 'blob' });
      } else {
        throw new Error('Either documentId or templateId with data must be provided');
      }
      
      // Create a blob URL for the PDF
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      setPdfUrl(url);
    } catch (err) {
      console.error('Error loading document preview:', err);
      setError('Failed to load document preview');
    } finally {
      setLoading(false);
    }
  };
  
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };
  
  const changePage = (offset) => {
    setPageNumber(prevPageNumber => {
      const newPageNumber = prevPageNumber + offset;
      return Math.min(Math.max(1, newPageNumber), numPages);
    });
  };
  
  const previousPage = () => changePage(-1);
  
  const nextPage = () => changePage(1);
  
  const zoomIn = () => setScale(prevScale => Math.min(2.0, prevScale + 0.1));
  
  const zoomOut = () => setScale(prevScale => Math.max(0.5, prevScale - 0.1));
  
  const rotateLeft = () => setRotation(prevRotation => (prevRotation - 90) % 360);
  
  const rotateRight = () => setRotation(prevRotation => (prevRotation + 90) % 360);
  
  const downloadPdf = () => {
    if (pdfUrl) {
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = `${title || 'document'}.pdf`;
      link.click();
    }
  };
  
  const printPdf = () => {
    if (pdfUrl) {
      const iframe = document.createElement('iframe');
      iframe.style.display = 'none';
      iframe.src = pdfUrl;
      
      iframe.onload = () => {
        iframe.contentWindow.print();
      };
      
      document.body.appendChild(iframe);
    }
  };
  
  // Handle cleanup when component unmounts
  useEffect(() => {
    return () => {
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }
    };
  }, [pdfUrl]);
  
  return (
    <Paper elevation={3} sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">{title || 'Document Preview'}</Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Download">
            <IconButton onClick={downloadPdf} disabled={!pdfUrl}>
              <Download />
            </IconButton>
          </Tooltip>
          <Tooltip title="Print">
            <IconButton onClick={printPdf} disabled={!pdfUrl}>
              <Print />
            </IconButton>
          </Tooltip>
          <Tooltip title="Zoom In">
            <IconButton onClick={zoomIn} disabled={!pdfUrl || scale >= 2.0}>
              <ZoomIn />
            </IconButton>
          </Tooltip>
          <Tooltip title="Zoom Out">
            <IconButton onClick={zoomOut} disabled={!pdfUrl || scale <= 0.5}>
              <ZoomOut />
            </IconButton>
          </Tooltip>
          <Tooltip title="Rotate Left">
            <IconButton onClick={rotateLeft} disabled={!pdfUrl}>
              <RotateLeft />
            </IconButton>
          </Tooltip>
          <Tooltip title="Rotate Right">
            <IconButton onClick={rotateRight} disabled={!pdfUrl}>
              <RotateRight />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      
      <Box sx={{ flex: 1, overflow: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <Typography color="error">{error}</Typography>
          </Box>
        ) : pdfUrl ? (
          <Box sx={{ flex: 1, width: '100%', textAlign: 'center' }}>
            <Document
              file={pdfUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              loading={<CircularProgress />}
              error={<Typography color="error">Failed to load PDF document</Typography>}
              options={{ workerSrc: pdfjs.GlobalWorkerOptions.workerSrc }}
            >
              <Page
                pageNumber={pageNumber}
                scale={scale}
                rotate={rotation}
                renderTextLayer={false}
                renderAnnotationLayer={false}
                renderInteractiveForms={false}
                width={Math.min(600, window.innerWidth - 60)}
              />
            </Document>
            
            <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2 }}>
              <Button
                variant="outlined"
                onClick={previousPage}
                disabled={pageNumber <= 1}
              >
                Previous
              </Button>
              
              <Typography>
                Page {pageNumber} of {numPages || '--'}
              </Typography>
              
              <Button
                variant="outlined"
                onClick={nextPage}
                disabled={pageNumber >= numPages}
              >
                Next
              </Button>
            </Box>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <Typography>No document to preview</Typography>
          </Box>
        )}
      </Box>
      
      {documentId && (
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<Lock />}
            onClick={() => {
              // Implement secure document download here
            }}
          >
            Download Signed Document
          </Button>
        </Box>
      )}
    </Paper>
  );
};

export default DocumentPreview; 
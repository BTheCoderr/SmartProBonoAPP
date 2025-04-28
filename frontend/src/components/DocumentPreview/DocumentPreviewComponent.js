import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, Typography, CircularProgress, IconButton, 
  Slider, Paper, Alert, Tooltip, Button 
} from '@mui/material';
import {
  ZoomIn, ZoomOut, Print, Download, Fullscreen,
  RotateLeft, RotateRight, NavigateNext, NavigateBefore
} from '@mui/icons-material';
import PropTypes from 'prop-types';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const DocumentPreviewComponent = ({ 
  documentUrl, 
  documentType = 'pdf',
  previewTitle = 'Document Preview',
  onClose,
  onDownload,
  showToolbar = true,
  initialZoom = 1.0
}) => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [zoom, setZoom] = useState(initialZoom);
  const [rotation, setRotation] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const containerRef = useRef(null);
  const documentRef = useRef(null);

  // Handle document load success
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setLoading(false);
  };

  // Handle document load error
  const onDocumentLoadError = (error) => {
    console.error('Error loading document:', error);
    setError('Failed to load document. Please try again later.');
    setLoading(false);
  };

  // Navigate to previous page
  const goToPrevPage = () => {
    if (pageNumber > 1) {
      setPageNumber(pageNumber - 1);
    }
  };

  // Navigate to next page
  const goToNextPage = () => {
    if (pageNumber < numPages) {
      setPageNumber(pageNumber + 1);
    }
  };

  // Handle zoom in
  const zoomIn = () => {
    setZoom(Math.min(zoom + 0.2, 3));
  };

  // Handle zoom out
  const zoomOut = () => {
    setZoom(Math.max(zoom - 0.2, 0.5));
  };

  // Handle zoom slider change
  const handleZoomChange = (event, newValue) => {
    setZoom(newValue);
  };

  // Rotate document left
  const rotateLeft = () => {
    setRotation((rotation - 90) % 360);
  };

  // Rotate document right
  const rotateRight = () => {
    setRotation((rotation + 90) % 360);
  };

  // Handle print
  const handlePrint = () => {
    if (documentUrl) {
      const printWindow = window.open(documentUrl, '_blank');
      printWindow.onload = () => {
        printWindow.print();
      };
    }
  };

  // Handle download
  const handleDownload = () => {
    if (onDownload && typeof onDownload === 'function') {
      onDownload();
    } else if (documentUrl) {
      const link = document.createElement('a');
      link.href = documentUrl;
      link.download = `document.${documentType}`;
      link.click();
    }
  };

  // Handle fullscreen
  const handleFullscreen = () => {
    if (containerRef.current) {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else {
        containerRef.current.requestFullscreen();
      }
    }
  };

  // Render PDF preview
  const renderPdfPreview = () => (
    <Document
      file={documentUrl}
      onLoadSuccess={onDocumentLoadSuccess}
      onLoadError={onDocumentLoadError}
      loading={<CircularProgress />}
      ref={documentRef}
    >
      <Page
        pageNumber={pageNumber}
        scale={zoom}
        rotate={rotation}
        renderTextLayer={true}
        renderAnnotationLayer={true}
      />
    </Document>
  );

  // Render image preview
  const renderImagePreview = () => (
    <Box
      component="img"
      src={documentUrl}
      alt="Document preview"
      sx={{
        maxWidth: '100%',
        maxHeight: '80vh',
        transform: `scale(${zoom}) rotate(${rotation}deg)`,
        transition: 'transform 0.2s ease',
      }}
      onLoad={() => setLoading(false)}
      onError={() => {
        setError('Failed to load image. Please try again later.');
        setLoading(false);
      }}
    />
  );

  // Render document preview based on document type
  const renderDocumentPreview = () => {
    if (loading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
      );
    }

    if (error) {
      return (
        <Alert severity="error" sx={{ my: 2 }}>
          {error}
        </Alert>
      );
    }

    switch (documentType.toLowerCase()) {
      case 'pdf':
        return renderPdfPreview();
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
        return renderImagePreview();
      default:
        return (
          <Alert severity="warning" sx={{ my: 2 }}>
            Preview not available for this document type. Please download to view.
          </Alert>
        );
    }
  };

  return (
    <Paper
      ref={containerRef}
      elevation={3}
      sx={{ 
        p: 2, 
        display: 'flex', 
        flexDirection: 'column', 
        maxHeight: '90vh',
        width: '100%',
        overflow: 'hidden'
      }}
    >
      {/* Header with title */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2, alignItems: 'center' }}>
        <Typography variant="h6" component="h2">
          {previewTitle}
        </Typography>
        {onClose && (
          <Button onClick={onClose} color="primary">
            Close
          </Button>
        )}
      </Box>

      {/* Toolbar */}
      {showToolbar && (
        <Box sx={{ display: 'flex', mb: 2, flexWrap: 'wrap', gap: 1 }}>
          {/* Page navigation - only for PDFs */}
          {documentType.toLowerCase() === 'pdf' && numPages > 1 && (
            <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
              <Tooltip title="Previous page">
                <IconButton onClick={goToPrevPage} disabled={pageNumber <= 1}>
                  <NavigateBefore />
                </IconButton>
              </Tooltip>
              <Typography variant="body2" sx={{ mx: 1 }}>
                {pageNumber} / {numPages}
              </Typography>
              <Tooltip title="Next page">
                <IconButton onClick={goToNextPage} disabled={pageNumber >= numPages}>
                  <NavigateNext />
                </IconButton>
              </Tooltip>
            </Box>
          )}

          {/* Zoom controls */}
          <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
            <Tooltip title="Zoom out">
              <IconButton onClick={zoomOut} disabled={zoom <= 0.5}>
                <ZoomOut />
              </IconButton>
            </Tooltip>
            <Slider
              value={zoom}
              min={0.5}
              max={3}
              step={0.1}
              onChange={handleZoomChange}
              aria-labelledby="zoom-slider"
              sx={{ width: 100, mx: 1 }}
            />
            <Tooltip title="Zoom in">
              <IconButton onClick={zoomIn} disabled={zoom >= 3}>
                <ZoomIn />
              </IconButton>
            </Tooltip>
          </Box>

          {/* Rotation controls */}
          <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
            <Tooltip title="Rotate left">
              <IconButton onClick={rotateLeft}>
                <RotateLeft />
              </IconButton>
            </Tooltip>
            <Tooltip title="Rotate right">
              <IconButton onClick={rotateRight}>
                <RotateRight />
              </IconButton>
            </Tooltip>
          </Box>

          {/* Actions */}
          <Box sx={{ display: 'flex', alignItems: 'center', ml: 'auto' }}>
            <Tooltip title="Print">
              <IconButton onClick={handlePrint}>
                <Print />
              </IconButton>
            </Tooltip>
            <Tooltip title="Download">
              <IconButton onClick={handleDownload}>
                <Download />
              </IconButton>
            </Tooltip>
            <Tooltip title="Fullscreen">
              <IconButton onClick={handleFullscreen}>
                <Fullscreen />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      )}

      {/* Document preview */}
      <Box 
        sx={{ 
          flex: 1, 
          overflow: 'auto', 
          display: 'flex', 
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '300px'
        }}
      >
        {renderDocumentPreview()}
      </Box>
    </Paper>
  );
};

DocumentPreviewComponent.propTypes = {
  documentUrl: PropTypes.string.isRequired,
  documentType: PropTypes.string,
  previewTitle: PropTypes.string,
  onClose: PropTypes.func,
  onDownload: PropTypes.func,
  showToolbar: PropTypes.bool,
  initialZoom: PropTypes.number
};

export default DocumentPreviewComponent; 
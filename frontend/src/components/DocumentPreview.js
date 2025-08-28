import React, { useState, useEffect, useRef } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  IconButton,
  Tooltip,
  CircularProgress,
  Slider,
  Typography,
  Alert,
  Paper,
  Divider
} from '@mui/material';
import {
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  Fullscreen as FullscreenIcon,
  FullscreenExit as FullscreenExitIcon,
  NavigateBefore as NavigateBeforeIcon,
  NavigateNext as NavigateNextIcon,
  PanTool as PanToolIcon
} from '@mui/icons-material';
import { Document, Page, pdfjs } from 'react-pdf';
import { TransformWrapper, TransformComponent } from 'react-zoom-pan-pinch';
import ApiService from '../services/ApiService';
import debounce from 'lodash/debounce';

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const DocumentPreview = ({
  open,
  onClose,
  formData,
  formType,
  autoUpdate = true,
  showControls = true
}) => {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [scale, setScale] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const previewContainerRef = useRef(null);

  // Generate or update PDF preview
  const generatePreview = async (data) => {
    try {
      setLoading(true);
      setError(null);
      const response = await ApiService.post('/api/documents/preview', {
        formType,
        data
      }, { responseType: 'blob' });
      const url = URL.createObjectURL(response.data);
      setPdfUrl(url);
      setLastUpdate(new Date());
    } catch (err) {
      setError('Failed to generate preview');
      console.error('Preview generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Debounced preview generation for real-time updates
  const debouncedGeneratePreview = debounce(generatePreview, 1000);

  // Initial preview generation and auto-update setup
  useEffect(() => {
    if (open && formData) {
      generatePreview(formData);
    }
    return () => {
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }
    };
  }, [open, formData]);

  // Handle document load
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setCurrentPage(1);
  };

  // Handle zoom controls
  const handleZoomIn = () => {
    setScale(prevScale => Math.min(prevScale + 0.2, 3));
  };

  const handleZoomOut = () => {
    setScale(prevScale => Math.max(prevScale - 0.2, 0.5));
  };

  const handleZoomChange = (event, newValue) => {
    setScale(newValue);
  };

  // Handle page navigation
  const handlePreviousPage = () => {
    setCurrentPage(prevPage => Math.max(prevPage - 1, 1));
  };

  const handleNextPage = () => {
    setCurrentPage(prevPage => Math.min(prevPage + 1, numPages));
  };

  // Handle fullscreen toggle
  const toggleFullscreen = () => {
    if (!isFullscreen) {
      if (previewContainerRef.current.requestFullscreen) {
        previewContainerRef.current.requestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
    setIsFullscreen(!isFullscreen);
  };

  // Handle document download
  const handleDownload = async () => {
    try {
      const response = await ApiService.post('/api/documents/generate', {
        formType,
        data: formData
      }, { responseType: 'blob' });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${formType}_${new Date().getTime()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download document');
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="lg"
      fullWidth
      PaperProps={{
        sx: {
          height: '90vh',
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column'
        }
      }}
    >
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">
            Document Preview
            {lastUpdate && (
              <Typography variant="caption" sx={{ ml: 2 }}>
                Last updated: {lastUpdate.toLocaleTimeString()}
              </Typography>
            )}
          </Typography>
          {showControls && (
            <Box>
              <Tooltip title="Download">
                <IconButton onClick={handleDownload}>
                  <DownloadIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Refresh Preview">
                <IconButton onClick={() => generatePreview(formData)}>
                  <RefreshIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}>
                <IconButton onClick={toggleFullscreen}>
                  {isFullscreen ? <FullscreenExitIcon /> : <FullscreenIcon />}
                </IconButton>
              </Tooltip>
            </Box>
          )}
        </Box>
      </DialogTitle>

      <DialogContent ref={previewContainerRef} sx={{ p: 0, overflow: 'hidden' }}>
        {error && (
          <Alert severity="error" sx={{ m: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            height="100%"
          >
            <CircularProgress />
          </Box>
        ) : (
          <>
            {showControls && (
              <Paper
                elevation={3}
                sx={{
                  position: 'absolute',
                  bottom: 16,
                  left: '50%',
                  transform: 'translateX(-50%)',
                  zIndex: 1,
                  p: 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  bgcolor: 'rgba(255, 255, 255, 0.9)'
                }}
              >
                <Tooltip title="Zoom Out">
                  <IconButton onClick={handleZoomOut}>
                    <ZoomOutIcon />
                  </IconButton>
                </Tooltip>
                <Slider
                  value={scale}
                  min={0.5}
                  max={3}
                  step={0.1}
                  onChange={handleZoomChange}
                  sx={{ width: 100 }}
                  valueLabelDisplay="auto"
                  valueLabelFormat={value => `${Math.round(value * 100)}%`}
                />
                <Tooltip title="Zoom In">
                  <IconButton onClick={handleZoomIn}>
                    <ZoomInIcon />
                  </IconButton>
                </Tooltip>
                <Divider orientation="vertical" flexItem />
                <Tooltip title="Previous Page">
                  <IconButton
                    onClick={handlePreviousPage}
                    disabled={currentPage <= 1}
                  >
                    <NavigateBeforeIcon />
                  </IconButton>
                </Tooltip>
                <Typography>
                  Page {currentPage} of {numPages || '?'}
                </Typography>
                <Tooltip title="Next Page">
                  <IconButton
                    onClick={handleNextPage}
                    disabled={currentPage >= numPages}
                  >
                    <NavigateNextIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Pan Mode">
                  <IconButton>
                    <PanToolIcon />
                  </IconButton>
                </Tooltip>
              </Paper>
            )}

            <TransformWrapper
              initialScale={1}
              initialPositionX={0}
              initialPositionY={0}
              minScale={0.5}
              maxScale={3}
              wheel={{ step: 0.1 }}
            >
              <TransformComponent>
                <Document
                  file={pdfUrl}
                  onLoadSuccess={onDocumentLoadSuccess}
                  loading={
                    <Box
                      display="flex"
                      justifyContent="center"
                      alignItems="center"
                      height="100%"
                    >
                      <CircularProgress />
                    </Box>
                  }
                >
                  <Page
                    pageNumber={currentPage}
                    scale={scale}
                    renderTextLayer={false}
                    renderAnnotationLayer={false}
                  />
                </Document>
              </TransformComponent>
            </TransformWrapper>
          </>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default DocumentPreview; 
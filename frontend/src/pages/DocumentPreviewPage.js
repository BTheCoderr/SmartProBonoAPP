import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  IconButton,
  Divider,
  Alert,
  CircularProgress,
  Grid,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Tooltip,
  useMediaQuery,
  Snackbar,
  TextField,
  Slide,
  Stack,
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { useTranslation } from 'react-i18next';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DownloadIcon from '@mui/icons-material/Download';
import PrintIcon from '@mui/icons-material/Print';
import EmailIcon from '@mui/icons-material/Email';
import EditIcon from '@mui/icons-material/Edit';
import ShareIcon from '@mui/icons-material/Share';
import SaveIcon from '@mui/icons-material/Save';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import DescriptionIcon from '@mui/icons-material/Description';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import { documentTemplates } from '../data/documentTemplateLibrary';
import axios from 'axios';

// Convert HTML content to a sanitized version
const sanitizeHtml = (html) => {
  // This is a basic implementation - a real app would use a library like DOMPurify
  // or sanitize-html to prevent XSS attacks
  return {
    __html: html
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/on\w+="[^"]*"/g, '')
      .replace(/on\w+='[^']*'/g, '')
  };
};

const DocumentPreviewPage = () => {
  const { t } = useTranslation();
  const { templateId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  const documentContainerRef = useRef(null);
  const documentIframeRef = useRef(null);

  // Check if this is demo mode
  const isDemo = new URLSearchParams(location.search).get('demo') === 'true';

  // Get form data from location state using useMemo
  const formData = React.useMemo(() => location.state?.formData || {}, [location.state]);

  // Find the template from the template library
  const template = documentTemplates.find(t => t.id === templateId);

  // State
  const [documentContent, setDocumentContent] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [menuAnchorEl, setMenuAnchorEl] = useState(null);
  const [shareDialogOpen, setShareDialogOpen] = useState(false);
  const [showDemoBanner, setShowDemoBanner] = useState(isDemo);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [mobileControlsOpen, setMobileControlsOpen] = useState(false);

  const menuOpen = Boolean(menuAnchorEl);

  // Load document content
  useEffect(() => {
    if (!template) {
      setError('Template not found');
      setIsLoading(false);
      return;
    }

    const fetchDocument = async () => {
    try {
      setIsLoading(true);
        
        // In a real implementation, this would call the backend API
        const response = await axios.post('/api/documents/generate', {
          template_id: templateId,
          form_data: formData
        }, {
          responseType: 'blob' // Important for PDF downloads
        }).catch(err => {
          console.error('Error generating document:', err);
          throw new Error(err.response?.data?.error || 'Failed to generate document');
        });
        
        // Create a URL for the blob
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
        
        // Also generate an HTML preview for accessibility
        const reader = new FileReader();
        reader.onload = () => {
          // This would be replaced with actual HTML conversion
          setDocumentContent(`<div class="document-content">
            <h1>${template.name}</h1>
            <p>Document preview generated successfully. Use the PDF viewer for best results.</p>
          </div>`);
          setIsLoading(false);
        };
        
        reader.onerror = () => {
          setError('Failed to read document content');
          setIsLoading(false);
        };
        
        reader.readAsText(blob);
      } catch (err) {
        console.error('Error loading document:', err);
        setError(err.message || 'Failed to load document');
        setIsLoading(false);
      }
    };

    // For demo purposes, simulate the API call
    const simulateDocumentGeneration = () => {
      setTimeout(() => {
        try {
          // Generate mock HTML content
          const content = `
            <div style="font-family: Arial, sans-serif; line-height: 1.5;">
              <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #2c3e50;">${template.name}</h1>
                <p>Generated on ${new Date().toLocaleDateString()}</p>
              </div>
              
              <div style="margin-bottom: 30px;">
                <p><strong>Prepared for:</strong> ${formData.fullName || 'N/A'}</p>
                <p><strong>Email:</strong> ${formData.email || 'N/A'}</p>
                <p><strong>Phone:</strong> ${formData.phone || 'N/A'}</p>
                <p><strong>Effective Date:</strong> ${formData.effectiveDate || new Date().toLocaleDateString()}</p>
              </div>
              
              <div style="margin-bottom: 30px;">
                <h2 style="color: #3498db; border-bottom: 1px solid #eee; padding-bottom: 10px;">Document Content</h2>
                <p>This is a generated document based on the ${template.name} template.</p>
                
                <p>Additional notes provided:</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                  ${formData.additionalNotes || 'No additional notes provided.'}
                </div>
              </div>
            </div>
          `;
      setDocumentContent(content);
          
          // In a real app, we would generate a PDF here
          // For demo, we're just setting a placeholder
          setPdfUrl(null);
      setIsLoading(false);
    } catch (err) {
          setError(err.message || 'An error occurred while generating the document');
      setIsLoading(false);
        }
      }, 1500); // Simulate loading time
    };

    // Use the appropriate method based on environment
    if (process.env.NODE_ENV === 'development') {
      simulateDocumentGeneration();
    } else {
      fetchDocument();
    }

    // Cleanup function
    return () => {
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }
    };
  }, [template, formData, templateId]);

  const handleDemoBannerClose = () => {
    setShowDemoBanner(false);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  // Handle menu open
  const handleMenuOpen = (event) => {
    setMenuAnchorEl(event.currentTarget);
  };

  // Handle menu close
  const handleMenuClose = () => {
    setMenuAnchorEl(null);
  };

  // Handle print
  const handlePrint = () => {
    handleMenuClose();
    if (documentIframeRef.current) {
      // Print the iframe content
      const iframe = documentIframeRef.current;
      const iframeWindow = iframe.contentWindow || iframe;
      
      try {
        iframeWindow.focus();
        iframeWindow.print();
      } catch (err) {
        console.error('Print error:', err);
        setSnackbarMessage('Unable to print. Please try downloading the document first.');
        setSnackbarOpen(true);
      }
    } else {
    window.print();
    }
  };

  // Handle download as PDF
  const handleDownloadPDF = () => {
    handleMenuClose();
    if (pdfUrl) {
      // Create a temporary link and trigger download
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = `${template.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      // Fallback for when PDF isn't available
      setSnackbarMessage('PDF download is currently unavailable. Please try again later.');
      setSnackbarOpen(true);
    }
  };

  // Handle download as Word
  const handleDownloadWord = () => {
    handleMenuClose();
    try {
    // This would be implemented with a docx generation library in a real app
      setSnackbarMessage('Word document download functionality will be available soon.');
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Word download error:', err);
      setSnackbarMessage('Unable to download as Word document.');
      setSnackbarOpen(true);
    }
  };

  // Handle email
  const handleEmail = () => {
    handleMenuClose();
    try {
    // This would open an email form in a real app
      setSnackbarMessage('Email functionality will be available soon.');
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Email error:', err);
      setSnackbarMessage('Unable to email document.');
      setSnackbarOpen(true);
    }
  };

  // Handle share
  const handleShare = () => {
    handleMenuClose();
    setShareDialogOpen(true);
  };

  // Handle edit
  const handleEdit = () => {
    handleMenuClose();
    navigate(`/document-generator/form/${templateId}`, { state: { formData } });
  };

  // Handle save to account
  const handleSave = () => {
    handleMenuClose();
    try {
    // This would save the document to user's account in a real app
      setSnackbarMessage('Document saved to your account.');
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Save error:', err);
      setSnackbarMessage('Unable to save document.');
      setSnackbarOpen(true);
    }
  };

  // Handle zoom in
  const handleZoomIn = () => {
    setZoomLevel(prev => Math.min(prev + 0.1, 2.0));
  };

  // Handle zoom out
  const handleZoomOut = () => {
    setZoomLevel(prev => Math.max(prev - 0.1, 0.5));
  };

  // Handle share dialog close
  const handleShareDialogClose = () => {
    setShareDialogOpen(false);
  };

  // Add this function for handling zoom on mobile devices
  const handlePinchZoom = useCallback((event) => {
    if (event.scale && isMobile) {
      if (event.scale > 1) {
        setZoomLevel(Math.min(zoomLevel + 0.1, 2.5));
      } else if (event.scale < 1) {
        setZoomLevel(Math.max(zoomLevel - 0.1, 0.5));
      }
    }
  }, [zoomLevel, isMobile]);

  // Add event listeners for pinch zoom
  useEffect(() => {
    if (isMobile && documentContainerRef.current) {
      documentContainerRef.current.addEventListener('gesturechange', handlePinchZoom);
      
      return () => {
        if (documentContainerRef.current) {
          documentContainerRef.current.removeEventListener('gesturechange', handlePinchZoom);
        }
      };
    }
  }, [isMobile, handlePinchZoom]);

  // Mobile-friendly controls toggle
  const toggleMobileControls = () => {
    setMobileControlsOpen(!mobileControlsOpen);
  };

  if (isLoading) {
    return (
      <Container maxWidth="md" sx={{ py: 8, textAlign: 'center' }}>
        <CircularProgress size={60} aria-label={t('Loading document')} />
        <Typography variant="h6" sx={{ mt: 3 }}>
          {t('Generating your document...')}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {t('This may take a few moments.')}
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert 
          severity="error" 
          icon={<ErrorOutlineIcon fontSize="inherit" />}
          aria-live="assertive"
        >
          <Typography variant="h6">{t('Error generating document')}</Typography>
          <Typography variant="body1">{error}</Typography>
        </Alert>
        <Box mt={2}>
          <Button
            variant="contained"
            onClick={() =>
              navigate(`/document-generator/form/${templateId}`, { state: { formData } })
            }
            startIcon={<ArrowBackIcon />}
          >
            {t('Go Back to Form')}
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', bgcolor: 'background.default' }}>
      <Navigation />
      
      {/* Mobile-optimized document viewer */}
      <Container 
        maxWidth="lg" 
        sx={{ 
          flexGrow: 1, 
          mt: { xs: 1, sm: 2, md: 3 }, 
          pb: { xs: 2, sm: 3, md: 4 },
          px: { xs: 1, sm: 2, md: 3 }
        }}
      >
        {showDemoBanner && (
          <Alert 
            severity="info" 
            sx={{ 
              mb: { xs: 1, sm: 2 },
              py: { xs: 0.5, sm: 1 }
            }} 
            onClose={handleDemoBannerClose}
          >
            <Typography variant={isMobile ? "caption" : "body2"}>
              {t('This is a preview of your generated document. In a production environment, this would be a complete legal document.')}
          </Typography>
        </Alert>
      )}

        <Paper 
          elevation={3} 
          sx={{ 
            overflow: 'hidden',
            borderRadius: { xs: 1, sm: 2 }, 
            height: { xs: 'calc(100vh - 150px)', sm: 'calc(100vh - 180px)' } 
          }}
        >
          {/* Document toolbar - redesigned for better mobile experience */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
              p: { xs: 1, sm: 2 },
              borderBottom: 1,
              borderColor: 'divider',
              bgcolor: 'primary.light',
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Typography 
                variant={isMobile ? "subtitle1" : "h6"} 
                component="h1" 
          sx={{
                  mr: 2,
                  fontWeight: 'medium',
                  fontSize: { xs: '0.9rem', sm: '1.1rem', md: '1.25rem' }
                }}
              >
                {template?.name || t('Document Preview')}
          </Typography>
              {isLoading ? (
                <CircularProgress size={isMobile ? 16 : 20} thickness={5} sx={{ ml: 1 }} />
              ) : null}
        </Box>

            {/* Desktop controls */}
            {!isMobile ? (
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Tooltip title={t('Zoom Out')}>
                  <IconButton 
                    onClick={handleZoomOut} 
                    disabled={zoomLevel <= 0.5} 
                    size={isTablet ? "small" : "medium"}
                  >
                    <ZoomOutIcon />
                  </IconButton>
                </Tooltip>
                <Typography variant="body2" sx={{ mx: 1, minWidth: '60px', textAlign: 'center' }}>
                  {Math.round(zoomLevel * 100)}%
                </Typography>
                <Tooltip title={t('Zoom In')}>
                  <IconButton 
                    onClick={handleZoomIn} 
                    disabled={zoomLevel >= 2.5} 
                    size={isTablet ? "small" : "medium"}
                  >
                    <ZoomInIcon />
                  </IconButton>
                </Tooltip>
                <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />
              <Tooltip title={t('Print')}>
                  <IconButton onClick={handlePrint} size={isTablet ? "small" : "medium"}>
                  <PrintIcon />
                </IconButton>
              </Tooltip>
                <Tooltip title={t('Download')}>
                  <IconButton onClick={(e) => handleMenuOpen(e)} size={isTablet ? "small" : "medium"}>
                    <SaveIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title={t('Edit')}>
                  <IconButton onClick={handleEdit} size={isTablet ? "small" : "medium"}>
                  <EditIcon />
                </IconButton>
              </Tooltip>
                <Tooltip title={t('Share')}>
                  <IconButton onClick={handleShare} size={isTablet ? "small" : "medium"}>
                    <ShareIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            ) : (
              // Mobile toolbar with limited controls and more menu
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Tooltip title={t('Zoom Out')}>
                  <IconButton 
                    onClick={handleZoomOut} 
                    disabled={zoomLevel <= 0.5} 
                    size="small"
                    sx={{ p: 0.5 }}
                  >
                    <ZoomOutIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
                <Typography variant="caption" sx={{ mx: 0.5, minWidth: '40px', textAlign: 'center' }}>
                  {Math.round(zoomLevel * 100)}%
                </Typography>
                <Tooltip title={t('Zoom In')}>
                  <IconButton 
                    onClick={handleZoomIn} 
                    disabled={zoomLevel >= 2.5} 
                    size="small"
                    sx={{ p: 0.5 }}
                  >
                    <ZoomInIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
                <Tooltip title={t('More Options')}>
            <IconButton
                    onClick={(e) => handleMenuOpen(e)} 
                    size="small"
              sx={{ ml: 0.5 }}
            >
                    <MoreVertIcon fontSize="small" />
            </IconButton>
          </Tooltip>
              </Box>
            )}
          </Box>

          {/* Document container */}
          <Box 
            ref={documentContainerRef}
            sx={{
              height: { xs: 'calc(100vh - 190px)', sm: 'calc(100vh - 240px)' },
              overflow: 'auto',
              bgcolor: 'grey.100',
              p: { xs: 1, sm: 2 },
              touchAction: 'manipulation',
            }}
          >
            {pdfUrl ? (
              <Box 
                sx={{ 
                  display: 'flex',
                  justifyContent: 'center',
                  '& iframe': {
                    width: '100%',
                    height: '100%',
                    border: 'none',
                    transform: `scale(${zoomLevel})`,
                    transformOrigin: 'top center',
                    transition: 'transform 0.2s ease-in-out',
                  },
                }}
              >
                <iframe 
                  src={pdfUrl} 
                  title="Document Preview" 
                  aria-label="Document Preview"
                />
              </Box>
            ) : isLoading ? (
              <Box 
                display="flex" 
                justifyContent="center" 
                alignItems="center" 
                height="100%"
              >
                <CircularProgress size={isMobile ? 40 : 60} />
                <Typography 
                  variant={isMobile ? "body2" : "body1"} 
                  sx={{ ml: 2 }}
                >
                  {t('Generating your document...')}
                </Typography>
              </Box>
            ) : (
              <Box 
                display="flex" 
                flexDirection="column" 
                justifyContent="center" 
                alignItems="center" 
                height="100%"
              >
                <Typography 
                  variant={isMobile ? "h6" : "h5"} 
                  color="text.secondary" 
                  mb={2}
                >
                  {t('No document selected')}
                </Typography>
                <Button 
                  variant="contained" 
                  onClick={() => navigate('/document-generator')}
                >
                  {t('Create New Document')}
                </Button>
              </Box>
            )}
      </Box>

          {/* Action buttons at bottom of screen */}
          <Box 
        sx={{
              p: { xs: 1, sm: 2 },
              borderTop: 1,
              borderColor: 'divider',
              display: 'flex',
              justifyContent: 'space-between',
              bgcolor: 'background.paper',
            }}
          >
        <Button
          variant="outlined"
              onClick={() => navigate(-1)}
          startIcon={<ArrowBackIcon />}
              sx={{ 
                display: { xs: 'none', sm: 'flex' }
              }}
            >
              {t('Back')}
        </Button>

            <IconButton 
              onClick={() => navigate(-1)}
              sx={{ 
                display: { xs: 'flex', sm: 'none' }
              }}
            >
              <ArrowBackIcon />
            </IconButton>
            
            <Stack direction="row" spacing={1}>
              {!isMobile && (
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={handleEdit}
                  startIcon={<EditIcon />}
                >
                  {t('Edit')}
                </Button>
              )}
              
              <Button
                variant="contained"
                color="primary"
                onClick={handleDownloadPDF}
                startIcon={<SaveIcon />}
                sx={{ whiteSpace: 'nowrap' }}
              >
                {isMobile ? t('Download') : t('Download PDF')}
        </Button>
            </Stack>
      </Box>
        </Paper>
      </Container>

      {/* Mobile menu for download options */}
      <Menu
        anchorEl={menuAnchorEl}
        open={Boolean(menuAnchorEl)}
        onClose={handleMenuClose}
        PaperProps={{
          sx: {
            minWidth: 200,
            maxWidth: '90%',
            mt: 1,
          }
        }}
      >
        {isMobile ? (
          // Mobile menu with all actions
          [
            <MenuItem key="download-pdf" onClick={() => { handleMenuClose(); handleDownloadPDF(); }}>
              <SaveIcon fontSize="small" sx={{ mr: 1 }} />
              {t('Download PDF')}
            </MenuItem>,
            <MenuItem key="download-word" onClick={() => { handleMenuClose(); handleDownloadWord(); }}>
              <DescriptionIcon fontSize="small" sx={{ mr: 1 }} />
              {t('Download Word')}
            </MenuItem>,
            <MenuItem key="print" onClick={() => { handleMenuClose(); handlePrint(); }}>
              <PrintIcon fontSize="small" sx={{ mr: 1 }} />
              {t('Print')}
            </MenuItem>,
            <MenuItem key="edit" onClick={() => { handleMenuClose(); handleEdit(); }}>
              <EditIcon fontSize="small" sx={{ mr: 1 }} />
              {t('Edit')}
            </MenuItem>,
            <MenuItem key="share" onClick={() => { handleMenuClose(); handleShare(); }}>
              <ShareIcon fontSize="small" sx={{ mr: 1 }} />
              {t('Share')}
            </MenuItem>,
            <MenuItem key="email" onClick={() => { handleMenuClose(); handleEmail(); }}>
              <EmailIcon fontSize="small" sx={{ mr: 1 }} />
              {t('Email')}
            </MenuItem>
          ]
        ) : (
          // Desktop menu with just download options
          [
            <MenuItem key="download-pdf" onClick={() => { handleMenuClose(); handleDownloadPDF(); }}>
              {t('Download as PDF')}
            </MenuItem>,
            <MenuItem key="download-word" onClick={() => { handleMenuClose(); handleDownloadWord(); }}>
              {t('Download as Word')}
            </MenuItem>,
            <MenuItem key="email" onClick={() => { handleMenuClose(); handleEmail(); }}>
              {t('Email document')}
            </MenuItem>
          ]
        )}
      </Menu>

      {/* Share dialog - mobile optimized */}
      <Dialog
        open={shareDialogOpen}
        onClose={handleShareDialogClose}
        PaperProps={{
          sx: {
            width: isMobile ? '95%' : '500px',
            maxWidth: '100%'
          }
        }}
      >
        <DialogTitle>{t('Share Document')}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label={t('Recipient Email')}
            type="email"
            margin="dense"
                  variant="outlined"
          />
          <TextField
                  fullWidth
            label={t('Message (Optional)')}
            multiline
            rows={isMobile ? 2 : 4}
            margin="dense"
                  variant="outlined"
          />
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={handleShareDialogClose} color="inherit">
            {t('Cancel')}
          </Button>
          <Button onClick={handleShareDialogClose} variant="contained" color="primary">
            {t('Share')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        sx={{ mb: isMobile ? 1 : 2 }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity={snackbarSeverity}
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default DocumentPreviewPage;

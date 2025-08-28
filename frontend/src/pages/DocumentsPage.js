import React, { useState } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Grid,
  Paper, 
  Chip,
  useTheme,
  Divider,
  Alert,
  Button
} from '@mui/material';
import { 
  Description as DocumentIcon,
  Upload as UploadIcon,
  Chat as ChatIcon,
  CheckCircle as SuccessIcon,
  Schedule as ProcessingIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import DocumentUpload from '../components/DocumentUpload';
import DocumentChat from '../components/DocumentChat';

const DocumentsPage = () => {
  const [currentDocument, setCurrentDocument] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState(null);
  const theme = useTheme();

  const handleDocumentUploaded = (documentId) => {
    // Add the new document to the list
    const newDoc = {
      id: documentId,
      title: 'New Document',
      status: 'processed',
      createdAt: new Date(),
    };
    
      setDocuments(prev => [newDoc, ...prev]);
    setCurrentDocument(newDoc);
    setError(null);
  };

  const handleUploadError = (errorMessage) => {
    setError(errorMessage);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'uploaded': return <UploadIcon />;
      case 'processing': return <ProcessingIcon />;
      case 'processed': return <SuccessIcon />;
      case 'error': return <ErrorIcon />;
      default: return <DocumentIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'uploaded': return 'warning';
      case 'processing': return 'info';
      case 'processed': return 'success';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'uploaded': return 'Uploaded';
      case 'processing': return 'Processing';
      case 'processed': return 'Ready';
      case 'error': return 'Error';
      default: return 'Unknown';
    }
  };

          return (
                <Box 
                  sx={{ 
        minHeight: '100vh',
        backgroundColor: '#fafafa',
        pt: { xs: 8, md: 10 },
        pb: { xs: 6, md: 8 },
      }}
    >
      <Container maxWidth="xl">
        {/* Page Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Box sx={{ textAlign: 'center', mb: { xs: 6, md: 8 } }}>
            <Typography
              variant="h2"
              sx={{
                color: theme.palette.text.primary,
                fontWeight: 800,
                mb: 2,
                background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Document AI Assistant
            </Typography>
            <Typography
              variant="h5"
              sx={{
                color: theme.palette.text.secondary,
                maxWidth: 600,
                mx: 'auto',
                lineHeight: 1.6,
              }}
            >
              Upload legal documents and get instant AI-powered answers to your questions. 
              Perfect for understanding contracts, forms, and legal paperwork.
            </Typography>
          </Box>
        </motion.div>

        {/* Error Alert */}
        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
          >
            <Alert
              severity="error"
              sx={{ mb: 4, borderRadius: 2 }}
              action={
                <Button color="inherit" size="small" onClick={() => setError(null)}>
                  Dismiss
                </Button>
              }
            >
              {error}
            </Alert>
          </motion.div>
        )}

        <Grid container spacing={4}>
          {/* Left Column - Upload & Document List */}
          <Grid item xs={12} lg={5}>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              {/* Upload Section */}
              <Box sx={{ mb: 4 }}>
                <DocumentUpload
                  onUploaded={handleDocumentUploaded}
                  onError={handleUploadError}
                />
              </Box>

              {/* Documents List */}
              <Paper
                elevation={3}
                sx={{
                  borderRadius: 3,
                  overflow: 'hidden',
                  background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
                }}
              >
                <Box
                  sx={{
                    p: 3,
                    background: `linear-gradient(135deg, ${theme.palette.secondary.main} 0%, ${theme.palette.secondary.dark} 100%)`,
                    color: 'white',
                  }}
                >
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Your Documents
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    {documents.length} document{documents.length !== 1 ? 's' : ''} uploaded
                  </Typography>
                </Box>

                <Box sx={{ p: 2 }}>
                  {documents.length === 0 ? (
                    <Box
                      sx={{
                        textAlign: 'center',
                        py: 6,
                        color: theme.palette.text.secondary,
                      }}
                    >
                      <DocumentIcon sx={{ fontSize: 48, mb: 2, opacity: 0.5 }} />
                      <Typography variant="h6" gutterBottom>
                        No Documents Yet
                      </Typography>
                      <Typography variant="body2">
                        Upload your first document to get started with AI analysis
                      </Typography>
                    </Box>
                  ) : (
                    <Box sx={{ space: 2 }}>
                      {documents.map((doc, index) => (
                        <motion.div
                          key={doc.id}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.3, delay: index * 0.1 }}
                        >
                          <Paper
                            variant="outlined"
                            sx={{
                              p: 2,
                              mb: 2,
                              cursor: 'pointer',
                              border: currentDocument?.id === doc.id 
                                ? `2px solid ${theme.palette.primary.main}` 
                                : '1px solid',
                              backgroundColor: currentDocument?.id === doc.id 
                                ? 'rgba(59, 130, 246, 0.05)' 
                                : 'transparent',
                              transition: 'all 0.3s ease',
                              '&:hover': {
                                borderColor: theme.palette.primary.main,
                                backgroundColor: 'rgba(59, 130, 246, 0.05)',
                                transform: 'translateY(-1px)',
                                boxShadow: theme.shadows[4],
                              },
                            }}
                            onClick={() => setCurrentDocument(doc)}
                          >
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              <Box
                                sx={{
                                  p: 1,
                                  borderRadius: 1,
                                  backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                  color: theme.palette.primary.main,
                                }}
                              >
                                <DocumentIcon />
                              </Box>
                              
                              <Box sx={{ flex: 1 }}>
                                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                  {doc.title}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  {doc.createdAt.toLocaleDateString()}
                                </Typography>
                              </Box>

                              <Chip
                                icon={getStatusIcon(doc.status)}
                                label={getStatusText(doc.status)}
                                color={getStatusColor(doc.status)}
                                size="small"
                                variant="outlined"
                              />
                            </Box>
                          </Paper>
                        </motion.div>
                      ))}
                    </Box>
                  )}
              </Box>
              </Paper>
            </motion.div>
          </Grid>

          {/* Right Column - Chat Interface */}
          <Grid item xs={12} lg={7}>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              {currentDocument ? (
                <DocumentChat
                  documentId={currentDocument.id}
                  documentTitle={currentDocument.title}
                />
              ) : (
                <Paper
                  elevation={3}
                  sx={{
                    borderRadius: 3,
                    p: 6,
                    textAlign: 'center',
                    background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
                    height: 'fit-content',
                  }}
                >
                  <ChatIcon sx={{ fontSize: 64, mb: 3, opacity: 0.5, color: theme.palette.primary.main }} />
                  <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                    Select a Document
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                    Choose a document from the list to start chatting with our AI assistant
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Upload a document first if you don't have any yet
                  </Typography>
                </Paper>
              )}
            </motion.div>
          </Grid>
        </Grid>

        {/* Features Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <Box sx={{ mt: { xs: 8, md: 12 } }}>
            <Divider sx={{ mb: 6 }} />
            
            <Typography
              variant="h4"
              sx={{
                textAlign: 'center',
                mb: 6,
                color: theme.palette.text.primary,
                fontWeight: 700,
              }}
            >
              How It Works
            </Typography>

            <Grid container spacing={4}>
              {[
                {
                  icon: <UploadIcon sx={{ fontSize: 40 }} />,
                  title: 'Upload Documents',
                  description: 'Upload PDFs, Word documents, or text files. Our system supports multiple formats and languages.',
                },
                {
                  icon: <ProcessingIcon sx={{ fontSize: 40 }} />,
                  title: 'AI Processing',
                  description: 'Advanced OCR and AI extract text, create searchable chunks, and generate semantic embeddings.',
                },
                {
                  icon: <ChatIcon sx={{ fontSize: 40 }} />,
                  title: 'Ask Questions',
                  description: 'Get instant, accurate answers about your documents. Our AI understands context and provides sources.',
                },
              ].map((feature, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <motion.div
                    whileHover={{ y: -8 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Paper
                      elevation={2}
                      sx={{
                        p: 4,
                        textAlign: 'center',
                        borderRadius: 3,
                        height: '100%',
                        background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
                        border: '1px solid rgba(0,0,0,0.05)',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          boxShadow: theme.shadows[8],
                          borderColor: theme.palette.primary.light,
                        },
                      }}
                    >
                      <Box
                        sx={{
                          display: 'inline-flex',
                          p: 2,
                          borderRadius: 2,
                          backgroundColor: 'rgba(59, 130, 246, 0.1)',
                          color: theme.palette.primary.main,
                          mb: 3,
                        }}
                      >
                        {feature.icon}
          </Box>
          
                      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                        {feature.title}
                      </Typography>
          
                      <Typography variant="body2" color="text.secondary">
                        {feature.description}
                      </Typography>
        </Paper>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
};

export default DocumentsPage; 
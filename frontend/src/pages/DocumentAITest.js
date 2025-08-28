import React, { useState, useEffect } from 'react';
import {
  Box, Container, Typography, Paper, Button, Alert, CircularProgress, 
  useTheme, Grid, Chip, Card, CardContent, Divider
} from '@mui/material';
import { motion } from 'framer-motion';
import DocumentUpload from '../components/DocumentUpload';
import DocumentChat from '../components/DocumentChat';

const DocumentAITest = () => {
  const [currentDocument, setCurrentDocument] = useState(null);
  const [workerHealth, setWorkerHealth] = useState(null);
  const [isCheckingHealth, setIsCheckingHealth] = useState(false);
  const [testResults, setTestResults] = useState({});
  const theme = useTheme();

  useEffect(() => {
    checkWorkerHealth();
  }, []);

  const checkWorkerHealth = async () => {
    setIsCheckingHealth(true);
    try {
      const response = await fetch('http://localhost:8001/health');
      const data = await response.json();
      setWorkerHealth(data);
      
      // Test other endpoints
      await testEndpoints();
    } catch (error) {
      setWorkerHealth({ status: 'error', message: error.message });
    } finally {
      setIsCheckingHealth(false);
    }
  };

  const testEndpoints = async () => {
    const results = {};
    
    // Test upload endpoint
    try {
      const uploadResponse = await fetch('http://localhost:8001/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          document_id: 'test123',
          user_id: 'test-user',
          title: 'test.pdf',
          storage_path: '/tmp/test.pdf'
        })
      });
      results.upload = uploadResponse.ok ? '✅ Working' : '❌ Failed';
    } catch (error) {
      results.upload = '❌ Error: ' + error.message;
    }

    // Test process endpoint
    try {
      const processResponse = await fetch('http://localhost:8001/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: 'test123' })
      });
      results.process = processResponse.ok ? '✅ Working' : '❌ Failed';
    } catch (error) {
      results.process = '❌ Error: ' + error.message;
    }

    // Test ask endpoint
    try {
      const askResponse = await fetch('http://localhost:8001/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          document_id: 'test123', 
          question: 'What is this document about?' 
        })
      });
      results.ask = askResponse.ok ? '✅ Working' : '❌ Failed';
    } catch (error) {
      results.ask = '❌ Error: ' + error.message;
    }

    setTestResults(results);
  };

  const handleDocumentUploaded = (documentId) => {
    setCurrentDocument(documentId);
  };

  const handleUploadError = (errorMessage) => {
    console.error('Upload error:', errorMessage);
  };

  const getHealthColor = () => {
    if (!workerHealth) return 'default';
    return workerHealth.status === 'healthy' ? 'success' : 'error';
  };

  const getHealthText = () => {
    if (!workerHealth) return 'Unknown';
    return workerHealth.status === 'healthy' ? 'Healthy' : 'Error';
  };

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      backgroundColor: '#fafafa',
      pt: { xs: 8, md: 10 }
    }}>
      <Container maxWidth="xl">
        {/* Page Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography 
              variant="h2" 
              sx={{ 
                color: '#1e293b',
                fontWeight: 800,
                mb: 2
              }}
            >
              Document AI System Test
            </Typography>
            <Typography 
              variant="h5" 
              sx={{ 
                color: '#475569',
                maxWidth: '600px',
                mx: 'auto'
              }}
            >
              Test the integration between your React frontend and the Python Document AI worker
            </Typography>
          </Box>
        </motion.div>

        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Card sx={{ mb: 4, boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#1e293b', mb: 2 }}>
                System Status
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Chip 
                      label={getHealthText()} 
                      color={getHealthColor()}
                      variant="outlined"
                    />
                    <Typography variant="body2" sx={{ color: '#64748b' }}>
                      Python Worker (Port 8001)
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Button 
                    variant="outlined" 
                    onClick={checkWorkerHealth}
                    disabled={isCheckingHealth}
                    startIcon={isCheckingHealth ? <CircularProgress size={16} /> : null}
                  >
                    {isCheckingHealth ? 'Checking...' : 'Check Health'}
                  </Button>
                </Grid>
              </Grid>
              
              {workerHealth && (
                <Box sx={{ mt: 2, p: 2, bgcolor: '#f8fafc', borderRadius: 2 }}>
                  <Typography variant="body2" sx={{ color: '#64748b' }}>
                    <strong>Response:</strong> {JSON.stringify(workerHealth, null, 2)}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Endpoint Tests */}
        {Object.keys(testResults).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Card sx={{ mb: 4, boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
              <CardContent>
                <Typography variant="h6" sx={{ color: '#1e293b', mb: 2 }}>
                  Endpoint Test Results
                </Typography>
                <Grid container spacing={2}>
                  {Object.entries(testResults).map(([endpoint, result]) => (
                    <Grid item xs={12} sm={4} key={endpoint}>
                      <Box sx={{ 
                        p: 2, 
                        bgcolor: '#f8fafc', 
                        borderRadius: 2,
                        border: '1px solid #e2e8f0'
                      }}>
                        <Typography variant="subtitle2" sx={{ color: '#1e293b', mb: 1 }}>
                          {endpoint.charAt(0).toUpperCase() + endpoint.slice(1)}
                        </Typography>
                        <Typography variant="body2" sx={{ 
                          color: result.includes('✅') ? '#059669' : '#dc2626',
                          fontWeight: 500
                        }}>
                          {result}
                        </Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Test Instructions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <Card sx={{ mb: 4, boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#1e293b', mb: 2 }}>
                How to Test
              </Typography>
              <Box component="ol" sx={{ color: '#475569', pl: 2 }}>
                <li>Upload a PDF document using the upload component below</li>
                <li>Wait for the document to be processed</li>
                <li>Ask questions about the document using the chat interface</li>
                <li>Verify that all responses come from your local AI worker</li>
              </Box>
            </CardContent>
          </Card>
        </motion.div>

        {/* Test Components */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <Grid container spacing={4}>
            {/* Left Column - Upload and Document List */}
            <Grid item xs={12} lg={6}>
              <Card sx={{ boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
                <CardContent>
                  <Typography variant="h6" sx={{ color: '#1e293b', mb: 3 }}>
                    Document Upload & Management
                  </Typography>
                  <DocumentUpload 
                    onUploaded={handleDocumentUploaded}
                    onError={handleUploadError}
                  />
                  
                  {currentDocument && (
                    <Box sx={{ mt: 3, p: 2, bgcolor: '#f0f9ff', borderRadius: 2 }}>
                      <Typography variant="body2" sx={{ color: '#0369a1' }}>
                        <strong>Current Document:</strong> {currentDocument}
                      </Typography>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Right Column - Chat Interface */}
            <Grid item xs={12} lg={6}>
              <Card sx={{ boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
                <CardContent>
                  <Typography variant="h6" sx={{ color: '#1e293b', mb: 3 }}>
                    AI Chat Interface
                  </Typography>
                  {currentDocument ? (
                    <DocumentChat documentId={currentDocument} />
                  ) : (
                    <Box sx={{ 
                      p: 4, 
                      textAlign: 'center', 
                      bgcolor: '#f8fafc',
                      borderRadius: 2
                    }}>
                      <Typography variant="body2" sx={{ color: '#64748b' }}>
                        Upload a document first to start chatting with the AI
                      </Typography>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </motion.div>

        {/* Troubleshooting */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
        >
          <Card sx={{ mt: 4, boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#1e293b', mb: 2 }}>
                Troubleshooting
              </Typography>
              <Box component="ul" sx={{ color: '#475569', pl: 2 }}>
                <li>Make sure the Python worker is running on port 8001</li>
                <li>Check that your React app can reach localhost:8001</li>
                <li>Verify that the worker endpoints are responding correctly</li>
                <li>Check the browser console for any JavaScript errors</li>
              </Box>
            </CardContent>
          </Card>
        </motion.div>
      </Container>
    </Box>
  );
};

export default DocumentAITest;

import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Tabs, Tab, Button, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import MobileFileScanner from '../components/MobileFileScanner';
import { documentsApi } from '../services/api';
import { useAuth } from '../context/AuthContext';

const ScanDocument = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [scanResults, setScanResults] = useState(null);
  const [documentCategories, setDocumentCategories] = useState([
    { id: 'identification', label: 'ID Documents' },
    { id: 'immigration', label: 'Immigration' },
    { id: 'legal', label: 'Legal Forms' }
  ]);
  const navigate = useNavigate();
  const { currentUser } = useAuth();

  useEffect(() => {
    // Fetch available document categories if needed
    const fetchCategories = async () => {
      try {
        const response = await documentsApi.getDocumentCategories();
        if (response && response.categories) {
          setDocumentCategories(response.categories);
        }
      } catch (error) {
        console.error('Error fetching document categories:', error);
      }
    };

    // Uncomment when API endpoint is ready
    // fetchCategories();
  }, []);

  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  const handleScanComplete = (result) => {
    setScanResults(result);
  };

  const handleSaveDocument = async () => {
    if (!scanResults) return;
    
    try {
      const documentData = {
        title: `Scanned ${documentCategories[selectedTab].label} Document`,
        description: 'Document scanned via mobile scanner',
        category: documentCategories[selectedTab].id,
        file_url: scanResults.fileUrl,
        tags: ['scanned', documentCategories[selectedTab].id],
        user_id: currentUser?.id,
        metadata: {
          extracted_data: scanResults.extractedData
        }
      };
      
      const savedDoc = await documentsApi.saveDocument(documentData);
      
      // Navigate to the document viewer with the saved document ID
      if (savedDoc && savedDoc.id) {
        navigate(`/documents/${savedDoc.id}`);
      }
    } catch (error) {
      console.error('Error saving document:', error);
    }
  };

  const getCurrentDocumentType = () => {
    return documentCategories[selectedTab]?.id || 'general';
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 'bold' }}>
        Scan & Process Documents
      </Typography>
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs 
          value={selectedTab} 
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="document category tabs"
        >
          {documentCategories.map((category) => (
            <Tab key={category.id} label={category.label} />
          ))}
        </Tabs>
      </Box>
      
      <MobileFileScanner 
        onScanComplete={handleScanComplete}
        documentType={getCurrentDocumentType()}
      />
      
      {scanResults && (
        <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Document Processing Complete
          </Typography>
          
          <Typography variant="body2" sx={{ mb: 3 }}>
            Your document has been successfully scanned and processed. You can now save it to your documents.
          </Typography>
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <Button 
              variant="outlined" 
              onClick={() => setScanResults(null)}
            >
              Scan New Document
            </Button>
            
            <Button 
              variant="contained" 
              onClick={handleSaveDocument}
            >
              Save Document
            </Button>
          </Box>
        </Paper>
      )}
      
      <Box sx={{ mt: 4 }}>
        <Typography variant="subtitle2" color="text.secondary">
          Need help? Our AI can assist with document classification and processing.
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Take clear, well-lit photos for best results. Your documents are processed securely.
        </Typography>
      </Box>
    </Container>
  );
};

export default ScanDocument; 
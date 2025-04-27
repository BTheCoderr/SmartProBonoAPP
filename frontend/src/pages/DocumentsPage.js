import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Paper, 
  Divider, 
  Tab, 
  Tabs, 
  TextField, 
  InputAdornment,
  Button,
  Grid, 
  Card, 
  CardContent, 
  CardActions,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Fab,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { 
  Search as SearchIcon, 
  Add as AddIcon,
  Description as DescriptionIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Share as ShareIcon,
  FileDownload as FileDownloadIcon,
  History as HistoryIcon,
  FileCopy as FileCopyIcon,
  PostAdd as PostAddIcon,
  MoreVert as MoreVertIcon,
  ContentCopy as ContentCopyIcon,
  LocalOffer as TagIcon,
  CompareArrows as CompareIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';
import DocumentUpload from '../components/DocumentUpload';
import DocumentEditor from '../components/DocumentEditor';
import ShareDocumentDialog from '../components/ShareDocumentDialog';
import DocumentVersionHistoryDialog from '../components/DocumentVersionHistoryDialog';
import DocumentTemplateDialog from '../components/DocumentTemplateDialog';
import DocumentFromTemplateDialog from '../components/DocumentFromTemplateDialog';
import TagManagerDialog from '../components/TagManagerDialog';
import DocumentComparisonTool from '../components/DocumentComparisonTool';
import { documentsApi } from '../services/api';

// Document type icons and colors
const documentTypeConfig = {
  'legal': { color: '#2196f3', icon: <DescriptionIcon /> },
  'contract': { color: '#4caf50', icon: <DescriptionIcon /> },
  'form': { color: '#ff9800', icon: <DescriptionIcon /> },
  'template': { color: '#9c27b0', icon: <FileCopyIcon /> },
  'other': { color: '#757575', icon: <DescriptionIcon /> }
};

const DocumentsPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [documents, setDocuments] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [filteredDocuments, setFilteredDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  
  // New state variables for our dialogs
  const [openEditorDialog, setOpenEditorDialog] = useState(false);
  const [openShareDialog, setOpenShareDialog] = useState(false);
  const [openVersionHistoryDialog, setOpenVersionHistoryDialog] = useState(false);
  const [openTemplateDialog, setOpenTemplateDialog] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  
  // Menu state 
  const [menuAnchorEl, setMenuAnchorEl] = useState(null);
  const menuOpen = Boolean(menuAnchorEl);

  const [createFromTemplateOpen, setCreateFromTemplateOpen] = useState(false);
  const [selectedTemplateId, setSelectedTemplateId] = useState(null);

  const [openTagDialog, setOpenTagDialog] = useState(false);
  const [openComparisonTool, setOpenComparisonTool] = useState(false);

  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments();
    fetchTemplates();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await documentsApi.getDocumentHistory();
      setDocuments(response.documents || []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching documents:', err);
      setError('Failed to load documents. Please try again later.');
      setLoading(false);
    }
  };
  
  const fetchTemplates = async () => {
    try {
      const response = await documentsApi.getTemplates();
      setTemplates(response.templates || []);
    } catch (err) {
      console.error('Error fetching templates:', err);
      // Don't set error since this is secondary content
    }
  };

  // Filter documents when tab or search changes
  useEffect(() => {
    if (!documents) return;

    let filtered = [...documents];
    
    // Filter by tab
    if (tabValue === 1) {
      filtered = filtered.filter(doc => doc.type === 'legal');
    } else if (tabValue === 2) {
      filtered = filtered.filter(doc => doc.type === 'contract');
    } else if (tabValue === 3) {
      filtered = filtered.filter(doc => doc.type === 'template');
    }
    
    // Filter by search
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(doc => 
        doc.title.toLowerCase().includes(query) || 
        (doc.description && doc.description.toLowerCase().includes(query))
      );
    }
    
    setFilteredDocuments(filtered);
  }, [tabValue, searchQuery, documents]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleDocumentUpload = async (fileData) => {
    try {
      // Create document record in backend
      const newDoc = await documentsApi.saveDocument({
        title: fileData.original_filename,
        type: 'other',
        content: fileData.secure_url,
        cloudinaryData: fileData
      });
      
      // Add to local state
      setDocuments(prev => [newDoc, ...prev]);
    } catch (err) {
      console.error('Error saving document:', err);
      setError('Failed to save document. Please try again.');
    }
  };

  const handleDocumentAction = (action, doc) => {
    setSelectedDocument(doc);
    
    if (action === 'view') {
      window.open(doc.content, '_blank');
    } else if (action === 'delete') {
      setOpenDialog(true);
    } else if (action === 'edit') {
      setOpenEditorDialog(true);
    } else if (action === 'share') {
      setOpenShareDialog(true);
    } else if (action === 'history') {
      setOpenVersionHistoryDialog(true);
    } else if (action === 'tags') {
      setOpenTagDialog(true);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!selectedDocument) return;
    
    try {
      await documentsApi.deleteDocument(selectedDocument._id);
      setDocuments(prev => prev.filter(doc => doc._id !== selectedDocument._id));
      setOpenDialog(false);
      setSelectedDocument(null);
    } catch (err) {
      console.error('Error deleting document:', err);
      setError('Failed to delete document. Please try again.');
    }
  };
  
  const handleSaveDocument = async (content) => {
    if (!selectedDocument) return;
    
    try {
      const updatedDoc = await documentsApi.updateDocument(selectedDocument._id, {
        content,
        lastModified: new Date()
      });
      
      // Update document in state
      setDocuments(prev => prev.map(doc => 
        doc._id === selectedDocument._id ? { ...doc, ...updatedDoc } : doc
      ));
      
      // Close editor dialog
      setOpenEditorDialog(false);
    } catch (err) {
      console.error('Error saving document:', err);
      setError('Failed to save document. Please try again.');
    }
  };
  
  const handleCreateTemplate = () => {
    setSelectedTemplate(null);
    setOpenTemplateDialog(true);
  };
  
  const handleEditTemplate = (template) => {
    setSelectedTemplate(template);
    setOpenTemplateDialog(true);
  };
  
  const handleSaveTemplate = async (template) => {
    try {
      if (templates.some(t => t._id === template._id)) {
        // Update existing template in state
        setTemplates(prev => prev.map(t => 
          t._id === template._id ? template : t
        ));
      } else {
        // Add new template to state
        setTemplates(prev => [template, ...prev]);
      }
      
      // Close template dialog
      setOpenTemplateDialog(false);
    } catch (err) {
      console.error('Error saving template:', err);
      setError('Failed to save template. Please try again.');
    }
  };
  
  const handleShareComplete = (userIds) => {
    // Update local document state to reflect sharing
    if (selectedDocument) {
      const updatedDoc = {
        ...selectedDocument,
        sharedWith: [...(selectedDocument.sharedWith || []), ...userIds]
      };
      
      setDocuments(prev => prev.map(doc => 
        doc._id === selectedDocument._id ? updatedDoc : doc
      ));
    }
  };
  
  const handleVersionRevert = async (version) => {
    // Reload the document after reverting
    await fetchDocuments();
  };
  
  const handleMenuClick = (event) => {
    setMenuAnchorEl(event.currentTarget);
  };
  
  const handleMenuClose = () => {
    setMenuAnchorEl(null);
  };
  
  const handleCreateFromTemplate = (templateId = null) => {
    setSelectedTemplateId(templateId);
    setCreateFromTemplateOpen(true);
  };

  const handleDocumentCreated = (newDocument) => {
    // Refresh documents after creating a new one
    fetchDocuments();
  };

  const handleTagsUpdated = (tags) => {
    // Update document in state
    if (selectedDocument) {
      setDocuments(prev => prev.map(doc => 
        doc._id === selectedDocument._id ? { ...doc, tags } : doc
      ));
    }
  };
  
  const handleOpenComparisonTool = () => {
    setOpenComparisonTool(true);
  };

  const renderDocumentCards = () => {
    if (loading) {
      return (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      );
    }

    if (error) {
      return (
        <Box my={4}>
          <Typography color="error" align="center">{error}</Typography>
        </Box>
      );
    }

    if (filteredDocuments.length === 0) {
      return (
        <Box my={4}>
          <Typography align="center" color="textSecondary">
            No documents found. Upload a new document to get started.
          </Typography>
        </Box>
      );
    }

    return (
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {filteredDocuments.map((doc) => {
          const typeConfig = documentTypeConfig[doc.type] || documentTypeConfig.other;
          return (
            <Grid item xs={12} sm={6} md={4} key={doc._id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Box 
                  sx={{ 
                    height: 12, 
                    backgroundColor: typeConfig.color,
                    width: '100%'
                  }} 
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box display="flex" alignItems="center" mb={1}>
                    {typeConfig.icon}
                    <Typography variant="h6" component="h2" sx={{ ml: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {doc.title}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    Created: {new Date(doc.createdAt).toLocaleDateString()}
                  </Typography>
                  {doc.description && (
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {doc.description.length > 100 
                        ? `${doc.description.substring(0, 100)}...` 
                        : doc.description}
                    </Typography>
                  )}
                  <Box mt={2}>
                    <Chip 
                      label={doc.type || 'Other'} 
                      size="small" 
                      sx={{ backgroundColor: typeConfig.color, color: 'white' }} 
                    />
                    {doc.sharedWith && doc.sharedWith.length > 0 && (
                      <Chip 
                        label={`Shared (${doc.sharedWith.length})`}
                        size="small"
                        sx={{ ml: 1, backgroundColor: '#757575', color: 'white' }} 
                      />
                    )}
                    {doc.tags && doc.tags.length > 0 && (
                      <Chip 
                        icon={<TagIcon />}
                        label={`${doc.tags.length} tags`}
                        size="small"
                        sx={{ ml: 1 }}
                        onClick={() => handleDocumentAction('tags', doc)}
                      />
                    )}
                  </Box>
                </CardContent>
                <CardActions>
                  <IconButton size="small" onClick={() => handleDocumentAction('view', doc)}>
                    <FileDownloadIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDocumentAction('edit', doc)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDocumentAction('share', doc)}>
                    <ShareIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDocumentAction('history', doc)}>
                    <HistoryIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDocumentAction('tags', doc)}>
                    <TagIcon />
                  </IconButton>
                  <Box flexGrow={1} />
                  <IconButton size="small" color="error" onClick={() => handleDocumentAction('delete', doc)}>
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    );
  };
  
  const renderTemplateSection = () => {
    if (templates.length === 0) return null;
    
    return (
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>Templates</Typography>
        <Divider sx={{ mb: 3 }} />
        
        <Grid container spacing={3}>
          {templates.map(template => (
            <Grid item xs={12} sm={6} md={3} key={template._id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Box 
                  sx={{ 
                    height: 12, 
                    backgroundColor: '#9c27b0',
                    width: '100%'
                  }} 
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <FileCopyIcon />
                    <Typography variant="h6" component="h2" sx={{ ml: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {template.title}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    {template.category}
                  </Typography>
                  {template.description && (
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {template.description.length > 80 
                        ? `${template.description.substring(0, 80)}...` 
                        : template.description}
                    </Typography>
                  )}
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    startIcon={<ContentCopyIcon />}
                    onClick={() => handleCreateFromTemplate(template._id)}
                  >
                    Use Template
                  </Button>
                  <Box flexGrow={1} />
                  <IconButton size="small" onClick={() => handleEditTemplate(template)}>
                    <EditIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
          
          {/* Add new template card */}
          <Grid item xs={12} sm={6} md={3}>
            <Card 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                border: '2px dashed #ccc',
                backgroundColor: 'rgba(0, 0, 0, 0.03)',
                justifyContent: 'center',
                alignItems: 'center',
                p: 3,
                cursor: 'pointer'
              }}
              onClick={handleCreateTemplate}
            >
              <PostAddIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                Create Template
              </Typography>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  return (
    <PageLayout>
      <Container maxWidth="lg">
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Document Management
          </Typography>
          <Typography variant="body1" paragraph>
            Upload, manage, and share your legal documents securely with SmartProBono.
            Our platform uses Cloudinary for reliable document storage and fast access.
          </Typography>
          
          <Divider sx={{ my: 3 }} />
          
          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" gutterBottom>
              Upload Documents
            </Typography>
            <Typography variant="body1" paragraph>
              Select the appropriate category for your files to ensure they are stored correctly.
              All uploads are secure and only accessible to authorized users.
            </Typography>
            <DocumentUpload onUploadComplete={handleDocumentUpload} />
          </Box>
          
          <Divider sx={{ my: 3 }} />
          
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 2 }}>
              <Typography variant="h5">My Documents</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <TextField
                  placeholder="Search documents..."
                  variant="outlined"
                  size="small"
                  value={searchQuery}
                  onChange={handleSearchChange}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                  }}
                  sx={{ width: { xs: '100%', sm: '300px' } }}
                />
                
                <Button
                  variant="outlined"
                  color="primary"
                  startIcon={<CompareIcon />}
                  onClick={handleOpenComparisonTool}
                >
                  Compare
                </Button>
                
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<AddIcon />}
                  onClick={handleMenuClick}
                >
                  Create
                </Button>
                
                <Menu
                  anchorEl={menuAnchorEl}
                  open={menuOpen}
                  onClose={handleMenuClose}
                >
                  <MenuItem onClick={handleCreateTemplate}>
                    <ListItemIcon>
                      <PostAddIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText>Create Template</ListItemText>
                  </MenuItem>
                  
                  {templates.length > 0 && (
                    <MenuItem
                      onClick={() => {
                        handleMenuClose();
                        // Would open template selection dialog
                      }}
                    >
                      <ListItemIcon>
                        <ContentCopyIcon fontSize="small" />
                      </ListItemIcon>
                      <ListItemText>Use Template</ListItemText>
                    </MenuItem>
                  )}
                </Menu>
              </Box>
            </Box>
            
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              sx={{ mt: 2 }}
              variant="scrollable"
              scrollButtons="auto"
            >
              <Tab label="All Documents" />
              <Tab label="Legal Documents" />
              <Tab label="Contracts" />
              <Tab label="Templates" />
            </Tabs>
          </Box>
          
          {renderDocumentCards()}
          
          {renderTemplateSection()}
        </Paper>
      </Container>
      
      {/* Delete Confirmation Dialog */}
      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this document?
            {selectedDocument && ` "${selectedDocument.title}"`}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error">Delete</Button>
        </DialogActions>
      </Dialog>
      
      {/* Document Editor Dialog */}
      {selectedDocument && (
        <Dialog
          open={openEditorDialog}
          onClose={() => setOpenEditorDialog(false)}
          maxWidth="lg"
          fullWidth
          PaperProps={{ sx: { height: '90vh' } }}
        >
          <DialogTitle>
            Edit Document: {selectedDocument.title}
          </DialogTitle>
          <DialogContent dividers>
            <DocumentEditor
              documentId={selectedDocument._id}
              initialContent={selectedDocument.content}
              onSave={handleSaveDocument}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenEditorDialog(false)}>Close</Button>
          </DialogActions>
        </Dialog>
      )}
      
      {/* Document Sharing Dialog */}
      {selectedDocument && (
        <ShareDocumentDialog
          open={openShareDialog}
          onClose={() => setOpenShareDialog(false)}
          document={selectedDocument}
          onShareComplete={handleShareComplete}
        />
      )}
      
      {/* Document Version History Dialog */}
      {selectedDocument && (
        <DocumentVersionHistoryDialog
          open={openVersionHistoryDialog}
          onClose={() => setOpenVersionHistoryDialog(false)}
          document={selectedDocument}
          onRevertToVersion={handleVersionRevert}
        />
      )}
      
      {/* Document Template Dialog */}
      <DocumentTemplateDialog
        open={openTemplateDialog}
        onClose={() => setOpenTemplateDialog(false)}
        onSave={handleSaveTemplate}
        initialTemplate={selectedTemplate}
      />
      
      <DocumentFromTemplateDialog
        open={createFromTemplateOpen}
        onClose={() => setCreateFromTemplateOpen(false)}
        onDocumentCreated={handleDocumentCreated}
        initialTemplateId={selectedTemplateId}
      />
      
      {/* Tag Manager Dialog */}
      {selectedDocument && (
        <TagManagerDialog
          open={openTagDialog}
          onClose={() => setOpenTagDialog(false)}
          document={selectedDocument}
          onTagsUpdated={handleTagsUpdated}
        />
      )}
      
      {/* Document Comparison Tool */}
      <DocumentComparisonTool
        open={openComparisonTool}
        onClose={() => setOpenComparisonTool(false)}
        documents={documents}
      />
    </PageLayout>
  );
};

export default DocumentsPage; 
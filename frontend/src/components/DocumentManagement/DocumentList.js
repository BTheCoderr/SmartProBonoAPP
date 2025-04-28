import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, TablePagination, IconButton, Chip, Tooltip,
  TextField, MenuItem, Select, FormControl, InputLabel, InputAdornment,
  CircularProgress, Alert, Button
} from '@mui/material';
import {
  Search, FilterList, GetApp, Visibility, Delete, Edit, 
  Share, History, InsertDriveFile, Description, Image,
  PictureAsPdf, Archive, Code, Movie, AudioFile
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import ApiService from '../../services/ApiService';

const getFileIcon = (fileType) => {
  if (!fileType) return <InsertDriveFile />;
  
  if (fileType.includes('pdf')) return <PictureAsPdf color="error" />;
  if (fileType.includes('image')) return <Image color="primary" />;
  if (fileType.includes('word') || fileType.includes('document')) return <Description color="primary" />;
  if (fileType.includes('zip') || fileType.includes('rar')) return <Archive color="warning" />;
  if (fileType.includes('text')) return <Code color="info" />;
  if (fileType.includes('video')) return <Movie color="secondary" />;
  if (fileType.includes('audio')) return <AudioFile color="success" />;
  
  return <InsertDriveFile />;
};

const getAccessLevelColor = (level) => {
  switch (level) {
    case 'public': return 'success';
    case 'internal': return 'info';
    case 'confidential': return 'warning';
    case 'restricted': return 'error';
    default: return 'default';
  }
};

const DocumentList = ({ 
  onViewDocument, 
  onEditDocument, 
  onDeleteDocument, 
  onShareDocument,
  onViewHistory,
  refreshTrigger
}) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalCount, setTotalCount] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    documentType: '',
    accessLevel: '',
    status: 'active'
  });
  const [sortBy, setSortBy] = useState('created_at');
  const [sortDirection, setSortDirection] = useState('desc');
  
  const navigate = useNavigate();

  // Load documents
  useEffect(() => {
    fetchDocuments();
  }, [page, rowsPerPage, sortBy, sortDirection, filters, refreshTrigger]);

  // Fetch documents with current filters, sorting, and pagination
  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Build query parameters
      const queryParams = new URLSearchParams({
        page: page + 1, // API uses 1-based indexing
        limit: rowsPerPage,
        sort: sortBy,
        direction: sortDirection
      });
      
      // Add filters if they have values
      if (filters.documentType) queryParams.append('document_type', filters.documentType);
      if (filters.accessLevel) queryParams.append('access_level', filters.accessLevel);
      if (filters.status) queryParams.append('status', filters.status);
      
      // Add search term if present
      if (searchTerm.trim()) queryParams.append('search', searchTerm.trim());
      
      const response = await ApiService.get(`/api/documents?${queryParams.toString()}`);
      
      setDocuments(response.data.documents || []);
      setTotalCount(response.data.total || 0);
    } catch (err) {
      console.error('Error fetching documents:', err);
      setError('Failed to load documents. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Handle page change
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  // Handle rows per page change
  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Handle search
  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  // Apply search (on Enter key)
  const applySearch = (event) => {
    if (event.key === 'Enter') {
      setPage(0); // Reset to first page
      fetchDocuments();
    }
  };

  // Handle filter changes
  const handleFilterChange = (filterName) => (event) => {
    setFilters({
      ...filters,
      [filterName]: event.target.value
    });
    setPage(0); // Reset to first page
  };

  // Handle sort change
  const handleSortChange = (column) => {
    if (sortBy === column) {
      // Toggle direction if same column
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // Default to desc for new column
      setSortBy(column);
      setSortDirection('desc');
    }
    setPage(0); // Reset to first page
  };

  // Handle download document
  const handleDownload = async (documentId, filename) => {
    try {
      const response = await ApiService.getFile(`/api/documents/${documentId}/file`);
      
      // Create blob URL and trigger download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Error downloading document:', err);
      setError('Failed to download document. Please try again later.');
    }
  };

  // Render functions
  const renderFilters = () => (
    <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
      <TextField
        label="Search Documents"
        value={searchTerm}
        onChange={handleSearch}
        onKeyPress={applySearch}
        variant="outlined"
        size="small"
        sx={{ minWidth: 250, flex: 1 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
        }}
      />
      
      <FormControl size="small" sx={{ minWidth: 150 }}>
        <InputLabel id="document-type-label">Document Type</InputLabel>
        <Select
          labelId="document-type-label"
          value={filters.documentType}
          onChange={handleFilterChange('documentType')}
          label="Document Type"
        >
          <MenuItem value="">All Types</MenuItem>
          <MenuItem value="contract">Contract</MenuItem>
          <MenuItem value="court_filing">Court Filing</MenuItem>
          <MenuItem value="legal_letter">Legal Letter</MenuItem>
          <MenuItem value="immigration_form">Immigration Form</MenuItem>
          <MenuItem value="small_claims">Small Claims</MenuItem>
          <MenuItem value="other">Other</MenuItem>
        </Select>
      </FormControl>
      
      <FormControl size="small" sx={{ minWidth: 150 }}>
        <InputLabel id="access-level-label">Access Level</InputLabel>
        <Select
          labelId="access-level-label"
          value={filters.accessLevel}
          onChange={handleFilterChange('accessLevel')}
          label="Access Level"
        >
          <MenuItem value="">All Levels</MenuItem>
          <MenuItem value="public">Public</MenuItem>
          <MenuItem value="internal">Internal</MenuItem>
          <MenuItem value="confidential">Confidential</MenuItem>
          <MenuItem value="restricted">Restricted</MenuItem>
        </Select>
      </FormControl>
      
      <FormControl size="small" sx={{ minWidth: 120 }}>
        <InputLabel id="status-label">Status</InputLabel>
        <Select
          labelId="status-label"
          value={filters.status}
          onChange={handleFilterChange('status')}
          label="Status"
        >
          <MenuItem value="active">Active</MenuItem>
          <MenuItem value="archived">Archived</MenuItem>
          <MenuItem value="">All</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );

  const renderDocumentList = () => (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Table sx={{ minWidth: 650 }} size="medium">
        <TableHead>
          <TableRow>
            <TableCell>Document</TableCell>
            <TableCell 
              onClick={() => handleSortChange('metadata.document_type')}
              sx={{ cursor: 'pointer' }}
            >
              Type {sortBy === 'metadata.document_type' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableCell>
            <TableCell 
              onClick={() => handleSortChange('access_level')}
              sx={{ cursor: 'pointer' }}
            >
              Access Level {sortBy === 'access_level' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableCell>
            <TableCell 
              onClick={() => handleSortChange('created_at')}
              sx={{ cursor: 'pointer' }}
            >
              Created {sortBy === 'created_at' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableCell>
            <TableCell 
              onClick={() => handleSortChange('updated_at')}
              sx={{ cursor: 'pointer' }}
            >
              Updated {sortBy === 'updated_at' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {loading && !documents.length ? (
            <TableRow>
              <TableCell colSpan={6} align="center">
                <CircularProgress size={40} sx={{ my: 2 }} />
              </TableCell>
            </TableRow>
          ) : error ? (
            <TableRow>
              <TableCell colSpan={6}>
                <Alert severity="error">{error}</Alert>
              </TableCell>
            </TableRow>
          ) : !documents.length ? (
            <TableRow>
              <TableCell colSpan={6} align="center">
                <Typography variant="body1" color="text.secondary" sx={{ py: 2 }}>
                  No documents found. Try adjusting your filters or upload a new document.
                </Typography>
                <Button 
                  variant="contained" 
                  color="primary"
                  onClick={() => navigate('/documents/upload')}
                  sx={{ mt: 1 }}
                >
                  Upload Document
                </Button>
              </TableCell>
            </TableRow>
          ) : (
            documents.map((doc) => (
              <TableRow key={doc._id}>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {getFileIcon(doc.file_type)}
                    <Box sx={{ ml: 2 }}>
                      <Typography variant="body1">
                        {doc.metadata?.title || doc.original_filename || 'Untitled Document'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {doc.original_filename}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip 
                    label={doc.metadata?.document_type || 'Unknown'} 
                    size="small"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Chip 
                    label={doc.access_level || 'Internal'} 
                    size="small"
                    color={getAccessLevelColor(doc.access_level)}
                  />
                </TableCell>
                <TableCell>
                  {new Date(doc.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  {new Date(doc.updated_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <Tooltip title="View">
                    <IconButton 
                      size="small"
                      onClick={() => onViewDocument(doc)}
                    >
                      <Visibility />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Download">
                    <IconButton 
                      size="small"
                      onClick={() => handleDownload(doc._id, doc.original_filename)}
                    >
                      <GetApp />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Edit">
                    <IconButton 
                      size="small"
                      onClick={() => onEditDocument(doc)}
                    >
                      <Edit />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Share">
                    <IconButton 
                      size="small"
                      onClick={() => onShareDocument(doc)}
                    >
                      <Share />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Version History">
                    <IconButton 
                      size="small"
                      onClick={() => onViewHistory(doc)}
                    >
                      <History />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton 
                      size="small"
                      color="error"
                      onClick={() => onDeleteDocument(doc)}
                    >
                      <Delete />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25, 50]}
        component="div"
        count={totalCount}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </TableContainer>
  );

  return (
    <Box>
      {renderFilters()}
      {renderDocumentList()}
    </Box>
  );
};

DocumentList.propTypes = {
  onViewDocument: PropTypes.func.isRequired,
  onEditDocument: PropTypes.func.isRequired,
  onDeleteDocument: PropTypes.func.isRequired,
  onShareDocument: PropTypes.func.isRequired,
  onViewHistory: PropTypes.func.isRequired,
  refreshTrigger: PropTypes.any
};

export default DocumentList; 
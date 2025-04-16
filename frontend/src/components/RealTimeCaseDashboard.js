import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Tooltip,
  Divider,
  FormControl,
  InputLabel,
  Select,
  Alert,
  TextField,
  CircularProgress,
  Card,
  CardContent,
  CardActions,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Snackbar,
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import {
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  MoreVert as MoreVertIcon,
  Assignment as AssignmentIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  ArrowUpward as ArrowUpwardIcon,
  ArrowDownward as ArrowDownwardIcon,
  Notifications as NotificationsIcon,
  Clear as ClearIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { useWebSocket } from '../contexts/WebSocketContext';
import { getAllCases, updateCasesBatch, deleteCasesBatch } from '../services/caseService';
import { useMediaQuery } from '@mui/material';

// Status and priority colors
const STATUS_COLORS = {
  new: 'primary',
  in_progress: 'secondary',
  pending_review: 'warning',
  completed: 'success',
  closed: 'default',
};

const PRIORITY_COLORS = {
  urgent: 'error',
  high: 'warning',
  medium: 'info',
  low: 'success',
};

const RealTimeCaseDashboard = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  const { isConnected, addEventListener, joinCaseRoom, clearCaseUpdates } = useWebSocket();

  // State
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCases, setSelectedCases] = useState([]);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: '',
  });
  const [sortField, setSortField] = useState('updated');
  const [sortDirection, setSortDirection] = useState('desc');
  const [anchorEl, setAnchorEl] = useState(null);
  const [batchDialogOpen, setBatchDialogOpen] = useState(false);
  const [batchAction, setBatchAction] = useState(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('info');
  const [batchUpdateData, setBatchUpdateData] = useState(null);

  // Fetch cases on mount and when filters change
  useEffect(() => {
    fetchCases();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters, sortField, sortDirection]);

  // Set up WebSocket listeners for real-time updates
  useEffect(() => {
    if (!isConnected) return;

    // Join room for all cases
    joinCaseRoom('all');

    // Listen for case updates
    const unsubscribeCaseUpdated = addEventListener('case_updated', handleCaseUpdate);
    const unsubscribeCaseCreated = addEventListener('case_created', handleCaseCreated);
    const unsubscribeCaseStatusChanged = addEventListener('case_status_changed', handleCaseUpdate);
    const unsubscribeCasePriorityChanged = addEventListener('case_priority_changed', handleCaseUpdate);
    const unsubscribeCaseAssigned = addEventListener('case_assigned', handleCaseUpdate);

    // Cleanup when unmounting
    return () => {
      unsubscribeCaseUpdated();
      unsubscribeCaseCreated();
      unsubscribeCaseStatusChanged();
      unsubscribeCasePriorityChanged();
      unsubscribeCaseAssigned();
      clearCaseUpdates();
    };
  }, [isConnected, addEventListener, joinCaseRoom, clearCaseUpdates]);

  // Handler for case updates from WebSocket
  const handleCaseUpdate = useCallback((updatedCase) => {
    setCases((prevCases) => {
      const index = prevCases.findIndex((c) => c.id === updatedCase.id);
      if (index === -1) return prevCases;
      
      const newCases = [...prevCases];
      newCases[index] = { ...newCases[index], ...updatedCase };
      return newCases;
    });
    
    showSnackbar(`Case ${updatedCase.title || updatedCase.id} was updated`, 'info');
  }, []);

  // Handler for new cases from WebSocket
  const handleCaseCreated = useCallback((newCase) => {
    setCases((prevCases) => {
      // Check if case already exists
      if (prevCases.some((c) => c.id === newCase.id)) return prevCases;
      return [newCase, ...prevCases];
    });
    
    showSnackbar(`New case created: ${newCase.title || newCase.id}`, 'success');
  }, []);

  // Fetch cases from API
  const fetchCases = async () => {
    try {
      setLoading(true);
      const response = await getAllCases({
        ...filters,
        sort_by: sortField,
        sort_direction: sortDirection,
      });
      setCases(response);
      setError(null);
    } catch (err) {
      console.error('Error fetching cases:', err);
      setError('Failed to load cases. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle filter changes
  const handleFilterChange = (field, value) => {
    setFilters((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  // Handle sort changes
  const handleSort = (field) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  // Handle case selection
  const handleCaseSelect = (caseId) => {
    setSelectedCases((prev) => {
      if (prev.includes(caseId)) {
        return prev.filter((id) => id !== caseId);
      } else {
        return [...prev, caseId];
      }
    });
  };

  // Handle "Select All" toggle
  const handleSelectAll = () => {
    if (selectedCases.length === cases.length) {
      setSelectedCases([]);
    } else {
      setSelectedCases(cases.map((c) => c.id));
    }
  };

  // Open batch actions menu
  const handleBatchMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  // Close batch actions menu
  const handleBatchMenuClose = () => {
    setAnchorEl(null);
  };

  // Open batch action dialog
  const handleBatchAction = (action) => {
    setBatchAction(action);
    setBatchDialogOpen(true);
    handleBatchMenuClose();
  };

  // Close batch action dialog
  const handleBatchDialogClose = () => {
    setBatchDialogOpen(false);
    setBatchAction(null);
  };

  // Execute batch action
  const executeBatchAction = async () => {
    if (!batchAction || selectedCases.length === 0) return;

    try {
      setLoading(true);

      switch (batchAction) {
        case 'status':
          await updateCasesBatch(selectedCases, { status: 'in_progress' });
          showSnackbar(`Updated status for ${selectedCases.length} cases`, 'success');
          break;
        case 'priority':
          await updateCasesBatch(selectedCases, { priority: 'high' });
          showSnackbar(`Updated priority for ${selectedCases.length} cases`, 'success');
          break;
        case 'delete':
          await deleteCasesBatch(selectedCases);
          showSnackbar(`Deleted ${selectedCases.length} cases`, 'success');
          break;
        default:
          break;
      }

      // Refresh cases and clear selection
      await fetchCases();
      setSelectedCases([]);
    } catch (err) {
      console.error('Error executing batch action:', err);
      showSnackbar('Failed to perform batch action', 'error');
    } finally {
      setLoading(false);
      handleBatchDialogClose();
    }
  };

  // Show a case's details
  const handleViewCase = (caseId) => {
    navigate(`/cases/${caseId}`);
  };

  // Show snackbar message
  const showSnackbar = (message, severity = 'info') => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setSnackbarOpen(true);
  };

  // Close snackbar
  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  // Render case status chip
  const renderStatusChip = (status) => (
    <Chip
      label={t(status)}
      color={STATUS_COLORS[status] || 'default'}
      size="small"
      sx={{ textTransform: 'capitalize' }}
    />
  );

  // Render case priority chip
  const renderPriorityChip = (priority) => (
    <Chip
      label={t(priority)}
      color={PRIORITY_COLORS[priority] || 'default'}
      size="small"
      sx={{ textTransform: 'capitalize' }}
    />
  );

  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Box sx={{ width: '100%' }}>
      {/* Header with title and actions */}
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: { xs: 'column', sm: 'row' },
          justifyContent: 'space-between', 
          alignItems: { xs: 'stretch', sm: 'center' },
          mb: { xs: 2, sm: 3 },
          gap: { xs: 2, sm: 0 }
        }}
      >
        <Typography variant="h5" component="h1" sx={{ fontWeight: 600 }}>
          {t('Case Dashboard')}
          {isConnected && (
            <Chip
              label={t('Live')}
              color="success"
              size="small"
              sx={{ ml: 1.5, height: '22px' }}
            />
          )}
        </Typography>

        <Box 
          sx={{ 
            display: 'flex', 
            gap: { xs: 1, sm: 2 },
            flexWrap: 'wrap',
            justifyContent: { xs: 'space-between', sm: 'flex-end' } 
          }}
        >
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            size={isMobile ? 'small' : 'medium'}
            onClick={fetchCases}
          >
            {isMobile ? t('Refresh') : t('Refresh Cases')}
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/cases/new')}
            size={isMobile ? 'small' : 'medium'}
          >
            {isMobile ? t('New') : t('New Case')}
          </Button>
        </Box>
      </Box>

      {/* Filters section - collapsible on mobile */}
      <Paper 
        sx={{ 
          p: { xs: 1.5, sm: 2 }, 
          mb: { xs: 2, sm: 3 },
          display: 'flex',
          flexDirection: 'column',
          gap: 2
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="subtitle1" component="h2">
            <FilterIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
            {t('Filters')}
          </Typography>
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <FormControl fullWidth size={isMobile ? 'small' : 'medium'}>
              <InputLabel>{t('Status')}</InputLabel>
              <Select
                value={filters.status}
                label={t('Status')}
                onChange={(e) => handleFilterChange('status', e.target.value)}
              >
                <MenuItem value="">{t('All Statuses')}</MenuItem>
                <MenuItem value="new">{t('New')}</MenuItem>
                <MenuItem value="in_progress">{t('In Progress')}</MenuItem>
                <MenuItem value="pending_review">{t('Pending Review')}</MenuItem>
                <MenuItem value="completed">{t('Completed')}</MenuItem>
                <MenuItem value="closed">{t('Closed')}</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={4}>
            <FormControl fullWidth size={isMobile ? 'small' : 'medium'}>
              <InputLabel>{t('Priority')}</InputLabel>
              <Select
                value={filters.priority}
                label={t('Priority')}
                onChange={(e) => handleFilterChange('priority', e.target.value)}
              >
                <MenuItem value="">{t('All Priorities')}</MenuItem>
                <MenuItem value="urgent">{t('Urgent')}</MenuItem>
                <MenuItem value="high">{t('High')}</MenuItem>
                <MenuItem value="medium">{t('Medium')}</MenuItem>
                <MenuItem value="low">{t('Low')}</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              label={t('Search')}
              variant="outlined"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              size={isMobile ? 'small' : 'medium'}
              InputProps={{
                endAdornment: filters.search ? (
                  <IconButton
                    size="small"
                    onClick={() => handleFilterChange('search', '')}
                    edge="end"
                  >
                    <ClearIcon fontSize="small" />
                  </IconButton>
                ) : null,
              }}
            />
          </Grid>
        </Grid>
      </Paper>

      {/* Batch actions bar - only show when cases are selected */}
      {selectedCases.length > 0 && (
        <Paper
          sx={{
            p: { xs: 1.5, sm: 2 },
            mb: { xs: 2, sm: 3 },
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: 1
          }}
        >
          <Typography variant="subtitle2">
            {t('{{count}} cases selected', { count: selectedCases.length })}
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Button
              variant="outlined"
              size={isMobile ? 'small' : 'medium'}
              onClick={() => handleBatchAction('status')}
            >
              {t('Update Status')}
            </Button>
            <Button
              variant="outlined"
              size={isMobile ? 'small' : 'medium'}
              onClick={() => handleBatchAction('priority')}
            >
              {t('Update Priority')}
            </Button>
            <Button
              variant="outlined"
              color="secondary"
              size={isMobile ? 'small' : 'medium'}
              onClick={() => handleBatchAction('delete')}
            >
              {t('Delete')}
            </Button>
          </Box>
        </Paper>
      )}

      {/* Error handling */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
          <Button size="small" onClick={fetchCases} sx={{ ml: 2 }}>
            {t('Retry')}
          </Button>
        </Alert>
      )}

      {/* Loading state */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Cases grid */}
      {!loading && cases.length === 0 ? (
        <Paper
          sx={{
            p: 4,
            textAlign: 'center',
            borderStyle: 'dashed',
            borderWidth: 1,
            borderColor: 'divider',
          }}
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            {t('No cases found')}
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            {filters.status || filters.priority || filters.search
              ? t('Try adjusting your filters')
              : t('Get started by creating your first case')}
          </Typography>
          {!(filters.status || filters.priority || filters.search) && (
            <Button
              variant="contained"
              onClick={() => navigate('/cases/new')}
              sx={{ mt: 2 }}
            >
              {t('Create Case')}
            </Button>
          )}
        </Paper>
      ) : (
        <Grid container spacing={2}>
          {!loading &&
            cases.map((caseItem) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={caseItem.id}>
                <Box sx={{ position: 'relative' }}>
                  {/* Checkbox for case selection */}
                  <Checkbox
                    checked={selectedCases.includes(caseItem.id)}
                    onChange={() => handleCaseSelect(caseItem.id)}
                    sx={{
                      position: 'absolute',
                      top: 8,
                      right: 8,
                      zIndex: 1,
                      p: 0.5,
                      backgroundColor: 'rgba(255, 255, 255, 0.8)',
                      borderRadius: '50%',
                    }}
                  />
                  <CaseCard
                    caseData={caseItem}
                    variant="compact"
                    onClick={() => handleCaseSelect(caseItem.id)}
                  />
                </Box>
              </Grid>
            ))}
        </Grid>
      )}

      {/* Batch action dialog */}
      <Dialog
        open={batchDialogOpen}
        onClose={handleBatchDialogClose}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>
          {batchAction === 'status'
            ? t('Update Status')
            : batchAction === 'priority'
            ? t('Update Priority')
            : t('Delete Cases')}
        </DialogTitle>
        <DialogContent>
          {batchAction === 'delete' ? (
            <DialogContentText>
              {t('Are you sure you want to delete {{count}} cases? This action cannot be undone.', {
                count: selectedCases.length,
              })}
            </DialogContentText>
          ) : batchAction === 'status' ? (
            <FormControl fullWidth sx={{ mt: 1 }}>
              <InputLabel>{t('New Status')}</InputLabel>
              <Select
                value={batchUpdateData?.status || ''}
                label={t('New Status')}
                onChange={(e) =>
                  setBatchUpdateData({ ...batchUpdateData, status: e.target.value })
                }
              >
                <MenuItem value="new">{t('New')}</MenuItem>
                <MenuItem value="in_progress">{t('In Progress')}</MenuItem>
                <MenuItem value="pending_review">{t('Pending Review')}</MenuItem>
                <MenuItem value="completed">{t('Completed')}</MenuItem>
                <MenuItem value="closed">{t('Closed')}</MenuItem>
              </Select>
            </FormControl>
          ) : (
            <FormControl fullWidth sx={{ mt: 1 }}>
              <InputLabel>{t('New Priority')}</InputLabel>
              <Select
                value={batchUpdateData?.priority || ''}
                label={t('New Priority')}
                onChange={(e) =>
                  setBatchUpdateData({ ...batchUpdateData, priority: e.target.value })
                }
              >
                <MenuItem value="urgent">{t('Urgent')}</MenuItem>
                <MenuItem value="high">{t('High')}</MenuItem>
                <MenuItem value="medium">{t('Medium')}</MenuItem>
                <MenuItem value="low">{t('Low')}</MenuItem>
              </Select>
            </FormControl>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleBatchDialogClose} color="inherit">
            {t('Cancel')}
          </Button>
          <Button
            onClick={executeBatchAction}
            color={batchAction === 'delete' ? 'error' : 'primary'}
            variant="contained"
          >
            {batchAction === 'delete' ? t('Delete') : t('Update')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: isMobile ? 'center' : 'right',
        }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity={snackbarSeverity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default RealTimeCaseDashboard; 
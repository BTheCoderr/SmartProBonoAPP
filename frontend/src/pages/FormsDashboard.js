import React, { useState, useEffect } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  Container, Grid, Paper, Typography, Box, Button, Divider,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  CircularProgress, Alert, Chip, IconButton, Card, CardContent,
  LinearProgress, Tabs, Tab, TextField, InputAdornment,
  Menu, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions,
  Tooltip, TablePagination
} from '@mui/material';
import {
  Search, Assignment, AssignmentTurnedIn, VisibilityOutlined, GetAppOutlined,
  DeleteOutline, Edit, DescriptionOutlined, Add, FilterList, Sort,
  MoreVert, Visibility, GetApp, Delete, FileCopy, CheckCircle,
  Error, HourglassEmpty, Refresh, Assessment, Download, Save
} from '@mui/icons-material';
import { format } from 'date-fns';
import ApiService from '../services/ApiService';
import AnalyticsService from '../services/AnalyticsService';
import { useSnackbar } from 'notistack';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip,
  ResponsiveContainer, LineChart, Line, PieChart as RechartsPieChart,
  Pie, Cell
} from 'recharts';
import { Chart } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip as ChartTooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  ChartTooltip,
  Legend
);

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const StatusChip = ({ status }) => {
  const statusProps = {
    completed: { color: 'success', label: 'Completed' },
    in_progress: { color: 'primary', label: 'In Progress' },
    submitted: { color: 'info', label: 'Submitted' },
    draft: { color: 'default', label: 'Draft' },
    review: { color: 'warning', label: 'Under Review' },
    rejected: { color: 'error', label: 'Rejected' }
  };

  const { color, label } = statusProps[status] || { color: 'default', label: status };

  return <Chip color={color} label={label} size="small" />;
};

const FormsDashboard = () => {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [forms, setForms] = useState([]);
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('updatedAt');
  const [sortOrder, setSortOrder] = useState('desc');
  const [stats, setStats] = useState(null);
  const [completionRates, setCompletionRates] = useState([]);
  const [abandonmentData, setAbandonmentData] = useState([]);
  const [selectedForm, setSelectedForm] = useState(null);
  const [menuAnchorEl, setMenuAnchorEl] = useState(null);
  const [analyticsDialog, setAnalyticsDialog] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filters, setFilters] = useState({
    status: 'all',
    type: 'all',
    search: '',
    dateRange: 'all'
  });
  const [analytics, setAnalytics] = useState({
    totalForms: 0,
    completionRate: 0,
    averageCompletionTime: 0,
    formTypeDistribution: [],
    statusDistribution: [],
    weeklySubmissions: []
  });

  // Load dashboard data
  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);
      try {
        const [formsData, statsData, completionData, abandonmentData] = await Promise.all([
          loadForms(),
          AnalyticsService.getDashboardStats(),
          AnalyticsService.getCompletionRates(),
          AnalyticsService.getAbandonmentAnalysis()
        ]);

        setForms(formsData);
        setStats(statsData);
        setCompletionRates(completionData);
        setAbandonmentData(abandonmentData);
      } catch (err) {
        console.error('Error loading dashboard data:', err);
        setError('Failed to load dashboard data');
        enqueueSnackbar('Failed to load dashboard data', { variant: 'error' });
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, [refreshKey]);

  // Load forms and drafts
  const loadForms = async () => {
    setLoading(true);
    setError(null);
    try {
      const drafts = [];
      
      // Check for drafts in localStorage
      ['small_claims', 'eviction_response', 'fee_waiver'].forEach(formType => {
        const draft = localStorage.getItem(`${formType}FormDraft`);
        if (draft) {
          try {
            const parsedDraft = JSON.parse(draft);
            drafts.push({
              id: `draft-${formType}`,
              title: `${formType.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} (Draft)`,
              type: formType,
              status: 'draft',
              createdAt: parsedDraft.timestamp,
              updatedAt: parsedDraft.timestamp,
              documentId: null,
              completionPercentage: calculateDraftCompletion(parsedDraft.values, formType)
            });
          } catch (err) {
            console.error(`Error parsing ${formType} draft:`, err);
          }
        }
      });

      // Fetch submitted forms from API
      const response = await ApiService.get('/api/forms');
      return [...drafts, ...response.data];
    } catch (err) {
      console.error('Error fetching forms:', err);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const calculateDraftCompletion = (values, formType) => {
    const requiredFields = {
      small_claims: ['plaintiff_name', 'defendant_name', 'claim_amount'],
      eviction_response: ['tenant_name', 'landlord_name', 'property_address'],
      fee_waiver: ['applicant_name', 'court_county', 'monthly_income']
    };

    const fields = requiredFields[formType] || [];
    const completed = fields.filter(field => values[field]).length;
    return Math.round((completed / fields.length) * 100);
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('asc');
    }
  };

  const handleMenuOpen = (event, form) => {
    setSelectedForm(form);
    setMenuAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setMenuAnchorEl(null);
  };

  const handleAnalyticsOpen = async (form) => {
    try {
      const analytics = await AnalyticsService.getFormAnalytics(form.type);
      setSelectedForm({ ...form, analytics });
      setAnalyticsDialog(true);
    } catch (err) {
      enqueueSnackbar('Failed to load form analytics', { variant: 'error' });
    }
    handleMenuClose();
  };

  const handleDeleteForm = async (form) => {
    if (window.confirm('Are you sure you want to delete this form?')) {
      try {
        if (form.status === 'draft') {
          localStorage.removeItem(`${form.type}FormDraft`);
        } else {
          await ApiService.delete(`/api/forms/${form.id}`);
        }
        
        setForms(forms.filter(f => f.id !== form.id));
        enqueueSnackbar('Form deleted successfully', { variant: 'success' });
        setRefreshKey(prev => prev + 1);
      } catch (err) {
        enqueueSnackbar('Failed to delete form', { variant: 'error' });
      }
    }
    handleMenuClose();
  };

  const handleContinueForm = (form) => {
    const routes = {
      small_claims: '/forms/small-claims',
      eviction_response: '/forms/eviction-response',
      fee_waiver: '/forms/fee-waiver'
    };

    navigate(routes[form.type] || '/forms');
    handleMenuClose();
  };

  const handleView = (formId) => {
    navigate(`/documents/${formId}`);
  };

  const handleDownload = async (formId) => {
    try {
      const blob = await ApiService.downloadPDF(formId);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `document-${formId}.pdf`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download document. Please try again.');
    }
  };

  const handleEdit = (formId, formType) => {
    navigate(`/forms/${formType}/${formId}/edit`);
  };

  const handleDuplicate = async (formId) => {
    try {
      await ApiService.duplicateDocument(formId);
      setRefreshKey(prev => prev + 1);
    } catch (err) {
      setError('Failed to duplicate form. Please try again.');
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  // Apply filters and search
  const filteredAndSearchedForms = forms.filter(form => {
    if (filters.status !== 'all' && form.status !== filters.status) return false;
    if (filters.type !== 'all' && form.type !== filters.type) return false;
    if (filters.search && !form.title.toLowerCase().includes(filters.search.toLowerCase())) return false;
    return true;
  });

  // Apply sorting
  const sortedForms = [...filteredAndSearchedForms].sort((a, b) => {
    const aValue = a[sortBy];
    const bValue = b[sortBy];
    const modifier = sortOrder === 'asc' ? 1 : -1;
    return aValue < bValue ? -1 * modifier : aValue > bValue ? 1 * modifier : 0;
  });

  // Apply pagination
  const paginatedForms = sortedForms.slice(page * rowsPerPage, (page + 1) * rowsPerPage);

  const renderAnalyticsDialog = () => (
    <Dialog 
      open={analyticsDialog} 
      onClose={() => setAnalyticsDialog(false)}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        Form Analytics: {selectedForm?.title}
      </DialogTitle>
      <DialogContent>
        {selectedForm?.analytics && (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Chart type="bar" data={selectedForm.analytics.fieldCompletionRates} />
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6">Completion Rate</Typography>
                  <Box sx={{ height: 200 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={[
                            { name: 'Completed', value: selectedForm.analytics.completionRate },
                            { name: 'Incomplete', value: 100 - selectedForm.analytics.completionRate }
                          ]}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {selectedForm.analytics.completionRate > 0 && (
                            <Cell key="completed" fill={COLORS[0]} />
                          )}
                          {100 - selectedForm.analytics.completionRate > 0 && (
                            <Cell key="incomplete" fill={COLORS[1]} />
                          )}
                        </Pie>
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6">Time to Complete</Typography>
                  <Box sx={{ height: 200 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={selectedForm.analytics.timeToComplete}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <RechartsTooltip />
                        <Line type="monotone" dataKey="minutes" stroke="#8884d8" />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6">Field Completion Rates</Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={selectedForm.analytics.fieldCompletionRates}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="field" />
                        <YAxis />
                        <RechartsTooltip />
                        <Bar dataKey="rate" fill="#8884d8" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setAnalyticsDialog(false)}>Close</Button>
      </DialogActions>
    </Dialog>
  );

  // Handle pagination
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>Forms Dashboard</Typography>
        <Typography variant="body1" color="text.secondary">
          Track and manage all your legal forms in one place.
        </Typography>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Completion Statistics</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Typography variant="body2" sx={{ mr: 1 }}>Overall Progress:</Typography>
                <LinearProgress 
                  variant="determinate" 
                  value={forms.length ? (stats?.completed / forms.length) * 100 : 0} 
                  sx={{ flexGrow: 1 }}
                />
                <Typography variant="body2" sx={{ ml: 1 }}>
                  {forms.length ? Math.round((stats?.completed / forms.length) * 100) : 0}%
                </Typography>
              </Box>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={4}>
                  <Typography variant="h4" align="center">{stats?.completed || 0}</Typography>
                  <Typography variant="body2" align="center" color="text.secondary">Completed</Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="h4" align="center">{stats?.inProgress || 0}</Typography>
                  <Typography variant="body2" align="center" color="text.secondary">In Progress</Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="h4" align="center">{stats?.draft || 0}</Typography>
                  <Typography variant="body2" align="center" color="text.secondary">Drafts</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Quick Actions</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                <Button 
                  variant="outlined" 
                  startIcon={<Add />}
                  component={RouterLink}
                  to="/forms"
                >
                  Start New Form
                </Button>
                <Button 
                  variant="outlined" 
                  startIcon={<Assignment />}
                  onClick={() => {
                    const inProgressForm = forms.find(form => form.status === 'in_progress');
                    if (inProgressForm) {
                      handleContinueForm(inProgressForm);
                    } else {
                      navigate('/forms');
                    }
                  }}
                >
                  Continue Form
                </Button>
                <Button 
                  variant="outlined" 
                  startIcon={<AssignmentTurnedIn />}
                  component={RouterLink}
                  to="/documents"
                >
                  View Documents
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper elevation={2} sx={{ p: 2, mb: 4 }}>
        <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="All Forms" />
            <Tab label="Completed" />
            <Tab label="In Progress" />
            <Tab label="Drafts" />
          </Tabs>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              placeholder="Search forms..."
              size="small"
              value={searchTerm}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
            <IconButton>
              <FilterList />
            </IconButton>
            <IconButton onClick={() => handleSort('updatedAt')}>
              <Sort />
            </IconButton>
          </Box>
        </Box>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : paginatedForms.length === 0 ? (
          <Alert severity="info">
            No forms found. <RouterLink to="/forms">Create your first form</RouterLink>.
          </Alert>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Form Name</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Last Updated</TableCell>
                  <TableCell>Completion</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {paginatedForms.map(form => (
                  <TableRow key={form.id}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <DescriptionOutlined sx={{ mr: 1, color: 'primary.main' }} />
                        {form.title}
                      </Box>
                    </TableCell>
                    <TableCell>
                      <StatusChip status={form.status} />
                    </TableCell>
                    <TableCell>
                      {format(new Date(form.updatedAt), 'MMM d, yyyy h:mm a')}
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={form.completionPercentage} 
                          sx={{ width: '100px', mr: 1 }}
                        />
                        <Typography variant="body2">{form.completionPercentage}%</Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <Tooltip title="View">
                          <IconButton size="small" onClick={() => handleView(form.id)}>
                            <Visibility />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Download">
                          <IconButton size="small" onClick={() => handleDownload(form.id)}>
                            <GetApp />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Edit">
                          <IconButton size="small" onClick={() => handleEdit(form.id, form.type)}>
                            <Edit />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Duplicate">
                          <IconButton size="small" onClick={() => handleDuplicate(form.id)}>
                            <FileCopy />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete">
                          <IconButton size="small" onClick={() => handleDeleteForm(form)}>
                            <Delete />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      <Menu
        anchorEl={menuAnchorEl}
        open={Boolean(menuAnchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => handleContinueForm(selectedForm)}>
          <Edit sx={{ mr: 1 }} /> Continue Editing
        </MenuItem>
        <MenuItem onClick={() => handleAnalyticsOpen(selectedForm)}>
          <Assessment sx={{ mr: 1 }} /> View Analytics
        </MenuItem>
        <MenuItem onClick={() => handleDeleteForm(selectedForm)}>
          <Delete sx={{ mr: 1 }} /> Delete
        </MenuItem>
      </Menu>

      {renderAnalyticsDialog()}

      {/* Filters */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              label="Search Forms"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} />
              }}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              select
              label="Status"
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <MenuItem value="all">All Status</MenuItem>
              <MenuItem value="completed">Completed</MenuItem>
              <MenuItem value="in_progress">In Progress</MenuItem>
              <MenuItem value="draft">Draft</MenuItem>
              <MenuItem value="error">Error</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              select
              label="Form Type"
              value={filters.type}
              onChange={(e) => handleFilterChange('type', e.target.value)}
            >
              <MenuItem value="all">All Types</MenuItem>
              <MenuItem value="small_claims">Small Claims</MenuItem>
              <MenuItem value="fee_waiver">Fee Waiver</MenuItem>
              <MenuItem value="eviction_response">Eviction Response</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              fullWidth
              select
              label="Date Range"
              value={filters.dateRange}
              onChange={(e) => handleFilterChange('dateRange', e.target.value)}
            >
              <MenuItem value="all">All Time</MenuItem>
              <MenuItem value="week">Last Week</MenuItem>
              <MenuItem value="month">Last Month</MenuItem>
              <MenuItem value="quarter">Last Quarter</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Paper>

      {/* Forms Table */}
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Form Title</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Progress</TableCell>
                <TableCell>Last Modified</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedForms.map((form) => (
                <TableRow key={form.id}>
                  <TableCell>{form.title}</TableCell>
                  <TableCell>
                    <Chip
                      label={form.type.replace('_', ' ').toUpperCase()}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{getStatusChip(form.status)}</TableCell>
                  <TableCell>
                    <Box display="flex" alignItems="center">
                      <LinearProgress
                        variant="determinate"
                        value={form.completionPercentage}
                        sx={{ flexGrow: 1, mr: 1 }}
                      />
                      <Typography variant="body2">
                        {form.completionPercentage}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    {format(new Date(form.updatedAt), 'PPp')}
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="View">
                      <IconButton
                        size="small"
                        onClick={() => handleView(form.id)}
                      >
                        <Visibility />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Download">
                      <IconButton
                        size="small"
                        onClick={() => handleDownload(form.id)}
                      >
                        <GetApp />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Edit">
                      <IconButton
                        size="small"
                        onClick={() => handleEdit(form.id, form.type)}
                      >
                        <Edit />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete">
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteForm(form)}
                      >
                        <Delete />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={sortedForms.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </Container>
  );
};

export default FormsDashboard; 
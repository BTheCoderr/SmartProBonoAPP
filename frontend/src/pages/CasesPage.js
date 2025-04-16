import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  TextField,
  InputAdornment,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Button,
  Chip,
  Paper,
  Tabs,
  Tab,
  Divider,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
// Icons
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';
import AddIcon from '@mui/icons-material/Add';
import SortIcon from '@mui/icons-material/Sort';
import ClearAllIcon from '@mui/icons-material/ClearAll';
// Components
import CaseCard from '../components/CaseCard';
// Data
import {
  CASE_STATUS,
  CASE_TYPES,
  PRIORITY_LEVELS,
  getStatusLabel,
  getCaseTypeLabel,
  getPriorityLabel,
} from '../data/casesData';
// Services
import { getAllCases } from '../services/caseService';
const CasesPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  // State
  const [cases, setCases] = useState([]);
  const [filteredCases, setFilteredCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [sortBy, setSortBy] = useState('updated_desc');
  const [tabValue, setTabValue] = useState(0);
  // Tabs for different case views
  const tabs = [
    { label: 'All Cases', value: 'all' },
    { label: 'Active', value: 'active' },
    { label: 'Pending Action', value: 'pending' },
    { label: 'Closed', value: 'closed' },
  ];
  // Load cases data
  useEffect(() => {
    const fetchCases = async () => {
      setLoading(true);
      setError(null);
      try {
        const casesData = await getAllCases();
        setCases(casesData);
      } catch (err) {
        console.error('Error fetching cases:', err);
        setError('Failed to fetch cases. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    fetchCases();
  }, []);
  // Filter and sort cases based on current filters
  useEffect(() => {
    if (cases.length === 0) return;
    let filtered = [...cases];
    // Apply tab filtering
    if (tabValue > 0) {
      const tabFilter = tabs[tabValue].value;
      switch (tabFilter) {
        case 'active':
          filtered = filtered.filter(
            c => c.status === CASE_STATUS.IN_PROGRESS || c.status === CASE_STATUS.NEW
          );
          break;
        case 'pending':
          filtered = filtered.filter(
            c => c.status === CASE_STATUS.PENDING_CLIENT || c.status === CASE_STATUS.PENDING_COURT
          );
          break;
        case 'closed':
          filtered = filtered.filter(
            c => c.status === CASE_STATUS.RESOLVED || c.status === CASE_STATUS.CLOSED
          );
          break;
        default:
          break;
      }
    }
    // Apply status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(c => c.status === statusFilter);
    }
    // Apply type filter
    if (typeFilter !== 'all') {
      filtered = filtered.filter(c => c.type === typeFilter);
    }
    // Apply priority filter
    if (priorityFilter !== 'all') {
      filtered = filtered.filter(c => c.priority === priorityFilter);
    }
    // Apply search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(
        c =>
          c.title.toLowerCase().includes(term) ||
          c.description.toLowerCase().includes(term) ||
          c.client.name.toLowerCase().includes(term) ||
          (c.assignedTo && c.assignedTo.name.toLowerCase().includes(term))
      );
    }
    // Apply sorting
    switch (sortBy) {
      case 'updated_desc':
        filtered.sort((a, b) => new Date(b.updated) - new Date(a.updated));
        break;
      case 'updated_asc':
        filtered.sort((a, b) => new Date(a.updated) - new Date(b.updated));
        break;
      case 'created_desc':
        filtered.sort((a, b) => new Date(b.created) - new Date(a.created));
        break;
      case 'created_asc':
        filtered.sort((a, b) => new Date(a.created) - new Date(b.created));
        break;
      case 'priority_desc':
        filtered.sort((a, b) => {
          const priorityOrder = {
            [PRIORITY_LEVELS.URGENT]: 3,
            [PRIORITY_LEVELS.HIGH]: 2,
            [PRIORITY_LEVELS.MEDIUM]: 1,
            [PRIORITY_LEVELS.LOW]: 0,
          };
          return priorityOrder[b.priority] - priorityOrder[a.priority];
        });
        break;
      default:
        break;
    }
    setFilteredCases(filtered);
  }, [cases, searchTerm, statusFilter, typeFilter, priorityFilter, sortBy, tabValue, tabs]);
  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  // Handle search input change
  const handleSearchChange = e => {
    setSearchTerm(e.target.value);
  };
  // Handle filter changes
  const handleStatusFilterChange = e => {
    setStatusFilter(e.target.value);
  };
  const handleTypeFilterChange = e => {
    setTypeFilter(e.target.value);
  };
  const handlePriorityFilterChange = e => {
    setPriorityFilter(e.target.value);
  };
  const handleSortChange = e => {
    setSortBy(e.target.value);
  };
  // Clear all filters
  const handleClearFilters = () => {
    setSearchTerm('');
    setStatusFilter('all');
    setTypeFilter('all');
    setPriorityFilter('all');
    setSortBy('updated_desc');
    setTabValue(0);
  };
  // Navigate to create new case
  const handleCreateNewCase = () => {
    navigate('/cases/new');
  };
  // Show loading spinner while data is loading
  if (loading) {
    return (
      <Box>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              {t('Loading cases...')}
            </Typography>
          </Box>
        </Container>
      </Box>
    );
  }
  // Show error message if there was a problem loading cases
  if (error) {
    return (
      <Box>
        <Container maxWidth="lg">
          <Box sx={{ mt: 4, mb: 8 }}>
            <Typography variant="h4" component="h1" sx={{ mb: 3 }}>
              {t('Legal Cases')}
            </Typography>
            <Alert severity="error" sx={{ mb: 3 }}>
              <Typography variant="subtitle1">{t('Error loading cases')}</Typography>
              <Typography variant="body2">{error}</Typography>
            </Alert>
            <Button variant="contained" startIcon={<AddIcon />} onClick={handleCreateNewCase}>
              {t('Create New Case')}
            </Button>
          </Box>
        </Container>
      </Box>
    );
  }
  return (
    <Box>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            {t('Legal Cases')}
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleCreateNewCase}>
            {t('Create New Case')}
          </Button>
        </Box>
        <Paper sx={{ mb: 4 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="case status tabs"
          >
            {tabs.map((tab, index) => (
              <Tab key={tab.value} label={t(tab.label)} id={`tab-${index}`} />
            ))}
          </Tabs>
        </Paper>
        <Paper sx={{ mb: 4, p: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder={t('Search cases...')}
                value={searchTerm}
                onChange={handleSearchChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="status-filter-label">{t('Status')}</InputLabel>
                <Select
                  labelId="status-filter-label"
                  value={statusFilter}
                  onChange={handleStatusFilterChange}
                  label={t('Status')}
                >
                  <MenuItem value="all">{t('All Statuses')}</MenuItem>
                  {Object.values(CASE_STATUS).map(status => (
                    <MenuItem key={status} value={status}>
                      {getStatusLabel(status)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="type-filter-label">{t('Case Type')}</InputLabel>
                <Select
                  labelId="type-filter-label"
                  value={typeFilter}
                  onChange={handleTypeFilterChange}
                  label={t('Case Type')}
                >
                  <MenuItem value="all">{t('All Types')}</MenuItem>
                  {Object.values(CASE_TYPES).map(type => (
                    <MenuItem key={type} value={type}>
                      {getCaseTypeLabel(type)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="priority-filter-label">{t('Priority')}</InputLabel>
                <Select
                  labelId="priority-filter-label"
                  value={priorityFilter}
                  onChange={handlePriorityFilterChange}
                  label={t('Priority')}
                >
                  <MenuItem value="all">{t('All Priorities')}</MenuItem>
                  {Object.values(PRIORITY_LEVELS).map(priority => (
                    <MenuItem key={priority} value={priority}>
                      {getPriorityLabel(priority)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="sort-label">{t('Sort By')}</InputLabel>
                <Select
                  labelId="sort-label"
                  value={sortBy}
                  onChange={handleSortChange}
                  label={t('Sort By')}
                  startAdornment={
                    <InputAdornment position="start">
                      <SortIcon fontSize="small" />
                    </InputAdornment>
                  }
                >
                  <MenuItem value="updated_desc">{t('Last Updated')} ↓</MenuItem>
                  <MenuItem value="updated_asc">{t('Last Updated')} ↑</MenuItem>
                  <MenuItem value="created_desc">{t('Date Created')} ↓</MenuItem>
                  <MenuItem value="created_asc">{t('Date Created')} ↑</MenuItem>
                  <MenuItem value="priority_desc">{t('Priority')} ↓</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
          {(searchTerm ||
            statusFilter !== 'all' ||
            typeFilter !== 'all' ||
            priorityFilter !== 'all' ||
            tabValue > 0) && (
            <Box display="flex" alignItems="center" mt={2}>
              <FilterListIcon fontSize="small" sx={{ mr: 1 }} />
              <Typography variant="body2" sx={{ mr: 2 }}>
                {t('Active filters:')}
              </Typography>
              {tabValue > 0 && (
                <Chip
                  label={`${tabs[tabValue].label}`}
                  size="small"
                  onDelete={() => setTabValue(0)}
                  sx={{ mr: 1 }}
                />
              )}
              {searchTerm && (
                <Chip
                  label={`${t('Search')}: ${searchTerm}`}
                  size="small"
                  onDelete={() => setSearchTerm('')}
                  sx={{ mr: 1 }}
                />
              )}
              {statusFilter !== 'all' && (
                <Chip
                  label={`${t('Status')}: ${getStatusLabel(statusFilter)}`}
                  size="small"
                  onDelete={() => setStatusFilter('all')}
                  sx={{ mr: 1 }}
                />
              )}
              {typeFilter !== 'all' && (
                <Chip
                  label={`${t('Type')}: ${getCaseTypeLabel(typeFilter)}`}
                  size="small"
                  onDelete={() => setTypeFilter('all')}
                  sx={{ mr: 1 }}
                />
              )}
              {priorityFilter !== 'all' && (
                <Chip
                  label={`${t('Priority')}: ${getPriorityLabel(priorityFilter)}`}
                  size="small"
                  onDelete={() => setPriorityFilter('all')}
                  sx={{ mr: 1 }}
                />
              )}
              <Button
                variant="outlined"
                size="small"
                startIcon={<ClearAllIcon />}
                onClick={handleClearFilters}
                sx={{ ml: 'auto' }}
              >
                {t('Clear All')}
              </Button>
            </Box>
          )}
        </Paper>
        {filteredCases.length === 0 ? (
          <Alert severity="info" sx={{ my: 4 }}>
            <Typography variant="subtitle1">{t('No cases found')}</Typography>
            <Typography variant="body2">
              {t('Try adjusting your search or filter criteria, or create a new case.')}
            </Typography>
          </Alert>
        ) : (
          <>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                {t('Showing')} {filteredCases.length}{' '}
                {filteredCases.length === 1 ? t('case') : t('cases')}
              </Typography>
            </Box>
            <Box>
              {filteredCases.map(caseItem => (
                <CaseCard key={caseItem.id} caseData={caseItem} />
              ))}
            </Box>
          </>
        )}
      </Container>
    </Box>
  );
};
export default CasesPage;
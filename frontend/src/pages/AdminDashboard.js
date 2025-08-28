import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Tabs,
  Tab,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Menu,
  MenuItem,
  Badge
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import SecurityIcon from '@mui/icons-material/Security';
import GroupIcon from '@mui/icons-material/Group';
import GavelIcon from '@mui/icons-material/Gavel';
import DescriptionIcon from '@mui/icons-material/Description';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';
import AssignmentIcon from '@mui/icons-material/Assignment';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import NotificationsIcon from '@mui/icons-material/Notifications';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

// Mock data for users - in a real app this would come from an API
const mockUsers = [
  { id: 1, username: 'johnsmith', email: 'john@example.com', role: 'client', active: true, created_at: '2023-08-15T12:00:00Z' },
  { id: 2, username: 'sarahjones', email: 'sarah@example.com', role: 'lawyer', active: true, created_at: '2023-09-20T10:30:00Z' },
  { id: 3, username: 'mikebrown', email: 'mike@example.com', role: 'client', active: false, created_at: '2023-07-05T09:15:00Z' },
  { id: 4, username: 'emilydavis', email: 'emily@example.com', role: 'admin', active: true, created_at: '2023-06-10T14:45:00Z' },
  { id: 5, username: 'alexwilson', email: 'alex@example.com', role: 'client', active: true, created_at: '2023-10-25T11:20:00Z' }
];

// Stats cards data
const statsCardsData = [
  { title: 'Total Users', value: 153, icon: <PersonIcon fontSize="large" color="primary" /> },
  { title: 'Active Lawyers', value: 28, icon: <GavelIcon fontSize="large" color="success" /> },
  { title: 'Active Cases', value: 47, icon: <DescriptionIcon fontSize="large" color="warning" /> },
  { title: 'New Users (Last 30d)', value: 21, icon: <GroupIcon fontSize="large" color="info" /> }
];

const AdminDashboard = () => {
  const { currentUser } = useAuth();
  const [users, setUsers] = useState(mockUsers);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState(null);
  const [actionAnchorEl, setActionAnchorEl] = useState(null);
  const [selectedCase, setSelectedCase] = useState(null);
  const [assignDialogOpen, setAssignDialogOpen] = useState(false);
  const [statusDialogOpen, setStatusDialogOpen] = useState(false);
  const [notesDialogOpen, setNotesDialogOpen] = useState(false);
  const [activeFilters, setActiveFilters] = useState([]);
  const [selectedCaseId, setSelectedCaseId] = useState(null);

  // Mock data - would normally come from API
  const [casesData, setCasesData] = useState({
    new: [
      { 
        id: 'case-001', 
        clientName: 'John Smith', 
        caseType: 'Expungement', 
        status: 'New',
        submittedDate: '2023-06-15', 
        priority: 'Medium',
        documents: 3
      },
      { 
        id: 'case-002', 
        clientName: 'Maria Rodriguez', 
        caseType: 'Housing Defense', 
        status: 'New',
        submittedDate: '2023-06-17', 
        priority: 'High',
        documents: 2
      },
      { 
        id: 'case-003', 
        clientName: 'David Johnson', 
        caseType: 'Fee Waiver', 
        status: 'New',
        submittedDate: '2023-06-18', 
        priority: 'Low',
        documents: 1
      }
    ],
    active: [
      { 
        id: 'case-004', 
        clientName: 'Susan Taylor', 
        caseType: 'Housing Defense', 
        status: 'In Progress',
        submittedDate: '2023-06-10', 
        assignedTo: 'Jane Lawyer',
        lastUpdated: '2023-06-16',
        priority: 'High',
        documents: 4
      },
      { 
        id: 'case-005', 
        clientName: 'Robert Brown', 
        caseType: 'Expungement', 
        status: 'Under Review',
        submittedDate: '2023-06-12', 
        assignedTo: 'Mike Attorney',
        lastUpdated: '2023-06-17',
        priority: 'Medium',
        documents: 3
      }
    ],
    completed: [
      { 
        id: 'case-006', 
        clientName: 'Emily Wilson', 
        caseType: 'Fee Waiver', 
        status: 'Completed',
        submittedDate: '2023-06-05', 
        completedDate: '2023-06-15',
        assignedTo: 'Jane Lawyer',
        priority: 'Medium',
        documents: 2
      },
      { 
        id: 'case-007', 
        clientName: 'Michael Garcia', 
        caseType: 'Expungement', 
        status: 'Completed',
        submittedDate: '2023-06-02', 
        completedDate: '2023-06-14',
        assignedTo: 'Mike Attorney',
        priority: 'Low',
        documents: 3
      }
    ]
  });

  // Mock list of available attorneys
  const attorneys = [
    { id: 'atty-001', name: 'Jane Lawyer', specialization: 'Housing' },
    { id: 'atty-002', name: 'Mike Attorney', specialization: 'Criminal' },
    { id: 'atty-003', name: 'Sarah Counsel', specialization: 'Family Law' },
    { id: 'atty-004', name: 'Robert Legal', specialization: 'Immigration' }
  ];

  // Filters
  const filterOptions = [
    { label: 'High Priority', value: 'high-priority' },
    { label: 'Expungement Cases', value: 'expungement' },
    { label: 'Housing Cases', value: 'housing' },
    { label: 'Fee Waiver Cases', value: 'fee-waiver' },
    { label: 'Newest First', value: 'newest' },
    { label: 'Oldest First', value: 'oldest' }
  ];

  // In a real application, you would fetch users from your API
  useEffect(() => {
    // Simulating API call
    setLoading(true);
    setTimeout(() => {
      setUsers(mockUsers);
      setLoading(false);
    }, 1000);

    // Real API call would look like:
    // const fetchUsers = async () => {
    //   try {
    //     setLoading(true);
    //     const response = await axios.get('/api/admin/users');
    //     setUsers(response.data.users);
    //   } catch (error) {
    //     setError('Failed to load users');
    //     console.error(error);
    //   } finally {
    //     setLoading(false);
    //   }
    // };
    // fetchUsers();
  }, []);

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleFilterClick = (event) => {
    setFilterAnchorEl(event.currentTarget);
  };

  const handleFilterClose = () => {
    setFilterAnchorEl(null);
  };

  const handleActionClick = (event, caseId) => {
    setActionAnchorEl(event.currentTarget);
    setSelectedCaseId(caseId);
  };

  const handleActionClose = () => {
    setActionAnchorEl(null);
    setSelectedCaseId(null);
  };

  const handleAssignClick = () => {
    setAssignDialogOpen(true);
    handleActionClose();
  };

  const handleStatusClick = () => {
    setStatusDialogOpen(true);
    handleActionClose();
  };

  const handleNotesClick = () => {
    setNotesDialogOpen(true);
    handleActionClose();
  };

  const handleFilterSelect = (filter) => {
    if (activeFilters.includes(filter)) {
      setActiveFilters(activeFilters.filter(f => f !== filter));
    } else {
      setActiveFilters([...activeFilters, filter]);
    }
    handleFilterClose();
  };

  const handleAssignCase = (attorneyId) => {
    // Mock implementation - would normally call API
    const attorneyName = attorneys.find(a => a.id === attorneyId)?.name;
    
    if (tabValue === 0 && selectedCaseId) {
      // Move case from new to active
      const caseToMove = casesData.new.find(c => c.id === selectedCaseId);
      if (caseToMove) {
        const updatedCase = {
          ...caseToMove,
          status: 'Assigned',
          assignedTo: attorneyName,
          lastUpdated: new Date().toISOString().split('T')[0]
        };
        
        setCasesData({
          ...casesData,
          new: casesData.new.filter(c => c.id !== selectedCaseId),
          active: [...casesData.active, updatedCase]
        });
      }
    } else if (tabValue === 1 && selectedCaseId) {
      // Update assignee in active cases
      setCasesData({
        ...casesData,
        active: casesData.active.map(c => 
          c.id === selectedCaseId 
            ? { ...c, assignedTo: attorneyName, lastUpdated: new Date().toISOString().split('T')[0] } 
            : c
        )
      });
    }
    
    setAssignDialogOpen(false);
  };

  const handleUpdateStatus = (newStatus) => {
    // Mock implementation - would normally call API
    if (tabValue === 1 && selectedCaseId) {
      if (newStatus === 'Completed') {
        // Move from active to completed
        const caseToMove = casesData.active.find(c => c.id === selectedCaseId);
        if (caseToMove) {
          const updatedCase = {
            ...caseToMove,
            status: 'Completed',
            completedDate: new Date().toISOString().split('T')[0]
          };
          
          setCasesData({
            ...casesData,
            active: casesData.active.filter(c => c.id !== selectedCaseId),
            completed: [...casesData.completed, updatedCase]
          });
        }
      } else {
        // Update status in active cases
        setCasesData({
          ...casesData,
          active: casesData.active.map(c => 
            c.id === selectedCaseId 
              ? { ...c, status: newStatus, lastUpdated: new Date().toISOString().split('T')[0] } 
              : c
          )
        });
      }
    }
    
    setStatusDialogOpen(false);
  };

  // Filter cases based on search term and active filters
  const filterCases = (cases) => {
    if (!cases) return [];
    
    return cases.filter(c => {
      // Search filter
      const matchesSearch = searchTerm === '' || 
        c.clientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.id.toLowerCase().includes(searchTerm.toLowerCase());
      
      // Apply additional filters
      let matchesFilters = true;
      
      if (activeFilters.includes('high-priority')) {
        matchesFilters = matchesFilters && c.priority === 'High';
      }
      
      if (activeFilters.includes('expungement')) {
        matchesFilters = matchesFilters && c.caseType === 'Expungement';
      }
      
      if (activeFilters.includes('housing')) {
        matchesFilters = matchesFilters && c.caseType === 'Housing Defense';
      }
      
      if (activeFilters.includes('fee-waiver')) {
        matchesFilters = matchesFilters && c.caseType === 'Fee Waiver';
      }
      
      return matchesSearch && matchesFilters;
    }).sort((a, b) => {
      if (activeFilters.includes('newest')) {
        return new Date(b.submittedDate) - new Date(a.submittedDate);
      }
      
      if (activeFilters.includes('oldest')) {
        return new Date(a.submittedDate) - new Date(b.submittedDate);
      }
      
      return 0;
    });
  };

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'new':
        return 'info';
      case 'assigned':
      case 'in progress':
        return 'primary';
      case 'under review':
        return 'warning';
      case 'completed':
        return 'success';
      default:
        return 'default';
    }
  };

  const renderCaseTable = (cases) => (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Case ID</TableCell>
            <TableCell>Client Name</TableCell>
            <TableCell>Case Type</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Date</TableCell>
            {tabValue !== 0 && <TableCell>Assigned To</TableCell>}
            <TableCell>Priority</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {cases.map((caseItem) => (
            <TableRow key={caseItem.id}>
              <TableCell>{caseItem.id}</TableCell>
              <TableCell>{caseItem.clientName}</TableCell>
              <TableCell>{caseItem.caseType}</TableCell>
              <TableCell>
                <Chip 
                  label={caseItem.status} 
                  size="small" 
                  color={getStatusColor(caseItem.status)}
                />
              </TableCell>
              <TableCell>
                {tabValue === 0 && caseItem.submittedDate}
                {tabValue === 1 && caseItem.lastUpdated}
                {tabValue === 2 && caseItem.completedDate}
              </TableCell>
              {tabValue !== 0 && <TableCell>{caseItem.assignedTo}</TableCell>}
              <TableCell>
                <Chip 
                  label={caseItem.priority} 
                  size="small" 
                  color={getPriorityColor(caseItem.priority)}
                />
              </TableCell>
              <TableCell>
                <IconButton
                  aria-label="case actions"
                  onClick={(e) => handleActionClick(e, caseItem.id)}
                >
                  <MoreVertIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
          {cases.length === 0 && (
            <TableRow>
              <TableCell colSpan={tabValue !== 0 ? 8 : 7} align="center">
                <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
                  No cases found
                </Typography>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );

  const renderTabContent = () => {
    switch (tabValue) {
      case 0:
        return renderCaseTable(filterCases(casesData.new));
      case 1:
        return renderCaseTable(filterCases(casesData.active));
      case 2:
        return renderCaseTable(filterCases(casesData.completed));
      default:
        return null;
    }
  };

  if (!currentUser || currentUser.role !== 'admin') {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">
          You do not have permission to access this page. This area is restricted to administrators.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5" component="h1" gutterBottom>
            Admin Dashboard
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<PersonAddIcon />}
            >
              Add Attorney
            </Button>
            <IconButton color="primary">
              <Badge badgeContent={4} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Box>
        </Box>

        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <AssignmentIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
                  <Box>
                    <Typography variant="h5">{casesData.new.length}</Typography>
                    <Typography variant="body2" color="text.secondary">New Cases</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <AssignmentIndIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
                  <Box>
                    <Typography variant="h5">{casesData.active.length}</Typography>
                    <Typography variant="body2" color="text.secondary">Active Cases</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <AssignmentTurnedInIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
                  <Box>
                    <Typography variant="h5">{casesData.completed.length}</Typography>
                    <Typography variant="body2" color="text.secondary">Completed Cases</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Box sx={{ mb: 3 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label={`New Cases (${casesData.new.length})`} id="tab-0" />
            <Tab label={`Active Cases (${casesData.active.length})`} id="tab-1" />
            <Tab label={`Completed Cases (${casesData.completed.length})`} id="tab-2" />
          </Tabs>
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <TextField
            placeholder="Search cases..."
            variant="outlined"
            size="small"
            value={searchTerm}
            onChange={handleSearch}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ width: '40%' }}
          />
          <Box>
            {activeFilters.map((filter) => (
              <Chip
                key={filter}
                label={filterOptions.find(f => f.value === filter)?.label}
                onDelete={() => handleFilterSelect(filter)}
                sx={{ mr: 1 }}
                size="small"
              />
            ))}
            <Button
              startIcon={<FilterListIcon />}
              onClick={handleFilterClick}
              variant="outlined"
              size="small"
            >
              Filter
            </Button>
          </Box>
        </Box>

        {renderTabContent()}
      </Paper>

      {/* Filter Menu */}
      <Menu
        anchorEl={filterAnchorEl}
        open={Boolean(filterAnchorEl)}
        onClose={handleFilterClose}
      >
        {filterOptions.map((option) => (
          <MenuItem 
            key={option.value}
            onClick={() => handleFilterSelect(option.value)}
            selected={activeFilters.includes(option.value)}
          >
            {option.label}
          </MenuItem>
        ))}
      </Menu>

      {/* Actions Menu */}
      <Menu
        anchorEl={actionAnchorEl}
        open={Boolean(actionAnchorEl)}
        onClose={handleActionClose}
      >
        <MenuItem onClick={handleAssignClick}>
          <AssignmentIndIcon fontSize="small" sx={{ mr: 1 }} />
          Assign Case
        </MenuItem>
        {tabValue === 1 && (
          <MenuItem onClick={handleStatusClick}>
            <AssignmentTurnedInIcon fontSize="small" sx={{ mr: 1 }} />
            Update Status
          </MenuItem>
        )}
        <MenuItem onClick={handleNotesClick}>
          <AssignmentIcon fontSize="small" sx={{ mr: 1 }} />
          Add Notes
        </MenuItem>
      </Menu>

      {/* Assign Case Dialog */}
      <Dialog open={assignDialogOpen} onClose={() => setAssignDialogOpen(false)}>
        <DialogTitle>Assign Case</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Select an attorney to assign this case to:
          </Typography>
          <Grid container spacing={2}>
            {attorneys.map((attorney) => (
              <Grid item xs={12} key={attorney.id}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => handleAssignCase(attorney.id)}
                  sx={{ justifyContent: 'flex-start', textAlign: 'left' }}
                >
                  <Box>
                    <Typography variant="subtitle1">{attorney.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Specialization: {attorney.specialization}
                    </Typography>
                  </Box>
                </Button>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAssignDialogOpen(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Update Status Dialog */}
      <Dialog open={statusDialogOpen} onClose={() => setStatusDialogOpen(false)}>
        <DialogTitle>Update Case Status</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Select a new status for this case:
          </Typography>
          <Grid container spacing={2}>
            {['Assigned', 'In Progress', 'Under Review', 'Completed'].map((status) => (
              <Grid item xs={12} sm={6} key={status}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => handleUpdateStatus(status)}
                >
                  {status}
                </Button>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setStatusDialogOpen(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Add Notes Dialog */}
      <Dialog open={notesDialogOpen} onClose={() => setNotesDialogOpen(false)}>
        <DialogTitle>Add Case Notes</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Case Notes"
            fullWidth
            multiline
            rows={4}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNotesDialogOpen(false)}>Cancel</Button>
          <Button onClick={() => setNotesDialogOpen(false)} variant="contained">
            Save Notes
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AdminDashboard; 
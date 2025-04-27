import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  Alert,
  CircularProgress,
  Avatar,
  Badge,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Snackbar
} from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import AssignmentIcon from '@mui/icons-material/Assignment';
import EventIcon from '@mui/icons-material/Event';
import FlightIcon from '@mui/icons-material/Flight';
import PersonIcon from '@mui/icons-material/Person';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import config from '../config';
import { immigrationApi } from '../services/api';

// Mock data for cases - in a real app, this would come from an API
const mockCases = [
  { 
    id: 1, 
    title: 'Tenant Rights Dispute', 
    client: 'John Smith',
    client_id: 101,
    category: 'housing',
    status: 'active',
    priority: 'high',
    last_updated: '2024-04-10T14:30:00Z',
    description: 'Tenant facing potential eviction due to landlord neglect of property conditions.',
    upcoming_meeting: '2024-04-22T15:00:00Z'
  },
  { 
    id: 2, 
    title: 'Employment Contract Review', 
    client: 'Sarah Johnson',
    client_id: 102,
    category: 'employment',
    status: 'active',
    priority: 'medium',
    last_updated: '2024-04-12T09:45:00Z',
    description: 'Review of new employment contract for potential issues with non-compete clauses.',
    upcoming_meeting: null
  },
  { 
    id: 3, 
    title: 'Visa Application Support', 
    client: 'Carlos Rodriguez',
    client_id: 103,
    category: 'immigration',
    status: 'pending',
    priority: 'high',
    last_updated: '2024-04-05T11:20:00Z',
    description: 'Support with family visa application process and documentation.',
    upcoming_meeting: '2024-04-24T10:30:00Z'
  },
  { 
    id: 4, 
    title: 'Small Business Contract Preparation', 
    client: 'Lisa Chen',
    client_id: 104,
    category: 'contracts',
    status: 'active',
    priority: 'medium',
    last_updated: '2024-04-08T16:15:00Z',
    description: 'Preparing service contract for small web development business.',
    upcoming_meeting: '2024-04-26T13:45:00Z'
  },
  { 
    id: 5, 
    title: 'Housing Discrimination Case', 
    client: 'Michael Brown',
    client_id: 105,
    category: 'housing',
    status: 'closed',
    priority: 'low',
    last_updated: '2024-03-20T10:00:00Z',
    description: 'Housing discrimination case resolved through mediation.',
    upcoming_meeting: null
  }
];

// Mock data for immigration forms - in a real app, this would come from an API
const mockImmigrationForms = [
  {
    id: '1',
    firstName: 'Maria',
    lastName: 'Garcia',
    email: 'maria.garcia@example.com',
    phone: '555-123-4567',
    dateOfBirth: '1985-06-15',
    nationality: 'Mexican',
    currentImmigrationStatus: 'Visa Holder',
    desiredService: 'Green Card Application',
    createdAt: '2024-04-10T15:30:00Z',
    status: 'new'
  },
  {
    id: '2',
    firstName: 'Ahmed',
    lastName: 'Hassan',
    email: 'ahmed.hassan@example.com',
    phone: '555-234-5678',
    dateOfBirth: '1990-03-21',
    nationality: 'Egyptian',
    currentImmigrationStatus: 'Student Visa',
    desiredService: 'Employment-Based Immigration',
    createdAt: '2024-04-11T09:45:00Z',
    status: 'in-progress'
  },
  {
    id: '3',
    firstName: 'Li',
    lastName: 'Wei',
    email: 'li.wei@example.com',
    phone: '555-345-6789',
    dateOfBirth: '1975-11-08',
    nationality: 'Chinese',
    currentImmigrationStatus: 'Asylum Seeker',
    desiredService: 'Asylum/Refugee Status',
    createdAt: '2024-04-12T14:20:00Z',
    status: 'new'
  }
];

// Upcoming meetings for calendar section
const upcomingMeetings = mockCases
  .filter(c => c.upcoming_meeting)
  .map(c => ({
    id: c.id,
    title: c.title,
    client: c.client,
    datetime: c.upcoming_meeting,
    category: c.category
  }))
  .sort((a, b) => new Date(a.datetime) - new Date(b.datetime));

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;
  
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`dashboard-tabpanel-${index}`}
      aria-labelledby={`dashboard-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
};

const LawyerDashboard = () => {
  const { currentUser, accessToken } = useAuth();
  const [cases, setCases] = useState([]);
  const [immigrationForms, setImmigrationForms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  // Fetch data from API
  useEffect(() => {
    setLoading(true);
    
    const fetchData = async () => {
      try {
        // For now, using mock data for cases until we have a proper API endpoint
        setCases(mockCases);
        
        // Fetch immigration forms from API
        const forms = await immigrationApi.getIntakeForms(accessToken);
        setImmigrationForms(forms);
        
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message || 'An error occurred while fetching data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [accessToken]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleStatusUpdate = async (formId, newStatus) => {
    try {
      await immigrationApi.updateFormStatus(formId, newStatus, accessToken);
      
      // Update the form status in the local state
      setImmigrationForms(forms => forms.map(form => 
        form.id === formId || form._id === formId
          ? { ...form, status: newStatus }
          : form
      ));
      
      setNotification({
        open: true,
        message: 'Form status updated successfully',
        severity: 'success'
      });
    } catch (err) {
      console.error('Error updating form status:', err);
      setNotification({
        open: true,
        message: err.message || 'An error occurred while updating status',
        severity: 'error'
      });
    }
  };

  const handleCloseNotification = () => {
    setNotification({
      ...notification,
      open: false
    });
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const formatTime = (dateString) => {
    const options = { hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleTimeString(undefined, options);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'success';
      case 'pending': return 'warning';
      case 'closed': return 'default';
      case 'new': return 'info';
      case 'in-progress': return 'success';
      default: return 'default';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'housing': return '🏠';
      case 'employment': return '💼';
      case 'immigration': return '✈️';
      case 'contracts': return '📝';
      default: return '📄';
    }
  };

  // Filter active cases for the summary section
  const activeCases = cases.filter(c => c.status === 'active' || c.status === 'pending');
  const newImmigrationForms = immigrationForms.filter(form => form.status === 'new');

  if (!currentUser || currentUser.role !== 'lawyer') {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">
          You do not have permission to access this page. This area is restricted to lawyers.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Lawyer Dashboard
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Welcome back, {currentUser.first_name || currentUser.username}! Here's an overview of your cases.
        </Typography>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      ) : (
        <Box sx={{ width: '100%' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange} 
              aria-label="dashboard tabs"
              variant="scrollable"
              scrollButtons="auto"
            >
              <Tab 
                icon={<AssignmentIcon />} 
                iconPosition="start" 
                label="Active Cases" 
                id="dashboard-tab-0" 
                aria-controls="dashboard-tabpanel-0" 
              />
              <Tab 
                icon={<FlightIcon />} 
                iconPosition="start" 
                label={`Immigration Forms ${newImmigrationForms.length > 0 ? `(${newImmigrationForms.length})` : ''}`} 
                id="dashboard-tab-1" 
                aria-controls="dashboard-tabpanel-1" 
              />
              <Tab 
                icon={<EventIcon />} 
                iconPosition="start" 
                label="Calendar" 
                id="dashboard-tab-2" 
                aria-controls="dashboard-tabpanel-2" 
              />
            </Tabs>
          </Box>
          
          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={4}>
              {/* Left column - Case overview */}
              <Grid item xs={12} md={8}>
                <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
                  <Typography variant="h5" component="h2" gutterBottom>
                    <AssignmentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Active Cases ({activeCases.length})
                  </Typography>
                  
                  {activeCases.length === 0 ? (
                    <Alert severity="info">You have no active cases at the moment.</Alert>
                  ) : (
                    <Grid container spacing={3}>
                      {activeCases.map((caseItem) => (
                        <Grid item xs={12} key={caseItem.id}>
                          <Card variant="outlined">
                            <CardContent>
                              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                <Box>
                                  <Typography variant="h6">
                                    {getCategoryIcon(caseItem.category)} {caseItem.title}
                                  </Typography>
                                  <Typography variant="body2" color="text.secondary" gutterBottom>
                                    Client: {caseItem.client}
                                  </Typography>
                                </Box>
                                <Box>
                                  <Chip 
                                    label={caseItem.status.charAt(0).toUpperCase() + caseItem.status.slice(1)} 
                                    color={getStatusColor(caseItem.status)}
                                    size="small"
                                    sx={{ mr: 1 }}
                                  />
                                  <Chip 
                                    icon={<PriorityHighIcon />}
                                    label={caseItem.priority.charAt(0).toUpperCase() + caseItem.priority.slice(1)} 
                                    color={getPriorityColor(caseItem.priority)}
                                    size="small"
                                  />
                                </Box>
                              </Box>
                              
                              <Typography variant="body1" sx={{ my: 2 }}>
                                {caseItem.description}
                              </Typography>
                              
                              {caseItem.upcoming_meeting && (
                                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                                  <EventIcon fontSize="small" sx={{ mr: 1, color: 'primary.main' }} />
                                  <Typography variant="body2">
                                    Next meeting: {formatDate(caseItem.upcoming_meeting)} at {formatTime(caseItem.upcoming_meeting)}
                                  </Typography>
                                </Box>
                              )}
                            </CardContent>
                            <Divider />
                            <CardActions>
                              <Button size="small">View Details</Button>
                              <Button size="small">Add Document</Button>
                              <Button size="small">Schedule Meeting</Button>
                            </CardActions>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  )}
                </Paper>

                <Paper elevation={2} sx={{ p: 3 }}>
                  <Typography variant="h5" component="h2" gutterBottom>
                    <FolderIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Case Statistics
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} sm={4}>
                      <Card sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" color="primary">
                          {cases.filter(c => c.status === 'active').length}
                        </Typography>
                        <Typography variant="body2">Active Cases</Typography>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Card sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" color="warning.main">
                          {cases.filter(c => c.priority === 'high').length}
                        </Typography>
                        <Typography variant="body2">High Priority</Typography>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Card sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" color="success.main">
                          {cases.filter(c => c.status === 'closed').length}
                        </Typography>
                        <Typography variant="body2">Completed Cases</Typography>
                      </Card>
                    </Grid>
                  </Grid>
                </Paper>
              </Grid>

              {/* Right column - Calendar and info */}
              <Grid item xs={12} md={4}>
                <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
                  <Typography variant="h5" component="h2" sx={{ mb: 2 }}>
                    <EventIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Upcoming Meetings
                  </Typography>
                  
                  {upcomingMeetings.length === 0 ? (
                    <Alert severity="info">No upcoming meetings scheduled.</Alert>
                  ) : (
                    <List>
                      {upcomingMeetings.map((meeting, index) => (
                        <React.Fragment key={meeting.id}>
                          <ListItem alignItems="flex-start">
                            <Box sx={{ display: 'flex', alignItems: 'flex-start', width: '100%' }}>
                              <Avatar sx={{ 
                                bgcolor: 'primary.light', 
                                width: 40, 
                                height: 40, 
                                mr: 2, 
                                fontSize: '0.875rem' 
                              }}>
                                {formatDate(meeting.datetime).slice(0, 2)}
                              </Avatar>
                              <Box sx={{ width: '100%' }}>
                                <Typography variant="body1" fontWeight="medium">
                                  {formatTime(meeting.datetime)}
                                </Typography>
                                <Typography variant="body2">
                                  {meeting.title}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  Client: {meeting.client}
                                </Typography>
                              </Box>
                            </Box>
                          </ListItem>
                          {index < upcomingMeetings.length - 1 && <Divider component="li" />}
                        </React.Fragment>
                      ))}
                    </List>
                  )}
                  
                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
                    <Button variant="outlined" size="small">
                      View Full Calendar
                    </Button>
                  </Box>
                </Paper>

                <Paper elevation={2} sx={{ p: 3 }}>
                  <Typography variant="h5" component="h2" gutterBottom>
                    Quick Actions
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <Button 
                        variant="contained" 
                        fullWidth 
                        sx={{ justifyContent: 'flex-start', py: 1.5 }}
                      >
                        Create New Case
                      </Button>
                    </Grid>
                    <Grid item xs={12}>
                      <Button 
                        variant="outlined" 
                        fullWidth 
                        sx={{ justifyContent: 'flex-start', py: 1.5 }}
                      >
                        Schedule Meeting
                      </Button>
                    </Grid>
                    <Grid item xs={12}>
                      <Button 
                        variant="outlined" 
                        fullWidth 
                        sx={{ justifyContent: 'flex-start', py: 1.5 }}
                      >
                        Generate Document
                      </Button>
                    </Grid>
                  </Grid>
                </Paper>
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
              <Typography variant="h5" component="h2" gutterBottom>
                <FlightIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Immigration Intake Forms
              </Typography>
              
              {immigrationForms.length === 0 ? (
                <Alert severity="info">No immigration intake forms have been submitted yet.</Alert>
              ) : (
                <TableContainer>
                  <Table sx={{ minWidth: 650 }} aria-label="immigration forms table">
                    <TableHead>
                      <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Contact</TableCell>
                        <TableCell>Service</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Date Submitted</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {immigrationForms.map((form) => (
                        <TableRow key={form.id || form._id} hover>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                                <PersonIcon />
                              </Avatar>
                              <Box>
                                <Typography variant="subtitle2">
                                  {form.firstName} {form.lastName}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  {form.nationality}
                                </Typography>
                              </Box>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2">{form.email}</Typography>
                            <Typography variant="body2">{form.phone}</Typography>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2">{form.desiredService}</Typography>
                            <Typography variant="body2" color="text.secondary">
                              Status: {form.currentImmigrationStatus}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={form.status === 'new' ? 'New' : form.status === 'in-progress' ? 'In Progress' : 'Completed'} 
                              color={getStatusColor(form.status)}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {formatDate(form.createdAt)}
                          </TableCell>
                          <TableCell>
                            <Button 
                              variant="outlined" 
                              size="small" 
                              sx={{ mr: 1 }}
                              onClick={() => window.open(`/immigration/forms/${form.id || form._id}`, '_blank')}
                            >
                              View
                            </Button>
                            {form.status === 'new' ? (
                              <Button 
                                variant="contained" 
                                size="small"
                                onClick={() => handleStatusUpdate(form.id || form._id, 'in-progress')}
                              >
                                Assign
                              </Button>
                            ) : form.status === 'in-progress' ? (
                              <Button 
                                variant="contained" 
                                size="small"
                                onClick={() => handleStatusUpdate(form.id || form._id, 'completed')}
                              >
                                Complete
                              </Button>
                            ) : (
                              <Button 
                                variant="contained" 
                                size="small"
                                color="secondary"
                                onClick={() => handleStatusUpdate(form.id || form._id, 'archived')}
                              >
                                Archive
                              </Button>
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </Paper>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            {/* Calendar Tab Content */}
            <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
              <Typography variant="h5" component="h2" gutterBottom>
                <EventIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Upcoming Meetings
              </Typography>
              
              <List>
                {upcomingMeetings.length === 0 ? (
                  <Alert severity="info">No upcoming meetings scheduled.</Alert>
                ) : (
                  upcomingMeetings.map((meeting) => (
                    <React.Fragment key={meeting.id}>
                      <ListItem>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Typography variant="subtitle1">
                                {getCategoryIcon(meeting.category)} {meeting.title}
                              </Typography>
                            </Box>
                          }
                          secondary={
                            <>
                              <Typography variant="body2">
                                Client: {meeting.client}
                              </Typography>
                              <Typography variant="body2">
                                {formatDate(meeting.datetime)} at {formatTime(meeting.datetime)}
                              </Typography>
                            </>
                          }
                        />
                        <Button size="small" variant="outlined">Reschedule</Button>
                      </ListItem>
                      <Divider component="li" />
                    </React.Fragment>
                  ))
                )}
              </List>
            </Paper>
          </TabPanel>
        </Box>
      )}

      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity}
          variant="filled"
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default LawyerDashboard; 
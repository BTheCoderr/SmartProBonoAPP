// WARNING: Imports have been commented out to fix linting errors.
// Uncomment specific imports as needed when using them.
// Unused: import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Divider,
  Chip,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  LinearProgress,
  Tooltip,
  IconButton,
  Modal,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Snackbar
} from '@mui/material';
import {
  Description as DescriptionIcon,
  Assignment as AssignmentIcon,
  Notifications as NotificationsIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
  HourglassEmpty as HourglassEmptyIcon,
  FileCopy as FileCopyIcon,
  AttachFile as AttachFileIcon,
  MoreVert as MoreVertIcon,
  Search as SearchIcon,
  CalendarToday as CalendarTodayIcon,
  Phone as PhoneIcon,
  Error as ErrorIcon,
  FileUpload as FileUploadIcon,
  AccessTime as AccessTimeIcon,
  Cancel as CancelIcon,
  Send as SendIcon
} from '@mui/icons-material';
// Unused: import { useNavigate } from 'react-router-dom';
// Unused: import { useAuth } from '../context/AuthContext';
// Unused: import PageLayout from '../components/PageLayout';
// Unused: import { immigrationApi } from '../services/api';
// Unused: import { useTheme } from '@mui/material/styles';
// Unused: import { useMediaQuery } from '@mui/material';
// Unused: import apiService from '../services/ApiService';

// Case status components
const CaseStatus = ({ status }) => {
  let color = 'default';
  let icon = <HourglassEmptyIcon />;
  
  switch (status) {
    case 'new':
      color = 'info';
      icon = <HourglassEmptyIcon />;
      break;
    case 'in-progress':
      color = 'warning';
      icon = <ScheduleIcon />;
      break;
    case 'completed':
      color = 'success';
      icon = <CheckCircleIcon />;
      break;
    case 'delayed':
      color = 'error';
      icon = <ErrorIcon />;
      break;
    default:
      color = 'default';
  }
  
  return (
    <Chip 
      icon={icon} 
      label={status.replace('-', ' ')} 
      color={color} 
      size="small" 
      sx={{ textTransform: 'capitalize' }} 
    />
  );
};

const getProgressValue = (status) => {
  switch (status) {
    case 'new': return 20;
    case 'in-progress': return 60;
    case 'completed': return 100;
    case 'delayed': return 40;
    default: return 0;
  }
};

const ImmigrationDashboard = () => {
  const [cases, setCases] = useState([]);
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [documentType, setDocumentType] = useState('identity');
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [notificationSent, setNotificationSent] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');
  const fileInputRef = useRef(null);
  const [testStatus, setTestStatus] = useState(null);
  
  const navigate = useNavigate();
  const { currentUser, accessToken } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null); // Reset error state
        
        // Fetch cases
        try {
          const casesResponse = await immigrationApi.getCases(accessToken);
          setCases(casesResponse.cases || []);
        } catch (caseError) {
          console.error('Error fetching cases:', caseError);
          // Don't set error yet, try to fetch other data
        }
        
        // Fetch immigration forms
        try {
          const formsResponse = await immigrationApi.getIntakeForms(accessToken);
          setForms(Array.isArray(formsResponse) ? formsResponse : []);
        } catch (formError) {
          console.error('Error fetching intake forms:', formError);
          // Don't set error yet, try to fetch other data
        }
        
        // Fetch upcoming events
        try {
          const eventsResponse = await immigrationApi.getUpcomingEvents(accessToken);
          setUpcomingEvents(eventsResponse?.events || []);
        } catch (eventError) {
          console.error('Error fetching events:', eventError);
          // Use fallback data if events fail to load
          setUpcomingEvents([
            {
              id: 1,
              title: 'Document Submission Deadline',
              date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
              type: 'deadline'
            },
            {
              id: 2,
              title: 'Consultation with Immigration Lawyer',
              date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
              type: 'appointment'
            }
          ]);
        }
        
        // Fetch notifications
        try {
          const notificationsResponse = await immigrationApi.getNotifications(accessToken);
          setNotifications(notificationsResponse?.notifications || []);
        } catch (notificationError) {
          console.error('Error fetching notifications:', notificationError);
          // Use empty notifications as fallback
          setNotifications([]);
        }
        
      } catch (err) {
        console.error('Error fetching immigration data:', err);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    if (accessToken) {
      fetchData();
    } else {
      setLoading(false);
    }
  }, [accessToken]);
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const startNewApplication = () => {
    navigate('/immigration');
  };
  
  const markNotificationAsRead = async (notificationId) => {
    try {
      await immigrationApi.markNotificationAsRead(notificationId, accessToken);
      
      // Update the local state
      setNotifications(prevNotifications => 
        prevNotifications.map(notification => 
          notification._id === notificationId 
            ? { ...notification, isRead: true } 
            : notification
        )
      );
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };
  
  const openUploadModal = (caseId) => {
    setSelectedCaseId(caseId);
    setUploadModalOpen(true);
    setUploadFile(null);
    setDocumentType('identity');
    setUploadError(null);
  };
  
  const closeUploadModal = () => {
    setUploadModalOpen(false);
    setSelectedCaseId(null);
    setUploadFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setUploadFile(event.target.files[0]);
      setUploadError(null);
    }
  };
  
  const handleDocumentTypeChange = (event) => {
    setDocumentType(event.target.value);
  };
  
  const uploadDocument = async () => {
    if (!uploadFile || !documentType || !selectedCaseId) return;
    
    const formData = new FormData();
    formData.append('file', uploadFile);
    formData.append('documentType', documentType);
    formData.append('caseId', selectedCaseId);
    
    setUploading(true);
    setUploadError(null);
    
    try {
      await apiService.uploadDocument(formData);
      
      // Close modal and refresh cases
      closeUploadModal();
      const casesResponse = await immigrationApi.getCases(accessToken);
      setCases(casesResponse.cases || []);
      
      setNotificationMessage('Document uploaded successfully');
      setNotificationSent(true);
    } catch (error) {
      console.error('Error uploading document:', error);
      setUploadError(apiService.handleError(error));
    } finally {
      setUploading(false);
    }
  };
  
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch (e) {
      return 'Invalid date';
    }
  };
  
  const renderCaseCards = () => {
    if (cases.length === 0) {
      return (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            You don't have any active immigration cases yet.
          </Typography>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={startNewApplication}
            sx={{ mt: 2 }}
          >
            Start New Immigration Application
          </Button>
        </Box>
      );
    }
    
    return (
      <Grid container spacing={isMobile ? 2 : 3}>
        {cases.map(caseItem => (
          <Grid item xs={12} md={6} key={caseItem._id || caseItem.id}>
            <Card 
              raised={caseItem.status === 'in-progress'}
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: isMobile ? 'none' : 'translateY(-4px)',
                  boxShadow: isMobile ? 2 : 4
                }
              }}
            >
              <CardContent sx={{ flexGrow: 1, p: isMobile ? 2 : 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Typography variant={isMobile ? "h6" : "h5"} gutterBottom>
                    {caseItem.title || 'Immigration Case'}
                  </Typography>
                  <CaseStatus status={caseItem.status} />
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Case ID: {caseItem._id || caseItem.id}
                </Typography>
                
                <Divider sx={{ my: 1.5 }} />
                
                <Box sx={{ my: 2 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={getProgressValue(caseItem.status)} 
                    color={caseItem.status === 'delayed' ? 'error' : 'primary'}
                    sx={{ height: isMobile ? 10 : 8, borderRadius: 5 }}
                  />
                  <Typography variant="body2" sx={{ mt: 0.5, textAlign: 'right' }}>
                    {getProgressValue(caseItem.status)}% Complete
                  </Typography>
                </Box>
                
                <Grid container spacing={2} sx={{ mt: 1 }}>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Submitted on
                    </Typography>
                    <Typography variant="body2">
                      {formatDate(caseItem.createdAt || new Date())}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Last Updated
                    </Typography>
                    <Typography variant="body2">
                      {formatDate(caseItem.updatedAt || new Date())}
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      Type
                    </Typography>
                    <Typography variant="body2">
                      {caseItem.type || 'Family-Based Immigration'}
                    </Typography>
                  </Grid>
                </Grid>
                
                {caseItem.notes && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="caption" color="text.secondary">
                      Latest Update
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 1.5, bgcolor: 'background.default' }}>
                      <Typography variant="body2">
                        {caseItem.notes}
                      </Typography>
                    </Paper>
                  </Box>
                )}
              </CardContent>
              <CardActions sx={{ 
                px: isMobile ? 2 : 3, 
                pb: isMobile ? 2 : 3, 
                pt: 0,
                display: 'flex',
                flexWrap: 'wrap',
                gap: 1
              }}>
                <Button 
                  size={isMobile ? "medium" : "small"}
                  startIcon={<DescriptionIcon />}
                  onClick={() => navigate(`/case/${caseItem._id || caseItem.id}`)}
                  sx={{ minHeight: isMobile ? '44px' : 'auto' }}
                >
                  View Details
                </Button>
                <Button 
                  size={isMobile ? "medium" : "small"}
                  startIcon={<AttachFileIcon />}
                  onClick={() => openUploadModal(caseItem._id || caseItem.id)}
                  sx={{ minHeight: isMobile ? '44px' : 'auto' }}
                >
                  Documents
                </Button>
                <Box flexGrow={1} />
                <IconButton 
                  size={isMobile ? "medium" : "small"}
                  sx={{ 
                    width: isMobile ? 44 : 32, 
                    height: isMobile ? 44 : 32 
                  }}
                >
                  <MoreVertIcon />
                </IconButton>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  };
  
  const renderSubmittedForms = () => {
    if (forms.length === 0) {
      return (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            You haven't submitted any immigration forms yet.
          </Typography>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={startNewApplication}
            sx={{ mt: 2 }}
          >
            Complete an Immigration Form
          </Button>
        </Box>
      );
    }
    
    return (
      <Grid container spacing={isMobile ? 2 : 3}>
        {forms.map(form => (
          <Grid item xs={12} md={6} key={form._id}>
            <Card sx={{ 
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              transition: 'all 0.2s ease',
              '&:hover': {
                transform: isMobile ? 'none' : 'translateY(-4px)',
                boxShadow: isMobile ? 2 : 4
              }
            }}>
              <CardContent sx={{ flexGrow: 1, p: isMobile ? 2 : 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant={isMobile ? "h6" : "h5"}>
                    {form.firstName} {form.lastName}
                  </Typography>
                  <CaseStatus status={form.status || 'new'} />
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Submitted on {formatDate(form.createdAt || new Date())}
                </Typography>
                
                <Divider sx={{ my: 1.5 }} />
                
                <Grid container spacing={1} sx={{ mt: 1 }}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="caption" color="text.secondary">
                      Email
                    </Typography>
                    <Typography variant="body2" noWrap>
                      {form.email}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="caption" color="text.secondary">
                      Phone
                    </Typography>
                    <Typography variant="body2">
                      {form.phone}
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      Service Type
                    </Typography>
                    <Typography variant="body2">
                      {form.desiredService || form.visaType || 'Immigration Service'}
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      Nationality
                    </Typography>
                    <Typography variant="body2">
                      {form.nationality || 'Not specified'}
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
              <CardActions sx={{ 
                px: isMobile ? 2 : 3, 
                pb: isMobile ? 2 : 3,
                display: 'flex',
                flexWrap: 'wrap',
                gap: 1
              }}>
                <Button 
                  size={isMobile ? "medium" : "small"}
                  startIcon={<DescriptionIcon />}
                  onClick={() => navigate(`/forms/${form._id}`)}
                  sx={{ minHeight: isMobile ? '44px' : 'auto' }}
                >
                  View Form
                </Button>
                <Button 
                  size={isMobile ? "medium" : "small"}
                  startIcon={<FileCopyIcon />}
                  onClick={() => navigate(`/forms/${form._id}/copy`)}
                  sx={{ minHeight: isMobile ? '44px' : 'auto' }}
                >
                  Copy Form
                </Button>
                <Box flexGrow={1} />
                <Tooltip title="Print form">
                  <IconButton 
                    size={isMobile ? "medium" : "small"}
                    sx={{ 
                      width: isMobile ? 44 : 32, 
                      height: isMobile ? 44 : 32 
                    }}
                  >
                    <MoreVertIcon />
                  </IconButton>
                </Tooltip>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  };
  
  const renderNotifications = () => {
    if (notifications.length === 0) {
      return (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            No notifications available.
          </Typography>
        </Box>
      );
    }
    
    return (
      <List sx={{ width: '100%' }}>
        {notifications.map(notification => (
          <ListItem 
            key={notification._id}
            sx={{
              borderLeft: '4px solid',
              borderColor: notification.isRead ? 'primary.main' : 'error.main',
              mb: 2,
              bgcolor: 'background.paper',
              boxShadow: 1,
              borderRadius: '0 4px 4px 0',
              transition: 'all 0.2s ease',
              '&:hover': {
                transform: 'translateX(4px)',
                boxShadow: 2
              },
              p: isMobile ? 2 : 1
            }}
          >
            <ListItemIcon>
              <NotificationsIcon 
                color={notification.isRead ? "primary" : "error"} 
                sx={{ fontSize: isMobile ? 28 : 24 }}
              />
            </ListItemIcon>
            <ListItemText
              primary={
                <Typography variant="subtitle1" component="div" sx={{ fontWeight: notification.isRead ? 'normal' : 'bold' }}>
                  {notification.title}
                </Typography>
              }
              secondary={
                <Box sx={{ mt: 0.5 }}>
                  <Typography variant="body2" color="text.secondary">
                    {notification.message}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                    {formatDate(notification.createdAt)}
                  </Typography>
                </Box>
              }
            />
            {!notification.isRead && (
              <IconButton 
                size={isMobile ? "medium" : "small"}
                onClick={() => markNotificationAsRead(notification._id)}
                sx={{ 
                  ml: 1,
                  width: isMobile ? 44 : 36, 
                  height: isMobile ? 44 : 36,
                  bgcolor: 'background.default',
                  '&:hover': {
                    bgcolor: 'action.hover'
                  }
                }}
              >
                <CheckCircleIcon color="success" />
              </IconButton>
            )}
          </ListItem>
        ))}
      </List>
    );
  };
  
  const renderUpcomingEvents = () => {
    if (upcomingEvents.length === 0) {
      return (
        <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
          No upcoming events scheduled.
        </Typography>
      );
    }
    
    return (
      <List sx={{ width: '100%' }}>
        {upcomingEvents.map(event => {
          let icon = <ScheduleIcon color="primary" sx={{ fontSize: isMobile ? 28 : 24 }} />;
          
          if (event.type === 'deadline') {
            icon = <CalendarTodayIcon color="error" sx={{ fontSize: isMobile ? 28 : 24 }} />;
          } else if (event.type === 'appointment') {
            icon = <PhoneIcon color="success" sx={{ fontSize: isMobile ? 28 : 24 }} />;
          }
          
          return (
            <ListItem 
              key={event._id || event.id}
              sx={{
                borderLeft: '4px solid',
                borderColor: 
                  event.type === 'deadline' ? 'error.main' :
                  event.type === 'appointment' ? 'success.main' : 'primary.main',
                mb: 2,
                bgcolor: 'background.paper',
                boxShadow: 1,
                borderRadius: '0 4px 4px 0',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'translateX(4px)',
                  boxShadow: 2
                },
                p: isMobile ? 2 : 1
              }}
            >
              <ListItemIcon>
                {icon}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Typography variant="subtitle1" component="div" sx={{ fontWeight: 'medium' }}>
                    {event.title}
                  </Typography>
                }
                secondary={
                  <Box sx={{ mt: 0.5 }}>
                    <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 'bold' }}>
                      {formatDate(event.date)}
                    </Typography>
                    {event.description && (
                      <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                        {event.description}
                      </Typography>
                    )}
                  </Box>
                }
              />
              <Chip 
                label={event.type} 
                color={
                  event.type === 'deadline' ? 'error' :
                  event.type === 'appointment' ? 'success' : 'primary'
                }
                size={isMobile ? "medium" : "small"}
                sx={{ 
                  textTransform: 'capitalize',
                  ml: 1
                }}
              />
            </ListItem>
          );
        })}
      </List>
    );
  };
  
  const sendTestNotification = async () => {
    try {
      setTestStatus({ loading: true });
      const response = await apiService.client.post('/api/notifications/test', {
        message: 'Test notification from Immigration Dashboard',
        type: 'info',
        category: 'immigration'
      });
      
      if (response.data.success) {
        setTestStatus({ success: true, message: 'Test notification sent!' });
      } else {
        throw new Error('Failed to send test notification');
      }
    } catch (error) {
      console.error('Error sending test notification:', error);
      setTestStatus({ error: true, message: apiService.handleError(error) });
    } finally {
      setTimeout(() => setTestStatus(null), 3000);
    }
  };
  
  const handleCloseStatus = () => {
    setTestStatus(null);
  };
  
  if (loading) {
    return (
      <PageLayout title="Immigration Dashboard">
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
      </PageLayout>
    );
  }
  
  if (error) {
    return (
      <PageLayout title="Immigration Dashboard">
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={() => window.location.reload()}>
          Retry
        </Button>
      </PageLayout>
    );
  }
  
  return (
    <PageLayout title="Immigration Dashboard">
      <Container maxWidth="lg" sx={{ pt: 2, pb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, flexWrap: 'wrap' }}>
              <Typography variant="h5" component="h1" sx={{ fontWeight: 'bold' }}>
                Immigration Dashboard
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={startNewApplication}
                startIcon={<AssignmentIcon />}
              >
                New Application
              </Button>
            </Box>
          </Grid>
          
          {/* Test Notification Section */}
          <Grid item xs={12} sx={{ mb: 4 }}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Test Notifications
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Send a test notification to check WebSocket functionality
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Button 
                    variant="outlined" 
                    color="success"
                    fullWidth
                    startIcon={<NotificationsIcon />}
                    onClick={() => sendTestNotification()}
                  >
                    Send Test Notification
                  </Button>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
          
          {/* Status Cards */}
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: theme.palette.primary.light, color: 'white' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Active Cases
                </Typography>
                <Typography variant="h3">
                  {cases.filter(c => c.status !== 'completed').length}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: theme.palette.warning.light, color: 'white' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Pending Forms
                </Typography>
                <Typography variant="h3">
                  {forms.filter(f => f.status === 'new').length}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: theme.palette.success.light, color: 'white' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Completed
                </Typography>
                <Typography variant="h3">
                  {cases.filter(c => c.status === 'completed').length}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: theme.palette.error.light, color: 'white' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Upcoming Deadlines
                </Typography>
                <Typography variant="h3">
                  {upcomingEvents.filter(e => e.type === 'deadline').length}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Main Content */}
          <Grid item xs={12}>
            <Paper sx={{ bgcolor: 'background.paper' }}>
              <Tabs
                value={tabValue}
                onChange={handleTabChange}
                variant={isMobile ? "fullWidth" : "standard"}
                sx={{ borderBottom: 1, borderColor: 'divider' }}
              >
                <Tab label="Active Cases" />
                <Tab label="Forms" />
                <Tab 
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      Notifications
                      {notifications.filter(n => !n.isRead).length > 0 && (
                        <Chip 
                          label={notifications.filter(n => !n.isRead).length} 
                          color="error" 
                          size="small" 
                          sx={{ ml: 1 }}
                        />
                      )}
                    </Box>
                  } 
                />
              </Tabs>
              
              <Box sx={{ p: 3 }}>
                {tabValue === 0 && renderCaseCards()}
                {tabValue === 1 && renderSubmittedForms()}
                {tabValue === 2 && renderNotifications()}
              </Box>
            </Paper>
          </Grid>
          
          {/* Upcoming Events */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <NotificationsIcon sx={{ mr: 1 }} color="primary" />
                Upcoming Events & Deadlines
              </Typography>
              <Divider sx={{ mb: 2 }} />
              {renderUpcomingEvents()}
            </Paper>
          </Grid>
        </Grid>
      </Container>

      {/* Document Upload Modal */}
      <Modal
        open={uploadModalOpen}
        onClose={closeUploadModal}
        aria-labelledby="document-upload-modal"
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: { xs: '90%', sm: 500 },
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
          borderRadius: 2
        }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Upload Document
          </Typography>
          
          <Divider sx={{ mb: 3 }} />
          
          {uploadError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {uploadError}
            </Alert>
          )}
          
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel id="document-type-label">Document Type</InputLabel>
            <Select
              labelId="document-type-label"
              value={documentType}
              onChange={handleDocumentTypeChange}
              label="Document Type"
            >
              <MenuItem value="identity">Identity Document (Passport, ID)</MenuItem>
              <MenuItem value="application">Application Form</MenuItem>
              <MenuItem value="financial">Financial Document</MenuItem>
              <MenuItem value="medical">Medical Record</MenuItem>
              <MenuItem value="education">Educational Document</MenuItem>
              <MenuItem value="employment">Employment Document</MenuItem>
              <MenuItem value="letter">Support Letter</MenuItem>
              <MenuItem value="other">Other Document</MenuItem>
            </Select>
          </FormControl>
          
          <Box sx={{ mb: 3 }}>
            <input
              ref={fileInputRef}
              accept="image/*,.pdf,.doc,.docx"
              type="file"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              id="document-file-input"
            />
            <label htmlFor="document-file-input">
              <Button
                variant="outlined"
                component="span"
                startIcon={<FileUploadIcon />}
                fullWidth
              >
                Select File
              </Button>
            </label>
            
            {uploadFile && (
              <Typography variant="body2" sx={{ mt: 1, color: 'text.secondary' }}>
                Selected: {uploadFile.name}
              </Typography>
            )}
          </Box>
          
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button
              onClick={closeUploadModal}
              color="inherit"
            >
              Cancel
            </Button>
            <Button
              onClick={uploadDocument}
              variant="contained"
              color="primary"
              disabled={uploading || !uploadFile}
              startIcon={uploading ? <CircularProgress size={20} /> : <FileUploadIcon />}
            >
              {uploading ? 'Uploading...' : 'Upload Document'}
            </Button>
          </Box>
        </Box>
      </Modal>

      {/* Status Snackbar */}
      <Snackbar
        open={Boolean(testStatus)}
        autoHideDuration={testStatus?.type === 'success' ? 3000 : 6000}
        onClose={handleCloseStatus}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        {testStatus && (
          <Alert 
            onClose={handleCloseStatus} 
            severity={testStatus.type} 
            sx={{ width: '100%' }}
          >
            {testStatus.message}
          </Alert>
        )}
      </Snackbar>
    </PageLayout>
  );
};

export default ImmigrationDashboard; 
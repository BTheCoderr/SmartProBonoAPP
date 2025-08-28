import React, { useState, useEffect } from 'react';
import { 
  Container, Typography, Box, Grid, Paper, Card, CardContent, 
  Button, List, ListItem, ListItemText, ListItemIcon, Chip, Divider,
  Alert, IconButton, LinearProgress, Tab, Tabs, Avatar, Badge
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import NotificationsIcon from '@mui/icons-material/Notifications';
import DescriptionIcon from '@mui/icons-material/Description';
import ArticleIcon from '@mui/icons-material/Article';
import AssignmentIcon from '@mui/icons-material/Assignment';
import EventNoteIcon from '@mui/icons-material/EventNote';
import SettingsIcon from '@mui/icons-material/Settings';
import WarningIcon from '@mui/icons-material/Warning';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import MoreVertIcon from '@mui/icons-material/MoreVert';

function TabPanel(props) {
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
}

const Dashboard = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [documents, setDocuments] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [upcomingDeadlines, setUpcomingDeadlines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching data
    setTimeout(() => {
      setDocuments([
        { 
          id: '1', 
          title: 'Expungement Request Form', 
          status: 'completed', 
          lastUpdated: '2025-05-06T14:30:00Z',
          progress: 100,
          type: 'expungement'
        },
        { 
          id: '2', 
          title: 'Housing Defense Letter', 
          status: 'in_progress', 
          lastUpdated: '2025-05-03T09:15:00Z',
          progress: 65,
          type: 'housing'
        },
        { 
          id: '3', 
          title: 'Fee Waiver Application', 
          status: 'pending_review', 
          lastUpdated: '2025-05-01T11:45:00Z',
          progress: 90,
          type: 'fee_waiver'
        }
      ]);

      setNotifications([
        {
          id: '1',
          title: 'Document Ready for Review',
          message: 'Your expungement request form is ready for review.',
          date: '2025-05-06T16:30:00Z',
          read: false,
          type: 'document',
          documentId: '1'
        },
        {
          id: '2',
          title: 'Deadline Approaching',
          message: 'Housing defense submission deadline is in 2 days.',
          date: '2025-05-04T08:45:00Z',
          read: true,
          type: 'deadline',
          documentId: '2'
        },
        {
          id: '3',
          title: 'Application Status Update',
          message: 'Your fee waiver application has been submitted to the court.',
          date: '2025-05-02T13:20:00Z',
          read: true,
          type: 'status',
          documentId: '3'
        }
      ]);

      setUpcomingDeadlines([
        {
          id: '1',
          title: 'Housing Defense Submission',
          dueDate: '2025-05-08T23:59:59Z',
          documentId: '2',
          importance: 'high'
        },
        {
          id: '2',
          title: 'Fee Waiver Supporting Documents',
          dueDate: '2025-05-15T23:59:59Z',
          documentId: '3',
          importance: 'medium'
        }
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleViewDocument = (documentId) => {
    navigate(`/documents/${documentId}`);
  };

  const handleEditDocument = (documentId) => {
    navigate(`/documents/${documentId}/edit`);
  };

  const handleViewAllDocuments = () => {
    navigate('/documents');
  };

  const handleMarkNotificationRead = (notificationId) => {
    setNotifications(notifications.map(notification => 
      notification.id === notificationId 
        ? { ...notification, read: true } 
        : notification
    ));
  };

  const handleViewAllNotifications = () => {
    navigate('/notifications');
  };

  const handleViewProfile = () => {
    navigate('/profile');
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusChip = (status) => {
    const statusConfig = {
      completed: { color: 'success', label: 'Completed', icon: <CheckCircleIcon fontSize="small" /> },
      in_progress: { color: 'primary', label: 'In Progress', icon: <AccessTimeIcon fontSize="small" /> },
      pending_review: { color: 'warning', label: 'Pending Review', icon: <WarningIcon fontSize="small" /> },
      draft: { color: 'default', label: 'Draft', icon: <ArticleIcon fontSize="small" /> }
    };

    const { color, label, icon } = statusConfig[status] || statusConfig.draft;

    return (
      <Chip 
        icon={icon}
        label={label} 
        color={color} 
        size="small" 
        sx={{ fontWeight: 'medium' }}
      />
    );
  };

  const unreadNotifications = notifications.filter(notification => !notification.read).length;

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box py={4}>
          <Typography variant="h4" component="h1" gutterBottom>
            Dashboard
          </Typography>
          <Box sx={{ width: '100%', mt: 4 }}>
            <LinearProgress />
          </Box>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box py={4}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
          <Typography variant="h4" component="h1">
            Dashboard
          </Typography>
          <Box display="flex" alignItems="center">
            <Badge badgeContent={unreadNotifications} color="error" sx={{ mr: 2 }}>
              <IconButton color="primary" onClick={handleViewAllNotifications}>
                <NotificationsIcon />
              </IconButton>
            </Badge>
            <Button 
              variant="outlined"
              startIcon={<SettingsIcon />}
              onClick={handleViewProfile}
            >
              Profile & Settings
            </Button>
          </Box>
        </Box>
        
        <Card sx={{ mb: 4 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="dashboard tabs">
              <Tab label="Overview" />
              <Tab label="Documents" />
              <Tab label="Notifications" />
              <Tab label="Calendar" />
            </Tabs>
          </Box>
          
          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                        <DescriptionIcon />
                      </Avatar>
                      <Typography variant="h6">
                        Documents
                      </Typography>
                    </Box>
                    <Typography variant="h4" align="center" gutterBottom>
                      {documents.length}
                    </Typography>
                    <Grid container textAlign="center">
                      <Grid item xs={4}>
                        <Typography variant="body2" color="text.secondary">
                          Complete
                        </Typography>
                        <Typography variant="h6">
                          {documents.filter(doc => doc.status === 'completed').length}
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="text.secondary">
                          In Progress
                        </Typography>
                        <Typography variant="h6">
                          {documents.filter(doc => doc.status === 'in_progress').length}
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="text.secondary">
                          Pending
                        </Typography>
                        <Typography variant="h6">
                          {documents.filter(doc => doc.status === 'pending_review').length}
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={8}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Upcoming Deadlines
                    </Typography>
                    {upcomingDeadlines.length === 0 ? (
                      <Alert severity="info">No upcoming deadlines</Alert>
                    ) : (
                      <List>
                        {upcomingDeadlines.map((deadline) => (
                          <ListItem 
                            key={deadline.id}
                            secondaryAction={
                              <Button 
                                size="small" 
                                variant="outlined"
                                onClick={() => handleViewDocument(deadline.documentId)}
                              >
                                View
                              </Button>
                            }
                          >
                            <ListItemIcon>
                              <EventNoteIcon color={deadline.importance === 'high' ? 'error' : 'primary'} />
                            </ListItemIcon>
                            <ListItemText 
                              primary={deadline.title}
                              secondary={`Due: ${formatDate(deadline.dueDate)}`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    )}
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                      <Typography variant="h6">
                        Recent Documents
                      </Typography>
                      <Button size="small" onClick={handleViewAllDocuments}>
                        View All
                      </Button>
                    </Box>
                    <List>
                      {documents.slice(0, 3).map((document) => (
                        <ListItem 
                          key={document.id}
                          secondaryAction={
                            <Box>
                              <Button 
                                size="small" 
                                variant="outlined"
                                sx={{ mr: 1 }}
                                onClick={() => handleViewDocument(document.id)}
                              >
                                View
                              </Button>
                              <Button 
                                size="small" 
                                variant="contained"
                                onClick={() => handleEditDocument(document.id)}
                              >
                                Edit
                              </Button>
                            </Box>
                          }
                        >
                          <ListItemIcon>
                            <AssignmentIcon />
                          </ListItemIcon>
                          <ListItemText 
                            primary={
                              <Box display="flex" alignItems="center">
                                {document.title}
                                <Box ml={1}>
                                  {getStatusChip(document.status)}
                                </Box>
                              </Box>
                            }
                            secondary={`Last updated: ${formatDate(document.lastUpdated)} | Type: ${document.type.replace('_', ' ')}`}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={tabValue} index={1}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
              <Typography variant="h6">
                Your Documents
              </Typography>
              <Button 
                variant="contained" 
                startIcon={<ArticleIcon />}
                onClick={() => navigate('/forms')}
              >
                Create New Document
              </Button>
            </Box>
            
            {documents.length === 0 ? (
              <Alert severity="info">You don't have any documents yet</Alert>
            ) : (
              <List>
                {documents.map((document) => (
                  <Paper 
                    key={document.id} 
                    elevation={1} 
                    sx={{ mb: 2, overflow: 'hidden' }}
                  >
                    <Box p={2}>
                      <Grid container alignItems="center">
                        <Grid item xs={12} md={6}>
                          <Box display="flex" alignItems="center">
                            <DescriptionIcon sx={{ mr: 2, color: 'primary.main' }} />
                            <Box>
                              <Typography variant="subtitle1">
                                {document.title}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                Last updated: {formatDate(document.lastUpdated)}
                              </Typography>
                            </Box>
                          </Box>
                        </Grid>
                        <Grid item xs={12} md={3}>
                          <Box display="flex" alignItems="center" mt={{ xs: 1, md: 0 }}>
                            <Typography variant="body2" sx={{ mr: 1 }}>
                              Progress:
                            </Typography>
                            <Box sx={{ width: '100%', mr: 1 }}>
                              <LinearProgress 
                                variant="determinate" 
                                value={document.progress} 
                                sx={{ height: 8, borderRadius: 5 }}
                              />
                            </Box>
                            <Typography variant="body2">
                              {document.progress}%
                            </Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={12} md={3}>
                          <Box 
                            display="flex" 
                            justifyContent={{ xs: 'flex-start', md: 'flex-end' }}
                            mt={{ xs: 1, md: 0 }}
                          >
                            {getStatusChip(document.status)}
                            <Button 
                              size="small" 
                              sx={{ ml: 1 }}
                              onClick={() => handleViewDocument(document.id)}
                            >
                              View
                            </Button>
                            <Button 
                              size="small" 
                              variant="outlined"
                              sx={{ ml: 1 }}
                              onClick={() => handleEditDocument(document.id)}
                            >
                              Edit
                            </Button>
                          </Box>
                        </Grid>
                      </Grid>
                    </Box>
                  </Paper>
                ))}
              </List>
            )}
          </TabPanel>
          
          <TabPanel value={tabValue} index={2}>
            <Typography variant="h6" gutterBottom>
              Notifications
            </Typography>
            
            {notifications.length === 0 ? (
              <Alert severity="info">You don't have any notifications</Alert>
            ) : (
              <List>
                {notifications.map((notification) => (
                  <ListItem 
                    key={notification.id}
                    sx={{ 
                      mb: 1, 
                      bgcolor: notification.read ? 'transparent' : 'action.hover',
                      borderRadius: 1,
                    }}
                    secondaryAction={
                      <Button 
                        size="small" 
                        onClick={() => handleMarkNotificationRead(notification.id)}
                      >
                        {notification.read ? 'Already Read' : 'Mark as Read'}
                      </Button>
                    }
                  >
                    <ListItemIcon>
                      {notification.type === 'document' && <DescriptionIcon color="primary" />}
                      {notification.type === 'deadline' && <EventNoteIcon color="error" />}
                      {notification.type === 'status' && <AssignmentIcon color="info" />}
                    </ListItemIcon>
                    <ListItemText 
                      primary={
                        <Box display="flex" alignItems="center">
                          {notification.title}
                          {!notification.read && (
                            <Chip 
                              label="New" 
                              size="small" 
                              color="error" 
                              sx={{ ml: 1, height: 20 }}
                            />
                          )}
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2">
                            {notification.message}
                          </Typography>
                          <Typography variant="caption">
                            {formatDate(notification.date)}
                          </Typography>
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </TabPanel>
          
          <TabPanel value={tabValue} index={3}>
            <Typography variant="h6" gutterBottom>
              Calendar & Deadlines
            </Typography>
            <Alert severity="info" sx={{ mb: 2 }}>
              Calendar integration coming soon. For now, view your upcoming deadlines here.
            </Alert>
            
            {upcomingDeadlines.length === 0 ? (
              <Alert severity="info">No upcoming deadlines</Alert>
            ) : (
              <List>
                {upcomingDeadlines.map((deadline) => (
                  <Card key={deadline.id} sx={{ mb: 2 }}>
                    <CardContent>
                      <Box display="flex" alignItems="center" mb={1}>
                        <EventNoteIcon 
                          color={deadline.importance === 'high' ? 'error' : 'primary'} 
                          sx={{ mr: 2 }}
                        />
                        <Typography variant="h6">
                          {deadline.title}
                        </Typography>
                      </Box>
                      <Typography variant="body1" gutterBottom>
                        Due: {formatDate(deadline.dueDate)}
                      </Typography>
                      <Box mt={2} display="flex" justifyContent="flex-end">
                        <Button 
                          variant="outlined" 
                          onClick={() => handleViewDocument(deadline.documentId)}
                        >
                          View Related Document
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                ))}
              </List>
            )}
          </TabPanel>
        </Card>
      </Box>
    </Container>
  );
};

export default Dashboard; 
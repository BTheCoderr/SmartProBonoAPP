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
  Button,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Badge,
} from '@mui/material';
import {
  Assignment as AssignmentIcon,
  Schedule as ScheduleIcon,
  Notifications as NotificationsIcon,
  Description as DescriptionIcon,
  CalendarToday as CalendarIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  Message as MessageIcon
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { useRealTimeUpdates } from '../hooks/useRealTimeUpdates';
import PageLayout from '../components/PageLayout';

const ClientPortal = () => {
  const { currentUser } = useAuth();
  const { notifications: realTimeNotifications, unreadCount } = useRealTimeUpdates();
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [cases, setCases] = useState([]);
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [openMessageDialog, setOpenMessageDialog] = useState(false);
  const [messageText, setMessageText] = useState('');

  // Mock data - in real app, this would come from API
  useEffect(() => {
    const fetchClientData = async () => {
      setLoading(true);
      try {
        // Simulate API calls
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setCases([
          {
            id: 1,
            title: 'Immigration Case - Green Card Application',
            status: 'In Progress',
            priority: 'High',
            progress: 65,
            assignedLawyer: 'Sarah Johnson',
            lastUpdate: '2024-01-15',
            description: 'Processing I-485 application for permanent residence',
            nextAction: 'Biometrics appointment scheduled',
            nextActionDate: '2024-01-25'
          },
          {
            id: 2,
            title: 'Family Law - Divorce Proceedings',
            status: 'Under Review',
            priority: 'Medium',
            progress: 30,
            assignedLawyer: 'Michael Chen',
            lastUpdate: '2024-01-12',
            description: 'Divorce petition and custody agreement preparation',
            nextAction: 'Document review and filing',
            nextActionDate: '2024-01-30'
          }
        ]);

        setUpcomingEvents([
          {
            id: 1,
            title: 'Biometrics Appointment',
            date: '2024-01-25',
            time: '10:00 AM',
            location: 'USCIS Application Support Center',
            type: 'appointment',
            caseId: 1
          },
          {
            id: 2,
            title: 'Court Hearing - Divorce Case',
            date: '2024-02-15',
            time: '2:00 PM',
            location: 'Providence Family Court',
            type: 'hearing',
            caseId: 2
          },
          {
            id: 3,
            title: 'Document Submission Deadline',
            date: '2024-01-30',
            time: '5:00 PM',
            location: 'Online Portal',
            type: 'deadline',
            caseId: 2
          }
        ]);

        setNotifications([
          {
            id: 1,
            title: 'Case Update',
            message: 'Your immigration case has been updated. New documents are available.',
            type: 'info',
            date: '2024-01-15',
            read: false,
            caseId: 1
          },
          {
            id: 2,
            title: 'Appointment Reminder',
            message: 'Your biometrics appointment is scheduled for January 25th at 10:00 AM.',
            type: 'warning',
            date: '2024-01-14',
            read: false,
            caseId: 1
          },
          {
            id: 3,
            title: 'Document Request',
            message: 'Please upload your financial disclosure documents by January 30th.',
            type: 'error',
            date: '2024-01-13',
            read: true,
            caseId: 2
          }
        ]);

        setDocuments([
          {
            id: 1,
            name: 'I-485 Application Form',
            type: 'Form',
            status: 'Completed',
            uploadDate: '2024-01-10',
            caseId: 1,
            size: '2.3 MB'
          },
          {
            id: 2,
            name: 'Supporting Documents Package',
            type: 'Documents',
            status: 'Under Review',
            uploadDate: '2024-01-12',
            caseId: 1,
            size: '15.7 MB'
          },
          {
            id: 3,
            name: 'Divorce Petition',
            type: 'Legal Document',
            status: 'Draft',
            uploadDate: '2024-01-08',
            caseId: 2,
            size: '1.2 MB'
          }
        ]);

      } catch (err) {
        setError('Failed to load client data');
      } finally {
        setLoading(false);
      }
    };

    fetchClientData();
  }, []);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleSendMessage = () => {
    // In real app, this would send message to lawyer
    console.log('Sending message:', messageText);
    setOpenMessageDialog(false);
    setMessageText('');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'In Progress': return 'primary';
      case 'Under Review': return 'warning';
      case 'Completed': return 'success';
      case 'Pending': return 'info';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High': return 'error';
      case 'Medium': return 'warning';
      case 'Low': return 'success';
      default: return 'default';
    }
  };

  const getEventIcon = (type) => {
    switch (type) {
      case 'appointment': return <ScheduleIcon />;
      case 'hearing': return <AssignmentIcon />;
      case 'deadline': return <WarningIcon />;
      default: return <CalendarIcon />;
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'info': return <InfoIcon />;
      case 'warning': return <WarningIcon />;
      case 'error': return <WarningIcon />;
      default: return <NotificationsIcon />;
    }
  };

  const renderCasesTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Your Cases
      </Typography>
      <Grid container spacing={3}>
        {cases.map((caseItem) => (
          <Grid item xs={12} md={6} key={caseItem.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" component="h2">
                    {caseItem.title}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip 
                      label={caseItem.status} 
                      color={getStatusColor(caseItem.status)}
                      size="small"
                    />
                    <Chip 
                      label={caseItem.priority} 
                      color={getPriorityColor(caseItem.priority)}
                      size="small"
                    />
                  </Box>
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Assigned to: {caseItem.assignedLawyer}
                </Typography>
                
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {caseItem.description}
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Progress: {caseItem.progress}%
                  </Typography>
                  <Box sx={{ width: '100%', bgcolor: 'grey.200', borderRadius: 1, height: 8 }}>
                    <Box 
                      sx={{ 
                        width: `${caseItem.progress}%`, 
                        bgcolor: 'primary.main', 
                        borderRadius: 1, 
                        height: 8 
                      }} 
                    />
                  </Box>
                </Box>
                
                <Divider sx={{ my: 2 }} />
                
                <Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Next Action: {caseItem.nextAction}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Due: {caseItem.nextActionDate}
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button size="small" startIcon={<MessageIcon />}>
                  Contact Lawyer
                </Button>
                <Button size="small" startIcon={<DescriptionIcon />}>
                  View Documents
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderCalendarTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Upcoming Events & Court Dates
      </Typography>
      <List>
        {upcomingEvents.map((event, index) => (
          <React.Fragment key={event.id}>
            <ListItem>
              <ListItemIcon>
                <Box sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  width: 40, 
                  height: 40, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main',
                  color: 'white'
                }}>
                  {getEventIcon(event.type)}
                </Box>
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6">{event.title}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {event.date} at {event.time}
                    </Typography>
                  </Box>
                }
                secondary={
                  <Typography color="text.secondary">
                    {event.location}
                  </Typography>
                }
              />
            </ListItem>
            {index < upcomingEvents.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
    </Box>
  );

  const renderDocumentsTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Your Documents
      </Typography>
      <List>
        {documents.map((doc) => (
          <ListItem key={doc.id} divider>
            <ListItemIcon>
              <DescriptionIcon />
            </ListItemIcon>
            <ListItemText
              primary={doc.name}
              secondary={`${doc.type} • ${doc.size} • Uploaded ${doc.uploadDate}`}
            />
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip 
                label={doc.status} 
                color={getStatusColor(doc.status)}
                size="small"
              />
              <IconButton size="small">
                <DownloadIcon />
              </IconButton>
            </Box>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderNotificationsTab = () => {
    // Combine static notifications with real-time notifications
    const allNotifications = [...notifications, ...realTimeNotifications];
    
    return (
      <Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Notifications & Updates
          </Typography>
          {unreadCount > 0 && (
            <Chip 
              label={`${unreadCount} new`} 
              color="error" 
              size="small"
            />
          )}
        </Box>
        <List>
          {allNotifications.length === 0 ? (
            <ListItem>
              <ListItemText
                primary="No notifications yet"
                secondary="You'll receive real-time updates about your cases here"
              />
            </ListItem>
          ) : (
            allNotifications.map((notification) => (
              <ListItem key={notification.id} divider>
                <ListItemIcon>
                  <Badge color="error" variant="dot" invisible={notification.read}>
                    {getNotificationIcon(notification.type)}
                  </Badge>
                </ListItemIcon>
                <ListItemText
                  primary={notification.title}
                  secondary={
                    <Box>
                      <Typography variant="body2">{notification.message}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {notification.date || new Date(notification.timestamp).toLocaleDateString()}
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))
          )}
        </List>
      </Box>
    );
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <PageLayout
      title="Client Portal"
      description="View your cases, court dates, and legal updates"
      showBanner={false}
    >
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Welcome back, {currentUser?.first_name || currentUser?.username}!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Here's an overview of your legal cases and upcoming events.
          </Typography>
        </Box>

        <Paper sx={{ mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} variant="fullWidth">
            <Tab label="My Cases" icon={<AssignmentIcon />} />
            <Tab label="Calendar" icon={<CalendarIcon />} />
            <Tab label="Documents" icon={<DescriptionIcon />} />
            <Tab 
              label={
                <Badge badgeContent={notifications.filter(n => !n.read).length} color="error">
                  Notifications
                </Badge>
              } 
              icon={<NotificationsIcon />} 
            />
          </Tabs>
        </Paper>

        <Box sx={{ mt: 3 }}>
          {activeTab === 0 && renderCasesTab()}
          {activeTab === 1 && renderCalendarTab()}
          {activeTab === 2 && renderDocumentsTab()}
          {activeTab === 3 && renderNotificationsTab()}
        </Box>

        {/* Quick Actions */}
        <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            variant="contained"
            startIcon={<MessageIcon />}
            onClick={() => setOpenMessageDialog(true)}
          >
            Contact Your Lawyer
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => window.location.reload()}
          >
            Refresh Data
          </Button>
        </Box>

        {/* Message Dialog */}
        <Dialog open={openMessageDialog} onClose={() => setOpenMessageDialog(false)} maxWidth="sm" fullWidth>
          <DialogTitle>Send Message to Your Lawyer</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Message"
              fullWidth
              multiline
              rows={4}
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              placeholder="Type your message here..."
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenMessageDialog(false)}>Cancel</Button>
            <Button onClick={handleSendMessage} variant="contained">
              Send Message
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </PageLayout>
  );
};

export default ClientPortal;

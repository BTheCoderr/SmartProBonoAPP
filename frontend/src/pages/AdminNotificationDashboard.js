import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  TextField,
  Button,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  Alert,
  IconButton,
  Tooltip,
  Card,
  CardContent,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Send as SendIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  People as PeopleIcon,
  Devices as DevicesIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { API_URL } from '../config';
import { useNavigate } from 'react-router-dom';

// Helper to format date
const formatDate = (dateString) => {
  if (!dateString) return 'Unknown';
  const date = new Date(dateString);
  return date.toLocaleString();
};

// Helper to get icon based on notification type
const getNotificationIcon = (type) => {
  switch (type) {
    case 'success':
      return <CheckCircleIcon color="success" />;
    case 'error':
      return <ErrorIcon color="error" />;
    case 'warning':
      return <WarningIcon color="warning" />;
    case 'info':
    default:
      return <InfoIcon color="info" />;
  }
};

const AdminNotificationDashboard = () => {
  const { accessToken, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  
  // State for notifications
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // State for pagination
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  // State for connection stats
  const [stats, setStats] = useState({
    connectedUsers: 0,
    totalConnections: 0,
    lastUpdated: null,
  });
  const [loadingStats, setLoadingStats] = useState(false);
  
  // State for broadcast form
  const [broadcastMessage, setBroadcastMessage] = useState('');
  const [broadcastType, setBroadcastType] = useState('info');
  const [broadcastTitle, setBroadcastTitle] = useState('');
  const [sendingBroadcast, setSendingBroadcast] = useState(false);
  const [broadcastSuccess, setBroadcastSuccess] = useState(false);
  
  // State for deletion confirmation
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [notificationToDelete, setNotificationToDelete] = useState(null);
  
  // Fetch notifications when component mounts
  useEffect(() => {
    if (isAuthenticated && accessToken) {
      fetchNotifications();
      fetchStats();
    }
  }, [isAuthenticated, accessToken]);
  
  // Check if user is authorized
  useEffect(() => {
    if (isAuthenticated && !isAdmin) {
      navigate('/access-denied');
    }
  }, [isAuthenticated, isAdmin, navigate]);
  
  // Fetch all notifications
  const fetchNotifications = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${API_URL}/api/admin/notifications`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      
      if (response.data && response.data.data) {
        setNotifications(response.data.data);
      } else {
        // Fallback for development/testing
        setNotifications([
          {
            _id: '1',
            title: 'System Maintenance',
            message: 'The system will be down for maintenance tonight from 2-4 AM EST.',
            type: 'info',
            category: 'system',
            createdAt: new Date().toISOString(),
            sentTo: 'all',
            readCount: 12,
            deliveryCount: 25,
            errorCount: 0
          },
          {
            _id: '2',
            title: 'Form Processing Delay',
            message: 'There is currently a delay in processing immigration forms due to high volume.',
            type: 'warning',
            category: 'immigration',
            createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
            sentTo: 'immigration-users',
            readCount: 43,
            deliveryCount: 120,
            errorCount: 2
          },
          {
            _id: '3',
            title: 'New Feature Available',
            message: 'Document scanning is now available in the mobile app.',
            type: 'success',
            category: 'system',
            createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
            sentTo: 'all',
            readCount: 156,
            deliveryCount: 450,
            errorCount: 0
          }
        ]);
      }
    } catch (err) {
      console.error('Error fetching notifications:', err);
      setError('Failed to load notifications. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  // Fetch connection statistics
  const fetchStats = async () => {
    setLoadingStats(true);
    
    try {
      const response = await axios.get(`${API_URL}/api/test/websocket-stats`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      
      if (response.data) {
        setStats({
          connectedUsers: response.data.connected_users || 0,
          totalConnections: response.data.total_connections || 0,
          lastUpdated: new Date().toISOString()
        });
      }
    } catch (err) {
      console.error('Error fetching WebSocket stats:', err);
      // Don't set error state to avoid overriding notification errors
    } finally {
      setLoadingStats(false);
    }
  };
  
  // Send broadcast notification
  const sendBroadcast = async () => {
    if (!broadcastMessage.trim()) {
      setError('Message cannot be empty');
      return;
    }
    
    setSendingBroadcast(true);
    setError(null);
    setBroadcastSuccess(false);
    
    try {
      const response = await axios.post(
        `${API_URL}/api/admin/notifications/broadcast`,
        {
          message: broadcastMessage,
          type: broadcastType,
          title: broadcastTitle || 'System Notification',
        },
        {
          headers: { Authorization: `Bearer ${accessToken}` }
        }
      );
      
      if (response.data && response.data.success) {
        setBroadcastSuccess(true);
        setBroadcastMessage('');
        setBroadcastTitle('');
        // Refresh notifications list
        fetchNotifications();
      } else {
        setError('Failed to send broadcast');
      }
    } catch (err) {
      console.error('Error sending broadcast:', err);
      setError(`Failed to send broadcast: ${err.response?.data?.message || err.message}`);
    } finally {
      setSendingBroadcast(false);
    }
  };
  
  // Delete notification
  const deleteNotification = async () => {
    if (!notificationToDelete) return;
    
    try {
      await axios.delete(`${API_URL}/api/admin/notifications/${notificationToDelete}`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      
      // Remove deleted notification from list
      setNotifications(notifications.filter(n => n._id !== notificationToDelete));
      setNotificationToDelete(null);
      setDeleteDialogOpen(false);
    } catch (err) {
      console.error('Error deleting notification:', err);
      setError(`Failed to delete notification: ${err.response?.data?.message || err.message}`);
      setDeleteDialogOpen(false);
    }
  };
  
  // Handle pagination change
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };
  
  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  
  // Confirm deletion
  const handleDeleteClick = (id) => {
    setNotificationToDelete(id);
    setDeleteDialogOpen(true);
  };
  
  // Check if component should render
  if (!isAuthenticated) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">Please log in to access this page</Alert>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Notification Management
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Manage system notifications and monitor connections
        </Typography>
      </Box>
      
      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <PeopleIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Connected Users</Typography>
              </Box>
              {loadingStats ? (
                <CircularProgress size={24} />
              ) : (
                <Typography variant="h3">{stats.connectedUsers}</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <DevicesIcon color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Connections</Typography>
              </Box>
              {loadingStats ? (
                <CircularProgress size={24} />
              ) : (
                <Typography variant="h3">{stats.totalConnections}</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SpeedIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">System Status</Typography>
              </Box>
              <Chip 
                label="Online" 
                color="success" 
                sx={{ fontSize: '1.25rem', height: 36, px: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Broadcast Form */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Send Broadcast Notification
        </Typography>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {broadcastSuccess && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Broadcast sent successfully!
          </Alert>
        )}
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              label="Title"
              variant="outlined"
              fullWidth
              value={broadcastTitle}
              onChange={(e) => setBroadcastTitle(e.target.value)}
              placeholder="System Notification"
              margin="normal"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Notification Type</InputLabel>
              <Select
                value={broadcastType}
                onChange={(e) => setBroadcastType(e.target.value)}
                label="Notification Type"
              >
                <MenuItem value="info">Info</MenuItem>
                <MenuItem value="success">Success</MenuItem>
                <MenuItem value="warning">Warning</MenuItem>
                <MenuItem value="error">Error</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Message"
              variant="outlined"
              fullWidth
              multiline
              rows={3}
              value={broadcastMessage}
              onChange={(e) => setBroadcastMessage(e.target.value)}
              placeholder="Enter your notification message here..."
              margin="normal"
              required
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<SendIcon />}
              onClick={sendBroadcast}
              disabled={!broadcastMessage.trim() || sendingBroadcast}
              sx={{ mr: 2 }}
            >
              {sendingBroadcast ? 'Sending...' : 'Send Broadcast'}
            </Button>
          </Grid>
        </Grid>
      </Paper>
      
      {/* Notifications Table */}
      <Paper sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Notification History
          </Typography>
          <Button 
            startIcon={<RefreshIcon />}
            onClick={fetchNotifications}
            disabled={loading}
          >
            Refresh
          </Button>
        </Box>
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Type</TableCell>
                    <TableCell>Title</TableCell>
                    <TableCell>Message</TableCell>
                    <TableCell>Sent To</TableCell>
                    <TableCell>Date</TableCell>
                    <TableCell>Stats</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {notifications
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((notification) => (
                      <TableRow key={notification._id}>
                        <TableCell>
                          <Tooltip title={notification.type}>
                            <Box>{getNotificationIcon(notification.type)}</Box>
                          </Tooltip>
                        </TableCell>
                        <TableCell>{notification.title}</TableCell>
                        <TableCell>{notification.message}</TableCell>
                        <TableCell>
                          <Chip 
                            label={notification.sentTo} 
                            size="small" 
                            color={notification.sentTo === 'all' ? 'primary' : 'default'}
                          />
                        </TableCell>
                        <TableCell>{formatDate(notification.createdAt)}</TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                            <Typography variant="caption">
                              Delivered: {notification.deliveryCount}
                            </Typography>
                            <Typography variant="caption">
                              Read: {notification.readCount}
                            </Typography>
                            {notification.errorCount > 0 && (
                              <Typography variant="caption" color="error.main">
                                Errors: {notification.errorCount}
                              </Typography>
                            )}
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Tooltip title="Delete">
                            <IconButton 
                              size="small" 
                              color="error"
                              onClick={() => handleDeleteClick(notification._id)}
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    ))}
                  
                  {notifications.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={7} align="center">
                        <Typography variant="body2" color="textSecondary" sx={{ py: 2 }}>
                          No notifications found
                        </Typography>
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
            
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={notifications.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </>
        )}
      </Paper>
      
      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Delete Notification</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this notification? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={deleteNotification} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AdminNotificationDashboard; 
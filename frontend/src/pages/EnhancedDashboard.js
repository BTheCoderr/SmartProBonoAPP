import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon, 
  Chip, 
  LinearProgress,
  Button,
  IconButton
} from '@mui/material';
import { 
  Notifications as NotificationsIcon,
  Description as DescriptionIcon,
  EventNote as EventNoteIcon,
  TrendingUp as TrendingUpIcon,
  Gavel as GavelIcon,
  People as PeopleIcon,
  Assignment as AssignmentIcon,
  CheckCircle as CheckCircleIcon,
  AccessTime as AccessTimeIcon,
  Add as AddIcon,
  MoreVert as MoreVertIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const EnhancedDashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalCases: 0,
    activeCases: 0,
    completedCases: 0,
    pendingTasks: 0,
    totalClients: 0,
    upcomingDeadlines: 0
  });

  const [recentActivity, setRecentActivity] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [upcomingDeadlines, setUpcomingDeadlines] = useState([]);
  const [recentDocuments, setRecentDocuments] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      
      // Simulate API calls
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock data
      setStats({
        totalCases: 24,
        activeCases: 12,
        completedCases: 8,
        pendingTasks: 15,
        totalClients: 18,
        upcomingDeadlines: 5
      });

      setRecentActivity([
        { id: 1, action: 'New case created', client: 'John Smith', time: '2 hours ago', type: 'case' },
        { id: 2, action: 'Document signed', client: 'Maria Garcia', time: '4 hours ago', type: 'document' },
        { id: 3, action: 'Court date scheduled', client: 'David Johnson', time: '1 day ago', type: 'court' },
        { id: 4, action: 'Payment received', client: 'Sarah Wilson', time: '2 days ago', type: 'payment' },
        { id: 5, action: 'Case status updated', client: 'Michael Brown', time: '3 days ago', type: 'case' }
      ]);

      setNotifications([
        { id: 1, message: 'Court hearing scheduled for tomorrow', type: 'urgent', time: '1 hour ago' },
        { id: 2, message: 'New client inquiry received', type: 'info', time: '3 hours ago' },
        { id: 3, message: 'Document review completed', type: 'success', time: '5 hours ago' },
        { id: 4, message: 'Payment overdue for 3 clients', type: 'warning', time: '1 day ago' }
      ]);

      setUpcomingDeadlines([
        { id: 1, title: 'Court Hearing - Smith vs. State', date: '2024-01-20', type: 'urgent', client: 'John Smith' },
        { id: 2, title: 'Document Filing Deadline', date: '2024-01-22', type: 'normal', client: 'Maria Garcia' },
        { id: 3, title: 'Client Meeting', date: '2024-01-25', type: 'normal', client: 'David Johnson' },
        { id: 4, title: 'Contract Review', date: '2024-01-28', type: 'normal', client: 'Sarah Wilson' }
      ]);

      setRecentDocuments([
        { id: 1, name: 'I-485 Application - John Smith', type: 'Immigration', status: 'Draft', date: '2024-01-15' },
        { id: 2, name: 'Divorce Petition - Maria Garcia', type: 'Family Law', status: 'Review', date: '2024-01-14' },
        { id: 3, name: 'DUI Defense Strategy - David Johnson', type: 'Criminal', status: 'Complete', date: '2024-01-13' },
        { id: 4, name: 'Personal Injury Claim - Sarah Wilson', type: 'Personal Injury', status: 'Draft', date: '2024-01-12' }
      ]);

      setLoading(false);
    };

    fetchDashboardData();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'urgent': return 'error';
      case 'normal': return 'primary';
      case 'completed': return 'success';
      case 'draft': return 'warning';
      case 'review': return 'info';
      default: return 'default';
    }
  };

  const getActivityIcon = (type) => {
    switch (type) {
      case 'case': return <GavelIcon />;
      case 'document': return <DescriptionIcon />;
      case 'court': return <EventNoteIcon />;
      case 'payment': return <TrendingUpIcon />;
      default: return <AssignmentIcon />;
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <LinearProgress sx={{ width: '50%' }} />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Welcome back, {user?.name || 'User'}! Here's what's happening with your cases.
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={2}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <GavelIcon color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.totalCases}</Typography>
                  <Typography color="textSecondary">Total Cases</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <AssignmentIcon color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.activeCases}</Typography>
                  <Typography color="textSecondary">Active Cases</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <CheckCircleIcon color="info" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.completedCases}</Typography>
                  <Typography color="textSecondary">Completed</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <PeopleIcon color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.totalClients}</Typography>
                  <Typography color="textSecondary">Clients</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <AccessTimeIcon color="error" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.pendingTasks}</Typography>
                  <Typography color="textSecondary">Pending Tasks</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <EventNoteIcon color="secondary" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.upcomingDeadlines}</Typography>
                  <Typography color="textSecondary">Deadlines</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Recent Activity</Typography>
                <Button size="small" onClick={() => navigate('/activity')}>
                  View All
                </Button>
              </Box>
              <List>
                {recentActivity.map((activity) => (
                  <ListItem key={activity.id} sx={{ px: 0 }}>
                    <ListItemIcon>
                      {getActivityIcon(activity.type)}
                    </ListItemIcon>
                    <ListItemText
                      primary={activity.action}
                      secondary={`${activity.client} • ${activity.time}`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Notifications */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Notifications</Typography>
                <IconButton size="small">
                  <MoreVertIcon />
                </IconButton>
              </Box>
              <List>
                {notifications.map((notification) => (
                  <ListItem key={notification.id} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <NotificationsIcon color={getStatusColor(notification.type)} />
                    </ListItemIcon>
                    <ListItemText
                      primary={notification.message}
                      secondary={notification.time}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Upcoming Deadlines */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Upcoming Deadlines</Typography>
                <Button size="small" onClick={() => navigate('/deadlines')}>
                  View All
                </Button>
              </Box>
              <List>
                {upcomingDeadlines.map((deadline) => (
                  <ListItem key={deadline.id} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <EventNoteIcon color={getStatusColor(deadline.type)} />
                    </ListItemIcon>
                    <ListItemText
                      primary={deadline.title}
                      secondary={`${deadline.client} • ${deadline.date}`}
                    />
                    <Chip 
                      label={deadline.type} 
                      color={getStatusColor(deadline.type)} 
                      size="small" 
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Documents */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Recent Documents</Typography>
                <Button size="small" onClick={() => navigate('/documents')}>
                  View All
                </Button>
              </Box>
              <List>
                {recentDocuments.map((document) => (
                  <ListItem key={document.id} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <DescriptionIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary={document.name}
                      secondary={`${document.type} • ${document.date}`}
                    />
                    <Chip 
                      label={document.status} 
                      color={getStatusColor(document.status)} 
                      size="small" 
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Quick Actions
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={() => navigate('/client-portal')}
              >
                New Case
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<DescriptionIcon />}
                onClick={() => navigate('/documents')}
              >
                Upload Document
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<EventNoteIcon />}
                onClick={() => navigate('/calendar')}
              >
                Schedule Meeting
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<GavelIcon />}
                onClick={() => navigate('/ai-virtual-paralegal')}
              >
                AI Assistant
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EnhancedDashboard;

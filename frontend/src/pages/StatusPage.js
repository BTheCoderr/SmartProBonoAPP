import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
  LinearProgress
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Cloud as CloudIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
  Storage as StorageIcon,
  Api as ApiIcon,
  Chat as ChatIcon,
  Description as DescriptionIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const StatusPage = () => {
  const [systemStatus] = useState({
    overall: 'operational',
    services: [
      { name: 'Web Application', status: 'operational', responseTime: '120ms' },
      { name: 'API Services', status: 'operational', responseTime: '85ms' },
      { name: 'AI Chat System', status: 'operational', responseTime: '1.2s' },
      { name: 'Document Generation', status: 'operational', responseTime: '2.1s' },
      { name: 'Database', status: 'operational', responseTime: '45ms' },
      { name: 'Authentication', status: 'operational', responseTime: '90ms' },
      { name: 'File Storage', status: 'operational', responseTime: '150ms' },
      { name: 'Email Services', status: 'operational', responseTime: '200ms' }
    ],
    incidents: [],
    lastUpdated: new Date().toISOString()
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call to get system status
    const fetchStatus = async () => {
      setLoading(true);
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      setLoading(false);
    };

    fetchStatus();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'operational': return 'success';
      case 'degraded': return 'warning';
      case 'outage': return 'error';
      case 'maintenance': return 'info';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'operational': return <CheckCircleIcon />;
      case 'degraded': return <WarningIcon />;
      case 'outage': return <ErrorIcon />;
      case 'maintenance': return <InfoIcon />;
      default: return <InfoIcon />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'operational': return 'Operational';
      case 'degraded': return 'Degraded Performance';
      case 'outage': return 'Service Outage';
      case 'maintenance': return 'Under Maintenance';
      default: return 'Unknown';
    }
  };

  const getOverallStatusColor = () => {
    const hasOutage = systemStatus.services.some(service => service.status === 'outage');
    const hasDegraded = systemStatus.services.some(service => service.status === 'degraded');
    
    if (hasOutage) return 'error';
    if (hasDegraded) return 'warning';
    return 'success';
  };

  if (loading) {
    return (
      <PageLayout
        title="System Status"
        description="Real-time status of SmartProBono services"
      >
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <LinearProgress />
          <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
            Loading system status...
          </Typography>
        </Container>
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title="System Status"
      description="Real-time status of SmartProBono services"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Overall Status */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <SpeedIcon color="primary" />
                <Typography variant="h5">
                  System Status
                </Typography>
                <ChatIcon color="secondary" />
                <DescriptionIcon color="action" />
              </Box>
              <Chip
                icon={getStatusIcon(systemStatus.overall)}
                label={getStatusText(systemStatus.overall)}
                color={getOverallStatusColor()}
                size="large"
              />
            </Box>
            <Divider sx={{ my: 2 }} />
            <Typography variant="body2" color="text.secondary">
              Last updated: {new Date(systemStatus.lastUpdated).toLocaleString()}
            </Typography>
          </CardContent>
        </Card>

        <Grid container spacing={4}>
          {/* Services Status */}
          <Grid item xs={12} md={8}>
            <Typography variant="h6" gutterBottom>
              Service Status
            </Typography>
            
            <Grid container spacing={2}>
              {systemStatus.services.map((service, index) => (
                <Grid item xs={12} sm={6} key={index}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="subtitle1" fontWeight="bold">
                          {service.name}
                        </Typography>
                        <Chip
                          icon={getStatusIcon(service.status)}
                          label={getStatusText(service.status)}
                          color={getStatusColor(service.status)}
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        Response Time: {service.responseTime}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Grid>

          {/* System Information */}
          <Grid item xs={12} md={4}>
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  System Information
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <CloudIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Infrastructure"
                      secondary="AWS Cloud"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <SecurityIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Security"
                      secondary="SSL/TLS Encrypted"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <StorageIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Database"
                      secondary="Supabase PostgreSQL"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <ApiIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="API Version"
                      secondary="v3.0.0"
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>

            {/* Performance Metrics */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Performance Metrics
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Average Response Time
                  </Typography>
                  <Typography variant="h6" color="primary">
                    150ms
                  </Typography>
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Uptime (30 days)
                  </Typography>
                  <Typography variant="h6" color="success.main">
                    99.9%
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Active Users
                  </Typography>
                  <Typography variant="h6" color="primary">
                    1,247
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Recent Incidents */}
        {systemStatus.incidents.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Recent Incidents
            </Typography>
            {systemStatus.incidents.map((incident, index) => (
              <Alert
                key={index}
                severity={incident.severity}
                sx={{ mb: 2 }}
              >
                <Typography variant="subtitle2">
                  {incident.title}
                </Typography>
                <Typography variant="body2">
                  {incident.description}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {new Date(incident.timestamp).toLocaleString()}
                </Typography>
              </Alert>
            ))}
          </Box>
        )}

        {/* No Incidents Message */}
        {systemStatus.incidents.length === 0 && (
          <Box sx={{ mt: 4 }}>
            <Alert severity="success">
              <Typography variant="subtitle2">
                All Systems Operational
              </Typography>
              <Typography variant="body2">
                No recent incidents or outages to report. All services are running normally.
              </Typography>
            </Alert>
          </Box>
        )}

        {/* Contact Information */}
        <Paper sx={{ p: 3, mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Status Updates
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            We provide real-time status updates and incident notifications. For immediate assistance, contact our support team.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Chip
              icon={<InfoIcon />}
              label="Status Page RSS Feed"
              clickable
              color="primary"
              variant="outlined"
            />
            <Chip
              icon={<InfoIcon />}
              label="Email Notifications"
              clickable
              color="primary"
              variant="outlined"
            />
            <Chip
              icon={<InfoIcon />}
              label="Twitter Updates"
              clickable
              color="primary"
              variant="outlined"
            />
          </Box>
        </Paper>
      </Container>
    </PageLayout>
  );
};

export default StatusPage;


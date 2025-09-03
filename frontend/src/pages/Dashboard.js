import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon, 
  Chip, 
  Divider,
  Alert, 
  IconButton, 
  LinearProgress, 
  Tab, 
  Tabs, 
  Avatar, 
  Badge,
  Stack
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { 
  PageLayout, 
  Section, 
  Button, 
  Card, 
  CardContent,
  designTokens 
} from '../design-system';
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
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import GavelIcon from '@mui/icons-material/Gavel';
import ChatIcon from '@mui/icons-material/Chat';
import DocumentScannerIcon from '@mui/icons-material/DocumentScanner';

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
        <Box sx={{ pt: designTokens.spacing[6] }}>
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
    const fetchData = async () => {
      setLoading(true);
      
      // Mock data
      const mockDocuments = [
        { id: 1, name: 'Contract Agreement', type: 'Contract', status: 'Draft', date: '2024-01-15' },
        { id: 2, name: 'Employment Agreement', type: 'Employment', status: 'Review', date: '2024-01-14' },
        { id: 3, name: 'NDA Template', type: 'Template', status: 'Complete', date: '2024-01-13' },
      ];

      const mockNotifications = [
        { id: 1, message: 'New legal document template available', type: 'info', time: '2 hours ago' },
        { id: 2, message: 'Contract review deadline approaching', type: 'warning', time: '1 day ago' },
        { id: 3, message: 'Document signed successfully', type: 'success', time: '2 days ago' },
      ];

      const mockDeadlines = [
        { id: 1, title: 'Contract Review', date: '2024-01-20', type: 'urgent' },
        { id: 2, title: 'Legal Consultation', date: '2024-01-25', type: 'normal' },
        { id: 3, title: 'Document Submission', date: '2024-01-30', type: 'normal' },
      ];

      setTimeout(() => {
        setDocuments(mockDocuments);
        setNotifications(mockNotifications);
        setUpcomingDeadlines(mockDeadlines);
        setLoading(false);
      }, 1000);
    };

    fetchData();
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Complete': return 'success';
      case 'Review': return 'warning';
      case 'Draft': return 'info';
      default: return 'default';
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'info': return <NotificationsIcon />;
      case 'warning': return <WarningIcon />;
      case 'success': return <CheckCircleIcon />;
      default: return <NotificationsIcon />;
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case 'info': return designTokens.colors.info[500];
      case 'warning': return designTokens.colors.warning[500];
      case 'success': return designTokens.colors.success[500];
      default: return designTokens.colors.neutral[500];
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  if (loading) {
    return (
      <PageLayout background="light" padding="normal">
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
          <LinearProgress sx={{ width: '100%', maxWidth: 400 }} />
        </Box>
      </PageLayout>
    );
  }

  return (
    <PageLayout background="light" padding="normal">
      {/* Welcome Section */}
      <Section variant="hero" background="gradient" header={false}>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <Box sx={{ textAlign: 'center', py: designTokens.spacing[8] }}>
            <motion.div variants={itemVariants}>
              <Typography
                variant="h2"
                sx={{
                  fontWeight: designTokens.typography.fontWeight.bold,
                  color: 'white',
                  mb: designTokens.spacing[4],
                  textShadow: '0 2px 8px rgba(0,0,0,0.3)',
                }}
              >
                Welcome back, {currentUser?.first_name || 'User'}!
              </Typography>
              <Typography
                variant="h5"
                sx={{
                  color: 'rgba(255, 255, 255, 0.9)',
                  mb: designTokens.spacing[6],
                  textShadow: '0 1px 4px rgba(0,0,0,0.3)',
                }}
              >
                Here's what's happening with your legal matters
              </Typography>
              <Alert severity="info" sx={{ mb: 2, maxWidth: 600, mx: 'auto' }}>
                <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Welcome to your personalized legal assistance dashboard
              </Alert>
              <IconButton sx={{ color: 'white', mt: 2 }}>
                <SettingsIcon />
              </IconButton>
            </motion.div>
          </Box>
        </motion.div>
      </Section>

      {/* Quick Actions */}
      <Section variant="default" background="white" header={false}>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <Box sx={{ mb: designTokens.spacing[8] }}>
            <Typography
              variant="h4"
              sx={{
                fontWeight: designTokens.typography.fontWeight.bold,
                color: designTokens.colors.neutral[800],
                mb: designTokens.spacing[6],
                textAlign: 'center',
              }}
            >
              Quick Actions
            </Typography>
            <Grid container spacing={designTokens.spacing[4]}>
              {[
                { title: 'AI Legal Chat', icon: <ChatIcon />, path: '/legal-chat', color: 'primary' },
                { title: 'Scan Document', icon: <DocumentScannerIcon />, path: '/scan-document', color: 'secondary' },
                { title: 'Legal Templates', icon: <DescriptionIcon />, path: '/templates', color: 'success' },
                { title: 'Case Tracking', icon: <GavelIcon />, path: '/cases', color: 'warning' },
              ].map((action, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                  <motion.div variants={itemVariants}>
                    <Card
                      variant="default"
                      hoverable
                      sx={{
                        textAlign: 'center',
                        cursor: 'pointer',
                        height: '100%',
                        '&:hover': {
                          transform: 'translateY(-4px)',
                        },
                      }}
                      onClick={() => navigate(action.path)}
                    >
                      <CardContent sx={{ p: designTokens.spacing[6] }}>
                        <Badge badgeContent={action.badge || 0} color="error">
                          <Box
                            sx={{
                              width: 60,
                              height: 60,
                              borderRadius: '50%',
                              background: designTokens.gradients[action.color] || designTokens.gradients.primary,
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              margin: '0 auto',
                              mb: designTokens.spacing[4],
                            }}
                          >
                            {React.cloneElement(action.icon, { 
                              sx: { fontSize: 30, color: 'white' } 
                            })}
                          </Box>
                        </Badge>
                        <Typography
                          variant="h6"
                          sx={{
                            fontWeight: designTokens.typography.fontWeight.semibold,
                            color: designTokens.colors.neutral[800],
                          }}
                        >
                          {action.title}
                        </Typography>
                      </CardContent>
                    </Card>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </Box>
        </motion.div>
      </Section>

      {/* Dashboard Content */}
      <Section variant="default" background="light" header={false}>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <Card variant="elevated" sx={{ p: designTokens.spacing[6] }}>
            <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
              <Typography variant="h6">Dashboard Sections:</Typography>
            </Stack>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              sx={{
                borderBottom: 1,
                borderColor: 'divider',
                mb: designTokens.spacing[6],
              }}
            >
              <Tab label="Overview" />
              <Tab label="Documents" />
              <Tab label="Notifications" />
              <Tab label="Deadlines" />
            </Tabs>

            <TabPanel value={tabValue} index={0}>
              <Grid container spacing={designTokens.spacing[6]}>
                {/* Stats Cards */}
                <Grid item xs={12} md={4}>
                  <motion.div variants={itemVariants}>
                    <Card variant="gradient" sx={{ textAlign: 'center', p: designTokens.spacing[6] }}>
                      <ArticleIcon sx={{ fontSize: 48, color: designTokens.colors.success[500], mb: designTokens.spacing[3] }} />
                      <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold, mb: designTokens.spacing[2] }}>
                        {documents.length}
                      </Typography>
                      <Typography variant="body1" color="text.secondary">
                        Active Documents
                      </Typography>
                    </Card>
                  </motion.div>
                </Grid>
                <Grid item xs={12} md={4}>
                  <motion.div variants={itemVariants}>
                    <Card variant="gradient" sx={{ textAlign: 'center', p: designTokens.spacing[6] }}>
                      <AssignmentIcon sx={{ fontSize: 48, color: designTokens.colors.primary[500], mb: designTokens.spacing[3] }} />
                      <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold, mb: designTokens.spacing[2] }}>
                        {documents.filter(doc => doc.status === 'Complete').length}
                      </Typography>
                      <Typography variant="body1" color="text.secondary">
                        Completed Tasks
                      </Typography>
                    </Card>
                  </motion.div>
                </Grid>
                <Grid item xs={12} md={4}>
                  <motion.div variants={itemVariants}>
                    <Card variant="gradient" sx={{ textAlign: 'center', p: designTokens.spacing[6] }}>
                      <AccessTimeIcon sx={{ fontSize: 48, color: designTokens.colors.warning[500], mb: designTokens.spacing[3] }} />
                      <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold, mb: designTokens.spacing[2] }}>
                        {upcomingDeadlines.length}
                      </Typography>
                      <Typography variant="body1" color="text.secondary">
                        Upcoming Deadlines
                      </Typography>
                    </Card>
                  </motion.div>
                </Grid>
              </Grid>
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <motion.div variants={itemVariants}>
                <List>
                  {documents.map((doc, index) => (
                    <React.Fragment key={doc.id}>
                      <ListItem
                        sx={{
                          p: designTokens.spacing[4],
                          borderRadius: designTokens.borderRadius.md,
                          '&:hover': {
                            backgroundColor: designTokens.colors.neutral[50],
                          },
                        }}
                      >
                        <ListItemIcon>
                          <DescriptionIcon sx={{ color: designTokens.colors.primary[500] }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="h6" sx={{ fontWeight: designTokens.typography.fontWeight.semibold }}>
                              {doc.name}
                            </Typography>
                          }
                          secondary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: designTokens.spacing[2], mt: designTokens.spacing[1] }}>
                              <Chip
                                label={doc.type}
                                size="small"
                                variant="outlined"
                                sx={{ fontSize: '0.75rem' }}
                              />
                              <Chip
                                label={doc.status}
                                size="small"
                                color={getStatusColor(doc.status)}
                                sx={{ fontSize: '0.75rem' }}
                              />
                              <Typography variant="caption" color="text.secondary">
                                {doc.date}
                              </Typography>
                            </Box>
                          }
                        />
                        <Button variant="outlined" size="small" sx={{ mr: 1 }}>
                          View
                        </Button>
                        <IconButton>
                          <MoreVertIcon />
                        </IconButton>
                      </ListItem>
                      {index < documents.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </motion.div>
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <motion.div variants={itemVariants}>
                <List>
                  {notifications.map((notification, index) => (
                    <React.Fragment key={notification.id}>
                      <ListItem
                        sx={{
                          p: designTokens.spacing[4],
                          borderRadius: designTokens.borderRadius.md,
                          '&:hover': {
                            backgroundColor: designTokens.colors.neutral[50],
                          },
                        }}
                      >
                        <ListItemIcon>
                          <Avatar sx={{ backgroundColor: getNotificationColor(notification.type), width: 40, height: 40 }}>
                            {getNotificationIcon(notification.type)}
                          </Avatar>
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="body1" sx={{ fontWeight: designTokens.typography.fontWeight.medium }}>
                              {notification.message}
                            </Typography>
                          }
                          secondary={
                            <Typography variant="caption" color="text.secondary">
                              {notification.time}
                            </Typography>
                          }
                        />
                      </ListItem>
                      {index < notifications.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </motion.div>
            </TabPanel>

            <TabPanel value={tabValue} index={3}>
              <motion.div variants={itemVariants}>
                <List>
                  {upcomingDeadlines.map((deadline, index) => (
                    <React.Fragment key={deadline.id}>
                      <ListItem
                        sx={{
                          p: designTokens.spacing[4],
                          borderRadius: designTokens.borderRadius.md,
                          '&:hover': {
                            backgroundColor: designTokens.colors.neutral[50],
                          },
                        }}
                      >
                        <ListItemIcon>
                          <EventNoteIcon sx={{ color: deadline.type === 'urgent' ? designTokens.colors.error[500] : designTokens.colors.primary[500] }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="h6" sx={{ fontWeight: designTokens.typography.fontWeight.semibold }}>
                              {deadline.title}
                            </Typography>
                          }
                          secondary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: designTokens.spacing[2], mt: designTokens.spacing[1] }}>
                              <Chip
                                label={deadline.date}
                                size="small"
                                color={deadline.type === 'urgent' ? 'error' : 'default'}
                                sx={{ fontSize: '0.75rem' }}
                              />
                              {deadline.type === 'urgent' && (
                                <Chip
                                  label="Urgent"
                                  size="small"
                                  color="error"
                                  sx={{ fontSize: '0.75rem' }}
                                />
                              )}
                            </Box>
                          }
                        />
                      </ListItem>
                      {index < upcomingDeadlines.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </motion.div>
            </TabPanel>
          </Card>
        </motion.div>
      </Section>
    </PageLayout>
  );
};

export default Dashboard;
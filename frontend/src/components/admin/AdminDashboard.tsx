import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Tab,
  Tabs,
  CircularProgress,
  Alert
} from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import { api } from '../../services/api';
import UserManagement from './UserManagement';
import SystemSettings from './SystemSettings';
import PerformanceMetrics from './PerformanceMetrics';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`admin-tabpanel-${index}`}
      aria-labelledby={`admin-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const AdminDashboard: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    // Check admin access
    if (user?.role !== 'admin') {
      setError('Access denied. Admin privileges required.');
    }
  }, [user]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ width: '100%', mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Admin Dashboard
        </Typography>

        <Paper sx={{ width: '100%', mb: 2 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
          >
            <Tab label="User Management" />
            <Tab label="System Settings" />
            <Tab label="Performance Metrics" />
          </Tabs>

          <TabPanel value={tabValue} index={0}>
            <UserManagement />
          </TabPanel>
          <TabPanel value={tabValue} index={1}>
            <SystemSettings />
          </TabPanel>
          <TabPanel value={tabValue} index={2}>
            <PerformanceMetrics />
          </TabPanel>
        </Paper>
      </Box>
    </Container>
  );
};

export default AdminDashboard; 
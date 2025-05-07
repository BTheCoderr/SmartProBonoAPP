import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import AnalyticsService from '../../services/AnalyticsService';

const AnalyticsOverview = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState({
    formStats: null,
    completionRates: null,
    recentActivity: null,
  });

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [formStats, completionRates] = await Promise.all([
        AnalyticsService.getDashboardStats(),
        AnalyticsService.getFormAnalytics('all', '7d'),
      ]);

      setData({
        formStats,
        completionRates,
        recentActivity: formStats.recentActivity || [],
      });
    } catch (err) {
      setError('Failed to load analytics data');
      console.error('Analytics load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderStats = () => {
    const { formStats } = data;
    if (!formStats) return null;

    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Form Views
              </Typography>
              <Typography variant="h4">
                {formStats.totalViews}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Users
              </Typography>
              <Typography variant="h4">
                {formStats.activeUsers}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Completion Rate
              </Typography>
              <Typography variant="h4">
                {formStats.completionRate}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg. Time to Complete
              </Typography>
              <Typography variant="h4">
                {Math.round(formStats.avgCompletionTime / 60)} min
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderCompletionChart = () => {
    const { completionRates } = data;
    if (!completionRates?.daily) return null;

    return (
      <Box sx={{ height: 300, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Daily Completion Rates
        </Typography>
        <ResponsiveContainer>
          <LineChart data={completionRates.daily}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="completionRate"
              stroke="#8884d8"
              name="Completion Rate (%)"
            />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    );
  };

  const renderRecentActivity = () => {
    const { recentActivity } = data;
    if (!recentActivity?.length) return null;

    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Form Activity
        </Typography>
        <ResponsiveContainer height={300}>
          <BarChart data={recentActivity}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="hour" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="views" fill="#8884d8" name="Views" />
            <Bar dataKey="starts" fill="#82ca9d" name="Starts" />
            <Bar dataKey="completions" fill="#ffc658" name="Completions" />
          </BarChart>
        </ResponsiveContainer>
      </Box>
    );
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {renderStats()}
      {renderCompletionChart()}
      {renderRecentActivity()}
    </Box>
  );
};

export default AnalyticsOverview; 
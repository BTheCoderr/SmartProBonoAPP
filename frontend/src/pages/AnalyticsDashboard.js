import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Tabs,
  Tab,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Divider,
  Alert
} from '@mui/material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { format } from 'date-fns';
import ApiService from '../services/ApiService';
import AnalyticsOverview from '../components/analytics/AnalyticsOverview';

const AnalyticsDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [selectedForm, setSelectedForm] = useState('all');
  const [dateRange, setDateRange] = useState('7d');
  const [analytics, setAnalytics] = useState({
    formAnalytics: null,
    fieldAnalytics: null,
    abandonmentAnalysis: null,
    successRate: null
  });

  useEffect(() => {
    loadAnalytics();
  }, [selectedForm, dateRange]);

  const loadAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      const [formAnalytics, abandonmentAnalysis, successRate] = await Promise.all([
        ApiService.get(`/api/analytics/forms/${selectedForm}`, { params: { dateRange } }),
        ApiService.get(`/api/analytics/forms/${selectedForm}/abandonment`),
        ApiService.get(`/api/analytics/forms/${selectedForm}/success-rate`, { params: { dateRange } })
      ]);

      setAnalytics({
        formAnalytics: formAnalytics.data,
        abandonmentAnalysis: abandonmentAnalysis.data,
        successRate: successRate.data
      });
    } catch (err) {
      setError('Failed to load analytics data. Please try again later.');
      console.error('Analytics load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleFormChange = (event) => {
    setSelectedForm(event.target.value);
  };

  const handleDateRangeChange = (event) => {
    setDateRange(event.target.value);
  };

  const renderOverviewStats = () => {
    const { formAnalytics } = analytics;
    if (!formAnalytics) return null;

    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Form Views
              </Typography>
              <Typography variant="h4">
                {formAnalytics.total_views}
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
                {((formAnalytics.total_completions / formAnalytics.total_starts) * 100).toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Sessions
              </Typography>
              <Typography variant="h4">
                {formAnalytics.active_sessions}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg. Completion Time
              </Typography>
              <Typography variant="h4">
                {Math.round(formAnalytics.avg_completion_time / 60)} min
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderCompletionChart = () => {
    const { formAnalytics } = analytics;
    if (!formAnalytics) return null;

    const data = [
      { name: 'Started', value: formAnalytics.total_starts },
      { name: 'Completed', value: formAnalytics.total_completions },
      { name: 'Abandoned', value: formAnalytics.total_abandonments }
    ];

    return (
      <Box sx={{ height: 300, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Form Completion Status
        </Typography>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={80}
              fill="#8884d8"
              label
            />
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </Box>
    );
  };

  const renderFieldAnalytics = () => {
    const { formAnalytics } = analytics;
    if (!formAnalytics?.field_completion_rates) return null;

    const data = Object.entries(formAnalytics.field_completion_rates).map(([field, rate]) => ({
      field,
      completionRate: rate * 100
    }));

    return (
      <Box sx={{ height: 400, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Field Completion Rates
        </Typography>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="field" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="completionRate" fill="#82ca9d" name="Completion Rate (%)" />
          </BarChart>
        </ResponsiveContainer>
      </Box>
    );
  };

  const renderAbandonmentAnalysis = () => {
    const { abandonmentAnalysis } = analytics;
    if (!abandonmentAnalysis) return null;

    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Abandonment Analysis
        </Typography>
        <Grid container spacing={3}>
          {abandonmentAnalysis.abandonment_analysis.map((reason) => (
            <Grid item xs={12} md={4} key={reason.reason_type}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    {reason.reason_type}
                  </Typography>
                  <Typography variant="h5">
                    {reason.count} abandonments
                  </Typography>
                  <Typography variant="body2">
                    Avg. Completion: {reason.avg_completion_percentage.toFixed(1)}%
                  </Typography>
                  <Typography variant="body2">
                    Avg. Time Spent: {Math.round(reason.avg_time_spent / 60)} min
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };

  const renderSuccessRate = () => {
    const { successRate } = analytics;
    if (!successRate) return null;

    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Success Rate Analysis
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Overall Success Rate
                </Typography>
                <Typography variant="h4">
                  {((successRate.successful_submissions / successRate.total_attempts) * 100).toFixed(1)}%
                </Typography>
                <Typography variant="body2">
                  {successRate.successful_submissions} out of {successRate.total_attempts} attempts
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Avg. Attempts Before Success
                </Typography>
                <Typography variant="h4">
                  {successRate.avg_attempts_before_success.toFixed(1)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Real-time Success Rate
                </Typography>
                <Typography variant="h4">
                  {successRate.real_time_success_rate.toFixed(1)}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  const renderCompletionTimeDistribution = () => {
    const { successRate } = analytics;
    if (!successRate?.completion_time_distribution) return null;

    const data = successRate.completion_time_distribution.map((time, index) => ({
      time: Math.round(time / 60),
      count: 1
    })).reduce((acc, curr) => {
      const existing = acc.find(item => item.time === curr.time);
      if (existing) {
        existing.count += curr.count;
      } else {
        acc.push(curr);
      }
      return acc;
    }, []).sort((a, b) => a.time - b.time);

    return (
      <Box sx={{ height: 300, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Completion Time Distribution (minutes)
        </Typography>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="count" stroke="#8884d8" name="Number of Submissions" />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    );
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Box sx={{ mb: 3 }}>
          <Typography variant="h4" gutterBottom>
            Analytics Dashboard
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Form Type</InputLabel>
                <Select
                  value={selectedForm}
                  onChange={handleFormChange}
                  label="Form Type"
                >
                  <MenuItem value="all">All Forms</MenuItem>
                  <MenuItem value="small_claims">Small Claims</MenuItem>
                  <MenuItem value="fee_waiver">Fee Waiver</MenuItem>
                  <MenuItem value="eviction_response">Eviction Response</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Date Range</InputLabel>
                <Select
                  value={dateRange}
                  onChange={handleDateRangeChange}
                  label="Date Range"
                >
                  <MenuItem value="7d">Last 7 Days</MenuItem>
                  <MenuItem value="30d">Last 30 Days</MenuItem>
                  <MenuItem value="90d">Last 90 Days</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <Button
                fullWidth
                variant="contained"
                onClick={loadAnalytics}
                disabled={loading}
              >
                Refresh Data
              </Button>
            </Grid>
          </Grid>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <Tabs
              value={activeTab}
              onChange={handleTabChange}
              indicatorColor="primary"
              textColor="primary"
              variant="fullWidth"
              sx={{ mb: 3 }}
            >
              <Tab label="Overview" />
              <Tab label="Form Details" />
              <Tab label="Field Analysis" />
              <Tab label="User Behavior" />
            </Tabs>

            <Box hidden={activeTab !== 0}>
              <AnalyticsOverview />
            </Box>

            <Box hidden={activeTab !== 1}>
              {renderOverviewStats()}
              {renderCompletionChart()}
            </Box>

            <Box hidden={activeTab !== 2}>
              {renderFieldAnalytics()}
            </Box>

            <Box hidden={activeTab !== 3}>
              {renderAbandonmentAnalysis()}
              {renderSuccessRate()}
              {renderCompletionTimeDistribution()}
            </Box>
          </>
        )}
      </Paper>
    </Container>
  );
};

export default AnalyticsDashboard; 
import React from 'react';
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from 'recharts';
import { Box, Grid, Paper, Typography, CircularProgress } from '@mui/material';
import useRealTimeAnalytics from '../../hooks/useRealTimeAnalytics';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const AnalyticsDashboard = ({ formType }) => {
  const { realTimeData, isConnected } = useRealTimeAnalytics(formType);

  if (!isConnected) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  const {
    activeUsers,
    recentSubmissions,
    fieldCompletionRates,
    errorRates,
    averageCompletionTime
  } = realTimeData;

  // Transform field completion rates for visualization
  const fieldCompletionData = Object.entries(fieldCompletionRates).map(([field, rate]) => ({
    name: field,
    rate
  }));

  // Transform error rates for visualization
  const errorRatesData = Object.entries(errorRates).map(([type, rate]) => ({
    name: type,
    value: rate
  }));

  // Transform recent submissions for timeline
  const submissionTimeline = recentSubmissions.map(submission => ({
    time: new Date(submission.timestamp).toLocaleTimeString(),
    completed: 1
  }));

  return (
    <Box p={3}>
      <Grid container spacing={3}>
        {/* Active Users Card */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6" color="textSecondary">
              Active Users
            </Typography>
            <Typography variant="h3">
              {activeUsers}
            </Typography>
          </Paper>
        </Grid>

        {/* Average Completion Time Card */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6" color="textSecondary">
              Avg. Completion Time
            </Typography>
            <Typography variant="h3">
              {Math.round(averageCompletionTime / 1000)}s
            </Typography>
          </Paper>
        </Grid>

        {/* Field Completion Rates Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Field Completion Rates
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={fieldCompletionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="rate" fill="#8884d8" name="Completion Rate %" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Error Distribution Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Error Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={errorRatesData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {errorRatesData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Submission Timeline Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Submissions Timeline
            </Typography>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={submissionTimeline}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="completed"
                  stroke="#82ca9d"
                  name="Submissions"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AnalyticsDashboard; 
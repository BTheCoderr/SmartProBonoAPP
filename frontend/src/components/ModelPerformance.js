import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';

const ModelPerformance = () => {
  const [performanceData, setPerformanceData] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedModel, setSelectedModel] = useState('all');
  const [error, setError] = useState(null);

  const models = ['all', 'mistral', 'llama', 'falcon', 'openai'];

  useEffect(() => {
    fetchPerformanceData();
    // Refresh every 5 minutes
    const interval = setInterval(fetchPerformanceData, 300000);
    return () => clearInterval(interval);
  }, [selectedModel, fetchPerformanceData]);

  const fetchPerformanceData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/performance/${selectedModel}`);
      setPerformanceData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch performance data');
      console.error('Error fetching performance data:', err);
    } finally {
      setLoading(false);
    }
  };

  const MetricCard = ({ title, value, unit = '' }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          {title}
        </Typography>
        <Typography variant="h5" component="div">
          {typeof value === 'number' ? value.toFixed(2) : value}
          {unit}
        </Typography>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={2}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box p={2}>
      <Box mb={3}>
        <FormControl fullWidth>
          <InputLabel>Select Model</InputLabel>
          <Select
            value={selectedModel}
            onChange={e => setSelectedModel(e.target.value)}
            label="Select Model"
          >
            {models.map(model => (
              <MenuItem key={model} value={model}>
                {model.charAt(0).toUpperCase() + model.slice(1)}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Average Response Time"
            value={performanceData.average_response_time}
            unit="s"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard title="Success Rate" value={performanceData.success_rate} unit="%" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard title="Total Requests" value={performanceData.total_requests} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard title="Error Rate" value={performanceData.error_rate} unit="%" />
        </Grid>
      </Grid>
    </Box>
  );
};

export default ModelPerformance;

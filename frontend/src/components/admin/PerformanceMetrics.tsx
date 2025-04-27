import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Typography,
  CircularProgress,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import api from '../../services/api';

interface MetricData {
  timestamp: string;
  value: number;
}

interface PerformanceData {
  api_response_times: MetricData[];
  error_rates: MetricData[];
  active_users: MetricData[];
  memory_usage: MetricData[];
  cpu_usage: MetricData[];
  database_queries: MetricData[];
}

const PerformanceMetrics: React.FC = () => {
  const [metrics, setMetrics] = useState<PerformanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<'1h' | '24h' | '7d' | '30d'>('24h');

  useEffect(() => {
    fetchMetrics();
  }, [timeRange]);

  const fetchMetrics = async () => {
    try {
      const response = await api.get('/api/admin/metrics', {
        params: { range: timeRange }
      });
      setMetrics(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch performance metrics');
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return timeRange === '1h'
      ? date.toLocaleTimeString()
      : date.toLocaleDateString();
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

  if (!metrics) {
    return <Alert severity="error">No metrics data available</Alert>;
  }

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Time Range</InputLabel>
          <Select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as typeof timeRange)}
            label="Time Range"
          >
            <MenuItem value="1h">Last Hour</MenuItem>
            <MenuItem value="24h">Last 24 Hours</MenuItem>
            <MenuItem value="7d">Last 7 Days</MenuItem>
            <MenuItem value="30d">Last 30 Days</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="API Response Times" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics.api_response_times}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={formatTimestamp}
                  />
                  <YAxis />
                  <Tooltip
                    labelFormatter={formatTimestamp}
                    formatter={(value: number) => [`${value.toFixed(2)}ms`, 'Response Time']}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#8884d8"
                    name="Response Time"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Error Rates" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics.error_rates}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={formatTimestamp}
                  />
                  <YAxis />
                  <Tooltip
                    labelFormatter={formatTimestamp}
                    formatter={(value: number) => [`${value.toFixed(2)}%`, 'Error Rate']}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#ff5252"
                    name="Error Rate"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Active Users" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics.active_users}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={formatTimestamp}
                  />
                  <YAxis />
                  <Tooltip
                    labelFormatter={formatTimestamp}
                    formatter={(value: number) => [value, 'Active Users']}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#4caf50"
                    name="Active Users"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="System Resources" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics.cpu_usage}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={formatTimestamp}
                  />
                  <YAxis />
                  <Tooltip
                    labelFormatter={formatTimestamp}
                    formatter={(value: number) => [`${value.toFixed(1)}%`, '']}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#ff9800"
                    name="CPU Usage"
                  />
                  <Line
                    type="monotone"
                    data={metrics.memory_usage}
                    dataKey="value"
                    stroke="#2196f3"
                    name="Memory Usage"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardHeader title="Database Performance" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics.database_queries}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={formatTimestamp}
                  />
                  <YAxis />
                  <Tooltip
                    labelFormatter={formatTimestamp}
                    formatter={(value: number) => [`${value.toFixed(2)}ms`, 'Query Time']}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#9c27b0"
                    name="Query Response Time"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PerformanceMetrics; 
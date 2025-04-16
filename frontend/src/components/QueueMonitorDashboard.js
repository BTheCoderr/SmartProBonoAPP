import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
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

const QueueMonitorDashboard = () => {
  const [queueStats, setQueueStats] = useState(null);
  const [queueHistory, setQueueHistory] = useState([]);
  const [lawyerPerformance, setLawyerPerformance] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const { socket } = useWebSocket();

  useEffect(() => {
    // Initial data fetch
    fetchQueueData();

    // Set up real-time updates
    if (socket) {
      socket.on('queue_update', handleQueueUpdate);
      return () => socket.off('queue_update', handleQueueUpdate);
    }
  }, [socket]);

  const fetchQueueData = async () => {
    try {
      const [statsRes, historyRes, performanceRes] = await Promise.all([
        fetch('/api/priority-queue/status'),
        fetch('/api/priority-queue/analytics'),
        fetch('/api/priority-queue/audit')
      ]);

      const stats = await statsRes.json();
      const history = await historyRes.json();
      const performance = await performanceRes.json();

      setQueueStats(stats);
      setQueueHistory(history);
      setLawyerPerformance(performance);
      setError(null);
    } catch (err) {
      setError('Failed to fetch queue data');
      console.error('Error fetching queue data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleQueueUpdate = (data) => {
    setQueueStats(prev => ({
      ...prev,
      ...data
    }));
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Queue Monitor Dashboard
      </Typography>

      {/* Current Queue Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Cases
              </Typography>
              <Typography variant="h4">
                {queueStats?.total_cases || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Urgent Cases
              </Typography>
              <Typography variant="h4" color="error">
                {queueStats?.urgent_cases || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Wait Time
              </Typography>
              <Typography variant="h4">
                {queueStats?.average_wait_time?.toFixed(1) || 0} min
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Success Rate
              </Typography>
              <Typography variant="h4">
                {queueStats?.success_rate?.toFixed(1) || 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Queue History Chart */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Queue History
          </Typography>
          <Box sx={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={queueHistory}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="total_cases" stroke="#8884d8" />
                <Line type="monotone" dataKey="urgent_cases" stroke="#ff0000" />
                <Line type="monotone" dataKey="high_cases" stroke="#ffa500" />
                <Line type="monotone" dataKey="medium_cases" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        </CardContent>
      </Card>

      {/* Lawyer Performance Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Lawyer Performance
          </Typography>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Lawyer</TableCell>
                <TableCell align="right">Cases Handled</TableCell>
                <TableCell align="right">Avg. Response Time</TableCell>
                <TableCell align="right">Success Rate</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {lawyerPerformance.map((lawyer) => (
                <TableRow key={lawyer.id}>
                  <TableCell>{lawyer.name}</TableCell>
                  <TableCell align="right">{lawyer.cases_handled}</TableCell>
                  <TableCell align="right">
                    {lawyer.avg_response_time.toFixed(1)} min
                  </TableCell>
                  <TableCell align="right">
                    {(lawyer.success_rate * 100).toFixed(1)}%
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </Box>
  );
};

export default QueueMonitorDashboard; 
import React, { useEffect, useState } from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
    CircularProgress,
    Alert,
    Card,
    CardContent,
    CardHeader,
    Tabs,
    Tab,
    useTheme
} from '@mui/material';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell
} from 'recharts';
import { analytics } from '../../services/analytics';
import { format } from 'date-fns';

interface MetricsData {
    performance: {
        responseTime: number;
        errorRate: number;
        cpuUsage: number;
        memoryUsage: number;
    };
    users: {
        activeUsers: number;
        newUsers: number;
        concurrentUsers: number;
    };
    documents: {
        generationSuccess: number;
        generationFailure: number;
        averageProcessingTime: number;
    };
    forms: {
        completionRate: number;
        averageCompletionTime: number;
        abandonmentRate: number;
    };
}

const Dashboard: React.FC = () => {
    const theme = useTheme();
    const [metrics, setMetrics] = useState<MetricsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [timeRange, setTimeRange] = useState('24h');
    const [activeTab, setActiveTab] = useState(0);

    useEffect(() => {
        fetchMetrics();
        const interval = setInterval(fetchMetrics, 60000); // Refresh every minute
        return () => clearInterval(interval);
    }, [timeRange]);

    const fetchMetrics = async () => {
        try {
            const response = await fetch(`/api/analytics/metrics?timeRange=${timeRange}`);
            if (!response.ok) throw new Error('Failed to fetch metrics');
            const data = await response.json();
            setMetrics(data);
            setError(null);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error}</Alert>;
    if (!metrics) return null;

    const PerformanceMetrics = () => (
        <Card>
            <CardHeader title="Performance Metrics" />
            <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={metrics.performance.history}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="timestamp" tickFormatter={(time) => format(time, 'HH:mm')} />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="responseTime" stroke={theme.palette.primary.main} />
                        <Line type="monotone" dataKey="cpuUsage" stroke={theme.palette.secondary.main} />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );

    const UserMetrics = () => (
        <Card>
            <CardHeader title="User Activity" />
            <CardContent>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <Typography variant="h6">Active Users</Typography>
                        <Typography variant="h4">{metrics.users.activeUsers}</Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="h6">New Users</Typography>
                        <Typography variant="h4">{metrics.users.newUsers}</Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="h6">Concurrent Users</Typography>
                        <Typography variant="h4">{metrics.users.concurrentUsers}</Typography>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );

    const DocumentMetrics = () => (
        <Card>
            <CardHeader title="Document Processing" />
            <CardContent>
                <Grid container spacing={2}>
                    <Grid item xs={6}>
                        <PieChart width={200} height={200}>
                            <Pie
                                data={[
                                    { name: 'Success', value: metrics.documents.generationSuccess },
                                    { name: 'Failure', value: metrics.documents.generationFailure }
                                ]}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={80}
                                paddingAngle={5}
                            >
                                <Cell fill={theme.palette.success.main} />
                                <Cell fill={theme.palette.error.main} />
                            </Pie>
                        </PieChart>
                    </Grid>
                    <Grid item xs={6}>
                        <Typography variant="h6">Avg. Processing Time</Typography>
                        <Typography variant="h4">
                            {metrics.documents.averageProcessingTime.toFixed(2)}s
                        </Typography>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );

    const FormMetrics = () => (
        <Card>
            <CardHeader title="Form Analytics" />
            <CardContent>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <Typography variant="h6">Completion Rate</Typography>
                        <Typography variant="h4">
                            {(metrics.forms.completionRate * 100).toFixed(1)}%
                        </Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="h6">Avg. Completion Time</Typography>
                        <Typography variant="h4">
                            {metrics.forms.averageCompletionTime.toFixed(1)}m
                        </Typography>
                    </Grid>
                    <Grid item xs={4}>
                        <Typography variant="h6">Abandonment Rate</Typography>
                        <Typography variant="h4">
                            {(metrics.forms.abandonmentRate * 100).toFixed(1)}%
                        </Typography>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Analytics Dashboard
            </Typography>
            
            <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 3 }}>
                <Tab label="Overview" />
                <Tab label="Performance" />
                <Tab label="Users" />
                <Tab label="Documents" />
                <Tab label="Forms" />
            </Tabs>

            <Grid container spacing={3}>
                {activeTab === 0 && (
                    <>
                        <Grid item xs={12}>
                            <UserMetrics />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <DocumentMetrics />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <FormMetrics />
                        </Grid>
                    </>
                )}
                
                {activeTab === 1 && (
                    <Grid item xs={12}>
                        <PerformanceMetrics />
                    </Grid>
                )}
                
                {activeTab === 2 && (
                    <Grid item xs={12}>
                        <UserMetrics />
                    </Grid>
                )}
                
                {activeTab === 3 && (
                    <Grid item xs={12}>
                        <DocumentMetrics />
                    </Grid>
                )}
                
                {activeTab === 4 && (
                    <Grid item xs={12}>
                        <FormMetrics />
                    </Grid>
                )}
            </Grid>
        </Box>
    );
};

export default Dashboard; 
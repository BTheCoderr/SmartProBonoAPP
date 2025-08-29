import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '../components/ui/tabs';
import { Badge } from '../components/ui/badge';
import { Alert, AlertDescription } from '../components/ui/alert';
import { useToast } from '../hooks/use-toast';
import { 
  Shield, 
  Activity, 
  AlertTriangle, 
  Clock, 
  Download,
  Filter,
  RefreshCw,
  Eye,
  EyeOff
} from 'lucide-react';

const AuditDashboard = () => {
  const [auditLogs, setAuditLogs] = useState([]);
  const [securityEvents, setSecurityEvents] = useState([]);
  const [userActivities, setUserActivities] = useState([]);
  const [dashboardStats, setDashboardStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    event_type: '',
    user_id: '',
    start_date: '',
    end_date: '',
    limit: 100,
    severity: ''
  });
  const [selectedTab, setSelectedTab] = useState('overview');
  const [showSensitiveData, setShowSensitiveData] = useState(false);
  const { toast } = useToast();

  // Fetch dashboard statistics
  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('/api/audit/dashboard/stats?hours=24', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setDashboardStats(data.data);
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  // Fetch audit logs
  const fetchAuditLogs = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const response = await fetch(`/api/audit/logs?${params}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAuditLogs(data.data);
      } else {
        toast({
          title: "Error",
          description: "Failed to fetch audit logs",
          variant: "destructive"
        });
      }
    } catch (error) {
      console.error('Error fetching audit logs:', error);
      toast({
        title: "Error",
        description: "Failed to fetch audit logs",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  // Fetch security events
  const fetchSecurityEvents = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.severity) params.append('severity', filters.severity);
      if (filters.start_date) params.append('start_date', filters.start_date);
      if (filters.end_date) params.append('end_date', filters.end_date);
      if (filters.limit) params.append('limit', filters.limit);

      const response = await fetch(`/api/audit/security-events?${params}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSecurityEvents(data.data);
      }
    } catch (error) {
      console.error('Error fetching security events:', error);
    }
  };

  // Export audit logs
  const exportAuditLogs = async () => {
    try {
      const exportData = {
        event_type: filters.event_type || null,
        user_id: filters.user_id || null,
        start_date: filters.start_date || null,
        end_date: filters.end_date || null,
        format: 'csv'
      };

      const response = await fetch('/api/audit/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(exportData)
      });
      
      if (response.ok) {
        const data = await response.json();
        
        // Create and download CSV file
        const blob = new Blob([data.data.content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.data.filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        toast({
          title: "Success",
          description: `Exported ${data.data.count} audit logs`
        });
      }
    } catch (error) {
      console.error('Error exporting audit logs:', error);
      toast({
        title: "Error",
        description: "Failed to export audit logs",
        variant: "destructive"
      });
    }
  };

  // Load data on component mount and when filters change
  useEffect(() => {
    fetchDashboardStats();
  }, []);

  useEffect(() => {
    if (selectedTab === 'logs') {
      fetchAuditLogs();
    } else if (selectedTab === 'security') {
      fetchSecurityEvents();
    }
  }, [selectedTab, filters]);

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'destructive';
      case 'high': return 'destructive';
      case 'medium': return 'secondary';
      case 'low': return 'outline';
      default: return 'outline';
    }
  };

  const getEventTypeColor = (eventType) => {
    switch (eventType) {
      case 'security': return 'destructive';
      case 'user_activity': return 'default';
      case 'data_access': return 'secondary';
      case 'performance': return 'outline';
      case 'api_usage': return 'default';
      case 'system': return 'outline';
      default: return 'outline';
    }
  };

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const formatDuration = (ms) => {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Audit Dashboard</h1>
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSensitiveData(!showSensitiveData)}
          >
            {showSensitiveData ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            {showSensitiveData ? 'Hide' : 'Show'} Sensitive Data
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={exportAuditLogs}
          >
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              fetchDashboardStats();
              if (selectedTab === 'logs') fetchAuditLogs();
              if (selectedTab === 'security') fetchSecurityEvents();
            }}
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      <Tabs value={selectedTab} onValueChange={setSelectedTab}>
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="logs">Audit Logs</TabsTrigger>
          <TabsTrigger value="security">Security Events</TabsTrigger>
          <TabsTrigger value="activities">User Activities</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {dashboardStats && (
            <>
              {/* Statistics Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Audit Logs</CardTitle>
                    <Activity className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{dashboardStats.totals.audit_logs}</div>
                    <p className="text-xs text-muted-foreground">Last 24 hours</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Security Events</CardTitle>
                    <Shield className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{dashboardStats.totals.security_events}</div>
                    <p className="text-xs text-muted-foreground">Last 24 hours</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">User Activities</CardTitle>
                    <Activity className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{dashboardStats.totals.user_activities}</div>
                    <p className="text-xs text-muted-foreground">Last 24 hours</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Avg Response Time</CardTitle>
                    <Clock className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{dashboardStats.performance.avg_response_time_ms}ms</div>
                    <p className="text-xs text-muted-foreground">Last 24 hours</p>
                  </CardContent>
                </Card>
              </div>

              {/* Security Events by Severity */}
              <Card>
                <CardHeader>
                  <CardTitle>Security Events by Severity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(dashboardStats.security_by_severity).map(([severity, count]) => (
                      <div key={severity} className="text-center">
                        <Badge variant={getSeverityColor(severity)} className="mb-2">
                          {severity.toUpperCase()}
                        </Badge>
                        <div className="text-2xl font-bold">{count}</div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Top Endpoints */}
              <Card>
                <CardHeader>
                  <CardTitle>Top Endpoints</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {dashboardStats.top_endpoints.map((endpoint, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <span className="font-mono text-sm">{endpoint.endpoint}</span>
                        <Badge variant="outline">{endpoint.count} requests</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>

        <TabsContent value="logs" className="space-y-6">
          {/* Filters */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Filter className="h-5 w-5 mr-2" />
                Filters
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="event_type">Event Type</Label>
                  <Select value={filters.event_type} onValueChange={(value) => setFilters({...filters, event_type: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="All event types" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">All</SelectItem>
                      <SelectItem value="security">Security</SelectItem>
                      <SelectItem value="user_activity">User Activity</SelectItem>
                      <SelectItem value="data_access">Data Access</SelectItem>
                      <SelectItem value="performance">Performance</SelectItem>
                      <SelectItem value="api_usage">API Usage</SelectItem>
                      <SelectItem value="system">System</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="user_id">User ID</Label>
                  <Input
                    id="user_id"
                    type="number"
                    value={filters.user_id}
                    onChange={(e) => setFilters({...filters, user_id: e.target.value})}
                    placeholder="Enter user ID"
                  />
                </div>

                <div>
                  <Label htmlFor="severity">Severity</Label>
                  <Select value={filters.severity} onValueChange={(value) => setFilters({...filters, severity: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="All severities" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">All</SelectItem>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="critical">Critical</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="start_date">Start Date</Label>
                  <Input
                    id="start_date"
                    type="datetime-local"
                    value={filters.start_date}
                    onChange={(e) => setFilters({...filters, start_date: e.target.value})}
                  />
                </div>

                <div>
                  <Label htmlFor="end_date">End Date</Label>
                  <Input
                    id="end_date"
                    type="datetime-local"
                    value={filters.end_date}
                    onChange={(e) => setFilters({...filters, end_date: e.target.value})}
                  />
                </div>

                <div>
                  <Label htmlFor="limit">Limit</Label>
                  <Input
                    id="limit"
                    type="number"
                    value={filters.limit}
                    onChange={(e) => setFilters({...filters, limit: parseInt(e.target.value)})}
                    placeholder="100"
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Audit Logs Table */}
          <Card>
            <CardHeader>
              <CardTitle>Audit Logs</CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <RefreshCw className="h-6 w-6 animate-spin" />
                  <span className="ml-2">Loading audit logs...</span>
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Time</TableHead>
                      <TableHead>Event Type</TableHead>
                      <TableHead>Severity</TableHead>
                      <TableHead>User ID</TableHead>
                      <TableHead>Action</TableHead>
                      <TableHead>Endpoint</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Duration</TableHead>
                      <TableHead>Description</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {auditLogs.map((log) => (
                      <TableRow key={log.id}>
                        <TableCell className="text-sm">
                          {formatDateTime(log.created_at)}
                        </TableCell>
                        <TableCell>
                          <Badge variant={getEventTypeColor(log.event_type)}>
                            {log.event_type}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={getSeverityColor(log.severity)}>
                            {log.severity}
                          </Badge>
                        </TableCell>
                        <TableCell>{log.user_id || '-'}</TableCell>
                        <TableCell className="font-mono text-sm">{log.action}</TableCell>
                        <TableCell className="font-mono text-sm">{log.endpoint || '-'}</TableCell>
                        <TableCell>
                          {log.status_code ? (
                            <Badge variant={log.status_code >= 400 ? 'destructive' : 'outline'}>
                              {log.status_code}
                            </Badge>
                          ) : '-'}
                        </TableCell>
                        <TableCell>
                          {log.processing_time_ms ? formatDuration(log.processing_time_ms) : '-'}
                        </TableCell>
                        <TableCell className="max-w-xs truncate">
                          {log.description || '-'}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-6">
          {/* Security Events Table */}
          <Card>
            <CardHeader>
              <CardTitle>Security Events</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Time</TableHead>
                    <TableHead>Event Type</TableHead>
                    <TableHead>Severity</TableHead>
                    <TableHead>User ID</TableHead>
                    <TableHead>IP Address</TableHead>
                    <TableHead>Blocked</TableHead>
                    <TableHead>Reason</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {securityEvents.map((event) => (
                    <TableRow key={event.id}>
                      <TableCell className="text-sm">
                        {formatDateTime(event.created_at)}
                      </TableCell>
                      <TableCell className="font-mono text-sm">{event.event_type}</TableCell>
                      <TableCell>
                        <Badge variant={getSeverityColor(event.severity)}>
                          {event.severity}
                        </Badge>
                      </TableCell>
                      <TableCell>{event.user_id || '-'}</TableCell>
                      <TableCell className="font-mono text-sm">{event.ip_address || '-'}</TableCell>
                      <TableCell>
                        {event.blocked ? (
                          <Badge variant="destructive">Blocked</Badge>
                        ) : (
                          <Badge variant="outline">Allowed</Badge>
                        )}
                      </TableCell>
                      <TableCell className="max-w-xs truncate">
                        {event.reason || '-'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="activities" className="space-y-6">
          <Alert>
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              User activities are tracked automatically. This feature requires additional implementation.
            </AlertDescription>
          </Alert>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AuditDashboard;

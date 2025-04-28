import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Grid,
  TextField,
  Switch,
  FormControlLabel,
  Button,
  Alert,
  CircularProgress,
  Typography,
  Divider
} from '@mui/material';
import api from '../../services/api';

interface SystemSettings {
  maintenance_mode: boolean;
  max_file_size_mb: number;
  allowed_file_types: string[];
  notification_settings: {
    email_notifications: boolean;
    system_notifications: boolean;
  };
  security_settings: {
    two_factor_required: boolean;
    password_expiry_days: number;
    session_timeout_minutes: number;
  };
  api_settings: {
    rate_limit_per_minute: number;
    max_concurrent_requests: number;
  };
}

const SystemSettings: React.FC = () => {
  const [settings, setSettings] = useState<SystemSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await api.get<{data: SystemSettings}>('/api/admin/settings');
      setSettings(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch system settings');
      setLoading(false);
    }
  };

  const handleSaveSettings = async () => {
    if (!settings) return;

    setSaveStatus('saving');
    try {
      await api.put('/api/admin/settings', settings);
      setSaveStatus('success');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } catch (err) {
      setSaveStatus('error');
      setError('Failed to save settings');
    }
  };

  const handleChange = (path: string[], value: any) => {
    if (!settings) return;

    const newSettings = { ...settings };
    let current: any = newSettings;
    
    for (let i = 0; i < path.length - 1; i++) {
      current = current[path[i]];
    }
    current[path[path.length - 1]] = value;
    
    setSettings(newSettings);
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

  if (!settings) {
    return <Alert severity="error">No settings data available</Alert>;
  }

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardHeader title="General Settings" />
            <CardContent>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.maintenance_mode}
                    onChange={(e) => handleChange(['maintenance_mode'], e.target.checked)}
                  />
                }
                label="Maintenance Mode"
              />
              <TextField
                fullWidth
                label="Max File Size (MB)"
                type="number"
                value={settings.max_file_size_mb}
                onChange={(e) => handleChange(['max_file_size_mb'], parseInt(e.target.value))}
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardHeader title="Notification Settings" />
            <CardContent>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notification_settings.email_notifications}
                    onChange={(e) => handleChange(['notification_settings', 'email_notifications'], e.target.checked)}
                  />
                }
                label="Email Notifications"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notification_settings.system_notifications}
                    onChange={(e) => handleChange(['notification_settings', 'system_notifications'], e.target.checked)}
                  />
                }
                label="System Notifications"
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardHeader title="Security Settings" />
            <CardContent>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.security_settings.two_factor_required}
                    onChange={(e) => handleChange(['security_settings', 'two_factor_required'], e.target.checked)}
                  />
                }
                label="Require Two-Factor Authentication"
              />
              <TextField
                fullWidth
                label="Password Expiry (Days)"
                type="number"
                value={settings.security_settings.password_expiry_days}
                onChange={(e) => handleChange(['security_settings', 'password_expiry_days'], parseInt(e.target.value))}
                sx={{ mt: 2 }}
              />
              <TextField
                fullWidth
                label="Session Timeout (Minutes)"
                type="number"
                value={settings.security_settings.session_timeout_minutes}
                onChange={(e) => handleChange(['security_settings', 'session_timeout_minutes'], parseInt(e.target.value))}
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardHeader title="API Settings" />
            <CardContent>
              <TextField
                fullWidth
                label="Rate Limit (Requests per Minute)"
                type="number"
                value={settings.api_settings.rate_limit_per_minute}
                onChange={(e) => handleChange(['api_settings', 'rate_limit_per_minute'], parseInt(e.target.value))}
              />
              <TextField
                fullWidth
                label="Max Concurrent Requests"
                type="number"
                value={settings.api_settings.max_concurrent_requests}
                onChange={(e) => handleChange(['api_settings', 'max_concurrent_requests'], parseInt(e.target.value))}
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        {saveStatus === 'success' && (
          <Alert severity="success" sx={{ mr: 2 }}>
            Settings saved successfully
          </Alert>
        )}
        {saveStatus === 'error' && (
          <Alert severity="error" sx={{ mr: 2 }}>
            Failed to save settings
          </Alert>
        )}
        <Button
          variant="contained"
          color="primary"
          onClick={handleSaveSettings}
          disabled={saveStatus === 'saving'}
        >
          {saveStatus === 'saving' ? 'Saving...' : 'Save Settings'}
        </Button>
      </Box>
    </Box>
  );
};

export default SystemSettings; 
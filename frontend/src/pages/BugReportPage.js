import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  Alert,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  Divider,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import { BugReport as BugReportIcon, Send as SendIcon } from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const BugReportPage = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    steps: '',
    expected: '',
    actual: '',
    severity: 'medium',
    browser: '',
    device: '',
    email: '',
    canContact: false
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const severities = [
    { value: 'low', label: 'Low', color: 'success', description: 'Minor issue, workaround available' },
    { value: 'medium', label: 'Medium', color: 'warning', description: 'Noticeable issue, affects usability' },
    { value: 'high', label: 'High', color: 'error', description: 'Major issue, significantly impacts functionality' },
    { value: 'critical', label: 'Critical', color: 'error', description: 'System breaking, prevents core functionality' }
  ];

  const browsers = [
    'Chrome',
    'Firefox',
    'Safari',
    'Edge',
    'Other'
  ];

  const devices = [
    'Desktop',
    'Mobile',
    'Tablet',
    'Other'
  ];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleCheckboxChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.checked
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setSubmitted(true);
      setLoading(false);
    }, 1000);
  };

  if (submitted) {
    return (
      <PageLayout
        title="Bug Report Submitted"
        description="Thank you for helping us improve SmartProBono!"
      >
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 6 }}>
              <BugReportIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
              <Typography variant="h4" gutterBottom>
                Report Submitted!
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Thank you for reporting this bug. Our development team will investigate and work on a fix.
              </Typography>
              <Alert severity="info" sx={{ mt: 2, mb: 3 }}>
                If you provided your email, we'll notify you when the issue is resolved.
              </Alert>
              <Button
                variant="contained"
                onClick={() => {
                  setSubmitted(false);
                  setFormData({
                    title: '',
                    description: '',
                    steps: '',
                    expected: '',
                    actual: '',
                    severity: 'medium',
                    browser: '',
                    device: '',
                    email: '',
                    canContact: false
                  });
                }}
                sx={{ mt: 2 }}
              >
                Report Another Bug
              </Button>
            </CardContent>
          </Card>
        </Container>
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title="Bug Report"
      description="Help us fix issues by reporting bugs you encounter"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Report a Bug
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Found something that's not working correctly? Help us fix it by providing detailed information about the issue.
                </Typography>
                
                <Divider sx={{ my: 2 }} />
                
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                  <Grid container spacing={3}>
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Bug Title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        required
                        placeholder="Brief description of the bug"
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth required>
                        <InputLabel>Severity</InputLabel>
                        <Select
                          name="severity"
                          value={formData.severity}
                          onChange={handleChange}
                          label="Severity"
                        >
                          {severities.map((severity) => (
                            <MenuItem key={severity.value} value={severity.value}>
                              <Box>
                                <Chip
                                  label={severity.label}
                                  size="small"
                                  color={severity.color}
                                  sx={{ mr: 1 }}
                                />
                                {severity.description}
                              </Box>
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth>
                        <InputLabel>Browser</InputLabel>
                        <Select
                          name="browser"
                          value={formData.browser}
                          onChange={handleChange}
                          label="Browser"
                        >
                          {browsers.map((browser) => (
                            <MenuItem key={browser} value={browser}>
                              {browser}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth>
                        <InputLabel>Device</InputLabel>
                        <Select
                          name="device"
                          value={formData.device}
                          onChange={handleChange}
                          label="Device"
                        >
                          {devices.map((device) => (
                            <MenuItem key={device} value={device}>
                              {device}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Email (Optional)"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="We'll notify you when this is fixed"
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        multiline
                        rows={3}
                        required
                        placeholder="What happened? Describe the bug in detail."
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Steps to Reproduce"
                        name="steps"
                        value={formData.steps}
                        onChange={handleChange}
                        multiline
                        rows={3}
                        required
                        placeholder="1. Go to... 2. Click on... 3. See error..."
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Expected Behavior"
                        name="expected"
                        value={formData.expected}
                        onChange={handleChange}
                        multiline
                        rows={2}
                        placeholder="What should have happened?"
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Actual Behavior"
                        name="actual"
                        value={formData.actual}
                        onChange={handleChange}
                        multiline
                        rows={2}
                        placeholder="What actually happened?"
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <FormControlLabel
                        control={
                          <Checkbox
                            name="canContact"
                            checked={formData.canContact}
                            onChange={handleCheckboxChange}
                          />
                        }
                        label="I can be contacted for additional information if needed"
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <Button
                        type="submit"
                        variant="contained"
                        size="large"
                        startIcon={<SendIcon />}
                        disabled={loading}
                        sx={{ mt: 2 }}
                      >
                        {loading ? 'Submitting...' : 'Submit Bug Report'}
                      </Button>
                    </Grid>
                  </Grid>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Before Reporting
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Please check:
              </Typography>
              <Box component="ul" sx={{ pl: 2, m: 0 }}>
                <li>Try refreshing the page</li>
                <li>Clear your browser cache</li>
                <li>Check if the issue occurs in another browser</li>
                <li>Make sure you're using the latest version</li>
              </Box>
            </Paper>
            
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                What We Need
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                To fix bugs quickly, we need:
              </Typography>
              <Box component="ul" sx={{ pl: 2, m: 0 }}>
                <li>Clear description of the issue</li>
                <li>Steps to reproduce the problem</li>
                <li>Expected vs actual behavior</li>
                <li>Browser and device information</li>
                <li>Screenshots if applicable</li>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </PageLayout>
  );
};

export default BugReportPage;


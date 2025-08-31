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
  Divider
} from '@mui/material';
import { Send as SendIcon, Lightbulb as LightbulbIcon } from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const FeatureRequestPage = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    priority: 'medium',
    email: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const categories = [
    'User Interface',
    'Legal Features',
    'Document Generation',
    'AI Chat',
    'Analytics',
    'Integration',
    'Performance',
    'Other'
  ];

  const priorities = [
    { value: 'low', label: 'Low', color: 'success' },
    { value: 'medium', label: 'Medium', color: 'warning' },
    { value: 'high', label: 'High', color: 'error' },
    { value: 'critical', label: 'Critical', color: 'error' }
  ];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
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
        title="Feature Request Submitted"
        description="Thank you for your suggestion!"
      >
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 6 }}>
              <LightbulbIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
              <Typography variant="h4" gutterBottom>
                Thank You!
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Your feature request has been submitted successfully. We'll review it and consider it for future updates.
              </Typography>
              <Button
                variant="contained"
                onClick={() => {
                  setSubmitted(false);
                  setFormData({
                    title: '',
                    description: '',
                    category: '',
                    priority: 'medium',
                    email: ''
                  });
                }}
                sx={{ mt: 2 }}
              >
                Submit Another Request
              </Button>
            </CardContent>
          </Card>
        </Container>
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title="Feature Request"
      description="Help us improve SmartProBono by suggesting new features"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Suggest a Feature
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Have an idea for improving SmartProBono? We'd love to hear it! Your suggestions help us build better tools for the legal community.
                </Typography>
                
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                  <Grid container spacing={3}>
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Feature Title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        required
                        placeholder="Brief description of your feature idea"
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth required>
                        <InputLabel>Category</InputLabel>
                        <Select
                          name="category"
                          value={formData.category}
                          onChange={handleChange}
                          label="Category"
                        >
                          {categories.map((category) => (
                            <MenuItem key={category} value={category}>
                              {category}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth>
                        <InputLabel>Priority</InputLabel>
                        <Select
                          name="priority"
                          value={formData.priority}
                          onChange={handleChange}
                          label="Priority"
                        >
                          {priorities.map((priority) => (
                            <MenuItem key={priority.value} value={priority.value}>
                              <Chip
                                label={priority.label}
                                size="small"
                                color={priority.color}
                                sx={{ mr: 1 }}
                              />
                              {priority.label}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Email (Optional)"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="We'll notify you when this feature is implemented"
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Detailed Description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        multiline
                        rows={6}
                        required
                        placeholder="Describe your feature idea in detail. What problem does it solve? How would it work?"
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
                        {loading ? 'Submitting...' : 'Submit Feature Request'}
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
                What We're Looking For
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                We prioritize features that:
              </Typography>
              <Box component="ul" sx={{ pl: 2, m: 0 }}>
                <li>Improve user experience</li>
                <li>Enhance legal workflow efficiency</li>
                <li>Increase accessibility to legal services</li>
                <li>Integrate well with existing features</li>
                <li>Benefit the broader legal community</li>
              </Box>
            </Paper>
            
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recent Features Added
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Chip label="AI Chat" color="primary" size="small" sx={{ mr: 1, mb: 1 }} />
                <Chip label="Document Scanner" color="primary" size="small" sx={{ mr: 1, mb: 1 }} />
                <Chip label="Multi-Agent System" color="primary" size="small" sx={{ mr: 1, mb: 1 }} />
              </Box>
              <Typography variant="body2" color="text.secondary">
                Based on community feedback, we've recently added these features to make legal assistance more accessible.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </PageLayout>
  );
};

export default FeatureRequestPage;


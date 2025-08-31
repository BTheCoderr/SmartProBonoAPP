import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Button,
  TextField,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Chip,
  LinearProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Paper,
  Divider,
  Stepper,
  Step,
  StepLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Tabs,
  Tab
} from '@mui/material';
import {
  Description as DescriptionIcon,
  AutoAwesome as AutoAwesomeIcon,
  Download as DownloadIcon,
  Preview as PreviewIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Share as ShareIcon,
  ExpandMore as ExpandMoreIcon,
  Business as BusinessIcon,
  Security as SecurityIcon,
  Person as PersonIcon,
  Storage as StorageIcon,
  Timeline as TimelineIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const PolicyGeneratorPage = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [generating, setGenerating] = useState(false);
  const [generatedPolicy, setGeneratedPolicy] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [policyConfig, setPolicyConfig] = useState({
    businessName: '',
    businessType: '',
    websiteUrl: '',
    contactEmail: '',
    dataTypes: [],
    dataSources: [],
    dataSharing: [],
    complianceFrameworks: [],
    retentionPeriod: '',
    securityMeasures: [],
    thirdPartyServices: []
  });
  const [openPreview, setOpenPreview] = useState(false);

  const policyTypes = [
    {
      id: 'privacy',
      name: 'Privacy Policy',
      description: 'Comprehensive privacy policy covering data collection, usage, and protection',
      icon: <PersonIcon />,
      frameworks: ['GDPR', 'CCPA', 'PIPEDA']
    },
    {
      id: 'terms',
      name: 'Terms of Service',
      description: 'Legal terms and conditions for your website or service',
      icon: <BusinessIcon />,
      frameworks: ['General Legal']
    },
    {
      id: 'cookie',
      name: 'Cookie Policy',
      description: 'Policy explaining cookie usage and user consent',
      icon: <StorageIcon />,
      frameworks: ['GDPR', 'ePrivacy']
    },
    {
      id: 'data',
      name: 'Data Protection Policy',
      description: 'Internal policy for data handling and protection',
      icon: <SecurityIcon />,
      frameworks: ['GDPR', 'HIPAA', 'SOX']
    }
  ];

  const dataTypes = [
    'Personal Information (Name, Email, Phone)',
    'Financial Information',
    'Health Information',
    'Location Data',
    'Device Information',
    'Usage Analytics',
    'Cookies and Tracking',
    'Social Media Data',
    'Biometric Data',
    'Communication Data'
  ];

  const dataSources = [
    'Website Forms',
    'User Registration',
    'Newsletter Signup',
    'Customer Support',
    'Mobile App',
    'Social Media',
    'Third-party Integrations',
    'Analytics Tools',
    'Payment Processing',
    'Marketing Campaigns'
  ];

  const dataSharing = [
    'Marketing Partners',
    'Analytics Providers',
    'Payment Processors',
    'Cloud Service Providers',
    'Legal Authorities',
    'Business Partners',
    'Affiliates',
    'Subsidiaries'
  ];

  const securityMeasures = [
    'SSL/TLS Encryption',
    'Data Encryption at Rest',
    'Access Controls',
    'Regular Security Audits',
    'Employee Training',
    'Incident Response Plan',
    'Data Backup',
    'Multi-factor Authentication',
    'Firewall Protection',
    'Regular Updates'
  ];

  const thirdPartyServices = [
    'Google Analytics',
    'Facebook Pixel',
    'Mailchimp',
    'Stripe',
    'PayPal',
    'AWS',
    'Microsoft Azure',
    'Salesforce',
    'HubSpot',
    'Zendesk'
  ];

  const generationSteps = [
    'Analyzing Requirements',
    'Generating Policy Structure',
    'Adding Legal Language',
    'Customizing Content',
    'Reviewing Compliance',
    'Finalizing Document'
  ];

  const mockGeneratedPolicy = {
    type: 'Privacy Policy',
    content: `# Privacy Policy

## 1. Information We Collect

We collect information you provide directly to us, such as when you create an account, make a purchase, or contact us for support.

### Personal Information
- Name and contact information
- Email address
- Phone number
- Billing and shipping addresses

### Automatically Collected Information
- Device information
- Usage data
- Cookies and similar technologies

## 2. How We Use Your Information

We use the information we collect to:
- Provide and maintain our services
- Process transactions
- Send you technical notices and support messages
- Respond to your comments and questions
- Improve our services

## 3. Information Sharing

We may share your information in the following circumstances:
- With your consent
- To comply with legal obligations
- To protect our rights and safety
- In connection with a business transfer

## 4. Data Security

We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.

## 5. Your Rights

Depending on your location, you may have certain rights regarding your personal information, including:
- Access to your data
- Correction of inaccurate data
- Deletion of your data
- Data portability
- Objection to processing

## 6. Contact Us

If you have any questions about this Privacy Policy, please contact us at:
Email: ${policyConfig.contactEmail}
Address: 225 Dyer St, Providence, RI 02903

Last updated: ${new Date().toLocaleDateString()}`,
    complianceScore: 92,
    wordCount: 450,
    lastGenerated: new Date().toISOString()
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleGeneratePolicy = () => {
    setGenerating(true);
    setActiveStep(0);

    // Simulate generation process
    const interval = setInterval(() => {
      setActiveStep(prev => {
        if (prev >= generationSteps.length - 1) {
          clearInterval(interval);
          setGenerating(false);
          setGeneratedPolicy(mockGeneratedPolicy);
          return prev;
        }
        return prev + 1;
      });
    }, 1500);
  };

  const handleConfigChange = (field, value) => {
    setPolicyConfig(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const renderPolicyTypeSelection = () => (
    <Grid container spacing={3}>
      {policyTypes.map((type) => (
        <Grid item xs={12} md={6} key={type.id}>
          <Card
            sx={{
              cursor: 'pointer',
              '&:hover': { boxShadow: 4 },
              border: policyConfig.policyType === type.id ? '2px solid' : '1px solid',
              borderColor: policyConfig.policyType === type.id ? 'primary.main' : 'divider'
            }}
            onClick={() => handleConfigChange('policyType', type.id)}
          >
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                {type.icon}
                <Typography variant="h6" sx={{ ml: 1 }}>
                  {type.name}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                {type.description}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {type.frameworks.map((framework) => (
                  <Chip key={framework} label={framework} size="small" variant="outlined" />
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  const renderConfigurationForm = () => (
    <Card>
      <CardHeader title="Policy Configuration" />
      <CardContent>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Business Name"
              value={policyConfig.businessName}
              onChange={(e) => handleConfigChange('businessName', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Website URL"
              value={policyConfig.websiteUrl}
              onChange={(e) => handleConfigChange('websiteUrl', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Contact Email"
              type="email"
              value={policyConfig.contactEmail}
              onChange={(e) => handleConfigChange('contactEmail', e.target.value)}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Business Type</InputLabel>
              <Select
                value={policyConfig.businessType}
                onChange={(e) => handleConfigChange('businessType', e.target.value)}
              >
                <MenuItem value="E-commerce">E-commerce</MenuItem>
                <MenuItem value="SaaS">SaaS</MenuItem>
                <MenuItem value="Healthcare">Healthcare</MenuItem>
                <MenuItem value="Financial">Financial Services</MenuItem>
                <MenuItem value="Education">Education</MenuItem>
                <MenuItem value="Non-profit">Non-profit</MenuItem>
                <MenuItem value="Other">Other</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Data Retention Period"
              value={policyConfig.retentionPeriod}
              onChange={(e) => handleConfigChange('retentionPeriod', e.target.value)}
              margin="normal"
              placeholder="e.g., 3 years, 7 years, until account deletion"
            />
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Data Types Collected</InputLabel>
              <Select
                multiple
                value={policyConfig.dataTypes}
                onChange={(e) => handleConfigChange('dataTypes', e.target.value)}
                renderValue={(selected) => selected.join(', ')}
              >
                {dataTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    <Checkbox checked={policyConfig.dataTypes.indexOf(type) > -1} />
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Data Sources</InputLabel>
              <Select
                multiple
                value={policyConfig.dataSources}
                onChange={(e) => handleConfigChange('dataSources', e.target.value)}
                renderValue={(selected) => selected.join(', ')}
              >
                {dataSources.map((source) => (
                  <MenuItem key={source} value={source}>
                    <Checkbox checked={policyConfig.dataSources.indexOf(source) > -1} />
                    {source}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Data Sharing Partners</InputLabel>
              <Select
                multiple
                value={policyConfig.dataSharing}
                onChange={(e) => handleConfigChange('dataSharing', e.target.value)}
                renderValue={(selected) => selected.join(', ')}
              >
                {dataSharing.map((partner) => (
                  <MenuItem key={partner} value={partner}>
                    <Checkbox checked={policyConfig.dataSharing.indexOf(partner) > -1} />
                    {partner}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Security Measures</InputLabel>
              <Select
                multiple
                value={policyConfig.securityMeasures}
                onChange={(e) => handleConfigChange('securityMeasures', e.target.value)}
                renderValue={(selected) => selected.join(', ')}
              >
                {securityMeasures.map((measure) => (
                  <MenuItem key={measure} value={measure}>
                    <Checkbox checked={policyConfig.securityMeasures.indexOf(measure) > -1} />
                    {measure}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  const renderGenerationProgress = () => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Generating Policy
        </Typography>
        <Stepper activeStep={activeStep} orientation="vertical">
          {generationSteps.map((step, index) => (
            <Step key={step}>
              <StepLabel>{step}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <LinearProgress sx={{ mt: 2 }} />
      </CardContent>
    </Card>
  );

  const renderGeneratedPolicy = () => (
    <Box>
      <Card sx={{ mb: 3 }}>
        <CardHeader
          title="Generated Policy"
          action={
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Chip
                label={`${generatedPolicy.complianceScore}% Compliant`}
                color="success"
                icon={<CheckCircleIcon />}
              />
              <Chip
                label={`${generatedPolicy.wordCount} words`}
                variant="outlined"
              />
            </Box>
          }
        />
        <CardContent>
          <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<PreviewIcon />}
              onClick={() => setOpenPreview(true)}
            >
              Preview
            </Button>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
            >
              Download PDF
            </Button>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
            >
              Download HTML
            </Button>
            <Button
              variant="outlined"
              startIcon={<ShareIcon />}
            >
              Share
            </Button>
          </Box>
          
          <Paper sx={{ p: 3, bgcolor: 'grey.50', maxHeight: 400, overflow: 'auto' }}>
            <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '14px' }}>
              {generatedPolicy.content}
            </pre>
          </Paper>
        </CardContent>
      </Card>
    </Box>
  );

  const renderPreviewDialog = () => (
    <Dialog open={openPreview} onClose={() => setOpenPreview(false)} maxWidth="md" fullWidth>
      <DialogTitle>Policy Preview</DialogTitle>
      <DialogContent>
        <Box sx={{ p: 2 }}>
          <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '14px' }}>
            {generatedPolicy?.content}
          </pre>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setOpenPreview(false)}>Close</Button>
        <Button variant="contained" startIcon={<DownloadIcon />}>
          Download
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <PageLayout
      title="Policy Generator"
      description="Generate comprehensive legal policies with AI assistance"
    >
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            AI Policy Generator
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Create comprehensive, compliant legal policies tailored to your business needs
          </Typography>
        </Box>

        <Paper sx={{ mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} variant="fullWidth">
            <Tab label="Policy Type" icon={<DescriptionIcon />} />
            <Tab label="Configuration" icon={<EditIcon />} />
            <Tab label="Generate" icon={<AutoAwesomeIcon />} />
          </Tabs>
        </Paper>

        <Box sx={{ mt: 3 }}>
          {activeTab === 0 && renderPolicyTypeSelection()}
          {activeTab === 1 && renderConfigurationForm()}
          {activeTab === 2 && (
            <Box>
              {!generating && !generatedPolicy && (
                <Card>
                  <CardContent sx={{ textAlign: 'center', py: 6 }}>
                    <AutoAwesomeIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
                    <Typography variant="h5" gutterBottom>
                      Ready to Generate Your Policy
                    </Typography>
                    <Typography variant="body1" color="text.secondary" paragraph>
                      Review your configuration and click generate to create your customized policy.
                    </Typography>
                    <Button
                      variant="contained"
                      size="large"
                      startIcon={<AutoAwesomeIcon />}
                      onClick={handleGeneratePolicy}
                      disabled={!policyConfig.businessName || !policyConfig.contactEmail}
                    >
                      Generate Policy
                    </Button>
                  </CardContent>
                </Card>
              )}

              {generating && renderGenerationProgress()}
              {generatedPolicy && renderGeneratedPolicy()}
            </Box>
          )}
        </Box>

        {renderPreviewDialog()}
      </Container>
    </PageLayout>
  );
};

export default PolicyGeneratorPage;

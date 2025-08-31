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
  ListItemSecondaryAction,
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
  AccordionDetails
} from '@mui/material';
import {
  Security as SecurityIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  PlayArrow as PlayArrowIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  ExpandMore as ExpandMoreIcon,
  Business as BusinessIcon,
  Web as WebIcon,
  Storage as StorageIcon,
  Person as PersonIcon,
  Assessment as AssessmentIcon,
  Timeline as TimelineIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const ComplianceScannerPage = () => {
  const [scanning, setScanning] = useState(false);
  const [scanResults, setScanResults] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [scanConfig, setScanConfig] = useState({
    websiteUrl: '',
    businessType: '',
    dataTypes: [],
    complianceFrameworks: [],
    includeSubdomains: false
  });
  const [openConfig, setOpenConfig] = useState(false);

  const complianceFrameworks = [
    { id: 'gdpr', name: 'GDPR', description: 'General Data Protection Regulation' },
    { id: 'ccpa', name: 'CCPA', description: 'California Consumer Privacy Act' },
    { id: 'hipaa', name: 'HIPAA', description: 'Health Insurance Portability and Accountability Act' },
    { id: 'sox', name: 'SOX', description: 'Sarbanes-Oxley Act' },
    { id: 'pci', name: 'PCI DSS', description: 'Payment Card Industry Data Security Standard' },
    { id: 'iso27001', name: 'ISO 27001', description: 'Information Security Management' }
  ];

  const dataTypes = [
    'Personal Information',
    'Financial Data',
    'Health Information',
    'Payment Information',
    'Biometric Data',
    'Location Data',
    'Behavioral Data',
    'Communication Data'
  ];

  const businessTypes = [
    'Healthcare',
    'Financial Services',
    'E-commerce',
    'Education',
    'Technology',
    'Government',
    'Non-profit',
    'Other'
  ];

  const scanSteps = [
    'Website Analysis',
    'Data Collection Assessment',
    'Security Configuration Review',
    'Privacy Policy Analysis',
    'Cookie Compliance Check',
    'Data Processing Audit',
    'Generating Report'
  ];

  const mockScanResults = {
    overallScore: 78,
    complianceStatus: 'Needs Improvement',
    issues: [
      {
        id: 1,
        severity: 'high',
        category: 'Privacy Policy',
        title: 'Missing Cookie Consent Banner',
        description: 'Your website does not have a visible cookie consent banner.',
        recommendation: 'Implement a GDPR-compliant cookie consent banner.',
        framework: 'GDPR'
      },
      {
        id: 2,
        severity: 'medium',
        category: 'Data Security',
        title: 'Insecure Data Transmission',
        description: 'Some forms are not using HTTPS encryption.',
        recommendation: 'Ensure all data transmission uses HTTPS.',
        framework: 'GDPR'
      },
      {
        id: 3,
        severity: 'low',
        category: 'Privacy Policy',
        title: 'Privacy Policy Needs Update',
        description: 'Privacy policy does not mention data retention periods.',
        recommendation: 'Update privacy policy to include data retention information.',
        framework: 'CCPA'
      }
    ],
    recommendations: [
      'Implement a comprehensive cookie consent management system',
      'Add SSL certificates to all subdomains',
      'Create a data retention policy',
      'Implement data subject access request procedures',
      'Add privacy policy links to all forms'
    ],
    complianceScores: {
      gdpr: 65,
      ccpa: 72,
      hipaa: 85,
      pci: 90
    }
  };

  const handleStartScan = () => {
    setScanning(true);
    setActiveStep(0);
    setScanResults(null);

    // Simulate scanning process
    const interval = setInterval(() => {
      setActiveStep(prev => {
        if (prev >= scanSteps.length - 1) {
          clearInterval(interval);
          setScanning(false);
          setScanResults(mockScanResults);
          return prev;
        }
        return prev + 1;
      });
    }, 2000);
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'info';
      default: return 'default';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'high': return <ErrorIcon />;
      case 'medium': return <WarningIcon />;
      case 'low': return <InfoIcon />;
      default: return <InfoIcon />;
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  const renderScanConfiguration = () => (
    <Dialog open={openConfig} onClose={() => setOpenConfig(false)} maxWidth="md" fullWidth>
      <DialogTitle>Configure Compliance Scan</DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 2 }}>
          <TextField
            fullWidth
            label="Website URL"
            value={scanConfig.websiteUrl}
            onChange={(e) => setScanConfig({...scanConfig, websiteUrl: e.target.value})}
            margin="normal"
            placeholder="https://example.com"
          />
          
          <FormControl fullWidth margin="normal">
            <InputLabel>Business Type</InputLabel>
            <Select
              value={scanConfig.businessType}
              onChange={(e) => setScanConfig({...scanConfig, businessType: e.target.value})}
            >
              {businessTypes.map((type) => (
                <MenuItem key={type} value={type}>{type}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth margin="normal">
            <InputLabel>Data Types Collected</InputLabel>
            <Select
              multiple
              value={scanConfig.dataTypes}
              onChange={(e) => setScanConfig({...scanConfig, dataTypes: e.target.value})}
              renderValue={(selected) => selected.join(', ')}
            >
              {dataTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  <Checkbox checked={scanConfig.dataTypes.indexOf(type) > -1} />
                  {type}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth margin="normal">
            <InputLabel>Compliance Frameworks</InputLabel>
            <Select
              multiple
              value={scanConfig.complianceFrameworks}
              onChange={(e) => setScanConfig({...scanConfig, complianceFrameworks: e.target.value})}
              renderValue={(selected) => selected.join(', ')}
            >
              {complianceFrameworks.map((framework) => (
                <MenuItem key={framework.id} value={framework.id}>
                  <Checkbox checked={scanConfig.complianceFrameworks.indexOf(framework.id) > -1} />
                  {framework.name} - {framework.description}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControlLabel
            control={
              <Checkbox
                checked={scanConfig.includeSubdomains}
                onChange={(e) => setScanConfig({...scanConfig, includeSubdomains: e.target.checked})}
              />
            }
            label="Include subdomains in scan"
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setOpenConfig(false)}>Cancel</Button>
        <Button variant="contained" onClick={() => setOpenConfig(false)}>
          Save Configuration
        </Button>
      </DialogActions>
    </Dialog>
  );

  const renderScanProgress = () => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Compliance Scan in Progress
        </Typography>
        <Stepper activeStep={activeStep} orientation="vertical">
          {scanSteps.map((step, index) => (
            <Step key={step}>
              <StepLabel>{step}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <LinearProgress sx={{ mt: 2 }} />
      </CardContent>
    </Card>
  );

  const renderScanResults = () => (
    <Box>
      {/* Overall Score */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">Overall Compliance Score</Typography>
            <Chip
              label={`${scanResults.overallScore}/100`}
              color={getScoreColor(scanResults.overallScore)}
              size="large"
            />
          </Box>
          <LinearProgress
            variant="determinate"
            value={scanResults.overallScore}
            color={getScoreColor(scanResults.overallScore)}
            sx={{ height: 10, borderRadius: 5 }}
          />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Status: {scanResults.complianceStatus}
          </Typography>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Framework Scores */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Framework Compliance Scores" />
            <CardContent>
              {Object.entries(scanResults.complianceScores).map(([framework, score]) => (
                <Box key={framework} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2" sx={{ textTransform: 'uppercase', fontWeight: 'bold' }}>
                      {framework}
                    </Typography>
                    <Typography variant="body2" color={getScoreColor(score)}>
                      {score}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={score}
                    color={getScoreColor(score)}
                  />
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Issues */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Compliance Issues" />
            <CardContent>
              <List>
                {scanResults.issues.map((issue) => (
                  <ListItem key={issue.id} divider>
                    <ListItemIcon>
                      {getSeverityIcon(issue.severity)}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {issue.title}
                          <Chip
                            label={issue.severity}
                            size="small"
                            color={getSeverityColor(issue.severity)}
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            {issue.description}
                          </Typography>
                          <Typography variant="caption" color="primary">
                            Recommendation: {issue.recommendation}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Action Items" />
            <CardContent>
              <List>
                {scanResults.recommendations.map((recommendation, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <CheckCircleIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={recommendation} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  return (
    <PageLayout
      title="Compliance Scanner"
      description="Analyze your website and systems for compliance with major regulations"
    >
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Compliance Scanner
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Automatically analyze your website and systems for compliance with GDPR, CCPA, HIPAA, and other major regulations
          </Typography>
        </Box>

        {!scanning && !scanResults && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Card>
                <CardHeader title="Start Compliance Scan" />
                <CardContent>
                  <Typography variant="body1" paragraph>
                    Our compliance scanner will analyze your website and systems to identify potential compliance issues with major regulations.
                  </Typography>
                  
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      What We Scan:
                    </Typography>
                    <List>
                      <ListItem>
                        <ListItemIcon><WebIcon /></ListItemIcon>
                        <ListItemText primary="Website structure and forms" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><StorageIcon /></ListItemIcon>
                        <ListItemText primary="Data collection practices" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><SecurityIcon /></ListItemIcon>
                        <ListItemText primary="Security configurations" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><PersonIcon /></ListItemIcon>
                        <ListItemText primary="Privacy policy compliance" />
                      </ListItem>
                    </List>
                  </Box>

                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                      variant="contained"
                      size="large"
                      startIcon={<PlayArrowIcon />}
                      onClick={handleStartScan}
                    >
                      Start Scan
                    </Button>
                    <Button
                      variant="outlined"
                      startIcon={<SettingsIcon />}
                      onClick={() => setOpenConfig(true)}
                    >
                      Configure Scan
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card>
                <CardHeader title="Supported Frameworks" />
                <CardContent>
                  <List dense>
                    {complianceFrameworks.map((framework) => (
                      <ListItem key={framework.id}>
                        <ListItemText
                          primary={framework.name}
                          secondary={framework.description}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}

        {scanning && renderScanProgress()}
        {scanResults && renderScanResults()}

        {scanResults && (
          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<RefreshIcon />}
              onClick={handleStartScan}
            >
              Run New Scan
            </Button>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
            >
              Download Report
            </Button>
          </Box>
        )}

        {renderScanConfiguration()}
      </Container>
    </PageLayout>
  );
};

export default ComplianceScannerPage;

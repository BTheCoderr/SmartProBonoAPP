import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Button,
  Stepper,
  Step,
  StepLabel,
  Tabs,
  Tab,

} from '@mui/material';
import {
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  TrendingDown as TrendingDownIcon,
  Timeline as TimelineIcon,
  Business as BusinessIcon,
  Storage as StorageIcon,
  Person as PersonIcon,
  ExpandMore as ExpandMoreIcon,
  PlayArrow as PlayArrowIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const RiskAssessmentPage = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [assessing, setAssessing] = useState(false);
  const [assessmentResults, setAssessmentResults] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [riskConfig, setRiskConfig] = useState({
    businessType: '',
    industry: '',
    dataVolume: 'medium',
    userCount: 'medium',
    complianceRequirements: [],
    securityMeasures: [],
    incidentHistory: 'none',
    thirdPartyIntegrations: [],
    geographicPresence: [],
    budget: 'medium'
  });
  const [, setOpenConfig] = useState(false);

  const handleRiskConfigUpdate = (newConfig) => {
    setRiskConfig(prev => ({ ...prev, ...newConfig }));
  };

  const riskCategories = [
    {
      id: 'data_breach',
      name: 'Data Breach Risk',
      description: 'Risk of unauthorized access to sensitive data',
      icon: <StorageIcon />,
      factors: ['Data encryption', 'Access controls', 'Network security', 'Employee training']
    },
    {
      id: 'compliance',
      name: 'Compliance Risk',
      description: 'Risk of non-compliance with regulations',
      icon: <SecurityIcon />,
      factors: ['Regulatory requirements', 'Policy implementation', 'Audit readiness', 'Documentation']
    },
    {
      id: 'operational',
      name: 'Operational Risk',
      description: 'Risk of business disruption or loss',
      icon: <BusinessIcon />,
      factors: ['System availability', 'Backup systems', 'Disaster recovery', 'Staff availability']
    },
    {
      id: 'reputational',
      name: 'Reputational Risk',
      description: 'Risk of damage to business reputation',
      icon: <PersonIcon />,
      factors: ['Customer trust', 'Public relations', 'Media coverage', 'Social media presence']
    },
    {
      id: 'financial',
      name: 'Financial Risk',
      description: 'Risk of financial loss or penalties',
      icon: <TrendingDownIcon />,
      factors: ['Insurance coverage', 'Legal costs', 'Regulatory fines', 'Revenue impact']
    }
  ];

  const assessmentSteps = [
    'Analyzing Business Profile',
    'Evaluating Data Security',
    'Assessing Compliance Posture',
    'Calculating Risk Scores',
    'Generating Recommendations',
    'Creating Action Plan'
  ];

  const mockAssessmentResults = {
    overallRiskScore: 65,
    riskLevel: 'Medium',
    lastAssessed: new Date().toISOString(),
    categories: [
      {
        id: 'data_breach',
        name: 'Data Breach Risk',
        score: 45,
        level: 'Low',
        trends: 'improving',
        factors: [
          { name: 'Data Encryption', score: 80, status: 'good' },
          { name: 'Access Controls', score: 60, status: 'fair' },
          { name: 'Network Security', score: 70, status: 'good' },
          { name: 'Employee Training', score: 40, status: 'poor' }
        ]
      },
      {
        id: 'compliance',
        name: 'Compliance Risk',
        score: 75,
        level: 'High',
        trends: 'stable',
        factors: [
          { name: 'GDPR Compliance', score: 50, status: 'fair' },
          { name: 'CCPA Compliance', score: 60, status: 'fair' },
          { name: 'Policy Implementation', score: 70, status: 'good' },
          { name: 'Audit Readiness', score: 40, status: 'poor' }
        ]
      },
      {
        id: 'operational',
        name: 'Operational Risk',
        score: 55,
        level: 'Medium',
        trends: 'improving',
        factors: [
          { name: 'System Availability', score: 85, status: 'excellent' },
          { name: 'Backup Systems', score: 60, status: 'fair' },
          { name: 'Disaster Recovery', score: 45, status: 'poor' },
          { name: 'Staff Availability', score: 70, status: 'good' }
        ]
      }
    ],
    recommendations: [
      {
        priority: 'high',
        category: 'compliance',
        title: 'Implement GDPR Compliance Program',
        description: 'Develop comprehensive GDPR compliance procedures and documentation',
        impact: 'Reduce compliance risk by 25%',
        effort: 'medium',
        timeline: '3-6 months'
      },
      {
        priority: 'high',
        category: 'data_breach',
        title: 'Enhance Employee Security Training',
        description: 'Implement regular security awareness training for all employees',
        impact: 'Reduce data breach risk by 20%',
        effort: 'low',
        timeline: '1-2 months'
      },
      {
        priority: 'medium',
        category: 'operational',
        title: 'Improve Disaster Recovery Plan',
        description: 'Develop and test comprehensive disaster recovery procedures',
        impact: 'Reduce operational risk by 15%',
        effort: 'high',
        timeline: '6-12 months'
      }
    ],
    actionPlan: {
      immediate: ['Conduct security training', 'Update privacy policies'],
      shortTerm: ['Implement GDPR compliance', 'Enhance access controls'],
      longTerm: ['Develop disaster recovery plan', 'Regular security audits']
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleStartAssessment = () => {
    setAssessing(true);
    setActiveStep(0);
    setAssessmentResults(null);

    // Simulate assessment process
    const interval = setInterval(() => {
      setActiveStep(prev => {
        if (prev >= assessmentSteps.length - 1) {
          clearInterval(interval);
          setAssessing(false);
          setAssessmentResults(mockAssessmentResults);
          return prev;
        }
        return prev + 1;
      });
    }, 2000);
  };

  const getRiskLevelColor = (level) => {
    switch (level.toLowerCase()) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      case 'critical': return 'error';
      default: return 'default';
    }
  };

  const getRiskLevelIcon = (level) => {
    switch (level.toLowerCase()) {
      case 'low': return <CheckCircleIcon />;
      case 'medium': return <WarningIcon />;
      case 'high': return <ErrorIcon />;
      case 'critical': return <ErrorIcon />;
      default: return <InfoIcon />;
    }
  };

  const getFactorStatusColor = (status) => {
    switch (status) {
      case 'excellent': return 'success';
      case 'good': return 'success';
      case 'fair': return 'warning';
      case 'poor': return 'error';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const renderRiskOverview = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent sx={{ textAlign: 'center' }}>
            <Typography variant="h2" color={getRiskLevelColor(assessmentResults.riskLevel)}>
              {assessmentResults.overallRiskScore}
            </Typography>
            <Typography variant="h6" gutterBottom>
              Overall Risk Score
            </Typography>
            <Chip
              icon={getRiskLevelIcon(assessmentResults.riskLevel)}
              label={assessmentResults.riskLevel} Risk
              color={getRiskLevelColor(assessmentResults.riskLevel)}
              size="large"
            />
            <LinearProgress
              variant="determinate"
              value={assessmentResults.overallRiskScore}
              color={getRiskLevelColor(assessmentResults.riskLevel)}
              sx={{ mt: 2, height: 8, borderRadius: 4 }}
            />
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={8}>
        <Card>
          <CardHeader title="Risk Categories" />
          <CardContent>
            <Grid container spacing={2}>
              {assessmentResults.categories.map((category) => (
                <Grid item xs={12} sm={6} key={category.id}>
                  <Paper sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="subtitle2" fontWeight="bold">
                        {category.name}
                      </Typography>
                      <Chip
                        label={category.score}
                        size="small"
                        color={getRiskLevelColor(category.level)}
                      />
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={category.score}
                      color={getRiskLevelColor(category.level)}
                      sx={{ mb: 1 }}
                    />
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="caption" color="text.secondary">
                        {category.level} Risk
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {category.trends}
                      </Typography>
                    </Box>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const renderRiskDetails = () => (
    <Box>
      {assessmentResults.categories.map((category) => (
        <Accordion key={category.id} sx={{ mb: 2 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
              <Typography variant="h6" sx={{ flex: 1 }}>
                {category.name}
              </Typography>
              <Chip
                label={`${category.score}/100`}
                color={getRiskLevelColor(category.level)}
                sx={{ mr: 2 }}
              />
              <Chip
                label={category.level}
                color={getRiskLevelColor(category.level)}
                variant="outlined"
              />
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              {category.factors.map((factor, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      {factor.name}
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={factor.score}
                      color={getFactorStatusColor(factor.status)}
                      sx={{ mb: 1 }}
                    />
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="caption" color="text.secondary">
                        {factor.score}%
                      </Typography>
                      <Chip
                        label={factor.status}
                        size="small"
                        color={getFactorStatusColor(factor.status)}
                      />
                    </Box>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );

  const renderRecommendations = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Risk Mitigation Recommendations
      </Typography>
      <Grid container spacing={3}>
        {assessmentResults.recommendations.map((rec, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6">
                    {rec.title}
                  </Typography>
                  <Chip
                    label={rec.priority}
                    color={getPriorityColor(rec.priority)}
                    size="small"
                  />
                </Box>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {rec.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                  <Chip label={`Impact: ${rec.impact}`} size="small" variant="outlined" />
                  <Chip label={`Effort: ${rec.effort}`} size="small" variant="outlined" />
                  <Chip label={`Timeline: ${rec.timeline}`} size="small" variant="outlined" />
                </Box>
                <Button variant="outlined" size="small">
                  View Details
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderActionPlan = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Action Plan
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Immediate (0-1 months)" color="error" />
            <CardContent>
              <List dense>
                {assessmentResults.actionPlan.immediate.map((action, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <ErrorIcon color="error" />
                    </ListItemIcon>
                    <ListItemText primary={action} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Short Term (1-6 months)" color="warning" />
            <CardContent>
              <List dense>
                {assessmentResults.actionPlan.shortTerm.map((action, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <WarningIcon color="warning" />
                    </ListItemIcon>
                    <ListItemText primary={action} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Long Term (6+ months)" color="info" />
            <CardContent>
              <List dense>
                {assessmentResults.actionPlan.longTerm.map((action, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <InfoIcon color="info" />
                    </ListItemIcon>
                    <ListItemText primary={action} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderAssessmentProgress = () => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Risk Assessment in Progress
        </Typography>
        <Stepper activeStep={activeStep} orientation="vertical">
          {assessmentSteps.map((step, index) => (
            <Step key={step}>
              <StepLabel>{step}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <LinearProgress sx={{ mt: 2 }} />
      </CardContent>
    </Card>
  );

  return (
    <PageLayout
      title="Risk Assessment"
      description="Comprehensive risk analysis and mitigation planning"
    >
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Risk Assessment Dashboard
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Alert severity="info" sx={{ mb: 2 }}>
            Configure your risk assessment settings below
          </Alert>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Current Risk Config: {riskConfig.businessType || 'Not set'} - {riskConfig.industry || 'Not set'}
          </Typography>
          <Button variant="outlined" onClick={() => handleRiskConfigUpdate({ businessType: 'Technology', industry: 'Software' })}>
            Update Risk Config
          </Button>
          <Typography variant="subtitle1" color="text.secondary">
            Analyze and mitigate risks across your organization with AI-powered assessment tools
          </Typography>
        </Box>

        {!assessing && !assessmentResults && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Card>
                <CardHeader title="Start Risk Assessment" />
                <CardContent>
                  <Typography variant="body1" paragraph>
                    Our comprehensive risk assessment will analyze your organization across multiple risk categories and provide actionable recommendations.
                  </Typography>
                  
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Assessment Areas:
                    </Typography>
                    <Grid container spacing={2}>
                      {riskCategories.map((category) => (
                        <Grid item xs={12} sm={6} key={category.id}>
                          <Paper sx={{ p: 2 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                              {category.icon}
                              <Typography variant="subtitle2" sx={{ ml: 1 }}>
                                {category.name}
                              </Typography>
                            </Box>
                            <Typography variant="body2" color="text.secondary">
                              {category.description}
                            </Typography>
                          </Paper>
                        </Grid>
                      ))}
                    </Grid>
                  </Box>

                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                      variant="contained"
                      size="large"
                      startIcon={<PlayArrowIcon />}
                      onClick={handleStartAssessment}
                    >
                      Start Assessment
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={() => setOpenConfig(true)}
                    >
                      Configure Assessment
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card>
                <CardHeader title="Risk Categories" />
                <CardContent>
                  <List dense>
                    {riskCategories.map((category) => (
                      <ListItem key={category.id}>
                        <ListItemIcon>{category.icon}</ListItemIcon>
                        <ListItemText
                          primary={category.name}
                          secondary={category.description}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}

        {assessing && renderAssessmentProgress()}

        {assessmentResults && (
          <Box>
            <Paper sx={{ mb: 3 }}>
              <Tabs value={activeTab} onChange={handleTabChange} variant="fullWidth">
                <Tab label="Overview" icon={<AssessmentIcon />} />
                <Tab label="Risk Details" icon={<SecurityIcon />} />
                <Tab label="Recommendations" icon={<CheckCircleIcon />} />
                <Tab label="Action Plan" icon={<TimelineIcon />} />
              </Tabs>
            </Paper>

            <Box sx={{ mt: 3 }}>
              {activeTab === 0 && renderRiskOverview()}
              {activeTab === 1 && renderRiskDetails()}
              {activeTab === 2 && renderRecommendations()}
              {activeTab === 3 && renderActionPlan()}
            </Box>

            <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
              <Button
                variant="contained"
                startIcon={<RefreshIcon />}
                onClick={handleStartAssessment}
              >
                Run New Assessment
              </Button>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
              >
                Download Report
              </Button>
            </Box>
          </Box>
        )}
      </Container>
    </PageLayout>
  );
};

export default RiskAssessmentPage;

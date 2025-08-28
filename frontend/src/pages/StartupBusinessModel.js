import React from 'react';
import { Box, Typography, Grid, Paper, Container, List, ListItem, ListItemIcon, ListItemText, Card, CardContent, Chip } from '@mui/material';
import { styled } from '@mui/material/styles';
import BusinessIcon from '@mui/icons-material/Business';
import ComplianceIcon from '@mui/icons-material/VerifiedUser';
import AutomationIcon from '@mui/icons-material/AutoMode';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SecurityIcon from '@mui/icons-material/Security';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import PaidIcon from '@mui/icons-material/Paid';
import GroupsIcon from '@mui/icons-material/Groups';
import ScaleIcon from '@mui/icons-material/Scale';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(3),
  color: theme.palette.text.primary,
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
}));

const StartupBusinessModel = () => {
  const revenueMetrics = [
    { label: 'Target ARR Year 1', value: '$500K', color: 'primary' },
    { label: 'Target ARR Year 3', value: '$5M', color: 'secondary' },
    { label: 'Average Contract Value', value: '$3.6K', color: 'success' },
    { label: 'Customer Acquisition Cost', value: '$450', color: 'warning' },
    { label: 'Customer Lifetime Value', value: '$12K', color: 'info' },
    { label: 'Gross Margin', value: '85%', color: 'error' }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700, color: '#333' }}>
          AI Legal Agents for Startups
        </Typography>
        <Typography variant="h4" component="h2" sx={{ color: '#666', mb: 3 }}>
          $100k+ MRR Business Opportunity
        </Typography>
        <Typography variant="h6" sx={{ maxWidth: 800, mx: 'auto', color: '#555' }}>
          Automated legal compliance infrastructure that scales with high-growth startups. 
          From GDPR to SOC 2, we handle compliance so founders can focus on building.
        </Typography>
      </Box>

      {/* Revenue Metrics */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" gutterBottom align="center" sx={{ mb: 3 }}>
          Revenue Metrics
        </Typography>
        <Grid container spacing={2} justifyContent="center">
          {revenueMetrics.map((metric, index) => (
            <Grid item xs={6} md={2} key={index}>
              <Paper sx={{ p: 2, textAlign: 'center', height: '100%' }}>
                <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                  {metric.value}
                </Typography>
                <Chip label={metric.label} color={metric.color} variant="outlined" size="small" />
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Grid container spacing={4}>
        {/* Customer Segments */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <BusinessIcon sx={{ mr: 1 }} /> Target Customers
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <RocketLaunchIcon sx={{ color: 'primary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Early-Stage Startups" 
                  secondary="Pre-seed to Series A companies needing legal infrastructure ($199-$499/month)" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <TrendingUpIcon sx={{ color: 'secondary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Growth-Stage Startups" 
                  secondary="Series A+ companies scaling compliance operations ($499-$1299/month)" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <GroupsIcon sx={{ color: 'success.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Startup Accelerators" 
                  secondary="Y Combinator, Techstars, 500 Startups portfolio companies (enterprise deals)" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <ScaleIcon sx={{ color: 'warning.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Legal/Compliance Teams" 
                  secondary="In-house legal teams at tech companies seeking automation tools" 
                />
              </ListItem>
            </List>
          </Item>
        </Grid>

        {/* Revenue Streams */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <AttachMoneyIcon sx={{ mr: 1 }} /> Revenue Model
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <PaidIcon sx={{ color: 'primary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="SaaS Subscriptions" 
                  secondary="$199-$1299/month recurring revenue from compliance automation" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon sx={{ color: 'secondary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Enterprise Contracts" 
                  secondary="$50K-$200K annual contracts with accelerators and enterprise clients" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <AutomationIcon sx={{ color: 'success.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Professional Services" 
                  secondary="Implementation, training, and custom compliance consulting" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <TrendingUpIcon sx={{ color: 'warning.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Partner Revenue" 
                  secondary="White-label solutions for law firms and consultants" 
                />
              </ListItem>
            </List>
          </Item>
        </Grid>

        {/* Value Proposition */}
        <Grid item xs={12}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <ComplianceIcon sx={{ mr: 1 }} /> Value Proposition
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card sx={{ height: '100%', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                  <CardContent>
                    <SecurityIcon sx={{ fontSize: 40, mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                      Instant Compliance
                    </Typography>
                    <Typography variant="body2">
                      Go from zero to GDPR/SOC 2 compliant in under 24 hours with AI-powered automation
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card sx={{ height: '100%', background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
                  <CardContent>
                    <AutomationIcon sx={{ fontSize: 40, mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                      Cost Reduction
                    </Typography>
                    <Typography variant="body2">
                      Save $50K-$200K annually on legal fees with automated policy generation and compliance monitoring
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card sx={{ height: '100%', background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
                  <CardContent>
                    <TrendingUpIcon sx={{ fontSize: 40, mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                      Growth Enablement
                    </Typography>
                    <Typography variant="body2">
                      Scale compliance as you grow - from MVP to IPO with the same automated legal infrastructure
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Item>
        </Grid>

        {/* Customer Journey */}
        <Grid item xs={12}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <RocketLaunchIcon sx={{ mr: 1 }} /> Customer Journey
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Card sx={{ background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    🎯 Discovery (Marketing Qualified Lead)
                  </Typography>
                  <Typography variant="body2">
                    Startup discovers AI Legal Agents through accelerator partnerships, content marketing, or referrals
                  </Typography>
                </CardContent>
              </Card>
              
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                <ArrowForwardIcon sx={{ transform: 'rotate(90deg)', fontSize: 32, color: 'primary.main' }} />
              </Box>
              
              <Card sx={{ background: 'linear-gradient(90deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    📋 Risk Assessment (Free Trial)
                  </Typography>
                  <Typography variant="body2">
                    Free compliance audit identifies gaps in current legal setup, generates risk score and action plan
                  </Typography>
                </CardContent>
              </Card>
              
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                <ArrowForwardIcon sx={{ transform: 'rotate(90deg)', fontSize: 32, color: 'secondary.main' }} />
              </Box>
              
              <Card sx={{ background: 'linear-gradient(90deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    🚀 Rapid Implementation (Paid Conversion)
                  </Typography>
                  <Typography variant="body2">
                    AI agents auto-generate policies, terms of service, and compliance frameworks within 24 hours
                  </Typography>
                </CardContent>
              </Card>
              
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                <ArrowForwardIcon sx={{ transform: 'rotate(90deg)', fontSize: 32, color: 'success.main' }} />
              </Box>
              
              <Card sx={{ background: 'linear-gradient(90deg, #fa709a 0%, #fee140 100%)', color: 'white' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    📈 Ongoing Monitoring & Scaling (Expansion Revenue)
                  </Typography>
                  <Typography variant="body2">
                    Continuous compliance monitoring, automatic updates, and scaling to new jurisdictions as startup grows
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          </Item>
        </Grid>

        {/* Market Opportunity */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <TrendingUpIcon sx={{ mr: 1 }} /> Market Opportunity
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon sx={{ color: 'primary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="$50B+ Legal Tech Market" 
                  secondary="Growing 10%+ annually with increasing startup compliance needs" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <RocketLaunchIcon sx={{ color: 'secondary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="500K+ New Startups Annually" 
                  secondary="Each needing compliance from Day 1, average $3.6K annual spend" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <ComplianceIcon sx={{ color: 'success.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Regulatory Complexity Increasing" 
                  secondary="GDPR, CCPA, SOC 2 creating $200B+ compliance market" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <AutomationIcon sx={{ color: 'warning.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="AI Automation Trend" 
                  secondary="Legal automation market growing 25%+ annually, early adopter advantage" 
                />
              </ListItem>
            </List>
          </Item>
        </Grid>

        {/* Competitive Advantage */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <SecurityIcon sx={{ mr: 1 }} /> Competitive Advantages
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <AutomationIcon sx={{ color: 'primary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="AI-First Approach" 
                  secondary="Automated policy generation vs. manual template libraries" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <RocketLaunchIcon sx={{ color: 'secondary.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Startup-Specific Focus" 
                  secondary="Built for startup needs vs. enterprise-first solutions" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <TrendingUpIcon sx={{ color: 'success.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Growth-Aligned Pricing" 
                  secondary="Scales with company size vs. expensive fixed enterprise contracts" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <GroupsIcon sx={{ color: 'warning.main' }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Accelerator Partnerships" 
                  secondary="Direct access to 1000+ startups through YC, Techstars relationships" 
                />
              </ListItem>
            </List>
          </Item>
        </Grid>

        {/* Financial Projections */}
        <Grid item xs={12}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <AttachMoneyIcon sx={{ mr: 1 }} /> 3-Year Financial Projections
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h3" sx={{ color: 'primary.main', fontWeight: 700 }}>
                    Year 1
                  </Typography>
                  <Typography variant="h6" gutterBottom>$500K ARR</Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    • 140 customers<br/>
                    • $3.6K ACV<br/>
                    • 15% monthly growth<br/>
                    • Break-even by month 8
                  </Typography>
                  <Chip label="Foundation" color="primary" />
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h3" sx={{ color: 'secondary.main', fontWeight: 700 }}>
                    Year 2
                  </Typography>
                  <Typography variant="h6" gutterBottom>$2M ARR</Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    • 550 customers<br/>
                    • $4.2K ACV<br/>
                    • Enterprise tier launch<br/>
                    • $500K profit margin
                  </Typography>
                  <Chip label="Growth" color="secondary" />
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h3" sx={{ color: 'success.main', fontWeight: 700 }}>
                    Year 3
                  </Typography>
                  <Typography variant="h6" gutterBottom>$5M ARR</Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    • 1,200 customers<br/>
                    • $5.8K ACV<br/>
                    • International expansion<br/>
                    • $2M+ profit margin
                  </Typography>
                  <Chip label="Scale" color="success" />
                </Card>
              </Grid>
            </Grid>
          </Item>
        </Grid>
      </Grid>
    </Container>
  );
};

export default StartupBusinessModel; 
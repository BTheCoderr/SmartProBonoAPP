import React from 'react';
import { 
  Container, Typography, Grid, Card, CardContent, CardActions, 
  Button, Box, Paper, Divider, Chip
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { Description, AttachMoney, AccessTime, Gavel } from '@mui/icons-material';

const legalForms = [
  {
    id: 'small-claims',
    title: 'Small Claims Complaint',
    description: 'Use this form to file a Small Claims Complaint for monetary damages up to $10,000. This form is suitable for breach of contract, property damage, and other monetary claims.',
    route: '/forms/small-claims',
    complexity: 'Medium',
    time: '20-30 minutes',
    fee: '$30-75',
    category: 'Civil',
    icon: <Gavel sx={{ fontSize: 40 }} />,
    tags: ['Money', 'Contract', 'Civil']
  },
  {
    id: 'eviction-response',
    title: 'Eviction Response',
    description: 'Use this form to respond to an eviction notice (unlawful detainer). This form allows you to present defenses and protect your housing rights.',
    route: '/forms/eviction-response',
    complexity: 'High',
    time: '30-45 minutes',
    fee: '$0-50',
    category: 'Housing',
    icon: <Description sx={{ fontSize: 40 }} />,
    tags: ['Housing', 'Eviction', 'Defense']
  },
  {
    id: 'fee-waiver',
    title: 'Fee Waiver Request',
    description: 'Use this form to request a waiver of court filing fees based on financial hardship. This can make legal proceedings more accessible.',
    route: '/forms/fee-waiver',
    complexity: 'Low',
    time: '10-15 minutes',
    fee: '$0',
    category: 'Financial',
    icon: <AttachMoney sx={{ fontSize: 40 }} />,
    tags: ['Financial', 'Court Fees', 'Waiver'],
    comingSoon: true
  }
];

const FormsIndexPage = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={0} sx={{ p: 3, mb: 4, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
          Legal Forms
        </Typography>
        <Typography variant="body1">
          Create professional legal documents instantly. Fill out the information, preview the document,
          and download or print your completed forms.
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {legalForms.map((form) => (
          <Grid item xs={12} md={6} lg={4} key={form.id}>
            <Card 
              elevation={3} 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                position: 'relative',
                '&:hover': {
                  boxShadow: 6,
                  transform: 'translateY(-4px)',
                  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out'
                }
              }}
            >
              {form.comingSoon && (
                <Chip 
                  label="Coming Soon" 
                  color="secondary" 
                  size="small"
                  sx={{ 
                    position: 'absolute', 
                    top: 10, 
                    right: 10,
                    zIndex: 1
                  }} 
                />
              )}
              <Box sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
                <Box sx={{ mr: 2, color: 'primary.main' }}>
                  {form.icon}
                </Box>
                <Typography variant="h6" component="h2">
                  {form.title}
                </Typography>
              </Box>
              
              <Divider />
              
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {form.description}
                </Typography>
                
                <Grid container spacing={1} sx={{ mt: 2 }}>
                  <Grid item xs={4}>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Complexity
                    </Typography>
                    <Typography variant="body2" fontWeight="medium">
                      {form.complexity}
                    </Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Est. Time
                    </Typography>
                    <Typography variant="body2" fontWeight="medium">
                      {form.time}
                    </Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Filing Fee
                    </Typography>
                    <Typography variant="body2" fontWeight="medium">
                      {form.fee}
                    </Typography>
                  </Grid>
                </Grid>
                
                <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {form.tags.map(tag => (
                    <Chip 
                      key={tag} 
                      label={tag} 
                      size="small" 
                      variant="outlined"
                      sx={{ fontSize: '0.7rem' }}
                    />
                  ))}
                </Box>
              </CardContent>
              
              <CardActions sx={{ p: 2, pt: 0 }}>
                <Button 
                  component={RouterLink} 
                  to={form.route}
                  variant="contained" 
                  disabled={form.comingSoon}
                  fullWidth
                >
                  {form.comingSoon ? 'Coming Soon' : 'Create Form'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      <Paper elevation={1} sx={{ p: 3, mt: 4, bgcolor: 'background.paper' }}>
        <Typography variant="h6" gutterBottom>
          Need Help?
        </Typography>
        <Typography variant="body2" paragraph>
          Our forms are designed to be easy to use, but legal matters can be complex. If you need assistance or have questions, consider:
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Button 
              variant="outlined" 
              component={RouterLink}
              to="/virtual-paralegal"
              fullWidth
            >
              Ask Virtual Paralegal
            </Button>
          </Grid>
          <Grid item xs={12} md={4}>
            <Button 
              variant="outlined"
              component={RouterLink}
              to="/resources"
              fullWidth
            >
              View Resources
            </Button>
          </Grid>
          <Grid item xs={12} md={4}>
            <Button 
              variant="outlined"
              component={RouterLink}
              to="/contact"
              fullWidth
            >
              Contact Support
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default FormsIndexPage; 
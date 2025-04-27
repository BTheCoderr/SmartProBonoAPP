import React from 'react';
import { 
  Container, 
  Typography, 
  Paper, 
  Box,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Button 
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArticleIcon from '@mui/icons-material/Article';
import GavelIcon from '@mui/icons-material/Gavel';
import ExpungementWizard from '../components/ExpungementWizard';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ExpungementPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const benefits = [
    'Improve your employment opportunities',
    'Increase housing options',
    'Clear your public record',
    'Restore certain rights',
    'Reduce stigma and discrimination'
  ];

  const eligibilityRequirements = [
    'Completed all terms of your sentence',
    'Waiting period has passed (varies by state)',
    'No current charges pending',
    'Certain offenses may not be eligible'
  ];

  const handleStartClick = () => {
    if (!isAuthenticated) {
      // Redirect to login page if not authenticated
      navigate('/login', { state: { from: '/expungement' } });
    } else {
      // Scroll to the wizard section
      const element = document.getElementById('expungement-wizard');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Criminal Record Expungement
        </Typography>
        
        <Typography variant="h6" color="textSecondary" gutterBottom>
          Clear your record and get a fresh start
        </Typography>
        
        <Grid container spacing={4} sx={{ mt: 2, mb: 6 }}>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Typography variant="h5" gutterBottom>
                <GavelIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                What is Expungement?
              </Typography>
              
              <Typography variant="body1" paragraph>
                Expungement is a legal process that allows you to clear or seal your criminal record 
                from public view. It gives you a chance to move forward without past mistakes holding you back.
              </Typography>
              
              <Typography variant="body1" paragraph>
                While the expungement process varies by state, our tool guides you through the steps and
                helps prepare the necessary paperwork for your jurisdiction.
              </Typography>
              
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Benefits of Expungement
                </Typography>
                
                <List>
                  {benefits.map((benefit, index) => (
                    <ListItem key={index} sx={{ py: 0.5 }}>
                      <ListItemIcon>
                        <CheckCircleIcon color="success" />
                      </ListItemIcon>
                      <ListItemText primary={benefit} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Typography variant="h5" gutterBottom>
                <ArticleIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Eligibility & Process
              </Typography>
              
              <Typography variant="body1" paragraph>
                While eligibility requirements vary by state, generally you may be eligible if:
              </Typography>
              
              <List>
                {eligibilityRequirements.map((requirement, index) => (
                  <ListItem key={index} sx={{ py: 0.5 }}>
                    <ListItemIcon>
                      <CheckCircleIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={requirement} />
                  </ListItem>
                ))}
              </List>
              
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  How Our Tool Helps
                </Typography>
                
                <Typography variant="body1" paragraph>
                  Our expungement tool will:
                </Typography>
                
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="secondary" />
                    </ListItemIcon>
                    <ListItemText primary="Check your eligibility based on your case details" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="secondary" />
                    </ListItemIcon>
                    <ListItemText primary="Provide state-specific guidance and requirements" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="secondary" />
                    </ListItemIcon>
                    <ListItemText primary="Generate the necessary court documents" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="secondary" />
                    </ListItemIcon>
                    <ListItemText primary="Offer step-by-step filing instructions" />
                  </ListItem>
                </List>
              </Box>
            </Paper>
          </Grid>
        </Grid>
        
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Button 
            variant="contained" 
            color="primary" 
            size="large"
            onClick={handleStartClick}
            sx={{ px: 4, py: 1.5 }}
          >
            Start Expungement Process
          </Button>
          
          <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
            {isAuthenticated ? 'Begin your fresh start today!' : 'Sign in or create an account to get started'}
          </Typography>
        </Box>
        
        <Divider sx={{ mb: 6 }} />
        
        <Box id="expungement-wizard">
          {isAuthenticated ? (
            <ExpungementWizard />
          ) : (
            <Card sx={{ p: 3, textAlign: 'center' }}>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Sign in to start the expungement process
                </Typography>
                <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
                  You'll need an account to use our expungement tool and save your progress.
                </Typography>
                <Button 
                  variant="contained" 
                  color="primary"
                  onClick={() => navigate('/login', { state: { from: '/expungement' } })}
                >
                  Sign In or Register
                </Button>
              </CardContent>
            </Card>
          )}
        </Box>
      </Box>
    </Container>
  );
};

export default ExpungementPage; 
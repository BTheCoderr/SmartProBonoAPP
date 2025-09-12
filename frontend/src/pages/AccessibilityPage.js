import React from 'react';
import { Container, Typography, Box, Paper, Divider, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { CheckCircle, Computer, Smartphone, VolumeUp } from '@mui/icons-material';
import Header from '../components/Header';
import Footer from '../components/Footer';

const AccessibilityPage = () => {
  return (
    <>
      <Header />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Accessibility Statement
          </Typography>
          
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 4 }}>
            Last updated: {new Date().toLocaleDateString()}
          </Typography>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Our Commitment
            </Typography>
            <Typography variant="body1" paragraph>
              SmartProBono is committed to ensuring digital accessibility for people with disabilities. 
              We are continually improving the user experience for everyone and applying the relevant 
              accessibility standards to make our platform more inclusive.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Accessibility Features
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Keyboard Navigation" 
                  secondary="Full keyboard navigation support for all interactive elements"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Screen Reader Compatibility" 
                  secondary="Compatible with major screen readers including NVDA, JAWS, and VoiceOver"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="High Contrast Mode" 
                  secondary="Support for high contrast display settings"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Text Scaling" 
                  secondary="Text can be scaled up to 200% without loss of functionality"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Alternative Text" 
                  secondary="All images include descriptive alternative text"
                />
              </ListItem>
            </List>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Supported Technologies
            </Typography>
            <Typography variant="body1" paragraph>
              Our platform is designed to be compatible with:
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <Computer color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Desktop Browsers" 
                  secondary="Chrome, Firefox, Safari, Edge (latest versions)"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Smartphone color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Mobile Devices" 
                  secondary="iOS and Android with accessibility features enabled"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <VolumeUp color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Assistive Technologies" 
                  secondary="Screen readers, voice recognition software, and other assistive tools"
                />
              </ListItem>
            </List>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Standards Compliance
            </Typography>
            <Typography variant="body1" paragraph>
              We aim to conform to the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA 
              standards. These guidelines help make web content more accessible to people with 
              disabilities and user-friendly for everyone.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Known Limitations
            </Typography>
            <Typography variant="body1" paragraph>
              While we strive to make our platform fully accessible, we acknowledge that some 
              areas may need improvement. We are actively working to address these limitations 
              and welcome feedback from users.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Feedback and Support
            </Typography>
            <Typography variant="body1" paragraph>
              If you encounter any accessibility barriers or have suggestions for improvement, 
              please contact us:
            </Typography>
            <Typography variant="body1">
              Email: accessibility@smartprobono.com<br />
              Phone: [Your Phone Number]<br />
              Address: SmartProBono Legal Services<br />
              [Your Address Here]
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Alternative Formats
            </Typography>
            <Typography variant="body1" paragraph>
              We can provide information in alternative formats upon request, including:
            </Typography>
            <Typography component="ul" sx={{ pl: 2 }}>
              <li>Large print documents</li>
              <li>Audio recordings</li>
              <li>Braille materials</li>
              <li>Plain language versions</li>
            </Typography>
          </Box>

          <Divider sx={{ my: 3 }} />
          
          <Typography variant="body2" color="text.secondary" align="center">
            This accessibility statement is effective as of {new Date().toLocaleDateString()} and 
            will be updated as we continue to improve our platform's accessibility.
          </Typography>
        </Paper>
      </Container>
      <Footer />
    </>
  );
};

export default AccessibilityPage;
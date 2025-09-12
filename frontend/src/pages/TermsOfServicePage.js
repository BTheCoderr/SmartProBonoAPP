import React from 'react';
import { Container, Typography, Box, Paper, Divider } from '@mui/material';
import Header from '../components/Header';
import Footer from '../components/Footer';

const TermsOfServicePage = () => {
  return (
    <>
      <Header />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Terms of Service
          </Typography>
          
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 4 }}>
            Last updated: {new Date().toLocaleDateString()}
          </Typography>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              1. Acceptance of Terms
            </Typography>
            <Typography variant="body1" paragraph>
              By accessing and using SmartProBono's services, you accept and agree to be bound by 
              the terms and provision of this agreement. If you do not agree to abide by the above, 
              please do not use this service.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              2. Description of Service
            </Typography>
            <Typography variant="body1" paragraph>
              SmartProBono provides technology-driven legal assistance services, including but not 
              limited to:
            </Typography>
            <Typography component="ul" sx={{ pl: 2 }}>
              <li>AI-powered legal document analysis</li>
              <li>Case management and tracking tools</li>
              <li>Legal resource libraries and guides</li>
              <li>Connection to legal professionals</li>
              <li>Document generation and processing</li>
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              3. User Responsibilities
            </Typography>
            <Typography variant="body1" paragraph>
              As a user of our services, you agree to:
            </Typography>
            <Typography component="ul" sx={{ pl: 2 }}>
              <li>Provide accurate and complete information</li>
              <li>Use the service only for lawful purposes</li>
              <li>Respect the intellectual property rights of others</li>
              <li>Not attempt to gain unauthorized access to our systems</li>
              <li>Not use the service to transmit harmful or malicious code</li>
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              4. Legal Disclaimer
            </Typography>
            <Typography variant="body1" paragraph>
              SmartProBono provides technology tools and resources but does not provide legal advice. 
              Our services are not a substitute for professional legal counsel. Users should consult 
              with qualified attorneys for specific legal matters.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              5. Limitation of Liability
            </Typography>
            <Typography variant="body1" paragraph>
              In no event shall SmartProBono be liable for any indirect, incidental, special, 
              consequential, or punitive damages, including without limitation, loss of profits, 
              data, use, goodwill, or other intangible losses, resulting from your use of the service.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              6. Privacy and Data Protection
            </Typography>
            <Typography variant="body1" paragraph>
              Your privacy is important to us. Please review our Privacy Policy, which also governs 
              your use of the service, to understand our practices.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              7. Modifications
            </Typography>
            <Typography variant="body1" paragraph>
              We reserve the right to modify these terms at any time. We will notify users of any 
              material changes by posting the new terms on this page and updating the "Last updated" 
              date.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              8. Contact Information
            </Typography>
            <Typography variant="body1" paragraph>
              If you have any questions about these Terms of Service, please contact us at:
            </Typography>
            <Typography variant="body1">
              Email: legal@smartprobono.com<br />
              Address: SmartProBono Legal Services<br />
              [Your Address Here]
            </Typography>
          </Box>

          <Divider sx={{ my: 3 }} />
          
          <Typography variant="body2" color="text.secondary" align="center">
            These terms of service are effective as of {new Date().toLocaleDateString()} and will 
            remain in effect except with respect to any changes in its provisions in the future.
          </Typography>
        </Paper>
      </Container>
      <Footer />
    </>
  );
};

export default TermsOfServicePage;
import React from 'react';
import { Container, Typography, Box, Paper, Divider } from '@mui/material';
import Header from '../components/Header';
import Footer from '../components/Footer';

const PrivacyPolicyPage = () => {
  return (
    <>
      <Header />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Privacy Policy
          </Typography>
          
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 4 }}>
            Last updated: {new Date().toLocaleDateString()}
          </Typography>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              1. Information We Collect
            </Typography>
            <Typography variant="body1" paragraph>
              We collect information you provide directly to us, such as when you create an account, 
              use our services, or contact us for support. This may include:
            </Typography>
            <Typography component="ul" sx={{ pl: 2 }}>
              <li>Name, email address, and contact information</li>
              <li>Legal case information and documents</li>
              <li>Communication preferences</li>
              <li>Payment information (processed securely through third-party providers)</li>
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              2. How We Use Your Information
            </Typography>
            <Typography variant="body1" paragraph>
              We use the information we collect to:
            </Typography>
            <Typography component="ul" sx={{ pl: 2 }}>
              <li>Provide, maintain, and improve our legal services</li>
              <li>Process transactions and send related information</li>
              <li>Send technical notices, updates, and support messages</li>
              <li>Respond to your comments and questions</li>
              <li>Monitor and analyze trends and usage</li>
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              3. Information Sharing
            </Typography>
            <Typography variant="body1" paragraph>
              We do not sell, trade, or otherwise transfer your personal information to third parties 
              without your consent, except as described in this policy. We may share your information:
            </Typography>
            <Typography component="ul" sx={{ pl: 2 }}>
              <li>With your consent</li>
              <li>To comply with legal obligations</li>
              <li>To protect our rights and safety</li>
              <li>With service providers who assist us in operating our platform</li>
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              4. Data Security
            </Typography>
            <Typography variant="body1" paragraph>
              We implement appropriate security measures to protect your personal information against 
              unauthorized access, alteration, disclosure, or destruction. However, no method of 
              transmission over the internet is 100% secure.
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              5. Your Rights
            </Typography>
            <Typography variant="body1" paragraph>
              You have the right to:
            </Typography>
            <Typography component="ul" sx={{ pl: 2 }}>
              <li>Access your personal information</li>
              <li>Correct inaccurate information</li>
              <li>Delete your personal information</li>
              <li>Object to processing of your information</li>
              <li>Data portability</li>
            </Typography>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              6. Contact Us
            </Typography>
            <Typography variant="body1" paragraph>
              If you have any questions about this Privacy Policy, please contact us at:
            </Typography>
            <Typography variant="body1">
              Email: privacy@smartprobono.com<br />
              Address: SmartProBono Legal Services<br />
              [Your Address Here]
            </Typography>
          </Box>

          <Divider sx={{ my: 3 }} />
          
          <Typography variant="body2" color="text.secondary" align="center">
            This privacy policy is effective as of {new Date().toLocaleDateString()} and will remain 
            in effect except with respect to any changes in its provisions in the future.
          </Typography>
        </Paper>
      </Container>
      <Footer />
    </>
  );
};

export default PrivacyPolicyPage;
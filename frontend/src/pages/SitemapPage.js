import React from 'react';
import { Container, Typography, Box, Paper, Grid, Link, List, ListItem } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';

const SitemapPage = () => {
  const mainPages = [
    { name: 'Home', path: '/' },
    { name: 'About Us', path: '/about' },
    { name: 'Services', path: '/services' },
    { name: 'Resources', path: '/resources' },
    { name: 'Contact', path: '/contact' },
  ];

  const legalTools = [
    { name: 'Legal Tools', path: '/legal-tools' },
    { name: 'Document Scanner', path: '/scan-document' },
    { name: 'PDF Generator', path: '/generate-document' },
    { name: 'AI Legal Chat', path: '/legal-chat' },
    { name: 'Safety Check', path: '/safety-check' },
  ];

  const crmSystems = [
    { name: 'Client Portal', path: '/client-portal' },
    { name: 'Bondsman Dashboard', path: '/bondsman-dashboard' },
    { name: 'AI Virtual Paralegal', path: '/ai-virtual-paralegal' },
  ];

  const resources = [
    { name: 'Rights Information', path: '/rights' },
    { name: 'Immigration Rights', path: '/rights/immigration' },
    { name: 'Legal Guides', path: '/resources/guides' },
    { name: 'External Resources', path: '/resources/external' },
    { name: 'FAQ', path: '/faq' },
    { name: 'Glossary', path: '/glossary' },
  ];

  const legal = [
    { name: 'Privacy Policy', path: '/privacy' },
    { name: 'Terms of Service', path: '/terms' },
    { name: 'Accessibility', path: '/accessibility' },
  ];

  const support = [
    { name: 'Help Center', path: '/help' },
    { name: 'Bug Report', path: '/bug-report' },
    { name: 'Feature Request', path: '/feature-request' },
    { name: 'Status Page', path: '/status' },
  ];

  const company = [
    { name: 'Our Mission', path: '/mission' },
    { name: 'Team', path: '/team' },
    { name: 'Careers', path: '/careers' },
    { name: 'Partners', path: '/partners' },
    { name: 'Press', path: '/press' },
  ];

  return (
    <>
      <Header />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Sitemap
          </Typography>
          
          <Typography variant="body1" align="center" sx={{ mb: 4 }}>
            Find all pages and sections of the SmartProBono platform
          </Typography>

          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom color="primary">
                  Main Pages
                </Typography>
                <List dense>
                  {mainPages.map((page) => (
                    <ListItem key={page.name} sx={{ pl: 0 }}>
                      <Link component={RouterLink} to={page.path} color="inherit">
                        {page.name}
                      </Link>
                    </ListItem>
                  ))}
                </List>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom color="primary">
                  Legal Tools
                </Typography>
                <List dense>
                  {legalTools.map((page) => (
                    <ListItem key={page.name} sx={{ pl: 0 }}>
                      <Link component={RouterLink} to={page.path} color="inherit">
                        {page.name}
                      </Link>
                    </ListItem>
                  ))}
                </List>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom color="primary">
                  CRM Systems
                </Typography>
                <List dense>
                  {crmSystems.map((page) => (
                    <ListItem key={page.name} sx={{ pl: 0 }}>
                      <Link component={RouterLink} to={page.path} color="inherit">
                        {page.name}
                      </Link>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom color="primary">
                  Resources
                </Typography>
                <List dense>
                  {resources.map((page) => (
                    <ListItem key={page.name} sx={{ pl: 0 }}>
                      <Link component={RouterLink} to={page.path} color="inherit">
                        {page.name}
                      </Link>
                    </ListItem>
                  ))}
                </List>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom color="primary">
                  Legal & Policies
                </Typography>
                <List dense>
                  {legal.map((page) => (
                    <ListItem key={page.name} sx={{ pl: 0 }}>
                      <Link component={RouterLink} to={page.path} color="inherit">
                        {page.name}
                      </Link>
                    </ListItem>
                  ))}
                </List>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom color="primary">
                  Support
                </Typography>
                <List dense>
                  {support.map((page) => (
                    <ListItem key={page.name} sx={{ pl: 0 }}>
                      <Link component={RouterLink} to={page.path} color="inherit">
                        {page.name}
                      </Link>
                    </ListItem>
                  ))}
                </List>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom color="primary">
                  Company
                </Typography>
                <List dense>
                  {company.map((page) => (
                    <ListItem key={page.name} sx={{ pl: 0 }}>
                      <Link component={RouterLink} to={page.path} color="inherit">
                        {page.name}
                      </Link>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, p: 3, bgcolor: 'grey.50', borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              Need Help Finding Something?
            </Typography>
            <Typography variant="body1" paragraph>
              If you can't find what you're looking for, try our search function or contact our 
              support team. We're here to help you navigate our platform and find the resources 
              you need.
            </Typography>
            <Typography variant="body1">
              <Link component={RouterLink} to="/help" color="primary">
                Visit our Help Center
              </Link>
              {' or '}
              <Link component={RouterLink} to="/contact" color="primary">
                Contact Support
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Container>
      <Footer />
    </>
  );
};

export default SitemapPage;
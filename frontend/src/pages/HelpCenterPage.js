import React from 'react';
import { Container, Typography, Box, Grid, Card, CardContent, Button } from '@mui/material';
import { Help as HelpIcon, Support as SupportIcon, Chat as ChatIcon } from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const HelpCenterPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          Help Center
        </Typography>
        <Typography variant="h5" color="text.secondary">
          Get the support you need
        </Typography>
      </Box>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ textAlign: 'center', p: 2 }}>
            <CardContent>
              <HelpIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>FAQ</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Find answers to common questions
              </Typography>
              <Button variant="contained">View FAQ</Button>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ textAlign: 'center', p: 2 }}>
            <CardContent>
              <SupportIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>Contact Support</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Get help from our support team
              </Typography>
              <Button variant="contained" color="success">Contact Us</Button>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ textAlign: 'center', p: 2 }}>
            <CardContent>
              <ChatIcon sx={{ fontSize: 48, color: 'info.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>Live Chat</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Chat with us in real-time
              </Typography>
              <Button variant="contained" color="info">Start Chat</Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  </PageLayout>
);

export default HelpCenterPage;

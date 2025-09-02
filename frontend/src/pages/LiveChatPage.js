import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Avatar, 
  Chip,
  Paper,
  Alert,
  Grid
} from '@mui/material';
import { 
  Chat as ChatIcon,
  Person as PersonIcon,
  Support as SupportIcon
} from '@mui/icons-material';
import { PageLayout, Section, Button, Card } from '../design-system';
import AIEnhancedChat from '../components/AIEnhancedChat';

const LiveChatPage = () => {
  const [isChatActive, setIsChatActive] = useState(false);

  const handleStartChat = () => {
    setIsChatActive(true);
  };

  if (!isChatActive) {
    return (
      <PageLayout
        title="AI Support Assistant"
        description="Get instant help from our AI-powered legal assistant"
      >
        <Section sx={{ py: 8 }}>
          <Container maxWidth="md">
            <Box sx={{ textAlign: 'center', mb: 6 }}>
              <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
                AI Support Assistant
              </Typography>
              <Typography variant="h5" color="text.secondary" sx={{ mb: 4 }}>
                Get instant help from our AI-powered legal assistant
              </Typography>
            </Box>
            
            <Card sx={{ textAlign: 'center', p: 6 }}>
              <Box sx={{ mb: 4 }}>
                <Avatar
                  sx={{
                    width: 80,
                    height: 80,
                    bgcolor: 'primary.main',
                    mx: 'auto',
                    mb: 3
                  }}
                >
                  <ChatIcon sx={{ fontSize: 40 }} />
                </Avatar>
                <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
                  Chat with AI Assistant
                </Typography>
                <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
                  Our AI assistant is available 24/7 to help you with legal questions and document guidance.
                </Typography>
              </Box>

              <Box sx={{ mb: 4 }}>
                <Grid container spacing={3} justifyContent="center">
                  <Grid item xs={12} sm={4}>
                    <Box sx={{ textAlign: 'center' }}>
                      <SupportIcon sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        AI-Powered Help
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Advanced AI trained on legal knowledge
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Box sx={{ textAlign: 'center' }}>
                      <ChatIcon sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        Instant Responses
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        AI provides immediate answers to your questions
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Box sx={{ textAlign: 'center' }}>
                      <PersonIcon sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        Smart Guidance
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        AI adapts responses to your specific situation
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Box>

              <Button
                variant="contained"
                size="large"
                onClick={handleStartChat}
                sx={{
                  px: 6,
                  py: 2,
                  fontSize: '1.1rem',
                  fontWeight: 600
                }}
              >
                Start AI Chat
              </Button>
            </Card>
          </Container>
        </Section>
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title="AI Support Assistant"
      description="Chat with our AI-powered legal assistant"
    >
      <Section sx={{ py: 4 }}>
        <Container maxWidth="md">
          <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                <SupportIcon />
              </Avatar>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  AI Legal Assistant
                </Typography>
                <Chip 
                  label="AI Active" 
                  color="primary" 
                  size="small" 
                  sx={{ height: 20, fontSize: '0.75rem' }}
                />
              </Box>
            </Box>
            <Button
              variant="outlined"
              size="small"
              onClick={() => setIsChatActive(false)}
            >
              End Chat
            </Button>
          </Box>

          <Paper
            sx={{
              height: 500,
              display: 'flex',
              flexDirection: 'column',
              border: '1px solid',
              borderColor: 'divider'
            }}
          >
            <AIEnhancedChat />
          </Paper>

          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="body2">
              <strong>AI Assistant Notice:</strong> This is an AI-powered assistant that provides general legal information. 
              For specific legal advice, please consult with a qualified attorney. This is not a substitute for professional legal counsel.
            </Typography>
          </Alert>
        </Container>
      </Section>
    </PageLayout>
  );
};

export default LiveChatPage;

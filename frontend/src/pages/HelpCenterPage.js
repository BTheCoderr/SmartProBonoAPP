import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  TextField,
  InputAdornment,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import { 
  Help as HelpIcon, 
  Support as SupportIcon, 
  Chat as ChatIcon,
  Search as SearchIcon,
  ExpandMore as ExpandMoreIcon,
  QuestionMark as QuestionMarkIcon,
  BugReport as BugReportIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  Article as ArticleIcon,
  VideoLibrary as VideoIcon,
  Book as BookIcon
} from '@mui/icons-material';
import { PageLayout } from '../design-system';
import { useNavigate } from 'react-router-dom';

const HelpCenterPage = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedFaq, setExpandedFaq] = useState(false);

  const faqData = [
    {
      question: "How do I create an account?",
      answer: "Click the 'Sign Up' button in the top right corner, fill in your information, and verify your email address. It's completely free to get started!"
    },
    {
      question: "How does the document scanner work?",
      answer: "Upload your legal document (PDF, image, or Word file) and our AI will analyze it to identify key information, potential issues, and provide actionable insights."
    },
    {
      question: "Is my data secure?",
      answer: "Yes! We use enterprise-grade encryption and never share your personal information. All documents are processed securely and can be deleted at any time."
    },
    {
      question: "Can I get legal advice from the AI chat?",
      answer: "Our AI provides general legal information and guidance, but it's not a substitute for professional legal advice. Always consult with a qualified attorney for specific legal matters."
    },
    {
      question: "How much does SmartProBono cost?",
      answer: "Basic features are completely free! Premium features like advanced document analysis and priority support are available with our affordable subscription plans."
    }
  ];

  const quickLinks = [
    { title: "Contact Support", icon: <SupportIcon />, path: "/contact", color: "primary" },
    { title: "Report a Bug", icon: <BugReportIcon />, path: "/bug-report", color: "error" },
    { title: "Feature Request", icon: <HelpIcon />, path: "/feature-request", color: "success" }
  ];

  const resources = [
    { title: "User Guide", icon: <BookIcon />, description: "Complete guide to using SmartProBono" },
    { title: "Video Tutorials", icon: <VideoIcon />, description: "Step-by-step video instructions" },
    { title: "Legal Templates", icon: <ArticleIcon />, description: "Downloadable legal document templates" }
  ];

  return (
    <PageLayout
      title="Help Center"
      description="Find answers to common questions and get support"
    >
      <Container maxWidth="lg">
        {/* Search Section */}
        <Box sx={{ mb: 6 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
            Search Help Articles
          </Typography>
          <TextField
            fullWidth
            placeholder="Search for help topics..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon color="action" />
                </InputAdornment>
              ),
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }
            }}
          />
        </Box>

        <Grid container spacing={4}>
          {/* Quick Links */}
          <Grid item xs={12} md={4}>
            <Card sx={{ mb: 3, borderRadius: 2, boxShadow: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                  Quick Links
                </Typography>
                <List>
                  {quickLinks.map((link, index) => (
                    <ListItem 
                      key={index}
                      button 
                      onClick={() => navigate(link.path)}
                      sx={{ 
                        borderRadius: 1, 
                        mb: 1,
                        '&:hover': { bgcolor: 'action.hover' }
                      }}
                    >
                      <ListItemIcon>
                        <Box sx={{ color: `${link.color}.main` }}>
                          {link.icon}
                        </Box>
                      </ListItemIcon>
                      <ListItemText 
                        primary={link.title}
                        primaryTypographyProps={{ fontWeight: 500 }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>

            {/* Resources */}
            <Card sx={{ borderRadius: 2, boxShadow: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                  Resources
                </Typography>
                <List>
                  {resources.map((resource, index) => (
                    <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start', py: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Box sx={{ color: 'primary.main', mr: 2 }}>
                          {resource.icon}
                        </Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                          {resource.title}
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ ml: 5 }}>
                        {resource.description}
                      </Typography>
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* FAQ Section */}
          <Grid item xs={12} md={8}>
            <Card sx={{ borderRadius: 2, boxShadow: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <QuestionMarkIcon sx={{ color: 'primary.main', mr: 2, fontSize: 28 }} />
                  <Typography variant="h6" sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                    Frequently Asked Questions
                  </Typography>
                </Box>
                
                <Box sx={{ mb: 2 }}>
                  <Chip 
                    label="Getting Started" 
                    color="primary" 
                    size="small" 
                    sx={{ mr: 1, mb: 1 }}
                  />
                </Box>

                {faqData.map((faq, index) => (
                  <Accordion 
                    key={index}
                    expanded={expandedFaq === index}
                    onChange={() => setExpandedFaq(expandedFaq === index ? false : index)}
                    sx={{ 
                      mb: 1, 
                      borderRadius: 1,
                      '&:before': { display: 'none' },
                      boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                    }}
                  >
                    <AccordionSummary
                      expandIcon={<ExpandMoreIcon />}
                      sx={{ 
                        '& .MuiAccordionSummary-content': { margin: '12px 0' }
                      }}
                    >
                      <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                        {faq.question}
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2" color="text.secondary">
                        {faq.answer}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                ))}
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Contact Support Section */}
        <Box sx={{ mt: 6, textAlign: 'center' }}>
          <Card sx={{ borderRadius: 2, boxShadow: 2, p: 4 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                Still Need Help?
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Can't find what you're looking for? Our support team is here to help.
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  startIcon={<EmailIcon />}
                  onClick={() => navigate('/contact')}
                  sx={{ borderRadius: 2 }}
                >
                  Contact Support
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<PhoneIcon />}
                  sx={{ borderRadius: 2 }}
                >
                  Call Us
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default HelpCenterPage;

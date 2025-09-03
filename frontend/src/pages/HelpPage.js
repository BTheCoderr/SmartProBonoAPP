import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,

  Paper,

  InputAdornment
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Search as SearchIcon,
  Help as HelpIcon,
  QuestionAnswer as QuestionAnswerIcon,

  Description as DescriptionIcon,
  ContactSupport as ContactSupportIcon,
  BugReport as BugReportIcon,
  Lightbulb as LightbulbIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,

} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const HelpPage = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const faqCategories = [
    {
      title: 'Getting Started',
      icon: <HelpIcon />,
      questions: [
        {
          question: 'How do I create an account?',
          answer: 'Click the "Sign Up" button in the top right corner, fill in your information, and verify your email address.'
        },
        {
          question: 'What can SmartProBono help me with?',
          answer: 'SmartProBono provides AI-powered legal assistance, document generation, compliance guidance, and connects you with legal resources for immigration, family law, business law, and more.'
        },
        {
          question: 'Is SmartProBono free to use?',
          answer: 'Yes! SmartProBono offers free legal assistance and resources. Some premium features may be available for advanced users.'
        }
      ]
    },
    {
      title: 'AI Chat & Legal Assistance',
      icon: <QuestionAnswerIcon />,
      questions: [
        {
          question: 'How does the AI legal chat work?',
          answer: 'Our AI system uses specialized legal agents to provide accurate, contextual legal guidance. Each agent specializes in different areas of law and can help with specific questions.'
        },
        {
          question: 'Can the AI replace a real lawyer?',
          answer: 'No, our AI provides general legal information and guidance. For complex legal matters, we always recommend consulting with a qualified attorney.'
        },
        {
          question: 'What types of legal questions can I ask?',
          answer: 'You can ask about immigration law, family law, business law, criminal law, compliance issues, document generation, and general legal procedures.'
        }
      ]
    },
    {
      title: 'Document Generation',
      icon: <DescriptionIcon />,
      questions: [
        {
          question: 'What documents can I generate?',
          answer: 'You can generate various legal documents including contracts, forms, letters, and templates for immigration, business, family law, and other legal matters.'
        },
        {
          question: 'Are generated documents legally binding?',
          answer: 'Generated documents are templates and starting points. They should be reviewed by a qualified attorney before use to ensure they meet your specific legal needs.'
        },
        {
          question: 'How do I customize document templates?',
          answer: 'Use our document builder to fill in your specific information, and the system will generate a customized document based on your inputs.'
        }
      ]
    },
    {
      title: 'Account & Security',
      icon: <SecurityIcon />,
      questions: [
        {
          question: 'How is my data protected?',
          answer: 'We use industry-standard encryption and security measures to protect your personal information. All data is stored securely and never shared without your consent.'
        },
        {
          question: 'Can I delete my account?',
          answer: 'Yes, you can delete your account at any time from your profile settings. This will permanently remove all your data from our systems.'
        },
        {
          question: 'What if I forget my password?',
          answer: 'Use the "Forgot Password" link on the login page to reset your password via email.'
        }
      ]
    },
    {
      title: 'Technical Issues',
      icon: <SpeedIcon />,
      questions: [
        {
          question: 'The page is loading slowly. What should I do?',
          answer: 'Try refreshing the page, clearing your browser cache, or using a different browser. If the issue persists, contact our support team.'
        },
        {
          question: 'I\'m getting an error message. What does it mean?',
          answer: 'Error messages usually indicate a temporary issue. Try refreshing the page or logging out and back in. If the error continues, report it using our bug report form.'
        },
        {
          question: 'Which browsers are supported?',
          answer: 'SmartProBono works best with Chrome, Firefox, Safari, and Edge. Make sure you\'re using the latest version of your browser.'
        }
      ]
    }
  ];

  const quickLinks = [
    { title: 'Contact Support', path: '/contact', icon: <ContactSupportIcon /> },
    { title: 'Report a Bug', path: '/bug-report', icon: <BugReportIcon /> },
    { title: 'Feature Request', path: '/feature-request', icon: <LightbulbIcon /> },
    { title: 'System Status', path: '/status', icon: <SpeedIcon /> }
  ];

  const filteredFAQs = faqCategories.map(category => ({
    ...category,
    questions: category.questions.filter(q => 
      q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.answer.toLowerCase().includes(searchQuery.toLowerCase())
    )
  })).filter(category => category.questions.length > 0);

  return (
    <PageLayout
      title="Help Center"
      description="Find answers to common questions and get support"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Search Section */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
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
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Paper>

        <Grid container spacing={4}>
          {/* Quick Links */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quick Links
                </Typography>
                <List>
                  {quickLinks.map((link, index) => (
                    <ListItem
                      key={index}
                      component="a"
                      href={link.path}
                      sx={{
                        cursor: 'pointer',
                        '&:hover': { bgcolor: 'action.hover' },
                        borderRadius: 1
                      }}
                    >
                      <ListItemIcon>{link.icon}</ListItemIcon>
                      <ListItemText primary={link.title} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>

            {/* Contact Info */}
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Need More Help?
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Can't find what you're looking for? Our support team is here to help.
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" fontWeight="bold">
                    Email Support:
                  </Typography>
                  <Typography variant="body2" color="primary">
                    support@smartprobono.org
                  </Typography>
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" fontWeight="bold">
                    Phone Support:
                  </Typography>
                  <Typography variant="body2">
                    (401) 217-9799
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" fontWeight="bold">
                    Business Hours:
                  </Typography>
                  <Typography variant="body2">
                    Monday - Friday: 9 AM - 6 PM EST
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* FAQ Section */}
          <Grid item xs={12} md={8}>
            <Typography variant="h5" gutterBottom>
              Frequently Asked Questions
            </Typography>
            
            {searchQuery && (
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Showing results for "{searchQuery}"
              </Typography>
            )}

            {filteredFAQs.length === 0 && searchQuery ? (
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="h6" gutterBottom>
                  No results found
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Try different keywords or browse our categories below.
                </Typography>
              </Paper>
            ) : (
              filteredFAQs.map((category, categoryIndex) => (
                <Box key={categoryIndex} sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {category.icon}
                    {category.title}
                  </Typography>
                  
                  {category.questions.map((faq, faqIndex) => (
                    <Accordion key={faqIndex} sx={{ mb: 1 }}>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="subtitle1">
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
                </Box>
              ))
            )}

            {!searchQuery && (
              <Box sx={{ mt: 4 }}>
                <Typography variant="h6" gutterBottom>
                  Still Need Help?
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  If you can't find the answer you're looking for, don't hesitate to reach out to our support team.
                </Typography>
                <Button
                  variant="contained"
                  href="/contact"
                  sx={{ mr: 2 }}
                >
                  Contact Support
                </Button>
                <Button
                  variant="outlined"
                  href="/bug-report"
                >
                  Report an Issue
                </Button>
              </Box>
            )}
          </Grid>
        </Grid>
      </Container>
    </PageLayout>
  );
};

export default HelpPage;


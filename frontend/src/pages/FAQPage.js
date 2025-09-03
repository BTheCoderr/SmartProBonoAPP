import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField,
  InputAdornment,
  Grid,
  Chip
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Search as SearchIcon,
  Help as HelpIcon,
  QuestionAnswer as QuestionAnswerIcon
} from '@mui/icons-material';
import { PageLayout, Button, Card } from '../design-system';

const FAQPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [expanded, setExpanded] = useState(false);

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  const faqCategories = [
    {
      title: 'General Questions',
      icon: <HelpIcon />,
      questions: [
        {
          question: 'What is SmartProBono?',
          answer: 'SmartProBono is a free legal assistance platform that provides AI-powered document generation, legal guidance, and connects users with legal resources. Our mission is to make legal help accessible to everyone.'
        },
        {
          question: 'Is SmartProBono really free?',
          answer: 'Yes! Our core services including document generation, document scanning, and basic legal guidance are completely free. We believe everyone deserves access to legal assistance regardless of their financial situation.'
        },
        {
          question: 'Do I need to create an account?',
          answer: 'No account is required for most of our services. You can generate documents, scan documents, and access legal resources without signing up. Creating an account allows you to save your work and access additional features.'
        }
      ]
    },
    {
      title: 'Document Services',
      icon: <QuestionAnswerIcon />,
      questions: [
        {
          question: 'What types of documents can I generate?',
          answer: 'You can generate various legal documents including lease agreements, employment contracts, non-disclosure agreements, power of attorney documents, wills, and partnership agreements. We regularly add new templates.'
        },
        {
          question: 'How accurate are the generated documents?',
          answer: 'Our documents are created using industry-standard templates and legal best practices. However, we recommend having any important documents reviewed by a qualified attorney, as laws vary by jurisdiction.'
        },
        {
          question: 'Can I scan and analyze my existing documents?',
          answer: 'Yes! Our document scanner can analyze PDF, DOC, and DOCX files to identify potential issues, suggest improvements, and provide legal insights. This service is also free to use.'
        }
      ]
    },
    {
      title: 'Legal Guidance',
      icon: <HelpIcon />,
      questions: [
        {
          question: 'Is the legal advice provided by SmartProBono binding?',
          answer: 'No. The information provided by SmartProBono is for educational purposes only and does not constitute legal advice. For specific legal matters, you should consult with a qualified attorney.'
        },
        {
          question: 'How can I find a lawyer for my specific case?',
          answer: 'We provide resources to help you find qualified attorneys in your area. You can use our "Find Legal Help" feature to connect with legal aid organizations and private attorneys who specialize in your type of case.'
        },
        {
          question: 'What if I have an emergency legal situation?',
          answer: 'For emergency legal situations, call 911 if you\'re in immediate danger. For urgent legal matters, contact your local legal aid organization or use our emergency resources page to find immediate assistance.'
        }
      ]
    }
  ];

  const filteredCategories = faqCategories.map(category => ({
    ...category,
    questions: category.questions.filter(q => 
      q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      q.answer.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })).filter(category => category.questions.length > 0);

  return (
    <PageLayout>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Hero Section */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
            Frequently Asked Questions
          </Typography>
          <Typography variant="h5" color="text.secondary" sx={{ mb: 4 }}>
            Find answers to common questions about our services
          </Typography>
          <Button variant="contained" color="primary" size="large">
            Get Started
          </Button>
          
          <TextField
            fullWidth
            placeholder="Search FAQs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ maxWidth: 600, mx: 'auto' }}
          />
        </Box>

        {/* FAQ Categories */}
        {filteredCategories.map((category, categoryIndex) => (
          <Box key={categoryIndex} sx={{ mb: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              {category.icon}
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                {category.title}
              </Typography>
            </Box>
            
            {category.questions.map((faq, faqIndex) => (
              <Accordion
                key={faqIndex}
                expanded={expanded === `${categoryIndex}-${faqIndex}`}
                onChange={handleChange(`${categoryIndex}-${faqIndex}`)}
                sx={{ mb: 1 }}
              >
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6" sx={{ fontWeight: 'medium' }}>
                    {faq.question}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body1" color="text.secondary">
                    {faq.answer}
                  </Typography>
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        ))}

        {searchTerm && filteredCategories.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 6 }}>
            <Typography variant="h6" color="text.secondary">
              No FAQs found matching your search term.
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Try different keywords or browse all categories above.
            </Typography>
          </Box>
        )}

        {/* Contact Section */}
        <Box sx={{ mt: 8, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>
            Still Have Questions?
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            Can't find what you're looking for? We're here to help!
          </Typography>
          <Grid container spacing={3} justifyContent="center">
            <Grid item xs={12} sm={6} md={4}>
              <Card sx={{ textAlign: 'center', p: 2 }}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Contact Support
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Get help from our support team
                  </Typography>
                  <Chip label="support@smartprobono.org" color="primary" />
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Card sx={{ textAlign: 'center', p: 2 }}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Live Chat
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Chat with us in real-time
                  </Typography>
                  <Chip label="Available 24/7" color="success" />
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Card sx={{ textAlign: 'center', p: 2 }}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Legal Help
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Connect with legal professionals
                  </Typography>
                  <Chip label="Find an Attorney" color="info" />
                </Box>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default FAQPage;

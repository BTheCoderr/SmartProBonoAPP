import React from 'react';
import {
  Typography,
  Box,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider
} from '@mui/material';
import {
  VideoLibrary as VideoLibraryIcon,
  Description as DescriptionIcon,
  Article as ArticleIcon,
  School as SchoolIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { PageLayout, Section, Button, Card, CardContent, designTokens } from '../design-system';

const LegalGuidesPage = () => {
  const navigate = useNavigate();

  const legalGuides = [
    {
      title: 'Legal Process Overview',
      type: 'video',
      description: 'Comprehensive video guide explaining the general legal process and what to expect.',
      link: '/resources/guides/legal-process.mp4',
      icon: <VideoLibraryIcon />,
      category: 'Process'
    },
    {
      title: 'Document Templates',
      type: 'template',
      description: 'Common legal document templates for various legal situations.',
      link: '/resources/templates',
      icon: <DescriptionIcon />,
      category: 'Templates'
    },
    {
      title: 'Court Procedures',
      type: 'article',
      description: 'Step-by-step guide to court procedures and what to expect in different types of cases.',
      link: '/resources/guides/court-procedures',
      icon: <ArticleIcon />,
      category: 'Court'
    },
    {
      title: 'Legal Research Basics',
      type: 'article',
      description: 'How to conduct legal research and find relevant laws and cases.',
      link: '/resources/guides/legal-research',
      icon: <SchoolIcon />,
      category: 'Research'
    },
    {
      title: 'Understanding Legal Documents',
      type: 'video',
      description: 'Video guide to understanding common legal documents and terminology.',
      link: '/resources/guides/understanding-documents.mp4',
      icon: <VideoLibraryIcon />,
      category: 'Education'
    },
    {
      title: 'Contract Basics',
      type: 'article',
      description: 'Essential information about contracts, their elements, and enforceability.',
      link: '/resources/guides/contract-basics',
      icon: <ArticleIcon />,
      category: 'Contracts'
    },
    {
      title: 'Small Claims Court',
      type: 'pdf',
      description: 'Complete guide to filing and handling small claims court cases.',
      link: '/resources/guides/small-claims.pdf',
      icon: <DescriptionIcon />,
      category: 'Court'
    },
    {
      title: 'Legal Writing Tips',
      type: 'article',
      description: 'Best practices for legal writing and communication.',
      link: '/resources/guides/legal-writing',
      icon: <ArticleIcon />,
      category: 'Writing'
    }
  ];

  const categories = [...new Set(legalGuides.map(guide => guide.category))];

  return (
    <PageLayout
      title="Legal Guides"
      description="Comprehensive guides on various legal topics and procedures"
    >
      <Section>
        <Box sx={{ mb: 4 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/resources')}
            sx={{
              mb: 3,
              color: designTokens.colors.primary[600],
              '&:hover': {
                backgroundColor: designTokens.colors.primary[50]
              }
            }}
          >
            Back to Resources
          </Button>
          
          <Typography variant="h4" sx={{ 
            fontWeight: designTokens.typography.fontWeight.bold,
            color: designTokens.colors.neutral[900],
            mb: 2
          }}>
            Legal Guides
          </Typography>
          
          <Typography variant="body1" sx={{ 
            color: designTokens.colors.neutral[600],
            mb: 4,
            fontSize: '1.1rem',
            lineHeight: 1.6
          }}>
            Comprehensive guides on various legal topics, procedures, and best practices to help you navigate the legal system.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {categories.map((category, categoryIndex) => (
            <Grid item xs={12} key={categoryIndex}>
              <Card>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    {category}
                  </Typography>
                  <Divider sx={{ mb: 2 }} />
                  <List>
                    {legalGuides
                      .filter(guide => guide.category === category)
                      .map((guide, guideIndex) => (
                        <ListItem
                          key={guideIndex}
                          sx={{
                            mb: 2,
                            bgcolor: 'background.paper',
                            borderRadius: 1,
                            '&:hover': {
                              bgcolor: 'action.hover',
                            },
                          }}
                        >
                          <ListItemIcon>{guide.icon}</ListItemIcon>
                          <ListItemText
                            primary={
                              <Box display="flex" alignItems="center" gap={1}>
                                {guide.title}
                                <Chip
                                  label={guide.type}
                                  size="small"
                                  color={
                                    guide.type === 'pdf'
                                      ? 'error'
                                      : guide.type === 'video'
                                      ? 'primary'
                                      : guide.type === 'template'
                                      ? 'secondary'
                                      : 'default'
                                  }
                                />
                              </Box>
                            }
                            secondary={guide.description}
                          />
                          <Button
                            variant="outlined"
                            size="small"
                            href={guide.link}
                            target={guide.type === 'link' ? '_blank' : '_self'}
                            rel={guide.type === 'link' ? 'noopener noreferrer' : ''}
                          >
                            {guide.type === 'link' ? 'Visit' : 'View'}
                          </Button>
                        </ListItem>
                      ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom>
            Need More Help?
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            These guides provide general information. For specific legal advice, consult with a qualified attorney.
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/legal-chat')}
            sx={{ mr: 2 }}
          >
            Chat with AI Legal Assistant
          </Button>
          <Button
            variant="outlined"
            onClick={() => navigate('/contact')}
          >
            Contact Support
          </Button>
        </Box>
      </Section>
    </PageLayout>
  );
};

export default LegalGuidesPage;


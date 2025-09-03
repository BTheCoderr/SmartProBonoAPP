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
  PictureAsPdf as PictureAsPdfIcon,
  Article as ArticleIcon,
  VideoLibrary as VideoLibraryIcon,
  Description as DescriptionIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { PageLayout, Section, Button, Card, CardContent, designTokens } from '../design-system';

const ImmigrationResourcesPage = () => {
  const navigate = useNavigate();

  const immigrationResources = [
    {
      title: 'Immigration Forms Guide',
      type: 'pdf',
      description: 'Step-by-step guide for common immigration forms including I-485, I-130, I-765, and more.',
      link: '/resources/immigration/forms-guide.pdf',
      icon: <PictureAsPdfIcon />,
      category: 'Forms'
    },
    {
      title: 'Document Checklist',
      type: 'pdf',
      description: 'Comprehensive checklist of required documents for various immigration applications.',
      link: '/resources/immigration/document-checklist.pdf',
      icon: <PictureAsPdfIcon />,
      category: 'Checklists'
    },
    {
      title: 'Know Your Rights',
      type: 'article',
      description: 'Understanding your rights during immigration proceedings and interactions with ICE.',
      link: '/rights/immigration',
      icon: <ArticleIcon />,
      category: 'Rights'
    },
    {
      title: 'Green Card Process',
      type: 'article',
      description: 'Complete guide to obtaining permanent residency in the United States.',
      link: '/resources/immigration/green-card-process',
      icon: <ArticleIcon />,
      category: 'Process'
    },
    {
      title: 'Naturalization Guide',
      type: 'pdf',
      description: 'Step-by-step guide to becoming a U.S. citizen through naturalization.',
      link: '/resources/immigration/naturalization-guide.pdf',
      icon: <PictureAsPdfIcon />,
      category: 'Citizenship'
    },
    {
      title: 'Work Visa Options',
      type: 'article',
      description: 'Overview of different work visa categories and requirements.',
      link: '/resources/immigration/work-visas',
      icon: <ArticleIcon />,
      category: 'Work Visas'
    },
    {
      title: 'Family-Based Immigration',
      type: 'pdf',
      description: 'Guide to family-based immigration petitions and processes.',
      link: '/resources/immigration/family-based.pdf',
      icon: <PictureAsPdfIcon />,
      category: 'Family'
    },
    {
      title: 'Asylum and Refugee Status',
      type: 'article',
      description: 'Information about seeking asylum or refugee status in the United States.',
      link: '/resources/immigration/asylum-refugee',
      icon: <ArticleIcon />,
      category: 'Asylum'
    }
  ];

  const categories = [...new Set(immigrationResources.map(resource => resource.category))];

  return (
    <PageLayout
      title="Immigration Resources"
      description="Comprehensive immigration resources and guides"
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
            Immigration Resources
          </Typography>
          
          <Typography variant="body1" sx={{ 
            color: designTokens.colors.neutral[600],
            mb: 4,
            fontSize: '1.1rem',
            lineHeight: 1.6
          }}>
            Essential documents, guides, and information for immigration processes and procedures.
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
                    {immigrationResources
                      .filter(resource => resource.category === category)
                      .map((resource, resourceIndex) => (
                        <ListItem
                          key={resourceIndex}
                          sx={{
                            mb: 2,
                            bgcolor: 'background.paper',
                            borderRadius: 1,
                            '&:hover': {
                              bgcolor: 'action.hover',
                            },
                          }}
                        >
                          <ListItemIcon>{resource.icon}</ListItemIcon>
                          <ListItemText
                            primary={
                              <Box display="flex" alignItems="center" gap={1}>
                                {resource.title}
                                <Chip
                                  label={resource.type}
                                  size="small"
                                  color={
                                    resource.type === 'pdf'
                                      ? 'error'
                                      : resource.type === 'video'
                                      ? 'primary'
                                      : 'default'
                                  }
                                />
                              </Box>
                            }
                            secondary={resource.description}
                          />
                          <Button
                            variant="outlined"
                            size="small"
                            href={resource.link}
                            target={resource.type === 'link' ? '_blank' : '_self'}
                            rel={resource.type === 'link' ? 'noopener noreferrer' : ''}
                          >
                            {resource.type === 'link' ? 'Visit' : 'View'}
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
            These resources provide general information. For specific legal advice, consult with an immigration attorney.
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

export default ImmigrationResourcesPage;

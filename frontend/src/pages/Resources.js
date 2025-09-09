import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CardContent,
  CardActions
} from '@mui/material';
import DescriptionIcon from '@mui/icons-material/Description';
import { School as SchoolIcon } from '@mui/icons-material';
import GavelIcon from '@mui/icons-material/Gavel';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import { PageLayout, Section, Button, Card } from '../design-system';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import ArticleIcon from '@mui/icons-material/Article';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import { Link as LinkIcon } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const Resources = ({ type = 'standard' }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const resourceCategories = [
    {
      title: t('resources.categories.immigration.title'),
      description: t('resources.categories.immigration.description'),
      resources: [
        {
          title: t('resources.items.immigrationFormsGuide.title'),
          type: 'pdf',
          description: t('resources.items.immigrationFormsGuide.description'),
          link: '/resources/immigration/forms-guide.pdf',
          icon: <PictureAsPdfIcon />,
        },
        {
          title: t('resources.items.documentChecklist.title'),
          type: 'pdf',
          description: t('resources.items.documentChecklist.description'),
          link: '/resources/immigration/document-checklist.pdf',
          icon: <PictureAsPdfIcon />,
        },
        {
          title: t('resources.items.knowYourRights.title'),
          type: 'article',
          description: t('resources.items.knowYourRights.description'),
          link: '/rights/immigration',
          icon: <ArticleIcon />,
        },
      ],
    },
    {
      title: t('resources.categories.legalGuides.title'),
      description: t('resources.categories.legalGuides.description'),
      resources: [
        {
          title: t('resources.items.legalProcessOverview.title'),
          type: 'video',
          description: t('resources.items.legalProcessOverview.description'),
          link: '/resources/guides/legal-process.mp4',
          icon: <VideoLibraryIcon />,
        },
        {
          title: t('resources.items.documentTemplates.title'),
          type: 'template',
          description: t('resources.items.documentTemplates.description'),
          link: '/resources/templates',
          icon: <DescriptionIcon />,
        },
      ],
    },
    {
      title: t('resources.categories.external.title'),
      description: t('resources.categories.external.description'),
      resources: [
        {
          title: t('resources.items.uscisWebsite.title'),
          type: 'link',
          description: t('resources.items.uscisWebsite.description'),
          link: 'https://www.uscis.gov',
          icon: <LinkIcon />,
        },
        {
          title: t('resources.items.immigrationCourt.title'),
          type: 'link',
          description: t('resources.items.immigrationCourt.description'),
          link: 'https://www.justice.gov/eoir',
          icon: <LinkIcon />,
        },
      ],
    },
  ];

  const handleAccessDocuments = () => {
    navigate('/documents');
  };

  const handleLearnMoreRights = () => {
    navigate('/rights');
  };

  const handleResourceClick = (resource) => {
    if (resource.type === 'link' || resource.type === 'article') {
      // Navigate to internal pages
      navigate(resource.link);
    } else if (resource.type === 'pdf') {
      // Check if it's a document checklist
      if (resource.title.toLowerCase().includes('checklist')) {
        navigate('/resources/checklist/immigration');
      } else {
        // For other PDFs, show a message since we don't have actual PDFs
        alert(`PDF: ${resource.title}\n\nThis would open the PDF document: ${resource.link}\n\nIn a real implementation, this would download or display the PDF.`);
      }
    } else if (resource.type === 'video') {
      // For videos, show a message
      alert(`Video: ${resource.title}\n\nThis would play the video: ${resource.link}\n\nIn a real implementation, this would open a video player.`);
    } else if (resource.type === 'template') {
      // Navigate to templates page
      navigate('/services/contracts');
    } else {
      // Default action
      alert(`Opening: ${resource.title}\n\nLink: ${resource.link}`);
    }
  };

  const handleLearnMoreProcedures = () => {
    navigate('/procedures');
  };

  return (
    <PageLayout
      title={t('resources.title')}
      description={t('resources.subtitle')}
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            {t('resources.title')}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary" paragraph>
            {t('resources.description')}
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {resourceCategories.map((category, index) => (
            <Grid item xs={12} key={index}>
              <Card>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    {category.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {category.description}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <List>
                    {category.resources.map((resource, resourceIndex) => (
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
                          onClick={() => handleResourceClick(resource)}
                          sx={{
                            borderColor: '#1565C0',
                            color: '#1565C0',
                            '&:hover': {
                              borderColor: '#0D47A1',
                              backgroundColor: 'rgba(21, 101, 192, 0.04)',
                            },
                          }}
                        >
                          {resource.type === 'link' ? t('resources.buttons.visit') : t('resources.buttons.view')}
                        </Button>
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    color="primary"
                    onClick={() => {
                      if (category.title === 'Immigration Resources') {
                        navigate('/resources/immigration');
                      } else if (category.title === 'Legal Guides') {
                        navigate('/resources/guides');
                      } else if (category.title === 'External Resources') {
                        navigate('/resources/external');
                      }
                    }}
                  >
                    View All {category.title}
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </PageLayout>
  );
};

export default Resources;
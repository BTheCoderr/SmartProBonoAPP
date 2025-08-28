// WARNING: Imports have been commented out to fix linting errors.
// Uncomment specific imports as needed when using them.
import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Chip,
  Paper,
  InputAdornment,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CardActions
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import DescriptionIcon from '@mui/icons-material/Description';
import SchoolIcon from '@mui/icons-material/School';
import GavelIcon from '@mui/icons-material/Gavel';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import PageLayout from '../components/PageLayout';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import ArticleIcon from '@mui/icons-material/Article';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import LinkIcon from '@mui/icons-material/Link';

const resourceCategories = [
  {
    title: 'Immigration Resources',
    description: 'Essential documents and guides for immigration processes',
    resources: [
      {
        title: 'Immigration Forms Guide',
        type: 'pdf',
        description: 'Step-by-step guide for common immigration forms',
        link: '/resources/immigration/forms-guide.pdf',
        icon: <PictureAsPdfIcon />,
      },
      {
        title: 'Document Checklist',
        type: 'pdf',
        description: 'Comprehensive checklist of required documents',
        link: '/resources/immigration/document-checklist.pdf',
        icon: <PictureAsPdfIcon />,
      },
      {
        title: 'Know Your Rights',
        type: 'article',
        description: 'Understanding your rights during immigration proceedings',
        link: '/rights/immigration',
        icon: <ArticleIcon />,
      },
    ],
  },
  {
    title: 'Legal Guides',
    description: 'Comprehensive guides on various legal topics',
    resources: [
      {
        title: 'Legal Process Overview',
        type: 'video',
        description: 'Video guide explaining the legal process',
        link: '/resources/guides/legal-process.mp4',
        icon: <VideoLibraryIcon />,
      },
      {
        title: 'Document Templates',
        type: 'template',
        description: 'Common legal document templates',
        link: '/resources/templates',
        icon: <DescriptionIcon />,
      },
    ],
  },
  {
    title: 'External Resources',
    description: 'Helpful links to government and non-profit organizations',
    resources: [
      {
        title: 'USCIS Official Website',
        type: 'link',
        description: 'U.S. Citizenship and Immigration Services',
        link: 'https://www.uscis.gov',
        icon: <LinkIcon />,
      },
      {
        title: 'Immigration Court Information',
        type: 'link',
        description: 'Executive Office for Immigration Review',
        link: 'https://www.justice.gov/eoir',
        icon: <LinkIcon />,
      },
    ],
  },
];

const Resources = ({ type = 'standard' }) => {
  const navigate = useNavigate();

  const handleAccessDocuments = () => {
    navigate('/documents');
  };

  const handleLearnMoreRights = () => {
    navigate('/rights');
  };

  const handleLearnMoreProcedures = () => {
    navigate('/procedures');
  };

  return (
    <PageLayout
      title="Legal Resources"
      description="Access free legal resources, documents, and educational materials"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Legal Resources
          </Typography>
          <Typography variant="subtitle1" color="text.secondary" paragraph>
            Access our collection of legal resources, guides, and templates to help you understand and navigate your legal journey.
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
                <CardActions>
                  <Button size="small" color="primary">
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
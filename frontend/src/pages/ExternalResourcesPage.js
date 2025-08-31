import React from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider
} from '@mui/material';
import {
  LinkIcon,
  AccountBalanceIcon,
  SecurityIcon,
  SchoolIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import PageLayout from '../components/PageLayout';

const ExternalResourcesPage = () => {
  const navigate = useNavigate();

  const externalResources = [
    {
      title: 'USCIS Official Website',
      type: 'link',
      description: 'U.S. Citizenship and Immigration Services - Official government website for immigration information.',
      link: 'https://www.uscis.gov',
      icon: <AccountBalanceIcon />,
      category: 'Government'
    },
    {
      title: 'Immigration Court Information',
      type: 'link',
      description: 'Executive Office for Immigration Review - Information about immigration court proceedings.',
      link: 'https://www.justice.gov/eoir',
      icon: <AccountBalanceIcon />,
      category: 'Government'
    },
    {
      title: 'Legal Aid Society',
      type: 'link',
      description: 'Non-profit organization providing free legal services to low-income individuals.',
      link: 'https://www.legalaid.org',
      icon: <SecurityIcon />,
      category: 'Legal Aid'
    },
    {
      title: 'American Bar Association',
      type: 'link',
      description: 'Professional organization for lawyers with resources for finding legal help.',
      link: 'https://www.americanbar.org',
      icon: <SchoolIcon />,
      category: 'Professional'
    },
    {
      title: 'State Bar Associations',
      type: 'link',
      description: 'Find your state bar association for lawyer referrals and legal resources.',
      link: 'https://www.americanbar.org/directories/bar-associations/',
      icon: <AccountBalanceIcon />,
      category: 'Professional'
    },
    {
      title: 'Legal Services Corporation',
      type: 'link',
      description: 'Independent nonprofit that funds civil legal aid for low-income Americans.',
      link: 'https://www.lsc.gov',
      icon: <SecurityIcon />,
      category: 'Legal Aid'
    },
    {
      title: 'Court Locator',
      type: 'link',
      description: 'Find federal and state courts near you.',
      link: 'https://www.uscourts.gov/find-a-court',
      icon: <AccountBalanceIcon />,
      category: 'Government'
    },
    {
      title: 'LawHelp.org',
      type: 'link',
      description: 'Free legal information and resources for low-income individuals.',
      link: 'https://www.lawhelp.org',
      icon: <SchoolIcon />,
      category: 'Legal Aid'
    },
    {
      title: 'Pro Bono Net',
      type: 'link',
      description: 'Network of legal aid organizations providing free legal help.',
      link: 'https://www.probono.net',
      icon: <SecurityIcon />,
      category: 'Legal Aid'
    },
    {
      title: 'Federal Trade Commission',
      type: 'link',
      description: 'Consumer protection information and resources.',
      link: 'https://www.ftc.gov',
      icon: <AccountBalanceIcon />,
      category: 'Government'
    },
    {
      title: 'Equal Employment Opportunity Commission',
      type: 'link',
      description: 'Information about workplace discrimination and employment rights.',
      link: 'https://www.eeoc.gov',
      icon: <AccountBalanceIcon />,
      category: 'Government'
    },
    {
      title: 'National Consumer Law Center',
      type: 'link',
      description: 'Resources for consumer protection and debt-related legal issues.',
      link: 'https://www.nclc.org',
      icon: <SecurityIcon />,
      category: 'Consumer'
    }
  ];

  const categories = [...new Set(externalResources.map(resource => resource.category))];

  return (
    <PageLayout
      title="External Resources"
      description="Helpful links to government and non-profit organizations"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/resources')}
            sx={{ mb: 2 }}
          >
            Back to Resources
          </Button>
          <Typography variant="h4" component="h1" gutterBottom>
            External Resources
          </Typography>
          <Typography variant="subtitle1" color="text.secondary" paragraph>
            Helpful links to government agencies, non-profit organizations, and other legal resources that can provide additional assistance.
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
                    {externalResources
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
                                  label="External Link"
                                  size="small"
                                  color="primary"
                                />
                              </Box>
                            }
                            secondary={resource.description}
                          />
                          <Button
                            variant="outlined"
                            size="small"
                            href={resource.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            startIcon={<LinkIcon />}
                          >
                            Visit
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
            Disclaimer
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            These external resources are provided for informational purposes only. SmartProBono is not responsible for the content or availability of these external websites. Always verify information and consult with qualified professionals for legal advice.
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
      </Container>
    </PageLayout>
  );
};

export default ExternalResourcesPage;


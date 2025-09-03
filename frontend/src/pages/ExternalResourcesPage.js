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
  Link as LinkIcon,
  AccountBalance as AccountBalanceIcon,
  Security as SecurityIcon,
  School as SchoolIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { PageLayout, Section, Button, Card, CardContent, designTokens } from '../design-system';

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
      <Section>
        <Box sx={{ mb: 4 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/resources')}
            variant="outlined"
            sx={{
              mb: 3,
              color: designTokens.colors.primary[600],
              borderColor: designTokens.colors.primary[600],
              fontWeight: 600,
              '&:hover': {
                backgroundColor: designTokens.colors.primary[50],
                borderColor: designTokens.colors.primary[700],
                color: designTokens.colors.primary[700]
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
            External Resources
          </Typography>
          
          <Typography variant="body1" sx={{ 
            color: designTokens.colors.neutral[600],
            mb: 4,
            fontSize: '1.1rem',
            lineHeight: 1.6
          }}>
            Helpful links to government agencies, non-profit organizations, and other legal resources that can provide additional assistance.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {categories.map((category, categoryIndex) => (
            <Grid item xs={12} key={categoryIndex}>
              <Card
                sx={{
                  border: `1px solid ${designTokens.colors.neutral[200]}`,
                  borderRadius: designTokens.borderRadius.lg,
                  boxShadow: designTokens.shadows.sm,
                  '&:hover': {
                    boxShadow: designTokens.shadows.md,
                  }
                }}
              >
                <CardContent sx={{ p: designTokens.spacing[4] }}>
                  <Typography variant="h5" sx={{ 
                    fontWeight: designTokens.typography.fontWeight.semibold,
                    color: designTokens.colors.neutral[900],
                    mb: 2
                  }}>
                    {category}
                  </Typography>
                  <Divider sx={{ mb: 3, borderColor: designTokens.colors.neutral[200] }} />
                  <List>
                    {externalResources
                      .filter(resource => resource.category === category)
                      .map((resource, resourceIndex) => (
                        <ListItem
                          key={resourceIndex}
                          sx={{
                            mb: 2,
                            p: designTokens.spacing[3],
                            bgcolor: designTokens.colors.neutral[50],
                            borderRadius: designTokens.borderRadius.md,
                            border: `1px solid ${designTokens.colors.neutral[200]}`,
                            '&:hover': {
                              bgcolor: designTokens.colors.primary[50],
                              border: `1px solid ${designTokens.colors.primary[200]}`,
                              transform: 'translateY(-2px)',
                              boxShadow: designTokens.shadows.sm,
                            },
                            transition: 'all 0.2s ease'
                          }}
                        >
                          <ListItemIcon sx={{ color: designTokens.colors.primary[600] }}>
                            {resource.icon}
                          </ListItemIcon>
                          <ListItemText
                            primary={
                              <Box display="flex" alignItems="center" gap={1}>
                                <Typography sx={{ 
                                  fontWeight: designTokens.typography.fontWeight.medium,
                                  color: designTokens.colors.neutral[900]
                                }}>
                                  {resource.title}
                                </Typography>
                                <Chip
                                  label="External Link"
                                  size="small"
                                  sx={{
                                    backgroundColor: designTokens.colors.primary[100],
                                    color: designTokens.colors.primary[700],
                                    fontWeight: designTokens.typography.fontWeight.medium
                                  }}
                                />
                              </Box>
                            }
                            secondary={
                              <Typography sx={{ 
                                color: designTokens.colors.neutral[600],
                                mt: 0.5
                              }}>
                                {resource.description}
                              </Typography>
                            }
                          />
                          <Button
                            variant="outlined"
                            size="small"
                            href={resource.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            startIcon={<LinkIcon />}
                            sx={{
                              borderColor: designTokens.colors.primary[300],
                              color: designTokens.colors.primary[600],
                              '&:hover': {
                                borderColor: designTokens.colors.primary[500],
                                backgroundColor: designTokens.colors.primary[50],
                              }
                            }}
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

        <Box sx={{ 
          mt: 6, 
          p: 4, 
          backgroundColor: designTokens.colors.neutral[50],
          borderRadius: designTokens.borderRadius.lg,
          border: `1px solid ${designTokens.colors.neutral[200]}`,
          textAlign: 'center'
        }}>
          <Typography variant="h6" sx={{ 
            fontWeight: designTokens.typography.fontWeight.semibold,
            color: designTokens.colors.neutral[900],
            mb: 2
          }}>
            Disclaimer
          </Typography>
          <Typography variant="body2" sx={{ 
            color: designTokens.colors.neutral[600],
            mb: 3,
            lineHeight: 1.6
          }}>
            These external resources are provided for informational purposes only. SmartProBono is not responsible for the content or availability of these external websites. Always verify information and consult with qualified professionals for legal advice.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              onClick={() => navigate('/legal-chat')}
              sx={{
                backgroundColor: designTokens.colors.primary[600],
                color: designTokens.colors.neutral[50],
                '&:hover': {
                  backgroundColor: designTokens.colors.primary[700],
                }
              }}
            >
              Chat with AI Legal Assistant
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate('/contact')}
              sx={{
                borderColor: designTokens.colors.primary[300],
                color: designTokens.colors.primary[600],
                '&:hover': {
                  borderColor: designTokens.colors.primary[500],
                  backgroundColor: designTokens.colors.primary[50],
                }
              }}
            >
              Contact Support
            </Button>
          </Box>
        </Box>
      </Section>
    </PageLayout>
  );
};

export default ExternalResourcesPage;


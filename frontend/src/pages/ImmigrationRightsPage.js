import React from 'react';
import {
  Typography,
  Box,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import {
  Gavel as GavelIcon,
  Security as SecurityIcon,
  BusinessCenter as BusinessCenterIcon,
  Home as HomeIcon,
  HealthAndSafety as HealthAndSafetyIcon,
  AccountBalance as AccountBalanceIcon,
  ArrowBack as ArrowBackIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { PageLayout, Section, designTokens } from '../design-system';

const ImmigrationRightsPage = () => {
  const navigate = useNavigate();

  const immigrationRights = [
    {
      title: 'Right to Due Process',
      icon: <GavelIcon sx={{ fontSize: 40, color: '#1565C0' }} />,
      description: 'Fair treatment in immigration proceedings',
      rights: [
        'Right to legal representation',
        'Right to present evidence',
        'Right to appeal decisions',
        'Right to interpretation services'
      ],
      color: '#1565C0'
    },
    {
      title: 'Right to Non-Discrimination',
      icon: <SecurityIcon sx={{ fontSize: 40, color: '#14B8A6' }} />,
      description: 'Protection from discrimination based on national origin',
      rights: [
        'Equal treatment regardless of country of origin',
        'Protection from racial profiling',
        'Fair access to services',
        'Equal employment opportunities'
      ],
      color: '#14B8A6'
    },
    {
      title: 'Right to Family Unity',
      icon: <HomeIcon sx={{ fontSize: 40, color: '#1565C0' }} />,
      description: 'Protection of family relationships',
      rights: [
        'Right to petition for family members',
        'Protection from family separation',
        'Right to visit detained family',
        'Family-based immigration options'
      ],
      color: '#1565C0'
    },
    {
      title: 'Right to Work',
      icon: <BusinessCenterIcon sx={{ fontSize: 40, color: '#14B8A6' }} />,
      description: 'Employment rights for immigrants',
      rights: [
        'Right to work with proper authorization',
        'Protection from workplace discrimination',
        'Right to fair wages',
        'Protection from exploitation'
      ],
      color: '#14B8A6'
    },
    {
      title: 'Right to Education',
      icon: <AccountBalanceIcon sx={{ fontSize: 40, color: '#1565C0' }} />,
      description: 'Access to educational opportunities',
      rights: [
        'Right to public education (K-12)',
        'Access to higher education',
        'Equal treatment in schools',
        'Language assistance programs'
      ],
      color: '#1565C0'
    },
    {
      title: 'Right to Healthcare',
      icon: <HealthAndSafetyIcon sx={{ fontSize: 40, color: '#14B8A6' }} />,
      description: 'Access to healthcare services',
      rights: [
        'Emergency medical care',
        'Access to public health programs',
        'Protection of medical privacy',
        'Language interpretation in healthcare'
      ],
      color: '#14B8A6'
    }
  ];

  const handleBackClick = () => {
    navigate('/rights');
  };

  return (
    <PageLayout
      title="Immigration Rights"
      description="Know your rights as an immigrant in the United States"
    >
      <Section>
        <Box sx={{ mb: 4 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={handleBackClick}
            sx={{
              mb: 3,
              color: designTokens.colors.primary[600],
              '&:hover': {
                backgroundColor: designTokens.colors.primary[50]
              }
            }}
          >
            Back to All Rights
          </Button>
          
          <Typography variant="h4" sx={{ 
            fontWeight: designTokens.typography.fontWeight.bold,
            color: designTokens.colors.neutral[900],
            mb: 2
          }}>
            Immigration Rights
          </Typography>
          
          <Typography variant="body1" sx={{ 
            color: designTokens.colors.neutral[600],
            mb: 4,
            fontSize: '1.1rem',
            lineHeight: 1.6
          }}>
            Understanding your rights as an immigrant is crucial for protecting yourself and your family. 
            These rights are protected by the U.S. Constitution and federal laws, regardless of your immigration status.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {immigrationRights.map((right, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card
                sx={{
                  height: '100%',
                  transition: 'all 0.3s ease',
                  border: `2px solid transparent`,
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: designTokens.shadows.large,
                    border: `2px solid ${right.color}`,
                  }
                }}
              >
                <CardContent sx={{ p: designTokens.spacing[4] }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    {right.icon}
                    <Box sx={{ ml: 2 }}>
                      <Typography variant="h6" sx={{ 
                        fontWeight: designTokens.typography.fontWeight.semibold,
                        color: designTokens.colors.neutral[900]
                      }}>
                        {right.title}
                      </Typography>
                      <Typography variant="body2" sx={{ 
                        color: designTokens.colors.neutral[600],
                        mt: 0.5
                      }}>
                        {right.description}
                      </Typography>
                    </Box>
                  </Box>
                  
                  <Divider sx={{ my: 2 }} />
                  
                  <List dense>
                    {right.rights.map((rightItem, rightIndex) => (
                      <ListItem key={rightIndex} sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <CheckCircleIcon 
                            sx={{ 
                              fontSize: 20, 
                              color: right.color 
                            }} 
                          />
                        </ListItemIcon>
                        <ListItemText 
                          primary={rightItem}
                          sx={{
                            '& .MuiListItemText-primary': {
                              fontSize: '0.9rem',
                              color: designTokens.colors.neutral[700]
                            }
                          }}
                        />
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
          backgroundColor: designTokens.colors.primary[50],
          borderRadius: designTokens.borderRadius.lg,
          border: `1px solid ${designTokens.colors.primary[200]}`
        }}>
          <Typography variant="h6" sx={{ 
            fontWeight: designTokens.typography.fontWeight.semibold,
            color: designTokens.colors.primary[800],
            mb: 2
          }}>
            Important Reminders
          </Typography>
          <Typography variant="body2" sx={{ 
            color: designTokens.colors.primary[700],
            mb: 2
          }}>
            • You have the right to remain silent and not answer questions about your immigration status
          </Typography>
          <Typography variant="body2" sx={{ 
            color: designTokens.colors.primary[700],
            mb: 2
          }}>
            • You have the right to speak with an attorney before answering questions
          </Typography>
          <Typography variant="body2" sx={{ 
            color: designTokens.colors.primary[700],
            mb: 2
          }}>
            • You have the right to refuse consent to searches without a warrant
          </Typography>
          <Typography variant="body2" sx={{ 
            color: designTokens.colors.primary[700]
          }}>
            • If you are detained, you have the right to contact your consulate
          </Typography>
        </Box>
      </Section>
    </PageLayout>
  );
};

export default ImmigrationRightsPage;

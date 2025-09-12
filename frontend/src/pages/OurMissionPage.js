import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import {
  Gavel as GavelIcon,
  Public as PublicIcon,
  Security as SecurityIcon,
  School as SchoolIcon,
  CheckCircle as CheckCircleIcon,
  Star as StarIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';
import { PageLayout } from '../design-system';
import { useTranslation } from 'react-i18next';

const OurMissionPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const missionPoints = [
    {
      icon: <PublicIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: t('mission.points.universalAccess.title'),
      description: t('mission.points.universalAccess.description')
    },
    {
      icon: <GavelIcon sx={{ fontSize: 40, color: 'success.main' }} />,
      title: t('mission.points.technology.title'),
      description: t('mission.points.technology.description')
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 40, color: 'info.main' }} />,
      title: t('mission.points.community.title'),
      description: t('mission.points.community.description')
    },
    {
      icon: <SchoolIcon sx={{ fontSize: 40, color: 'warning.main' }} />,
      title: t('mission.points.education.title'),
      description: t('mission.points.education.description')
    }
  ];

  const values = [
    'Accessibility - Making legal help available to everyone',
    'Innovation - Using cutting-edge technology to improve legal services',
    'Integrity - Maintaining the highest ethical standards',
    'Empowerment - Giving people the tools to protect their rights',
    'Community - Building partnerships with legal professionals and organizations',
    'Transparency - Clear, honest communication with all stakeholders'
  ];

  const impactStats = [
    { number: '10,000+', label: 'Lives Impacted', icon: <StarIcon /> },
    { number: '500+', label: 'Legal Professionals', icon: <GavelIcon /> },
    { number: '50+', label: 'Cities Served', icon: <PublicIcon /> },
    { number: '95%', label: 'Success Rate', icon: <TrendingUpIcon /> }
  ];

  const goals = [
    {
      title: 'Short-term Goals (2024)',
      items: [
        'Expand AI capabilities to cover more legal areas',
        'Partner with 100+ legal aid organizations',
        'Launch mobile app for better accessibility',
        'Reach 50,000 users nationwide'
      ]
    },
    {
      title: 'Long-term Vision (2025-2030)',
      items: [
        'Become the leading platform for accessible legal assistance',
        'Develop AI that can handle complex legal research',
        'Expand internationally to serve global communities',
        'Create a comprehensive legal education platform'
      ]
    }
  ];

  return (
    <PageLayout
      title={t('mission.title')}
      description="Learn about our mission to make legal help accessible to everyone"
    >
      <Container maxWidth="lg">
        {/* Mission Statement */}
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
            {t('mission.title')}
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: '800px', mx: 'auto', mb: 4 }}>
            SmartProBono is dedicated to democratizing access to legal services by combining 
            artificial intelligence with human expertise to provide free, accessible, and 
            reliable legal assistance to everyone, regardless of their financial situation.
          </Typography>
        </Box>

        {/* Mission Points */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', textAlign: 'center', mb: 4 }}>
            What Drives Us
          </Typography>
          <Grid container spacing={4}>
            {missionPoints.map((point, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card sx={{ height: '100%', p: 3, textAlign: 'center', borderRadius: 2, boxShadow: 2 }}>
                  <CardContent>
                    <Box sx={{ mb: 2 }}>
                      {point.icon}
                    </Box>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                      {point.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {point.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Impact Statistics */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', textAlign: 'center', mb: 4 }}>
            Our Impact
          </Typography>
          <Grid container spacing={3}>
            {impactStats.map((stat, index) => (
              <Grid item xs={6} md={3} key={index}>
                <Paper sx={{ p: 3, textAlign: 'center', borderRadius: 2, boxShadow: 1 }}>
                  <Box sx={{ color: 'primary.main', mb: 1 }}>
                    {stat.icon}
                  </Box>
                  <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, color: '#0F3D5E' }}>
                    {stat.number}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {stat.label}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Values */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', textAlign: 'center', mb: 4 }}>
            Our Values
          </Typography>
          <Paper sx={{ p: 4, borderRadius: 2, boxShadow: 1 }}>
            <List>
              {values.map((value, index) => (
                <React.Fragment key={index}>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon>
                      <CheckCircleIcon sx={{ color: 'success.main' }} />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography variant="body1" sx={{ fontWeight: 500 }}>
                          {value}
                        </Typography>
                      }
                    />
                  </ListItem>
                  {index < values.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Box>

        {/* Goals */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', textAlign: 'center', mb: 4 }}>
            Our Goals
          </Typography>
          <Grid container spacing={4}>
            {goals.map((goal, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card sx={{ height: '100%', borderRadius: 2, boxShadow: 2 }}>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                      {goal.title}
                    </Typography>
                    <List dense>
                      {goal.items.map((item, itemIndex) => (
                        <ListItem key={itemIndex} sx={{ px: 0 }}>
                          <ListItemIcon>
                            <StarIcon sx={{ fontSize: 16, color: 'primary.main' }} />
                          </ListItemIcon>
                          <ListItemText
                            primary={
                              <Typography variant="body2">
                                {item}
                              </Typography>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Call to Action */}
        <Box sx={{ textAlign: 'center' }}>
          <Paper sx={{ p: 6, borderRadius: 2, boxShadow: 2, background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)', color: 'white' }}>
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
              Join Our Mission
            </Typography>
            <Typography variant="h6" paragraph sx={{ opacity: 0.9, maxWidth: '600px', mx: 'auto' }}>
              Whether you're seeking legal help or want to provide it, we're here to connect you 
              with the right resources and make justice accessible to all.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Chip
                label="Get Legal Help"
                clickable
                onClick={() => navigate('/get-legal-help')}
                sx={{ 
                  bgcolor: 'white', 
                  color: '#0F3D5E',
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' }
                }}
              />
              <Chip
                label="Become a Volunteer"
                clickable
                onClick={() => navigate('/volunteer')}
                sx={{ 
                  borderColor: 'white', 
                  color: 'white',
                  '&:hover': { borderColor: 'rgba(255,255,255,0.8)', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
              />
            </Box>
          </Paper>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default OurMissionPage;

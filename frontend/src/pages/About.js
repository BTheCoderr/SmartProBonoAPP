import React from 'react';
import { Container, Typography, Box, Grid, CardContent, Avatar, Chip } from '@mui/material';
import { 
  Gavel as GavelIcon, 
  People as PeopleIcon, 
  Public as PublicIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  Support as SupportIcon
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { PageLayout, Section, Button, Card as DesignCard } from '../design-system';

const About = () => {
  const { t } = useTranslation();
  
  const values = [
    {
      icon: <GavelIcon sx={{ fontSize: 40 }} />,
      title: t('about.values.justiceForAll.title'),
      description: t('about.values.justiceForAll.description')
    },
    {
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      title: t('about.values.communityFirst.title'),
      description: t('about.values.communityFirst.description')
    },
    {
      icon: <PublicIcon sx={{ fontSize: 40 }} />,
      title: t('about.values.accessibility.title'),
      description: t('about.values.accessibility.description')
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 40 }} />,
      title: t('about.values.innovation.title'),
      description: t('about.values.innovation.description')
    },
    {
      icon: <SpeedIcon sx={{ fontSize: 40 }} />,
      title: t('about.values.transparency.title'),
      description: t('about.values.transparency.description')
    },
    {
      icon: <SupportIcon sx={{ fontSize: 40 }} />,
      title: t('about.values.support.title'),
      description: t('about.values.support.description')
    }
  ];

  const stats = [
    { number: 'Growing', label: 'Community of Users' },
    { number: 'Expanding', label: 'Legal Professionals' },
    { number: 'Nationwide', label: 'Coverage' },
    { number: 'Dedicated', label: 'Support Team' }
  ];

  const features = [
    {
      title: 'AI-Powered Document Analysis',
      description: 'Our advanced AI technology analyzes legal documents, identifies key issues, and provides actionable insights to help you understand your legal situation.',
      icon: <GavelIcon sx={{ fontSize: 30, color: 'primary.main' }} />
    },
    {
      title: 'Smart Legal Chat',
      description: 'Get instant answers to your legal questions with our intelligent chat system that provides accurate, helpful guidance 24/7.',
      icon: <SupportIcon sx={{ fontSize: 30, color: 'success.main' }} />
    },
    {
      title: 'Document Generation',
      description: 'Create professional legal documents using our comprehensive library of templates, customized to your specific needs.',
      icon: <PublicIcon sx={{ fontSize: 30, color: 'info.main' }} />
    },
    {
      title: 'Secure & Private',
      description: 'Your data is protected with enterprise-grade security. All communications and documents are encrypted and confidential.',
      icon: <SecurityIcon sx={{ fontSize: 30, color: 'warning.main' }} />
    }
  ];

  const team = [
    {
      name: 'Legal Experts',
      role: 'Attorneys & Legal Professionals',
      description: 'Experienced lawyers specializing in various areas of law',
      avatar: <GavelIcon sx={{ fontSize: 40 }} />
    },
    {
      name: 'Technology Team',
      role: 'AI & Software Engineers',
      description: 'Building the future of legal technology with cutting-edge AI',
      avatar: <SpeedIcon sx={{ fontSize: 40 }} />
    },
    {
      name: 'Support Team',
      role: 'Customer Success',
      description: 'Dedicated to helping you succeed with our platform',
      avatar: <SupportIcon sx={{ fontSize: 40 }} />
    }
  ];

  return (
    <PageLayout
      title={t('pages.about.title')}
      description={t('pages.about.subtitle')}
    >
      {/* Hero Section */}
      <Section
        background="gradient"
        sx={{
          textAlign: 'center',
          py: 8,
          background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)',
          color: 'white'
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700, mb: 3 }}>
            {t('pages.about.hero.title')}
          </Typography>
          <Typography variant="h5" sx={{ mb: 4, opacity: 0.9 }}>
            {t('pages.about.hero.description')}
          </Typography>
          <Button
            variant="contained"
            size="large"
            sx={{
              bgcolor: 'white',
              color: 'primary.main',
              '&:hover': { bgcolor: 'grey.100' }
            }}
          >
            Get Started Today
          </Button>
        </Container>
      </Section>

      {/* Mission Section */}
      <Section sx={{ py: 8 }}>
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h3" component="h2" gutterBottom sx={{ fontWeight: 600 }}>
                Our Mission
              </Typography>
              <Typography variant="h6" color="text.secondary" paragraph>
                SmartProBono is dedicated to making legal services more accessible to those who need it most. 
                We leverage cutting-edge technology to connect clients with pro bono legal services and resources.
              </Typography>
              <Typography variant="body1" paragraph>
                Founded on the principle that justice should be accessible to everyone, we've built a platform 
                that breaks down traditional barriers to legal representation. Our AI-powered tools help match 
                clients with the right legal professionals, streamline case management, and provide educational 
                resources to empower individuals in their legal journey.
              </Typography>
              <Box sx={{ mt: 3 }}>
                <Chip label="Community Focused" color="primary" sx={{ mr: 1, mb: 1 }} />
                <Chip label="Technology Driven" color="secondary" sx={{ mr: 1, mb: 1 }} />
                <Chip label="Accessible Legal Help" color="success" />
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  height: 400,
                  background: 'linear-gradient(45deg, #f3f4f6 30%, #e5e7eb 90%)',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <Typography variant="h6" color="text.secondary">
                  Mission Visualization
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Section>

      {/* Values Section */}
      <Section sx={{ py: 8, bgcolor: 'grey.50' }}>
        <Container maxWidth="lg">
          <Box textAlign="center" mb={6}>
            <Typography variant="h3" component="h2" gutterBottom sx={{ fontWeight: 600 }}>
              Our Values
            </Typography>
            <Typography variant="h6" color="text.secondary">
              The principles that guide everything we do
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {values.map((value, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <DesignCard sx={{ height: '100%', textAlign: 'center' }}>
                  <CardContent sx={{ p: 4 }}>
                    <Avatar
                      sx={{
                        width: 80,
                        height: 80,
                        bgcolor: 'primary.main',
                        mx: 'auto',
                        mb: 3
                      }}
                    >
                      {value.icon}
                    </Avatar>
                    <Typography variant="h5" component="h3" gutterBottom sx={{ fontWeight: 600 }}>
                      {value.title}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                      {value.description}
                    </Typography>
                  </CardContent>
                </DesignCard>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Section>

      {/* Stats Section */}
      <Section sx={{ py: 8 }}>
        <Container maxWidth="lg">
          <Box textAlign="center" mb={6}>
            <Typography variant="h3" component="h2" gutterBottom sx={{ fontWeight: 600 }}>
              Our Impact
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Numbers that reflect our commitment to justice
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {stats.map((stat, index) => (
              <Grid item xs={6} md={3} key={index}>
                <Box textAlign="center">
                  <Typography variant="h2" component="div" sx={{ fontWeight: 700, color: 'primary.main' }}>
                    {stat.number}
                  </Typography>
                  <Typography variant="h6" color="text.secondary">
                    {stat.label}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Section>

      {/* Features Section */}
      <Section sx={{ py: 8, bgcolor: 'grey.50' }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography variant="h3" component="h2" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
              Our Technology
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ maxWidth: '600px', mx: 'auto' }}>
              We leverage cutting-edge AI technology to make legal assistance more accessible, efficient, and effective.
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} md={6} key={index}>
                <DesignCard sx={{ height: '100%', p: 3, textAlign: 'center' }}>
                  <CardContent>
                    <Box sx={{ mb: 2 }}>
                      {feature.icon}
                    </Box>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </DesignCard>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Section>

      {/* Team Section */}
      <Section sx={{ py: 8 }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography variant="h3" component="h2" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
              Our Team
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ maxWidth: '600px', mx: 'auto' }}>
              Meet the dedicated professionals who make SmartProBono possible.
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {team.map((member, index) => (
              <Grid item xs={12} md={4} key={index}>
                <DesignCard sx={{ height: '100%', p: 3, textAlign: 'center' }}>
                  <CardContent>
                    <Avatar sx={{ width: 80, height: 80, mx: 'auto', mb: 2, bgcolor: 'primary.main' }}>
                      {member.avatar}
                    </Avatar>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                      {member.name}
                    </Typography>
                    <Typography variant="subtitle1" color="primary" gutterBottom>
                      {member.role}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {member.description}
                    </Typography>
                  </CardContent>
                </DesignCard>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Section>

      {/* CTA Section */}
      <Section
        background="gradient"
        sx={{
          py: 8,
          textAlign: 'center',
          background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)',
          color: 'white'
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h3" component="h2" gutterBottom sx={{ fontWeight: 600 }}>
            Join Our Mission
          </Typography>
          <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
            Whether you're seeking legal help or want to provide it, we're here to connect you with the right resources.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              size="large"
              sx={{
                bgcolor: 'white',
                color: 'primary.main',
                '&:hover': { bgcolor: 'grey.100' }
              }}
            >
              Get Legal Help
            </Button>
            <Button
              variant="outlined"
              size="large"
              sx={{
                borderColor: 'white',
                color: 'white',
                '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
              }}
            >
              Become a Volunteer
            </Button>
          </Box>
        </Container>
      </Section>
    </PageLayout>
  );
};

export default About; 
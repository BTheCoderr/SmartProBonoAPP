import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Button,
  Chip,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Article as ArticleIcon,
  VideoLibrary as VideoIcon,
  Radio as RadioIcon,
  Newspaper as NewspaperIcon,
  CalendarToday as CalendarIcon,
  Link as LinkIcon,
  Download as DownloadIcon,
  Email as EmailIcon
} from '@mui/icons-material';
import { PageLayout } from '../design-system';
import { useTranslation } from 'react-i18next';

const PressPage = () => {
  const { t } = useTranslation();
  const pressReleases = [
    {
      title: 'SmartProBono Launches AI-Powered Legal Assistant Platform',
      date: '2024-01-15',
      summary: 'Revolutionary platform combines artificial intelligence with legal expertise to make legal assistance accessible to everyone.',
      category: 'Product Launch',
      featured: true
    },
    {
      title: 'Partnership with National Legal Aid Organizations Announced',
      date: '2024-01-10',
      summary: 'SmartProBono partners with leading legal aid organizations to expand access to free legal services nationwide.',
      category: 'Partnership',
      featured: false
    },
    {
      title: 'SmartProBono Receives $2M Grant for Legal Technology Innovation',
      date: '2024-01-05',
      summary: 'Grant funding will support development of advanced AI features and expansion of services to underserved communities.',
      category: 'Funding',
      featured: false
    }
  ];

  const mediaCoverage = [
    {
      title: 'AI Revolutionizes Legal Aid: SmartProBono Makes Justice Accessible',
      outlet: 'Legal Tech Today',
      date: '2024-01-20',
      type: 'Article',
      url: '#',
      icon: <NewspaperIcon />
    },
    {
      title: 'TechCrunch: SmartProBono Raises Series A Funding',
      outlet: 'TechCrunch',
      date: '2024-01-18',
      type: 'Article',
      url: '#',
      icon: <ArticleIcon />
    },
    {
      title: 'NPR Interview: The Future of Legal Technology',
      outlet: 'NPR',
      date: '2024-01-15',
      type: 'Radio',
      url: '#',
      icon: <RadioIcon />
    },
    {
      title: 'YouTube: SmartProBono Demo and Founder Interview',
      outlet: 'Legal Innovation Channel',
      date: '2024-01-12',
      type: 'Video',
      url: '#',
      icon: <VideoIcon />
    }
  ];

  const awards = [
    {
      title: 'Best Legal Technology Innovation 2024',
      organization: 'Legal Innovation Awards',
      date: '2024-01-25',
      description: 'Recognized for outstanding innovation in making legal services more accessible through technology.'
    },
    {
      title: 'Social Impact Technology Award',
      organization: 'Tech for Good Foundation',
      date: '2024-01-20',
      description: 'Honored for using technology to address social justice and legal access challenges.'
    },
    {
      title: 'Startup of the Year - Legal Tech',
      organization: 'Legal Tech Association',
      date: '2024-01-15',
      description: 'Awarded for exceptional growth and impact in the legal technology sector.'
    }
  ];

  return (
    <PageLayout
      title={t('press.title')}
      description={t('press.subtitle')}
    >
      <Container maxWidth="lg">
        {/* Press Kit Section */}
        <Box sx={{ mb: 6 }}>
          <Paper sx={{ p: 4, borderRadius: 2, boxShadow: 2, background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)', color: 'white' }}>
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
              Press Kit
            </Typography>
            <Typography variant="h6" paragraph sx={{ opacity: 0.9 }}>
              Download our press kit for logos, images, and company information.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                startIcon={<DownloadIcon />}
                sx={{ 
                  bgcolor: 'white', 
                  color: '#0F3D5E',
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' }
                }}
              >
                Download Press Kit
              </Button>
              <Button
                variant="outlined"
                startIcon={<EmailIcon />}
                sx={{ 
                  borderColor: 'white', 
                  color: 'white',
                  '&:hover': { borderColor: 'rgba(255,255,255,0.8)', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
              >
                Contact Press Team
              </Button>
            </Box>
          </Paper>
        </Box>

        {/* Press Releases */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', mb: 4 }}>
            {t('press.sections.pressReleases')}
          </Typography>
          <Grid container spacing={3}>
            {pressReleases.map((release, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card sx={{ height: '100%', borderRadius: 2, boxShadow: 2, border: release.featured ? '2px solid #0F3D5E' : 'none' }}>
                  <CardContent sx={{ p: 3 }}>
                    {release.featured && (
                      <Chip 
                        label="Featured" 
                        color="primary" 
                        size="small" 
                        sx={{ mb: 2 }}
                      />
                    )}
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                      {release.title}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <CalendarIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                      <Typography variant="body2" color="text.secondary">
                        {new Date(release.date).toLocaleDateString()}
                      </Typography>
                      <Chip 
                        label={release.category} 
                        size="small" 
                        variant="outlined"
                        sx={{ ml: 2 }}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {release.summary}
                    </Typography>
                    <Button
                      size="small"
                      startIcon={<LinkIcon />}
                      sx={{ textTransform: 'none' }}
                    >
                      {t('press.buttons.readMore')}
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Media Coverage */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', mb: 4 }}>
            Media Coverage
          </Typography>
          <Grid container spacing={3}>
            {mediaCoverage.map((item, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card sx={{ height: '100%', borderRadius: 2, boxShadow: 1 }}>
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Box sx={{ color: 'primary.main', mr: 1 }}>
                        {item.icon}
                      </Box>
                      <Typography variant="subtitle2" color="primary">
                        {item.type}
                      </Typography>
                    </Box>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                      {item.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {item.outlet}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <CalendarIcon sx={{ fontSize: 14, mr: 1, color: 'text.secondary' }} />
                      <Typography variant="caption" color="text.secondary">
                        {new Date(item.date).toLocaleDateString()}
                      </Typography>
                    </Box>
                    <Button
                      size="small"
                      startIcon={<LinkIcon />}
                      sx={{ textTransform: 'none' }}
                    >
                      View Article
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Awards & Recognition */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', mb: 4 }}>
            Awards & Recognition
          </Typography>
          <List>
            {awards.map((award, index) => (
              <React.Fragment key={index}>
                <ListItem sx={{ px: 0 }}>
                  <ListItemIcon>
                    <Box sx={{ 
                      width: 40, 
                      height: 40, 
                      borderRadius: '50%', 
                      bgcolor: 'primary.main', 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center',
                      color: 'white'
                    }}>
                      🏆
                    </Box>
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Typography variant="h6" sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                        {award.title}
                      </Typography>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="primary" gutterBottom>
                          {award.organization}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {award.description}
        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(award.date).toLocaleDateString()}
        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                {index < awards.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Box>

        {/* Contact Information */}
        <Box sx={{ textAlign: 'center' }}>
          <Paper sx={{ p: 4, borderRadius: 2, boxShadow: 1 }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
              Press Contact
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              For media inquiries, interviews, or press kit requests, please contact our press team.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                startIcon={<EmailIcon />}
                sx={{ borderRadius: 2 }}
              >
                press@smartprobono.org
              </Button>
              <Button
                variant="outlined"
                startIcon={<LinkIcon />}
                sx={{ borderRadius: 2 }}
              >
                Media Resources
              </Button>
            </Box>
          </Paper>
      </Box>
    </Container>
  </PageLayout>
);
};

export default PressPage;

import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Avatar, 
  Chip,
  Paper
} from '@mui/material';
import {
  Gavel as GavelIcon,
  Code as CodeIcon,
  Support as SupportIcon,
  Security as SecurityIcon,
  School as SchoolIcon,
  Public as PublicIcon,
  Star as StarIcon,
  LinkedIn as LinkedInIcon,
  Twitter as TwitterIcon
} from '@mui/icons-material';
import { PageLayout } from '../design-system';
import { useTranslation } from 'react-i18next';

const TeamPage = () => {
  const { t } = useTranslation();
  const teamMembers = [
    {
      name: 'Sarah Johnson',
      role: 'Chief Legal Officer',
      department: 'Legal',
      bio: 'Former public defender with 15+ years of experience in criminal and civil law. Passionate about making legal services accessible to underserved communities.',
      avatar: 'https://via.placeholder.com/150x150/0F3D5E/FFFFFF?text=SJ',
      expertise: ['Criminal Law', 'Civil Rights', 'Public Defense'],
      education: 'JD, Harvard Law School',
      icon: <GavelIcon sx={{ fontSize: 30 }} />
    },
    {
      name: 'Michael Chen',
      role: 'Chief Technology Officer',
      department: 'Engineering',
      bio: 'AI and machine learning expert with a background in legal technology. Leads our technical innovation and AI development initiatives.',
      avatar: 'https://via.placeholder.com/150x150/1FB6A6/FFFFFF?text=MC',
      expertise: ['Artificial Intelligence', 'Machine Learning', 'Legal Tech'],
      education: 'MS Computer Science, Stanford University',
      icon: <CodeIcon sx={{ fontSize: 30 }} />
    },
    {
      name: 'Dr. Maria Rodriguez',
      role: 'Head of User Experience',
      department: 'Product',
      bio: 'UX researcher and designer focused on making complex legal processes intuitive and accessible. Previously worked at major tech companies.',
      avatar: 'https://via.placeholder.com/150x150/FF6B6B/FFFFFF?text=MR',
      expertise: ['User Experience', 'Product Design', 'Accessibility'],
      education: 'PhD Human-Computer Interaction, MIT',
      icon: <SupportIcon sx={{ fontSize: 30 }} />
    },
    {
      name: 'David Kim',
      role: 'Chief Security Officer',
      department: 'Security',
      bio: 'Cybersecurity expert specializing in data protection and privacy law. Ensures our platform meets the highest security standards.',
      avatar: 'https://via.placeholder.com/150x150/4ECDC4/FFFFFF?text=DK',
      expertise: ['Cybersecurity', 'Data Privacy', 'Compliance'],
      education: 'MS Information Security, Carnegie Mellon',
      icon: <SecurityIcon sx={{ fontSize: 30 }} />
    },
    {
      name: 'Jennifer Walsh',
      role: 'Head of Legal Education',
      department: 'Education',
      bio: 'Legal educator and former law professor. Develops our educational content and training programs for both users and legal professionals.',
      avatar: 'https://via.placeholder.com/150x150/45B7D1/FFFFFF?text=JW',
      expertise: ['Legal Education', 'Curriculum Development', 'Training'],
      education: 'JD, Yale Law School',
      icon: <SchoolIcon sx={{ fontSize: 30 }} />
    },
    {
      name: 'Alex Thompson',
      role: 'Community Outreach Director',
      department: 'Community',
      bio: 'Community organizer and advocate for legal access. Builds partnerships with legal aid organizations and community groups.',
      avatar: 'https://via.placeholder.com/150x150/96CEB4/FFFFFF?text=AT',
      expertise: ['Community Outreach', 'Partnerships', 'Advocacy'],
      education: 'MPA, Georgetown University',
      icon: <PublicIcon sx={{ fontSize: 30 }} />
    }
  ];

  const departments = [
    {
      name: 'Legal Team',
      description: 'Experienced attorneys and legal professionals who ensure our platform provides accurate, reliable legal guidance.',
      count: '12+ members',
      color: 'primary'
    },
    {
      name: 'Engineering Team',
      description: 'AI researchers, software engineers, and data scientists building the technology that powers our platform.',
      count: '25+ members',
      color: 'success'
    },
    {
      name: 'Product Team',
      description: 'Designers, researchers, and product managers focused on creating the best possible user experience.',
      count: '8+ members',
      color: 'info'
    },
    {
      name: 'Community Team',
      description: 'Outreach specialists and community managers who connect us with users and legal professionals.',
      count: '6+ members',
      color: 'warning'
    }
  ];

  return (
    <PageLayout
      title={t('team.title')}
      description={t('team.subtitle')}
    >
      <Container maxWidth="lg">
        {/* Team Introduction */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
            {t('team.title')}
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: '800px', mx: 'auto', mb: 4 }}>
            We're a diverse group of legal professionals, technologists, and advocates united by a common mission: 
            making legal assistance accessible to everyone, regardless of their financial situation.
          </Typography>
        </Box>

        {/* Leadership Team */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', textAlign: 'center', mb: 4 }}>
            Leadership Team
          </Typography>
          <Grid container spacing={4}>
            {teamMembers.map((member, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <Card sx={{ height: '100%', borderRadius: 2, boxShadow: 2, transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-4px)' } }}>
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ textAlign: 'center', mb: 3 }}>
                      <Avatar
                        src={member.avatar}
                        alt={member.name}
                        sx={{ width: 100, height: 100, mx: 'auto', mb: 2 }}
                      />
                      <Typography variant="h6" sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                        {member.name}
                      </Typography>
                      <Typography variant="subtitle1" color="primary" gutterBottom>
                        {member.role}
                      </Typography>
                      <Chip 
                        label={member.department} 
                        size="small" 
                        color={member.color}
                        variant="outlined"
                      />
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {member.bio}
                    </Typography>
                    
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                        Expertise:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {member.expertise.map((skill, skillIndex) => (
                          <Chip key={skillIndex} label={skill} size="small" variant="outlined" />
                        ))}
                      </Box>
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                      {member.education}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Departments */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', textAlign: 'center', mb: 4 }}>
            Our Departments
          </Typography>
          <Grid container spacing={3}>
            {departments.map((dept, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Paper sx={{ p: 3, textAlign: 'center', height: '100%', borderRadius: 2, boxShadow: 1 }}>
                  <Box sx={{ mb: 2 }}>
                    <StarIcon sx={{ fontSize: 40, color: `${dept.color}.main` }} />
                  </Box>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                    {dept.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {dept.description}
                  </Typography>
                  <Chip 
                    label={dept.count} 
                    size="small" 
                    color={dept.color}
                    variant="filled"
                  />
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Join Our Team */}
        <Box sx={{ textAlign: 'center', mt: 8 }}>
          <Paper sx={{ p: 6, borderRadius: 2, boxShadow: 2, background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)', color: 'white' }}>
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
              Join Our Mission
            </Typography>
            <Typography variant="h6" paragraph sx={{ opacity: 0.9, maxWidth: '600px', mx: 'auto' }}>
              We're always looking for passionate individuals who want to make a difference in the legal world. 
              Help us build the future of accessible legal assistance.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Chip
                icon={<LinkedInIcon />}
                label="View Open Positions"
                clickable
                sx={{ 
                  bgcolor: 'white', 
                  color: '#0F3D5E',
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' }
                }}
              />
              <Chip
                icon={<TwitterIcon />}
                label="Follow Our Updates"
                clickable
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

export default TeamPage;

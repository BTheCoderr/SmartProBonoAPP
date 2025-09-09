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
  Avatar,
  Paper
} from '@mui/material';
import { 
  Business as BusinessIcon,
  Handshake as HandshakeIcon,
  Star as StarIcon,
  Email as EmailIcon,
  Language as LanguageIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  Support as SupportIcon
} from '@mui/icons-material';
import { PageLayout } from '../design-system';

const PartnersPage = () => {
  const partnerCategories = [
    {
      title: "Legal Technology Partners",
      description: "Leading legal tech companies that enhance our platform capabilities",
      partners: [
        {
          name: "LegalTech Solutions",
          description: "AI-powered legal research and case law analysis",
          logo: "https://via.placeholder.com/120x60/0F3D5E/FFFFFF?text=LegalTech",
          category: "Technology",
          rating: 4.9
        },
        {
          name: "DocuFlow Systems",
          description: "Document management and workflow automation",
          logo: "https://via.placeholder.com/120x60/1FB6A6/FFFFFF?text=DocuFlow",
          category: "Document Management",
          rating: 4.8
        },
        {
          name: "SecureLegal",
          description: "Enterprise-grade security and compliance solutions",
          logo: "https://via.placeholder.com/120x60/FF6B6B/FFFFFF?text=SecureLegal",
          category: "Security",
          rating: 5.0
        }
      ]
    },
    {
      title: "Legal Service Providers",
      description: "Law firms and legal professionals who trust our platform",
      partners: [
        {
          name: "Pro Bono Legal Group",
          description: "Nationwide network of pro bono attorneys",
          logo: "https://via.placeholder.com/120x60/4ECDC4/FFFFFF?text=ProBono",
          category: "Legal Services",
          rating: 4.9
        },
        {
          name: "Community Legal Aid",
          description: "Free legal assistance for underserved communities",
          logo: "https://via.placeholder.com/120x60/45B7D1/FFFFFF?text=Community",
          category: "Legal Aid",
          rating: 4.7
        },
        {
          name: "Immigration Law Associates",
          description: "Specialized immigration legal services",
          logo: "https://via.placeholder.com/120x60/96CEB4/FFFFFF?text=Immigration",
          category: "Immigration Law",
          rating: 4.8
        }
      ]
    },
    {
      title: "Technology Partners",
      description: "Technology companies that power our infrastructure",
      partners: [
        {
          name: "CloudSecure",
          description: "Secure cloud infrastructure and data storage",
          logo: "https://via.placeholder.com/120x60/FFEAA7/333333?text=CloudSecure",
          category: "Cloud Services",
          rating: 4.9
        },
        {
          name: "AI Solutions Inc",
          description: "Advanced AI and machine learning capabilities",
          logo: "https://via.placeholder.com/120x60/DDA0DD/FFFFFF?text=AI+Solutions",
          category: "Artificial Intelligence",
          rating: 4.8
        }
      ]
    }
  ];

  const benefits = [
    {
      icon: <SecurityIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: "Enhanced Security",
      description: "Enterprise-grade security measures protect all data and communications"
    },
    {
      icon: <SpeedIcon sx={{ fontSize: 40, color: 'success.main' }} />,
      title: "Faster Processing",
      description: "Optimized infrastructure ensures quick document processing and analysis"
    },
    {
      icon: <SupportIcon sx={{ fontSize: 40, color: 'info.main' }} />,
      title: "24/7 Support",
      description: "Round-the-clock technical support from our partner network"
    },
    {
      icon: <LanguageIcon sx={{ fontSize: 40, color: 'warning.main' }} />,
      title: "Global Reach",
      description: "International partners enable worldwide legal assistance"
    }
  ];

  return (
    <PageLayout
      title="Partners"
      description="Our partners who help us make legal assistance accessible"
    >
      <Container maxWidth="lg">
        {/* Partnership Benefits */}
        <Box sx={{ mb: 6 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E', textAlign: 'center', mb: 4 }}>
            Why Partner With Us?
          </Typography>
          <Grid container spacing={3}>
            {benefits.map((benefit, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card sx={{ textAlign: 'center', p: 3, height: '100%', borderRadius: 2, boxShadow: 2 }}>
                  <CardContent>
                    <Box sx={{ mb: 2 }}>
                      {benefit.icon}
                    </Box>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                      {benefit.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {benefit.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Partner Categories */}
        {partnerCategories.map((category, categoryIndex) => (
          <Box key={categoryIndex} sx={{ mb: 6 }}>
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                {category.title}
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ maxWidth: '600px', mx: 'auto' }}>
                {category.description}
              </Typography>
            </Box>

            <Grid container spacing={3}>
              {category.partners.map((partner, partnerIndex) => (
                <Grid item xs={12} md={6} lg={4} key={partnerIndex}>
                  <Card sx={{ height: '100%', borderRadius: 2, boxShadow: 2, transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-4px)' } }}>
                    <CardContent sx={{ p: 3 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Avatar
                          src={partner.logo}
                          alt={partner.name}
                          sx={{ width: 60, height: 60, mr: 2 }}
                        >
                          <BusinessIcon sx={{ fontSize: 30 }} />
                        </Avatar>
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="h6" sx={{ fontWeight: 600, color: '#0F3D5E' }}>
                            {partner.name}
                          </Typography>
                          <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                            <StarIcon sx={{ fontSize: 16, color: 'warning.main', mr: 0.5 }} />
                            <Typography variant="body2" color="text.secondary">
                              {partner.rating}/5.0
                            </Typography>
                          </Box>
                        </Box>
                      </Box>
                      
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {partner.description}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                        <Chip 
                          label={partner.category} 
                          size="small" 
                          color="primary" 
                          variant="outlined"
                        />
                        <Button 
                          size="small" 
                          startIcon={<EmailIcon />}
                          sx={{ textTransform: 'none' }}
                        >
                          Contact
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        ))}

        {/* Become a Partner Section */}
        <Box sx={{ mt: 8, mb: 4 }}>
          <Paper sx={{ p: 6, textAlign: 'center', borderRadius: 2, boxShadow: 2, background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)', color: 'white' }}>
            <HandshakeIcon sx={{ fontSize: 60, mb: 2 }} />
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
              Become a Partner
            </Typography>
            <Typography variant="h6" paragraph sx={{ opacity: 0.9, maxWidth: '600px', mx: 'auto' }}>
              Join our network of partners and help us make legal assistance more accessible to everyone.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap', mt: 3 }}>
              <Button
                variant="contained"
                size="large"
                startIcon={<EmailIcon />}
                sx={{ 
                  bgcolor: 'white', 
                  color: '#0F3D5E',
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' },
                  borderRadius: 2
                }}
              >
                Partner With Us
              </Button>
              <Button
                variant="outlined"
                size="large"
                sx={{ 
                  borderColor: 'white', 
                  color: 'white',
                  '&:hover': { borderColor: 'rgba(255,255,255,0.8)', bgcolor: 'rgba(255,255,255,0.1)' },
                  borderRadius: 2
                }}
              >
                Learn More
              </Button>
            </Box>
          </Paper>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default PartnersPage;

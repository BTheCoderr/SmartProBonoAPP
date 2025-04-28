import React from 'react';
import { Box, Card, Typography, Grid, Avatar, Rating, Chip } from '@mui/material';
import { styled } from '@mui/material/styles';
import GavelIcon from '@mui/icons-material/Gavel';
import SecurityIcon from '@mui/icons-material/Security';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import GroupsIcon from '@mui/icons-material/Groups';

const StyledBadge = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  textAlign: 'center',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[1],
  transition: 'transform 0.2s',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[3],
  },
}));

const testimonials = [
  {
    id: 1,
    name: "Sarah Johnson",
    role: "Pro Bono Attorney",
    avatar: "/avatars/sarah.jpg",
    rating: 5,
    text: "SmartProBono has revolutionized how we handle pro bono cases. The AI assistance helps us serve more clients efficiently.",
  },
  {
    id: 2,
    name: "Michael Chen",
    role: "Legal Aid Director",
    avatar: "/avatars/michael.jpg",
    rating: 5,
    text: "This platform has been instrumental in expanding our reach to underserved communities.",
  },
  {
    id: 3,
    name: "Lisa Rodriguez",
    role: "Community Legal Worker",
    avatar: "/avatars/lisa.jpg",
    rating: 5,
    text: "The document automation features save us countless hours, allowing us to focus on helping more people.",
  },
];

const certifications = [
  { label: 'HIPAA Compliant', icon: <SecurityIcon /> },
  { label: 'ABA Approved', icon: <GavelIcon /> },
  { label: 'SSL Secured', icon: <VerifiedUserIcon /> },
  { label: '10,000+ Users', icon: <GroupsIcon /> },
];

const TrustSignals = () => {
  return (
    <Box sx={{ py: 4 }}>
      {/* Trust Badges */}
      <Grid container spacing={3} sx={{ mb: 6 }}>
        <Grid item xs={12}>
          <Typography variant="h4" align="center" gutterBottom>
            Trusted by Legal Professionals
          </Typography>
        </Grid>
        {certifications.map((cert, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <StyledBadge>
              {cert.icon}
              <Typography variant="h6" sx={{ mt: 1 }}>
                {cert.label}
              </Typography>
            </StyledBadge>
          </Grid>
        ))}
      </Grid>

      {/* Testimonials */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" align="center" gutterBottom>
          What Legal Professionals Say
        </Typography>
        <Grid container spacing={3}>
          {testimonials.map((testimonial) => (
            <Grid item xs={12} md={4} key={testimonial.id}>
              <Card sx={{ p: 3, height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar
                    src={testimonial.avatar}
                    alt={testimonial.name}
                    sx={{ width: 56, height: 56, mr: 2 }}
                  />
                  <Box>
                    <Typography variant="h6">{testimonial.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {testimonial.role}
                    </Typography>
                  </Box>
                </Box>
                <Rating value={testimonial.rating} readOnly sx={{ mb: 2 }} />
                <Typography variant="body1" sx={{ flex: 1 }}>
                  "{testimonial.text}"
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Statistics */}
      <Box sx={{ textAlign: 'center', mt: 6 }}>
        <Typography variant="h4" gutterBottom>
          Making Legal Aid Accessible
        </Typography>
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h3" color="primary">10K+</Typography>
            <Typography variant="h6">Users Helped</Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h3" color="primary">50+</Typography>
            <Typography variant="h6">Legal Aid Organizations</Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h3" color="primary">95%</Typography>
            <Typography variant="h6">Satisfaction Rate</Typography>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default TrustSignals; 
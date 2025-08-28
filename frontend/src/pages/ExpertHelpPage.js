import React, { useState } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Paper, 
  Grid, 
  Avatar,
  Button,
  TextField,
  Card,
  CardContent,
  CardActions,
  Divider,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Tab,
  Tabs,
  CircularProgress
} from '@mui/material';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import BusinessIcon from '@mui/icons-material/Business';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import { useNavigate } from 'react-router-dom';

// Mock icon components
const SecurityIcon = () => <Box component="span" sx={{ display: 'inline-block', width: 24, height: 24 }}></Box>;
const TrendingUpIcon = () => <Box component="span" sx={{ display: 'inline-block', width: 24, height: 24 }}></Box>;
const AccountBalanceIcon = () => <Box component="span" sx={{ display: 'inline-block', width: 24, height: 24 }}></Box>;
const StarHalfIcon = () => <Box component="span" sx={{ display: 'inline-block', width: 24, height: 24 }}></Box>;

// Mock data for startup legal experts
const attorneys = [
  {
    id: 1,
    name: "Alexandra Chen",
    avatar: "AC",
    specialties: ["GDPR Compliance", "Data Privacy", "EU Regulations"],
    rating: 4.9,
    reviewCount: 127,
    location: "Palo Alto, CA",
    availability: "24-48 hours",
    bio: "GDPR compliance expert with 8+ years helping startups navigate European data protection regulations and avoid costly fines.",
    languages: ["English", "Mandarin"],
    hourlyRate: "$350-450",
    successRate: "98%"
  },
  {
    id: 2,
    name: "David Rodriguez",
    avatar: "DR",
    specialties: ["SOC 2 Compliance", "Security Frameworks", "Enterprise Sales"],
    rating: 4.8,
    reviewCount: 93,
    location: "Austin, TX",
    availability: "Same day",
    bio: "SOC 2 specialist who has helped 200+ startups achieve enterprise-grade security compliance for major client deals.",
    languages: ["English", "Spanish"],
    hourlyRate: "$400-500",
    successRate: "95%"
  },
  {
    id: 3,
    name: "Sarah Goldman",
    avatar: "SG",
    specialties: ["Fundraising", "Term Sheets", "Corporate Law"],
    rating: 5.0,
    reviewCount: 156,
    location: "New York, NY",
    availability: "1-2 hours",
    bio: "Venture-backed startup attorney with $2B+ in funding closed. Expert in Series A-C rounds and complex deal structures.",
    languages: ["English"],
    hourlyRate: "$500-650",
    successRate: "100%"
  },
  {
    id: 4,
    name: "Michael Kim",
    avatar: "MK",
    specialties: ["IP Strategy", "Patent Filing", "Trademark Protection"],
    rating: 4.7,
    reviewCount: 81,
    location: "San Francisco, CA",
    availability: "2-3 days",
    bio: "Intellectual property strategist specializing in tech startups, with 500+ patents filed and $50M+ in IP value created.",
    languages: ["English", "Korean"],
    hourlyRate: "$300-400",
    successRate: "92%"
  }
];

// Startup-focused legal topics
const legalTopics = [
  { id: 1, name: "GDPR Compliance", icon: <SecurityIcon /> },
  { id: 2, name: "SOC 2 Certification", icon: <VerifiedUserIcon /> },
  { id: 3, name: "Fundraising & VCs", icon: <TrendingUpIcon /> },
  { id: 4, name: "Corporate Formation", icon: <BusinessIcon /> },
  { id: 5, name: "IP & Patents", icon: <AccountBalanceIcon /> },
  { id: 6, name: "Employment Law", icon: <RocketLaunchIcon /> }
];

const ExpertHelpPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [searching, setSearching] = useState(false);
  const [query, setQuery] = useState('');
  const navigate = useNavigate();
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic);
  };
  
  const handleSearch = () => {
    setSearching(true);
    // Simulate search delay
    setTimeout(() => {
      setSearching(false);
    }, 1500);
  };
  
  const renderRatingStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push(<StarIcon key={`full-${i}`} sx={{ color: '#FFD700' }} />);
    }
    
    if (hasHalfStar) {
      stars.push(<StarHalfIcon key="half" sx={{ color: '#FFD700' }} />);
    }
    
    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<StarBorderIcon key={`empty-${i}`} sx={{ color: '#FFD700' }} />);
    }
    
    return stars;
  };
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom fontWeight="bold" sx={{ color: '#333' }}>
        Startup Legal Experts
      </Typography>
      <Typography variant="h6" color="text.secondary" paragraph>
        Connect with specialized attorneys who understand startup legal needs. From GDPR compliance to Series A funding, 
        get expert guidance that scales with your growth.
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Typography variant="h6" gutterBottom>
          🚀 Find Your Startup Legal Expert
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="e.g., 'Need GDPR compliance for EU customers' or 'Raising Series A, need term sheet review'"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              sx={{ 
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  backgroundColor: 'rgba(255,255,255,0.9)',
                  '& fieldset': { borderColor: 'rgba(255,255,255,0.3)' },
                  '&:hover fieldset': { borderColor: 'rgba(255,255,255,0.5)' },
                  '&.Mui-focused fieldset': { borderColor: 'white' }
                }
              }}
            />
          </Grid>
          <Grid item xs={12} md={4} sx={{ display: 'flex', alignItems: 'center' }}>
            <Button 
              variant="outlined" 
              fullWidth 
              disabled={searching || !query.trim()}
              onClick={handleSearch}
              sx={{ 
                height: 54,
                borderColor: 'white',
                color: 'white',
                '&:hover': {
                  borderColor: 'white',
                  backgroundColor: 'rgba(255,255,255,0.1)'
                }
              }}
            >
              {searching ? <CircularProgress size={24} sx={{ color: 'white' }} /> : "Find Expert"}
            </Button>
          </Grid>
        </Grid>
        
        <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
          💡 Or browse by startup legal area:
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {legalTopics.map((topic) => (
            <Chip
              key={topic.id}
              label={topic.name}
              icon={topic.icon}
              onClick={() => handleTopicSelect(topic)}
              sx={{ 
                mb: 1,
                backgroundColor: selectedTopic?.id === topic.id ? 'rgba(255,255,255,0.9)' : 'rgba(255,255,255,0.2)',
                color: selectedTopic?.id === topic.id ? '#333' : 'white',
                border: selectedTopic?.id === topic.id ? 'none' : '1px solid rgba(255,255,255,0.3)',
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.3)'
                }
              }}
            />
          ))}
        </Box>
      </Paper>
      
      <Tabs value={tabValue} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="All Experts" />
        <Tab label="Compliance Specialists" />
        <Tab label="Fundraising Experts" />
        <Tab label="Corporate Law" />
      </Tabs>
      
      <Grid container spacing={3}>
        {attorneys.map((attorney) => (
          <Grid item xs={12} md={6} key={attorney.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar 
                    sx={{ 
                      bgcolor: 'primary.main', 
                      mr: 2,
                      width: 56,
                      height: 56,
                      fontSize: '1.2rem'
                    }}
                  >
                    {attorney.avatar}
                  </Avatar>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" fontWeight="bold">
                      {attorney.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      {renderRatingStars(attorney.rating)}
                      <Typography variant="body2" sx={{ ml: 1 }}>
                        {attorney.rating} ({attorney.reviewCount} reviews)
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="success.main" sx={{ fontWeight: 600 }}>
                      {attorney.successRate} Success Rate
                    </Typography>
                  </Box>
                </Box>
                
                <Box sx={{ mb: 2 }}>
                  {attorney.specialties.map((specialty, index) => (
                    <Chip 
                      key={index}
                      label={specialty} 
                      size="small" 
                      color="primary"
                      variant="outlined"
                      sx={{ mr: 0.5, mb: 0.5 }}
                    />
                  ))}
                </Box>
                
                <Typography variant="body2" color="text.secondary" paragraph>
                  {attorney.bio}
                </Typography>
                
                <List dense>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon>
                      <LocationOnIcon color="action" />
                    </ListItemIcon>
                    <ListItemText primary={attorney.location} />
                  </ListItem>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon>
                      <AccessTimeIcon color="action" />
                    </ListItemIcon>
                    <ListItemText primary={`Available: ${attorney.availability}`} />
                  </ListItem>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon>
                      <AttachMoneyIcon color="action" />
                    </ListItemIcon>
                    <ListItemText primary={`${attorney.hourlyRate}/hour`} />
                  </ListItem>
                </List>
              </CardContent>
              
              <Divider />
              
              <CardActions sx={{ p: 2 }}>
                <Button 
                  variant="contained" 
                  fullWidth
                  onClick={() => navigate('/legal-chat')}
                  sx={{ 
                    background: 'linear-gradient(45deg, #667eea, #764ba2)',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #5a6fd8, #6a4190)',
                    }
                  }}
                >
                  Connect Now
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      <Paper sx={{ p: 3, mt: 4, textAlign: 'center', background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
        <Typography variant="h5" gutterBottom fontWeight="bold">
          🎯 Need Immediate Help?
        </Typography>
        <Typography variant="body1" paragraph>
          For urgent compliance issues or time-sensitive legal matters, connect with our AI Legal Assistant for instant guidance.
        </Typography>
        <Button 
          variant="outlined"
          size="large"
          onClick={() => navigate('/legal-chat')}
          sx={{ 
            borderColor: 'white',
            color: 'white',
            '&:hover': {
              borderColor: 'white',
              backgroundColor: 'rgba(255,255,255,0.1)'
            }
          }}
        >
          Start AI Chat →
        </Button>
      </Paper>
    </Container>
  );
};

export default ExpertHelpPage; 
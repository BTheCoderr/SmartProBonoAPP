import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Avatar,
  Rating,
  InputAdornment,
} from '@mui/material';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import { useTranslation } from 'react-i18next';

const FindLawyerPage = () => {
  const { t } = useTranslation();

  const [searchParams, setSearchParams] = useState({
    location: '',
    practiceArea: '',
    language: '',
    experience: '',
  });

  // Mock data for lawyers - replace with API call
  const lawyers = [
    {
      id: 1,
      name: 'Sarah Johnson',
      photo: 'https://i.pravatar.cc/150?img=1',
      practiceAreas: ['Immigration', 'Family Law'],
      languages: ['English', 'Spanish'],
      experience: '15 years',
      rating: 4.8,
      location: 'New York, NY',
      bio: 'Specializing in immigration and family law with a focus on helping underserved communities.',
    },
    {
      id: 2,
      name: 'Michael Chen',
      photo: 'https://i.pravatar.cc/150?img=2',
      practiceAreas: ['Civil Rights', 'Employment Law'],
      languages: ['English', 'Mandarin'],
      experience: '10 years',
      rating: 4.5,
      location: 'San Francisco, CA',
      bio: 'Dedicated to protecting civil rights and ensuring fair employment practices.',
    },
    {
      id: 3,
      name: 'Maria Rodriguez',
      photo: 'https://i.pravatar.cc/150?img=3',
      practiceAreas: ['Criminal Defense', 'Immigration'],
      languages: ['English', 'Spanish', 'Portuguese'],
      experience: '8 years',
      rating: 4.7,
      location: 'Miami, FL',
      bio: 'Passionate about defending immigrant rights and providing criminal defense services.',
    },
  ];

  const practiceAreas = [
    'Immigration',
    'Family Law',
    'Civil Rights',
    'Criminal Defense',
    'Employment Law',
    'Housing Law',
  ];

  const languages = ['English', 'Spanish', 'Mandarin', 'Portuguese', 'Arabic', 'French'];

  const handleSearchChange = (event) => {
    const { name, value } = event.target;
    setSearchParams((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleConnect = async (lawyerId) => {
    try {
      // TODO: Implement connection logic with backend
      const response = await fetch(`/api/connect-lawyer/${lawyerId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ lawyerId }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to connect with lawyer');
      }
      
      // Show success message using your preferred notification system
    } catch (error) {
      // Handle error using your preferred error handling system
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          {t('Find a Pro Bono Lawyer')}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          {t('Connect with experienced attorneys ready to help with your legal needs')}
        </Typography>
      </Box>

      {/* Search and Filter Section */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                name="location"
                label="Location"
                value={searchParams.location}
                onChange={handleSearchChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LocationOnIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel>Practice Area</InputLabel>
                <Select
                  name="practiceArea"
                  value={searchParams.practiceArea}
                  onChange={handleSearchChange}
                  label="Practice Area"
                >
                  <MenuItem value="">All</MenuItem>
                  {practiceAreas.map((area) => (
                    <MenuItem key={area} value={area}>
                      {area}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel>Language</InputLabel>
                <Select
                  name="language"
                  value={searchParams.language}
                  onChange={handleSearchChange}
                  label="Language"
                >
                  <MenuItem value="">All</MenuItem>
                  {languages.map((lang) => (
                    <MenuItem key={lang} value={lang}>
                      {lang}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel>Experience</InputLabel>
                <Select
                  name="experience"
                  value={searchParams.experience}
                  onChange={handleSearchChange}
                  label="Experience"
                >
                  <MenuItem value="">Any</MenuItem>
                  <MenuItem value="0-5">0-5 years</MenuItem>
                  <MenuItem value="5-10">5-10 years</MenuItem>
                  <MenuItem value="10+">10+ years</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Lawyer Listings */}
      <Grid container spacing={3}>
        {lawyers.map((lawyer) => (
          <Grid item xs={12} md={6} lg={4} key={lawyer.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar
                    src={lawyer.photo}
                    alt={lawyer.name}
                    sx={{ width: 64, height: 64, mr: 2 }}
                  />
                  <Box>
                    <Typography variant="h6" component="h2">
                      {lawyer.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
                      <Rating value={lawyer.rating} readOnly size="small" />
                      <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                        ({lawyer.rating})
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      <LocationOnIcon sx={{ fontSize: 'small', mr: 0.5, verticalAlign: 'middle' }} />
                      {lawyer.location}
                    </Typography>
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" paragraph>
                  {lawyer.bio}
                </Typography>

                <Box sx={{ mb: 1 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Practice Areas:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {lawyer.practiceAreas.map((area) => (
                      <Chip key={area} label={area} size="small" />
                    ))}
                  </Box>
                </Box>

                <Box>
                  <Typography variant="subtitle2" gutterBottom>
                    Languages:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {lawyer.languages.map((lang) => (
                      <Chip key={lang} label={lang} size="small" variant="outlined" />
                    ))}
                  </Box>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  onClick={() => handleConnect(lawyer.id)}
                >
                  Connect
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default FindLawyerPage; 
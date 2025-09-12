import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  TextField, 
  Button, 
  Grid, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Checkbox, 
  FormControlLabel, 
  FormGroup,
  Alert,
  Snackbar
} from '@mui/material';
import { Send, VolunteerActivism } from '@mui/icons-material';
import Header from '../components/Header';
import Footer from '../components/Footer';

const VolunteerFormPage = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    profession: '',
    experience: '',
    areasOfInterest: [],
    availability: '',
    motivation: '',
    additionalInfo: ''
  });
  
  const [submitted, setSubmitted] = useState(false);
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      areasOfInterest: checked 
        ? [...prev.areasOfInterest, name]
        : prev.areasOfInterest.filter(area => area !== name)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the data to your backend
    console.log('Volunteer form submitted:', formData);
    setSubmitted(true);
    setOpenSnackbar(true);
  };

  const areasOfInterest = [
    'Immigration Law',
    'Family Law',
    'Criminal Defense',
    'Personal Injury',
    'Civil Rights',
    'Housing Law',
    'Employment Law',
    'Elder Law',
    'Veterans Affairs',
    'General Legal Support'
  ];

  if (submitted) {
    return (
      <>
        <Header />
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
            <VolunteerActivism sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" component="h1" gutterBottom>
              Thank You for Your Interest!
            </Typography>
            <Typography variant="h6" color="text.secondary" paragraph>
              We've received your volunteer application and will review it within 2-3 business days.
            </Typography>
            <Typography variant="body1" paragraph>
              Our team will contact you to discuss next steps and how you can contribute to making 
              legal help more accessible to everyone.
            </Typography>
            <Button 
              variant="contained" 
              size="large" 
              onClick={() => setSubmitted(false)}
              sx={{ mt: 2 }}
            >
              Submit Another Application
            </Button>
          </Paper>
        </Container>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Header />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Become a Volunteer
          </Typography>
          
          <Typography variant="h6" color="text.secondary" align="center" sx={{ mb: 4 }}>
            Join our mission to make legal help accessible to everyone
          </Typography>

          <Box component="form" onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  name="firstName"
                  label="First Name"
                  value={formData.firstName}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  name="lastName"
                  label="Last Name"
                  value={formData.lastName}
                  onChange={handleChange}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  name="email"
                  label="Email Address"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  name="phone"
                  label="Phone Number"
                  value={formData.phone}
                  onChange={handleChange}
                />
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Profession</InputLabel>
                  <Select
                    name="profession"
                    value={formData.profession}
                    label="Profession"
                    onChange={handleChange}
                  >
                    <MenuItem value="attorney">Attorney</MenuItem>
                    <MenuItem value="paralegal">Paralegal</MenuItem>
                    <MenuItem value="law_student">Law Student</MenuItem>
                    <MenuItem value="legal_assistant">Legal Assistant</MenuItem>
                    <MenuItem value="other_legal">Other Legal Professional</MenuItem>
                    <MenuItem value="non_legal">Non-Legal Professional</MenuItem>
                    <MenuItem value="student">Student</MenuItem>
                    <MenuItem value="other">Other</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="experience"
                  label="Years of Experience"
                  value={formData.experience}
                  onChange={handleChange}
                  placeholder="e.g., 5 years, Recent graduate, etc."
                />
              </Grid>

              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Areas of Interest
                </Typography>
                <FormGroup>
                  <Grid container>
                    {areasOfInterest.map((area) => (
                      <Grid item xs={12} sm={6} key={area}>
                        <FormControlLabel
                          control={
                            <Checkbox
                              name={area}
                              checked={formData.areasOfInterest.includes(area)}
                              onChange={handleCheckboxChange}
                            />
                          }
                          label={area}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </FormGroup>
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Availability</InputLabel>
                  <Select
                    name="availability"
                    value={formData.availability}
                    label="Availability"
                    onChange={handleChange}
                  >
                    <MenuItem value="weekdays">Weekdays</MenuItem>
                    <MenuItem value="weekends">Weekends</MenuItem>
                    <MenuItem value="evenings">Evenings</MenuItem>
                    <MenuItem value="flexible">Flexible</MenuItem>
                    <MenuItem value="limited">Limited (specify in additional info)</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="motivation"
                  label="Why do you want to volunteer with SmartProBono?"
                  multiline
                  rows={3}
                  value={formData.motivation}
                  onChange={handleChange}
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="additionalInfo"
                  label="Additional Information"
                  multiline
                  rows={3}
                  value={formData.additionalInfo}
                  onChange={handleChange}
                  placeholder="Any additional information you'd like to share..."
                />
              </Grid>

              <Grid item xs={12}>
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="large"
                  startIcon={<Send />}
                  sx={{ mt: 2 }}
                >
                  Submit Volunteer Application
                </Button>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      </Container>
      <Footer />
      
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={() => setOpenSnackbar(false)}
      >
        <Alert onClose={() => setOpenSnackbar(false)} severity="success">
          Thank you! Your volunteer application has been submitted.
        </Alert>
      </Snackbar>
    </>
  );
};

export default VolunteerFormPage;

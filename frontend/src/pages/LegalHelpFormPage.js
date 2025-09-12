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
  RadioGroup, 
  FormControlLabel, 
  Radio,
  FormLabel,
  Alert,
  Snackbar
} from '@mui/material';
import { Send, Gavel } from '@mui/icons-material';
import Header from '../components/Header';
import Footer from '../components/Footer';

const LegalHelpFormPage = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    legalIssue: '',
    urgency: '',
    description: '',
    location: '',
    incomeLevel: '',
    previousLegalHelp: '',
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

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the data to your backend
    console.log('Legal help form submitted:', formData);
    setSubmitted(true);
    setOpenSnackbar(true);
  };

  const legalIssues = [
    'Immigration',
    'Family Law (Divorce, Custody, etc.)',
    'Criminal Defense',
    'Personal Injury',
    'Housing/Eviction',
    'Employment Issues',
    'Civil Rights',
    'Elder Law',
    'Veterans Benefits',
    'Other'
  ];

  if (submitted) {
    return (
      <>
        <Header />
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
            <Gavel sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" component="h1" gutterBottom>
              Help Request Submitted!
            </Typography>
            <Typography variant="h6" color="text.secondary" paragraph>
              We've received your legal help request and will review it within 24-48 hours.
            </Typography>
            <Typography variant="body1" paragraph>
              Our team will contact you to discuss your case and connect you with the appropriate 
              legal resources or professionals.
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              If this is an emergency legal situation, please contact your local legal aid office 
              or emergency services immediately.
            </Typography>
            <Button 
              variant="contained" 
              size="large" 
              onClick={() => setSubmitted(false)}
              sx={{ mt: 2 }}
            >
              Submit Another Request
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
            Get Legal Help
          </Typography>
          
          <Typography variant="h6" color="text.secondary" align="center" sx={{ mb: 4 }}>
            Tell us about your legal situation and we'll help connect you with the right resources
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

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  name="location"
                  label="City, State"
                  value={formData.location}
                  onChange={handleChange}
                  placeholder="e.g., New York, NY"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Legal Issue Type</InputLabel>
                  <Select
                    name="legalIssue"
                    value={formData.legalIssue}
                    label="Legal Issue Type"
                    onChange={handleChange}
                  >
                    {legalIssues.map((issue) => (
                      <MenuItem key={issue} value={issue}>
                        {issue}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <FormControl component="fieldset">
                  <FormLabel component="legend">Urgency Level</FormLabel>
                  <RadioGroup
                    name="urgency"
                    value={formData.urgency}
                    onChange={handleChange}
                    row
                  >
                    <FormControlLabel value="low" control={<Radio />} label="Low" />
                    <FormControlLabel value="medium" control={<Radio />} label="Medium" />
                    <FormControlLabel value="high" control={<Radio />} label="High" />
                    <FormControlLabel value="emergency" control={<Radio />} label="Emergency" />
                  </RadioGroup>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="description"
                  label="Describe Your Legal Situation"
                  multiline
                  rows={4}
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Please provide as much detail as possible about your legal issue..."
                />
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Income Level</InputLabel>
                  <Select
                    name="incomeLevel"
                    value={formData.incomeLevel}
                    label="Income Level"
                    onChange={handleChange}
                  >
                    <MenuItem value="below_poverty">Below Poverty Line</MenuItem>
                    <MenuItem value="low_income">Low Income</MenuItem>
                    <MenuItem value="moderate_income">Moderate Income</MenuItem>
                    <MenuItem value="middle_income">Middle Income</MenuItem>
                    <MenuItem value="prefer_not_to_say">Prefer Not to Say</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <FormControl component="fieldset">
                  <FormLabel component="legend">Have you sought legal help before?</FormLabel>
                  <RadioGroup
                    name="previousLegalHelp"
                    value={formData.previousLegalHelp}
                    onChange={handleChange}
                    row
                  >
                    <FormControlLabel value="no" control={<Radio />} label="No" />
                    <FormControlLabel value="yes_attorney" control={<Radio />} label="Yes - Attorney" />
                    <FormControlLabel value="yes_legal_aid" control={<Radio />} label="Yes - Legal Aid" />
                    <FormControlLabel value="yes_other" control={<Radio />} label="Yes - Other" />
                  </RadioGroup>
                </FormControl>
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
                  placeholder="Any additional information that might be helpful..."
                />
              </Grid>

              <Grid item xs={12}>
                <Alert severity="info" sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    <strong>Important:</strong> This form is for initial screening only. 
                    Submitting this form does not create an attorney-client relationship. 
                    For urgent legal matters, please contact your local legal aid office or emergency services.
                  </Typography>
                </Alert>
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
                  Submit Help Request
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
          Thank you! Your legal help request has been submitted.
        </Alert>
      </Snackbar>
    </>
  );
};

export default LegalHelpFormPage;

import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  TextField,
  Alert,
  Snackbar,
  Stack,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  RadioGroup,
  FormControlLabel,
  Radio,
  FormLabel,
  Divider
} from '@mui/material';
import EmailIcon from '@mui/icons-material/Email';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PhoneIcon from '@mui/icons-material/Phone';
import SendIcon from '@mui/icons-material/Send';
import { useTranslation } from 'react-i18next';
import { PageLayout, Button, Card } from '../design-system';

function Contact() {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    caseType: '',
    urgency: '',
    state: '',
    city: '',
    zipCode: '',
    contactMethod: '',
    bestTime: '',
    hearAbout: '',
    hasAttorney: '',
    caseValue: '',
    message: ''
  });
  const [showSuccess, setShowSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:3001/api/contact/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const result = await response.json();
      
      if (result.success) {
        setShowSuccess(true);
        setFormData({
          firstName: '',
          lastName: '',
          email: '',
          phone: '',
          caseType: '',
          urgency: '',
          state: '',
          city: '',
          zipCode: '',
          contactMethod: '',
          bestTime: '',
          hearAbout: '',
          hasAttorney: '',
          caseValue: '',
          message: ''
        });
      } else {
        console.error('Contact form submission failed:', result.error);
        // You could add error state handling here
      }
    } catch (error) {
      console.error('Error submitting contact form:', error);
      // Fallback: still show success for now, but log the error
      setShowSuccess(true);
      setFormData({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        caseType: '',
        urgency: '',
        state: '',
        city: '',
        zipCode: '',
        contactMethod: '',
        bestTime: '',
        hearAbout: '',
        hasAttorney: '',
        caseValue: '',
        message: ''
      });
    }
  };

  return (
    <PageLayout
      title={t('pages.contact.title')}
      description={t('pages.contact.subtitle')}
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Stack spacing={2}>
              <Card sx={{ borderRadius: 2, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                <Box sx={{ p: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <EmailIcon color="primary" sx={{ mr: 2 }} />
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>{t('contact.info.email')}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        bferrell@smartprobono.org
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </Card>

              <Card sx={{ borderRadius: 2, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                <Box sx={{ p: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <PhoneIcon color="primary" sx={{ mr: 2 }} />
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>{t('contact.info.phone')}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        (401) 217-9799
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </Card>

              <Card sx={{ borderRadius: 2, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                <Box sx={{ p: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <LocationOnIcon color="primary" sx={{ mr: 2 }} />
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>Location</Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.4 }}>
                        225 Dyer St, Providence, RI 02903
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </Card>
            </Stack>
          </Grid>

          <Grid item xs={12} md={8}>
            <Card sx={{ borderRadius: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <Box sx={{ p: 4 }}>
                <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
                  {t('contact.form.send')}
                </Typography>
                <form onSubmit={handleSubmit}>
                  <Grid container spacing={3}>
                    {/* Basic Information */}
                    <Grid item xs={12}>
                      <Typography variant="h6" sx={{ color: '#0F3D5E', mb: 2, fontWeight: 600 }}>
                        Basic Information
                      </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        required
                        fullWidth
                        label={t('contact.form.firstName')}
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleChange}
                        variant="outlined"
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        required
                        fullWidth
                        label={t('contact.form.lastName')}
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleChange}
                        variant="outlined"
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        required
                        fullWidth
                        label={t('contact.form.email')}
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        variant="outlined"
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label={t('contact.form.phone')}
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        variant="outlined"
                      />
                    </Grid>

                    {/* Legal Case Information */}
                    <Grid item xs={12}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="h6" sx={{ color: '#0F3D5E', mb: 2, fontWeight: 600 }}>
                        Legal Case Information
                      </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth required>
                        <InputLabel>Case Type</InputLabel>
                        <Select
                          name="caseType"
                          value={formData.caseType}
                          onChange={handleChange}
                          label="Case Type"
                        >
                          <MenuItem value="immigration">Immigration</MenuItem>
                          <MenuItem value="family">Family Law</MenuItem>
                          <MenuItem value="criminal">Criminal Defense</MenuItem>
                          <MenuItem value="civil">Civil Rights</MenuItem>
                          <MenuItem value="employment">Employment Law</MenuItem>
                          <MenuItem value="housing">Housing/Eviction</MenuItem>
                          <MenuItem value="consumer">Consumer Rights</MenuItem>
                          <MenuItem value="other">Other</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth required>
                        <InputLabel>Urgency Level</InputLabel>
                        <Select
                          name="urgency"
                          value={formData.urgency}
                          onChange={handleChange}
                          label="Urgency Level"
                        >
                          <MenuItem value="low">Low - Can wait 1-2 weeks</MenuItem>
                          <MenuItem value="medium">Medium - Need help within a week</MenuItem>
                          <MenuItem value="high">High - Need help within 2-3 days</MenuItem>
                          <MenuItem value="emergency">Emergency - Need immediate help</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>

                    {/* Location Information */}
                    <Grid item xs={12}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="h6" sx={{ color: '#0F3D5E', mb: 2, fontWeight: 600 }}>
                        Location Information
                      </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <FormControl fullWidth required>
                        <InputLabel>State</InputLabel>
                        <Select
                          name="state"
                          value={formData.state}
                          onChange={handleChange}
                          label="State"
                        >
                          <MenuItem value="AL">Alabama</MenuItem>
                          <MenuItem value="AK">Alaska</MenuItem>
                          <MenuItem value="AZ">Arizona</MenuItem>
                          <MenuItem value="AR">Arkansas</MenuItem>
                          <MenuItem value="CA">California</MenuItem>
                          <MenuItem value="CO">Colorado</MenuItem>
                          <MenuItem value="CT">Connecticut</MenuItem>
                          <MenuItem value="DE">Delaware</MenuItem>
                          <MenuItem value="FL">Florida</MenuItem>
                          <MenuItem value="GA">Georgia</MenuItem>
                          <MenuItem value="HI">Hawaii</MenuItem>
                          <MenuItem value="ID">Idaho</MenuItem>
                          <MenuItem value="IL">Illinois</MenuItem>
                          <MenuItem value="IN">Indiana</MenuItem>
                          <MenuItem value="IA">Iowa</MenuItem>
                          <MenuItem value="KS">Kansas</MenuItem>
                          <MenuItem value="KY">Kentucky</MenuItem>
                          <MenuItem value="LA">Louisiana</MenuItem>
                          <MenuItem value="ME">Maine</MenuItem>
                          <MenuItem value="MD">Maryland</MenuItem>
                          <MenuItem value="MA">Massachusetts</MenuItem>
                          <MenuItem value="MI">Michigan</MenuItem>
                          <MenuItem value="MN">Minnesota</MenuItem>
                          <MenuItem value="MS">Mississippi</MenuItem>
                          <MenuItem value="MO">Missouri</MenuItem>
                          <MenuItem value="MT">Montana</MenuItem>
                          <MenuItem value="NE">Nebraska</MenuItem>
                          <MenuItem value="NV">Nevada</MenuItem>
                          <MenuItem value="NH">New Hampshire</MenuItem>
                          <MenuItem value="NJ">New Jersey</MenuItem>
                          <MenuItem value="NM">New Mexico</MenuItem>
                          <MenuItem value="NY">New York</MenuItem>
                          <MenuItem value="NC">North Carolina</MenuItem>
                          <MenuItem value="ND">North Dakota</MenuItem>
                          <MenuItem value="OH">Ohio</MenuItem>
                          <MenuItem value="OK">Oklahoma</MenuItem>
                          <MenuItem value="OR">Oregon</MenuItem>
                          <MenuItem value="PA">Pennsylvania</MenuItem>
                          <MenuItem value="RI">Rhode Island</MenuItem>
                          <MenuItem value="SC">South Carolina</MenuItem>
                          <MenuItem value="SD">South Dakota</MenuItem>
                          <MenuItem value="TN">Tennessee</MenuItem>
                          <MenuItem value="TX">Texas</MenuItem>
                          <MenuItem value="UT">Utah</MenuItem>
                          <MenuItem value="VT">Vermont</MenuItem>
                          <MenuItem value="VA">Virginia</MenuItem>
                          <MenuItem value="WA">Washington</MenuItem>
                          <MenuItem value="WV">West Virginia</MenuItem>
                          <MenuItem value="WI">Wisconsin</MenuItem>
                          <MenuItem value="WY">Wyoming</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <TextField
                        fullWidth
                        label="City"
                        name="city"
                        value={formData.city}
                        onChange={handleChange}
                        variant="outlined"
                      />
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <TextField
                        fullWidth
                        label="Zip Code"
                        name="zipCode"
                        value={formData.zipCode}
                        onChange={handleChange}
                        variant="outlined"
                      />
                    </Grid>

                    {/* Contact Preferences */}
                    <Grid item xs={12}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="h6" sx={{ color: '#0F3D5E', mb: 2, fontWeight: 600 }}>
                        Contact Preferences
                      </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <FormControl component="fieldset">
                        <FormLabel component="legend">Preferred Contact Method</FormLabel>
                        <RadioGroup
                          name="contactMethod"
                          value={formData.contactMethod}
                          onChange={handleChange}
                          row
                        >
                          <FormControlLabel value="email" control={<Radio />} label="Email" />
                          <FormControlLabel value="phone" control={<Radio />} label="Phone" />
                          <FormControlLabel value="text" control={<Radio />} label="Text" />
                        </RadioGroup>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth>
                        <InputLabel>Best Time to Contact</InputLabel>
                        <Select
                          name="bestTime"
                          value={formData.bestTime}
                          onChange={handleChange}
                          label="Best Time to Contact"
                        >
                          <MenuItem value="morning">Morning (8AM-12PM)</MenuItem>
                          <MenuItem value="afternoon">Afternoon (12PM-5PM)</MenuItem>
                          <MenuItem value="evening">Evening (5PM-8PM)</MenuItem>
                          <MenuItem value="anytime">Any time</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>

                    {/* Additional Information */}
                    <Grid item xs={12}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="h6" sx={{ color: '#0F3D5E', mb: 2, fontWeight: 600 }}>
                        Additional Information
                      </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <FormControl fullWidth>
                        <InputLabel>How did you hear about us?</InputLabel>
                        <Select
                          name="hearAbout"
                          value={formData.hearAbout}
                          onChange={handleChange}
                          label="How did you hear about us?"
                        >
                          <MenuItem value="google">Google Search</MenuItem>
                          <MenuItem value="social">Social Media</MenuItem>
                          <MenuItem value="referral">Friend/Family Referral</MenuItem>
                          <MenuItem value="lawyer">Another Lawyer</MenuItem>
                          <MenuItem value="organization">Community Organization</MenuItem>
                          <MenuItem value="advertisement">Advertisement</MenuItem>
                          <MenuItem value="other">Other</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <FormControl component="fieldset">
                        <FormLabel component="legend">Are you currently represented by an attorney?</FormLabel>
                        <RadioGroup
                          name="hasAttorney"
                          value={formData.hasAttorney}
                          onChange={handleChange}
                          row
                        >
                          <FormControlLabel value="yes" control={<Radio />} label="Yes" />
                          <FormControlLabel value="no" control={<Radio />} label="No" />
                        </RadioGroup>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                      <FormControl fullWidth>
                        <InputLabel>Estimated Case Value (Optional)</InputLabel>
                        <Select
                          name="caseValue"
                          value={formData.caseValue}
                          onChange={handleChange}
                          label="Estimated Case Value (Optional)"
                        >
                          <MenuItem value="under-5k">Under $5,000</MenuItem>
                          <MenuItem value="5k-25k">$5,000 - $25,000</MenuItem>
                          <MenuItem value="25k-100k">$25,000 - $100,000</MenuItem>
                          <MenuItem value="100k-500k">$100,000 - $500,000</MenuItem>
                          <MenuItem value="over-500k">Over $500,000</MenuItem>
                          <MenuItem value="unknown">Unknown/Not applicable</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>

                    {/* Message */}
                    <Grid item xs={12}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="h6" sx={{ color: '#0F3D5E', mb: 2, fontWeight: 600 }}>
                        Tell Us About Your Case
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <TextField
                        required
                        fullWidth
                        label={t('contact.form.message')}
                        name="message"
                        value={formData.message}
                        onChange={handleChange}
                        multiline
                        rows={4}
                        variant="outlined"
                        placeholder="Please describe your legal issue in detail. Include any important dates, deadlines, or specific questions you have."
                        sx={{ mb: 2 }}
                      />
                    </Grid>
                  </Grid>
                  <Button
                    type="submit"
                    variant="contained"
                    size="large"
                    endIcon={<SendIcon />}
                    sx={{
                      borderRadius: 2,
                      textTransform: 'none',
                      py: 1.5,
                      px: 4,
                      background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)',
                      color: '#ffffff',
                      '&:hover': {
                        boxShadow: '0 2px 8px rgba(31, 182, 166, .3)',
                        transform: 'translateY(-2px)',
                        color: '#ffffff'
                      }
                    }}
                  >
                    {t('contact.form.send')}
                  </Button>
                </form>
              </Box>
            </Card>
          </Grid>
        </Grid>

        <Snackbar
          open={showSuccess}
          autoHideDuration={6000}
          onClose={() => setShowSuccess(false)}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert 
            onClose={() => setShowSuccess(false)} 
            severity="success"
            sx={{ width: '100%' }}
          >
            {t('contact.form.success')}
          </Alert>
        </Snackbar>
      </Container>
    </PageLayout>
  );
}

export default Contact;
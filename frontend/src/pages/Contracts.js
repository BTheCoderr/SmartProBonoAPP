import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  IconButton,
  CircularProgress,
} from '@mui/material';
import DescriptionIcon from '@mui/icons-material/Description';
import BusinessIcon from '@mui/icons-material/Business';
import WorkIcon from '@mui/icons-material/Work';
import HomeIcon from '@mui/icons-material/Home';
import PersonIcon from '@mui/icons-material/Person';
import GavelIcon from '@mui/icons-material/Gavel';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import DownloadIcon from '@mui/icons-material/Download';
import CloseIcon from '@mui/icons-material/Close';
import PageLayout from '../components/PageLayout';
import { contractsApi } from '../services/api';
const templates = {
  'Last Will and Testament': {
    icon: <DescriptionIcon fontSize="large" />,
    description: 'Template for creating a last will and testament',
    languages: ['English'],
    category: 'PERSONAL',
    color: '#1976d2',
    fields: ['fullName', 'address', 'beneficiaries', 'executor'],
  },
  'Power of Attorney': {
    icon: <GavelIcon fontSize="large" />,
    description: 'Legal document granting authority to act on behalf of another',
    languages: ['English'],
    category: 'LEGAL',
    color: '#2e7d32',
    fields: ['grantor', 'attorney', 'powers', 'effectiveDate'],
  },
  'Rental Agreement': {
    icon: <HomeIcon fontSize="large" />,
    description: 'Property rental contract',
    languages: ['English', 'Spanish', 'French'],
    category: 'REAL_ESTATE',
    color: '#ed6c02',
    fields: ['landlord', 'tenant', 'property', 'rent', 'term'],
  },
  'Employment Contract': {
    icon: <WorkIcon fontSize="large" />,
    description: 'Standard employment agreement template',
    languages: ['English', 'Spanish'],
    category: 'EMPLOYMENT',
    color: '#9c27b0',
    fields: ['employer', 'employee', 'position', 'salary', 'startDate'],
  },
  'Non-Disclosure Agreement': {
    icon: <BusinessIcon fontSize="large" />,
    description: 'Confidentiality agreement for business purposes',
    languages: ['English'],
    category: 'BUSINESS',
    color: '#0288d1',
    fields: ['disclosingParty', 'receivingParty', 'purpose', 'duration'],
  },
  'Service Agreement': {
    icon: <DescriptionIcon fontSize="large" />,
    description: 'Professional service contract template',
    languages: ['English', 'Spanish', 'French'],
    category: 'BUSINESS',
    color: '#7b1fa2',
    fields: ['serviceProvider', 'client', 'services', 'compensation'],
  },
};
const categories = [
  { value: 'ALL', label: 'ALL TEMPLATES', icon: <DescriptionIcon /> },
  { value: 'BUSINESS', label: 'BUSINESS', icon: <BusinessIcon /> },
  { value: 'EMPLOYMENT', label: 'EMPLOYMENT', icon: <WorkIcon /> },
  { value: 'REAL_ESTATE', label: 'REAL ESTATE', icon: <HomeIcon /> },
  { value: 'PERSONAL', label: 'PERSONAL', icon: <PersonIcon /> },
  { value: 'LEGAL', label: 'LEGAL', icon: <GavelIcon /> },
  { value: 'HEALTHCARE', label: 'HEALTHCARE', icon: <LocalHospitalIcon /> },
];
function Contracts() {
  const [category, setCategory] = useState('ALL');
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [showSuccess, setShowSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const handleCategoryChange = (event, newValue) => {
    setCategory(newValue);
  };
  const handleTemplateSelect = templateName => {
    setSelectedTemplate(templateName);
    setFormData({});
    setError(null);
  };
  const handleClose = () => {
    setSelectedTemplate(null);
    setFormData({});
    setError(null);
  };
  const handleInputChange = field => event => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };
  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      await contractsApi.generate(selectedTemplate, formData, selectedLanguage);
      setShowSuccess(true);
      handleClose();
    } catch (error) {
      console.error('Error generating document:', error);
      setError(error.message || 'Failed to generate document. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  const filteredTemplates = Object.entries(templates).filter(
    ([_, template]) => category === 'ALL' || template.category === category
  );
  return (
    <PageLayout
      title="Legal Contract Templates"
      description="Generate professional legal documents in multiple languages"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Legal Document Templates
        </Typography>
        <Tabs
          value={category}
          onChange={handleCategoryChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ mb: 4 }}
        >
          {categories.map(cat => (
            <Tab
              key={cat.value}
              value={cat.value}
              label={cat.label}
              icon={cat.icon}
              iconPosition="start"
            />
          ))}
        </Tabs>
        <Grid container spacing={3}>
          {filteredTemplates.map(([name, template]) => (
            <Grid item xs={12} sm={6} md={4} key={name}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    {template.icon}
                    <Typography variant="h6" sx={{ ml: 1 }}>
                      {name}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {template.description}
                  </Typography>
                  <Box sx={{ mt: 'auto' }}>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Available in: {template.languages.join(', ')}
                    </Typography>
                    <Button
                      variant="contained"
                      fullWidth
                      onClick={() => handleTemplateSelect(name)}
                      startIcon={<DownloadIcon />}
                      sx={{
                        mt: 2,
                        bgcolor: template.color,
                        '&:hover': {
                          bgcolor: template.color,
                          filter: 'brightness(0.9)',
                        },
                      }}
                    >
                      Generate
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
        <Dialog
          open={!!selectedTemplate}
          onClose={() => !loading && handleClose()}
          maxWidth="sm"
          fullWidth
        >
          {selectedTemplate && (
            <>
              <DialogTitle>
                <Box
                  sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
                >
                  <Typography variant="h6">Generate {selectedTemplate}</Typography>
                  <IconButton onClick={handleClose} size="small" disabled={loading}>
                    <CloseIcon />
                  </IconButton>
                </Box>
              </DialogTitle>
              <DialogContent dividers>
                {error && (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                  </Alert>
                )}
                <Grid container spacing={2}>
                  {templates[selectedTemplate].fields.map(field => (
                    <Grid item xs={12} key={field}>
                      <TextField
                        fullWidth
                        label={
                          field.charAt(0).toUpperCase() + field.slice(1).replace(/([A-Z])/g, ' $1')
                        }
                        value={formData[field] || ''}
                        onChange={handleInputChange(field)}
                        variant="outlined"
                        required
                        disabled={loading}
                      />
                    </Grid>
                  ))}
                  {templates[selectedTemplate].languages.length > 1 && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" gutterBottom>
                        Select Language
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        {templates[selectedTemplate].languages.map(lang => (
                          <Chip
                            key={lang}
                            label={lang}
                            onClick={() => !loading && setSelectedLanguage(lang)}
                            color={selectedLanguage === lang ? 'primary' : 'default'}
                            sx={{ cursor: loading ? 'not-allowed' : 'pointer' }}
                          />
                        ))}
                      </Box>
                    </Grid>
                  )}
                </Grid>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleClose} disabled={loading}>
                  Cancel
                </Button>
                <Button
                  variant="contained"
                  onClick={handleGenerate}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <DownloadIcon />}
                  sx={{
                    bgcolor: templates[selectedTemplate].color,
                    '&:hover': {
                      bgcolor: templates[selectedTemplate].color,
                      filter: 'brightness(0.9)',
                    },
                  }}
                >
                  {loading ? 'Generating...' : 'Generate Document'}
                </Button>
              </DialogActions>
            </>
          )}
        </Dialog>
        <Dialog open={showSuccess} onClose={() => setShowSuccess(false)} maxWidth="xs" fullWidth>
          <DialogContent>
            <Alert severity="success" onClose={() => setShowSuccess(false)}>
              Document generated successfully! Check your downloads folder.
            </Alert>
          </DialogContent>
        </Dialog>
      </Container>
    </PageLayout>
  );
}
export default Contracts;
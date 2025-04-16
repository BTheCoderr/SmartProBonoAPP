import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Chip,
  Paper,
  Tabs,
  Tab,
  InputAdornment,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert,
} from '@mui/material';
import PageLayout from '../components/PageLayout';
import SearchIcon from '@mui/icons-material/Search';
import BusinessIcon from '@mui/icons-material/Business';
import WorkIcon from '@mui/icons-material/Work';
import HomeIcon from '@mui/icons-material/Home';
import PersonIcon from '@mui/icons-material/Person';
import GavelIcon from '@mui/icons-material/Gavel';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import DescriptionIcon from '@mui/icons-material/Description';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DownloadIcon from '@mui/icons-material/Download';
import CloseIcon from '@mui/icons-material/Close';
import { useNavigate } from 'react-router-dom';
import { contractsApi } from '../services/api';

const categories = [
  { value: 'ALL', label: 'All Templates' },
  { value: 'BUSINESS', label: 'Business', icon: <BusinessIcon /> },
  { value: 'EMPLOYMENT', label: 'Employment', icon: <WorkIcon /> },
  { value: 'REAL_ESTATE', label: 'Real Estate', icon: <HomeIcon /> },
  { value: 'PERSONAL', label: 'Personal', icon: <PersonIcon /> },
  { value: 'LEGAL', label: 'Legal', icon: <GavelIcon /> },
  { value: 'HEALTHCARE', label: 'Healthcare', icon: <LocalHospitalIcon /> },
];

const templates = [
  {
    title: 'Last Will and Testament',
    description: 'Template for creating a last will and testament',
    category: 'LEGAL',
    languages: ['English'],
    icon: <DescriptionIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
    color: '#1976d2',
  },
  {
    title: 'Power of Attorney',
    description: 'Legal document granting authority to act on behalf of another',
    category: 'LEGAL',
    languages: ['English'],
    icon: <DescriptionIcon sx={{ fontSize: 40, color: '#2e7d32' }} />,
    color: '#2e7d32',
  },
  {
    title: 'Rental Agreement',
    description: 'Property rental contract',
    category: 'REAL_ESTATE',
    languages: ['English', 'Spanish', 'French'],
    icon: <DescriptionIcon sx={{ fontSize: 40, color: '#ed6c02' }} />,
    color: '#ed6c02',
  },
  {
    title: 'Employment Contract',
    description: 'Standard employment agreement template',
    category: 'EMPLOYMENT',
    languages: ['English', 'Spanish'],
    icon: <DescriptionIcon sx={{ fontSize: 40, color: '#9c27b0' }} />,
    color: '#9c27b0',
  },
  {
    title: 'Non-Disclosure Agreement',
    description: 'Confidentiality agreement for business purposes',
    category: 'BUSINESS',
    languages: ['English'],
    icon: <DescriptionIcon sx={{ fontSize: 40, color: '#0288d1' }} />,
    color: '#0288d1',
  },
  {
    title: 'Service Agreement',
    description: 'Professional service contract template',
    category: 'BUSINESS',
    languages: ['English', 'Spanish', 'French'],
    icon: <DescriptionIcon sx={{ fontSize: 40, color: '#7b1fa2' }} />,
    color: '#7b1fa2',
  },
];

function ContractsPage() {
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const navigate = useNavigate();

  const handleCategoryChange = (event, newValue) => {
    setSelectedCategory(newValue);
  };

  const handleGenerateClick = template => {
    setSelectedTemplate(template);
    setFormData({});
    setError(null);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
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
      // Check required fields
      const requiredFields = selectedTemplate.fields || [];
      const missingFields = requiredFields.filter(field => !formData[field]);

      if (missingFields.length > 0) {
        throw new Error(`Please fill in all required fields: ${missingFields.join(', ')}`);
      }

      // Generate the contract
      await contractsApi.generate(
        selectedTemplate.title,
        formData,
        'English' // Default to English for now
      );

      // Close dialog on success
      handleCloseDialog();
    } catch (err) {
      setError(err.message || 'Failed to generate contract');
    } finally {
      setLoading(false);
    }
  };

  const filteredTemplates = templates.filter(template => {
    const matchesCategory = selectedCategory === 'ALL' || template.category === selectedCategory;
    const matchesSearch =
      template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <PageLayout
      title="Contract Resources"
      description="Access and generate legal document templates"
    >
      {/* Search and Filter Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              placeholder="Search templates..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" />
                  </InputAdornment>
                ),
              }}
              sx={{ mb: 2 }}
            />
            <Tabs
              value={selectedCategory}
              onChange={handleCategoryChange}
              variant="scrollable"
              scrollButtons="auto"
              sx={{ borderBottom: 1, borderColor: 'divider' }}
            >
              {categories.map(category => (
                <Tab
                  key={category.value}
                  value={category.value}
                  label={category.label}
                  icon={category.icon}
                  iconPosition="start"
                />
              ))}
            </Tabs>
          </Grid>
        </Grid>
      </Paper>

      {/* Templates Grid */}
      <Grid container spacing={4} sx={{ mb: 8 }}>
        {filteredTemplates.map((template, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    mb: 2,
                    gap: 1,
                  }}
                >
                  {template.icon}
                  <Typography variant="h6" component="div">
                    {template.title}
                  </Typography>
                </Box>
                <Typography color="text.secondary" paragraph>
                  {template.description}
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                  {template.languages.map((lang, i) => (
                    <Chip
                      key={i}
                      label={lang}
                      size="small"
                      icon={<CheckCircleIcon />}
                      sx={{ bgcolor: `${template.color}15` }}
                    />
                  ))}
                </Box>
              </CardContent>
              <Box sx={{ p: 2, pt: 0 }}>
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<DownloadIcon />}
                  onClick={() => handleGenerateClick(template)}
                  sx={{
                    borderColor: template.color,
                    color: template.color,
                    '&:hover': {
                      borderColor: template.color,
                      bgcolor: `${template.color}08`,
                    },
                  }}
                >
                  Generate
                </Button>
              </Box>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Contract Generation Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={() => !loading && handleCloseDialog()}
        maxWidth="sm"
        fullWidth
      >
        {selectedTemplate && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Typography variant="h6">Generate {selectedTemplate.title}</Typography>
                <IconButton onClick={handleCloseDialog} size="small" disabled={loading}>
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
              {selectedTemplate.fields?.map(field => (
                <TextField
                  key={field}
                  fullWidth
                  label={field}
                  value={formData[field] || ''}
                  onChange={handleInputChange(field)}
                  margin="normal"
                  required
                  disabled={loading}
                />
              ))}
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog} disabled={loading}>
                Cancel
              </Button>
              <Button
                onClick={handleGenerate}
                variant="contained"
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <DownloadIcon />}
              >
                {loading ? 'Generating...' : 'Generate Document'}
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Help Section */}
      <Paper sx={{ p: 4, bgcolor: 'primary.main', color: 'white' }}>
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} md={8}>
            <Typography variant="h5" gutterBottom>
              Need Help with Documents?
            </Typography>
            <Typography paragraph>
              Our legal experts can help you understand and customize these templates for your
              specific needs.
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Free document review" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Professional guidance" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Multiple language support" />
              </ListItem>
            </List>
          </Grid>
          <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/legal-chat')}
              sx={{
                bgcolor: 'white',
                color: 'primary.main',
                '&:hover': {
                  bgcolor: 'rgba(255, 255, 255, 0.9)',
                },
              }}
            >
              Get Expert Help
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </PageLayout>
  );
}

export default ContractsPage;

import { useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  TextField,
  Tab,
  Tabs,
  Box,
  IconButton,
  InputAdornment,
  CircularProgress,
  Alert,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import ContractForm from './ContractForm';
import config from '../config';
const ContractTemplates = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [category, setCategory] = useState(0);
  const [open, setOpen] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const categories = [
    'All',
    'Business',
    'Employment',
    'Real Estate',
    'Personal',
    'Legal',
    'Technology',
    'Healthcare',
  ];
  const templates = [
    {
      title: 'Last Will and Testament',
      category: 'Personal',
      description: 'Template for creating a last will and testament',
      fields: ['Testator Name', 'Executor Name', 'Beneficiaries', 'Assets'],
      languages: ['English'],
    },
    {
      title: 'Power of Attorney',
      category: 'Legal',
      description: 'Legal document granting authority to act on behalf of another',
      fields: ['Principal Name', 'Agent Name', 'Powers Granted', 'Effective Date'],
      languages: ['English'],
    },
    {
      title: 'Rental Agreement',
      category: 'Real Estate',
      description: 'Property rental contract',
      fields: ['Landlord', 'Tenant', 'Property Address', 'Rent Amount', 'Term'],
      languages: ['English', 'Spanish', 'French'],
    },
    {
      title: 'Employment Contract',
      category: 'Employment',
      description: 'Standard employment agreement template',
      fields: ['Employer', 'Employee', 'Position', 'Salary', 'Start Date'],
      languages: ['English', 'Spanish'],
    },
    {
      title: 'Non-Disclosure Agreement',
      category: 'Business',
      description: 'Confidentiality agreement for business purposes',
      fields: ['Party A', 'Party B', 'Confidential Information', 'Duration'],
      languages: ['English'],
    },
    {
      title: 'Service Agreement',
      category: 'Business',
      description: 'Professional service contract template',
      fields: ['Provider Name', 'Client Name', 'Service Details', 'Payment Terms'],
      languages: ['English', 'Spanish', 'French'],
    },
  ];
  const handleSearch = event => {
    setSearchQuery(event.target.value);
  };
  const handleCategoryChange = (event, newValue) => {
    setCategory(newValue);
  };
  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = category === 0 || template.category === categories[category];
    return matchesSearch && matchesCategory;
  });
  const handleGenerateClick = template => {
    setSelectedTemplate(template);
    setOpen(true);
  };
  const handleExportPDF = async e => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      // Validate required fields
      const missingFields = selectedTemplate.fields.filter(field => !formData[field]);
      if (missingFields.length > 0) {
        throw new Error(`Please fill in all required fields: ${missingFields.join(', ')}`);
      }
      // Make API call to generate contract
      const response = await fetch(`${config.apiUrl}/api/contracts/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template: selectedTemplate.title.toLowerCase().replace(/\s+/g, '_'),
          formData: formData,
        }),
        // Important for receiving PDF data
        responseType: 'blob',
      });
      if (!response.ok) {
        throw new Error('Failed to generate contract');
      }
      // Create a blob from the PDF data
      const blob = await response.blob();
      // Create a link to download the PDF
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute(
        'download',
        `${selectedTemplate.title.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.pdf`
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      setOpen(false);
      setFormData({});
    } catch (err) {
      setError(err.message || 'Error generating document');
      console.error('Error generating document:', err);
    } finally {
      setLoading(false);
    }
  };
  const handleFormChange = e => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };
  return (
    <Box>
      {/* Search and Categories */}
      <Box sx={{ mb: 4 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search templates..."
          value={searchQuery}
          onChange={handleSearch}
          sx={{ mb: 2 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
        <Tabs
          value={category}
          onChange={handleCategoryChange}
          variant="scrollable"
          scrollButtons="auto"
        >
          {categories.map((cat, index) => (
            <Tab key={index} label={cat} />
          ))}
        </Tabs>
      </Box>
      {/* Templates Grid */}
      <Grid container spacing={3}>
        {filteredTemplates.map((template, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {/* Icon will be added here */}
                </Box>
                <Typography variant="h6" sx={{ ml: 1 }}>
                  {template.title}
                </Typography>
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
                    onClick={() => handleGenerateClick(template)}
                    startIcon={<FileDownloadIcon />}
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
      {/* Contract Form Dialog */}
      <ContractForm
        open={open}
        onClose={() => setOpen(false)}
        onGenerate={handleExportPDF}
        template={selectedTemplate}
        loading={loading}
      />
    </Box>
  );
};
export default ContractTemplates;
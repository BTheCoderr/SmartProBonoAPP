import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Stack,
  Divider,
} from '@mui/material';
import { Save as SaveIcon, Preview as PreviewIcon } from '@mui/icons-material';
import ContractTemplateService from '../services/ContractTemplateService';

const ContractForm = ({ templateId, onSave, onPreview, onCancel }) => {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [contractName, setContractName] = useState('');

  const template = ContractTemplateService.getTemplate(templateId);
  
  if (!template) {
    return (
      <Alert severity="error">
        Template not found
      </Alert>
    );
  }

  const handleInputChange = (key, value) => {
    setFormData(prev => ({
      ...prev,
      [key]: value
    }));
    
    // Clear error when user starts typing
    if (errors[key]) {
      setErrors(prev => ({
        ...prev,
        [key]: null
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    let isValid = true;

    // Check required fields
    template.content.variables.forEach(variable => {
      if (variable.required && (!formData[variable.key] || formData[variable.key].trim() === '')) {
        newErrors[variable.key] = `${variable.label} is required`;
        isValid = false;
      }
    });

    // Check contract name
    if (!contractName.trim()) {
      newErrors.contractName = 'Contract name is required';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const savedContract = ContractTemplateService.saveContract(templateId, formData, contractName);
      onSave(savedContract);
    } catch (error) {
      console.error('Error saving contract:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = () => {
    if (!validateForm()) {
      return;
    }
    
    const contract = ContractTemplateService.generateContract(templateId, formData);
    onPreview(contract);
  };

  const renderInput = (variable) => {
    const value = formData[variable.key] || '';
    const error = errors[variable.key];

    switch (variable.type) {
      case 'select':
        return (
          <FormControl fullWidth error={!!error} required={variable.required}>
            <InputLabel>{variable.label}</InputLabel>
            <Select
              value={value}
              onChange={(e) => handleInputChange(variable.key, e.target.value)}
              label={variable.label}
            >
              {variable.options.map((option) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );
      
      case 'textarea':
        return (
          <TextField
            fullWidth
            multiline
            rows={4}
            label={variable.label}
            value={value}
            onChange={(e) => handleInputChange(variable.key, e.target.value)}
            error={!!error}
            helperText={error}
            required={variable.required}
            variant="outlined"
          />
        );
      
      case 'date':
        return (
          <TextField
            fullWidth
            type="date"
            label={variable.label}
            value={value}
            onChange={(e) => handleInputChange(variable.key, e.target.value)}
            error={!!error}
            helperText={error}
            required={variable.required}
            InputLabelProps={{ shrink: true }}
            variant="outlined"
          />
        );
      
      case 'number':
        return (
          <TextField
            fullWidth
            type="number"
            label={variable.label}
            value={value}
            onChange={(e) => handleInputChange(variable.key, e.target.value)}
            error={!!error}
            helperText={error}
            required={variable.required}
            variant="outlined"
          />
        );
      
      default:
        return (
          <TextField
            fullWidth
            label={variable.label}
            value={value}
            onChange={(e) => handleInputChange(variable.key, e.target.value)}
            error={!!error}
            helperText={error}
            required={variable.required}
            variant="outlined"
          />
        );
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          {template.title}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          {template.description}
        </Typography>

        <Divider sx={{ mb: 3 }} />

        {/* Contract Name */}
        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            label="Contract Name"
            value={contractName}
            onChange={(e) => setContractName(e.target.value)}
            error={!!errors.contractName}
            helperText={errors.contractName}
            required
            variant="outlined"
            placeholder="e.g., Employment Agreement - John Smith"
          />
        </Box>

        {/* Form Fields */}
        <Grid container spacing={3}>
          {template.content.variables.map((variable) => (
            <Grid item xs={12} sm={6} key={variable.key}>
              {renderInput(variable)}
            </Grid>
          ))}
        </Grid>

        {/* Action Buttons */}
        <Stack direction="row" spacing={2} sx={{ mt: 4, justifyContent: 'flex-end' }}>
          <Button
            variant="outlined"
            onClick={onCancel}
            sx={{
              borderColor: '#1565C0',
              color: '#1565C0',
              '&:hover': {
                borderColor: '#0D47A1',
                backgroundColor: 'rgba(21, 101, 192, 0.04)',
              },
            }}
          >
            Cancel
          </Button>
          
          <Button
            variant="outlined"
            startIcon={<PreviewIcon />}
            onClick={handlePreview}
            sx={{
              borderColor: '#1565C0',
              color: '#1565C0',
              '&:hover': {
                borderColor: '#0D47A1',
                backgroundColor: 'rgba(21, 101, 192, 0.04)',
              },
            }}
          >
            Preview
          </Button>
          
          <Button
            variant="contained"
            startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
            onClick={handleSave}
            disabled={loading}
            sx={{
              backgroundColor: '#1565C0',
              '&:hover': {
                backgroundColor: '#0D47A1',
              },
            }}
          >
            {loading ? 'Saving...' : 'Save Contract'}
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ContractForm;
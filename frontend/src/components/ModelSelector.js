import React from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  Paper,
  Tooltip,
  Chip
} from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import MemoryIcon from '@mui/icons-material/Memory';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SchoolIcon from '@mui/icons-material/School';
import PsychologyIcon from '@mui/icons-material/Psychology';
import DescriptionIcon from '@mui/icons-material/Description';

// Component for selecting different AI models
const ModelSelector = ({ currentModel, onChange, premium = false }) => {
  // Model data with capabilities and characteristics
  const models = [
    {
      id: 'llama',
      name: 'Llama 3.2 (3B)',
      icon: <SmartToyIcon />,
      description: 'Fast and efficient model for general legal advice',
      capabilities: ['General Legal Advice', 'Fast Responses', 'Conversational'],
      premium: false
    },
    {
      id: 'mistral',
      name: 'Mistral 7B',
      icon: <MemoryIcon />,
      description: 'Balanced model with good legal reasoning capabilities',
      capabilities: ['Clear Explanations', 'Legal Analysis', 'Detailed Responses'],
      premium: false
    },
    {
      id: 'qwen',
      name: 'Qwen 2.5 (0.5B)',
      icon: <PsychologyIcon />,
      description: 'Lightweight model optimized for quick responses',
      capabilities: ['Quick Responses', 'Efficient', 'Lightweight'],
      premium: false
    },
    {
      id: 'gemma',
      name: 'Gemma 2B',
      icon: <SchoolIcon />,
      description: 'Google\'s efficient model for legal guidance',
      capabilities: ['Efficient', 'Clear Language', 'Good Reasoning'],
      premium: false
    },
    {
      id: 'phi',
      name: 'Phi-3 Mini',
      icon: <DescriptionIcon />,
      description: 'Microsoft\'s compact model for legal assistance',
      capabilities: ['Compact', 'Fast', 'Accurate'],
      premium: false
    },
    {
      id: 'falcon',
      name: 'Falcon Legal Assistant',
      icon: <PsychologyIcon />,
      description: 'Focused on explaining complex legal concepts clearly',
      capabilities: ['Simple Explanations', 'Plain Language', 'User-Friendly'],
      premium: false
    },
    {
      id: 'document',
      name: 'Document Expert',
      icon: <DescriptionIcon />,
      description: 'Specialized in document analysis and drafting',
      capabilities: ['Document Generation', 'Contract Analysis', 'Form Filling'],
      premium: true
    }
  ];

  // Filter models based on premium status
  const availableModels = premium 
    ? models 
    : models.filter(model => !model.premium);

  const handleChange = (e) => {
    onChange(e.target.value);
  };

  return (
    <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
      <Typography variant="subtitle2" gutterBottom>
        AI Model Selection
      </Typography>
      <FormControl fullWidth size="small">
        <InputLabel id="model-select-label">Choose AI Model</InputLabel>
        <Select
          labelId="model-select-label"
          id="model-select"
          value={currentModel}
          label="Choose AI Model"
          onChange={handleChange}
          renderValue={(selected) => {
            const model = models.find(m => m.id === selected);
            return (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {model?.icon}
                <Typography variant="body2">{model?.name}</Typography>
                {model?.premium && (
                  <Chip 
                    label="Premium" 
                    size="small" 
                    color="secondary"
                    sx={{ height: 20, fontSize: '0.7rem' }}
                  />
                )}
              </Box>
            );
          }}
        >
          {availableModels.map((model) => (
            <MenuItem key={model.id} value={model.id}>
              <Tooltip title={model.description} placement="right">
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, width: '100%' }}>
                  <Box sx={{ mr: 1 }}>{model.icon}</Box>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="body2">{model.name}</Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                      {model.capabilities.map((capability, index) => (
                        <Chip 
                          key={index} 
                          label={capability} 
                          size="small"
                          variant="outlined"
                          sx={{ height: 20, fontSize: '0.7rem' }} 
                        />
                      ))}
                    </Box>
                  </Box>
                  {model.premium && (
                    <Chip 
                      label="Premium" 
                      size="small" 
                      color="secondary"
                      sx={{ height: 20, fontSize: '0.7rem' }}
                    />
                  )}
                </Box>
              </Tooltip>
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Paper>
  );
};

export default ModelSelector; 
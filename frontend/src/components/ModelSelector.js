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
      id: 'custom',
      name: 'SmartProBono Assistant',
      icon: <AutoAwesomeIcon />,
      description: 'Our custom-tuned legal assistant with improved capabilities',
      capabilities: ['General Legal Advice', 'Document Analysis', 'Citation'],
      premium: false
    },
    {
      id: 'mistral',
      name: 'Mistral AI',
      icon: <MemoryIcon />,
      description: 'Good general-purpose model for legal advice',
      capabilities: ['Clear Explanations', 'Fast Responses', 'Conversational'],
      premium: false
    },
    {
      id: 'llama',
      name: 'LlaMA Legal Advisor',
      icon: <SmartToyIcon />,
      description: 'Specialized in detailed legal analysis with references',
      capabilities: ['Legal References', 'Statute Citations', 'Thorough Explanations'],
      premium: true
    },
    {
      id: 'deepseek',
      name: 'DeepSeek Legal',
      icon: <SchoolIcon />,
      description: 'Research-oriented model with comprehensive legal knowledge',
      capabilities: ['Research', 'Case Law', 'Legal Procedures'],
      premium: true
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
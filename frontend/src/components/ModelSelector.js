import React from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Tooltip,
  Typography,
} from '@mui/material';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import PropTypes from 'prop-types';

const ModelSelector = ({ currentModel, onModelChange, isLoading }) => {
  const models = [
    {
      id: 'mistral',
      name: 'TinyLlama Chat',
      description: 'Best for general legal chat and Q&A',
      specialization: ['chat', 'legal_qa'],
    },
    {
      id: 'llama',
      name: 'GPT2 Legal',
      description: 'Specialized in document drafting and contracts',
      specialization: ['document_drafting', 'contract_generation'],
    },
    {
      id: 'falcon',
      name: 'Falcon 7B',
      description: 'Advanced legal analysis and interpretation',
      specialization: ['statute_interpretation', 'complex_analysis'],
    },
    {
      id: 'deepseek',
      name: 'BLOOM',
      description: 'Focused on legal research and rights analysis',
      specialization: ['legal_research', 'rights_research'],
    },
  ];

  return (
    <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
      <FormControl size="small" sx={{ minWidth: 200 }}>
        <InputLabel>AI Model</InputLabel>
        <Select
          value={currentModel || 'mistral'}
          onChange={e => onModelChange(e.target.value)}
          disabled={isLoading}
          label="AI Model"
        >
          {models.map(model => (
            <MenuItem key={model.id} value={model.id}>
              <Box>
                <Typography variant="body2">{model.name}</Typography>
                <Typography variant="caption" color="text.secondary">
                  {model.description}
                </Typography>
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Tooltip title="Current Model Specializations">
        <Box>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.5 }}>
            Specializations:
          </Typography>
          <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
            {models
              .find(m => m.id === (currentModel || 'mistral'))
              ?.specialization.map(spec => (
                <Chip
                  key={spec}
                  label={spec.replace('_', ' ')}
                  size="small"
                  color="primary"
                  variant="outlined"
                  icon={<AutoFixHighIcon />}
                />
              ))}
          </Box>
        </Box>
      </Tooltip>
    </Box>
  );
};


// Define PropTypes
ModelSelector.propTypes = {
  /** TODO: Add description */
  currentModel: PropTypes.any,
  /** TODO: Add description */
  onModelChange: PropTypes.any,
  /** TODO: Add description */
  isLoading: PropTypes.any,
};

export default ModelSelector;

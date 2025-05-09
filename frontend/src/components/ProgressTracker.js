import React from 'react';
import { Box, Typography, LinearProgress, Paper, Tooltip } from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';

/**
 * ProgressTracker - A reusable component for displaying form completion progress
 * 
 * @param {Object} props
 * @param {number} props.progress - The progress percentage (0-100)
 * @param {string|Date} [props.lastSaved] - Timestamp of when the form was last saved
 * @param {boolean} [props.showSaveIcon=true] - Whether to show the save icon beside the last saved date
 * @param {Object} [props.sx] - Additional MUI styling for the component
 */
const ProgressTracker = ({ progress, lastSaved, showSaveIcon = true, sx = {} }) => {
  // Calculate color based on progress
  const getProgressColor = (value) => {
    if (value < 33) return 'error.main';
    if (value < 66) return 'warning.main';
    return 'success.main';
  };

  // Format the last saved date
  const formatLastSaved = (timestamp) => {
    if (!timestamp) return null;
    try {
      const date = typeof timestamp === 'string' ? new Date(timestamp) : timestamp;
      return date.toLocaleString();
    } catch (error) {
      console.error('Error formatting date:', error);
      return null;
    }
  };

  const formattedLastSaved = formatLastSaved(lastSaved);

  return (
    <Paper 
      elevation={1} 
      sx={{ 
        p: 2, 
        mb: 3, 
        borderRadius: 2,
        backgroundColor: 'background.paper',
        ...sx
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography variant="body1" fontWeight="medium">
          Form Completion: {progress}%
        </Typography>
        
        {formattedLastSaved && (
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {showSaveIcon && (
              <Tooltip title="Autosaved">
                <SaveIcon fontSize="small" sx={{ mr: 0.5, color: 'text.secondary' }} />
              </Tooltip>
            )}
            <Typography variant="caption" color="text.secondary">
              Last saved: {formattedLastSaved}
            </Typography>
          </Box>
        )}
      </Box>
      
      <LinearProgress 
        variant="determinate" 
        value={progress} 
        sx={{ 
          height: 10, 
          borderRadius: 5,
          mb: 1,
          backgroundColor: 'grey.200',
          '& .MuiLinearProgress-bar': {
            backgroundColor: getProgressColor(progress)
          }
        }} 
      />
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="caption" color="text.secondary">
          Not Started
        </Typography>
        <Typography variant="caption" color="text.secondary">
          In Progress
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Complete
        </Typography>
      </Box>
    </Paper>
  );
};

export default ProgressTracker; 
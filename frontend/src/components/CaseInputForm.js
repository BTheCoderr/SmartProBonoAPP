import React, { useState } from 'react';
import { 
  TextField, 
  Select, 
  MenuItem, 
  Button, 
  FormControl, 
  InputLabel, 
  Box, 
  Typography,
  Paper
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';

const CaseInputForm = ({ onSubmit, loading = false }) => {
  const [text, setText] = useState('');
  const [jurisdiction, setJurisdiction] = useState('ri');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onSubmit({ text: text.trim(), jurisdiction });
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Describe Your Legal Issue
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          multiline
          rows={4}
          fullWidth
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Describe your legal situation... (e.g., 'I was charged with possession in Providence, RI')"
          variant="outlined"
          disabled={loading}
        />
        
        <FormControl fullWidth>
          <InputLabel>Jurisdiction</InputLabel>
          <Select
            value={jurisdiction}
            onChange={(e) => setJurisdiction(e.target.value)}
            label="Jurisdiction"
            disabled={loading}
          >
            <MenuItem value="ri">Rhode Island</MenuItem>
            <MenuItem value="ma">Massachusetts</MenuItem>
            <MenuItem value="fed">Federal</MenuItem>
          </Select>
        </FormControl>
        
        <Button
          type="submit"
          variant="contained"
          endIcon={<SendIcon />}
          disabled={loading || !text.trim()}
          sx={{ alignSelf: 'flex-start' }}
        >
          {loading ? 'Analyzing...' : 'Get Legal Analysis'}
        </Button>
      </Box>
    </Paper>
  );
};

export default CaseInputForm;

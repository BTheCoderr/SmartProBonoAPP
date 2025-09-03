import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Stack,
  Divider,
  Paper,
} from '@mui/material';
import { Edit as EditIcon, Download as DownloadIcon, Close as CloseIcon } from '@mui/icons-material';

const ContractPreview = ({ contract, onEdit, onDownload, onClose }) => {
  const formatContent = (content) => {
    // Split content into paragraphs and format
    const paragraphs = content.split('\n\n');
    return paragraphs.map((paragraph, index) => {
      if (paragraph.trim() === '') return null;
      
      // Check if it's a section header (all caps)
      if (paragraph.match(/^[A-Z\s\d]+$/)) {
        return (
          <Typography
            key={index}
            variant="h6"
            sx={{
              fontWeight: 700,
              mt: index > 0 ? 3 : 0,
              mb: 2,
              color: '#1565C0',
            }}
          >
            {paragraph}
          </Typography>
        );
      }
      
      // Check if it's a numbered item
      if (paragraph.match(/^\d+\./)) {
        return (
          <Typography
            key={index}
            variant="body1"
            sx={{
              mb: 1,
              ml: 2,
              lineHeight: 1.6,
            }}
          >
            {paragraph}
          </Typography>
        );
      }
      
      // Regular paragraph
      return (
        <Typography
          key={index}
          variant="body1"
          sx={{
            mb: 2,
            lineHeight: 1.6,
            textAlign: 'justify',
          }}
        >
          {paragraph}
        </Typography>
      );
    });
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Card>
        <CardContent>
          {/* Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, color: '#1565C0' }}>
              Contract Preview
            </Typography>
            <Button
              variant="outlined"
              startIcon={<CloseIcon />}
              onClick={onClose}
              sx={{
                borderColor: '#1565C0',
                color: '#1565C0',
                '&:hover': {
                  borderColor: '#0D47A1',
                  backgroundColor: 'rgba(21, 101, 192, 0.04)',
                },
              }}
            >
              Close
            </Button>
          </Box>

          <Divider sx={{ mb: 3 }} />

          {/* Contract Info */}
          <Box sx={{ mb: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              {contract.title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {contract.description}
            </Typography>
          </Box>

          {/* Contract Content */}
          <Paper sx={{ p: 3, backgroundColor: '#fafafa', border: '1px solid #e0e0e0' }}>
            <Box sx={{ fontFamily: 'monospace', fontSize: '0.9rem' }}>
              {formatContent(contract.generatedContent)}
            </Box>
          </Paper>

          {/* Action Buttons */}
          <Stack direction="row" spacing={2} sx={{ mt: 3, justifyContent: 'center' }}>
            <Button
              variant="outlined"
              startIcon={<EditIcon />}
              onClick={onEdit}
              sx={{
                borderColor: '#1565C0',
                color: '#1565C0',
                '&:hover': {
                  borderColor: '#0D47A1',
                  backgroundColor: 'rgba(21, 101, 192, 0.04)',
                },
              }}
            >
              Edit Contract
            </Button>
            
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={onDownload}
              sx={{
                backgroundColor: '#1565C0',
                '&:hover': {
                  backgroundColor: '#0D47A1',
                },
              }}
            >
              Download PDF
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ContractPreview;

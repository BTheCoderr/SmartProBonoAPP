import React from 'react';
import { Box, Grid, Card, CardActionArea, CardContent, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const options = [
  { label: 'Document Generation', path: '/documents' },
  { label: 'Legal Research', path: '/resources' },
  { label: 'Consultation', path: '/contact' },
  { label: 'Immigration', path: '/immigration' },
  { label: 'Expungement', path: '/expungement' },
  { label: 'Virtual Paralegal', path: '/virtual-paralegal' },
];

export default function LegalNeedsWizard() {
  const navigate = useNavigate();
  return (
    <Box sx={{ mb: 4, mt: 4 }}>
      <Typography variant="h5" gutterBottom align="center">
        What legal help do you need?
      </Typography>
      <Grid container spacing={2}>  
        {options.map((opt) => (
          <Grid item xs={12} sm={6} md={4} key={opt.label}>
            <Card>
              <CardActionArea onClick={() => navigate(opt.path)}>
                <CardContent>
                  <Typography variant="h6" align="center">
                    {opt.label}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

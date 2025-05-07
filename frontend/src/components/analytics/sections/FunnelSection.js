import React from 'react';
import { Grid, Paper, Typography } from '@mui/material';
import {
  FunnelChart, Funnel, ResponsiveContainer,
  Tooltip, LabelList
} from 'recharts';

export const FunnelSection = ({ funnelData }) => (
  <Grid item xs={12} md={6}>
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Conversion Funnel
      </Typography>
      <ResponsiveContainer width="100%" height={400}>
        <FunnelChart>
          <Tooltip />
          <Funnel
            data={funnelData}
            dataKey="value"
            nameKey="name"
            labelLine
          >
            <LabelList position="right" fill="#000" stroke="none" dataKey="name" />
          </Funnel>
        </FunnelChart>
      </ResponsiveContainer>
    </Paper>
  </Grid>
); 
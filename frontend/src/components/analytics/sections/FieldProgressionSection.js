import React from 'react';
import { Grid, Paper, Typography } from '@mui/material';
import {
  ResponsiveContainer, Sankey, SankeyNode, SankeyLink
} from 'recharts';

export const FieldProgressionSection = ({ fieldProgressionData }) => (
  <Grid item xs={12}>
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Field Progression Flow
      </Typography>
      <ResponsiveContainer width="100%" height={400}>
        <Sankey
          data={fieldProgressionData}
          node={<SankeyNode />}
          link={<SankeyLink />}
          nodePadding={50}
          margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
        />
      </ResponsiveContainer>
    </Paper>
  </Grid>
); 
import React from 'react';
import { Grid, Paper, Typography, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';

export const ConversionRatesTable = ({ conversionRates }) => (
  <Grid item xs={12} md={6}>
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Conversion Rates
      </Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Conversion Step</TableCell>
            <TableCell align="right">Rate</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>View to Start</TableCell>
            <TableCell align="right">{conversionRates.viewToStart}%</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Start to Interaction</TableCell>
            <TableCell align="right">{conversionRates.startToInteraction}%</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Interaction to Completion</TableCell>
            <TableCell align="right">{conversionRates.interactionToCompletion}%</TableCell>
          </TableRow>
          <TableRow>
            <TableCell><strong>Overall Conversion</strong></TableCell>
            <TableCell align="right"><strong>{conversionRates.overallConversion}%</strong></TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Paper>
  </Grid>
); 
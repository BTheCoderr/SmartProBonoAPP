import React, { useMemo } from 'react';
import {
  FunnelChart, Funnel, ResponsiveContainer,
  Tooltip, LabelList, Sankey, SankeyNode, SankeyLink
} from 'recharts';
import { Box, Grid, Paper, Typography } from '@mui/material';
import useRealTimeAnalytics from '../../hooks/useRealTimeAnalytics';
import { ConversionRatesTable } from './tables/ConversionRatesTable';
import { useFunnelData } from './hooks/useFunnelData';
import { useConversionRates } from './hooks/useConversionRates';
import { useFieldProgression } from './hooks/useFieldProgression';
import { FunnelSection } from './sections/FunnelSection';
import { FieldProgressionSection } from './sections/FieldProgressionSection';

const UserSessionAnalytics = ({ formType }) => {
  const { realTimeData } = useRealTimeAnalytics(formType);
  const funnelData = useFunnelData(realTimeData);
  const conversionRates = useConversionRates(realTimeData);
  const fieldProgressionData = useFieldProgression(realTimeData.fieldInteractions);

  return (
    <Box p={3}>
      <Grid container spacing={3}>
        <FunnelSection funnelData={funnelData} />
        <ConversionRatesTable conversionRates={conversionRates} />
        <FieldProgressionSection fieldProgressionData={fieldProgressionData} />
      </Grid>
    </Box>
  );
};

export default UserSessionAnalytics; 
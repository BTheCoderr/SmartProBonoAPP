import { useMemo } from 'react';

export const useConversionRates = (realTimeData) => {
  const { views, starts, completed, fieldInteractions } = realTimeData;

  return useMemo(() => {
    const calculateRate = (numerator, denominator) => 
      denominator ? Math.round((numerator / denominator) * 100) : 0;

    return {
      viewToStart: calculateRate(starts, views),
      startToInteraction: calculateRate(Object.keys(fieldInteractions || {}).length, starts),
      interactionToCompletion: calculateRate(completed, Object.keys(fieldInteractions || {}).length),
      overallConversion: calculateRate(completed, views)
    };
  }, [views, starts, fieldInteractions, completed]);
}; 
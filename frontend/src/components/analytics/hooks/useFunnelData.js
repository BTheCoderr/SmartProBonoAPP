import { useMemo } from 'react';

export const useFunnelData = (realTimeData) => {
  const { views, starts, completed, fieldInteractions } = realTimeData;

  return useMemo(() => [
    {
      value: views || 0,
      name: 'Views',
      fill: '#8884d8'
    },
    {
      value: starts || 0,
      name: 'Started',
      fill: '#83a6ed'
    },
    {
      value: Object.keys(fieldInteractions || {}).length,
      name: 'Interacted',
      fill: '#8dd1e1'
    },
    {
      value: completed || 0,
      name: 'Completed',
      fill: '#82ca9d'
    }
  ], [views, starts, fieldInteractions, completed]);
}; 
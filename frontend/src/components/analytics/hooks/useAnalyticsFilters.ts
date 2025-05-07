import { useState, useCallback } from 'react';
import { AnalyticsFilters, DateRange } from '../../../types/analytics';

export const useAnalyticsFilters = (initialFilters?: Partial<AnalyticsFilters>) => {
  const [filters, setFilters] = useState<AnalyticsFilters>({
    dateRange: {
      startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // Last 7 days
      endDate: new Date()
    },
    ...initialFilters
  });

  const setDateRange = useCallback((dateRange: DateRange) => {
    setFilters(prev => ({ ...prev, dateRange }));
  }, []);

  const setFormType = useCallback((formType: string) => {
    setFilters(prev => ({ ...prev, formType }));
  }, []);

  const setUserSegment = useCallback((userSegment: string) => {
    setFilters(prev => ({ ...prev, userSegment }));
  }, []);

  const setCustomMetrics = useCallback((customMetrics: string[]) => {
    setFilters(prev => ({ ...prev, customMetrics }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      dateRange: {
        startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
        endDate: new Date()
      }
    });
  }, []);

  return {
    filters,
    setDateRange,
    setFormType,
    setUserSegment,
    setCustomMetrics,
    resetFilters
  };
}; 
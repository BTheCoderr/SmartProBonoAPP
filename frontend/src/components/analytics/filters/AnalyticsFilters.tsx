import React from 'react';
import {
  Paper,
  Grid,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { AnalyticsFilters as AnalyticsFiltersType } from '../../../types/analytics';

interface AnalyticsFiltersProps {
  filters: AnalyticsFiltersType;
  onDateRangeChange: (startDate: Date, endDate: Date) => void;
  onFormTypeChange: (formType: string) => void;
  onUserSegmentChange: (segment: string) => void;
  onCustomMetricsChange: (metrics: string[]) => void;
  onReset: () => void;
  availableFormTypes: string[];
  availableSegments: string[];
  availableMetrics: string[];
}

export const AnalyticsFilters: React.FC<AnalyticsFiltersProps> = ({
  filters,
  onDateRangeChange,
  onFormTypeChange,
  onUserSegmentChange,
  onCustomMetricsChange,
  onReset,
  availableFormTypes,
  availableSegments,
  availableMetrics
}) => {
  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} md={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Box display="flex" gap={2}>
              <DatePicker
                label="Start Date"
                value={filters.dateRange?.startDate}
                onChange={(date) => {
                  if (date && filters.dateRange?.endDate) {
                    onDateRangeChange(date, filters.dateRange.endDate);
                  }
                }}
              />
              <DatePicker
                label="End Date"
                value={filters.dateRange?.endDate}
                onChange={(date) => {
                  if (date && filters.dateRange?.startDate) {
                    onDateRangeChange(filters.dateRange.startDate, date);
                  }
                }}
              />
            </Box>
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>Form Type</InputLabel>
            <Select
              value={filters.formType || ''}
              onChange={(e) => onFormTypeChange(e.target.value)}
            >
              <MenuItem value="">All Forms</MenuItem>
              {availableFormTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>User Segment</InputLabel>
            <Select
              value={filters.userSegment || ''}
              onChange={(e) => onUserSegmentChange(e.target.value)}
            >
              <MenuItem value="">All Users</MenuItem>
              {availableSegments.map((segment) => (
                <MenuItem key={segment} value={segment}>
                  {segment}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Custom Metrics</InputLabel>
            <Select
              multiple
              value={filters.customMetrics || []}
              onChange={(e) => onCustomMetricsChange(e.target.value as string[])}
            >
              {availableMetrics.map((metric) => (
                <MenuItem key={metric} value={metric}>
                  {metric}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <Box display="flex" justifyContent="flex-end">
            <Button onClick={onReset} sx={{ mr: 1 }}>
              Reset Filters
            </Button>
            <Button variant="contained" color="primary">
              Apply Filters
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
}; 
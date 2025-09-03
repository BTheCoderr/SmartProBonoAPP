/**
 * Color Audit Utility
 * Checks all pages and components for consistent brand color usage
 */

import { designTokens } from '../design-system';

// Brand colors that should be used consistently
export const brandColors = {
  primary: '#0F3D5E', // Navy
  secondary: '#1FB6A6', // Teal
  primaryLight: '#627d98',
  secondaryLight: '#2dd4bf',
  primaryDark: '#0F3D5E',
  secondaryDark: '#0f766e',
};

// Common color issues to check for
export const colorIssues = {
  oldBlue: ['#1565C0', '#42A5F5', '#0D47A1', '#3b82f6', '#2563eb', '#1d4ed8', '#1e40af'],
  oldTeal: ['#14B8A6', '#5EEAD4', '#0F766E'],
  genericColors: ['#1976d2', '#2196f3', '#21cbf3', '#00bcd4'],
};

// Pages to audit
export const pagesToAudit = [
  '/',
  '/dashboard',
  '/test',
  '/scan-document',
  '/documents',
  '/services',
  '/about',
  '/contact',
  '/login',
  '/register',
  '/admin',
  '/lawyer-dashboard',
  '/analytics',
  '/immigration',
  '/resources',
  '/rights',
  '/procedures',
  '/forms',
  '/contracts',
  '/virtual-paralegal',
  '/expert-help',
  '/legal-templates',
  '/signature',
  '/templates',
  '/status',
  '/help',
  '/faq',
  '/blog',
  '/team',
  '/careers',
  '/press',
  '/partners',
  '/mission',
  '/glossary',
  '/accessibility',
  '/sitemap',
  '/bug-report',
  '/feature-request',
];

// Components to audit
export const componentsToAudit = [
  'Header',
  'Footer',
  'Navigation',
  'Logo',
  'Button',
  'Card',
  'Paper',
  'TextField',
  'Chip',
  'Alert',
  'Dialog',
  'Menu',
  'Tabs',
  'Stepper',
  'Accordion',
  'List',
  'Table',
  'Avatar',
  'Badge',
  'Progress',
  'Snackbar',
  'Tooltip',
  'IconButton',
  'Fab',
  'AppBar',
  'Drawer',
  'Breadcrumbs',
  'Pagination',
  'Rating',
  'Slider',
  'Switch',
  'Checkbox',
  'Radio',
  'Select',
  'FormControl',
  'InputLabel',
  'OutlinedInput',
  'InputAdornment',
  'FormHelperText',
  'FormLabel',
  'FormGroup',
  'FormControlLabel',
  'RadioGroup',
  'CheckboxGroup',
  'Autocomplete',
  'DatePicker',
  'TimePicker',
  'DateTimePicker',
  'StaticDatePicker',
  'DesktopDatePicker',
  'MobileDatePicker',
  'CalendarPicker',
  'MonthPicker',
  'YearPicker',
  'ClockPicker',
  'Timeline',
  'TreeView',
  'DataGrid',
  'XGrid',
  'DateRangePicker',
  'DateRangePickerDay',
  'PickersDay',
  'CalendarPickerSkeleton',
  'MonthPickerSkeleton',
  'YearPickerSkeleton',
  'ClockPickerSkeleton',
  'DateRangePickerSkeleton',
  'PickersDaySkeleton',
  'CalendarPickerSkeleton',
  'MonthPickerSkeleton',
  'YearPickerSkeleton',
  'ClockPickerSkeleton',
  'DateRangePickerSkeleton',
  'PickersDaySkeleton',
];

// Color audit functions
export const auditColors = {
  // Check if a color matches brand colors
  isBrandColor: (color) => {
    const normalizedColor = color.toLowerCase().replace(/\s/g, '');
    return Object.values(brandColors).some(brandColor => 
      brandColor.toLowerCase() === normalizedColor
    );
  },

  // Check if a color is an old/incorrect color
  isOldColor: (color) => {
    const normalizedColor = color.toLowerCase().replace(/\s/g, '');
    return Object.values(colorIssues).flat().some(oldColor => 
      oldColor.toLowerCase() === normalizedColor
    );
  },

  // Get color recommendations
  getColorRecommendation: (color) => {
    const normalizedColor = color.toLowerCase().replace(/\s/g, '');
    
    // Map old colors to new brand colors
    const colorMap = {
      '#1565c0': brandColors.primary,
      '#42a5f5': brandColors.primaryLight,
      '#0d47a1': brandColors.primaryDark,
      '#3b82f6': brandColors.primary,
      '#2563eb': brandColors.primary,
      '#1d4ed8': brandColors.primary,
      '#1e40af': brandColors.primary,
      '#14b8a6': brandColors.secondary,
      '#5eead4': brandColors.secondaryLight,
      '#0f766e': brandColors.secondaryDark,
      '#1976d2': brandColors.primary,
      '#2196f3': brandColors.primary,
      '#21cbf3': brandColors.secondary,
      '#00bcd4': brandColors.secondary,
    };

    return colorMap[normalizedColor] || null;
  },

  // Generate color audit report
  generateReport: (auditResults) => {
    const report = {
      summary: {
        totalPages: auditResults.length,
        pagesWithIssues: auditResults.filter(result => result.issues.length > 0).length,
        totalIssues: auditResults.reduce((sum, result) => sum + result.issues.length, 0),
      },
      pages: auditResults,
      recommendations: [],
    };

    // Generate recommendations
    const allIssues = auditResults.flatMap(result => result.issues);
    const colorFrequency = {};
    
    allIssues.forEach(issue => {
      if (issue.type === 'oldColor') {
        colorFrequency[issue.color] = (colorFrequency[issue.color] || 0) + 1;
      }
    });

    Object.entries(colorFrequency).forEach(([color, count]) => {
      const recommendation = auditColors.getColorRecommendation(color);
      if (recommendation) {
        report.recommendations.push({
          oldColor: color,
          newColor: recommendation,
          occurrences: count,
          priority: count > 5 ? 'high' : count > 2 ? 'medium' : 'low',
        });
      }
    });

    return report;
  },
};

// Utility to check component colors
export const checkComponentColors = (component) => {
  const issues = [];
  
  // This would be used in a browser environment to check actual computed styles
  // For now, it's a placeholder for the audit logic
  
  return issues;
};

// Export default audit configuration
export default {
  brandColors,
  colorIssues,
  pagesToAudit,
  componentsToAudit,
  auditColors,
  checkComponentColors,
};

export interface RealTimeData {
  views: number;
  starts: number;
  completed: number;
  fieldInteractions: Record<string, number>;
  formData?: Record<string, any>;
  averageCompletionTime: number;
  averageSessionDuration: number;
  fieldErrors: Record<string, number>;
  recentSessions: SessionData[];
  recentBehavior: UserBehavior[];
}

export interface SessionData {
  formType: string;
  startTime: number;
  endTime: number;
  duration: number;
  interactions: FieldInteraction[];
  completedFields: string[];
  completionRate: number;
}

export interface FieldInteraction {
  fieldName: string;
  timestamp: number;
  isValid: boolean;
  value?: number;
}

export interface UserBehavior {
  timestamp: number;
  eventType: 'view' | 'start' | 'completion' | 'field_interaction';
  data: Record<string, any>;
  sessionDuration: number;
}

export interface FunnelDataPoint {
  value: number;
  name: string;
  fill: string;
}

export interface ConversionRates {
  viewToStart: number;
  startToInteraction: number;
  interactionToCompletion: number;
  overallConversion: number;
}

export interface FieldProgressionData {
  nodes: Array<{
    name: string;
    value: number;
  }>;
  links: Array<{
    source: string;
    target: string;
    value: number;
  }>;
}

export interface DateRange {
  startDate: Date;
  endDate: Date;
}

export interface AnalyticsFilters {
  dateRange?: DateRange;
  formType?: string;
  userSegment?: string;
  customMetrics?: string[];
}

export interface ComparativeAnalytics {
  current: RealTimeData;
  previous: RealTimeData;
  percentageChange: {
    views: number;
    starts: number;
    completed: number;
    averageCompletionTime: number;
  };
} 
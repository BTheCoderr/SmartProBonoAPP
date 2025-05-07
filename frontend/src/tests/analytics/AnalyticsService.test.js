import AnalyticsService from '../../services/AnalyticsService';
import ApiService from '../../services/ApiService';
import WebSocketService from '../../services/WebSocketService';

// Mock dependencies
jest.mock('../../services/ApiService');
jest.mock('../../services/WebSocketService');

describe('AnalyticsService', () => {
  const mockFormType = 'test_form';
  const mockTimestamp = '2024-03-21T12:00:00.000Z';

  beforeEach(() => {
    // Reset all mocks
    jest.clearAllMocks();
    
    // Mock Date.now and toISOString
    jest.spyOn(Date.prototype, 'toISOString').mockReturnValue(mockTimestamp);
    jest.spyOn(Date, 'now').mockReturnValue(new Date(mockTimestamp).getTime());
    
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(),
        setItem: jest.fn(),
        removeItem: jest.fn()
      },
      writable: true
    });
  });

  describe('trackFormView', () => {
    it('should track form view and emit websocket event', async () => {
      await AnalyticsService.trackFormView(mockFormType);

      expect(ApiService.post).toHaveBeenCalledWith('/api/analytics/form-view', {
        formType: mockFormType,
        timestamp: mockTimestamp
      });

      expect(WebSocketService.emit).toHaveBeenCalledWith('form_view', {
        formType: mockFormType,
        timestamp: mockTimestamp
      });
    });
  });

  describe('trackFormStart', () => {
    it('should track form start with device info', async () => {
      const mockScreenSize = { width: 1920, height: 1080 };
      Object.defineProperty(window, 'innerWidth', { value: mockScreenSize.width });
      Object.defineProperty(window, 'innerHeight', { value: mockScreenSize.height });

      await AnalyticsService.trackFormStart(mockFormType);

      expect(ApiService.post).toHaveBeenCalledWith('/api/analytics/form-start', {
        formType: mockFormType,
        timestamp: mockTimestamp,
        userAgent: navigator.userAgent,
        screenSize: mockScreenSize
      });

      expect(WebSocketService.emit).toHaveBeenCalledWith('form_start', expect.any(Object));
    });
  });

  describe('trackFormCompletion', () => {
    it('should track form completion with metrics', async () => {
      const mockCompletionTime = 5000;
      const mockFormMetrics = {
        fieldCount: 5,
        filledFields: 3,
        lastModified: mockTimestamp
      };

      jest.spyOn(AnalyticsService, 'getFormMetrics').mockReturnValue(mockFormMetrics);

      await AnalyticsService.trackFormCompletion(mockFormType, mockCompletionTime);

      expect(ApiService.post).toHaveBeenCalledWith('/api/analytics/form-completion', {
        formType: mockFormType,
        completionTime: mockCompletionTime,
        timestamp: mockTimestamp,
        formData: mockFormMetrics
      });
    });
  });

  describe('trackFormAbandonment', () => {
    it('should track form abandonment with timing data', async () => {
      const mockLastStep = 2;
      const mockCompletionPercentage = 60;
      const mockTimeSpent = 3000;
      const mockLastInteraction = {
        fieldName: 'test_field',
        timestamp: mockTimestamp
      };

      jest.spyOn(AnalyticsService, 'getTimeSpent').mockReturnValue(mockTimeSpent);
      jest.spyOn(AnalyticsService, 'getLastInteraction').mockReturnValue(mockLastInteraction);

      await AnalyticsService.trackFormAbandonment(
        mockFormType,
        mockLastStep,
        mockCompletionPercentage
      );

      expect(ApiService.post).toHaveBeenCalledWith('/api/analytics/form-abandonment', {
        formType: mockFormType,
        lastStep: mockLastStep,
        completionPercentage: mockCompletionPercentage,
        timestamp: mockTimestamp,
        timeSpent: mockTimeSpent,
        lastInteraction: mockLastInteraction
      });
    });
  });

  describe('trackFieldInteraction', () => {
    it('should track field interaction with validation', async () => {
      const mockFieldName = 'test_field';
      const mockValue = 'test value';
      const mockInteractionType = 'change';

      await AnalyticsService.trackFieldInteraction(
        mockFormType,
        mockFieldName,
        mockValue,
        mockInteractionType
      );

      expect(ApiService.post).toHaveBeenCalledWith('/api/analytics/field-interaction', {
        formType: mockFormType,
        fieldName: mockFieldName,
        interactionType: mockInteractionType,
        timestamp: mockTimestamp,
        valueLength: mockValue.length,
        isValid: true
      });
    });
  });

  describe('getFormAnalytics', () => {
    it('should fetch form analytics data', async () => {
      const mockAnalytics = {
        completionRate: 75,
        averageTime: 300,
        errorRate: 5
      };

      ApiService.get.mockResolvedValueOnce({ data: mockAnalytics });

      const result = await AnalyticsService.getFormAnalytics(mockFormType);

      expect(ApiService.get).toHaveBeenCalledWith(`/api/analytics/forms/${mockFormType}`);
      expect(result).toEqual(mockAnalytics);
    });
  });

  describe('helper methods', () => {
    describe('getFormMetrics', () => {
      it('should calculate form metrics from draft data', () => {
        const mockDraft = {
          values: {
            field1: 'value1',
            field2: '',
            field3: null,
            field4: 'value4'
          },
          timestamp: mockTimestamp
        };

        window.localStorage.getItem.mockReturnValueOnce(JSON.stringify(mockDraft));

        const metrics = AnalyticsService.getFormMetrics(mockFormType);

        expect(metrics).toEqual({
          fieldCount: 4,
          filledFields: 2,
          lastModified: mockTimestamp
        });
      });
    });

    describe('validateField', () => {
      it('should validate field values correctly', () => {
        expect(AnalyticsService.validateField('test', 'value')).toBe(true);
        expect(AnalyticsService.validateField('test', '')).toBe(false);
        expect(AnalyticsService.validateField('test', null)).toBe(false);
        expect(AnalyticsService.validateField('test', undefined)).toBe(false);
      });
    });
  });
}); 
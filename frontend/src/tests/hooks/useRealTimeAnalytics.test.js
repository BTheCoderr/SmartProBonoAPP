import { renderHook, act } from '@testing-library/react-hooks';
import useRealTimeAnalytics from '../../hooks/useRealTimeAnalytics';
import WebSocketService from '../../services/WebSocketService';
import AnalyticsService from '../../services/AnalyticsService';

// Mock dependencies
jest.mock('../../services/WebSocketService');
jest.mock('../../services/AnalyticsService');

describe('useRealTimeAnalytics', () => {
  const mockFormType = 'test_form';
  
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock initial analytics data
    AnalyticsService.getFormAnalytics.mockResolvedValue({
      averageCompletionTime: 300,
      errorRates: { validation: 5, submission: 2 }
    });
    
    AnalyticsService.getFieldCompletionRates.mockResolvedValue({
      field1: 80,
      field2: 60
    });
    
    // Mock WebSocket methods
    WebSocketService.connect.mockImplementation(() => {});
    WebSocketService.disconnect.mockImplementation(() => {});
    WebSocketService.subscribe.mockImplementation(() => jest.fn());
  });

  it('should initialize with default values', () => {
    const { result } = renderHook(() => useRealTimeAnalytics(mockFormType));

    expect(result.current.realTimeData).toEqual({
      activeUsers: 0,
      recentSubmissions: [],
      fieldCompletionRates: {},
      errorRates: {},
      averageCompletionTime: null
    });
    
    expect(result.current.isConnected).toBe(false);
  });

  it('should connect to WebSocket and load initial data', async () => {
    const { result, waitForNextUpdate } = renderHook(() => 
      useRealTimeAnalytics(mockFormType)
    );

    // Wait for initial data load
    await waitForNextUpdate();

    expect(WebSocketService.connect).toHaveBeenCalled();
    expect(result.current.isConnected).toBe(true);
    
    expect(AnalyticsService.getFormAnalytics).toHaveBeenCalledWith(mockFormType);
    expect(AnalyticsService.getFieldCompletionRates).toHaveBeenCalledWith(mockFormType);
    
    expect(result.current.realTimeData).toMatchObject({
      fieldCompletionRates: {
        field1: 80,
        field2: 60
      },
      errorRates: {
        validation: 5,
        submission: 2
      },
      averageCompletionTime: 300
    });
  });

  it('should handle analytics updates', async () => {
    const { result, waitForNextUpdate } = renderHook(() => 
      useRealTimeAnalytics(mockFormType)
    );

    await waitForNextUpdate();

    // Simulate analytics update
    const mockUpdate = {
      formType: mockFormType,
      metrics: {
        activeUsers: 5,
        averageCompletionTime: 250
      }
    };

    // Get the callback function that was registered
    const updateCallback = WebSocketService.subscribe.mock.calls.find(
      call => call[0] === 'analytics_update'
    )[1];

    // Call the callback with mock data
    act(() => {
      updateCallback(mockUpdate);
    });

    expect(result.current.realTimeData).toMatchObject({
      activeUsers: 5,
      averageCompletionTime: 250
    });
  });

  it('should handle form activity updates', async () => {
    const { result, waitForNextUpdate } = renderHook(() => 
      useRealTimeAnalytics(mockFormType)
    );

    await waitForNextUpdate();

    // Simulate form activity
    const mockActivity = {
      formType: mockFormType,
      activeUsers: 3,
      submission: {
        id: 'test-submission',
        timestamp: new Date().toISOString()
      }
    };

    // Get the callback function that was registered
    const activityCallback = WebSocketService.subscribe.mock.calls.find(
      call => call[0] === 'form_activity'
    )[1];

    // Call the callback with mock data
    act(() => {
      activityCallback(mockActivity);
    });

    expect(result.current.realTimeData.activeUsers).toBe(3);
    expect(result.current.realTimeData.recentSubmissions).toHaveLength(1);
    expect(result.current.realTimeData.recentSubmissions[0]).toEqual(mockActivity.submission);
  });

  it('should cleanup on unmount', () => {
    const { unmount } = renderHook(() => useRealTimeAnalytics(mockFormType));

    // Unmount the hook
    unmount();

    expect(WebSocketService.disconnect).toHaveBeenCalled();
  });

  it('should refresh analytics data', async () => {
    const mockNewAnalytics = {
      averageCompletionTime: 280,
      errorRates: { validation: 4, submission: 1 }
    };

    AnalyticsService.getFormAnalytics.mockResolvedValueOnce(mockNewAnalytics);

    const { result, waitForNextUpdate } = renderHook(() => 
      useRealTimeAnalytics(mockFormType)
    );

    await waitForNextUpdate();

    // Call refresh function
    await act(async () => {
      await result.current.refreshAnalytics();
    });

    expect(AnalyticsService.getFormAnalytics).toHaveBeenCalledTimes(2);
    expect(result.current.realTimeData).toMatchObject(mockNewAnalytics);
  });

  it('should ignore updates for different form types', async () => {
    const { result, waitForNextUpdate } = renderHook(() => 
      useRealTimeAnalytics(mockFormType)
    );

    await waitForNextUpdate();

    const initialData = { ...result.current.realTimeData };

    // Simulate update for different form type
    const mockUpdate = {
      formType: 'different_form',
      metrics: {
        activeUsers: 10,
        averageCompletionTime: 500
      }
    };

    // Get and call the analytics update callback
    const updateCallback = WebSocketService.subscribe.mock.calls.find(
      call => call[0] === 'analytics_update'
    )[1];

    act(() => {
      updateCallback(mockUpdate);
    });

    expect(result.current.realTimeData).toEqual(initialData);
  });
}); 
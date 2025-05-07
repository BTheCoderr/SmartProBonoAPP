import { ExportService } from '../../services/export.service';
import { AnalyticsController } from '../../controllers/analytics.controller';
import { Request, Response } from 'express';
import { mock, MockProxy } from 'jest-mock-extended';

describe('Analytics Export', () => {
  let exportService: ExportService;
  let controller: AnalyticsController;
  let req: MockProxy<Request>;
  let res: MockProxy<Response>;

  const mockAnalyticsData = {
    views: 100,
    starts: 80,
    completed: 60,
    fieldInteractions: {
      'field1': 75,
      'field2': 65
    }
  };

  beforeEach(() => {
    exportService = new ExportService();
    controller = new AnalyticsController();
    req = mock<Request>();
    res = mock<Response>();
    res.status.mockReturnThis();
    res.json.mockReturnThis();
    res.send.mockReturnThis();
  });

  describe('ExportService', () => {
    it('should export data to CSV format', async () => {
      const result = await exportService.exportData(mockAnalyticsData, 'csv');
      expect(result).toContain('views,starts,completed');
      expect(result).toContain('100,80,60');
    });

    it('should export data to JSON format', async () => {
      const result = await exportService.exportData(mockAnalyticsData, 'json');
      const parsed = JSON.parse(result as string);
      expect(parsed).toEqual(mockAnalyticsData);
    });

    it('should export data to Excel format', async () => {
      const result = await exportService.exportData(mockAnalyticsData, 'excel');
      expect(Buffer.isBuffer(result)).toBeTruthy();
    });

    it('should throw error for unsupported format', async () => {
      await expect(exportService.exportData(mockAnalyticsData, 'pdf')).rejects.toThrow('Unsupported export format');
    });
  });

  describe('AnalyticsController', () => {
    it('should handle export request with valid parameters', async () => {
      req.body = {
        formType: 'test_form',
        format: 'csv',
        startDate: '2024-01-01',
        endDate: '2024-01-31'
      };

      await controller.exportData(req, res);

      expect(res.setHeader).toHaveBeenCalledWith('Content-Type', 'text/csv');
      expect(res.setHeader).toHaveBeenCalledWith(
        'Content-Disposition',
        expect.stringContaining('analytics_test_form')
      );
      expect(res.send).toHaveBeenCalled();
    });

    it('should handle missing parameters', async () => {
      req.body = {
        formType: 'test_form'
      };

      await controller.exportData(req, res);

      expect(res.status).toHaveBeenCalledWith(400);
      expect(res.json).toHaveBeenCalledWith({
        error: 'Missing required parameters'
      });
    });

    it('should handle rate limiting', async () => {
      // Make multiple requests to trigger rate limit
      for (let i = 0; i < 6; i++) {
        req.body = {
          formType: 'test_form',
          format: 'csv',
          startDate: '2024-01-01',
          endDate: '2024-01-31'
        };
        req.ip = '127.0.0.1';

        await controller.exportData(req, res);
      }

      expect(res.status).toHaveBeenCalledWith(429);
      expect(res.json).toHaveBeenCalledWith(
        expect.objectContaining({
          error: expect.stringContaining('Too many export requests')
        })
      );
    });
  });
}); 
import { Request, Response } from 'express';
import { AnalyticsService } from '../services/analytics.service';
import { ExportService } from '../services/export.service';
import { RateLimiter } from '../middleware/rateLimiter';

const analyticsService = new AnalyticsService();
const exportService = new ExportService();
const exportRateLimiter = new RateLimiter({
  windowMs: 60 * 1000, // 1 minute
  maxRequests: 5 // 5 requests per minute
});

export class AnalyticsController {
  async exportData(req: Request, res: Response) {
    try {
      // Apply rate limiting
      const rateLimitResult = await exportRateLimiter.checkLimit(req.ip);
      if (!rateLimitResult.allowed) {
        return res.status(429).json({
          error: 'Too many export requests. Please try again later.',
          retryAfter: rateLimitResult.retryAfter
        });
      }

      const { formType, format, startDate, endDate } = req.body;

      // Validate input
      if (!formType || !format || !startDate || !endDate) {
        return res.status(400).json({
          error: 'Missing required parameters'
        });
      }

      // Get analytics data
      const data = await analyticsService.getAnalyticsData(formType, {
        startDate: new Date(startDate),
        endDate: new Date(endDate)
      });

      // Export data in requested format
      const exportedData = await exportService.exportData(data, format);

      // Set appropriate headers
      res.setHeader('Content-Type', exportService.getContentType(format));
      res.setHeader(
        'Content-Disposition',
        `attachment; filename=analytics_${formType}_${new Date().toISOString()}.${format}`
      );

      res.send(exportedData);
    } catch (error) {
      console.error('Export error:', error);
      res.status(500).json({
        error: 'Failed to export analytics data'
      });
    }
  }

  // Other controller methods...
} 
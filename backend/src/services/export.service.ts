import { Parser } from 'json2csv';
import * as XLSX from 'xlsx';
import * as PDFDocument from 'pdfkit';
import { Readable } from 'stream';

export type ExportFormat = 'csv' | 'json' | 'excel' | 'pdf' | 'xml';

interface ExportOptions {
  format: ExportFormat;
  template?: string;
  filters?: Record<string, any>;
  compression?: boolean;
}

export class ExportService {
  async exportData(data: any, options: ExportOptions | ExportFormat): Promise<Buffer | string> {
    const exportOptions: ExportOptions = typeof options === 'string' ? { format: options } : options;

    switch (exportOptions.format) {
      case 'csv':
        return this.exportToCsv(data, exportOptions);
      case 'json':
        return this.exportToJson(data, exportOptions);
      case 'excel':
        return this.exportToExcel(data, exportOptions);
      case 'pdf':
        return this.exportToPdf(data, exportOptions);
      case 'xml':
        return this.exportToXml(data, exportOptions);
      default:
        throw new Error('Unsupported export format');
    }
  }

  private async exportToCsv(data: any, options: ExportOptions): Promise<string> {
    try {
      const parser = new Parser({
        flatten: true,
        includeEmptyRows: false
      });
      const csv = parser.parse(data);
      return options.compression ? await this.compressData(csv) : csv;
    } catch (error) {
      console.error('CSV export error:', error);
      throw new Error('Failed to export data to CSV');
    }
  }

  private async exportToJson(data: any, options: ExportOptions): Promise<string> {
    try {
      const json = JSON.stringify(data, null, 2);
      return options.compression ? await this.compressData(json) : json;
    } catch (error) {
      console.error('JSON export error:', error);
      throw new Error('Failed to export data to JSON');
    }
  }

  private async exportToExcel(data: any, options: ExportOptions): Promise<Buffer> {
    try {
      const workbook = XLSX.utils.book_new();
      
      if (Array.isArray(data)) {
        // Single sheet
        const worksheet = XLSX.utils.json_to_sheet(data);
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Analytics Data');
      } else {
        // Multiple sheets
        Object.entries(data).forEach(([sheetName, sheetData]) => {
          const worksheet = XLSX.utils.json_to_sheet(sheetData as any[]);
          XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
        });
      }

      const buffer = XLSX.write(workbook, { type: 'buffer', bookType: 'xlsx' });
      return options.compression ? await this.compressBuffer(buffer) : buffer;
    } catch (error) {
      console.error('Excel export error:', error);
      throw new Error('Failed to export data to Excel');
    }
  }

  private async exportToPdf(data: any, options: ExportOptions): Promise<Buffer> {
    return new Promise((resolve, reject) => {
      try {
        const doc = new PDFDocument();
        const chunks: Buffer[] = [];

        doc.on('data', chunk => chunks.push(chunk));
        doc.on('end', () => {
          const buffer = Buffer.concat(chunks);
          resolve(options.compression ? this.compressBuffer(buffer) : buffer);
        });

        // Add title
        doc.fontSize(16).text('Analytics Report', { align: 'center' });
        doc.moveDown();

        // Add data
        Object.entries(data).forEach(([key, value]) => {
          doc.fontSize(12).text(`${key}:`, { continued: true });
          doc.text(` ${JSON.stringify(value)}`);
          doc.moveDown();
        });

        doc.end();
      } catch (error) {
        console.error('PDF export error:', error);
        reject(new Error('Failed to export data to PDF'));
      }
    });
  }

  private async exportToXml(data: any, options: ExportOptions): Promise<string> {
    try {
      const xml = this.jsonToXml(data);
      return options.compression ? await this.compressData(xml) : xml;
    } catch (error) {
      console.error('XML export error:', error);
      throw new Error('Failed to export data to XML');
    }
  }

  private jsonToXml(data: any, rootName: string = 'analytics'): string {
    const toXml = (obj: any, name: string): string => {
      if (obj === null || obj === undefined) return `<${name}/>`;
      if (typeof obj !== 'object') return `<${name}>${obj}</${name}>`;
      if (Array.isArray(obj)) {
        return obj.map(item => toXml(item, 'item')).join('');
      }
      return `<${name}>${Object.entries(obj)
        .map(([key, value]) => toXml(value, key))
        .join('')}</${name}>`;
    };

    return `<?xml version="1.0" encoding="UTF-8"?>${toXml(data, rootName)}`;
  }

  private async compressData(data: string): Promise<string> {
    // Implement compression logic here
    return data; // Placeholder
  }

  private async compressBuffer(buffer: Buffer): Promise<Buffer> {
    // Implement compression logic here
    return buffer; // Placeholder
  }

  getContentType(format: ExportFormat): string {
    switch (format) {
      case 'csv':
        return 'text/csv';
      case 'json':
        return 'application/json';
      case 'excel':
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      case 'pdf':
        return 'application/pdf';
      case 'xml':
        return 'application/xml';
      default:
        return 'application/octet-stream';
    }
  }
} 
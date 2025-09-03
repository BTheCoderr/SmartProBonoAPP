/**
 * SmartProBono PDF Generation Service
 * Handles PDF generation using the combined pdfme + pdf-lib approach
 */

class PdfService {
  constructor() {
    this.baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:3000';
  }

  /**
   * Generate a PDF document with the given data
   * @param {Object} data - PDF data including clientName, caseNumber, etc.
   * @returns {Promise<Blob>} - Generated PDF as a Blob
   */
  async generatePdf(data) {
    try {
      const response = await fetch(`${this.baseUrl}/api/pdf/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`PDF generation failed: ${response.statusText}`);
      }

      return await response.blob();
    } catch (error) {
      console.error('PDF generation error:', error);
      throw error;
    }
  }

  /**
   * Download a PDF blob as a file
   * @param {Blob} pdfBlob - PDF blob to download
   * @param {string} filename - Name for the downloaded file
   */
  downloadPdf(pdfBlob, filename = 'smartprobono-document.pdf') {
    const url = URL.createObjectURL(pdfBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  /**
   * Generate and download a PDF in one step
   * @param {Object} data - PDF data
   * @param {string} filename - Optional filename
   */
  async generateAndDownload(data, filename) {
    try {
      const pdfBlob = await this.generatePdf(data);
      this.downloadPdf(pdfBlob, filename);
      return pdfBlob;
    } catch (error) {
      console.error('Generate and download error:', error);
      throw error;
    }
  }

  /**
   * Generate a legal document PDF with common SmartProBono fields
   * @param {Object} options - Document options
   */
  async generateLegalDocument(options = {}) {
    const defaultData = {
      clientName: options.clientName || 'Client Name',
      caseNumber: options.caseNumber || `SPB-${Date.now()}`,
      dateIssued: options.dateIssued || new Date().toLocaleDateString(),
      bodyText: options.bodyText || 'This is a SmartProBono legal document.',
      tableRows: options.tableRows || [
        { cols: ['Document Type', 'Status', 'Notes'] },
        { cols: ['Legal Document', 'Generated', 'Ready for review'] },
      ],
      attachments: options.attachments || [],
    };

    return await this.generatePdf(defaultData);
  }

  /**
   * Generate an intake summary PDF
   * @param {Object} intakeData - Client intake data
   */
  async generateIntakeSummary(intakeData) {
    const data = {
      clientName: intakeData.clientName || 'Client',
      caseNumber: intakeData.caseNumber || `INTAKE-${Date.now()}`,
      dateIssued: new Date().toLocaleDateString(),
      bodyText: `Intake Summary for ${intakeData.clientName || 'Client'}\n\nCase Type: ${intakeData.caseType || 'General Legal Matter'}\nPriority: ${intakeData.priority || 'Standard'}`,
      tableRows: [
        { cols: ['Field', 'Value', 'Status'] },
        { cols: ['Client Name', intakeData.clientName || 'N/A', 'Complete'] },
        { cols: ['Case Type', intakeData.caseType || 'N/A', 'Complete'] },
        { cols: ['Priority', intakeData.priority || 'Standard', 'Complete'] },
        { cols: ['Contact Info', intakeData.contactInfo || 'N/A', 'Complete'] },
      ],
    };

    return await this.generatePdf(data);
  }
}

// Export a singleton instance
export default new PdfService();

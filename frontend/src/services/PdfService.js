/**
 * SmartProBono PDF Generation Service
 * Handles PDF generation using the combined pdfme + pdf-lib approach
 * Now with Supabase storage integration
 */

import { generatePdfBuffer } from '../lib/pdf/generateWithPdfme';
import { addHeaderFooter, drawSimpleTable, mergePdfs, placeSignatureImage } from '../lib/pdf/enhanceWithPdfLib';
import { uploadPdfAndGetSignedUrl, buildPdfPath, recordPdfDoc, getSignedUrl, listPdfsForCase } from '../lib/pdf/storage';
import SignatureService from './SignatureService';

class PdfService {
  constructor() {
    this.baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:3001';
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

  /**
   * Generate PDF and save to Supabase Storage
   * @param {Object} data - PDF data
   * @param {string} createdBy - User ID who created the PDF
   * @returns {Promise<Object>} - Result with signed URL and storage path
   */
  async generateAndSaveToStorage(data, createdBy = null) {
    try {
      const caseNumber = data.caseNumber || `SPB-${Date.now()}`;
      
      // 1) Generate base PDF
      const basePdf = await generatePdfBuffer({
        clientName: data.clientName || 'John Doe',
        caseNumber,
        dateIssued: data.dateIssued || new Date().toLocaleDateString(),
        bodyText: data.bodyText || 'This is a SmartProBono document.',
      });

      // 2) Add header/footer
      let current = await addHeaderFooter(basePdf, {
        header: 'SmartProBono • Access to Justice',
        footer: 'Confidential — For client use only',
      });

      // 3) Add table if provided
      if (data.tableRows && data.tableRows.length > 0) {
        current = await drawSimpleTable(
          current,
          data.tableRows,
          { x: 36, y: 520 },
          [250, 100, 150],
          24
        );
      }

      // 4) Merge attachments if provided
      if (data.attachments && data.attachments.length > 0) {
        const buffers = [current, ...data.attachments.map(b64 => Buffer.from(b64, 'base64'))];
        current = await mergePdfs(buffers);
      }

      // 4.5) Add signature if requested and available
      if (data.includeSignature) {
        try {
          const signatureData = await SignatureService.getSignature(caseNumber);
          if (signatureData) {
            current = await placeSignatureImage(current, signatureData, {
              pageIndex: 0,
              x: 380,
              y: 120,
              width: 160,
              height: 60,
            });
            console.log('Signature added to PDF');
          } else {
            console.log('No signature found for case:', caseNumber);
          }
        } catch (error) {
          console.error('Error adding signature to PDF:', error);
          // Continue without signature rather than failing
        }
      }

      // 5) Save to Supabase Storage
      const path = buildPdfPath({ caseNumber, filenameBase: data.filenameBase || 'smartprobono' });
      const { signedUrl } = await uploadPdfAndGetSignedUrl(current, path, 60 * 60);

      // 6) Record in database
      await recordPdfDoc({ caseNumber, storagePath: path, createdBy });

      return {
        success: true,
        caseNumber,
        storagePath: path,
        signedUrl,
        pdfBytes: current
      };
    } catch (error) {
      console.error('Generate and save error:', error);
      throw error;
    }
  }

  /**
   * Get signed URL for existing PDF
   * @param {string} storagePath - Path to PDF in storage
   * @param {number} expiresIn - Expiration time in seconds
   * @returns {Promise<string>} - Signed URL
   */
  async getSignedUrl(storagePath, expiresIn = 3600) {
    try {
      const { signedUrl } = await getSignedUrl(storagePath, expiresIn);
      return signedUrl;
    } catch (error) {
      console.error('Get signed URL error:', error);
      throw error;
    }
  }

  /**
   * List PDFs for a case
   * @param {string} caseNumber - Case number
   * @returns {Promise<Array>} - List of PDF documents
   */
  async listPdfsForCase(caseNumber) {
    try {
      const { items } = await listPdfsForCase(caseNumber);
      return items;
    } catch (error) {
      console.error('List PDFs error:', error);
      throw error;
    }
  }

  /**
   * Generate and download PDF with Supabase storage
   * @param {Object} data - PDF data
   * @param {string} filename - Download filename
   * @param {string} createdBy - User ID
   */
  async generateSaveAndDownload(data, filename, createdBy = null) {
    try {
      const result = await this.generateAndSaveToStorage(data, createdBy);
      
      // Download the PDF
      this.downloadPdf(new Blob([result.pdfBytes], { type: 'application/pdf' }), filename);
      
      return result;
    } catch (error) {
      console.error('Generate save and download error:', error);
      throw error;
    }
  }

  /**
   * Upload signature for a case
   * @param {File} file - Signature file
   * @param {string} caseNumber - Case number
   * @returns {Promise<Object>} - Upload result
   */
  async uploadSignature(file, caseNumber) {
    try {
      return await SignatureService.uploadSignature(file, caseNumber);
    } catch (error) {
      console.error('Upload signature error:', error);
      throw error;
    }
  }

  /**
   * Check if signature exists for a case
   * @param {string} caseNumber - Case number
   * @returns {Promise<boolean>} - True if signature exists
   */
  async hasSignature(caseNumber) {
    try {
      return await SignatureService.hasSignature(caseNumber);
    } catch (error) {
      console.error('Check signature error:', error);
      return false;
    }
  }

  /**
   * Get signature URL for preview
   * @param {string} caseNumber - Case number
   * @param {number} expiresIn - Expiration time in seconds
   * @returns {Promise<string|null>} - Signed URL or null
   */
  async getSignatureUrl(caseNumber, expiresIn = 3600) {
    try {
      return await SignatureService.getSignatureUrl(caseNumber, expiresIn);
    } catch (error) {
      console.error('Get signature URL error:', error);
      return null;
    }
  }

  /**
   * Delete signature for a case
   * @param {string} caseNumber - Case number
   * @returns {Promise<boolean>} - Success status
   */
  async deleteSignature(caseNumber) {
    try {
      return await SignatureService.deleteSignature(caseNumber);
    } catch (error) {
      console.error('Delete signature error:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export default new PdfService();

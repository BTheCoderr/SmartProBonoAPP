/**
 * SmartProBono PDF Generation Service
 * Handles PDF generation using the combined pdfme + pdf-lib approach
 * Now with Supabase storage integration
 */

import { generatePdfBuffer } from '../lib/pdf/generateWithPdfme';
import { addHeaderFooter, drawSimpleTable, mergePdfs, placeSignatureImage, placeImageSignatureAt, placeTypedSignatureAt } from '../lib/pdf/enhanceWithPdfLib';
import { uploadPdfAndGetSignedUrl, buildPdfPath, recordPdfDoc, getSignedUrl, listPdfsForCase } from '../lib/pdf/storage';
import { fetchPlacementsByTemplate, fetchPdfmeTemplate } from '../lib/pdf/templates';
import { getCurrentUser } from '../lib/supabase/auth';
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

  /**
   * Generate PDF with auto-loaded signature placements
   * @param {Object} input - PDF generation parameters
   * @returns {Promise<Object>} - Generation result with signed URL
   */
  async generatePdfWithTemplate(input) {
    try {
      const {
        caseNumber,
        templateName,
        includeSignature = false,
        clientSignature = {},
        attorneySignature = {},
        bodyText,
        tableRows,
        clientName,
        dateIssued,
        attachments = []
      } = input;

      // Auto-load placements if not provided
      let savedPlacements = null;
      if (templateName && includeSignature) {
        savedPlacements = await fetchPlacementsByTemplate(templateName);
      }

      // Default positions
      const DEFAULT_CLIENT_POS = { pageIndex: 0, x: 380, y: 120, width: 160, height: 60, label: "Client" };
      const DEFAULT_ATTORNEY_POS = { pageIndex: 0, x: 380, y: 60, width: 160, height: 60, label: "Attorney" };

      // Determine final positions
      const clientPos = clientSignature.pos || 
        (savedPlacements?.client ? {
          pageIndex: savedPlacements.client.pageIndex,
          x: savedPlacements.client.x,
          y: savedPlacements.client.y,
          width: savedPlacements.client.width || 160,
          height: savedPlacements.client.height || 60,
          label: savedPlacements.client.label || "Client"
        } : DEFAULT_CLIENT_POS);

      const attorneyPos = attorneySignature.pos || 
        (savedPlacements?.attorney ? {
          pageIndex: savedPlacements.attorney.pageIndex,
          x: savedPlacements.attorney.x,
          y: savedPlacements.attorney.y,
          width: savedPlacements.attorney.width || 160,
          height: savedPlacements.attorney.height || 60,
          label: savedPlacements.attorney.label || "Attorney"
        } : DEFAULT_ATTORNEY_POS);

      // Load pdfme template if templateName provided
      let runtimeTemplate = null;
      if (templateName) {
        const loaded = await fetchPdfmeTemplate(templateName);
        runtimeTemplate = loaded?.templateJson;
      }

      // Generate base PDF
      let current = await generatePdfBuffer({
        clientName: clientName || "John Doe",
        caseNumber: caseNumber || "SPB-12345",
        dateIssued: dateIssued || new Date().toLocaleDateString(),
        bodyText: bodyText || "This is a SmartProBono document.",
      }, runtimeTemplate);

      // Add header/footer
      current = await addHeaderFooter(current, {
        header: "SmartProBono • Access to Justice",
        footer: "Confidential — For client use only",
      });

      // Add table if provided
      if (tableRows && tableRows.length > 0) {
        current = await drawSimpleTable(
          current,
          tableRows,
          { x: 36, y: 520 },
          [250, 100, 150],
          24
        );
      }

      // Merge attachments if provided
      if (attachments.length > 0) {
        const buffers = [current, ...attachments.map(b64 => new Uint8Array(Buffer.from(b64, "base64")))];
        current = await mergePdfs(buffers);
      }

      // Add signatures if requested
      if (includeSignature) {
        // Client signature
        if (clientSignature.type === "typed" && clientSignature.text) {
          current = await placeTypedSignatureAt(current, clientSignature.text, { ...clientPos, fontSize: clientPos.fontSize || 16 });
        } else {
          // Try to get client signature image
          const clientSigData = await SignatureService.getSignature(caseNumber, 'client');
          if (clientSigData) {
            current = await placeImageSignatureAt(current, clientSigData, clientPos);
          }
        }

        // Attorney signature
        if (attorneySignature.type === "typed" && attorneySignature.text) {
          current = await placeTypedSignatureAt(current, attorneySignature.text, { ...attorneyPos, fontSize: attorneyPos.fontSize || 16 });
        } else {
          // Try to get attorney signature image
          const attorneySigData = await SignatureService.getSignature(caseNumber, 'attorney');
          if (attorneySigData) {
            current = await placeImageSignatureAt(current, attorneySigData, attorneyPos);
          }
        }
      }

      // Save to storage and return signed URL
      const path = buildPdfPath({ caseNumber, filenameBase: "smartprobono" });
      const { signedUrl } = await uploadPdfAndGetSignedUrl(current, path, 60 * 60);

      // Record in database with user info
      const user = await getCurrentUser();
      await recordPdfDoc({
        caseNumber,
        storagePath: path,
        createdBy: user?.id || null
      });

      return {
        ok: true,
        caseNumber,
        storagePath: path,
        signedUrl,
        usedPlacements: savedPlacements ? 'auto-loaded' : 'default'
      };
    } catch (error) {
      console.error('Error generating PDF with template:', error);
      throw error;
    }
  }
}

// Create and export singleton instance
const pdfService = new PdfService();
export default pdfService;

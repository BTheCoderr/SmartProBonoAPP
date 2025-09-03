/**
 * SmartProBono Signature Service
 * Handles signature upload, storage, and retrieval
 */

import { supabaseAdmin } from '../lib/supabase/client';

const SIGNATURE_BUCKET = 'smartprobono-signatures';

class SignatureService {
  constructor() {
    this.bucket = SIGNATURE_BUCKET;
  }

  /**
   * Upload signature to Supabase Storage
   * @param {File} file - Signature file (PNG)
   * @param {string} caseNumber - Case number
   * @returns {Promise<Object>} - Upload result with path
   */
  async uploadSignature(file, caseNumber) {
    try {
      const path = `cases/${caseNumber}/signature.png`;
      
      // Convert file to buffer
      const arrayBuffer = await file.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);

      // Upload to Supabase Storage
      const { error } = await supabaseAdmin.storage
        .from(this.bucket)
        .upload(path, buffer, {
          contentType: 'image/png',
          upsert: true, // Overwrite if exists
        });

      if (error) {
        console.error('Signature upload error:', error);
        throw error;
      }

      return {
        success: true,
        path,
        message: 'Signature uploaded successfully'
      };
    } catch (error) {
      console.error('Upload signature error:', error);
      throw error;
    }
  }

  /**
   * Get signature from storage
   * @param {string} caseNumber - Case number
   * @returns {Promise<Uint8Array|null>} - Signature image data or null
   */
  async getSignature(caseNumber) {
    try {
      const path = `cases/${caseNumber}/signature.png`;
      
      const { data, error } = await supabaseAdmin.storage
        .from(this.bucket)
        .download(path);

      if (error) {
        if (error.message.includes('Object not found')) {
          return null; // No signature found
        }
        throw error;
      }

      // Convert blob to Uint8Array
      const arrayBuffer = await data.arrayBuffer();
      return new Uint8Array(arrayBuffer);
    } catch (error) {
      console.error('Get signature error:', error);
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
      const path = `cases/${caseNumber}/signature.png`;
      
      const { data, error } = await supabaseAdmin.storage
        .from(this.bucket)
        .list(`cases/${caseNumber}`, {
          search: 'signature.png'
        });

      if (error) {
        return false;
      }

      return data && data.length > 0;
    } catch (error) {
      console.error('Check signature error:', error);
      return false;
    }
  }

  /**
   * Delete signature for a case
   * @param {string} caseNumber - Case number
   * @returns {Promise<boolean>} - Success status
   */
  async deleteSignature(caseNumber) {
    try {
      const path = `cases/${caseNumber}/signature.png`;
      
      const { error } = await supabaseAdmin.storage
        .from(this.bucket)
        .remove([path]);

      if (error) {
        console.error('Delete signature error:', error);
        throw error;
      }

      return true;
    } catch (error) {
      console.error('Delete signature error:', error);
      throw error;
    }
  }

  /**
   * Get signed URL for signature (for preview)
   * @param {string} caseNumber - Case number
   * @param {number} expiresIn - Expiration time in seconds
   * @returns {Promise<string|null>} - Signed URL or null
   */
  async getSignatureUrl(caseNumber, expiresIn = 3600) {
    try {
      const path = `cases/${caseNumber}/signature.png`;
      
      const { data, error } = await supabaseAdmin.storage
        .from(this.bucket)
        .createSignedUrl(path, expiresIn);

      if (error) {
        if (error.message.includes('Object not found')) {
          return null;
        }
        throw error;
      }

      return data.signedUrl;
    } catch (error) {
      console.error('Get signature URL error:', error);
      return null;
    }
  }
}

// Export singleton instance
export default new SignatureService();

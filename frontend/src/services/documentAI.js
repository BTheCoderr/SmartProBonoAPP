// Document AI Service for SmartProBono
// This service handles communication with the Python worker and Supabase

const DOC_WORKER_URL = process.env.REACT_APP_DOC_WORKER_URL || 'http://localhost:8001';
const SUPABASE_URL = process.env.REACT_APP_SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.REACT_APP_SUPABASE_ANON_KEY;
const STORAGE_BUCKET = process.env.REACT_APP_SUPABASE_STORAGE_BUCKET || 'docs';

class DocumentAIService {
  constructor() {
    this.supabase = null;
    this.initializeSupabase();
  }

  initializeSupabase() {
    // Initialize Supabase client if available
    if (typeof window !== 'undefined' && window.supabase) {
      this.supabase = window.supabase;
    }
  }

  // Upload a document to local worker
  async uploadDocument(file, userId) {
    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', userId || 'anonymous');
      formData.append('title', file.name);
      
      // Upload file to worker
      const response = await fetch(`${DOC_WORKER_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${errorText}`);
      }

      const result = await response.json();
      return { id: result.document_id, path: result.path };
    } catch (error) {
      console.error('Document upload error:', error);
      throw error;
    }
  }

  // Process a document using the Python worker
  async processDocument(documentId, language = 'eng') {
    try {
      const response = await fetch(`${DOC_WORKER_URL}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_id: documentId,
          language: language
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Worker error: ${errorText}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Document processing error:', error);
      throw error;
    }
  }

  // Ask a question about a document
  async askQuestion(documentId, question) {
    try {
      const response = await fetch(`${DOC_WORKER_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_id: documentId,
          question: question
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Worker error: ${errorText}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Question asking error:', error);
      throw error;
    }
  }

  // Get document status
  async getDocumentStatus(documentId) {
    try {
      if (!this.supabase) {
        throw new Error('Supabase client not initialized');
      }

      const { data, error } = await this.supabase
        .from('documents')
        .select('status, title, created_at')
        .eq('id', documentId)
        .single();

      if (error) {
        throw new Error(`Database error: ${error.message}`);
      }

      return data;
    } catch (error) {
      console.error('Get document status error:', error);
      throw error;
    }
  }

  // Get user's documents
  async getUserDocuments(userId) {
    try {
      if (!this.supabase) {
        throw new Error('Supabase client not initialized');
      }

      const { data, error } = await this.supabase
        .from('documents')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false });

      if (error) {
        throw new Error(`Database error: ${error.message}`);
      }

      return data || [];
    } catch (error) {
      console.error('Get user documents error:', error);
      throw error;
    }
  }

  // Check if Python worker is healthy
  async checkWorkerHealth() {
    try {
      const response = await fetch(`${DOC_WORKER_URL}/health`);
      if (response.ok) {
        const result = await response.json();
        return { healthy: true, model: result.model };
      } else {
        return { healthy: false, error: 'Worker not responding' };
      }
    } catch (error) {
      return { healthy: false, error: error.message };
    }
  }

  // Generate UUID for document IDs
  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  // Get signed URL for document download (if needed)
  async getSignedUrl(path, expiresIn = 3600) {
    try {
      if (!this.supabase) {
        throw new Error('Supabase client not initialized');
      }

      const { data, error } = await this.supabase.storage
        .from(STORAGE_BUCKET)
        .createSignedUrl(path, expiresIn);

      if (error) {
        throw new Error(`Signed URL error: ${error.message}`);
      }

      return data.signedURL;
    } catch (error) {
      console.error('Get signed URL error:', error);
      throw error;
    }
  }
}

// Create and export a singleton instance
const documentAIService = new DocumentAIService();
export default documentAIService;

// Export the class for testing or custom instances
export { DocumentAIService };

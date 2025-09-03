import { supabaseAdmin } from '../supabase/client';

const BUCKET = process.env.REACT_APP_SUPABASE_STORAGE_BUCKET || 'smartprobono-pdfs';

// Upload PDF and get signed URL
export async function uploadPdfAndGetSignedUrl(pdfBytes, path, expireSeconds = 60 * 60) {
  try {
    // Upload the PDF
    const { error: uploadError } = await supabaseAdmin.storage
      .from(BUCKET)
      .upload(path, Buffer.from(pdfBytes), {
        contentType: 'application/pdf',
        upsert: true,
      });

    if (uploadError) {
      console.error('Upload error:', uploadError);
      throw uploadError;
    }

    // Create signed URL
    const { data, error: signError } = await supabaseAdmin.storage
      .from(BUCKET)
      .createSignedUrl(path, expireSeconds);

    if (signError) {
      console.error('Sign URL error:', signError);
      throw signError;
    }

    return { signedUrl: data.signedUrl, path };
  } catch (error) {
    console.error('PDF storage error:', error);
    throw error;
  }
}

// Build consistent PDF path
export function buildPdfPath(opts) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const base = opts.filenameBase || 'smartprobono';
  return `cases/${opts.caseNumber}/outputs/${base}_${timestamp}.pdf`;
}

// Record PDF document in database
export async function recordPdfDoc(params) {
  try {
    const { error } = await supabaseAdmin
      .from('pdf_documents')
      .insert({
        case_number: params.caseNumber,
        storage_path: params.storagePath,
        created_by: params.createdBy || null,
      });

    if (error) {
      console.error('Database record error:', error);
      throw error;
    }

    return { success: true };
  } catch (error) {
    console.error('Record PDF doc error:', error);
    throw error;
  }
}

// Get signed URL for existing PDF
export async function getSignedUrl(storagePath, expiresIn = 3600) {
  try {
    const { data, error } = await supabaseAdmin.storage
      .from(BUCKET)
      .createSignedUrl(storagePath, expiresIn);

    if (error) {
      console.error('Get signed URL error:', error);
      throw error;
    }

    return { signedUrl: data.signedUrl };
  } catch (error) {
    console.error('Get signed URL error:', error);
    throw error;
  }
}

// List PDFs for a case
export async function listPdfsForCase(caseNumber) {
  try {
    const { data, error } = await supabaseAdmin
      .from('pdf_documents')
      .select('id, storage_path, created_at')
      .eq('case_number', caseNumber)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('List PDFs error:', error);
      throw error;
    }

    return { items: data || [] };
  } catch (error) {
    console.error('List PDFs error:', error);
    throw error;
  }
}

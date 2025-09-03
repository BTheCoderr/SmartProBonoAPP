import { supabase } from '../supabase/client';

/**
 * Fetch signature placements by template name from Supabase
 * @param {string} templateName - Template name to fetch placements for
 * @returns {Promise<Object|null>} - Placements object or null if not found
 */
export async function fetchPlacementsByTemplate(templateName) {
  if (!templateName) return null;

  try {
    const { data, error } = await supabase
      .from('pdf_signature_layouts')
      .select('placements')
      .eq('template_name', templateName)
      .maybeSingle();

    if (error) {
      // Don't crash generation on layout fetch failures
      console.error('fetchPlacementsByTemplate error:', error.message);
      return null;
    }

    return data?.placements || null;
  } catch (error) {
    console.error('fetchPlacementsByTemplate error:', error);
    return null;
  }
}

/**
 * Save signature placements for a template
 * @param {string} templateName - Template name
 * @param {Object} placements - Placements object
 * @param {string} createdBy - User ID (optional)
 * @returns {Promise<boolean>} - Success status
 */
export async function savePlacementsForTemplate(templateName, placements, createdBy = null) {
  if (!templateName || !placements) {
    throw new Error('templateName and placements are required');
  }

  try {
    const { error } = await supabase
      .from('pdf_signature_layouts')
      .upsert(
        {
          template_name: templateName,
          placements: placements,
          created_by: createdBy,
        },
        { onConflict: 'template_name' }
      );

    if (error) {
      throw error;
    }

    return true;
  } catch (error) {
    console.error('savePlacementsForTemplate error:', error);
    throw error;
  }
}

/**
 * Get all saved template layouts
 * @returns {Promise<Array>} - Array of template layouts
 */
export async function getAllTemplateLayouts() {
  try {
    const { data, error } = await supabase
      .from('pdf_signature_layouts')
      .select('template_name, placements, created_at')
      .order('created_at', { ascending: false });

    if (error) {
      throw error;
    }

    return data || [];
  } catch (error) {
    console.error('getAllTemplateLayouts error:', error);
    return [];
  }
}

/**
 * Fetch pdfme template by template name
 * @param {string} templateName - Template name to fetch
 * @returns {Promise<Object|null>} - Template object with templateJson and basePdfBytes
 */
export async function fetchPdfmeTemplate(templateName) {
  if (!templateName) return null;

  try {
    const { data, error } = await supabase
      .from('pdf_templates')
      .select('template_json, base_pdf_path')
      .eq('template_name', templateName)
      .maybeSingle();

    if (error || !data) {
      console.error('fetchPdfmeTemplate error:', error);
      return null;
    }

    let basePdfBytes = undefined;
    if (data.base_pdf_path) {
      // Load base PDF from Storage if provided
      const { data: file } = await supabase.storage
        .from(process.env.REACT_APP_SUPABASE_STORAGE_BUCKET || 'smartprobono-pdfs')
        .download(data.base_pdf_path);
      
      if (file) {
        const buf = Buffer.from(await file.arrayBuffer());
        basePdfBytes = new Uint8Array(buf);
      }
    }

    return { templateJson: data.template_json, basePdfBytes };
  } catch (error) {
    console.error('fetchPdfmeTemplate error:', error);
    return null;
  }
}

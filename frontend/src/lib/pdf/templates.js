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

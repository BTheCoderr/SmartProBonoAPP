import { supabase } from '../../../lib/supabase/client';

export const dynamic = 'force-dynamic';

export async function GET(req) {
  try {
    const { searchParams } = new URL(req.url);
    const templateName = searchParams.get('templateName');

    if (!templateName) {
      return Response.json({ error: 'templateName required' }, { status: 400 });
    }

    const { data, error } = await supabase
      .from('pdf_signature_layouts')
      .select('template_name, placements, created_at')
      .eq('template_name', templateName)
      .maybeSingle();

    if (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }

    return Response.json({ 
      ok: true, 
      templateName, 
      placements: data?.placements || null 
    });
  } catch (e) {
    return Response.json({ error: e?.message || 'fetch failed' }, { status: 500 });
  }
}

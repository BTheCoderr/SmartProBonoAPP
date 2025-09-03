import { supabase } from '../../../lib/supabase/client';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const { data, error } = await supabase
      .from('pdf_templates')
      .select('template_name, version, base_pdf_path, created_at')
      .order('template_name', { ascending: true });

    if (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }

    return Response.json({ ok: true, items: data || [] });
  } catch (e) {
    return Response.json({ error: e?.message || 'list failed' }, { status: 500 });
  }
}

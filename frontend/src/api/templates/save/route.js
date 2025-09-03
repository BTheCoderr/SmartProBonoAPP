import { supabase } from '../../../lib/supabase/client';

export const dynamic = 'force-dynamic';

export async function POST(req) {
  try {
    const body = await req.json();

    if (!body.templateName || !body.templateJson) {
      return Response.json({ error: 'templateName and templateJson required' }, { status: 400 });
    }

    const { error } = await supabase
      .from('pdf_templates')
      .upsert(
        {
          template_name: body.templateName,
          template_json: body.templateJson,
          base_pdf_path: body.basePdfPath || null,
          version: body.version || 'v1',
          created_by: body.createdBy || null,
        },
        { onConflict: 'template_name' }
      );

    if (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }

    return Response.json({ ok: true });
  } catch (e) {
    return Response.json({ error: e?.message || 'save failed' }, { status: 500 });
  }
}

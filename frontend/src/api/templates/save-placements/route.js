import { supabase } from '../../../lib/supabase/client';
import { getUserOrThrow } from '../../../lib/supabase/auth';

export const dynamic = 'force-dynamic';

export async function POST(req) {
  try {
    // Check authentication
    const user = await getUserOrThrow();
    
    const body = await req.json();

    if (!body.templateName || !body.placements) {
      return Response.json({ error: 'templateName and placements required' }, { status: 400 });
    }

    // Upsert by template_name so you can revise layouts
    const { error } = await supabase
      .from('pdf_signature_layouts')
      .upsert(
        {
          template_name: body.templateName,
          placements: body.placements,
          created_by: user.id,
        },
        { onConflict: 'template_name' }
      );

    if (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }

    return Response.json({ ok: true });
  } catch (e) {
    if (e.message.includes('Unauthorized')) {
      return Response.json({ error: 'Unauthorized - Please log in to continue' }, { status: 401 });
    }
    return Response.json({ error: e?.message || 'save failed' }, { status: 500 });
  }
}

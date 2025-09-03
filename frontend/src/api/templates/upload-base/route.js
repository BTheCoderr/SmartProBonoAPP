import { supabase } from '../../../lib/supabase/client';
import { getUserOrThrow } from '../../../lib/supabase/auth';

export const dynamic = 'force-dynamic';
const BUCKET = process.env.REACT_APP_SUPABASE_STORAGE_BUCKET || 'smartprobono-pdfs';

export async function POST(req) {
  try {
    // Check authentication
    const user = await getUserOrThrow();
    
    const form = await req.formData();
    const file = form.get('file');
    const templateName = form.get('templateName');

    if (!file || !templateName) {
      return Response.json({ error: 'file and templateName required' }, { status: 400 });
    }

    const arrayBuffer = await file.arrayBuffer();
    const path = `templates/${templateName}/base.pdf`;

    const { error: upErr } = await supabase.storage
      .from(BUCKET)
      .upload(path, Buffer.from(arrayBuffer), {
        contentType: 'application/pdf',
        upsert: true,
      });

    if (upErr) {
      return Response.json({ error: upErr.message }, { status: 500 });
    }

    // Update the template record
    const { error: updErr } = await supabase
      .from('pdf_templates')
      .update({ base_pdf_path: path })
      .eq('template_name', templateName);

    if (updErr) {
      return Response.json({ error: updErr.message }, { status: 500 });
    }

    return Response.json({ ok: true, basePdfPath: path });
  } catch (e) {
    if (e.message.includes('Unauthorized')) {
      return Response.json({ error: 'Unauthorized - Please log in to continue' }, { status: 401 });
    }
    return Response.json({ error: e?.message || 'upload failed' }, { status: 500 });
  }
}

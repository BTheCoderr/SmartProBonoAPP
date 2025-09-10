import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { text, jurisdiction, results } = req.body;
    
    const { data, error } = await supabase
      .from('queries')
      .insert([{ 
        text, 
        jurisdiction, 
        results: results || {},
        created_at: new Date().toISOString()
      }]);
    
    if (error) {
      console.error('Supabase error:', error);
      return res.status(500).json({ error: error.message });
    }
    
    res.status(200).json({ success: true, data });
  } catch (error) {
    console.error('Error in saveQuery API:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}

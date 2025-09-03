import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'https://your-project.supabase.co';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'your-anon-key';

// Client-side Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Admin client for server-side operations (when we have a backend)
export const supabaseAdmin = createClient(
  supabaseUrl, 
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || 'your-service-role-key',
  {
    auth: { persistSession: false }
  }
);

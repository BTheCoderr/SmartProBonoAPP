import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'https://ewtcvsohdgkthuyajyyk.supabase.co';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY0MTA0NjQsImV4cCI6MjA3MTk4NjQ2NH0.NXO-6aVlkqc9HCL6MHRcW0V9JN4Z85WhvRxK6aJnBbI';

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Auth helpers
export const auth = {
  async signUp(email, password, fullName) {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
        },
      },
    });
    return { data, error };
  },

  async signIn(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    return { data, error };
  },

  async signOut() {
    const { error } = await supabase.auth.signOut();
    return { error };
  },

  async getCurrentUser() {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
  },

  onAuthStateChange(callback) {
    return supabase.auth.onAuthStateChange(callback);
  }
};

// Database helpers
export const db = {
  // Conversations
  async createConversation(userId, title, modelUsed) {
    const { data, error } = await supabase
      .from('conversations')
      .insert([{ user_id: userId, title, model_used: modelUsed }])
      .select()
      .single();
    return { data, error };
  },

  async getConversations(userId) {
    const { data, error } = await supabase
      .from('conversations')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });
    return { data, error };
  },

  // Messages
  async createMessage(conversationId, content, role, modelUsed) {
    const { data, error } = await supabase
      .from('messages')
      .insert([{ 
        conversation_id: conversationId, 
        content, 
        role, 
        model_used: modelUsed 
      }])
      .select()
      .single();
    return { data, error };
  },

  async getMessages(conversationId) {
    const { data, error } = await supabase
      .from('messages')
      .select('*')
      .eq('conversation_id', conversationId)
      .order('created_at', { ascending: true });
    return { data, error };
  },

  // Documents
  async uploadDocument(userId, title, filePath, fileType, fileSize, content, metadata) {
    const { data, error } = await supabase
      .from('documents')
      .insert([{ 
        user_id: userId, 
        title, 
        file_path: filePath, 
        file_type: fileType, 
        file_size: fileSize, 
        content, 
        metadata 
      }])
      .select()
      .single();
    return { data, error };
  },

  async getDocuments(userId) {
    const { data, error } = await supabase
      .from('documents')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });
    return { data, error };
  },

  // Feedback
  async createFeedback(userId, conversationId, rating, feedbackText) {
    const { data, error } = await supabase
      .from('feedback')
      .insert([{ 
        user_id: userId, 
        conversation_id: conversationId, 
        rating, 
        feedback_text: feedbackText 
      }])
      .select()
      .single();
    return { data, error };
  },

  // Beta signups
  async createBetaSignup(email) {
    const { data, error } = await supabase
      .from('beta_signups')
      .insert([{ email }])
      .select()
      .single();
    return { data, error };
  }
};

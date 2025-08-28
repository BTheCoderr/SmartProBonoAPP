// Supabase Configuration
export const supabaseConfig = {
  url: process.env.REACT_APP_SUPABASE_URL || 'YOUR_SUPABASE_URL',
  anonKey: process.env.REACT_APP_SUPABASE_ANON_KEY || 'YOUR_SUPABASE_ANON_KEY',
  serviceRoleKey: process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || 'YOUR_SERVICE_ROLE_KEY'
};

// Database schema
export const databaseSchema = {
  users: {
    id: 'uuid PRIMARY KEY DEFAULT gen_random_uuid()',
    email: 'varchar UNIQUE NOT NULL',
    full_name: 'varchar',
    avatar_url: 'varchar',
    role: 'varchar DEFAULT "user"',
    is_premium: 'boolean DEFAULT false',
    created_at: 'timestamp DEFAULT now()',
    updated_at: 'timestamp DEFAULT now()'
  },
  conversations: {
    id: 'uuid PRIMARY KEY DEFAULT gen_random_uuid()',
    user_id: 'uuid REFERENCES users(id) ON DELETE CASCADE',
    title: 'varchar',
    model_used: 'varchar',
    created_at: 'timestamp DEFAULT now()',
    updated_at: 'timestamp DEFAULT now()'
  },
  messages: {
    id: 'uuid PRIMARY KEY DEFAULT gen_random_uuid()',
    conversation_id: 'uuid REFERENCES conversations(id) ON DELETE CASCADE',
    content: 'text NOT NULL',
    role: 'varchar NOT NULL', // 'user' or 'assistant'
    model_used: 'varchar',
    created_at: 'timestamp DEFAULT now()'
  },
  documents: {
    id: 'uuid PRIMARY KEY DEFAULT gen_random_uuid()',
    user_id: 'uuid REFERENCES users(id) ON DELETE CASCADE',
    title: 'varchar NOT NULL',
    file_path: 'varchar',
    file_type: 'varchar',
    file_size: 'integer',
    content: 'text',
    metadata: 'jsonb',
    created_at: 'timestamp DEFAULT now()',
    updated_at: 'timestamp DEFAULT now()'
  },
  feedback: {
    id: 'uuid PRIMARY KEY DEFAULT gen_random_uuid()',
    user_id: 'uuid REFERENCES users(id) ON DELETE CASCADE',
    conversation_id: 'uuid REFERENCES conversations(id) ON DELETE CASCADE',
    rating: 'integer CHECK (rating >= 1 AND rating <= 5)',
    feedback_text: 'text',
    created_at: 'timestamp DEFAULT now()'
  },
  beta_signups: {
    id: 'uuid PRIMARY KEY DEFAULT gen_random_uuid()',
    email: 'varchar UNIQUE NOT NULL',
    status: 'varchar DEFAULT "pending"',
    created_at: 'timestamp DEFAULT now()'
  }
};

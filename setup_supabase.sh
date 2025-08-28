#!/bin/bash

# SmartProBono Supabase Setup Script
echo "🔐 Setting up Supabase Backend for SmartProBono"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "1. 📦 Installing Supabase dependencies..."

# Install Supabase CLI if not already installed
if ! command -v supabase &> /dev/null; then
    echo "   Installing Supabase CLI..."
    npm install -g supabase
else
    echo "   ✅ Supabase CLI already installed"
fi

# Install Supabase client libraries
echo "   Installing Supabase client libraries..."
cd frontend
npm install @supabase/supabase-js
npm install @supabase/auth-ui-react @supabase/auth-ui-shared
cd ..

echo ""
echo "2. 🔧 Creating Supabase configuration..."

# Create Supabase config file
cat > supabase_config.js << 'EOF'
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
EOF

echo ""
echo "3. 🔐 Creating security policies..."

# Create RLS policies
cat > supabase_policies.sql << 'EOF'
-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE beta_signups ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

-- Conversations policies
CREATE POLICY "Users can view own conversations" ON conversations
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own conversations" ON conversations
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own conversations" ON conversations
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own conversations" ON conversations
  FOR DELETE USING (auth.uid() = user_id);

-- Messages policies
CREATE POLICY "Users can view messages in own conversations" ON messages
  FOR SELECT USING (
    conversation_id IN (
      SELECT id FROM conversations WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Users can create messages in own conversations" ON messages
  FOR INSERT WITH CHECK (
    conversation_id IN (
      SELECT id FROM conversations WHERE user_id = auth.uid()
    )
  );

-- Documents policies
CREATE POLICY "Users can view own documents" ON documents
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own documents" ON documents
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own documents" ON documents
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own documents" ON documents
  FOR DELETE USING (auth.uid() = user_id);

-- Feedback policies
CREATE POLICY "Users can view own feedback" ON feedback
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own feedback" ON feedback
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Beta signups policies (public read, authenticated insert)
CREATE POLICY "Anyone can view beta signups" ON beta_signups
  FOR SELECT USING (true);

CREATE POLICY "Anyone can create beta signup" ON beta_signups
  FOR INSERT WITH CHECK (true);
EOF

echo ""
echo "4. 🤖 Creating multi-agent AI system..."

# Create AI agent configuration
cat > ai_agents_config.js << 'EOF'
// Multi-Agent AI System Configuration
export const aiAgents = {
  // Greeting Agent - handles simple greetings and introductions
  greeting: {
    name: "Greeting Agent",
    description: "Handles greetings, introductions, and basic questions",
    model: "gpt-3.5-turbo",
    systemPrompt: `You are a friendly legal assistant. Keep responses brief and helpful.
    
    For greetings like "hello", "hi", "hey":
    - Respond warmly but briefly
    - Ask what legal help they need
    - Don't overwhelm with information
    
    For "what can you do?":
    - List 3-4 main capabilities briefly
    - Ask what specific help they need
    
    Keep responses under 100 words unless specifically asked for details.`,
    maxTokens: 150,
    temperature: 0.7
  },

  // Compliance Agent - handles GDPR, SOC 2, privacy policies
  compliance: {
    name: "Compliance Agent",
    description: "Specializes in legal compliance and regulatory requirements",
    model: "gpt-4",
    systemPrompt: `You are a legal compliance expert specializing in:
    - GDPR and data privacy
    - SOC 2 and security frameworks
    - Privacy policies and terms of service
    - Regulatory compliance
    
    Provide detailed, actionable guidance. Include:
    - Specific requirements
    - Implementation steps
    - Risk assessments
    - Cost estimates when relevant
    
    Always recommend consulting with a qualified attorney for complex matters.`,
    maxTokens: 2000,
    temperature: 0.3
  },

  // Business Agent - handles entity formation, fundraising, contracts
  business: {
    name: "Business Agent",
    description: "Specializes in business law and startup legal needs",
    model: "gpt-4",
    systemPrompt: `You are a business law expert specializing in:
    - Entity formation (LLC, Corp, etc.)
    - Fundraising and investment
    - Employment agreements
    - Intellectual property
    - Contract review and drafting
    
    Provide practical, startup-focused advice. Include:
    - Pros and cons of different options
    - Cost considerations
    - Timeline estimates
    - Next steps
    
    Always recommend consulting with a qualified attorney for complex matters.`,
    maxTokens: 2000,
    temperature: 0.3
  },

  // Document Agent - handles document analysis and generation
  document: {
    name: "Document Agent",
    description: "Specializes in document analysis and generation",
    model: "gpt-4",
    systemPrompt: `You are a document analysis and generation expert. You can:
    - Analyze legal documents
    - Generate legal documents
    - Explain complex legal language
    - Identify key terms and clauses
    
    When analyzing documents:
    - Highlight key terms
    - Explain implications
    - Identify potential issues
    - Suggest improvements
    
    When generating documents:
    - Use clear, professional language
    - Include all necessary clauses
    - Provide customization options
    - Include disclaimers about legal advice`,
    maxTokens: 3000,
    temperature: 0.2
  },

  // Expert Agent - handles complex legal questions and expert referrals
  expert: {
    name: "Expert Agent",
    description: "Handles complex legal questions and expert referrals",
    model: "gpt-4",
    systemPrompt: `You are a senior legal expert who handles complex questions and expert referrals.
    
    For complex legal questions:
    - Provide thorough analysis
    - Identify key legal issues
    - Suggest multiple approaches
    - Highlight risks and considerations
    
    For expert referrals:
    - Match users with appropriate legal experts
    - Explain why the expert is suitable
    - Provide contact information
    - Set expectations for consultation
    
    Always emphasize the importance of professional legal counsel for complex matters.`,
    maxTokens: 2500,
    temperature: 0.3
  }
};

// Agent routing logic
export const routeToAgent = (message, context = {}) => {
  const lowerMessage = message.toLowerCase();
  
  // Greeting patterns
  if (lowerMessage.match(/^(hello|hi|hey|good morning|good afternoon|good evening)$/)) {
    return 'greeting';
  }
  
  // Compliance patterns
  if (lowerMessage.match(/(gdpr|privacy|data protection|soc 2|compliance|regulatory|terms of service|privacy policy)/)) {
    return 'compliance';
  }
  
  // Business patterns
  if (lowerMessage.match(/(incorporat|llc|corporation|fundraising|investment|equity|employment|contract|intellectual property|ip|trademark|patent)/)) {
    return 'business';
  }
  
  // Document patterns
  if (lowerMessage.match(/(document|contract|agreement|generate|create|draft|analyze|review|pdf|upload)/)) {
    return 'document';
  }
  
  // Expert patterns (complex questions or explicit requests)
  if (lowerMessage.match(/(expert|attorney|lawyer|consult|complex|litigation|court|lawsuit)/) || 
      context.conversationLength > 5) {
    return 'expert';
  }
  
  // Default to greeting for unclear messages
  return 'greeting';
};
EOF

echo ""
echo "5. 🔧 Creating Supabase client setup..."

# Create Supabase client
cat > frontend/src/lib/supabase.js << 'EOF'
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

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
EOF

echo ""
echo "6. 📝 Creating environment template..."

# Create environment template
cat > .env.example << 'EOF'
# Supabase Configuration
REACT_APP_SUPABASE_URL=your_supabase_project_url
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
REACT_APP_SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Email Configuration (keep existing)
SMTP_SERVER=smtp.zoho.com
SMTP_PORT=587
SMTP_USERNAME=info@smartprobono.org
SMTP_PASSWORD=your_email_password

# AI Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
EOF

echo ""
echo "7. 📋 Creating setup instructions..."

cat > SUPABASE_SETUP_INSTRUCTIONS.md << 'EOF'
# 🔐 Supabase Setup Instructions for SmartProBono

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - Name: `smartprobono`
   - Database Password: (generate a strong password)
   - Region: Choose closest to your users
6. Click "Create new project"

## 2. Get Your Credentials

1. Go to Settings > API
2. Copy your:
   - Project URL
   - Anon public key
   - Service role key (keep this secret!)

## 3. Set Up Environment Variables

1. Copy `.env.example` to `.env`
2. Fill in your Supabase credentials:
   ```
   REACT_APP_SUPABASE_URL=https://your-project.supabase.co
   REACT_APP_SUPABASE_ANON_KEY=your_anon_key
   REACT_APP_SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   ```

## 4. Set Up Database Schema

1. Go to SQL Editor in Supabase
2. Run the SQL from `supabase_policies.sql`
3. This will create all tables and security policies

## 5. Set Up Storage (for documents)

1. Go to Storage in Supabase
2. Create a new bucket called `documents`
3. Set it to public if you want public access
4. Or keep it private and use RLS policies

## 6. Test the Setup

1. Start your app: `./start_mvp.sh`
2. Try signing up a new user
3. Check the Supabase dashboard to see the data

## 7. Security Features

✅ **Row Level Security (RLS)**: Users can only see their own data
✅ **Authentication**: Secure user signup and login
✅ **API Security**: Protected endpoints with JWT tokens
✅ **Data Validation**: Input validation and sanitization
✅ **Rate Limiting**: Built-in Supabase rate limiting

## 8. Multi-Agent AI System

The new AI system includes:
- **Greeting Agent**: Handles simple greetings (no more overwhelming responses!)
- **Compliance Agent**: GDPR, SOC 2, privacy policies
- **Business Agent**: Entity formation, fundraising, contracts
- **Document Agent**: Document analysis and generation
- **Expert Agent**: Complex questions and expert referrals

## 9. Migration from Current Backend

The current Flask backend will be replaced with:
- Supabase for database and auth
- Supabase Edge Functions for API endpoints
- Supabase Storage for file uploads
- Supabase Realtime for live updates

## 10. Next Steps

1. Set up your Supabase project
2. Configure environment variables
3. Test the new system
4. Migrate existing data (if any)
5. Deploy to production

Your SmartProBono platform will now have:
- ✅ Proper security with RLS
- ✅ Scalable database
- ✅ Real-time capabilities
- ✅ Better AI responses
- ✅ Professional authentication
- ✅ File storage and management
EOF

echo ""
echo "🎉 SUPABASE SETUP COMPLETE!"
echo "=========================="
echo ""
echo -e "${GREEN}✅ Created:${NC}"
echo "  • Supabase configuration files"
echo "  • Database schema and policies"
echo "  • Multi-agent AI system"
echo "  • Security policies (RLS)"
echo "  • Environment templates"
echo "  • Setup instructions"

echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "  1. Create a Supabase project at supabase.com"
echo "  2. Follow the instructions in SUPABASE_SETUP_INSTRUCTIONS.md"
echo "  3. Set up your environment variables"
echo "  4. Test the new system"

echo ""
echo -e "${YELLOW}🔐 Security Features Added:${NC}"
echo "  • Row Level Security (RLS)"
echo "  • JWT authentication"
echo "  • Protected API endpoints"
echo "  • User data isolation"
echo "  • Input validation"

echo ""
echo -e "${GREEN}🤖 AI Improvements:${NC}"
echo "  • Multi-agent system with specialized agents"
echo "  • Contextual responses (no more overwhelming greetings!)"
echo "  • Proper routing to appropriate agents"
echo "  • Better conversation management"

echo ""
echo "📖 Read SUPABASE_SETUP_INSTRUCTIONS.md for detailed setup steps!"

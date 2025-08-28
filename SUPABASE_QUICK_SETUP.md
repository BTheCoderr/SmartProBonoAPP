# 🚀 Supabase Quick Setup Guide

## 📋 **Current Status**
✅ You're on the Supabase "Create a new project" page  
✅ Database password: `Smartprobono2025$$`  
✅ Project name: "Smartprobono.org's Project"  
✅ Region: East US (North Virginia)  

## 🔧 **Complete the Setup**

### **1. Finalize Project Creation**
- ✅ **Organization**: smartprobono (Free)
- ✅ **Project name**: Smartprobono.org's Project
- ✅ **Database Password**: `Smartprobono2025$$`
- ✅ **Region**: East US (North Virginia)

**Click "Create new project"** - This will take 2-3 minutes to set up.

### **2. Get Your Credentials**
Once your project is created, you'll need to get your API keys:

1. **Go to Settings > API** in your Supabase dashboard
2. **Copy these values:**
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **Anon public key** (starts with `eyJ...`)
   - **Service role key** (starts with `eyJ...` - keep this secret!)

### **3. Set Up Environment Variables**
Create a `.env` file in your project root:

```bash
# Supabase Configuration
REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your_anon_key_here
REACT_APP_SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Keep your existing email config
SMTP_SERVER=smtp.zoho.com
SMTP_PORT=587
SMTP_USERNAME=info@smartprobono.org
SMTP_PASSWORD=Monkey2123$$
```

### **4. Set Up Database Schema**
1. **Go to SQL Editor** in your Supabase dashboard
2. **Create a new query**
3. **Copy and paste this SQL:**

```sql
-- Create tables
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email varchar UNIQUE NOT NULL,
  full_name varchar,
  avatar_url varchar,
  role varchar DEFAULT 'user',
  is_premium boolean DEFAULT false,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

CREATE TABLE conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  title varchar,
  model_used varchar,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

CREATE TABLE messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id uuid REFERENCES conversations(id) ON DELETE CASCADE,
  content text NOT NULL,
  role varchar NOT NULL,
  model_used varchar,
  created_at timestamp DEFAULT now()
);

CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  title varchar NOT NULL,
  file_path varchar,
  file_type varchar,
  file_size integer,
  content text,
  metadata jsonb,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

CREATE TABLE feedback (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  conversation_id uuid REFERENCES conversations(id) ON DELETE CASCADE,
  rating integer CHECK (rating >= 1 AND rating <= 5),
  feedback_text text,
  created_at timestamp DEFAULT now()
);

CREATE TABLE beta_signups (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email varchar UNIQUE NOT NULL,
  status varchar DEFAULT 'pending',
  created_at timestamp DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE beta_signups ENABLE ROW LEVEL SECURITY;

-- Create security policies
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own conversations" ON conversations
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own conversations" ON conversations
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own conversations" ON conversations
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own conversations" ON conversations
  FOR DELETE USING (auth.uid() = user_id);

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

CREATE POLICY "Users can view own documents" ON documents
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own documents" ON documents
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own documents" ON documents
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own documents" ON documents
  FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own feedback" ON feedback
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own feedback" ON feedback
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Anyone can view beta signups" ON beta_signups
  FOR SELECT USING (true);

CREATE POLICY "Anyone can create beta signup" ON beta_signups
  FOR INSERT WITH CHECK (true);
```

4. **Click "Run"** to execute the SQL

### **5. Set Up Storage (Optional)**
1. **Go to Storage** in your Supabase dashboard
2. **Create a new bucket** called `documents`
3. **Set it to public** if you want public access
4. **Or keep it private** and use RLS policies

### **6. Test the Setup**
1. **Start your app:**
   ```bash
   ./start_mvp.sh
   ```

2. **Go to:** http://localhost:3002/legal-chat

3. **Test the improved AI:**
   - Say "hello" → Should get brief, friendly response
   - Ask "What is GDPR?" → Should get detailed compliance guidance
   - Ask "Should I form an LLC?" → Should get business law comparison

## 🎉 **You're All Set!**

Once you complete these steps, your SmartProBono MVP will have:

✅ **Enterprise-grade security** with Supabase  
✅ **Intelligent AI system** with specialized agents  
✅ **Professional database** with proper schema  
✅ **Scalable architecture** ready for production  
✅ **Better user experience** with contextual responses  

## 🚀 **Ready for Pilot Testing!**

Your platform is now ready for serious pilot testing with real users!

---

**Next:** Complete the Supabase project creation, then follow steps 2-6 above.

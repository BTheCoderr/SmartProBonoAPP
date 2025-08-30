# 🗄️ LangGraph Database Setup Guide

## 🚨 **Current Issue**
You're absolutely right! We created all the advanced LangGraph code, but **the database tables don't exist yet**. The system is trying to connect to Supabase tables that haven't been created.

## 🔧 **Quick Fix - Set Up Database Tables**

### **Step 1: Create Tables in Supabase**

1. **Go to your Supabase dashboard**: https://supabase.com/dashboard
2. **Navigate to your project**: "Smartprobono.org's Project"
3. **Go to SQL Editor** (left sidebar)
4. **Click "New Query"**
5. **Copy and paste this SQL**:

```sql
-- LangGraph Service Tables for SmartProBono
-- Run this SQL in your Supabase SQL editor

-- Case intakes table
CREATE TABLE IF NOT EXISTS case_intakes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid,
    raw_text text NOT NULL,
    summary text,
    case_type text,
    specialist_analysis text,
    plain_english_answer text,
    meta jsonb DEFAULT '{}'::jsonb,
    status text DEFAULT 'started',
    current_step text,
    needs_revision boolean DEFAULT false,
    revision_count integer DEFAULT 0,
    max_revisions integer DEFAULT 2,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Human review requests table
CREATE TABLE IF NOT EXISTS human_reviews (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id text NOT NULL,
    node_name text NOT NULL,
    state jsonb NOT NULL,
    review_type text NOT NULL,
    status text DEFAULT 'pending',
    created_at timestamptz DEFAULT now(),
    timeout_at timestamptz,
    human_feedback text,
    modified_state jsonb,
    reviewed_at timestamptz
);

-- LangGraph checkpoints table
CREATE TABLE IF NOT EXISTS langgraph_checkpoints (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id text NOT NULL,
    checkpoint_data jsonb NOT NULL,
    created_at timestamptz DEFAULT now(),
    metadata jsonb DEFAULT '{}'::jsonb
);

-- Lawyer profiles table
CREATE TABLE IF NOT EXISTS lawyer_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name text NOT NULL,
    email text,
    specialization text,
    is_active boolean DEFAULT true,
    created_at timestamptz DEFAULT now()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_case_intakes_user_id ON case_intakes(user_id);
CREATE INDEX IF NOT EXISTS idx_case_intakes_status ON case_intakes(status);
CREATE INDEX IF NOT EXISTS idx_case_intakes_created_at ON case_intakes(created_at);
CREATE INDEX IF NOT EXISTS idx_human_reviews_thread_id ON human_reviews(thread_id);
CREATE INDEX IF NOT EXISTS idx_human_reviews_status ON human_reviews(status);
CREATE INDEX IF NOT EXISTS idx_langgraph_checkpoints_thread_id ON langgraph_checkpoints(thread_id);

-- Enable Row Level Security
ALTER TABLE case_intakes ENABLE ROW LEVEL SECURITY;
ALTER TABLE human_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE langgraph_checkpoints ENABLE ROW LEVEL SECURITY;
ALTER TABLE lawyer_profiles ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view own case intakes" ON case_intakes
    FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can create case intakes" ON case_intakes
    FOR INSERT WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can update own case intakes" ON case_intakes
    FOR UPDATE USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Service role can manage all case intakes" ON case_intakes
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role can manage human reviews" ON human_reviews
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role can manage checkpoints" ON langgraph_checkpoints
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Anyone can view lawyer profiles" ON lawyer_profiles
    FOR SELECT USING (true);

CREATE POLICY "Service role can manage lawyer profiles" ON lawyer_profiles
    FOR ALL USING (auth.role() = 'service_role');

-- Insert sample lawyer data
INSERT INTO lawyer_profiles (full_name, email, specialization, is_active) VALUES
('John Smith', 'john.smith@law.com', 'Criminal Law', true),
('Sarah Johnson', 'sarah.johnson@law.com', 'Housing Law', true),
('Michael Brown', 'michael.brown@law.com', 'Family Law', true),
('Emily Davis', 'emily.davis@law.com', 'Employment Law', true),
('David Wilson', 'david.wilson@law.com', 'Immigration Law', true)
ON CONFLICT (email) DO NOTHING;
```

6. **Click "Run"** to execute the SQL

### **Step 2: Test the Connection**

After creating the tables, test the connection:

```bash
python3.13 test_supabase_connection.py
```

### **Step 3: Start the LangGraph Service**

```bash
./start_smartprobono.sh
```

### **Step 4: Test the Advanced System**

```bash
# Test the advanced intake
curl -X POST http://localhost:8010/intake/advanced \
  -H 'Content-Type: application/json' \
  -d '{"user_id": null, "full_text": "I was arrested for shoplifting", "meta": {}}'

# Check human reviews
curl http://localhost:8010/human-reviews/pending

# Get system info
curl http://localhost:8010/graph/info
```

## 🎯 **What This Sets Up**

### **Database Tables Created:**
- **`case_intakes`** - Main intake tracking with all workflow state
- **`human_reviews`** - Human-in-the-loop review requests
- **`langgraph_checkpoints`** - State persistence for durable execution
- **`lawyer_profiles`** - Lawyer directory for specialist routing

### **Security Features:**
- **Row Level Security (RLS)** enabled on all tables
- **Service role policies** for LangGraph system access
- **User isolation** for case intakes
- **Proper indexing** for performance

### **Advanced Features Enabled:**
- ✅ **Multi-agent workflow** with specialist routing
- ✅ **Human-in-the-loop** quality control
- ✅ **Checkpointing** for durable execution
- ✅ **Parallel execution** of specialists
- ✅ **State management** across the entire workflow

## 🚀 **After Setup**

Once you run the SQL and start the service, you'll have:

1. **Working database connection** to Supabase
2. **Advanced LangGraph system** with all features
3. **Human review system** for quality control
4. **Checkpointing** for failure recovery
5. **Parallel specialist execution** for comprehensive analysis

## 🎉 **Success!**

After completing these steps, your SmartProBono system will be **fully connected** with:
- ✅ Supabase database with proper tables
- ✅ Advanced LangGraph multi-agent system
- ✅ All official LangGraph patterns implemented
- ✅ Production-ready architecture

The system will be able to handle complex legal workflows with multiple AI agents working together, just like the official LangGraph documentation examples!

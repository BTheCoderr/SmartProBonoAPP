#!/usr/bin/env python3
"""
Setup LangGraph Database Tables in Supabase
This script creates all the necessary tables for the advanced LangGraph system
"""

import requests
import json
import os
from typing import Dict, Any

# Supabase configuration
SUPABASE_URL = "https://ewtcvsohdgkthuyajyyk.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjQxMDQ2NCwiZXhwIjoyMDcxOTg2NDY0fQ._9KbvHJ6JohciGAqwHlQGerGr2xkHEr36OmSB5oQjng"

def execute_sql(sql: str) -> Dict[str, Any]:
    """Execute SQL in Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {"sql": sql}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_langgraph_tables():
    """Create all LangGraph tables"""
    
    print("🚀 Setting up LangGraph Database Tables")
    print("=" * 50)
    
    # SQL for creating LangGraph tables
    sql = """
    -- LangGraph Service Tables for SmartProBono
    
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
    """
    
    print("📊 Creating LangGraph tables...")
    result = execute_sql(sql)
    
    if result["success"]:
        print("✅ LangGraph tables created successfully!")
    else:
        print(f"❌ Error creating tables: {result['error']}")
        return False
    
    # Insert sample lawyer data
    print("\n👥 Adding sample lawyer data...")
    sample_lawyers_sql = """
    INSERT INTO lawyer_profiles (full_name, email, specialization, is_active) VALUES
    ('John Smith', 'john.smith@law.com', 'Criminal Law', true),
    ('Sarah Johnson', 'sarah.johnson@law.com', 'Housing Law', true),
    ('Michael Brown', 'michael.brown@law.com', 'Family Law', true),
    ('Emily Davis', 'emily.davis@law.com', 'Employment Law', true),
    ('David Wilson', 'david.wilson@law.com', 'Immigration Law', true)
    ON CONFLICT (email) DO NOTHING;
    """
    
    result = execute_sql(sample_lawyers_sql)
    if result["success"]:
        print("✅ Sample lawyer data added!")
    else:
        print(f"⚠️  Warning: Could not add sample data: {result['error']}")
    
    return True

def test_connection():
    """Test the database connection"""
    print("\n🔍 Testing database connection...")
    
    # Test basic connection
    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {"apikey": SUPABASE_SERVICE_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Supabase connection working")
        else:
            print(f"❌ Supabase connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Test table access
    url = f"{SUPABASE_URL}/rest/v1/case_intakes?select=*&limit=1"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ case_intakes table accessible")
        else:
            print(f"❌ case_intakes table error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Table access error: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 LangGraph Database Setup")
    print("=" * 50)
    
    # Test connection first
    if not test_connection():
        print("❌ Database connection failed. Please check your Supabase configuration.")
        return
    
    # Create tables
    if create_langgraph_tables():
        print("\n🎉 LangGraph database setup complete!")
        print("\n📋 What was created:")
        print("  • case_intakes - Main intake tracking table")
        print("  • human_reviews - Human-in-the-loop review requests")
        print("  • langgraph_checkpoints - State persistence")
        print("  • lawyer_profiles - Lawyer directory")
        print("  • Indexes and RLS policies for security")
        
        print("\n🚀 Next steps:")
        print("  1. Start the LangGraph service: ./start_smartprobono.sh")
        print("  2. Test the advanced intake: curl -X POST http://localhost:8010/intake/advanced")
        print("  3. Check human reviews: curl http://localhost:8010/human-reviews/pending")
    else:
        print("❌ Database setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()

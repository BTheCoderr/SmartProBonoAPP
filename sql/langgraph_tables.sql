-- LangGraph Service Tables for SmartProBono
-- Run this SQL in your Supabase SQL editor

create table if not exists case_intakes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  raw_text text not null,
  summary text,
  meta jsonb default '{}'::jsonb,
  status text default 'started',
  created_at timestamptz default now()
);

create table if not exists lawyer_profiles (
  id uuid primary key default gen_random_uuid(),
  full_name text not null,
  email text,
  is_active boolean default true,
  created_at timestamptz default now()
);

-- Add some sample lawyer data for testing
insert into lawyer_profiles (full_name, email, is_active) values
('John Smith', 'john.smith@law.com', true),
('Sarah Johnson', 'sarah.johnson@law.com', true),
('Michael Brown', 'michael.brown@law.com', true)
on conflict do nothing;

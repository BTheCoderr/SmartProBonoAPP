-- SmartProBono Document AI Schema
-- Run this in your Supabase SQL editor

-- Enable vector extension for embeddings
create extension if not exists vector;

-- Documents table
create table if not exists documents (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id),
  title text,
  storage_path text not null,
  status text not null default 'uploaded',
  language text default 'eng',
  created_at timestamptz default now()
);

-- Document text chunks
create table if not exists doc_chunks (
  id bigserial primary key,
  document_id uuid references documents(id) on delete cascade,
  chunk_index int not null,
  text text not null
);

-- Document embeddings for semantic search
create table if not exists doc_embeddings (
  chunk_id bigint primary key references doc_chunks(id) on delete cascade,
  embedding vector(384)  -- for all-MiniLM-L6-v2
);

-- Enable Row Level Security
alter table documents enable row level security;
alter table doc_chunks enable row level security;
alter table doc_embeddings enable row level security;

-- RLS Policies for documents
create policy "own docs read" on documents for select using (auth.uid() = user_id);
create policy "own docs insert" on documents for insert with check (auth.uid() = user_id);
create policy "own docs update" on documents for update using (auth.uid() = user_id);

-- RLS Policies for doc_chunks
create policy "own chunks read" on doc_chunks for select using (
  exists(select 1 from documents d where d.id = doc_chunks.document_id and d.user_id = auth.uid())
);
create policy "own chunks insert" on doc_chunks for insert with check (
  exists(select 1 from documents d where d.id = document_id and d.user_id = auth.uid())
);

-- RLS Policies for doc_embeddings
create policy "own embeds read" on doc_embeddings for select using (
  exists(
    select 1 from doc_chunks c join documents d on d.id = c.document_id
    where c.id = doc_embeddings.chunk_id and d.user_id = auth.uid()
  )
);
create policy "own embeds insert" on doc_embeddings for insert with check (
  exists(
    select 1 from doc_chunks c join documents d on d.id = c.document_id
    where c.id = chunk_id and d.user_id = auth.uid()
  )
);

-- Create storage bucket for documents
-- Note: Run this in Supabase dashboard or via API
-- insert into storage.buckets (id, name, public) values ('docs', 'docs', false);

-- Storage policies (run these after creating the bucket)
-- create policy "Users can upload documents" on storage.objects for insert with check (
--   bucket_id = 'docs' and auth.uid()::text = (storage.foldername(name))[1]
-- );
-- create policy "Users can view own documents" on storage.objects for select using (
--   bucket_id = 'docs' and auth.uid()::text = (storage.foldername(name))[1]
-- );

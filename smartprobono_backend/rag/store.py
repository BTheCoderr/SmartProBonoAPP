"""
Haystack document store configuration for Supabase pgvector
"""
import os
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

def get_document_store() -> PgvectorDocumentStore:
    """Get configured pgvector document store for Supabase"""
    connection_string = os.getenv("PG_CONN_STR")
    
    if not connection_string:
        raise ValueError("PG_CONN_STR environment variable is required")
    
    # Configure pgvector document store
    ds = PgvectorDocumentStore(
        connection_string=connection_string,
        embedding_dimension=384,      # all-MiniLM-L6-v2 default
        vector_function="cosine_similarity",
        recreate_table=False,         # set True only for first run/dev resets
        search_strategy="hnsw",       # ANN; or "exact"
        table_name="spb_documents"
    )
    return ds

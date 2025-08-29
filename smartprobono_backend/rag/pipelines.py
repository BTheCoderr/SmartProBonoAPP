"""
Haystack RAG pipelines for document ingestion and querying
"""
from haystack import Pipeline
from haystack.components.converters.pypdf import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.components.writers import DocumentWriter
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.components.generators.ollama import OllamaGenerator
from .store import get_document_store
import os

# Configuration
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")

# Legal RAG prompt template
LEGAL_PROMPT_TEMPLATE = """
You are a legal information assistant for SmartProBono. Use only the provided context to answer questions.

IMPORTANT GUIDELINES:
- Provide general legal information only
- Do NOT give specific legal advice
- If you're not confident, say you'll escalate to a human attorney
- Always cite sources using [1], [2], etc.
- Be clear about limitations and when to consult an attorney

Question: {{query}}

{% if documents %}
Context from legal documents:
{% for d in documents %}
[{{loop.index}}] {{ d.content[:1200] }}
Source: {{ d.meta.get('filename', 'Unknown') }}
{% endfor %}
{% endif %}

Answer with concise, plain English and list citations as [1], [2], etc.
If the context doesn't contain enough information, say so and recommend consulting an attorney.
"""

def build_indexing_pipeline() -> Pipeline:
    """Build pipeline for ingesting and indexing documents"""
    ds = get_document_store()
    pipeline = Pipeline()
    
    # Document processing components
    pipeline.add_component("pdf", PyPDFToDocument())
    pipeline.add_component("clean", DocumentCleaner())
    pipeline.add_component("split", DocumentSplitter(
        split_by="sentence", 
        split_length=6, 
        split_overlap=1
    ))
    pipeline.add_component("embed", SentenceTransformersDocumentEmbedder(
        model=EMBED_MODEL
    ))
    pipeline.add_component("write", DocumentWriter(document_store=ds))

    # Connect the pipeline
    pipeline.connect("pdf", "clean")
    pipeline.connect("clean", "split")
    pipeline.connect("split", "embed")
    pipeline.connect("embed", "write")
    
    return pipeline

def build_query_pipeline() -> Pipeline:
    """Build pipeline for querying documents with RAG"""
    ds = get_document_store()
    pipeline = Pipeline()
    
    # Query processing components
    pipeline.add_component("q_embed", SentenceTransformersTextEmbedder(
        model=EMBED_MODEL
    ))
    pipeline.add_component("retrieve", PgvectorEmbeddingRetriever(
        document_store=ds, 
        top_k=6
    ))
    pipeline.add_component("prompt", PromptBuilder(
        template=LEGAL_PROMPT_TEMPLATE
    ))
    pipeline.add_component("llm", OllamaGenerator(
        model=OLLAMA_MODEL, 
        url=OLLAMA_URL
    ))

    # Connect the pipeline
    pipeline.connect("q_embed.embedding", "retrieve.query_embedding")
    pipeline.connect("retrieve.documents", "prompt.documents")
    pipeline.connect("prompt", "llm")
    
    return pipeline

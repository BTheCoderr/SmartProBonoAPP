"""
Instructor embeddings for legal case law semantic search.
Uses the free instructor-large model for generating embeddings.
"""

import logging
from typing import List, Union
import numpy as np

logger = logging.getLogger(__name__)

class InstructorEmbeddings:
    """Instructor embeddings for legal text."""
    
    def __init__(self, model_name: str = "hkunlp/instructor-large"):
        self.model_name = model_name
        self._model = None
        self._tokenizer = None
        
    def _load_model(self):
        """Load the instructor model (lazy loading)."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
                logger.info(f"Loaded instructor model: {self.model_name}")
            except ImportError:
                logger.warning("sentence-transformers not available, using fallback embeddings")
                self._model = None
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Args:
            texts: List of text documents to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
            
        self._load_model()
        
        if self._model is None:
            # Fallback to simple embeddings
            return self._fallback_embeddings(texts)
        
        try:
            embeddings = self._model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return self._fallback_embeddings(texts)
    
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query.
        
        Args:
            query: Query text to embed
            
        Returns:
            Embedding vector
        """
        embeddings = self.embed_documents([query])
        return embeddings[0] if embeddings else []
    
    def _fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Fallback embeddings when instructor model is not available."""
        logger.info("Using fallback embeddings (random vectors)")
        
        # Generate random embeddings as fallback
        embeddings = []
        for text in texts:
            # Create a simple hash-based embedding
            text_hash = hash(text) % (2**32)
            np.random.seed(text_hash)
            embedding = np.random.randn(384).tolist()  # 384-dimensional vector
            embeddings.append(embedding)
        
        return embeddings

def get_embeddings() -> InstructorEmbeddings:
    """Get a singleton instance of InstructorEmbeddings."""
    if not hasattr(get_embeddings, '_instance'):
        get_embeddings._instance = InstructorEmbeddings()
    return get_embeddings._instance

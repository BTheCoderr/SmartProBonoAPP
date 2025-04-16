"""
Vector Database Manager for SmartProBono
This module manages the vector database for legal knowledge retrieval.
"""

import os
import json
import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import uuid
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDatabaseManager:
    """
    Manages a vector database for legal knowledge retrieval, including
    indexing, searching, and maintaining metadata.
    """
    
    def __init__(self, 
                 data_dir: str = 'ai/vector_db',
                 model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize the vector database manager.
        
        Args:
            data_dir: Directory to store vector database files
            model_name: Name of the embedding model to use
        """
        self.data_dir = data_dir
        self.index_dir = os.path.join(data_dir, 'indexes')
        self.metadata_dir = os.path.join(data_dir, 'metadata')
        
        os.makedirs(self.index_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        # Initialize embedding model
        self.model_name = model_name
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            self.model = None
        
        # Keep track of index metadata
        self.metadata = {}
        self.loaded_indexes = {}
        
    def create_index(self, name: str, data_file: str, 
                    dimension: int = 384, 
                    index_type: str = 'Flat') -> bool:
        """
        Create a new vector index from a data file.
        
        Args:
            name: Name of the index
            data_file: Path to the data file (JSON with 'text' field)
            dimension: Embedding dimension
            index_type: Type of FAISS index to create ('Flat' or 'IVF')
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Creating index '{name}' from {data_file}")
        
        if not os.path.exists(data_file):
            logger.error(f"Data file not found: {data_file}")
            return False
        
        if self.model is None:
            logger.error("Embedding model not loaded")
            return False
        
        try:
            # Load data
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not data:
                logger.error("No data in file")
                return False
                
            texts = [item['text'] for item in data]
            metadata = [{'id': item.get('id', f"doc_{i}"), 
                        'metadata': item.get('metadata', {})} 
                       for i, item in enumerate(data)]
                
            # Create embeddings
            logger.info(f"Generating embeddings for {len(texts)} documents")
            embeddings = self.model.encode(texts, show_progress_bar=True, 
                                          convert_to_numpy=True)
            
            # Create index
            if index_type == 'Flat':
                index = faiss.IndexFlatL2(dimension)
            elif index_type == 'IVF':
                # IVF requires training, so we use a more complex setup
                quantizer = faiss.IndexFlatL2(dimension)
                n_cells = min(int(len(texts) ** 0.5), 100)  # Rule of thumb
                index = faiss.IndexIVFFlat(quantizer, dimension, n_cells)
                
                # Train on the data
                if len(texts) > n_cells:
                    index.train(embeddings)
                else:
                    logger.warning("Not enough data to train IVF index, falling back to Flat")
                    index = faiss.IndexFlatL2(dimension)
            else:
                logger.error(f"Unknown index type: {index_type}")
                return False
                
            # Add vectors to index
            index.add(embeddings)
            
            # Save index
            index_path = os.path.join(self.index_dir, f"{name}.index")
            faiss.write_index(index, index_path)
            
            # Save metadata
            metadata_path = os.path.join(self.metadata_dir, f"{name}.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
                
            # Update metadata record
            self.metadata[name] = {
                'name': name,
                'type': index_type,
                'documents': len(texts),
                'dimension': dimension,
                'created_at': pd.Timestamp.now().isoformat(),
                'model': self.model_name
            }
            
            # Save metadata record
            self._save_metadata_record()
            
            logger.info(f"Successfully created index '{name}' with {len(texts)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error creating index: {str(e)}")
            return False
            
    def load_index(self, name: str) -> bool:
        """
        Load an index into memory.
        
        Args:
            name: Name of the index to load
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Loading index '{name}'")
        
        if name in self.loaded_indexes:
            logger.info(f"Index '{name}' already loaded")
            return True
            
        index_path = os.path.join(self.index_dir, f"{name}.index")
        metadata_path = os.path.join(self.metadata_dir, f"{name}.json")
        
        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            logger.error(f"Index files not found for '{name}'")
            return False
            
        try:
            # Load index
            index = faiss.read_index(index_path)
            
            # Load metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                
            # Store in memory
            self.loaded_indexes[name] = {
                'index': index,
                'metadata': metadata
            }
            
            logger.info(f"Successfully loaded index '{name}'")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")
            return False
            
    def search(self, query: str, index_name: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search the vector database for relevant documents.
        
        Args:
            query: Query string
            index_name: Name of the index to search
            k: Number of results to return
            
        Returns:
            List of results with document text and metadata
        """
        logger.info(f"Searching index '{index_name}' for: {query}")
        
        if self.model is None:
            logger.error("Embedding model not loaded")
            return []
            
        # Load index if not already loaded
        if index_name not in self.loaded_indexes:
            success = self.load_index(index_name)
            if not success:
                logger.error(f"Failed to load index '{index_name}'")
                return []
                
        index_data = self.loaded_indexes[index_name]
        index = index_data['index']
        metadata = index_data['metadata']
        
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])
            
            # Search index
            distances, indices = index.search(query_embedding, k)
            
            # Format results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < 0 or idx >= len(metadata):
                    continue  # Index out of bounds
                    
                doc_metadata = metadata[idx]
                
                results.append({
                    'id': doc_metadata['id'],
                    'metadata': doc_metadata['metadata'],
                    'distance': float(distances[0][i]),
                    'score': 1.0 / (1.0 + float(distances[0][i]))  # Convert distance to similarity score
                })
                
            logger.info(f"Found {len(results)} results for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching index: {str(e)}")
            return []
    
    def search_by_jurisdiction(self, query: str, jurisdiction: str, 
                             index_name: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for documents in a specific jurisdiction.
        
        Args:
            query: Query string
            jurisdiction: Jurisdiction to filter by
            index_name: Name of the index to search
            k: Number of results to return
            
        Returns:
            List of results with document text and metadata
        """
        # First, do a broader search
        results = self.search(query, index_name, k=k*3)  # Get more results to filter
        
        if not results:
            return []
            
        # Filter by jurisdiction
        filtered_results = [r for r in results 
                           if r['metadata'].get('jurisdiction', '').lower() == jurisdiction.lower()]
        
        # If no matches for jurisdiction, return general results
        if not filtered_results:
            logger.info(f"No results for jurisdiction '{jurisdiction}', returning general results")
            return results[:k]
            
        # Return top-k jurisdiction-specific results
        return filtered_results[:k]
    
    def extract_citations(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract citations from search results.
        
        Args:
            results: List of search results
            
        Returns:
            List of extracted citations
        """
        citations = []
        seen_citations = set()  # Track already processed citations to avoid duplicates
        
        for result in results:
            # Extract any citation information from the result
            citation_text = result.get('text', '')
            citation_type = result.get('type', 'Unknown')
            
            # Skip if this exact citation has already been processed
            if citation_text in seen_citations:
                continue
                
            # Extract jurisdiction information
            jurisdiction = result.get('jurisdiction', 'Unknown')
            
            # Create basic citation
            citation = {
                'id': result.get('id', str(uuid.uuid4())),
                'text': citation_text,
                'type': citation_type,
                'jurisdiction': jurisdiction,
                'source': result.get('source', 'vector_search')
            }
            
            # Add additional metadata based on citation type
            if citation_type.lower() == 'case law' or 'v.' in citation_text:
                # Extract case name, reporter, etc. if available
                parts = citation_text.split(',', 1)
                if len(parts) > 1:
                    citation['case_name'] = parts[0].strip()
                    citation['citation_detail'] = parts[1].strip()
                    
                # Extract year if available
                year_match = re.search(r'\((\d{4})\)', citation_text)
                if year_match:
                    citation['year'] = year_match.group(1)
                    
                # Generate URL for case law if not present
                if 'url' not in citation:
                    case_name = citation.get('case_name', '').replace(' ', '+')
                    citation['url'] = f"https://caselaw.findlaw.com/search?query={case_name}"
                    
            elif citation_type.lower() == 'statute':
                # Extract code and section information
                code_match = re.search(r'([A-Za-z\.]+)\s+Code', citation_text)
                section_match = re.search(r'§\s+(\d+[\w\-\.]*)', citation_text)
                
                if code_match:
                    citation['code'] = code_match.group(1)
                if section_match:
                    citation['section'] = section_match.group(1)
                    
                # Generate URL for statute if not present
                if 'url' not in citation and jurisdiction and citation.get('section'):
                    jurisdiction_slug = jurisdiction.lower().replace(' ', '-')
                    section_slug = citation.get('section', '').replace('.', '-')
                    citation['url'] = f"https://www.law.cornell.edu/statutes/{jurisdiction_slug}/section/{section_slug}"
                    
            elif citation_type.lower() == 'regulation':
                # Extract CFR information
                cfr_match = re.search(r'(\d+)\s+C\.F\.R\.\s+§\s+(\d+[\.\d+]*)', citation_text)
                if cfr_match:
                    citation['title'] = cfr_match.group(1)
                    citation['section'] = cfr_match.group(2)
                    
                # Generate URL for CFR if not present
                if 'url' not in citation and citation.get('title') and citation.get('section'):
                    title = citation.get('title', '')
                    section = citation.get('section', '')
                    part = section.split('.')[0] if '.' in section else section
                    citation['url'] = f"https://www.ecfr.gov/current/title-{title}/part-{part}/section-{section}"
                    
            elif citation_type.lower() == 'constitution':
                # Extract constitutional information
                const_match = re.search(r'([A-Za-z\.]+)\s+Const\.\s+art\.\s+([IVX]+),\s+§\s+(\d+)', citation_text)
                if const_match:
                    citation['constitution'] = const_match.group(1)
                    citation['article'] = const_match.group(2)
                    citation['section'] = const_match.group(3)
                    
                # Generate URL for constitution if not present
                if 'url' not in citation and citation.get('article') and citation.get('section'):
                    article = self._roman_to_int(citation.get('article', 'I'))
                    section = citation.get('section', '1')
                    citation['url'] = f"https://constitution.congress.gov/browse/article-{article}/section-{section}/"
            
            # Add content snippet if available
            content = result.get('content', '')
            if content:
                # Limit content to reasonable size
                if len(content) > 500:
                    content = content[:500] + "..."
                citation['content'] = content
            
            # Add citation to results and track as seen
            citations.append(citation)
            seen_citations.add(citation_text)
            
        return citations
    
    def get_available_indexes(self) -> List[Dict[str, Any]]:
        """
        Get a list of available indexes.
        
        Returns:
            List of index metadata
        """
        return list(self.metadata.values())
    
    def _save_metadata_record(self) -> bool:
        """
        Save the metadata record to disk.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            metadata_record_path = os.path.join(self.data_dir, 'indexes.json')
            with open(metadata_record_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving metadata record: {str(e)}")
            return False
            
    def _load_metadata_record(self) -> bool:
        """Load the metadata record from disk."""
        metadata_record_path = os.path.join(self.data_dir, 'indexes.json')
        
        if not os.path.exists(metadata_record_path):
            logger.warning("No metadata record found")
            return False
            
        try:
            with open(metadata_record_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            return True
        except Exception as e:
            logger.error(f"Error loading metadata record: {str(e)}")
            return False
            
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID from any available index.
        
        Args:
            doc_id: The unique ID of the document to retrieve
            
        Returns:
            The document data or None if not found
        """
        try:
            # Check all available indexes
            for index_name, index_info in self.metadata.get('indexes', {}).items():
                index_path = os.path.join(self.data_dir, f"{index_name}.index")
                if not os.path.exists(index_path):
                    continue
                    
                # Load the index
                if not self.load_index(index_name):
                    continue
                    
                # Load documents metadata file for this index
                docs_path = os.path.join(self.data_dir, f"{index_name}_docs.json")
                if not os.path.exists(docs_path):
                    continue
                    
                try:
                    with open(docs_path, 'r', encoding='utf-8') as f:
                        docs = json.load(f)
                        
                    # Check if doc_id exists in this index
                    if doc_id in docs:
                        return docs[doc_id]
                except Exception as e:
                    logger.error(f"Error reading documents for index {index_name}: {str(e)}")
                    continue
            
            # Document not found in any index
            return None
        except Exception as e:
            logger.error(f"Error retrieving document by ID: {str(e)}")
            return None

    def _roman_to_int(self, roman: str) -> int:
        """
        Convert Roman numeral to integer.
        
        Args:
            roman: Roman numeral string
            
        Returns:
            Integer value
        """
        values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }
        
        result = 0
        prev_value = 0
        
        for char in reversed(roman.upper()):
            if char not in values:
                # Handle invalid characters by returning position 1
                return 1
                
            current_value = values[char]
            if current_value >= prev_value:
                result += current_value
            else:
                result -= current_value
            prev_value = current_value
            
        return max(1, result)  # Ensure at least 1 is returned

# Load environment-specific configuration (if needed)
def get_vector_db_config():
    """Get configuration for vector database from environment variables."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    return {
        'data_dir': os.environ.get('VECTOR_DB_DIR', 'ai/vector_db'),
        'model_name': os.environ.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    }

# Example usage
if __name__ == "__main__":
    config = get_vector_db_config()
    
    # Initialize vector database manager
    db_manager = VectorDatabaseManager(**config)
    
    # Create index from example data
    data_file = os.path.join('ai/data/processed', 'vector_db_chunks.json')
    if os.path.exists(data_file):
        db_manager.create_index('legal_knowledge', data_file)
    
    # Example search
    results = db_manager.search("What are my rights as a tenant?", "legal_knowledge")
    for result in results:
        print(f"Score: {result['score']:.4f}")
        print(f"Title: {result['metadata'].get('title', 'Untitled')}")
        print(f"Jurisdiction: {result['metadata'].get('jurisdiction', 'Unknown')}")
        print("-" * 50) 
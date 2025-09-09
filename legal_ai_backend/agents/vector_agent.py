"""
Vector Agent - Searches local case embeddings using ChromaDB.
Provides fast access to pre-embedded case law and legal documents.
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

@dataclass
class VectorSearchResult:
    """Structured result from vector search."""
    documents: List[str]
    metadatas: List[Dict[str, Any]]
    distances: List[float]
    ids: List[str]
    query: str
    collection_name: str

class VectorAgent:
    """Agent responsible for searching local case embeddings."""
    
    def __init__(self, persist_directory: str = "./vectorstore/chroma_data"):
        """
        Initialize vector agent with ChromaDB client.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        self.collection_name = "harvard_cases"
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Ensure the collection exists, create if not."""
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Using existing collection: {self.collection_name}")
        except Exception:
            # Create new collection if it doesn't exist
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Harvard Case Law Embeddings"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def build_search_query(self, context: Dict[str, Any]) -> str:
        """
        Build search query from context for vector search.
        
        Args:
            context: Intake context with legal information
            
        Returns:
            Search query string
        """
        topic = context.get("topic", "")
        keywords = context.get("keywords", [])
        case_type = context.get("case_type", "")
        suggested_charges = context.get("suggested_charges", [])
        
        # Build query components
        query_parts = []
        
        # Add topic
        if topic and topic != "general":
            query_parts.append(topic)
        
        # Add keywords
        query_parts.extend(keywords)
        
        # Add case type
        if case_type and case_type != "general":
            query_parts.append(case_type)
        
        # Add suggested charges
        if suggested_charges:
            charge_text = " ".join(suggested_charges[:2])  # First 2 charges
            query_parts.append(charge_text)
        
        # Join and clean
        query = " ".join(query_parts)
        query = " ".join(list(dict.fromkeys(query.split())))
        
        logger.info(f"Built vector search query: '{query}'")
        return query
    
    def search_cases(
        self, 
        context: Dict[str, Any], 
        n_results: int = 5,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> VectorSearchResult:
        """
        Search for cases using vector similarity.
        
        Args:
            context: Intake context with legal information
            n_results: Number of results to return
            where_filter: Metadata filter for search
            
        Returns:
            VectorSearchResult with found cases
        """
        try:
            # Build search query
            query = self.build_search_query(context)
            
            # Prepare where filter
            if not where_filter:
                jurisdiction = context.get("jurisdiction", "ri")
                where_filter = {"jurisdiction": jurisdiction}
            
            # Perform vector search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
            
            # Extract results
            documents = results["documents"][0] if results["documents"] else []
            metadatas = results["metadatas"][0] if results["metadatas"] else []
            distances = results["distances"][0] if results["distances"] else []
            ids = results["ids"][0] if results["ids"] else []
            
            result = VectorSearchResult(
                documents=documents,
                metadatas=metadatas,
                distances=distances,
                ids=ids,
                query=query,
                collection_name=self.collection_name
            )
            
            logger.info(f"Found {len(documents)} vector results for query: {query}")
            return result
            
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return VectorSearchResult(
                documents=[],
                metadatas=[],
                distances=[],
                ids=[],
                query=context.get("original_input", ""),
                collection_name=self.collection_name
            )
    
    def add_cases(self, cases: List[Dict[str, Any]]) -> bool:
        """
        Add cases to the vector store.
        
        Args:
            cases: List of case dictionaries with text and metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            documents = []
            metadatas = []
            ids = []
            
            for i, case in enumerate(cases):
                documents.append(case.get("text", ""))
                metadatas.append(case.get("metadata", {}))
                ids.append(f"case_{i}_{hash(case.get('text', ''))}")
            
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(cases)} cases to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding cases to vector store: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_cases": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}

def search_local(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for LangGraph - searches local vector store.
    
    Args:
        context: Intake context from previous agent
        
    Returns:
        Dictionary with search results
    """
    agent = VectorAgent()
    result = agent.search_cases(context, n_results=5)
    
    # Convert to serializable format
    cases_data = []
    for i, (doc, metadata, distance) in enumerate(zip(
        result.documents, 
        result.metadatas, 
        result.distances
    )):
        cases_data.append({
            "text": doc,
            "metadata": metadata,
            "similarity_score": 1 - distance,  # Convert distance to similarity
            "id": result.ids[i] if i < len(result.ids) else f"case_{i}"
        })
    
    return {
        "source": "vector_store",
        "cases": cases_data,
        "total_found": len(cases_data),
        "search_query": result.query,
        "collection_name": result.collection_name,
        "success": len(cases_data) > 0
    }

# Example usage and testing
if __name__ == "__main__":
    # Test the vector agent
    test_context = {
        "topic": "criminal",
        "jurisdiction": "ri",
        "case_type": "criminal",
        "keywords": ["gun", "possession"],
        "urgency": "high",
        "original_input": "I was charged with gun possession in Rhode Island",
        "suggested_charges": ["Unlawful possession of firearm"]
    }
    
    agent = VectorAgent()
    
    # Get collection stats
    stats = agent.get_collection_stats()
    print(f"Collection Stats: {stats}")
    
    # Search for cases
    result = agent.search_cases(test_context, n_results=3)
    
    print(f"Search Query: {result.query}")
    print(f"Found {len(result.documents)} cases:")
    print()
    
    for i, (doc, metadata, distance) in enumerate(zip(
        result.documents, 
        result.metadatas, 
        result.distances
    )):
        print(f"{i+1}. Similarity: {1-distance:.3f}")
        print(f"   Metadata: {metadata}")
        print(f"   Text: {doc[:200]}...")
        print()

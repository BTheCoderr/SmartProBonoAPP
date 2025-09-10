"""
Vector search agent for semantic case law search using ChromaDB.
This agent searches the embedded case law database for relevant cases.
"""

import logging
from typing import Dict, List, Any, Optional
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class VectorSearchAgent:
    """Agent for semantic search of embedded case law."""
    
    def __init__(self, collection_name: str = "legal_cases"):
        self.collection_name = collection_name
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./vectorstore/chroma_data"
        ))
        self.collection = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the ChromaDB collection."""
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
            logger.info(f"Connected to existing collection: {self.collection_name}")
        except Exception as e:
            logger.warning(f"Collection {self.collection_name} not found: {e}")
            try:
                # Create the collection if it doesn't exist
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Legal cases for semantic search"}
                )
                logger.info(f"Created new collection: {self.collection_name}")
            except Exception as create_error:
                logger.error(f"Failed to create collection: {create_error}")
                self.collection = None
    
    def search_cases(
        self, 
        query: str, 
        jurisdiction: Optional[str] = None,
        case_type: Optional[str] = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Search for relevant cases using semantic similarity.
        
        Args:
            query: Search query
            jurisdiction: Filter by jurisdiction (ri, ma, etc.)
            case_type: Filter by case type (criminal, civil, etc.)
            limit: Maximum number of results
            
        Returns:
            Dictionary with search results
        """
        if not self.collection:
            logger.warning("No collection available, returning empty results")
            return {
                "success": False,
                "cases": [],
                "error": "Vector database not initialized"
            }
        
        try:
            # Build where clause for filtering
            where_clause = {}
            if jurisdiction:
                where_clause["jurisdiction"] = jurisdiction
            if case_type:
                where_clause["case_type"] = case_type
            
            # Perform semantic search
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_clause if where_clause else None
            )
            
            # Format results
            cases = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    case = {
                        "case_name": results['metadatas'][0][i].get('case_name', 'Unknown'),
                        "court": results['metadatas'][0][i].get('court', 'Unknown Court'),
                        "date": results['metadatas'][0][i].get('date', 'Unknown Date'),
                        "jurisdiction": results['metadatas'][0][i].get('jurisdiction', 'Unknown'),
                        "case_type": results['metadatas'][0][i].get('case_type', 'Unknown'),
                        "text": doc,
                        "similarity_score": results['distances'][0][i] if results['distances'] else 0.0,
                        "topics": results['metadatas'][0][i].get('topics', [])
                    }
                    cases.append(case)
            
            logger.info(f"Found {len(cases)} cases for query: {query}")
            
            return {
                "success": True,
                "cases": cases,
                "query": query,
                "jurisdiction": jurisdiction,
                "total_results": len(cases)
            }
            
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return {
                "success": False,
                "cases": [],
                "error": str(e)
            }
    
    def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific case by ID.
        
        Args:
            case_id: Case identifier
            
        Returns:
            Case data or None if not found
        """
        if not self.collection:
            return None
            
        try:
            results = self.collection.get(ids=[case_id])
            if results['documents']:
                return {
                    "id": case_id,
                    "text": results['documents'][0],
                    "metadata": results['metadatas'][0] if results['metadatas'] else {}
                }
        except Exception as e:
            logger.error(f"Error getting case by ID: {e}")
        
        return None

def search_local(intake_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search local vector database for relevant cases.
    This function is called by the LangGraph pipeline.
    
    Args:
        intake_result: Results from the intake agent
        
    Returns:
        Search results from vector database
    """
    agent = VectorSearchAgent()
    
    # Extract search terms from intake result
    query = intake_result.get('query', '')
    jurisdiction = intake_result.get('jurisdiction', 'ri')
    case_type = intake_result.get('case_type')
    
    if not query:
        return {
            "success": False,
            "cases": [],
            "error": "No query provided"
        }
    
    return agent.search_cases(
        query=query,
        jurisdiction=jurisdiction,
        case_type=case_type,
        limit=5
    )
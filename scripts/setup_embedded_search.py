#!/usr/bin/env python3
"""
Setup script for embedded search layer using Harvard Case.Law data.
This populates ChromaDB with RI and MA case law for fast semantic search.
"""

import os
import sys
import json
import requests
import logging
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# from legal_ai_backend.embeddings.instructor_embeddings import InstructorEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddedSearchSetup:
    """Setup embedded search using Harvard Case.Law data."""
    
    def __init__(self):
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./vectorstore/chroma_data"
        ))
        # self.embedder = InstructorEmbeddings()  # Will use ChromaDB's built-in embeddings
        self.collection_name = "legal_cases"
        
    def download_harvard_cases(self, jurisdiction: str = "ri") -> List[Dict[str, Any]]:
        """Download case law data from Harvard Case.Law."""
        logger.info(f"Downloading Harvard Case.Law data for {jurisdiction}...")
        
        # For now, we'll create sample data since the actual download requires more setup
        # In production, you would download from https://case.law/download/
        sample_cases = self._create_sample_cases(jurisdiction)
        return sample_cases
    
    def _create_sample_cases(self, jurisdiction: str) -> List[Dict[str, Any]]:
        """Create sample case data for development."""
        cases = []
        
        if jurisdiction == "ri":
            cases = [
                {
                    "case_name": "State v. Johnson",
                    "court": "Rhode Island Supreme Court",
                    "date": "2022-03-15",
                    "text": "In this case, the defendant was charged with possession of a controlled substance. The court found that the search was conducted without proper warrant, violating the Fourth Amendment. The evidence was suppressed and the case was dismissed.",
                    "jurisdiction": "ri",
                    "case_type": "criminal",
                    "topics": ["possession", "search and seizure", "fourth amendment"]
                },
                {
                    "case_name": "Smith v. Landlord Corp",
                    "court": "Rhode Island Superior Court", 
                    "date": "2022-07-22",
                    "text": "This landlord-tenant dispute involved improper eviction procedures. The court ruled that the landlord failed to provide proper notice as required by state law. The tenant was awarded damages and the eviction was overturned.",
                    "jurisdiction": "ri",
                    "case_type": "civil",
                    "topics": ["landlord tenant", "eviction", "housing", "notice"]
                },
                {
                    "case_name": "Brown v. City of Providence",
                    "court": "Rhode Island District Court",
                    "date": "2023-01-10",
                    "text": "Traffic violation case where the defendant contested a speeding ticket. The court found that the radar equipment was not properly calibrated, resulting in dismissal of the charges.",
                    "jurisdiction": "ri", 
                    "case_type": "traffic",
                    "topics": ["traffic", "speeding", "radar", "equipment"]
                }
            ]
        elif jurisdiction == "ma":
            cases = [
                {
                    "case_name": "Commonwealth v. Williams",
                    "court": "Massachusetts Supreme Judicial Court",
                    "date": "2022-05-18",
                    "text": "Criminal case involving drug possession charges. The court established that mere proximity to drugs is insufficient for conviction without evidence of actual possession or control.",
                    "jurisdiction": "ma",
                    "case_type": "criminal", 
                    "topics": ["possession", "drugs", "evidence", "control"]
                },
                {
                    "case_name": "Davis v. Housing Authority",
                    "court": "Massachusetts Appeals Court",
                    "date": "2022-09-12",
                    "text": "Housing discrimination case where the plaintiff alleged violation of fair housing laws. The court found in favor of the plaintiff and awarded substantial damages.",
                    "jurisdiction": "ma",
                    "case_type": "civil",
                    "topics": ["housing", "discrimination", "fair housing", "damages"]
                }
            ]
        
        return cases
    
    def embed_cases(self, cases: List[Dict[str, Any]]) -> None:
        """Embed cases into ChromaDB for semantic search."""
        logger.info(f"Embedding {len(cases)} cases into ChromaDB...")
        
        # Create or get collection
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            logger.info(f"Using existing collection: {self.collection_name}")
        except:
            collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Legal cases for semantic search"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
        
        # Prepare documents and metadata
        documents = []
        metadatas = []
        ids = []
        
        for i, case in enumerate(cases):
            # Create a searchable text that includes case name, court, and full text
            searchable_text = f"""
            Case: {case['case_name']}
            Court: {case['court']}
            Date: {case['date']}
            Type: {case['case_type']}
            
            {case['text']}
            """
            
            documents.append(searchable_text)
            metadatas.append({
                "case_name": case['case_name'],
                "court": case['court'],
                "date": case['date'],
                "jurisdiction": case['jurisdiction'],
                "case_type": case['case_type'],
                "topics": ", ".join(case.get('topics', []))  # Convert list to string
            })
            ids.append(f"case_{i}_{case['jurisdiction']}")
        
        # Add to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Successfully embedded {len(cases)} cases into ChromaDB")
    
    def test_search(self, query: str, jurisdiction: str = "ri") -> List[Dict[str, Any]]:
        """Test semantic search functionality."""
        logger.info(f"Testing search for: '{query}' in {jurisdiction}")
        
        collection = self.chroma_client.get_collection(self.collection_name)
        
        # Search with jurisdiction filter
        results = collection.query(
            query_texts=[query],
            n_results=5,
            where={"jurisdiction": jurisdiction}
        )
        
        return results
    
    def setup_complete_system(self):
        """Setup the complete embedded search system."""
        logger.info("Setting up embedded search system...")
        
        # Download and embed RI cases
        ri_cases = self.download_harvard_cases("ri")
        self.embed_cases(ri_cases)
        
        # Download and embed MA cases  
        ma_cases = self.download_harvard_cases("ma")
        self.embed_cases(ma_cases)
        
        # Test the system
        logger.info("Testing embedded search...")
        test_results = self.test_search("possession", "ri")
        logger.info(f"Found {len(test_results['documents'][0])} results for 'possession' in RI")
        
        logger.info("✅ Embedded search system setup complete!")

def main():
    """Main setup function."""
    setup = EmbeddedSearchSetup()
    setup.setup_complete_system()

if __name__ == "__main__":
    main()

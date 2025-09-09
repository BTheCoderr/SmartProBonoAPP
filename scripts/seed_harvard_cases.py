"""
Script to seed Harvard Case Law data into ChromaDB vector store.
Downloads and embeds case law from Harvard's Case.Law database.
"""
import json
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)

class HarvardCaseSeeder:
    """Seeder for Harvard Case Law data into ChromaDB."""
    
    def __init__(self, persist_directory: str = "./vectorstore/chroma_data"):
        """
        Initialize the seeder.
        
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
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Ensure the collection exists, create if not."""
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Using existing collection: {self.collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Harvard Case Law Embeddings"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def download_harvard_data(self, jurisdiction: str = "ri", limit: int = 100) -> List[Dict[str, Any]]:
        """
        Download case data from Harvard Case.Law API.
        
        Args:
            jurisdiction: State code (ri, ma, ct, etc.)
            limit: Maximum number of cases to download
            
        Returns:
            List of case data
        """
        # Note: This is a simplified example. In practice, you would need to:
        # 1. Register for Harvard Case.Law API access
        # 2. Use proper authentication
        # 3. Handle pagination for large datasets
        
        logger.info(f"Downloading Harvard case data for {jurisdiction}...")
        
        # For demo purposes, we'll create sample data
        # In production, replace this with actual API calls
        sample_cases = self._create_sample_cases(jurisdiction, limit)
        
        logger.info(f"Downloaded {len(sample_cases)} cases")
        return sample_cases
    
    def _create_sample_cases(self, jurisdiction: str, limit: int) -> List[Dict[str, Any]]:
        """Create sample case data for demonstration."""
        sample_cases = [
            {
                "case_name": f"State v. Smith ({jurisdiction.upper()})",
                "court": f"{jurisdiction.upper()} Superior Court",
                "date_filed": "2023-01-15",
                "jurisdiction": {"slug": jurisdiction},
                "casebody": {
                    "data": {
                        "opinions": [{
                            "text": f"This case involves unlawful possession of a firearm in {jurisdiction.upper()}. The defendant was charged under state law for carrying a weapon without proper licensing. The court found that the defendant's Fourth Amendment rights were not violated during the search and seizure. The conviction was upheld on appeal."
                        }]
                    }
                }
            },
            {
                "case_name": f"Commonwealth v. Johnson ({jurisdiction.upper()})",
                "court": f"{jurisdiction.upper()} Supreme Court",
                "date_filed": "2022-11-20",
                "jurisdiction": {"slug": jurisdiction},
                "casebody": {
                    "data": {
                        "opinions": [{
                            "text": f"Defendant charged with assault with a deadly weapon in {jurisdiction.upper()}. The court analyzed the elements of assault and determined that the prosecution met its burden of proof. The defendant's self-defense claim was rejected based on the evidence presented."
                        }]
                    }
                }
            },
            {
                "case_name": f"People v. Rodriguez ({jurisdiction.upper()})",
                "court": f"{jurisdiction.upper()} District Court",
                "date_filed": "2023-03-10",
                "jurisdiction": {"slug": jurisdiction},
                "casebody": {
                    "data": {
                        "opinions": [{
                            "text": f"Criminal case involving drug possession in {jurisdiction.upper()}. The court examined the search warrant requirements and found that the police had probable cause. The defendant's motion to suppress evidence was denied."
                        }]
                    }
                }
            }
        ]
        
        return sample_cases[:limit]
    
    def process_case(self, case: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single case for embedding.
        
        Args:
            case: Case data from Harvard API
            
        Returns:
            Processed case data or None if invalid
        """
        try:
            # Extract case information
            case_name = case.get("case_name", "Unknown Case")
            court = case.get("court", "Unknown Court")
            date_filed = case.get("date_filed", "Unknown Date")
            jurisdiction = case.get("jurisdiction", {}).get("slug", "unknown")
            
            # Extract case text
            case_text = ""
            if "casebody" in case and "data" in case["casebody"]:
                opinions = case["casebody"]["data"].get("opinions", [])
                if opinions and len(opinions) > 0:
                    case_text = opinions[0].get("text", "")
            
            if not case_text:
                logger.warning(f"No case text found for {case_name}")
                return None
            
            # Create metadata
            metadata = {
                "case_name": case_name,
                "court": court,
                "date_filed": date_filed,
                "jurisdiction": jurisdiction,
                "case_type": "criminal",  # Simplified
                "source": "harvard_case_law"
            }
            
            return {
                "text": case_text,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error processing case: {e}")
            return None
    
    def embed_cases(self, cases: List[Dict[str, Any]]) -> bool:
        """
        Embed cases into ChromaDB.
        
        Args:
            cases: List of processed case data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            documents = []
            metadatas = []
            ids = []
            
            for i, case in enumerate(cases):
                if case is None:
                    continue
                
                documents.append(case["text"])
                metadatas.append(case["metadata"])
                ids.append(f"harvard_case_{i}_{hash(case['text'])}")
            
            if not documents:
                logger.warning("No valid cases to embed")
                return False
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully embedded {len(documents)} cases")
            return True
            
        except Exception as e:
            logger.error(f"Error embedding cases: {e}")
            return False
    
    def seed_jurisdiction(self, jurisdiction: str, limit: int = 100) -> bool:
        """
        Seed case data for a specific jurisdiction.
        
        Args:
            jurisdiction: State code
            limit: Maximum number of cases
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Starting seed process for {jurisdiction}")
            
            # Download cases
            cases = self.download_harvard_data(jurisdiction, limit)
            
            # Process cases
            processed_cases = []
            for case in tqdm(cases, desc="Processing cases"):
                processed = self.process_case(case)
                if processed:
                    processed_cases.append(processed)
            
            # Embed cases
            success = self.embed_cases(processed_cases)
            
            if success:
                logger.info(f"Successfully seeded {len(processed_cases)} cases for {jurisdiction}")
            else:
                logger.error(f"Failed to seed cases for {jurisdiction}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error seeding jurisdiction {jurisdiction}: {e}")
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

def main():
    """Main function to seed Harvard case data."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize seeder
    seeder = HarvardCaseSeeder()
    
    # Seed data for multiple jurisdictions
    jurisdictions = ["ri", "ma", "ct"]
    
    for jurisdiction in jurisdictions:
        print(f"Seeding data for {jurisdiction.upper()}...")
        success = seeder.seed_jurisdiction(jurisdiction, limit=50)
        
        if success:
            print(f"✅ Successfully seeded {jurisdiction.upper()}")
        else:
            print(f"❌ Failed to seed {jurisdiction.upper()}")
    
    # Print final stats
    stats = seeder.get_collection_stats()
    print(f"\nFinal Collection Stats:")
    print(f"Total Cases: {stats.get('total_cases', 0)}")
    print(f"Collection: {stats.get('collection_name', 'Unknown')}")

if __name__ == "__main__":
    main()

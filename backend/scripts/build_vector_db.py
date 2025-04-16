#!/usr/bin/env python3
"""
Build Vector Database Script for SmartProBono

This script builds and populates vector databases for legal knowledge retrieval,
creating domain-specific and jurisdiction-specific indexes.
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from tqdm import tqdm

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.vector_db_manager import VectorDatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("vector_db_build.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define constants
DEFAULT_DATA_DIR = Path(__file__).parent.parent / 'ai' / 'data'
DEFAULT_VECTOR_DB_DIR = Path(__file__).parent.parent / 'ai' / 'vector_db'

# Define domain-specific indexing configurations
DOMAIN_CONFIGS = {
    'tenant_rights': {
        'description': 'Legal knowledge on tenant rights and housing law',
        'index_name': 'tenant_rights',
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'metric': 'cosine',
        'index_type': 'HNSW'  # Hierarchical Navigable Small World for fast search
    },
    'employment': {
        'description': 'Legal knowledge on employment law and workplace rights',
        'index_name': 'employment',
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'metric': 'cosine',
        'index_type': 'HNSW'
    },
    'family_law': {
        'description': 'Legal knowledge on family law matters',
        'index_name': 'family_law',
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'metric': 'cosine',
        'index_type': 'HNSW'
    },
    'immigration': {
        'description': 'Legal knowledge on immigration law and procedures',
        'index_name': 'immigration',
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'metric': 'cosine',
        'index_type': 'HNSW'
    },
    'consumer_protection': {
        'description': 'Legal knowledge on consumer rights and protection laws',
        'index_name': 'consumer_protection',
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'metric': 'cosine',
        'index_type': 'HNSW'
    },
    'civil_rights': {
        'description': 'Legal knowledge on civil rights and liberties',
        'index_name': 'civil_rights',
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'metric': 'cosine',
        'index_type': 'HNSW'
    },
    'general': {
        'description': 'General legal knowledge across domains',
        'index_name': 'general',
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'metric': 'cosine',
        'index_type': 'HNSW'
    }
}

# Define jurisdiction options
JURISDICTIONS = [
    'federal',
    'california',
    'new_york',
    'texas',
    'florida',
    'illinois'
]

def load_vector_chunks(data_dir: Path, domain: Optional[str] = None, jurisdiction: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load vector chunks from processed data files.
    
    Args:
        data_dir: Base data directory
        domain: Optional domain to filter by
        jurisdiction: Optional jurisdiction to filter by
        
    Returns:
        List of text chunks with metadata
    """
    logger.info(f"Loading vector chunks for domain={domain}, jurisdiction={jurisdiction}")
    
    processed_dir = data_dir / 'processed'
    
    # Find all vector chunk files
    if domain and jurisdiction:
        # Look for domain and jurisdiction specific file
        chunk_file = processed_dir / f"vector_chunks_{domain}_{jurisdiction}.jsonl"
        if not chunk_file.exists():
            # Fall back to domain-only file
            chunk_file = processed_dir / f"vector_chunks_{domain}.jsonl"
    elif domain:
        # Look for domain specific file
        chunk_file = processed_dir / f"vector_chunks_{domain}.jsonl"
    elif jurisdiction:
        # Look for jurisdiction specific file
        chunk_file = processed_dir / f"vector_chunks_{jurisdiction}.jsonl"
    else:
        # Use main file
        chunk_file = processed_dir / "vector_chunks.jsonl"
    
    # If specific file not found, use the main file
    if not chunk_file.exists():
        chunk_file = processed_dir / "vector_chunks.jsonl"
        
    if not chunk_file.exists():
        logger.error(f"No vector chunks file found at {chunk_file}")
        return []
    
    # Load chunks
    chunks = []
    with open(chunk_file, 'r') as f:
        for line in f:
            try:
                chunk = json.loads(line)
                
                # Apply filtering if needed
                if domain and jurisdiction:
                    # Need to match both
                    domain_match = (
                        chunk['metadata'].get('domain') == domain or
                        chunk['metadata'].get('topic') == domain
                    )
                    jurisdiction_match = chunk['metadata'].get('jurisdiction') == jurisdiction
                    
                    if domain_match and jurisdiction_match:
                        chunks.append(chunk)
                elif domain:
                    # Need to match domain
                    domain_match = (
                        chunk['metadata'].get('domain') == domain or
                        chunk['metadata'].get('topic') == domain
                    )
                    
                    if domain_match:
                        chunks.append(chunk)
                elif jurisdiction:
                    # Need to match jurisdiction
                    if chunk['metadata'].get('jurisdiction') == jurisdiction:
                        chunks.append(chunk)
                else:
                    # No filtering
                    chunks.append(chunk)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in line: {line[:50]}...")
    
    logger.info(f"Loaded {len(chunks)} chunks for indexing")
    return chunks

def build_vector_index(vector_db: VectorDatabaseManager, config: Dict[str, Any], chunks: List[Dict[str, Any]]) -> bool:
    """
    Build a vector index from text chunks.
    
    Args:
        vector_db: Vector database manager
        config: Indexing configuration
        chunks: List of text chunks with metadata
        
    Returns:
        True if successful, False otherwise
    """
    index_name = config['index_name']
    logger.info(f"Building vector index: {index_name}")
    
    # Prepare data for indexing
    texts = []
    metadatas = []
    
    for chunk in chunks:
        texts.append(chunk['text'])
        metadatas.append(chunk['metadata'])
    
    # Create index
    try:
        # Save chunks to a temporary file
        temp_dir = vector_db.data_dir / 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = temp_dir / f"{index_name}_chunks.json"
        
        with open(temp_file, 'w') as f:
            json.dump({
                'texts': texts,
                'metadatas': metadatas
            }, f)
        
        # Create the index
        success = vector_db.create_index(
            name=index_name,
            data_file=str(temp_file),
            dimension=384,  # Dimension for all-MiniLM-L6-v2
            index_type=config['index_type']
        )
        
        if success:
            logger.info(f"Successfully built index: {index_name} with {len(texts)} documents")
        else:
            logger.error(f"Failed to build index: {index_name}")
        
        return success
    except Exception as e:
        logger.error(f"Error building index {index_name}: {str(e)}")
        return False

def main():
    """Main function to run the vector database build process."""
    parser = argparse.ArgumentParser(description='Build vector databases for legal knowledge')
    parser.add_argument('--data-dir', type=str, default=str(DEFAULT_DATA_DIR),
                        help='Directory containing processed data')
    parser.add_argument('--vector-db-dir', type=str, default=str(DEFAULT_VECTOR_DB_DIR),
                        help='Output directory for vector databases')
    parser.add_argument('--domains', type=str, nargs='+', 
                        default=['tenant_rights', 'employment', 'general'],
                        help='Legal domains to build vector databases for')
    parser.add_argument('--jurisdictions', type=str, nargs='+',
                        default=['federal', 'california'],
                        help='Jurisdictions to build vector databases for')
    parser.add_argument('--all-domains', action='store_true',
                        help='Build vector databases for all domains')
    parser.add_argument('--all-jurisdictions', action='store_true',
                        help='Build vector databases for all jurisdictions')
    
    args = parser.parse_args()
    
    # Convert to Path objects
    data_dir = Path(args.data_dir)
    vector_db_dir = Path(args.vector_db_dir)
    vector_db_dir.mkdir(exist_ok=True, parents=True)
    
    # Determine domains to process
    domains = list(DOMAIN_CONFIGS.keys()) if args.all_domains else args.domains
    logger.info(f"Building vector databases for domains: {domains}")
    
    # Determine jurisdictions to process
    jurisdictions = JURISDICTIONS if args.all_jurisdictions else args.jurisdictions
    if jurisdictions:
        logger.info(f"Including jurisdictions: {jurisdictions}")
    
    # Create vector database manager
    vector_db = VectorDatabaseManager(
        data_dir=str(vector_db_dir),
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    
    # Build domain-specific indexes
    successful_indexes = []
    failed_indexes = []
    
    # First build general index with all data
    general_chunks = load_vector_chunks(data_dir)
    if general_chunks:
        general_config = DOMAIN_CONFIGS['general']
        success = build_vector_index(vector_db, general_config, general_chunks)
        
        if success:
            successful_indexes.append(general_config['index_name'])
        else:
            failed_indexes.append(general_config['index_name'])
    
    # Build domain-specific indexes
    for domain in domains:
        if domain == 'general':
            continue  # Already handled above
        
        domain_config = DOMAIN_CONFIGS[domain]
        domain_chunks = load_vector_chunks(data_dir, domain=domain)
        
        if not domain_chunks:
            logger.warning(f"No chunks found for domain: {domain}")
            continue
        
        success = build_vector_index(vector_db, domain_config, domain_chunks)
        
        if success:
            successful_indexes.append(domain_config['index_name'])
        else:
            failed_indexes.append(domain_config['index_name'])
        
        # Build jurisdiction-specific indexes for this domain
        if jurisdictions:
            for jurisdiction in jurisdictions:
                jur_config = domain_config.copy()
                jur_config['index_name'] = f"{domain}_{jurisdiction}"
                jur_config['description'] += f" for {jurisdiction} jurisdiction"
                
                jur_chunks = load_vector_chunks(data_dir, domain=domain, jurisdiction=jurisdiction)
                
                if not jur_chunks:
                    logger.warning(f"No chunks found for domain {domain} in jurisdiction {jurisdiction}")
                    continue
                
                success = build_vector_index(vector_db, jur_config, jur_chunks)
                
                if success:
                    successful_indexes.append(jur_config['index_name'])
                else:
                    failed_indexes.append(jur_config['index_name'])
    
    # Build jurisdiction-specific indexes (without domain filtering)
    for jurisdiction in jurisdictions:
        jur_config = DOMAIN_CONFIGS['general'].copy()
        jur_config['index_name'] = f"general_{jurisdiction}"
        jur_config['description'] = f"General legal knowledge for {jurisdiction} jurisdiction"
        
        jur_chunks = load_vector_chunks(data_dir, jurisdiction=jurisdiction)
        
        if not jur_chunks:
            logger.warning(f"No chunks found for jurisdiction {jurisdiction}")
            continue
        
        success = build_vector_index(vector_db, jur_config, jur_chunks)
        
        if success:
            successful_indexes.append(jur_config['index_name'])
        else:
            failed_indexes.append(jur_config['index_name'])
    
    # Print summary
    logger.info("\n===== VECTOR DB BUILD COMPLETE =====")
    logger.info(f"Successfully built indexes: {len(successful_indexes)}")
    for index in successful_indexes:
        logger.info(f"  - {index}")
    
    if failed_indexes:
        logger.info(f"Failed indexes: {len(failed_indexes)}")
        for index in failed_indexes:
            logger.info(f"  - {index}")
    
    # Save metadata record
    vector_db._save_metadata_record()
    logger.info(f"Vector database built at: {vector_db_dir}")

if __name__ == "__main__":
    main() 
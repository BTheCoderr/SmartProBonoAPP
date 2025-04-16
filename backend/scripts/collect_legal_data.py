#!/usr/bin/env python3
"""
Legal Data Collection Script for SmartProBono

This script collects legal case data, statutes, and regulatory information from
various public sources and organizes them for model training and vector database creation.
"""

import os
import json
import requests
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("legal_data_collection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define constants
API_KEYS = {
    'case_law': os.environ.get('CASE_LAW_API_KEY', ''),
    'regulations': os.environ.get('REGULATIONS_API_KEY', ''),
    'statutes': os.environ.get('STATUTES_API_KEY', '')
}

DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / 'ai' / 'data'
JURISDICTIONS = [
    'federal', 'california', 'new_york', 'texas', 'florida', 
    'illinois', 'pennsylvania', 'ohio', 'michigan', 'georgia'
]
LEGAL_DOMAINS = [
    'tenant_rights', 'employment', 'family_law', 'immigration',
    'consumer_protection', 'civil_rights', 'criminal_defense'
]

class LegalDataCollector:
    """Collects and organizes legal data from public sources."""
    
    def __init__(self, output_dir: Path = DEFAULT_OUTPUT_DIR):
        """Initialize the collector with output directory."""
        self.output_dir = output_dir
        self.raw_dir = output_dir / 'raw'
        self.processed_dir = output_dir / 'processed'
        self.training_dir = output_dir / 'training'
        
        # Create directories
        for directory in [self.output_dir, self.raw_dir, self.processed_dir, self.training_dir]:
            directory.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"Initialized data collector with output dir: {output_dir}")
    
    def collect_case_law(self, jurisdiction: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Collect case law data from public APIs or datasets.
        
        Args:
            jurisdiction: Which jurisdiction to collect for
            limit: Maximum number of cases to collect
            
        Returns:
            List of case dictionaries
        """
        logger.info(f"Collecting case law for {jurisdiction} (limit: {limit})")
        
        # For demo purposes, we'll generate mock data
        # In production, this would call actual legal data APIs
        cases = []
        
        # Legal topics by jurisdiction
        topics_by_jurisdiction = {
            'federal': ['constitutional_law', 'civil_rights', 'administrative_law'],
            'california': ['property_law', 'employment_law', 'environmental_law'],
            'new_york': ['contract_law', 'tort_law', 'corporate_law'],
            'texas': ['property_law', 'oil_and_gas', 'criminal_law'],
            'florida': ['real_estate', 'maritime_law', 'elder_law'],
            'default': ['property_law', 'contract_law', 'tort_law', 'criminal_law']
        }
        
        topics = topics_by_jurisdiction.get(jurisdiction, topics_by_jurisdiction['default'])
        
        # Generate sample cases
        for i in range(limit):
            year = 2010 + (i % 14)  # Cases from 2010-2023
            topic = topics[i % len(topics)]
            
            case = {
                'id': f"{jurisdiction}-{year}-{1000 + i}",
                'name': f"Sample v. Example ({year})",
                'citation': f"{jurisdiction.capitalize()} Reports {300 + i} ({year})",
                'jurisdiction': jurisdiction,
                'year': year,
                'court': f"{jurisdiction.capitalize()} Supreme Court",
                'topic': topic,
                'summary': f"This case addresses {topic.replace('_', ' ')} issues in {jurisdiction}.",
                'holding': f"The court held that in {topic.replace('_', ' ')} cases, parties must demonstrate...",
                'full_text': f"OPINION OF THE COURT\n\nIn the matter of {topic.replace('_', ' ')}, this court finds...",
            }
            cases.append(case)
        
        # Save raw data
        self._save_raw_data(cases, f"case_law_{jurisdiction}.json")
        
        return cases
    
    def collect_statutes(self, jurisdiction: str) -> List[Dict[str, Any]]:
        """
        Collect statutory law from public sources.
        
        Args:
            jurisdiction: Which jurisdiction to collect for
            
        Returns:
            List of statute dictionaries
        """
        logger.info(f"Collecting statutes for {jurisdiction}")
        
        # For demo purposes, generate mock statute data
        statutes = []
        
        # Define common statute topics
        topics = [
            ('tenant_rights', 'Housing and Tenant Protection Act'),
            ('employment', 'Fair Labor Standards'),
            ('family_law', 'Family Code'),
            ('immigration', 'Immigration and Nationality'),
            ('consumer_protection', 'Consumer Protection'),
            ('civil_rights', 'Civil Rights Act'),
            ('criminal_defense', 'Criminal Code')
        ]
        
        # Generate sample statutes
        for i, (domain, title) in enumerate(topics):
            chapters = 3  # Each statute has multiple chapters
            for chapter in range(1, chapters + 1):
                sections = 5  # Each chapter has multiple sections
                for section in range(1, sections + 1):
                    statute = {
                        'id': f"{jurisdiction}-{domain}-{chapter}-{section}",
                        'title': f"{title} of {jurisdiction.capitalize()}",
                        'domain': domain,
                        'chapter': chapter,
                        'section': section,
                        'citation': f"{jurisdiction.capitalize()} Code §{chapter}.{section}",
                        'jurisdiction': jurisdiction,
                        'text': f"§{chapter}.{section} - Regarding {domain.replace('_', ' ')} in {jurisdiction}.\n\n" +
                               f"(a) Purpose: To establish regulations for {domain.replace('_', ' ')}.\n" +
                               f"(b) Requirements: All parties must comply with the following provisions...\n" +
                               f"(c) Remedies: Violations of this section may result in penalties including...",
                        'enacted_date': f"{2000 + i}-01-01",
                        'last_amended': f"{2020 + i}-06-15"
                    }
                    statutes.append(statute)
        
        # Save raw data
        self._save_raw_data(statutes, f"statutes_{jurisdiction}.json")
        
        return statutes
    
    def collect_regulations(self, jurisdiction: str) -> List[Dict[str, Any]]:
        """
        Collect regulatory information from public sources.
        
        Args:
            jurisdiction: Which jurisdiction to collect for
            
        Returns:
            List of regulation dictionaries
        """
        logger.info(f"Collecting regulations for {jurisdiction}")
        
        # For demo purposes, generate mock regulation data
        regulations = []
        
        # Define common regulation topics
        agencies = [
            ('HUD', 'Housing and Urban Development', 'tenant_rights'),
            ('DOL', 'Department of Labor', 'employment'),
            ('DHS', 'Department of Homeland Security', 'immigration'),
            ('FTC', 'Federal Trade Commission', 'consumer_protection'),
            ('DOJ', 'Department of Justice', 'civil_rights'),
            ('EPA', 'Environmental Protection Agency', 'environmental'),
            ('FDA', 'Food and Drug Administration', 'health')
        ]
        
        # Generate sample regulations
        for i, (acronym, agency, domain) in enumerate(agencies):
            parts = 2  # Each agency has multiple regulation parts
            for part in range(1, parts + 1):
                sections = 3  # Each part has multiple sections
                for section in range(1, sections + 1):
                    regulation = {
                        'id': f"{jurisdiction}-{acronym}-{part}-{section}",
                        'agency': agency,
                        'domain': domain,
                        'part': part,
                        'section': section,
                        'citation': f"{jurisdiction.capitalize()} Admin Code {acronym} {part}.{section}",
                        'jurisdiction': jurisdiction,
                        'text': f"Part {part}, Section {section} - {agency} Regulations\n\n" +
                               f"Purpose: These regulations implement the {domain.replace('_', ' ')} laws of {jurisdiction}.\n" +
                               f"Requirements: Regulated entities must comply with the following standards...\n" +
                               f"Enforcement: These regulations shall be enforced through the following procedures...",
                        'effective_date': f"{2010 + i}-03-15",
                        'last_revised': f"{2022 + i}-09-30"
                    }
                    regulations.append(regulation)
        
        # Save raw data
        self._save_raw_data(regulations, f"regulations_{jurisdiction}.json")
        
        return regulations
    
    def process_for_training(self, jurisdiction: Optional[str] = None):
        """
        Process collected data for model training.
        
        Args:
            jurisdiction: Optional jurisdiction to process (None for all)
        """
        logger.info(f"Processing data for training: {jurisdiction or 'all jurisdictions'}")
        
        # Load all data
        all_data = self._load_all_data(jurisdiction)
        
        # Create QA pairs for training
        qa_pairs = self._generate_qa_pairs(all_data)
        
        # Save training data
        training_file = self.training_dir / f"legal_qa_pairs{'_' + jurisdiction if jurisdiction else ''}.jsonl"
        with open(training_file, 'w') as f:
            for pair in qa_pairs:
                f.write(json.dumps(pair) + '\n')
        
        logger.info(f"Saved {len(qa_pairs)} QA pairs to {training_file}")
    
    def prepare_for_vector_db(self, jurisdiction: Optional[str] = None):
        """
        Process data for vector database indexing.
        
        Args:
            jurisdiction: Optional jurisdiction to process (None for all)
        """
        logger.info(f"Preparing data for vector database: {jurisdiction or 'all jurisdictions'}")
        
        # Load all data
        all_data = self._load_all_data(jurisdiction)
        
        # Create vector DB chunks
        chunks = self._create_vector_chunks(all_data)
        
        # Save processed data
        output_file = self.processed_dir / f"vector_chunks{'_' + jurisdiction if jurisdiction else ''}.jsonl"
        with open(output_file, 'w') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk) + '\n')
        
        logger.info(f"Saved {len(chunks)} vector chunks to {output_file}")
    
    def _save_raw_data(self, data: List[Dict[str, Any]], filename: str):
        """
        Save raw data to JSON file.
        
        Args:
            data: List of data items
            filename: Output filename
        """
        output_path = self.raw_dir / filename
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved {len(data)} items to {output_path}")
    
    def _load_all_data(self, jurisdiction: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load all collected data.
        
        Args:
            jurisdiction: Optional jurisdiction filter
            
        Returns:
            Dictionary with data categories
        """
        all_data = {
            'cases': [],
            'statutes': [],
            'regulations': []
        }
        
        # Determine which files to load
        file_pattern = f"*_{jurisdiction}.json" if jurisdiction else "*.json"
        
        for file_path in self.raw_dir.glob(file_pattern):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Determine category from filename
                filename = file_path.name
                if filename.startswith('case_law'):
                    all_data['cases'].extend(data)
                elif filename.startswith('statutes'):
                    all_data['statutes'].extend(data)
                elif filename.startswith('regulations'):
                    all_data['regulations'].extend(data)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
        
        logger.info(f"Loaded {len(all_data['cases'])} cases, {len(all_data['statutes'])} statutes, "
                   f"and {len(all_data['regulations'])} regulations")
        
        return all_data
    
    def _generate_qa_pairs(self, data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, str]]:
        """
        Generate question-answer pairs for training.
        
        Args:
            data: Dictionary with all legal data
            
        Returns:
            List of QA pairs
        """
        qa_pairs = []
        
        # Process case law
        for case in data['cases']:
            # Case holding question
            qa_pairs.append({
                'question': f"What was the holding in {case['name']}?",
                'answer': case['holding']
            })
            
            # Case jurisdiction question
            qa_pairs.append({
                'question': f"Which court decided {case['name']}?",
                'answer': f"The {case['court']} decided this case in {case['year']}."
            })
            
            # Case topic question
            qa_pairs.append({
                'question': f"What legal topic does {case['name']} address?",
                'answer': f"This case addresses {case['topic'].replace('_', ' ')} issues."
            })
        
        # Process statutes
        for statute in data['statutes']:
            # Statute content question
            qa_pairs.append({
                'question': f"What does {statute['citation']} regulate?",
                'answer': statute['text']
            })
            
            # Statute domain question
            qa_pairs.append({
                'question': f"Which legal domain does {statute['citation']} cover?",
                'answer': f"This statute covers {statute['domain'].replace('_', ' ')}."
            })
            
            # Statute amendment question
            qa_pairs.append({
                'question': f"When was {statute['citation']} last amended?",
                'answer': f"This statute was last amended on {statute['last_amended']}."
            })
        
        # Process regulations
        for regulation in data['regulations']:
            # Regulation agency question
            qa_pairs.append({
                'question': f"Which agency issued {regulation['citation']}?",
                'answer': f"The {regulation['agency']} ({regulation['jurisdiction']}) issued this regulation."
            })
            
            # Regulation content question
            qa_pairs.append({
                'question': f"What are the requirements in {regulation['citation']}?",
                'answer': regulation['text']
            })
            
            # Regulation effective date question
            qa_pairs.append({
                'question': f"When did {regulation['citation']} take effect?",
                'answer': f"This regulation took effect on {regulation['effective_date']}."
            })
        
        logger.info(f"Generated {len(qa_pairs)} QA pairs for training")
        return qa_pairs
    
    def _create_vector_chunks(self, data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Create text chunks for vector database indexing.
        
        Args:
            data: Dictionary with all legal data
            
        Returns:
            List of text chunks with metadata
        """
        chunks = []
        
        # Process case law
        for case in data['cases']:
            # Split case text into chunks (simplified version)
            text = case['full_text']
            chunk_size = 500  # Characters per chunk
            overlap = 100
            
            for i in range(0, len(text), chunk_size - overlap):
                chunk_text = text[i:i + chunk_size]
                if len(chunk_text) < 50:  # Skip very small chunks
                    continue
                
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        'source_type': 'case_law',
                        'id': case['id'],
                        'name': case['name'],
                        'citation': case['citation'],
                        'jurisdiction': case['jurisdiction'],
                        'year': case['year'],
                        'court': case['court'],
                        'topic': case['topic']
                    }
                })
        
        # Process statutes
        for statute in data['statutes']:
            # Add each statute as a chunk
            chunks.append({
                'text': statute['text'],
                'metadata': {
                    'source_type': 'statute',
                    'id': statute['id'],
                    'title': statute['title'],
                    'citation': statute['citation'],
                    'jurisdiction': statute['jurisdiction'],
                    'domain': statute['domain'],
                    'chapter': statute['chapter'],
                    'section': statute['section'],
                    'enacted_date': statute['enacted_date'],
                    'last_amended': statute['last_amended']
                }
            })
        
        # Process regulations
        for regulation in data['regulations']:
            # Add each regulation as a chunk
            chunks.append({
                'text': regulation['text'],
                'metadata': {
                    'source_type': 'regulation',
                    'id': regulation['id'],
                    'agency': regulation['agency'],
                    'citation': regulation['citation'],
                    'jurisdiction': regulation['jurisdiction'],
                    'domain': regulation['domain'],
                    'part': regulation['part'],
                    'section': regulation['section'],
                    'effective_date': regulation['effective_date'],
                    'last_revised': regulation['last_revised']
                }
            })
        
        logger.info(f"Created {len(chunks)} text chunks for vector database")
        return chunks

def main():
    """Main function to run the data collection process."""
    parser = argparse.ArgumentParser(description='Collect legal data for AI training')
    parser.add_argument('--output-dir', type=str, default=str(DEFAULT_OUTPUT_DIR),
                        help='Output directory for collected data')
    parser.add_argument('--jurisdictions', type=str, nargs='+', default=['federal', 'california'],
                        help='Jurisdictions to collect data for')
    parser.add_argument('--case-limit', type=int, default=50,
                        help='Maximum number of cases per jurisdiction')
    parser.add_argument('--skip-collection', action='store_true',
                        help='Skip data collection and only process existing data')
    parser.add_argument('--skip-processing', action='store_true',
                        help='Skip processing and only collect raw data')
    
    args = parser.parse_args()
    
    # Create collector
    collector = LegalDataCollector(Path(args.output_dir))
    
    # Collect data for each jurisdiction
    if not args.skip_collection:
        for jurisdiction in args.jurisdictions:
            collector.collect_case_law(jurisdiction, args.case_limit)
            collector.collect_statutes(jurisdiction)
            collector.collect_regulations(jurisdiction)
    
    # Process data
    if not args.skip_processing:
        collector.process_for_training()
        collector.prepare_for_vector_db()
        
        # Also create jurisdiction-specific training data
        for jurisdiction in args.jurisdictions:
            collector.process_for_training(jurisdiction)
            collector.prepare_for_vector_db(jurisdiction)
    
    logger.info("Data collection and processing complete!")

if __name__ == "__main__":
    main() 
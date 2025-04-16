"""
Legal Data Processor for SmartProBono
This module processes legal data from various sources for model fine-tuning and vector database creation.
"""

import os
import re
import json
import logging
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalDataProcessor:
    """
    Processes legal data from various sources and prepares it for model fine-tuning and 
    vector database creation. This includes cleaning text, extracting citations, and formatting data.
    """
    
    def __init__(self, data_dir: str = 'ai/data'):
        """
        Initialize the legal data processor.
        
        Args:
            data_dir: Directory where legal data is stored
        """
        self.data_dir = data_dir
        self.raw_data_dir = os.path.join(data_dir, 'raw')
        self.processed_data_dir = os.path.join(data_dir, 'processed')
        self.training_data_dir = os.path.join(data_dir, 'training')
        
        # Create required directories
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
        os.makedirs(self.training_data_dir, exist_ok=True)
        
        # Citation pattern regex
        self.citation_patterns = {
            'case_law': r'([A-Z][a-z]+\s+v\.\s+[A-Z][a-z]+),\s+(\d+)\s+([A-Z]\.[A-Z]\.[a-z]+\.?)\s+(\d+)\s+\((\d{4})\)',
            'statute': r'(\d+)\s+([A-Z]\.[A-Z]\.[A-Z]\.[A-Z]\.?)\s+§\s+(\d+[a-z]?)',
            'regulation': r'(\d+)\s+C\.F\.R\.\s+§\s+(\d+\.\d+)',
            'constitution': r'([A-Z]\.[A-Z]\.\s+[A-Za-z]+\.?)\s+([IVX]+),\s+§\s+(\d+)'
        }
        
    def process_legal_cases(self, input_file: str) -> pd.DataFrame:
        """
        Process a file of legal cases and extract key information.
        
        Args:
            input_file: Path to the legal cases file
            
        Returns:
            DataFrame with processed legal cases
        """
        logger.info(f"Processing legal cases from {input_file}")
        
        if not os.path.exists(input_file):
            logger.error(f"File not found: {input_file}")
            return pd.DataFrame()
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            cases = []
            for case in data:
                # Extract and clean case text
                case_text = case.get('text', '')
                case_text = self.clean_text(case_text)
                
                # Extract citations
                citations = self.extract_citations(case_text)
                
                # Extract jurisdiction info
                jurisdiction = case.get('jurisdiction', '')
                
                cases.append({
                    'title': case.get('title', ''),
                    'text': case_text,
                    'citations': citations,
                    'jurisdiction': jurisdiction,
                    'date': case.get('date', ''),
                    'url': case.get('url', ''),
                    'category': case.get('category', '')
                })
                
            return pd.DataFrame(cases)
        
        except Exception as e:
            logger.error(f"Error processing legal cases: {str(e)}")
            return pd.DataFrame()
    
    def extract_citations(self, text: str) -> List[Dict[str, str]]:
        """
        Extract legal citations from text.
        
        Args:
            text: Legal text to extract citations from
            
        Returns:
            List of extracted citations with type and text
        """
        citations = []
        
        for citation_type, pattern in self.citation_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                citations.append({
                    'type': citation_type,
                    'text': match.group(0),
                    'start': match.start(),
                    'end': match.end()
                })
        
        return citations
    
    def clean_text(self, text: str) -> str:
        """
        Clean legal text by removing excessive whitespace, normalizing formatting, etc.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Replace various types of quotation marks with standard ones
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove headers and footers (simplified approach)
        text = re.sub(r'\n\s*_{3,}.*?\n', '\n', text)
        
        return text.strip()
    
    def process_statutes(self, input_file: str) -> pd.DataFrame:
        """
        Process a file of legal statutes and extract key information.
        
        Args:
            input_file: Path to the legal statutes file
            
        Returns:
            DataFrame with processed statutes
        """
        logger.info(f"Processing statutes from {input_file}")
        
        if not os.path.exists(input_file):
            logger.error(f"File not found: {input_file}")
            return pd.DataFrame()
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            statutes = []
            for statute in data:
                # Extract and clean statute text
                statute_text = statute.get('text', '')
                statute_text = self.clean_text(statute_text)
                
                statutes.append({
                    'code': statute.get('code', ''),
                    'section': statute.get('section', ''),
                    'title': statute.get('title', ''),
                    'text': statute_text,
                    'jurisdiction': statute.get('jurisdiction', ''),
                    'effective_date': statute.get('effective_date', ''),
                    'url': statute.get('url', '')
                })
                
            return pd.DataFrame(statutes)
        
        except Exception as e:
            logger.error(f"Error processing statutes: {str(e)}")
            return pd.DataFrame()
    
    def create_qa_pairs(self, legal_df: pd.DataFrame, qa_template_file: str) -> pd.DataFrame:
        """
        Create question-answer pairs from legal data using templates.
        
        Args:
            legal_df: DataFrame containing legal data
            qa_template_file: File containing question templates
            
        Returns:
            DataFrame with generated question-answer pairs
        """
        logger.info("Creating question-answer pairs from legal data")
        
        if legal_df.empty:
            logger.error("No legal data provided")
            return pd.DataFrame()
        
        if not os.path.exists(qa_template_file):
            logger.error(f"Template file not found: {qa_template_file}")
            return pd.DataFrame()
        
        try:
            with open(qa_template_file, 'r', encoding='utf-8') as f:
                templates = json.load(f)
                
            qa_pairs = []
            
            for _, row in legal_df.iterrows():
                for template in templates:
                    # Skip templates that don't match the category
                    if 'category' in template and row.get('category') != template['category']:
                        continue
                        
                    # Generate question from template
                    question = template['question'].format(**row)
                    
                    # Generate answer
                    if 'answer_template' in template:
                        answer = template['answer_template'].format(**row)
                    else:
                        # Default to using the text field
                        answer = row.get('text', '')
                        
                    qa_pairs.append({
                        'question': question,
                        'answer': answer,
                        'jurisdiction': row.get('jurisdiction', ''),
                        'category': row.get('category', ''),
                        'source': row.get('url', '')
                    })
                    
            return pd.DataFrame(qa_pairs)
        
        except Exception as e:
            logger.error(f"Error creating QA pairs: {str(e)}")
            return pd.DataFrame()
    
    def generate_training_data(self, output_file: str):
        """
        Generate training data by combining processed data from various sources.
        
        Args:
            output_file: Path to save the training data
        """
        logger.info(f"Generating training data and saving to {output_file}")
        
        # Process cases
        cases_file = os.path.join(self.raw_data_dir, 'cases.json')
        cases_df = self.process_legal_cases(cases_file)
        
        # Process statutes
        statutes_file = os.path.join(self.raw_data_dir, 'statutes.json')
        statutes_df = self.process_statutes(statutes_file)
        
        # Create QA pairs
        qa_template_file = os.path.join(self.raw_data_dir, 'qa_templates.json')
        cases_qa_df = self.create_qa_pairs(cases_df, qa_template_file)
        statutes_qa_df = self.create_qa_pairs(statutes_df, qa_template_file)
        
        # Combine QA pairs
        qa_df = pd.concat([cases_qa_df, statutes_qa_df], ignore_index=True)
        
        # Save to file
        qa_df.to_json(output_file, orient='records', lines=True)
        
        logger.info(f"Generated {len(qa_df)} QA pairs for training")
        
        return qa_df

    def prepare_data_for_vector_db(self, input_files: List[str], output_file: str):
        """
        Prepare data for vector database by chunking text and formatting for embedding.
        
        Args:
            input_files: List of input files containing legal text
            output_file: File to save vectorizable data
        """
        logger.info(f"Preparing data for vector database from {len(input_files)} sources")
        
        chunks = []
        
        for file in input_files:
            if not os.path.exists(file):
                logger.warning(f"File not found: {file}")
                continue
                
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    # Extract text
                    text = item.get('text', '')
                    
                    if not text:
                        continue
                    
                    # Chunk text into smaller pieces
                    text_chunks = self.chunk_text(text, max_length=512)
                    
                    for i, chunk in enumerate(text_chunks):
                        chunks.append({
                            'id': f"{item.get('id', 'unknown')}_{i}",
                            'text': chunk,
                            'metadata': {
                                'source': item.get('url', ''),
                                'title': item.get('title', ''),
                                'jurisdiction': item.get('jurisdiction', ''),
                                'category': item.get('category', ''),
                                'date': item.get('date', '')
                            }
                        })
            
            except Exception as e:
                logger.error(f"Error processing {file}: {str(e)}")
        
        # Save chunks for vector database
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2)
            
        logger.info(f"Generated {len(chunks)} chunks for vector database")
        
        return chunks
    
    def chunk_text(self, text: str, max_length: int = 512, 
                  overlap: int = 50) -> List[str]:
        """
        Chunk text into smaller pieces for processing.
        
        Args:
            text: Text to chunk
            max_length: Maximum length of each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Find a good breaking point (period, newline, etc.)
            end = min(start + max_length, text_length)
            
            if end < text_length:
                # Try to find a period or newline to break at
                period_pos = text.rfind('.', start, end)
                newline_pos = text.rfind('\n', start, end)
                
                break_pos = max(period_pos, newline_pos)
                
                if break_pos > start:
                    end = break_pos + 1
            
            chunks.append(text[start:end])
            start = end - overlap
            
        return chunks

if __name__ == "__main__":
    processor = LegalDataProcessor()
    
    # Example usage:
    # Generate training data
    processor.generate_training_data(os.path.join(processor.training_data_dir, 'legal_qa_pairs.jsonl'))
    
    # Prepare data for vector database
    input_files = [
        os.path.join(processor.raw_data_dir, 'cases.json'),
        os.path.join(processor.raw_data_dir, 'statutes.json')
    ]
    processor.prepare_data_for_vector_db(input_files, 
                                        os.path.join(processor.processed_data_dir, 'vector_db_chunks.json')) 
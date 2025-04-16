"""
Document Analysis AI Module for SmartProBono
This module provides document analysis capabilities using AI models.
"""

import os
import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Placeholder for actual AI model integration
# In a production environment, you would use a real AI model API like OpenAI, HuggingFace, etc.

class DocumentAnalyzer:
    """
    Document analyzer service for legal documents.
    Provides methods to analyze various types of legal documents including
    contracts, legal briefs, and immigration forms.
    """
    
    def __init__(self, model_name: str = "legal-document-analyzer-v1"):
        """
        Initialize the document analyzer.
        
        Args:
            model_name: Name of the AI model to use (placeholder for future AI integration)
        """
        self.model_name = model_name
        logger.info(f"Initializing DocumentAnalyzer with model: {model_name}")
        self.api_key = os.environ.get('AI_API_KEY', 'demo_key')
        
        # Load document templates and patterns
        self._load_document_templates()
        
        self.supported_types = {
            "contract": self._analyze_contract,
            "legal_brief": self._analyze_legal_brief,
            "immigration_form": self._analyze_immigration_form
        }
    
    def _load_document_templates(self):
        """Load document templates and patterns from JSON files."""
        try:
            # In a real implementation, you would load actual templates
            self.templates = {
                "contract": {
                    "sections": ["parties", "terms", "conditions", "termination", "signatures"],
                    "required_fields": ["party_names", "effective_date", "term_length"]
                },
                "legal_brief": {
                    "sections": ["summary", "facts", "issues", "arguments", "conclusion"],
                    "required_fields": ["case_number", "court", "parties", "date"]
                },
                "immigration_form": {
                    "sections": ["personal_info", "travel_history", "purpose", "declarations"],
                    "required_fields": ["full_name", "nationality", "passport_number", "visa_type"]
                }
            }
        except Exception as e:
            print(f"Error loading document templates: {e}")
            self.templates = {}
    
    def analyze_document(self, text: Optional[str], doc_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a document and return structured analysis results.
        
        Args:
            text: The document text to analyze
            doc_type: Optional document type hint (contract, legal_brief, immigration_form)
            
        Returns:
            Dictionary containing analysis results
            
        Raises:
            ValueError: If text is empty or invalid
        """
        if not text:
            raise ValueError("Document text cannot be empty")
            
        try:
            # Detect document type if not provided
            doc_type = doc_type or self._detect_document_type(text)
            
            # Perform basic analysis
            basic_analysis = self._perform_basic_analysis(text)
            
            # Extract common entities
            entities = self._extract_entities(text)
            basic_analysis['named_entities'] = entities
            
            # Add complexity metrics
            basic_analysis['complexity_metrics'] = self._analyze_complexity(text)
            
            # Document type specific analysis
            specific_analysis = {}
            
            if doc_type == 'contract':
                specific_analysis = {
                    'contract_analysis': {
                        'parties': self._extract_parties(text),
                        'dates': self._extract_dates(text),
                        'key_clauses': self._identify_contract_clauses(text),
                        'obligations': self._extract_obligations(text),
                        'termination_conditions': self._find_termination_conditions(text)
                    }
                }
            elif doc_type == 'legal_brief':
                specific_analysis = {
                    'brief_analysis': {
                        'citations': self._extract_citations(text),
                        'arguments': self._identify_legal_arguments(text),
                        'requested_relief': self._extract_requested_relief(text),
                        'jurisdiction': self._identify_jurisdiction(text)
                    }
                }
            elif doc_type == 'immigration_form':
                specific_analysis = {
                    'immigration_analysis': {
                        'form_type': self._identify_form_type(text),
                        'personal_info': self._extract_personal_info(text),
                        'travel_history': self._extract_travel_history(text),
                        'required_documents': self._identify_required_documents(text)
                    }
                }
            
            # Add document structure analysis
            structure_analysis = self._analyze_structure(text)
            
            # Identify main topics
            topics = self._identify_topics(text)
            
            return {
                'document_type': doc_type,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'basic_analysis': basic_analysis,
                'structure': structure_analysis,
                'topics': topics,
                **specific_analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise ValueError(f"Failed to analyze document: {str(e)}")
    
    def _perform_basic_analysis(self, text: str) -> Dict[str, Any]:
        """Perform basic text analysis."""
        try:
            words = text.split()
            sentences = text.split('.')
            
            return {
                'length': len(text),
                'word_count': len(words),
                'sentence_count': len(sentences),
                'key_phrases': self._extract_key_phrases(text),
                'flesch_score': self._calculate_flesch_score(text)
            }
        except Exception as e:
            logger.error(f"Error in basic analysis: {str(e)}")
            return {
                'length': 0,
                'word_count': 0,
                'sentence_count': 0,
                'key_phrases': [],
                'flesch_score': 0
            }
    
    def _detect_document_type(self, text: str) -> str:
        """Detect the type of document based on content analysis."""
        text_lower = text.lower()
        
        # Check for contract indicators
        if any(word in text_lower for word in ['agreement', 'contract', 'parties', 'terms and conditions']):
            return 'contract'
            
        # Check for legal brief indicators
        if any(word in text_lower for word in ['court', 'plaintiff', 'defendant', 'motion', 'brief']):
            return 'legal_brief'
            
        # Check for immigration form indicators
        if any(word in text_lower for word in ['form i-', 'uscis', 'immigration', 'visa', 'passport']):
            return 'immigration_form'
            
        # Default to generic if no clear indicators
        return 'unknown'
    
    def _analyze_contract(self, text: str) -> Dict[str, Any]:
        """Analyze contract documents"""
        parties = self._extract_parties(text)
        dates = self._extract_dates(text)
        
        return {
            "contract_analysis": {
            "parties": parties,
                "dates": dates,
                "key_clauses": self._identify_contract_clauses(text),
            "obligations": self._extract_obligations(text),
                "termination_conditions": self._find_termination_conditions(text)
            }
        }
    
    def _analyze_legal_brief(self, text: str) -> Dict[str, Any]:
        """Analyze legal briefs"""
        return {
            "brief_analysis": {
                "case_citations": self._extract_citations(text),
                "legal_arguments": self._identify_legal_arguments(text),
                "requested_relief": self._extract_requested_relief(text),
                "jurisdiction": self._identify_jurisdiction(text)
            }
        }
    
    def _analyze_immigration_form(self, text: str) -> Dict[str, Any]:
        """Analyze immigration forms"""
        return {
            "immigration_analysis": {
                "form_type": self._identify_form_type(text),
                "personal_info": self._extract_personal_info(text),
            "travel_history": self._extract_travel_history(text),
                "required_documents": self._identify_required_documents(text)
            }
        }
    
    def _analyze_generic(self, text: str) -> Dict[str, Any]:
        """Analyze unknown document types"""
        # First extract basic entities
        entities = self._extract_entities(text) if hasattr(self, '_extract_entities') else {}
        
        # Perform structural analysis
        structure = self._analyze_structure(text)
        
        # Identify key topics
        topics = self._identify_topics(text)
        
        # Combine all analyses
        return {
            "generic_analysis": {
                "document_structure": structure,
                "named_entities": entities,
                "key_topics": topics,
                "complexity": self._analyze_complexity(text)
            }
        }
    
    def _analyze_complexity(self, text: str) -> Dict[str, float]:
        words = text.split()
        complex_words = [w for w in words if len(w) > 6]
        return {
            "flesch_reading_ease": self._calculate_flesch_score(text),
            "complex_word_ratio": len(complex_words) / len(words) if words else 0
        }
    
    def _extract_key_phrases(self, text: str, max_phrases: int = 5) -> list:
        # Simple implementation - could be enhanced with NLP
        sentences = re.split(r'[.!?]+', text)
        important_sentences = [s.strip() for s in sentences if any(marker in s.lower() for marker in 
            ["important", "shall", "must", "required", "agree", "terminate", "warrant"])]
        return important_sentences[:max_phrases]
    
    def _extract_parties(self, text: str) -> list:
        parties = []
        party_patterns = [
            r"(?:between|party)\s+([A-Za-z\s,]+)(?:and|,)",
            r"([A-Za-z\s]+)(?:\(\".*?\"\))",
        ]
        
        for pattern in party_patterns:
            matches = re.finditer(pattern, text)
            parties.extend(match.group(1).strip() for match in matches)
        
        return list(set(parties))
    
    def _extract_dates(self, text: str) -> Dict[str, str]:
        dates = {}
        date_patterns = {
            "effective_date": r"effective\s+date.*?(\w+\s+\d{1,2},?\s+\d{4})",
            "execution_date": r"executed\s+on.*?(\w+\s+\d{1,2},?\s+\d{4})",
            "termination_date": r"terminate.*?on.*?(\w+\s+\d{1,2},?\s+\d{4})"
        }
        
        for date_type, pattern in date_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                dates[date_type] = match.group(1)
        
        return dates
    
    def _identify_contract_clauses(self, text: str) -> Dict[str, str]:
        clauses = {}
        clause_patterns = {
            "confidentiality": r"(?:confidentiality|confidential information).*?(?=\n\n|\Z)",
            "termination": r"(?:termination|terminate).*?(?=\n\n|\Z)",
            "indemnification": r"(?:indemnification|indemnify).*?(?=\n\n|\Z)",
            "governing_law": r"(?:governing law|jurisdiction).*?(?=\n\n|\Z)"
        }
        
        for clause_type, pattern in clause_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                clauses[clause_type] = match.group(0).strip()
        
        return clauses
    
    def _calculate_flesch_score(self, text: str) -> float:
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        syllables = sum(self._count_syllables(word) for word in words)
        
        if not sentences or not words:
            return 0.0
            
        return 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))
    
    def _count_syllables(self, word: str) -> int:
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
            
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
            
        return count

    def _extract_obligations(self, text: str) -> List[str]:
        """Extract obligations from contract text."""
        obligations = []
        patterns = [
            r"shall\s+([^\.;]+)",
            r"must\s+([^\.;]+)",
            r"agrees\s+to\s+([^\.;]+)"
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            obligations.extend(match.group(1).strip() for match in matches)
        
        return obligations
    
    def _find_termination_conditions(self, text: str) -> List[str]:
        """Find termination conditions in contract."""
        conditions = []
        patterns = [
            r"(?:may\s+terminate|termination).*?(?:if|upon|in\s+the\s+event)([^\.;]+)",
            r"(?:grounds\s+for\s+termination)([^\.;]+)"
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            conditions.extend(match.group(1).strip() for match in matches)
        
        return conditions

    def _extract_citations(self, text: str) -> List[str]:
        """Extract legal citations from text."""
        citations = []
        patterns = [
            r"\d+\s+U\.S\.\s+\d+\s+\(\d{4}\)",  # Supreme Court
            r"\d+\s+F\.\d+\s+\d+\s+\(\d+\w+\s+Cir\.\s+\d{4}\)",  # Circuit Courts
            r"\d+\s+F\.\s*Supp\.\s*\d+\s+\(\w+\s+\d{4}\)"  # District Courts
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            citations.extend(match.group(0) for match in matches)
        
        return citations

    def _identify_legal_arguments(self, text: str) -> List[Dict[str, str]]:
        """Identify legal arguments in brief."""
        arguments = []
        sections = re.split(r'\n(?=[A-Z][A-Z\s]+\n)', text)
        
        for section in sections:
            if any(header in section.upper() for header in ['ARGUMENT', 'DISCUSSION']):
                arguments.append({
                    'heading': section.split('\n')[0].strip(),
                    'content': ' '.join(section.split('\n')[1:]).strip()
                })
        
        return arguments

    def _extract_requested_relief(self, text: str) -> str:
        """Extract requested relief from legal brief."""
        patterns = [
            r"WHEREFORE[^.]*?(?:plaintiff|defendant|petitioner).*?(?:requests|demands|prays)[^.]*\.",
            r"PRAYER\s+FOR\s+RELIEF.*?(?=\n\n|\Z)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0).strip()
        
        return ""

    def _identify_jurisdiction(self, text: str) -> Dict[str, str]:
        """Identify jurisdiction information."""
        jurisdiction = {}
        
        court_match = re.search(r"IN\s+THE\s+([^,\n]+)(?:,|COURT)", text)
        if court_match:
            jurisdiction['court'] = court_match.group(1).strip()
        
        district_match = re.search(r"(?:DISTRICT|CIRCUIT)\s+OF\s+([^,\n]+)", text)
        if district_match:
            jurisdiction['district'] = district_match.group(1).strip()
        
        return jurisdiction

    def _identify_form_type(self, text: str) -> str:
        """Identify immigration form type."""
        form_match = re.search(r"FORM\s+([I|N|G]-\d+[A-Z]*)", text)
        if form_match:
            return form_match.group(1)
        return "Unknown"

    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extract personal information from immigration form."""
        info = {}
        patterns = {
            'name': r"(?:Full\s+Name|Name):\s*([^\n]+)",
            'dob': r"(?:Date\s+of\s+Birth|DOB):\s*([^\n]+)",
            'nationality': r"(?:Nationality|Citizenship):\s*([^\n]+)",
            'passport': r"Passport\s+(?:Number|No\.):\s*([^\n]+)"
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info[field] = match.group(1).strip()
        
        return info
    
    def _extract_travel_history(self, text: str) -> List[Dict[str, str]]:
        """Extract travel history from immigration form."""
        history = []
        pattern = r"(\d{2}/\d{2}/\d{4})\s+(?:to|until)\s+(\d{2}/\d{2}/\d{4})\s+([^\n]+)"
        
        matches = re.finditer(pattern, text)
        for match in matches:
            history.append({
                'start_date': match.group(1),
                'end_date': match.group(2),
                'location': match.group(3).strip()
            })
        
        return history

    def _identify_required_documents(self, text: str) -> List[str]:
        """Identify required supporting documents."""
        documents = []
        patterns = [
            r"Required\s+Documents?:(.*?)(?=\n\n|\Z)",
            r"(?:Submit|Include|Attach)\s+the\s+following:(.*?)(?=\n\n|\Z)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                # Split by bullet points or numbers
                items = re.split(r'(?:\n\s*•|\n\s*\d+\.)\s*', match.group(1))
                documents.extend(item.strip() for item in items if item.strip())
        
        return documents

    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze document structure."""
        sections = text.split('\n\n')
        return {
            'section_count': len(sections),
            'sections': [section[:100] + '...' if len(section) > 100 else section 
                        for section in sections[:5]]  # First 5 sections
        }

    def _identify_topics(self, text: str) -> List[str]:
        """Identify main topics in document."""
        # Simple keyword-based topic identification
        topics = []
        topic_patterns = {
            'financial': r'(?:payment|money|financial|cost|price)',
            'legal': r'(?:law|legal|court|rights|jurisdiction)',
            'employment': r'(?:employee|employer|work|salary|position)',
            'property': r'(?:property|premises|lease|rent|building)',
            'immigration': r'(?:visa|passport|citizen|alien|status)'
        }
        
        for topic, pattern in topic_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                topics.append(topic)
        
        return topics
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text."""
        entities = {
            'organizations': [],
            'people': [],
            'dates': [],
            'monetary_values': []
        }
        
        # Organization patterns (e.g., Company Inc., Corp., LLC)
        org_pattern = r'(?:[A-Z][a-z]+\s+)+(?:Inc\.|Corp\.|LLC|Ltd\.|Corporation|Company)'
        entities['organizations'].extend(re.findall(org_pattern, text))
        
        # People patterns (e.g., Mr. John Smith, Dr. Jane Doe)
        people_pattern = r'(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+(?:[A-Z][a-z]+\s+)+[A-Z][a-z]+'
        entities['people'].extend(re.findall(people_pattern, text))
        
        # Date patterns (various formats)
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}-\d{2}-\d{2}',       # YYYY-MM-DD
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}'
        ]
        for pattern in date_patterns:
            entities['dates'].extend(re.findall(pattern, text))
        
        # Monetary values
        money_pattern = r'\$\d+(?:,\d{3})*(?:\.\d{2})?'
        entities['monetary_values'].extend(re.findall(money_pattern, text))
        
        return entities

# Example usage
if __name__ == "__main__":
    analyzer = DocumentAnalyzer()
    
    # Example contract text
    sample_text = """
    AGREEMENT
    
    This Agreement is made on April 15, 2023, between ABC Corporation, a Delaware corporation ("Company"), and John Smith, an individual ("Consultant").
    
    1. SERVICES
    Consultant shall provide marketing consulting services to Company as described in Exhibit A.
    
    2. TERM
    This Agreement shall commence on April 20, 2023 and continue until October 20, 2023, unless terminated earlier.
    
    3. COMPENSATION
    Company shall pay Consultant $5,000 per month for services rendered.
    
    4. CONFIDENTIALITY
    Consultant shall maintain all confidential information in strict confidence.
    
    5. INDEMNIFICATION
    Consultant shall indemnify and hold Company harmless from any claims arising from Consultant's performance.
    
    6. TERMINATION
    Either party may terminate this Agreement with 30 days written notice.
    
    IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
    
    ABC Corporation
    By: Jane Doe, CEO
    
    John Smith
    """
    
    # Analyze the document
    result = analyzer.analyze_document(sample_text)
    print(json.dumps(result, indent=2))

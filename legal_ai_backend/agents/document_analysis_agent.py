"""
Document Analysis Agent
Analyzes legal documents and extracts key information
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentType(Enum):
    """Types of legal documents"""
    CONTRACT = "contract"
    COURT_FILING = "court_filing"
    LEGAL_BRIEF = "legal_brief"
    STATUTE = "statute"
    CASE_OPINION = "case_opinion"
    LEGAL_FORM = "legal_form"
    CORRESPONDENCE = "correspondence"
    OTHER = "other"

@dataclass
class DocumentEntity:
    """Represents an entity extracted from a document"""
    entity_type: str  # 'person', 'organization', 'date', 'amount', 'legal_concept'
    text: str
    start_pos: int
    end_pos: int
    confidence: float
    context: str

@dataclass
class DocumentAnalysis:
    """Result of document analysis"""
    document_type: DocumentType
    key_entities: List[DocumentEntity]
    legal_concepts: List[str]
    important_dates: List[Dict[str, Any]]
    parties: List[Dict[str, Any]]
    legal_issues: List[str]
    recommendations: List[str]
    risk_assessment: Dict[str, Any]
    summary: str
    confidence: float

class DocumentAnalysisAgent:
    """Agent for analyzing legal documents"""
    
    def __init__(self):
        self.document_patterns = self._initialize_document_patterns()
        self.legal_concepts_db = self._initialize_legal_concepts()
        self.entity_patterns = self._initialize_entity_patterns()
        
    def _initialize_document_patterns(self) -> Dict[DocumentType, List[str]]:
        """Initialize patterns for identifying document types"""
        return {
            DocumentType.CONTRACT: [
                "agreement", "contract", "terms and conditions", "party of the first part",
                "whereas", "now therefore", "in consideration of"
            ],
            DocumentType.COURT_FILING: [
                "motion", "petition", "complaint", "answer", "brief", "memorandum",
                "in the matter of", "case number", "filed with the court"
            ],
            DocumentType.LEGAL_BRIEF: [
                "statement of facts", "argument", "conclusion", "appellant", "appellee",
                "standard of review", "legal authority"
            ],
            DocumentType.STATUTE: [
                "section", "subsection", "chapter", "title", "act of", "be it enacted",
                "legislative intent", "effective date"
            ],
            DocumentType.CASE_OPINION: [
                "opinion", "judgment", "holding", "concurring", "dissenting",
                "court finds", "we hold", "affirmed", "reversed"
            ],
            DocumentType.LEGAL_FORM: [
                "form", "application", "petition for", "declaration under penalty",
                "i hereby", "sworn to", "notary public"
            ]
        }
    
    def _initialize_legal_concepts(self) -> Dict[str, List[str]]:
        """Initialize database of legal concepts and their indicators"""
        return {
            "contract_law": [
                "consideration", "offer", "acceptance", "breach", "damages",
                "specific performance", "rescission", "reformation"
            ],
            "criminal_law": [
                "mens rea", "actus reus", "beyond reasonable doubt", "burden of proof",
                "presumption of innocence", "exclusionary rule", "miranda rights"
            ],
            "civil_procedure": [
                "subject matter jurisdiction", "personal jurisdiction", "venue",
                "statute of limitations", "discovery", "summary judgment"
            ],
            "constitutional_law": [
                "due process", "equal protection", "first amendment", "fourth amendment",
                "fifth amendment", "fourteenth amendment", "strict scrutiny"
            ],
            "tort_law": [
                "negligence", "duty of care", "breach", "causation", "damages",
                "strict liability", "intentional tort", "defamation"
            ]
        }
    
    def _initialize_entity_patterns(self) -> Dict[str, str]:
        """Initialize regex patterns for entity extraction"""
        return {
            "person": r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            "organization": r'\b[A-Z][a-z]+ (?:Inc|LLC|Corp|Company|Associates|Partners)\b',
            "date": r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            "amount": r'\$[\d,]+(?:\.\d{2})?',
            "case_number": r'Case No\.?\s*[A-Z0-9-]+',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
    
    def analyze_document(self, text: str, filename: Optional[str] = None) -> DocumentAnalysis:
        """Analyze a legal document and extract key information"""
        try:
            # Identify document type
            doc_type = self._identify_document_type(text, filename)
            
            # Extract entities
            entities = self._extract_entities(text)
            
            # Identify legal concepts
            legal_concepts = self._identify_legal_concepts(text)
            
            # Extract important dates
            important_dates = self._extract_dates(text)
            
            # Identify parties
            parties = self._identify_parties(text, entities)
            
            # Identify legal issues
            legal_issues = self._identify_legal_issues(text, legal_concepts)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(doc_type, legal_issues, entities)
            
            # Assess risks
            risk_assessment = self._assess_risks(doc_type, legal_issues, entities)
            
            # Generate summary
            summary = self._generate_summary(doc_type, legal_issues, parties, important_dates)
            
            # Calculate confidence
            confidence = self._calculate_confidence(entities, legal_concepts, doc_type)
            
            return DocumentAnalysis(
                document_type=doc_type,
                key_entities=entities,
                legal_concepts=legal_concepts,
                important_dates=important_dates,
                parties=parties,
                legal_issues=legal_issues,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                summary=summary,
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            return self._create_fallback_analysis()
    
    def _identify_document_type(self, text: str, filename: Optional[str]) -> DocumentType:
        """Identify the type of legal document"""
        text_lower = text.lower()
        
        # Check filename first
        if filename:
            filename_lower = filename.lower()
            for doc_type, patterns in self.document_patterns.items():
                for pattern in patterns:
                    if pattern in filename_lower:
                        return doc_type
        
        # Check content patterns
        type_scores = {}
        for doc_type, patterns in self.document_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 1
            type_scores[doc_type] = score
        
        # Return type with highest score, or OTHER if no clear match
        if type_scores:
            best_type = max(type_scores, key=type_scores.get)
            if type_scores[best_type] > 0:
                return best_type
        
        return DocumentType.OTHER
    
    def _extract_entities(self, text: str) -> List[DocumentEntity]:
        """Extract named entities from the document"""
        entities = []
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity = DocumentEntity(
                    entity_type=entity_type,
                    text=match.group(),
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=self._calculate_entity_confidence(match.group(), entity_type),
                    context=self._get_entity_context(text, match.start(), match.end())
                )
                entities.append(entity)
        
        return entities
    
    def _calculate_entity_confidence(self, text: str, entity_type: str) -> float:
        """Calculate confidence score for an entity"""
        # Simple confidence calculation based on format
        if entity_type == "person":
            # Check if it looks like a name (two capitalized words)
            words = text.split()
            if len(words) == 2 and all(word[0].isupper() for word in words):
                return 0.9
            return 0.6
        elif entity_type == "date":
            # Dates are usually high confidence
            return 0.8
        elif entity_type == "amount":
            # Money amounts are usually high confidence
            return 0.9
        else:
            return 0.7
    
    def _get_entity_context(self, text: str, start: int, end: int, context_length: int = 50) -> str:
        """Get context around an entity"""
        context_start = max(0, start - context_length)
        context_end = min(len(text), end + context_length)
        return text[context_start:context_end].strip()
    
    def _identify_legal_concepts(self, text: str) -> List[str]:
        """Identify legal concepts mentioned in the document"""
        concepts = []
        text_lower = text.lower()
        
        for category, concept_list in self.legal_concepts_db.items():
            for concept in concept_list:
                if concept.lower() in text_lower:
                    concepts.append(concept)
        
        return list(set(concepts))  # Remove duplicates
    
    def _extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract important dates from the document"""
        dates = []
        date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        
        matches = re.finditer(date_pattern, text, re.IGNORECASE)
        for match in matches:
            date_text = match.group()
            dates.append({
                "text": date_text,
                "position": match.start(),
                "context": self._get_entity_context(text, match.start(), match.end())
            })
        
        return dates
    
    def _identify_parties(self, text: str, entities: List[DocumentEntity]) -> List[Dict[str, Any]]:
        """Identify parties mentioned in the document"""
        parties = []
        
        # Look for person entities
        person_entities = [e for e in entities if e.entity_type == "person"]
        for entity in person_entities:
            parties.append({
                "name": entity.text,
                "type": "individual",
                "context": entity.context,
                "confidence": entity.confidence
            })
        
        # Look for organization entities
        org_entities = [e for e in entities if e.entity_type == "organization"]
        for entity in org_entities:
            parties.append({
                "name": entity.text,
                "type": "organization",
                "context": entity.context,
                "confidence": entity.confidence
            })
        
        return parties
    
    def _identify_legal_issues(self, text: str, legal_concepts: List[str]) -> List[str]:
        """Identify legal issues based on concepts and context"""
        issues = []
        
        # Map concepts to potential issues
        concept_to_issue = {
            "breach": "Contract breach or violation",
            "negligence": "Negligence claim",
            "damages": "Damages or compensation",
            "jurisdiction": "Jurisdictional issues",
            "statute of limitations": "Timing or deadline issues",
            "due process": "Constitutional rights issues"
        }
        
        for concept in legal_concepts:
            if concept.lower() in concept_to_issue:
                issues.append(concept_to_issue[concept.lower()])
        
        return list(set(issues))
    
    def _generate_recommendations(self, doc_type: DocumentType, legal_issues: List[str], entities: List[DocumentEntity]) -> List[str]:
        """Generate recommendations based on document analysis"""
        recommendations = []
        
        if doc_type == DocumentType.CONTRACT:
            recommendations.append("Review contract terms carefully for any unfavorable clauses")
            recommendations.append("Consider having the contract reviewed by an attorney")
        
        if legal_issues:
            recommendations.append("Consult with an attorney about the identified legal issues")
        
        if any(e.entity_type == "amount" for e in entities):
            recommendations.append("Verify all monetary amounts and calculations")
        
        if any(e.entity_type == "date" for e in entities):
            recommendations.append("Check all dates for accuracy and compliance with deadlines")
        
        return recommendations
    
    def _assess_risks(self, doc_type: DocumentType, legal_issues: List[str], entities: List[DocumentEntity]) -> Dict[str, Any]:
        """Assess potential risks in the document"""
        risk_level = "low"
        risk_factors = []
        
        if len(legal_issues) > 3:
            risk_level = "high"
            risk_factors.append("Multiple legal issues identified")
        
        if doc_type == DocumentType.CONTRACT:
            risk_level = "medium"
            risk_factors.append("Contract requires careful review")
        
        if any(e.entity_type == "amount" and float(e.text.replace('$', '').replace(',', '')) > 100000 for e in entities):
            risk_level = "high"
            risk_factors.append("High monetary amounts involved")
        
        return {
            "level": risk_level,
            "factors": risk_factors,
            "recommendation": "Consult with an attorney" if risk_level in ["medium", "high"] else "Review carefully"
        }
    
    def _generate_summary(self, doc_type: DocumentType, legal_issues: List[str], parties: List[Dict[str, Any]], dates: List[Dict[str, Any]]) -> str:
        """Generate a summary of the document"""
        summary_parts = []
        
        summary_parts.append(f"This appears to be a {doc_type.value.replace('_', ' ')} document.")
        
        if parties:
            party_names = [p["name"] for p in parties[:3]]  # Limit to 3 parties
            summary_parts.append(f"Key parties include: {', '.join(party_names)}.")
        
        if legal_issues:
            summary_parts.append(f"Identified legal issues: {', '.join(legal_issues[:3])}.")
        
        if dates:
            summary_parts.append(f"Contains {len(dates)} important dates.")
        
        return " ".join(summary_parts)
    
    def _calculate_confidence(self, entities: List[DocumentEntity], legal_concepts: List[str], doc_type: DocumentType) -> float:
        """Calculate overall confidence in the analysis"""
        if not entities and not legal_concepts:
            return 0.3
        
        entity_confidence = sum(e.confidence for e in entities) / len(entities) if entities else 0.5
        concept_confidence = 0.8 if legal_concepts else 0.5
        type_confidence = 0.9 if doc_type != DocumentType.OTHER else 0.6
        
        return (entity_confidence + concept_confidence + type_confidence) / 3
    
    def _create_fallback_analysis(self) -> DocumentAnalysis:
        """Create fallback analysis when main analysis fails"""
        return DocumentAnalysis(
            document_type=DocumentType.OTHER,
            key_entities=[],
            legal_concepts=[],
            important_dates=[],
            parties=[],
            legal_issues=[],
            recommendations=["Unable to analyze document. Please consult with an attorney."],
            risk_assessment={"level": "unknown", "factors": ["Analysis failed"], "recommendation": "Manual review required"},
            summary="Unable to analyze this document automatically.",
            confidence=0.0
        )

# Global instance
document_analysis_agent = DocumentAnalysisAgent()

def analyze_document(text: str, filename: Optional[str] = None) -> DocumentAnalysis:
    """Analyze a legal document"""
    return document_analysis_agent.analyze_document(text, filename)

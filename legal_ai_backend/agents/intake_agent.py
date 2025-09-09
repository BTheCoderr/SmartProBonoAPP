"""
Intake Agent - Extracts legal topic, jurisdiction, and case details from user input.
Uses keyword matching and simple NLP to categorize the legal issue.
"""
import re
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LegalIntake:
    """Structured intake information extracted from user input."""
    topic: str
    jurisdiction: str
    case_type: str
    keywords: List[str]
    urgency: str
    original_input: str
    suggested_charges: List[str]

class IntakeAgent:
    """Agent responsible for parsing and categorizing legal queries."""
    
    def __init__(self):
        # Legal topic keywords mapping
        self.topic_keywords = {
            "criminal": [
                "gun", "firearm", "weapon", "possession", "assault", "battery",
                "theft", "robbery", "burglary", "drug", "dui", "dwi", "domestic",
                "violence", "threat", "harassment", "stalking", "fraud", "embezzlement"
            ],
            "civil": [
                "contract", "breach", "employment", "discrimination", "harassment",
                "personal injury", "accident", "negligence", "malpractice", "divorce",
                "custody", "support", "property", "landlord", "tenant", "eviction"
            ],
            "family": [
                "divorce", "custody", "child support", "alimony", "adoption",
                "guardianship", "restraining order", "domestic violence", "prenup"
            ],
            "immigration": [
                "visa", "green card", "citizenship", "deportation", "asylum",
                "refugee", "work permit", "naturalization", "border", "detention"
            ],
            "business": [
                "llc", "corporation", "partnership", "contract", "employment",
                "intellectual property", "trademark", "copyright", "patent",
                "business formation", "compliance", "tax", "licensing"
            ]
        }
        
        # Jurisdiction keywords
        self.jurisdiction_keywords = {
            "ri": ["rhode island", "ri", "providence", "cranston", "warwick"],
            "ma": ["massachusetts", "ma", "boston", "cambridge", "worcester"],
            "ct": ["connecticut", "ct", "hartford", "new haven", "stamford"],
            "ny": ["new york", "ny", "manhattan", "brooklyn", "queens"],
            "ca": ["california", "ca", "los angeles", "san francisco", "san diego"]
        }
        
        # Case type keywords
        self.case_type_keywords = {
            "criminal": ["charged", "arrested", "indicted", "convicted", "plea", "trial"],
            "civil": ["sued", "lawsuit", "claim", "damages", "settlement"],
            "administrative": ["license", "permit", "appeal", "hearing", "violation"]
        }
        
        # Urgency indicators
        self.urgency_keywords = {
            "high": ["urgent", "emergency", "arrested", "detained", "court tomorrow", "deadline"],
            "medium": ["soon", "next week", "upcoming", "scheduled"],
            "low": ["general", "information", "research", "curious"]
        }
    
    def extract_jurisdiction(self, text: str) -> str:
        """Extract jurisdiction from text."""
        text_lower = text.lower()
        
        for jurisdiction, keywords in self.jurisdiction_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return jurisdiction
        
        # Default to Rhode Island if not specified
        return "ri"
    
    def extract_topic(self, text: str) -> str:
        """Extract legal topic from text."""
        text_lower = text.lower()
        
        # Count matches for each topic
        topic_scores = {}
        for topic, keywords in self.topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        
        return "general"
    
    def extract_case_type(self, text: str) -> str:
        """Extract case type from text."""
        text_lower = text.lower()
        
        for case_type, keywords in self.case_type_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return case_type
        
        return "general"
    
    def extract_urgency(self, text: str) -> str:
        """Extract urgency level from text."""
        text_lower = text.lower()
        
        for urgency, keywords in self.urgency_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return urgency
        
        return "medium"
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        # Simple keyword extraction - could be enhanced with NLP
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter for legal-relevant keywords
        legal_keywords = []
        all_keywords = []
        for topic_keywords in self.topic_keywords.values():
            all_keywords.extend(topic_keywords)
        
        for word in words:
            if word in all_keywords and word not in legal_keywords:
                legal_keywords.append(word)
        
        return legal_keywords
    
    def suggest_charges(self, topic: str, keywords: List[str]) -> List[str]:
        """Suggest possible charges based on topic and keywords."""
        charge_suggestions = {
            "criminal": {
                "gun": ["Unlawful possession of firearm", "Carrying without license", "Possession of weapon"],
                "assault": ["Simple assault", "Aggravated assault", "Battery"],
                "drug": ["Possession of controlled substance", "Drug trafficking", "Drug distribution"],
                "theft": ["Larceny", "Robbery", "Burglary", "Fraud"]
            }
        }
        
        suggestions = []
        if topic in charge_suggestions:
            for keyword in keywords:
                if keyword in charge_suggestions[topic]:
                    suggestions.extend(charge_suggestions[topic][keyword])
        
        return list(set(suggestions))  # Remove duplicates
    
    def process_intake(self, user_input: str) -> LegalIntake:
        """
        Process user input and extract structured legal information.
        
        Args:
            user_input: Raw user input text
            
        Returns:
            LegalIntake object with extracted information
        """
        try:
            # Extract basic information
            jurisdiction = self.extract_jurisdiction(user_input)
            topic = self.extract_topic(user_input)
            case_type = self.extract_case_type(user_input)
            urgency = self.extract_urgency(user_input)
            keywords = self.extract_keywords(user_input)
            suggested_charges = self.suggest_charges(topic, keywords)
            
            intake = LegalIntake(
                topic=topic,
                jurisdiction=jurisdiction,
                case_type=case_type,
                keywords=keywords,
                urgency=urgency,
                original_input=user_input,
                suggested_charges=suggested_charges
            )
            
            logger.info(f"Processed intake: {topic} case in {jurisdiction}")
            return intake
            
        except Exception as e:
            logger.error(f"Error processing intake: {e}")
            # Return default intake on error
            return LegalIntake(
                topic="general",
                jurisdiction="ri",
                case_type="general",
                keywords=[],
                urgency="medium",
                original_input=user_input,
                suggested_charges=[]
            )

def intake(user_input: str) -> Dict[str, Any]:
    """
    Main intake function for LangGraph.
    
    Args:
        user_input: Raw user input
        
    Returns:
        Dictionary with intake information
    """
    agent = IntakeAgent()
    intake_result = agent.process_intake(user_input)
    
    return {
        "topic": intake_result.topic,
        "jurisdiction": intake_result.jurisdiction,
        "case_type": intake_result.case_type,
        "keywords": intake_result.keywords,
        "urgency": intake_result.urgency,
        "original_input": intake_result.original_input,
        "suggested_charges": intake_result.suggested_charges
    }

# Example usage and testing
if __name__ == "__main__":
    # Test the intake agent
    test_inputs = [
        "I was charged with gun possession in Boston, what should I do?",
        "I need help with a divorce case in Rhode Island",
        "My landlord is trying to evict me, is this legal?",
        "I was arrested for DUI last night, urgent help needed"
    ]
    
    agent = IntakeAgent()
    
    for test_input in test_inputs:
        print(f"Input: {test_input}")
        result = agent.process_intake(test_input)
        print(f"Topic: {result.topic}")
        print(f"Jurisdiction: {result.jurisdiction}")
        print(f"Case Type: {result.case_type}")
        print(f"Urgency: {result.urgency}")
        print(f"Keywords: {result.keywords}")
        print(f"Suggested Charges: {result.suggested_charges}")
        print("-" * 50)

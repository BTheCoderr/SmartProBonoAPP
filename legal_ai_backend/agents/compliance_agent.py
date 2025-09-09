"""
Compliance Agent - Adds legal disclaimers and ensures ethical AI usage.
Provides appropriate warnings and compliance measures.
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class ComplianceResult:
    """Structured compliance result with disclaimers and warnings."""
    analysis: Dict[str, Any]
    disclaimers: List[str]
    warnings: List[str]
    recommendations: List[str]
    timestamp: str
    compliance_level: str

class ComplianceAgent:
    """Agent responsible for legal compliance and ethical AI usage."""
    
    def __init__(self):
        self.disclaimers = [
            "⚠️ **NOT LEGAL ADVICE**: This analysis is for informational purposes only and does not constitute legal advice.",
            "⚖️ **CONSULT AN ATTORNEY**: Always consult with a qualified, licensed attorney for specific legal advice about your situation.",
            "📅 **CASE LAW CHANGES**: Court decisions and laws may have changed since these cases were decided.",
            "🔍 **UNIQUE CIRCUMSTANCES**: Each legal case is unique and outcomes may vary based on specific facts and circumstances.",
            "🏛️ **JURISDICTION SPECIFIC**: Laws vary by jurisdiction. This analysis may not apply to your specific location.",
            "⏰ **TIME SENSITIVE**: Legal deadlines and statutes of limitations may apply to your case."
        ]
        
        self.warnings = {
            "criminal": [
                "🚨 **URGENT**: Criminal charges require immediate legal representation.",
                "📞 **CONTACT ATTORNEY NOW**: Do not speak to law enforcement without an attorney present.",
                "📋 **DOCUMENT EVERYTHING**: Keep records of all interactions and evidence."
            ],
            "civil": [
                "⏰ **DEADLINES**: Civil cases have strict filing deadlines.",
                "📄 **EVIDENCE PRESERVATION**: Preserve all relevant documents and evidence.",
                "💰 **DAMAGES**: Consider the potential financial impact of your case."
            ],
            "family": [
                "👨‍👩‍👧‍👦 **CHILDREN INVOLVED**: Family law cases involving children have special considerations.",
                "📋 **DOCUMENTATION**: Keep detailed records of all interactions and agreements.",
                "🤝 **MEDIATION**: Consider mediation or collaborative law approaches."
            ]
        }
        
        self.recommendations = {
            "high_urgency": [
                "Contact a qualified attorney immediately",
                "Do not delay in seeking legal representation",
                "Consider emergency legal aid services if you cannot afford an attorney"
            ],
            "medium_urgency": [
                "Schedule a consultation with an attorney within the next week",
                "Gather all relevant documents and evidence",
                "Research qualified attorneys in your area"
            ],
            "low_urgency": [
                "Consider scheduling a consultation with an attorney",
                "Research your legal rights and options",
                "Keep records of any relevant communications or events"
            ]
        }
    
    def determine_compliance_level(self, context: Dict[str, Any]) -> str:
        """
        Determine the appropriate compliance level based on context.
        
        Args:
            context: Intake context with legal information
            
        Returns:
            Compliance level: 'high', 'medium', or 'low'
        """
        urgency = context.get("urgency", "medium")
        case_type = context.get("case_type", "general")
        topic = context.get("topic", "general")
        
        # High compliance for criminal cases or high urgency
        if case_type == "criminal" or urgency == "high" or topic == "criminal":
            return "high"
        
        # Medium compliance for civil cases or medium urgency
        elif case_type == "civil" or urgency == "medium" or topic in ["civil", "family"]:
            return "medium"
        
        # Low compliance for general information requests
        else:
            return "low"
    
    def get_case_specific_warnings(self, context: Dict[str, Any]) -> List[str]:
        """
        Get case-specific warnings based on the legal topic.
        
        Args:
            context: Intake context with legal information
            
        Returns:
            List of case-specific warnings
        """
        case_type = context.get("case_type", "general")
        topic = context.get("topic", "general")
        
        warnings = []
        
        # Add general warnings
        if case_type in self.warnings:
            warnings.extend(self.warnings[case_type])
        
        if topic in self.warnings:
            warnings.extend(self.warnings[topic])
        
        # Add specific warnings based on keywords
        keywords = context.get("keywords", [])
        if "gun" in keywords or "firearm" in keywords:
            warnings.append("🔫 **FIREARM CHARGES**: Gun-related charges often carry severe penalties and require specialized legal expertise.")
        
        if "domestic" in keywords or "violence" in keywords:
            warnings.append("🏠 **DOMESTIC VIOLENCE**: These cases involve complex legal and safety considerations.")
        
        if "drug" in keywords:
            warnings.append("💊 **DRUG CHARGES**: Drug-related charges have specific legal procedures and potential mandatory minimums.")
        
        return list(set(warnings))  # Remove duplicates
    
    def get_recommendations(self, context: Dict[str, Any]) -> List[str]:
        """
        Get recommendations based on urgency and case type.
        
        Args:
            context: Intake context with legal information
            
        Returns:
            List of recommendations
        """
        urgency = context.get("urgency", "medium")
        case_type = context.get("case_type", "general")
        
        # Determine recommendation level
        if urgency == "high" or case_type == "criminal":
            rec_level = "high_urgency"
        elif urgency == "medium" or case_type == "civil":
            rec_level = "medium_urgency"
        else:
            rec_level = "low_urgency"
        
        recommendations = self.recommendations.get(rec_level, [])
        
        # Add case-specific recommendations
        if case_type == "criminal":
            recommendations.extend([
                "Research criminal defense attorneys in your area",
                "Consider public defender services if you cannot afford private counsel",
                "Do not discuss your case with anyone except your attorney"
            ])
        
        return recommendations
    
    def add_compliance_measures(
        self, 
        analysis: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> ComplianceResult:
        """
        Add compliance measures to the analysis.
        
        Args:
            analysis: Legal analysis from summarizer agent
            context: Original intake context
            
        Returns:
            ComplianceResult with added disclaimers and warnings
        """
        try:
            compliance_level = self.determine_compliance_level(context)
            warnings = self.get_case_specific_warnings(context)
            recommendations = self.get_recommendations(context)
            
            # Add compliance information to analysis
            enhanced_analysis = analysis.copy()
            enhanced_analysis["compliance_info"] = {
                "level": compliance_level,
                "timestamp": datetime.now().isoformat(),
                "case_type": context.get("case_type", "general"),
                "urgency": context.get("urgency", "medium")
            }
            
            result = ComplianceResult(
                analysis=enhanced_analysis,
                disclaimers=self.disclaimers,
                warnings=warnings,
                recommendations=recommendations,
                timestamp=datetime.now().isoformat(),
                compliance_level=compliance_level
            )
            
            logger.info(f"Added compliance measures for {compliance_level} level case")
            return result
            
        except Exception as e:
            logger.error(f"Error adding compliance measures: {e}")
            return ComplianceResult(
                analysis=analysis,
                disclaimers=self.disclaimers,
                warnings=["Error in compliance processing"],
                recommendations=["Consult with a qualified attorney"],
                timestamp=datetime.now().isoformat(),
                compliance_level="high"
            )

def guardrails(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for LangGraph - adds compliance measures to analysis.
    
    Args:
        analysis: Legal analysis from summarizer agent
        
    Returns:
        Dictionary with compliance-enhanced analysis
    """
    try:
        agent = ComplianceAgent()
        
        # Extract context from analysis (if available)
        context = analysis.get("context", {})
        
        # Add compliance measures
        result = agent.add_compliance_measures(analysis, context)
        
        return {
            "analysis": result.analysis,
            "disclaimers": result.disclaimers,
            "warnings": result.warnings,
            "recommendations": result.recommendations,
            "compliance_level": result.compliance_level,
            "timestamp": result.timestamp,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error in compliance processing: {e}")
        return {
            "analysis": analysis,
            "disclaimers": ["Error in compliance processing"],
            "warnings": ["Please consult with a qualified attorney"],
            "recommendations": ["Seek immediate legal assistance"],
            "compliance_level": "high",
            "timestamp": datetime.now().isoformat(),
            "success": False
        }

# Example usage and testing
if __name__ == "__main__":
    # Test the compliance agent
    test_analysis = {
        "case_summary": "Analysis of gun possession cases",
        "key_facts": ["Fact 1", "Fact 2"],
        "legal_rules": ["Rule 1", "Rule 2"],
        "practical_advice": ["Advice 1", "Advice 2"]
    }
    
    test_context = {
        "topic": "criminal",
        "case_type": "criminal",
        "urgency": "high",
        "keywords": ["gun", "possession"]
    }
    
    agent = ComplianceAgent()
    result = agent.add_compliance_measures(test_analysis, test_context)
    
    print(f"Compliance Level: {result.compliance_level}")
    print(f"Disclaimers: {len(result.disclaimers)}")
    print(f"Warnings: {len(result.warnings)}")
    print(f"Recommendations: {len(result.recommendations)}")
    print()
    print("Sample Disclaimer:", result.disclaimers[0])
    print("Sample Warning:", result.warnings[0] if result.warnings else "None")
    print("Sample Recommendation:", result.recommendations[0] if result.recommendations else "None")

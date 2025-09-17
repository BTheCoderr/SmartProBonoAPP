"""
Advanced Legal Reasoning Agent
Provides sophisticated legal analysis, precedent analysis, and reasoning chains
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class ReasoningType(Enum):
    """Types of legal reasoning"""
    ANALOGICAL = "analogical"  # Case-by-case reasoning
    DEDUCTIVE = "deductive"    # Rule-based reasoning
    INDUCTIVE = "inductive"    # Pattern-based reasoning
    POLICY = "policy"          # Policy-based reasoning
    PRECEDENT = "precedent"    # Precedent analysis

@dataclass
class LegalRule:
    """Represents a legal rule or principle"""
    rule_id: str
    rule_text: str
    jurisdiction: str
    source: str  # statute, case, regulation, etc.
    authority_level: str  # binding, persuasive, dicta
    applicability: float  # 0.0 to 1.0

@dataclass
class ReasoningStep:
    """Represents a step in legal reasoning"""
    step_number: int
    reasoning_type: ReasoningType
    premise: str
    conclusion: str
    supporting_evidence: List[str]
    confidence: float  # 0.0 to 1.0
    counterarguments: List[str] = None

@dataclass
class LegalAnalysis:
    """Comprehensive legal analysis result"""
    issue: str
    applicable_rules: List[LegalRule]
    reasoning_chain: List[ReasoningStep]
    conclusion: str
    confidence: float
    alternative_conclusions: List[Dict[str, Any]]
    policy_considerations: List[str]
    potential_weaknesses: List[str]

class AdvancedReasoningAgent:
    """Agent for advanced legal reasoning and analysis"""
    
    def __init__(self):
        self.legal_rules_db = self._initialize_legal_rules()
        self.reasoning_patterns = self._initialize_reasoning_patterns()
        
    def _initialize_legal_rules(self) -> Dict[str, List[LegalRule]]:
        """Initialize database of legal rules and principles"""
        return {
            "criminal_law": [
                LegalRule(
                    rule_id="burden_of_proof",
                    rule_text="The prosecution must prove guilt beyond a reasonable doubt",
                    jurisdiction="federal",
                    source="constitutional",
                    authority_level="binding",
                    applicability=1.0
                ),
                LegalRule(
                    rule_id="presumption_of_innocence",
                    rule_text="A defendant is presumed innocent until proven guilty",
                    jurisdiction="federal",
                    source="constitutional",
                    authority_level="binding",
                    applicability=1.0
                ),
                LegalRule(
                    rule_id="exclusionary_rule",
                    rule_text="Evidence obtained in violation of constitutional rights is inadmissible",
                    jurisdiction="federal",
                    source="constitutional",
                    authority_level="binding",
                    applicability=0.9
                )
            ],
            "civil_law": [
                LegalRule(
                    rule_id="preponderance_evidence",
                    rule_text="Civil cases require proof by preponderance of the evidence",
                    jurisdiction="federal",
                    source="common_law",
                    authority_level="binding",
                    applicability=1.0
                ),
                LegalRule(
                    rule_id="statute_of_limitations",
                    rule_text="Legal actions must be filed within specified time limits",
                    jurisdiction="federal",
                    source="statutory",
                    authority_level="binding",
                    applicability=0.95
                )
            ],
            "constitutional_law": [
                LegalRule(
                    rule_id="due_process",
                    rule_text="No person shall be deprived of life, liberty, or property without due process of law",
                    jurisdiction="federal",
                    source="constitutional",
                    authority_level="binding",
                    applicability=1.0
                ),
                LegalRule(
                    rule_id="equal_protection",
                    rule_text="No state shall deny equal protection of the laws",
                    jurisdiction="federal",
                    source="constitutional",
                    authority_level="binding",
                    applicability=1.0
                )
            ]
        }
    
    def _initialize_reasoning_patterns(self) -> Dict[str, List[str]]:
        """Initialize common legal reasoning patterns"""
        return {
            "analogical": [
                "Identify similar cases with similar facts",
                "Extract the legal principle from those cases",
                "Apply the principle to the current case",
                "Distinguish any material differences"
            ],
            "deductive": [
                "Identify the applicable legal rule",
                "Determine if the facts satisfy the rule's elements",
                "Apply the rule to reach a conclusion",
                "Consider exceptions or defenses"
            ],
            "inductive": [
                "Examine multiple similar cases",
                "Identify common patterns or principles",
                "Formulate a general rule",
                "Apply the rule to the current case"
            ],
            "policy": [
                "Identify the underlying policy goals",
                "Analyze how different outcomes serve those goals",
                "Consider practical consequences",
                "Balance competing policy interests"
            ]
        }
    
    def analyze_legal_issue(self, issue: str, facts: List[str], jurisdiction: str = "federal") -> LegalAnalysis:
        """Perform comprehensive legal analysis of an issue"""
        try:
            # Identify applicable legal rules
            applicable_rules = self._identify_applicable_rules(issue, facts, jurisdiction)
            
            # Generate reasoning chain
            reasoning_chain = self._generate_reasoning_chain(issue, facts, applicable_rules)
            
            # Reach conclusion
            conclusion, confidence = self._reach_conclusion(reasoning_chain, applicable_rules)
            
            # Identify alternative conclusions
            alternatives = self._identify_alternatives(issue, facts, applicable_rules)
            
            # Consider policy implications
            policy_considerations = self._analyze_policy_implications(issue, conclusion)
            
            # Identify potential weaknesses
            weaknesses = self._identify_weaknesses(reasoning_chain, applicable_rules)
            
            return LegalAnalysis(
                issue=issue,
                applicable_rules=applicable_rules,
                reasoning_chain=reasoning_chain,
                conclusion=conclusion,
                confidence=confidence,
                alternative_conclusions=alternatives,
                policy_considerations=policy_considerations,
                potential_weaknesses=weaknesses
            )
            
        except Exception as e:
            logger.error(f"Error in legal analysis: {e}")
            return self._create_fallback_analysis(issue)
    
    def _identify_applicable_rules(self, issue: str, facts: List[str], jurisdiction: str) -> List[LegalRule]:
        """Identify legal rules applicable to the issue"""
        applicable_rules = []
        
        # Simple keyword matching - in production, use NLP
        issue_keywords = set(issue.lower().split())
        
        for category, rules in self.legal_rules_db.items():
            for rule in rules:
                # Check if rule is applicable based on keywords and jurisdiction
                rule_keywords = set(rule.rule_text.lower().split())
                overlap = len(issue_keywords.intersection(rule_keywords))
                
                if overlap > 0 and (rule.jurisdiction == jurisdiction or rule.jurisdiction == "federal"):
                    # Adjust applicability based on keyword overlap
                    rule.applicability = min(1.0, overlap / len(issue_keywords))
                    applicable_rules.append(rule)
        
        # Sort by applicability
        applicable_rules.sort(key=lambda x: x.applicability, reverse=True)
        return applicable_rules[:5]  # Return top 5 most applicable rules
    
    def _generate_reasoning_chain(self, issue: str, facts: List[str], rules: List[LegalRule]) -> List[ReasoningStep]:
        """Generate a chain of legal reasoning steps"""
        reasoning_steps = []
        
        # Step 1: Identify the legal issue
        reasoning_steps.append(ReasoningStep(
            step_number=1,
            reasoning_type=ReasoningType.DEDUCTIVE,
            premise=f"The legal issue is: {issue}",
            conclusion="This requires analysis under applicable legal rules",
            supporting_evidence=facts,
            confidence=0.9
        ))
        
        # Step 2: Apply applicable rules
        for i, rule in enumerate(rules[:3]):  # Apply top 3 rules
            reasoning_steps.append(ReasoningStep(
                step_number=2 + i,
                reasoning_type=ReasoningType.DEDUCTIVE,
                premise=f"Applicable rule: {rule.rule_text}",
                conclusion=f"Under this rule, the facts suggest [analysis based on rule]",
                supporting_evidence=[rule.source, rule.jurisdiction],
                confidence=rule.applicability
            ))
        
        # Step 3: Analogical reasoning
        reasoning_steps.append(ReasoningStep(
            step_number=len(reasoning_steps) + 1,
            reasoning_type=ReasoningType.ANALOGICAL,
            premise="Similar cases with analogous facts have been decided",
            conclusion="The pattern from similar cases suggests [conclusion]",
            supporting_evidence=["Case law precedent", "Factual similarities"],
            confidence=0.7
        ))
        
        # Step 4: Policy considerations
        reasoning_steps.append(ReasoningStep(
            step_number=len(reasoning_steps) + 1,
            reasoning_type=ReasoningType.POLICY,
            premise="Policy considerations include fairness, efficiency, and justice",
            conclusion="The policy implications support [conclusion]",
            supporting_evidence=["Public policy", "Legal principles"],
            confidence=0.6
        ))
        
        return reasoning_steps
    
    def _reach_conclusion(self, reasoning_chain: List[ReasoningStep], rules: List[LegalRule]) -> Tuple[str, float]:
        """Reach a conclusion based on reasoning chain and rules"""
        if not reasoning_chain:
            return "Insufficient information for analysis", 0.0
        
        # Calculate weighted confidence based on reasoning steps
        total_confidence = sum(step.confidence for step in reasoning_chain)
        average_confidence = total_confidence / len(reasoning_chain)
        
        # Generate conclusion based on most confident reasoning
        strongest_step = max(reasoning_steps, key=lambda x: x.confidence)
        
        if strongest_step.reasoning_type == ReasoningType.DEDUCTIVE:
            conclusion = f"Based on applicable legal rules, {strongest_step.conclusion}"
        elif strongest_step.reasoning_type == ReasoningType.ANALOGICAL:
            conclusion = f"Based on similar cases, {strongest_step.conclusion}"
        elif strongest_step.reasoning_type == ReasoningType.POLICY:
            conclusion = f"From a policy perspective, {strongest_step.conclusion}"
        else:
            conclusion = f"Based on the analysis, {strongest_step.conclusion}"
        
        return conclusion, min(0.95, average_confidence)
    
    def _identify_alternatives(self, issue: str, facts: List[str], rules: List[LegalRule]) -> List[Dict[str, Any]]:
        """Identify alternative conclusions or interpretations"""
        alternatives = []
        
        # Alternative based on different rule interpretation
        if len(rules) > 1:
            alternatives.append({
                "type": "alternative_rule_interpretation",
                "description": f"Alternative interpretation under {rules[1].rule_text}",
                "confidence": rules[1].applicability,
                "reasoning": "Different legal rule may apply"
            })
        
        # Alternative based on factual differences
        alternatives.append({
            "type": "factual_distinction",
            "description": "Different outcome if facts were slightly different",
            "confidence": 0.6,
            "reasoning": "Small factual changes could lead to different result"
        })
        
        # Alternative based on policy considerations
        alternatives.append({
            "type": "policy_alternative",
            "description": "Different outcome based on policy considerations",
            "confidence": 0.5,
            "reasoning": "Policy arguments could support opposite conclusion"
        })
        
        return alternatives
    
    def _analyze_policy_implications(self, issue: str, conclusion: str) -> List[str]:
        """Analyze policy implications of the conclusion"""
        policy_considerations = [
            "Fairness and justice considerations",
            "Efficiency of legal system",
            "Deterrent effects of the rule",
            "Impact on individual rights",
            "Consistency with legal precedent",
            "Practical enforcement considerations"
        ]
        return policy_considerations
    
    def _identify_weaknesses(self, reasoning_chain: List[ReasoningStep], rules: List[LegalRule]) -> List[str]:
        """Identify potential weaknesses in the analysis"""
        weaknesses = []
        
        # Check for low confidence steps
        low_confidence_steps = [step for step in reasoning_chain if step.confidence < 0.6]
        if low_confidence_steps:
            weaknesses.append("Some reasoning steps have low confidence levels")
        
        # Check for limited rule coverage
        if len(rules) < 2:
            weaknesses.append("Limited number of applicable legal rules identified")
        
        # Check for missing reasoning types
        used_types = {step.reasoning_type for step in reasoning_chain}
        missing_types = set(ReasoningType) - used_types
        if missing_types:
            weaknesses.append(f"Analysis could benefit from {', '.join([t.value for t in missing_types])} reasoning")
        
        return weaknesses
    
    def _create_fallback_analysis(self, issue: str) -> LegalAnalysis:
        """Create a fallback analysis when main analysis fails"""
        return LegalAnalysis(
            issue=issue,
            applicable_rules=[],
            reasoning_chain=[],
            conclusion="Unable to perform comprehensive legal analysis. Consult with a qualified attorney.",
            confidence=0.0,
            alternative_conclusions=[],
            policy_considerations=[],
            potential_weaknesses=["Analysis failed due to technical error"]
        )

# Global instance
advanced_reasoning_agent = AdvancedReasoningAgent()

def analyze_legal_issue(issue: str, facts: List[str], jurisdiction: str = "federal") -> LegalAnalysis:
    """Analyze a legal issue with advanced reasoning"""
    return advanced_reasoning_agent.analyze_legal_issue(issue, facts, jurisdiction)

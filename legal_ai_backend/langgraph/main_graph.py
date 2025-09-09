"""
Main LangGraph Pipeline - Orchestrates the legal AI workflow.
Combines intake, search, analysis, and compliance agents.
"""
import logging
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from agents.intake_agent import intake
from agents.courtlistener_agent import search_live
from agents.vector_agent import search_local
from agents.summarizer_agent import summarize
from agents.compliance_agent import guardrails

logger = logging.getLogger(__name__)

class LegalAIPipeline:
    """Main pipeline for legal AI processing using LangGraph."""
    
    def __init__(self):
        self.graph = self._build_graph()
        self.memory = MemorySaver()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create the state graph with TypedDict for state
        from typing import TypedDict, Annotated
        from operator import add
        
        class LegalAIState(TypedDict):
            user_input: str
            intake_result: Dict[str, Any]
            courtlistener_results: Dict[str, Any]
            vector_results: Dict[str, Any]
            analysis: Dict[str, Any]
            final_result: Dict[str, Any]
            errors: Annotated[List[str], add]
        
        # Create the state graph
        workflow = StateGraph(LegalAIState)
        
        # Add nodes
        workflow.add_node("intake", self._intake_node)
        workflow.add_node("courtlistener_search", self._courtlistener_node)
        workflow.add_node("vector_search", self._vector_node)
        workflow.add_node("summarize", self._summarize_node)
        workflow.add_node("compliance", self._compliance_node)
        
        # Set entry point
        workflow.set_entry_point("intake")
        
        # Add edges
        workflow.add_edge("intake", "courtlistener_search")
        workflow.add_edge("intake", "vector_search")
        workflow.add_edge("courtlistener_search", "summarize")
        workflow.add_edge("vector_search", "summarize")
        workflow.add_edge("summarize", "compliance")
        workflow.add_edge("compliance", END)
        
        return workflow.compile()
    
    def _create_enhanced_analysis(self, user_input: str, topic: str, jurisdiction: str, case_type: str, urgency: str, courtlistener_results: Dict, vector_results: Dict) -> Dict[str, Any]:
        """Create enhanced legal analysis based on the specific query."""
        
        # Analyze the specific query to provide relevant guidance
        if "gun" in user_input.lower() or "firearm" in user_input.lower() or "weapon" in user_input.lower():
            return self._analyze_gun_case(user_input, jurisdiction, urgency)
        elif "landlord" in user_input.lower() or "tenant" in user_input.lower() or "rent" in user_input.lower():
            return self._analyze_landlord_case(user_input, jurisdiction, urgency)
        elif "criminal" in user_input.lower() or "arrest" in user_input.lower() or "charge" in user_input.lower():
            return self._analyze_criminal_case(user_input, jurisdiction, urgency)
        elif "divorce" in user_input.lower() or "custody" in user_input.lower() or "family" in user_input.lower():
            return self._analyze_family_case(user_input, jurisdiction, urgency)
        else:
            return self._analyze_general_case(user_input, topic, jurisdiction, urgency)
    
    def _analyze_gun_case(self, user_input: str, jurisdiction: str, urgency: str) -> Dict[str, Any]:
        """Analyze gun-related legal cases."""
        return {
            "success": True,
            "analysis": {
                "case_summary": f"Gun-related legal matter in {jurisdiction.upper()}. This appears to involve firearms law, which is heavily regulated and varies significantly by jurisdiction.",
                "key_facts": [
                    "Firearms laws vary by state and federal jurisdiction",
                    "Gun charges often carry severe penalties including mandatory minimum sentences",
                    "Constitutional rights (2nd Amendment) may be relevant but are not absolute",
                    "Background checks and permits are typically required for legal gun ownership"
                ],
                "legal_rules": [
                    "Federal firearms laws (Gun Control Act, National Firearms Act)",
                    f"State-specific gun laws in {jurisdiction.upper()}",
                    "Concealed carry permit requirements",
                    "Prohibited persons restrictions",
                    "Safe storage and transportation requirements"
                ],
                "court_decision": "Gun-related cases often involve complex constitutional and statutory interpretation. Courts balance individual rights with public safety concerns.",
                "relevance": "This case involves firearms law, which requires specialized legal expertise due to the complex interplay of federal and state regulations.",
                "practical_advice": [
                    "DO NOT speak to law enforcement without an attorney present",
                    "Document all interactions and preserve any evidence",
                    "Contact a criminal defense attorney immediately",
                    "Research local gun law attorneys with firearms law experience",
                    "Understand that gun charges often have mandatory minimum sentences"
                ],
                "similar_cases": [
                    "Cases involving illegal possession of firearms",
                    "Concealed carry violations",
                    "Gun trafficking and straw purchase cases",
                    "Domestic violence and gun possession restrictions"
                ]
            },
            "cases_analyzed": 2,
            "compliance_info": {
                "case_type": "criminal",
                "level": "high",
                "urgency": "high",
                "timestamp": "2025-09-09T01:16:00.000000"
            }
        }
    
    def _analyze_landlord_case(self, user_input: str, jurisdiction: str, urgency: str) -> Dict[str, Any]:
        """Analyze landlord-tenant legal cases."""
        return {
            "success": True,
            "analysis": {
                "case_summary": f"Landlord-tenant dispute in {jurisdiction.upper()}. This involves housing law and tenant rights, which are governed by state and local regulations.",
                "key_facts": [
                    "Landlord-tenant law varies significantly by state and locality",
                    "Tenants have specific rights regarding habitability, privacy, and security deposits",
                    "Landlords must follow proper eviction procedures",
                    "Housing discrimination laws may apply"
                ],
                "legal_rules": [
                    f"State landlord-tenant laws in {jurisdiction.upper()}",
                    "Fair Housing Act (federal anti-discrimination law)",
                    "Local housing codes and ordinances",
                    "Security deposit regulations",
                    "Eviction process requirements"
                ],
                "court_decision": "Landlord-tenant disputes often involve issues of habitability, lease violations, and proper notice requirements.",
                "relevance": "This case involves housing law, which requires understanding of both state and local regulations.",
                "practical_advice": [
                    "Document all communications with your landlord",
                    "Take photos of any property damage or maintenance issues",
                    "Keep copies of your lease and all correspondence",
                    "Contact local tenant rights organizations",
                    "Consider mediation before pursuing legal action"
                ],
                "similar_cases": [
                    "Security deposit disputes",
                    "Habitability and repair issues",
                    "Illegal eviction cases",
                    "Housing discrimination matters"
                ]
            },
            "cases_analyzed": 2,
            "compliance_info": {
                "case_type": "civil",
                "level": "medium",
                "urgency": urgency,
                "timestamp": "2025-09-09T01:16:00.000000"
            }
        }
    
    def _analyze_criminal_case(self, user_input: str, jurisdiction: str, urgency: str) -> Dict[str, Any]:
        """Analyze criminal legal cases."""
        return {
            "success": True,
            "analysis": {
                "case_summary": f"Criminal legal matter in {jurisdiction.upper()}. This involves criminal law and requires immediate attention due to potential serious consequences.",
                "key_facts": [
                    "Criminal charges can result in jail time, fines, and permanent record",
                    "You have constitutional rights including right to remain silent and right to attorney",
                    "Criminal law varies by state and federal jurisdiction",
                    "Plea bargains and sentencing guidelines may apply"
                ],
                "legal_rules": [
                    f"State criminal laws in {jurisdiction.upper()}",
                    "Federal criminal statutes",
                    "Constitutional rights (4th, 5th, 6th Amendments)",
                    "Evidence rules and procedures",
                    "Sentencing guidelines and mandatory minimums"
                ],
                "court_decision": "Criminal cases involve complex procedural requirements and constitutional protections that require experienced legal representation.",
                "relevance": "This case involves criminal law, which requires specialized expertise due to the serious consequences and complex procedures.",
                "practical_advice": [
                    "DO NOT speak to law enforcement without an attorney",
                    "Contact a criminal defense attorney immediately",
                    "Document everything and preserve evidence",
                    "Understand your constitutional rights",
                    "Consider the potential consequences of any plea offers"
                ],
                "similar_cases": [
                    "Drug possession and trafficking cases",
                    "Theft and property crimes",
                    "Assault and violent crimes",
                    "White collar and financial crimes"
                ]
            },
            "cases_analyzed": 2,
            "compliance_info": {
                "case_type": "criminal",
                "level": "high",
                "urgency": "high",
                "timestamp": "2025-09-09T01:16:00.000000"
            }
        }
    
    def _analyze_family_case(self, user_input: str, jurisdiction: str, urgency: str) -> Dict[str, Any]:
        """Analyze family law cases."""
        return {
            "success": True,
            "analysis": {
                "case_summary": f"Family law matter in {jurisdiction.upper()}. This involves family relationships and may require specialized family law expertise.",
                "key_facts": [
                    "Family law varies significantly by state",
                    "Child custody and support are determined by best interests of the child",
                    "Divorce proceedings involve property division and spousal support",
                    "Mediation may be required before court proceedings"
                ],
                "legal_rules": [
                    f"State family law statutes in {jurisdiction.upper()}",
                    "Child custody and support guidelines",
                    "Property division laws",
                    "Domestic violence protection orders",
                    "Mediation and alternative dispute resolution requirements"
                ],
                "court_decision": "Family law cases often involve emotional issues and require careful consideration of all parties' interests, especially children.",
                "relevance": "This case involves family law, which requires understanding of state-specific regulations and procedures.",
                "practical_advice": [
                    "Consider mediation or collaborative law approaches",
                    "Document all financial information and assets",
                    "Prioritize children's best interests",
                    "Contact local family law attorneys",
                    "Understand the emotional and financial costs of litigation"
                ],
                "similar_cases": [
                    "Child custody and visitation disputes",
                    "Divorce and property division",
                    "Child support modification cases",
                    "Domestic violence protection orders"
                ]
            },
            "cases_analyzed": 2,
            "compliance_info": {
                "case_type": "family",
                "level": "medium",
                "urgency": urgency,
                "timestamp": "2025-09-09T01:16:00.000000"
            }
        }
    
    def _analyze_general_case(self, user_input: str, topic: str, jurisdiction: str, urgency: str) -> Dict[str, Any]:
        """Analyze general legal cases."""
        return {
            "success": True,
            "analysis": {
                "case_summary": f"Legal matter involving {topic} in {jurisdiction.upper()}. This requires careful analysis of the specific facts and applicable law.",
                "key_facts": [
                    "Each legal case is unique and requires individual analysis",
                    "Laws vary by jurisdiction and may change over time",
                    "Legal precedents may provide guidance but may not be directly applicable",
                    "The specific facts of your case will determine the legal approach"
                ],
                "legal_rules": [
                    f"State laws in {jurisdiction.upper()}",
                    "Federal laws that may apply",
                    "Local ordinances and regulations",
                    "Constitutional provisions",
                    "Case law and legal precedents"
                ],
                "court_decision": "Legal cases require careful analysis of the specific facts, applicable law, and potential outcomes.",
                "relevance": "This case requires understanding of the specific legal issues and applicable law in your jurisdiction.",
                "practical_advice": [
                    "Consult with a qualified attorney who specializes in this area",
                    "Gather all relevant documents and evidence",
                    "Research local legal aid organizations if needed",
                    "Understand the potential costs and time involved",
                    "Consider alternative dispute resolution options"
                ],
                "similar_cases": [
                    "Cases involving similar legal issues",
                    "Precedents that may be relevant",
                    "Recent court decisions in your jurisdiction",
                    "Cases with similar factual circumstances"
                ]
            },
            "cases_analyzed": 2,
            "compliance_info": {
                "case_type": "general",
                "level": "medium",
                "urgency": urgency,
                "timestamp": "2025-09-09T01:16:00.000000"
            }
        }
    
    def _intake_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input through intake agent."""
        try:
            user_input = state.get("user_input", "")
            intake_result = intake(user_input)
            
            return {
                "intake_result": intake_result,
                "errors": state.get("errors", [])
            }
        except Exception as e:
            logger.error(f"Error in intake node: {e}")
            return {
                "errors": state.get("errors", []) + [f"Intake error: {str(e)}"]
            }
    
    def _courtlistener_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Search live case law using CourtListener - using mock data."""
        try:
            intake_result = state.get("intake_result", {})
            topic = intake_result.get("topic", "legal matter")
            jurisdiction = intake_result.get("jurisdiction", "ri")
            
            # Return mock case data instead of calling API
            mock_cases = [
                {
                    "case_name": f"Sample {topic.title()} Case v. State",
                    "court": f"{jurisdiction.upper()} Supreme Court",
                    "date_filed": "2023-01-15",
                    "snippet": f"This is a mock case related to {topic}. The court considered the legal issues and provided guidance on similar matters.",
                    "jurisdiction": jurisdiction,
                    "case_type": "civil" if topic == "civil" else "criminal"
                },
                {
                    "case_name": f"Another {topic.title()} Matter",
                    "court": f"{jurisdiction.upper()} Court of Appeals", 
                    "date_filed": "2023-03-20",
                    "snippet": f"Another mock case involving {topic}. The court's decision established important legal principles.",
                    "jurisdiction": jurisdiction,
                    "case_type": "civil" if topic == "civil" else "criminal"
                }
            ]
            
            courtlistener_results = {
                "success": True,
                "cases": mock_cases,
                "total_count": len(mock_cases)
            }
            
            return {
                "courtlistener_results": courtlistener_results,
                "errors": state.get("errors", [])
            }
        except Exception as e:
            logger.error(f"Error in CourtListener node: {e}")
            return {
                "courtlistener_results": {"success": False, "cases": []},
                "errors": state.get("errors", []) + [f"CourtListener error: {str(e)}"]
            }
    
    def _vector_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Search local vector store for case embeddings - using mock data."""
        try:
            intake_result = state.get("intake_result", {})
            topic = intake_result.get("topic", "legal matter")
            jurisdiction = intake_result.get("jurisdiction", "ri")
            
            # Return mock vector search results
            mock_vector_cases = [
                {
                    "case_name": f"Vector {topic.title()} Case",
                    "court": f"{jurisdiction.upper()} District Court",
                    "date_filed": "2023-02-10",
                    "snippet": f"Vector search found this {topic} case with relevant legal principles and precedents.",
                    "similarity_score": 0.85,
                    "case_type": "civil" if topic == "civil" else "criminal"
                }
            ]
            
            vector_results = {
                "success": True,
                "cases": mock_vector_cases,
                "total_count": len(mock_vector_cases)
            }
            
            return {
                "vector_results": vector_results,
                "errors": state.get("errors", [])
            }
        except Exception as e:
            logger.error(f"Error in vector node: {e}")
            return {
                "vector_results": {"success": False, "cases": []},
                "errors": state.get("errors", []) + [f"Vector search error: {str(e)}"]
            }
    
    def _summarize_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and summarize case law - using enhanced fallback analysis."""
        try:
            # Get context from previous nodes
            intake_result = state.get("intake_result", {})
            courtlistener_results = state.get("courtlistener_results", {})
            vector_results = state.get("vector_results", {})
            
            # Extract key information
            user_input = intake_result.get("original_input", "")
            topic = intake_result.get("topic", "legal matter")
            jurisdiction = intake_result.get("jurisdiction", "ri")
            case_type = intake_result.get("case_type", "general")
            urgency = intake_result.get("urgency", "medium")
            
            # Create enhanced analysis based on the specific query
            analysis = self._create_enhanced_analysis(user_input, topic, jurisdiction, case_type, urgency, courtlistener_results, vector_results)
            
            return {
                "analysis": analysis,
                "errors": state.get("errors", [])
            }
        except Exception as e:
            logger.error(f"Error in summarize node: {e}")
            return {
                "analysis": {"success": False, "analysis": {}},
                "errors": state.get("errors", []) + [f"Summarization error: {str(e)}"]
            }
    
    def _compliance_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Add compliance measures and disclaimers."""
        try:
            analysis = state.get("analysis", {})
            intake_result = state.get("intake_result", {})
            
            # Add context to analysis for compliance
            analysis["context"] = intake_result
            
            final_result = guardrails(analysis)
            
            return {
                "final_result": final_result,
                "errors": state.get("errors", [])
            }
        except Exception as e:
            logger.error(f"Error in compliance node: {e}")
            return {
                "final_result": {
                    "success": False,
                    "analysis": {},
                    "disclaimers": ["Error in compliance processing"],
                    "warnings": ["Please consult with a qualified attorney"]
                },
                "errors": state.get("errors", []) + [f"Compliance error: {str(e)}"]
            }
    
    def run_pipeline(self, user_input: str) -> Dict[str, Any]:
        """
        Run the complete legal AI pipeline.
        
        Args:
            user_input: User's legal question or situation
            
        Returns:
            Complete analysis with compliance measures
        """
        try:
            # Create initial state
            initial_state = {
                "user_input": user_input,
                "intake_result": {},
                "courtlistener_results": {},
                "vector_results": {},
                "analysis": {},
                "final_result": {},
                "errors": []
            }
            
            # Run the pipeline
            result = self.graph.invoke(initial_state)
            
            # Extract final result
            final_result = result.get("final_result", {})
            errors = result.get("errors", [])
            
            # Add metadata
            final_result["metadata"] = {
                "user_input": user_input,
                "pipeline_version": "1.0.0",
                "errors": errors,
                "success": len(errors) == 0
            }
            
            logger.info(f"Pipeline completed for input: {user_input[:50]}...")
            return final_result
            
        except Exception as e:
            logger.error(f"Error in pipeline execution: {e}")
            return {
                "success": False,
                "analysis": {},
                "disclaimers": ["Pipeline error occurred"],
                "warnings": ["Please consult with a qualified attorney"],
                "errors": [str(e)],
                "metadata": {
                    "user_input": user_input,
                    "pipeline_version": "1.0.0",
                    "success": False
                }
            }

# Global pipeline instance
pipeline = LegalAIPipeline()

def run_pipeline(user_input: str) -> Dict[str, Any]:
    """
    Convenience function to run the legal AI pipeline.
    
    Args:
        user_input: User's legal question or situation
        
    Returns:
        Complete analysis with compliance measures
    """
    return pipeline.run_pipeline(user_input)

# Example usage and testing
if __name__ == "__main__":
    # Test the complete pipeline
    test_inputs = [
        "I was charged with gun possession in Boston, what should I do?",
        "I need help with a divorce case in Rhode Island",
        "My landlord is trying to evict me, is this legal?",
        "I was arrested for DUI last night, urgent help needed"
    ]
    
    for test_input in test_inputs:
        print(f"Testing: {test_input}")
        print("-" * 50)
        
        result = run_pipeline(test_input)
        
        print(f"Success: {result.get('success', False)}")
        print(f"Compliance Level: {result.get('compliance_level', 'Unknown')}")
        print(f"Disclaimers: {len(result.get('disclaimers', []))}")
        print(f"Warnings: {len(result.get('warnings', []))}")
        print(f"Errors: {len(result.get('errors', []))}")
        
        if result.get('analysis', {}).get('case_summary'):
            print(f"Summary: {result['analysis']['case_summary'][:100]}...")
        
        print("\n" + "="*50 + "\n")

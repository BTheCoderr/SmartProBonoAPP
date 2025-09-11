"""
AI Case Analysis Service for SmartProBono
Provides AI-powered case analysis, recommendations, and predictive analytics.
"""
import openai
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from backend.database import db
from backend.models import Case, CourtDate, Document, User
import logging
import json
import re

logger = logging.getLogger(__name__)

class AICaseAnalysisService:
    """Service for AI-powered case analysis and recommendations."""
    
    def __init__(self):
        self.openai_api_key = openai.api_key
        self.model = "gpt-4"
        self.max_tokens = 2000
    
    def analyze_case(self, case_id: int) -> Dict[str, Any]:
        """Perform comprehensive AI analysis of a case."""
        try:
            case = Case.query.get(case_id)
            if not case:
                return {'success': False, 'error': 'Case not found'}
            
            # Gather case data
            case_data = self._gather_case_data(case)
            
            # Perform AI analysis
            analysis = self._perform_ai_analysis(case_data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(case_data, analysis)
            
            # Calculate risk assessment
            risk_assessment = self._assess_case_risk(case_data, analysis)
            
            # Predict case timeline
            timeline_prediction = self._predict_case_timeline(case_data, analysis)
            
            # Store analysis results
            self._store_analysis_results(case_id, analysis, recommendations, risk_assessment)
            
            return {
                'success': True,
                'analysis': analysis,
                'recommendations': recommendations,
                'risk_assessment': risk_assessment,
                'timeline_prediction': timeline_prediction
            }
            
        except Exception as e:
            logger.error(f"Error analyzing case: {e}")
            return {'success': False, 'error': str(e)}
    
    def _gather_case_data(self, case: Case) -> Dict[str, Any]:
        """Gather all relevant data for case analysis."""
        try:
            # Get case documents
            documents = Document.query.filter_by(case_id=case.id).all()
            
            # Get court dates
            court_dates = CourtDate.query.filter_by(case_id=case.id).all()
            
            # Get client information
            client = User.query.get(case.client_id)
            
            # Get attorney information
            attorney = User.query.get(case.attorney_id) if case.attorney_id else None
            
            return {
                'case': case.to_dict(),
                'client': client.to_dict() if client else None,
                'attorney': attorney.to_dict() if attorney else None,
                'documents': [doc.to_dict() for doc in documents],
                'court_dates': [cd.to_dict() for cd in court_dates],
                'analysis_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error gathering case data: {e}")
            return {}
    
    def _perform_ai_analysis(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform AI analysis on case data."""
        try:
            if not self.openai_api_key:
                return self._fallback_analysis(case_data)
            
            # Prepare prompt for AI analysis
            prompt = self._create_analysis_prompt(case_data)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert legal analyst specializing in case evaluation and strategy. Provide detailed, professional analysis of legal cases."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.3
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            analysis = self._parse_ai_response(ai_response)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error performing AI analysis: {e}")
            return self._fallback_analysis(case_data)
    
    def _create_analysis_prompt(self, case_data: Dict[str, Any]) -> str:
        """Create prompt for AI case analysis."""
        case = case_data['case']
        client = case_data['client']
        documents = case_data['documents']
        court_dates = case_data['court_dates']
        
        prompt = f"""
        Analyze the following legal case and provide comprehensive insights:
        
        CASE INFORMATION:
        - Title: {case['title']}
        - Type: {case['case_type']}
        - Status: {case['status']}
        - Priority: {case['priority']}
        - Practice Area: {case['practice_area']}
        - Description: {case['description']}
        - Created: {case['created_at']}
        - Due Date: {case['due_date']}
        
        CLIENT INFORMATION:
        - Name: {client['first_name']} {client['last_name']} if client else 'N/A'
        - Email: {client['email'] if client else 'N/A'}
        
        DOCUMENTS ({len(documents)} total):
        {self._format_documents_for_analysis(documents)}
        
        COURT DATES ({len(court_dates)} total):
        {self._format_court_dates_for_analysis(court_dates)}
        
        Please provide analysis in the following format:
        
        STRENGTHS:
        - [List key strengths of the case]
        
        WEAKNESSES:
        - [List potential weaknesses or challenges]
        
        LEGAL ISSUES:
        - [Identify key legal issues and complexities]
        
        EVIDENCE ASSESSMENT:
        - [Evaluate available evidence and documentation]
        
        STRATEGY RECOMMENDATIONS:
        - [Suggest legal strategies and approaches]
        
        TIMELINE CONSIDERATIONS:
        - [Analyze timeline and urgency factors]
        
        RISK FACTORS:
        - [Identify potential risks and mitigation strategies]
        """
        
        return prompt
    
    def _format_documents_for_analysis(self, documents: List[Dict]) -> str:
        """Format documents for AI analysis."""
        if not documents:
            return "No documents available"
        
        formatted = []
        for doc in documents[:10]:  # Limit to first 10 documents
            formatted.append(f"- {doc['title']} ({doc['document_type']})")
        
        return "\n".join(formatted)
    
    def _format_court_dates_for_analysis(self, court_dates: List[Dict]) -> str:
        """Format court dates for AI analysis."""
        if not court_dates:
            return "No court dates scheduled"
        
        formatted = []
        for cd in court_dates:
            formatted.append(f"- {cd['title']} on {cd['scheduled_date']} at {cd['court_location']}")
        
        return "\n".join(formatted)
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured format."""
        try:
            analysis = {
                'strengths': [],
                'weaknesses': [],
                'legal_issues': [],
                'evidence_assessment': [],
                'strategy_recommendations': [],
                'timeline_considerations': [],
                'risk_factors': []
            }
            
            # Parse each section
            sections = response.split('\n\n')
            current_section = None
            
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                
                # Check for section headers
                if section.startswith('STRENGTHS:'):
                    current_section = 'strengths'
                elif section.startswith('WEAKNESSES:'):
                    current_section = 'weaknesses'
                elif section.startswith('LEGAL ISSUES:'):
                    current_section = 'legal_issues'
                elif section.startswith('EVIDENCE ASSESSMENT:'):
                    current_section = 'evidence_assessment'
                elif section.startswith('STRATEGY RECOMMENDATIONS:'):
                    current_section = 'strategy_recommendations'
                elif section.startswith('TIMELINE CONSIDERATIONS:'):
                    current_section = 'timeline_considerations'
                elif section.startswith('RISK FACTORS:'):
                    current_section = 'risk_factors'
                elif current_section and section.startswith('- '):
                    # Add bullet point to current section
                    analysis[current_section].append(section[2:])
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return self._fallback_analysis({})
    
    def _fallback_analysis(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when AI is not available."""
        case = case_data.get('case', {})
        
        return {
            'strengths': [
                f"Case type: {case.get('case_type', 'Unknown')}",
                f"Priority level: {case.get('priority', 'Medium')}",
                f"Practice area: {case.get('practice_area', 'General')}"
            ],
            'weaknesses': [
                "Limited case information available",
                "No AI analysis performed"
            ],
            'legal_issues': [
                f"Case type: {case.get('case_type', 'Unknown')}",
                f"Status: {case.get('status', 'Unknown')}"
            ],
            'evidence_assessment': [
                f"Documents available: {len(case_data.get('documents', []))}",
                "Manual review required"
            ],
            'strategy_recommendations': [
                "Consult with legal expert",
                "Review all available documentation",
                "Prepare for court proceedings"
            ],
            'timeline_considerations': [
                f"Case created: {case.get('created_at', 'Unknown')}",
                f"Due date: {case.get('due_date', 'Not set')}"
            ],
            'risk_factors': [
                "Limited information available",
                "Manual analysis required"
            ]
        }
    
    def _generate_recommendations(self, case_data: Dict[str, Any], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # Document recommendations
        if len(case_data.get('documents', [])) < 3:
            recommendations.append({
                'type': 'document',
                'priority': 'high',
                'title': 'Gather Additional Documentation',
                'description': 'Collect more supporting documents to strengthen the case',
                'action': 'Request additional documents from client'
            })
        
        # Court date recommendations
        court_dates = case_data.get('court_dates', [])
        upcoming_dates = [cd for cd in court_dates if cd['scheduled_date'] and 
                         datetime.fromisoformat(cd['scheduled_date'].replace('Z', '+00:00')) > datetime.utcnow()]
        
        if not upcoming_dates:
            recommendations.append({
                'type': 'court_date',
                'priority': 'medium',
                'title': 'Schedule Court Date',
                'description': 'No upcoming court dates scheduled',
                'action': 'Schedule initial court appearance'
            })
        
        # Evidence recommendations
        if analysis.get('evidence_assessment'):
            recommendations.append({
                'type': 'evidence',
                'priority': 'high',
                'title': 'Review Evidence',
                'description': 'Thoroughly review all available evidence',
                'action': 'Conduct evidence review session'
            })
        
        # Strategy recommendations
        if analysis.get('strategy_recommendations'):
            recommendations.append({
                'type': 'strategy',
                'priority': 'high',
                'title': 'Develop Legal Strategy',
                'description': 'Create comprehensive legal strategy based on case analysis',
                'action': 'Schedule strategy meeting'
            })
        
        return recommendations
    
    def _assess_case_risk(self, case_data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess case risk level and factors."""
        risk_factors = []
        risk_score = 0
        
        # Analyze case age
        case = case_data.get('case', {})
        if case.get('created_at'):
            created_date = datetime.fromisoformat(case['created_at'].replace('Z', '+00:00'))
            days_old = (datetime.utcnow() - created_date).days
            
            if days_old > 365:
                risk_factors.append('Case is over 1 year old')
                risk_score += 2
            elif days_old > 180:
                risk_factors.append('Case is over 6 months old')
                risk_score += 1
        
        # Analyze document count
        doc_count = len(case_data.get('documents', []))
        if doc_count < 2:
            risk_factors.append('Limited documentation available')
            risk_score += 2
        elif doc_count < 5:
            risk_factors.append('Moderate documentation available')
            risk_score += 1
        
        # Analyze court dates
        court_dates = case_data.get('court_dates', [])
        if not court_dates:
            risk_factors.append('No court dates scheduled')
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 5:
            risk_level = 'high'
        elif risk_score >= 3:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'mitigation_strategies': self._get_mitigation_strategies(risk_factors)
        }
    
    def _get_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """Get mitigation strategies for identified risk factors."""
        strategies = []
        
        for factor in risk_factors:
            if 'documentation' in factor.lower():
                strategies.append('Request additional documentation from client')
            elif 'court date' in factor.lower():
                strategies.append('Schedule court appearance immediately')
            elif 'old' in factor.lower():
                strategies.append('Review case for statute of limitations')
            else:
                strategies.append('Address identified risk factor')
        
        return strategies
    
    def _predict_case_timeline(self, case_data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Predict case timeline and milestones."""
        case = case_data.get('case', {})
        case_type = case.get('case_type', 'general')
        
        # Base timeline predictions by case type
        timeline_templates = {
            'immigration': {
                'initial_review': 7,
                'document_preparation': 30,
                'filing': 45,
                'response': 90,
                'completion': 180
            },
            'family_law': {
                'initial_review': 14,
                'mediation': 30,
                'court_filing': 60,
                'hearing': 90,
                'completion': 120
            },
            'criminal_defense': {
                'initial_review': 3,
                'investigation': 14,
                'plea_negotiation': 30,
                'trial_prep': 60,
                'trial': 90
            },
            'personal_injury': {
                'initial_review': 7,
                'investigation': 30,
                'settlement_negotiation': 90,
                'litigation': 180,
                'completion': 365
            }
        }
        
        template = timeline_templates.get(case_type, timeline_templates['general'])
        
        # Calculate predicted dates
        start_date = datetime.utcnow()
        timeline = {}
        
        for milestone, days in template.items():
            timeline[milestone] = (start_date + timedelta(days=days)).isoformat()
        
        return {
            'case_type': case_type,
            'predicted_timeline': timeline,
            'confidence': 'medium',  # Could be enhanced with more sophisticated analysis
            'factors_considered': [
                'Case type',
                'Current status',
                'Documentation level',
                'Court schedule'
            ]
        }
    
    def _store_analysis_results(self, case_id: int, analysis: Dict[str, Any], 
                               recommendations: List[Dict[str, Any]], 
                               risk_assessment: Dict[str, Any]):
        """Store analysis results in the case record."""
        try:
            case = Case.query.get(case_id)
            if not case:
                return
            
            # Store in case metadata
            case.metadata = case.metadata or {}
            case.metadata['ai_analysis'] = {
                'analysis': analysis,
                'recommendations': recommendations,
                'risk_assessment': risk_assessment,
                'analysis_date': datetime.utcnow().isoformat()
            }
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error storing analysis results: {e}")
    
    def get_case_insights(self, case_id: int) -> Dict[str, Any]:
        """Get stored case insights and analysis."""
        try:
            case = Case.query.get(case_id)
            if not case or not case.metadata:
                return {'success': False, 'error': 'No analysis available'}
            
            ai_analysis = case.metadata.get('ai_analysis')
            if not ai_analysis:
                return {'success': False, 'error': 'No AI analysis available'}
            
            return {
                'success': True,
                'analysis': ai_analysis['analysis'],
                'recommendations': ai_analysis['recommendations'],
                'risk_assessment': ai_analysis['risk_assessment'],
                'analysis_date': ai_analysis['analysis_date']
            }
            
        except Exception as e:
            logger.error(f"Error getting case insights: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_case_summary(self, case_id: int) -> Dict[str, Any]:
        """Generate a concise case summary."""
        try:
            case = Case.query.get(case_id)
            if not case:
                return {'success': False, 'error': 'Case not found'}
            
            # Get basic case information
            summary = {
                'case_id': case.id,
                'title': case.title,
                'type': case.case_type,
                'status': case.status,
                'priority': case.priority,
                'created_date': case.created_at.isoformat() if case.created_at else None,
                'due_date': case.due_date.isoformat() if case.due_date else None,
                'description': case.description,
                'key_points': []
            }
            
            # Add key points from analysis if available
            if case.metadata and case.metadata.get('ai_analysis'):
                analysis = case.metadata['ai_analysis']['analysis']
                summary['key_points'] = [
                    f"Strengths: {len(analysis.get('strengths', []))} identified",
                    f"Legal issues: {len(analysis.get('legal_issues', []))} identified",
                    f"Recommendations: {len(analysis.get('strategy_recommendations', []))} provided"
                ]
            
            return {'success': True, 'summary': summary}
            
        except Exception as e:
            logger.error(f"Error generating case summary: {e}")
            return {'success': False, 'error': str(e)}

# Create singleton instance
ai_case_analysis_service = AICaseAnalysisService()

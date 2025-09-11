"""
Chatbot Integration Service for SmartProBono
Provides AI-powered chatbot for client support and legal assistance.
"""
import openai
from datetime import datetime
from typing import Dict, List, Any, Optional
from backend.database import db
from backend.models import User, Case, Document, CourtDate
import logging
import json
import re

logger = logging.getLogger(__name__)

class ChatbotIntegrationService:
    """Service for AI-powered chatbot functionality."""
    
    def __init__(self):
        self.openai_api_key = openai.api_key
        self.model = "gpt-4"
        self.max_tokens = 1000
        self.conversation_history = {}  # In production, this should be stored in database
    
    def process_message(self, user_id: int, message: str, session_id: str = None) -> Dict[str, Any]:
        """Process a user message and generate response."""
        try:
            if not session_id:
                session_id = f"user_{user_id}_{datetime.utcnow().timestamp()}"
            
            # Get user context
            user_context = self._get_user_context(user_id)
            
            # Get conversation history
            conversation_history = self._get_conversation_history(session_id)
            
            # Determine intent
            intent = self._classify_intent(message, user_context)
            
            # Generate response based on intent
            response = self._generate_response(message, intent, user_context, conversation_history)
            
            # Store conversation
            self._store_conversation(session_id, user_id, message, response)
            
            return {
                'success': True,
                'response': response['text'],
                'intent': intent,
                'suggestions': response.get('suggestions', []),
                'session_id': session_id
            }
            
        except Exception as e:
            logger.error(f"Error processing chatbot message: {e}")
            return {
                'success': False,
                'error': 'Sorry, I encountered an error. Please try again.',
                'session_id': session_id
            }
    
    def _get_user_context(self, user_id: int) -> Dict[str, Any]:
        """Get user context for personalized responses."""
        try:
            user = User.query.get(user_id)
            if not user:
                return {}
            
            # Get user's cases
            cases = Case.query.filter_by(client_id=user_id).all()
            
            # Get upcoming court dates
            upcoming_dates = CourtDate.query.filter(
                CourtDate.client_id == user_id,
                CourtDate.scheduled_date > datetime.utcnow()
            ).order_by(CourtDate.scheduled_date).limit(5).all()
            
            return {
                'user_id': user_id,
                'user_name': f"{user.first_name} {user.last_name}" if user.first_name else "Client",
                'user_role': user.role,
                'cases': [case.to_dict() for case in cases],
                'upcoming_dates': [cd.to_dict() for cd in upcoming_dates],
                'case_count': len(cases),
                'active_cases': len([c for c in cases if c.status in ['open', 'in_progress']])
            }
            
        except Exception as e:
            logger.error(f"Error getting user context: {e}")
            return {}
    
    def _classify_intent(self, message: str, user_context: Dict[str, Any]) -> str:
        """Classify user intent from message."""
        try:
            if not self.openai_api_key:
                return self._fallback_intent_classification(message)
            
            # Create intent classification prompt
            prompt = f"""
            Classify the following user message into one of these intents:
            
            - case_status: Questions about case status, progress, updates
            - court_dates: Questions about court dates, hearings, appointments
            - documents: Questions about documents, paperwork, filing
            - payments: Questions about payments, fees, billing
            - general_legal: General legal questions, advice requests
            - appointment: Request to schedule appointment, meeting
            - contact: Questions about contacting lawyer, support
            - other: General questions, greetings, unclear intent
            
            User context:
            - Name: {user_context.get('user_name', 'Unknown')}
            - Role: {user_context.get('user_role', 'client')}
            - Active cases: {user_context.get('active_cases', 0)}
            - Upcoming court dates: {len(user_context.get('upcoming_dates', []))}
            
            Message: "{message}"
            
            Respond with only the intent category name.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an intent classification system. Respond with only the intent category name."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            intent = response.choices[0].message.content.strip().lower()
            
            # Validate intent
            valid_intents = [
                'case_status', 'court_dates', 'documents', 'payments',
                'general_legal', 'appointment', 'contact', 'other'
            ]
            
            return intent if intent in valid_intents else 'other'
            
        except Exception as e:
            logger.error(f"Error classifying intent: {e}")
            return self._fallback_intent_classification(message)
    
    def _fallback_intent_classification(self, message: str) -> str:
        """Fallback intent classification using keyword matching."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['case', 'status', 'progress', 'update']):
            return 'case_status'
        elif any(word in message_lower for word in ['court', 'hearing', 'date', 'appointment']):
            return 'court_dates'
        elif any(word in message_lower for word in ['document', 'paperwork', 'file', 'filing']):
            return 'documents'
        elif any(word in message_lower for word in ['payment', 'fee', 'bill', 'cost']):
            return 'payments'
        elif any(word in message_lower for word in ['legal', 'advice', 'help', 'question']):
            return 'general_legal'
        elif any(word in message_lower for word in ['schedule', 'meeting', 'appointment']):
            return 'appointment'
        elif any(word in message_lower for word in ['contact', 'call', 'email', 'reach']):
            return 'contact'
        else:
            return 'other'
    
    def _generate_response(self, message: str, intent: str, user_context: Dict[str, Any], 
                          conversation_history: List[Dict]) -> Dict[str, Any]:
        """Generate appropriate response based on intent."""
        try:
            if intent == 'case_status':
                return self._generate_case_status_response(message, user_context)
            elif intent == 'court_dates':
                return self._generate_court_dates_response(message, user_context)
            elif intent == 'documents':
                return self._generate_documents_response(message, user_context)
            elif intent == 'payments':
                return self._generate_payments_response(message, user_context)
            elif intent == 'general_legal':
                return self._generate_general_legal_response(message, user_context)
            elif intent == 'appointment':
                return self._generate_appointment_response(message, user_context)
            elif intent == 'contact':
                return self._generate_contact_response(message, user_context)
            else:
                return self._generate_general_response(message, user_context)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'text': "I'm sorry, I couldn't process your request. Please try again or contact support.",
                'suggestions': ['Contact support', 'Schedule appointment']
            }
    
    def _generate_case_status_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for case status questions."""
        cases = user_context.get('cases', [])
        active_cases = [c for c in cases if c['status'] in ['open', 'in_progress']]
        
        if not cases:
            return {
                'text': "I don't see any cases associated with your account. Would you like to create a new case or contact support?",
                'suggestions': ['Create new case', 'Contact support', 'Schedule appointment']
            }
        
        if not active_cases:
            return {
                'text': f"You have {len(cases)} case(s) in your account, but none are currently active. All cases are in '{cases[0]['status']}' status. Would you like more details about any specific case?",
                'suggestions': ['View case details', 'Contact lawyer', 'Schedule appointment']
            }
        
        case_info = []
        for case in active_cases[:3]:  # Show up to 3 cases
            case_info.append(f"• {case['title']} - Status: {case['status']} (Priority: {case['priority']})")
        
        response_text = f"You have {len(active_cases)} active case(s):\n\n" + "\n".join(case_info)
        
        if len(active_cases) > 3:
            response_text += f"\n\n...and {len(active_cases) - 3} more cases."
        
        return {
            'text': response_text,
            'suggestions': ['View all cases', 'Get case details', 'Contact lawyer']
        }
    
    def _generate_court_dates_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for court dates questions."""
        upcoming_dates = user_context.get('upcoming_dates', [])
        
        if not upcoming_dates:
            return {
                'text': "You don't have any upcoming court dates scheduled. Would you like to schedule one or check your case status?",
                'suggestions': ['Schedule court date', 'Check case status', 'Contact lawyer']
            }
        
        date_info = []
        for date in upcoming_dates[:3]:  # Show up to 3 dates
            scheduled_date = datetime.fromisoformat(date['scheduled_date'].replace('Z', '+00:00'))
            formatted_date = scheduled_date.strftime('%A, %B %d, %Y at %I:%M %p')
            date_info.append(f"• {date['title']} - {formatted_date} at {date['court_location']}")
        
        response_text = f"You have {len(upcoming_dates)} upcoming court date(s):\n\n" + "\n".join(date_info)
        
        if len(upcoming_dates) > 3:
            response_text += f"\n\n...and {len(upcoming_dates) - 3} more dates."
        
        return {
            'text': response_text,
            'suggestions': ['View all court dates', 'Get directions', 'Contact lawyer']
        }
    
    def _generate_documents_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for document questions."""
        return {
            'text': "I can help you with document-related questions. You can upload documents, view existing ones, or get help with specific paperwork. What would you like to know?",
            'suggestions': ['Upload document', 'View documents', 'Get document help', 'Contact lawyer']
        }
    
    def _generate_payments_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for payment questions."""
        return {
            'text': "I can help you with payment-related questions. You can view your payment history, make a payment, or get billing information. What do you need?",
            'suggestions': ['Make payment', 'View payment history', 'Get billing info', 'Contact support']
        }
    
    def _generate_general_legal_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for general legal questions."""
        return {
            'text': "I can provide general legal information, but I cannot give specific legal advice. For detailed legal guidance, I recommend consulting with your attorney. What general information can I help you with?",
            'suggestions': ['Schedule consultation', 'Contact lawyer', 'View legal resources', 'Get case help']
        }
    
    def _generate_appointment_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for appointment requests."""
        return {
            'text': "I can help you schedule an appointment with your attorney. What type of appointment do you need?",
            'suggestions': ['Schedule consultation', 'Schedule court prep', 'Schedule document review', 'Contact lawyer directly']
        }
    
    def _generate_contact_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for contact questions."""
        return {
            'text': "I can help you get in touch with your legal team. You can contact your attorney directly, reach out to support, or schedule a meeting. How would you like to proceed?",
            'suggestions': ['Contact lawyer', 'Contact support', 'Schedule meeting', 'Send message']
        }
    
    def _generate_general_response(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate general response for unclear intents."""
        return {
            'text': f"Hello {user_context.get('user_name', 'there')}! I'm here to help you with your legal case. I can assist with case status, court dates, documents, payments, and more. What can I help you with today?",
            'suggestions': ['Check case status', 'View court dates', 'Upload documents', 'Make payment', 'Contact lawyer']
        }
    
    def _get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session."""
        return self.conversation_history.get(session_id, [])
    
    def _store_conversation(self, session_id: str, user_id: int, message: str, response: Dict[str, Any]):
        """Store conversation in history."""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        self.conversation_history[session_id].append({
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'message': message,
            'response': response['text'],
            'intent': response.get('intent', 'unknown')
        })
        
        # Keep only last 10 messages per session
        if len(self.conversation_history[session_id]) > 10:
            self.conversation_history[session_id] = self.conversation_history[session_id][-10:]
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get conversation summary for a session."""
        try:
            history = self.conversation_history.get(session_id, [])
            
            if not history:
                return {'success': False, 'error': 'No conversation history found'}
            
            # Analyze conversation
            intents = [msg.get('intent', 'unknown') for msg in history]
            intent_counts = {}
            for intent in intents:
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            # Get most common topics
            common_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
            return {
                'success': True,
                'message_count': len(history),
                'common_topics': [intent for intent, count in common_intents],
                'last_message': history[-1] if history else None,
                'conversation_duration': self._calculate_conversation_duration(history)
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_conversation_duration(self, history: List[Dict]) -> str:
        """Calculate conversation duration."""
        if len(history) < 2:
            return "0 minutes"
        
        start_time = datetime.fromisoformat(history[0]['timestamp'])
        end_time = datetime.fromisoformat(history[-1]['timestamp'])
        duration = end_time - start_time
        
        minutes = int(duration.total_seconds() / 60)
        if minutes < 1:
            return "Less than 1 minute"
        elif minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            return f"{hours} hours {remaining_minutes} minutes"
    
    def clear_conversation(self, session_id: str) -> Dict[str, Any]:
        """Clear conversation history for a session."""
        try:
            if session_id in self.conversation_history:
                del self.conversation_history[session_id]
                return {'success': True, 'message': 'Conversation cleared'}
            else:
                return {'success': False, 'error': 'Session not found'}
                
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return {'success': False, 'error': str(e)}

# Create singleton instance
chatbot_integration_service = ChatbotIntegrationService()

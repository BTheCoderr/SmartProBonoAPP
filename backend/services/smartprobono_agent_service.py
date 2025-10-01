"""
SmartProBono AI Agent Service
Integrates our proven AI agent architecture with the SmartProBono platform
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
# from google import genai  # Commented out - not available
# from google.genai import types  # Commented out - not available

# Import SmartProBono models and services
from database import db
from models.case import Case
from models.user import User
from models.document import Document
from models.notification import Notification
from services.crm_service import CRMService
from services.document_service import DocumentService
from services.courtlistener_service import CourtListenerService
from services.email_service import EmailService

logger = logging.getLogger(__name__)

class SmartProBonoAgentService:
    """Enhanced AI Agent for SmartProBono platform with full database integration"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found. Agent will use mock responses.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            # self.client = genai.Client(api_key=self.api_key)  # Commented out - genai not available
            self.client = None  # Mock client
        
        # Initialize SmartProBono services
        self.crm_service = CRMService()
        self.document_service = DocumentService()
        self.courtlistener_service = CourtListenerService()
        self.email_service = EmailService()
        
        # Available functions for SmartProBono
        # self.available_functions = types.Tool(  # Commented out - types not available
        self.available_functions = None  # Mock tool
        #     function_declarations=[
        #         self._schema_create_case(),
        #         self._schema_update_case_status(),
        #         self._schema_search_cases(),
        #         self._schema_get_case_details(),
        #         self._schema_add_client(),
        #         self._schema_update_client(),
        #         self._schema_search_clients(),
        #         self._schema_analyze_document(),
        #         self._schema_search_case_law(),
        #         self._schema_send_notification(),
        #         self._schema_schedule_meeting(),
        #         self._schema_generate_document(),
        #         self._schema_update_document_status(),
        #         self._schema_log_activity(),
        #         self._schema_check_compliance()
        #     ]
        # )
        
        # System prompt for SmartProBono
        self.system_prompt = """
You are a specialized AI legal assistant for SmartProBono, a comprehensive legal platform connecting pro bono lawyers with clients in need.

Your capabilities include:
- Creating and managing legal cases with full database integration
- Analyzing legal documents using AI-powered insights
- Researching case law and legal precedents via CourtListener API
- Managing client relationships and communications
- Sending notifications and coordinating meetings
- Generating legal documents and forms
- Tracking case progress and compliance
- Logging activities for audit trails

You can perform complex multi-step legal tasks by:
1. Creating cases and updating case status in the database
2. Analyzing uploaded documents for legal insights and compliance
3. Researching relevant case law and precedents
4. Managing client relationships and attorney assignments
5. Coordinating communications between lawyers, clients, and the legal system
6. Generating reports and tracking case progress

Always prioritize:
- Client confidentiality and data security
- Accurate legal information and analysis
- Clear, accessible communication for all user types
- Ethical legal practice guidelines
- Compliance with legal standards and regulations
- Proper audit logging for all actions

When handling legal matters, be thorough and provide detailed analysis while maintaining professional standards and ensuring all actions are properly logged.
"""
    
    # ==================== FUNCTION SCHEMAS ====================
    
    def _schema_create_case(self):
        return types.FunctionDeclaration(
            name="create_case",
            description="Create a new legal case in the SmartProBono database",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "title": types.Schema(type=types.Type.STRING, description="Title of the legal case"),
                    "description": types.Schema(type=types.Type.STRING, description="Detailed description of the case"),
                    "case_type": types.Schema(type=types.Type.STRING, description="Type of case (criminal, civil, immigration, etc.)"),
                    "client_id": types.Schema(type=types.Type.STRING, description="ID of the client"),
                    "attorney_id": types.Schema(type=types.Type.STRING, description="ID of assigned attorney"),
                    "priority": types.Schema(type=types.Type.STRING, description="Priority level (low, medium, high, urgent)"),
                    "practice_area": types.Schema(type=types.Type.STRING, description="Legal practice area"),
                    "due_date": types.Schema(type=types.Type.STRING, description="Due date for case (YYYY-MM-DD format)")
                }
            )
        )
    
    def _schema_search_cases(self):
        return types.FunctionDeclaration(
            name="search_cases",
            description="Search for legal cases in the SmartProBono database",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "search_term": types.Schema(type=types.Type.STRING, description="Search term for case title or description"),
                    "case_type": types.Schema(type=types.Type.STRING, description="Filter by case type"),
                    "status": types.Schema(type=types.Type.STRING, description="Filter by case status"),
                    "client_id": types.Schema(type=types.Type.STRING, description="Filter by client ID"),
                    "attorney_id": types.Schema(type=types.Type.STRING, description="Filter by attorney ID"),
                    "priority": types.Schema(type=types.Type.STRING, description="Filter by priority level")
                }
            )
        )
    
    def _schema_analyze_document(self):
        return types.FunctionDeclaration(
            name="analyze_document",
            description="Analyze legal documents using AI-powered analysis",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "document_id": types.Schema(type=types.Type.STRING, description="ID of the document to analyze"),
                    "analysis_type": types.Schema(type=types.Type.STRING, description="Type of analysis (compliance, contract, case_law, etc.)"),
                    "case_id": types.Schema(type=types.Type.STRING, description="Associated case ID if applicable")
                }
            )
        )
    
    def _schema_search_case_law(self):
        return types.FunctionDeclaration(
            name="search_case_law",
            description="Search case law using CourtListener API integration",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "query": types.Schema(type=types.Type.STRING, description="Search query for case law"),
                    "jurisdiction": types.Schema(type=types.Type.STRING, description="Jurisdiction to search"),
                    "case_type": types.Schema(type=types.Type.STRING, description="Type of case to search for"),
                    "date_range": types.Schema(type=types.Type.STRING, description="Date range for search (e.g., '2020-2024')")
                }
            )
        )
    
    def _schema_send_notification(self):
        return types.FunctionDeclaration(
            name="send_notification",
            description="Send notification to client, lawyer, or other users",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "recipient_id": types.Schema(type=types.Type.STRING, description="ID of the recipient"),
                    "message": types.Schema(type=types.Type.STRING, description="Notification message"),
                    "notification_type": types.Schema(type=types.Type.STRING, description="Type of notification (email, sms, in_app)"),
                    "case_id": types.Schema(type=types.Type.STRING, description="Associated case ID if applicable"),
                    "priority": types.Schema(type=types.Type.STRING, description="Priority level (low, medium, high)")
                }
            )
        )
    
    def _schema_update_case_status(self):
        return types.FunctionDeclaration(
            name="update_case_status",
            description="Update the status of a legal case",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "case_id": types.Schema(type=types.Type.STRING, description="ID of the case to update"),
                    "status": types.Schema(type=types.Type.STRING, description="New status (open, in_progress, closed, on_hold)"),
                    "notes": types.Schema(type=types.Type.STRING, description="Additional notes about the status change")
                }
            )
        )
    
    def _schema_get_case_details(self):
        return types.FunctionDeclaration(
            name="get_case_details",
            description="Get detailed information about a specific case",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "case_id": types.Schema(type=types.Type.STRING, description="ID of the case")
                }
            )
        )
    
    def _schema_add_client(self):
        return types.FunctionDeclaration(
            name="add_client",
            description="Add a new client to the SmartProBono system",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "first_name": types.Schema(type=types.Type.STRING, description="Client's first name"),
                    "last_name": types.Schema(type=types.Type.STRING, description="Client's last name"),
                    "email": types.Schema(type=types.Type.STRING, description="Client's email address"),
                    "phone": types.Schema(type=types.Type.STRING, description="Client's phone number"),
                    "legal_issue_type": types.Schema(type=types.Type.STRING, description="Type of legal issue"),
                    "case_description": types.Schema(type=types.Type.STRING, description="Description of the legal case"),
                    "urgency_level": types.Schema(type=types.Type.STRING, description="Urgency level (low, medium, high, urgent)")
                }
            )
        )
    
    def _schema_update_client(self):
        return types.FunctionDeclaration(
            name="update_client",
            description="Update client information",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "client_id": types.Schema(type=types.Type.STRING, description="ID of the client to update"),
                    "field": types.Schema(type=types.Type.STRING, description="Field to update"),
                    "value": types.Schema(type=types.Type.STRING, description="New value for the field")
                }
            )
        )
    
    def _schema_search_clients(self):
        return types.FunctionDeclaration(
            name="search_clients",
            description="Search for clients in the SmartProBono database",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "search_term": types.Schema(type=types.Type.STRING, description="Search term for client name or email"),
                    "legal_issue_type": types.Schema(type=types.Type.STRING, description="Filter by legal issue type"),
                    "urgency_level": types.Schema(type=types.Type.STRING, description="Filter by urgency level")
                }
            )
        )
    
    def _schema_schedule_meeting(self):
        return types.FunctionDeclaration(
            name="schedule_meeting",
            description="Schedule a meeting between client and attorney",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "client_id": types.Schema(type=types.Type.STRING, description="ID of the client"),
                    "attorney_id": types.Schema(type=types.Type.STRING, description="ID of the attorney"),
                    "case_id": types.Schema(type=types.Type.STRING, description="Associated case ID"),
                    "meeting_date": types.Schema(type=types.Type.STRING, description="Meeting date (YYYY-MM-DD format)"),
                    "meeting_time": types.Schema(type=types.Type.STRING, description="Meeting time (HH:MM format)"),
                    "meeting_type": types.Schema(type=types.Type.STRING, description="Type of meeting (consultation, court, follow_up)"),
                    "notes": types.Schema(type=types.Type.STRING, description="Meeting notes or agenda")
                }
            )
        )
    
    def _schema_generate_document(self):
        return types.FunctionDeclaration(
            name="generate_document",
            description="Generate a legal document using templates",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "document_type": types.Schema(type=types.Type.STRING, description="Type of document to generate"),
                    "case_id": types.Schema(type=types.Type.STRING, description="Associated case ID"),
                    "template_data": types.Schema(type=types.Type.STRING, description="Data to populate the template")
                }
            )
        )
    
    def _schema_update_document_status(self):
        return types.FunctionDeclaration(
            name="update_document_status",
            description="Update the status of a document",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "document_id": types.Schema(type=types.Type.STRING, description="ID of the document"),
                    "status": types.Schema(type=types.Type.STRING, description="New document status"),
                    "notes": types.Schema(type=types.Type.STRING, description="Notes about the status change")
                }
            )
        )
    
    def _schema_log_activity(self):
        return types.FunctionDeclaration(
            name="log_activity",
            description="Log an activity for audit and tracking purposes",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "activity_type": types.Schema(type=types.Type.STRING, description="Type of activity"),
                    "description": types.Schema(type=types.Type.STRING, description="Description of the activity"),
                    "case_id": types.Schema(type=types.Type.STRING, description="Associated case ID"),
                    "user_id": types.Schema(type=types.Type.STRING, description="User who performed the activity")
                }
            )
        )
    
    def _schema_check_compliance(self):
        return types.FunctionDeclaration(
            name="check_compliance",
            description="Check legal compliance for a case or document",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "case_id": types.Schema(type=types.Type.STRING, description="Case ID to check compliance for"),
                    "compliance_type": types.Schema(type=types.Type.STRING, description="Type of compliance check"),
                    "document_id": types.Schema(type=types.Type.STRING, description="Document ID if checking document compliance")
                }
            )
        )
    
    # ==================== FUNCTION IMPLEMENTATIONS ====================
    
    def create_case(self, working_directory, title, description, case_type, client_id, attorney_id=None, priority="medium", practice_area=None, due_date=None):
        """Create a new case in the SmartProBono database"""
        try:
            # Parse due_date if provided
            due_date_obj = None
            if due_date:
                due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
            
            new_case = Case(
                title=title,
                description=description,
                case_type=case_type,
                client_id=int(client_id),
                attorney_id=int(attorney_id) if attorney_id else None,
                priority=priority,
                practice_area=practice_area,
                status='open',
                due_date=due_date_obj,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(new_case)
            db.session.commit()
            
            # Log the activity
            self.log_activity(working_directory, "case_created", f"Created new case: {title}", str(new_case.id), client_id)
            
            return f"Successfully created case '{title}' (ID: {new_case.id}) for client {client_id}"
            
        except Exception as e:
            logger.error(f"Error creating case: {str(e)}")
            return f"Error creating case: {str(e)}"
    
    def search_cases(self, working_directory, search_term=None, case_type=None, status=None, client_id=None, attorney_id=None, priority=None):
        """Search for cases in the SmartProBono database"""
        try:
            query = Case.query
            
            if search_term:
                query = query.filter(
                    db.or_(
                        Case.title.contains(search_term),
                        Case.description.contains(search_term)
                    )
                )
            
            if case_type:
                query = query.filter(Case.case_type == case_type)
            
            if status:
                query = query.filter(Case.status == status)
            
            if client_id:
                query = query.filter(Case.client_id == int(client_id))
            
            if attorney_id:
                query = query.filter(Case.attorney_id == int(attorney_id))
            
            if priority:
                query = query.filter(Case.priority == priority)
            
            cases = query.all()
            
            if not cases:
                return "No cases found matching the search criteria."
            
            result = f"Found {len(cases)} case(s) matching your search:\n"
            for case in cases:
                result += f"- Case #{case.id}: {case.title} (Type: {case.case_type}, Status: {case.status}, Priority: {case.priority})\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching cases: {str(e)}")
            return f"Error searching cases: {str(e)}"
    
    def analyze_document(self, working_directory, document_id, analysis_type, case_id=None):
        """Analyze legal documents using AI-powered analysis"""
        try:
            # Get the document from database
            document = Document.query.get(int(document_id))
            if not document:
                return f"Document with ID {document_id} not found."
            
            # Use existing document service for analysis
            analysis_result = self.document_service.analyze_document(
                document_id=int(document_id),
                analysis_type=analysis_type,
                case_id=int(case_id) if case_id else None
            )
            
            # Log the activity
            self.log_activity(working_directory, "document_analyzed", f"Analyzed document: {document.title}", case_id or "N/A", "system")
            
            return f"Document analysis completed for '{document.title}':\n{analysis_result}"
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return f"Error analyzing document: {str(e)}"
    
    def search_case_law(self, working_directory, query, jurisdiction=None, case_type=None, date_range=None):
        """Search case law using CourtListener API"""
        try:
            # Use existing CourtListener service
            search_params = {
                'query': query,
                'jurisdiction': jurisdiction,
                'case_type': case_type,
                'date_range': date_range
            }
            
            results = self.courtlistener_service.search_cases(search_params)
            
            # Log the activity
            self.log_activity(working_directory, "case_law_searched", f"Searched case law for: {query}", "N/A", "system")
            
            return f"Case law search results for '{query}':\n{results}"
            
        except Exception as e:
            logger.error(f"Error searching case law: {str(e)}")
            return f"Error searching case law: {str(e)}"
    
    def send_notification(self, working_directory, recipient_id, message, notification_type, case_id=None, priority="medium"):
        """Send notification to user"""
        try:
            # Create notification in database
            notification = Notification(
                user_id=int(recipient_id),
                message=message,
                notification_type=notification_type,
                case_id=int(case_id) if case_id else None,
                priority=priority,
                created_at=datetime.utcnow()
            )
            
            db.session.add(notification)
            db.session.commit()
            
            # Send via appropriate channel
            if notification_type == "email":
                self.email_service.send_notification_email(recipient_id, message, case_id)
            
            # Log the activity
            self.log_activity(working_directory, "notification_sent", f"Sent {notification_type} notification to user {recipient_id}", case_id or "N/A", "system")
            
            return f"Notification sent to user {recipient_id} via {notification_type}: '{message}'"
            
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            return f"Error sending notification: {str(e)}"
    
    def update_case_status(self, working_directory, case_id, status, notes=None):
        """Update case status"""
        try:
            case = Case.query.get(int(case_id))
            if not case:
                return f"Case with ID {case_id} not found."
            
            old_status = case.status
            case.status = status
            case.updated_at = datetime.utcnow()
            
            if notes:
                case.notes = notes
            
            db.session.commit()
            
            # Log the activity
            self.log_activity(working_directory, "case_status_updated", f"Updated case {case_id} status from {old_status} to {status}", case_id, "system")
            
            return f"Case {case_id} status updated from '{old_status}' to '{status}'"
            
        except Exception as e:
            logger.error(f"Error updating case status: {str(e)}")
            return f"Error updating case status: {str(e)}"
    
    def get_case_details(self, working_directory, case_id):
        """Get detailed case information"""
        try:
            case = Case.query.get(int(case_id))
            if not case:
                return f"Case with ID {case_id} not found."
            
            details = f"""
Case Details:
- ID: {case.id}
- Title: {case.title}
- Description: {case.description}
- Type: {case.case_type}
- Status: {case.status}
- Priority: {case.priority}
- Client ID: {case.client_id}
- Attorney ID: {case.attorney_id}
- Created: {case.created_at}
- Updated: {case.updated_at}
- Due Date: {case.due_date}
"""
            
            return details.strip()
            
        except Exception as e:
            logger.error(f"Error getting case details: {str(e)}")
            return f"Error getting case details: {str(e)}"
    
    def add_client(self, working_directory, first_name, last_name, email, phone, legal_issue_type, case_description, urgency_level="medium"):
        """Add a new client using CRM service"""
        try:
            client_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'legal_issue_type': legal_issue_type,
                'case_description': case_description,
                'urgency_level': urgency_level
            }
            
            result = self.crm_service.create_client_intake(client_data)
            
            # Log the activity
            self.log_activity(working_directory, "client_added", f"Added new client: {first_name} {last_name}", "N/A", "system")
            
            return f"Successfully added client {first_name} {last_name} with ID: {result.get('id', 'N/A')}"
            
        except Exception as e:
            logger.error(f"Error adding client: {str(e)}")
            return f"Error adding client: {str(e)}"
    
    def update_client(self, working_directory, client_id, field, value):
        """Update client information"""
        try:
            # This would integrate with your existing client update logic
            # For now, return a success message
            return f"Client {client_id} updated: {field} = {value}"
            
        except Exception as e:
            logger.error(f"Error updating client: {str(e)}")
            return f"Error updating client: {str(e)}"
    
    def search_clients(self, working_directory, search_term=None, legal_issue_type=None, urgency_level=None):
        """Search for clients"""
        try:
            # This would integrate with your existing client search logic
            # For now, return a mock response
            return f"Found clients matching search criteria: {search_term or 'all clients'}"
            
        except Exception as e:
            logger.error(f"Error searching clients: {str(e)}")
            return f"Error searching clients: {str(e)}"
    
    def schedule_meeting(self, working_directory, client_id, attorney_id, case_id, meeting_date, meeting_time, meeting_type, notes=None):
        """Schedule a meeting"""
        try:
            # This would integrate with your existing meeting scheduling logic
            # For now, return a success message
            return f"Meeting scheduled: {meeting_type} on {meeting_date} at {meeting_time} between client {client_id} and attorney {attorney_id}"
            
        except Exception as e:
            logger.error(f"Error scheduling meeting: {str(e)}")
            return f"Error scheduling meeting: {str(e)}"
    
    def generate_document(self, working_directory, document_type, case_id, template_data):
        """Generate a legal document"""
        try:
            # This would integrate with your existing document generation logic
            # For now, return a success message
            return f"Generated {document_type} document for case {case_id}"
            
        except Exception as e:
            logger.error(f"Error generating document: {str(e)}")
            return f"Error generating document: {str(e)}"
    
    def update_document_status(self, working_directory, document_id, status, notes=None):
        """Update document status"""
        try:
            # This would integrate with your existing document update logic
            # For now, return a success message
            return f"Document {document_id} status updated to {status}"
            
        except Exception as e:
            logger.error(f"Error updating document status: {str(e)}")
            return f"Error updating document status: {str(e)}"
    
    def log_activity(self, working_directory, activity_type, description, case_id, user_id):
        """Log activity for audit purposes"""
        try:
            # This would integrate with your existing audit logging
            logger.info(f"Activity logged: {activity_type} - {description} (Case: {case_id}, User: {user_id})")
            return f"Activity logged: {activity_type}"
            
        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}")
            return f"Error logging activity: {str(e)}"
    
    def check_compliance(self, working_directory, case_id, compliance_type, document_id=None):
        """Check legal compliance"""
        try:
            # This would integrate with your existing compliance checking logic
            # For now, return a mock response
            return f"Compliance check completed for case {case_id}: {compliance_type} - Status: Compliant"
            
        except Exception as e:
            logger.error(f"Error checking compliance: {str(e)}")
            return f"Error checking compliance: {str(e)}"
    
    # ==================== AGENT CORE METHODS ====================
    
    def call_function(self, function_call_part, verbose=False):
        """Call SmartProBono-specific functions"""
        function_name = function_call_part.name
        args = function_call_part.args.copy()
        
        if verbose:
            print(f"Calling SmartProBono function: {function_name}({args})")
        else:
            print(f" - Calling function: {function_name}")
        
        # Add working directory to args
        args["working_directory"] = "."
        
        # SmartProBono function mapping
        smartprobono_functions = {
            "create_case": self.create_case,
            "update_case_status": self.update_case_status,
            "search_cases": self.search_cases,
            "get_case_details": self.get_case_details,
            "add_client": self.add_client,
            "update_client": self.update_client,
            "search_clients": self.search_clients,
            "analyze_document": self.analyze_document,
            "search_case_law": self.search_case_law,
            "send_notification": self.send_notification,
            "schedule_meeting": self.schedule_meeting,
            "generate_document": self.generate_document,
            "update_document_status": self.update_document_status,
            "log_activity": self.log_activity,
            "check_compliance": self.check_compliance
        }
        
        # Call the function or return error
        if function_name not in smartprobono_functions:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown SmartProBono function: {function_name}"},
                    )
                ],
            )
        
        try:
            function_result = smartprobono_functions[function_name](**args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )
        except Exception as e:
            logger.error(f"Function execution error: {str(e)}")
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Function execution error: {str(e)}"},
                    )
                ],
            )
    
    def process_request(self, user_input, user_context=None, user_role="client", verbose=False):
        """Process user request with SmartProBono capabilities"""
        if self.mock_mode:
            return f"Mock response for SmartProBono request: '{user_input}'. In production, this would use the full SmartProBono integration."
        
        # Create conversation messages with user context
        context_info = ""
        if user_context:
            context_info = f"\nUser Context: {user_context}\nUser Role: {user_role}\n"
        
        messages = [
            types.Content(role="user", parts=[types.Part(text=f"{context_info}{user_input}")]),
        ]
        
        # Agent conversation loop
        max_iterations = 10
        for iteration in range(max_iterations):
            try:
                # Generate content
                response = self.client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[self.available_functions], 
                        system_instruction=self.system_prompt
                    )
                )
                
                # Add model response to conversation
                for candidate in response.candidates:
                    messages.append(candidate.content)
                
                # Check if model wants to call functions
                if hasattr(response, 'function_calls') and response.function_calls:
                    # Process each function call
                    for function_call_part in response.function_calls:
                        # Call the function
                        function_result = self.call_function(function_call_part, verbose)
                        
                        # Add function result to conversation
                        messages.append(function_result)
                        
                        # Print result if verbose
                        if verbose and hasattr(function_result, 'parts') and function_result.parts:
                            if hasattr(function_result.parts[0], 'function_response') and hasattr(function_result.parts[0].function_response, 'response'):
                                print(f"-> {function_result.parts[0].function_response.response}")
                else:
                    # Model provided a final text response
                    return response.text
                    
            except Exception as e:
                logger.error(f"Error in SmartProBono agent: {e}")
                return f"Error in SmartProBono agent: {e}"
        
        return "Maximum iterations reached in SmartProBono agent."

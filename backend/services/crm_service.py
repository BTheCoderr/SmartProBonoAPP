"""
Comprehensive CRM Service for SmartProBono
Handles all client, lawyer, and bondsman operations with full database integration.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, desc, asc
from database import db
from models import (
    User, Case, Document, Payment, BailBond, CourtDate, 
    ClientIntake, Task, Notification
)
import logging

logger = logging.getLogger(__name__)

class CRMService:
    """Comprehensive CRM service for managing all aspects of the legal practice."""
    
    def __init__(self):
        self.db = db
    
    # ==================== CLIENT OPERATIONS ====================
    
    def create_client_intake(self, intake_data):
        """Create a new client intake."""
        try:
            intake = ClientIntake(
                first_name=intake_data['first_name'],
                last_name=intake_data['last_name'],
                email=intake_data['email'],
                phone=intake_data['phone'],
                date_of_birth=datetime.strptime(intake_data['date_of_birth'], '%Y-%m-%d').date() if intake_data.get('date_of_birth') else None,
                street_address=intake_data.get('street_address'),
                city=intake_data.get('city'),
                state=intake_data.get('state'),
                zip_code=intake_data.get('zip_code'),
                country=intake_data.get('country', 'USA'),
                legal_issue_type=intake_data['legal_issue_type'],
                case_description=intake_data['case_description'],
                urgency_level=intake_data.get('urgency_level', 'medium'),
                income_level=intake_data.get('income_level'),
                can_afford_legal_fees=intake_data.get('can_afford_legal_fees'),
                needs_pro_bono=intake_data.get('needs_pro_bono', False),
                case_start_date=datetime.strptime(intake_data['case_start_date'], '%Y-%m-%d').date() if intake_data.get('case_start_date') else None,
                previous_legal_representation=intake_data.get('previous_legal_representation', False),
                previous_attorney_name=intake_data.get('previous_attorney_name'),
                notes=intake_data.get('notes'),
                metadata=intake_data.get('metadata', {})
            )
            
            self.db.session.add(intake)
            self.db.session.commit()
            
            # Create initial task for intake review
            self.create_task({
                'title': f'Review intake for {intake.get_full_name()}',
                'description': f'Review intake application for {intake.legal_issue_type} case',
                'task_type': 'intake_review',
                'priority': intake.urgency_level,
                'intake_id': intake.id,
                'assigned_to': 1,  # Default to admin/lawyer
                'due_date': datetime.utcnow() + timedelta(days=2)
            })
            
            return intake.to_dict()
        except Exception as e:
            logger.error(f"Error creating client intake: {e}")
            self.db.session.rollback()
            raise e
    
    def get_client_cases(self, client_id):
        """Get all cases for a specific client."""
        try:
            cases = Case.query.filter_by(client_id=client_id).all()
            return [case.to_dict() for case in cases]
        except Exception as e:
            logger.error(f"Error getting client cases: {e}")
            raise e
    
    def get_client_documents(self, client_id):
        """Get all documents for a specific client."""
        try:
            documents = Document.query.join(Case).filter(Case.client_id == client_id).all()
            return [doc.to_dict() for doc in documents]
        except Exception as e:
            logger.error(f"Error getting client documents: {e}")
            raise e
    
    def get_client_court_dates(self, client_id):
        """Get all court dates for a specific client."""
        try:
            court_dates = CourtDate.query.filter_by(client_id=client_id).all()
            return [cd.to_dict() for cd in court_dates]
        except Exception as e:
            logger.error(f"Error getting client court dates: {e}")
            raise e
    
    def get_client_notifications(self, client_id):
        """Get all notifications for a specific client."""
        try:
            notifications = Notification.query.filter_by(user_id=client_id).order_by(desc(Notification.created_at)).all()
            return [notif.to_dict() for notif in notifications]
        except Exception as e:
            logger.error(f"Error getting client notifications: {e}")
            raise e
    
    # ==================== LAWYER OPERATIONS ====================
    
    def get_all_clients(self, lawyer_id=None):
        """Get all clients, optionally filtered by assigned lawyer."""
        try:
            query = User.query.filter_by(role='client')
            if lawyer_id:
                # Get clients assigned to specific lawyer
                cases = Case.query.filter_by(attorney_id=lawyer_id).all()
                client_ids = [case.client_id for case in cases]
                query = query.filter(User.id.in_(client_ids))
            
            clients = query.all()
            return [client.to_dict() for client in clients]
        except Exception as e:
            logger.error(f"Error getting clients: {e}")
            raise e
    
    def get_lawyer_clients(self, lawyer_id):
        """Get clients assigned to a specific lawyer (alias for get_all_clients)."""
        return self.get_all_clients(lawyer_id)
    
    def create_case(self, case_data):
        """Create a new case."""
        try:
            case = Case(
                title=case_data['title'],
                description=case_data['description'],
                client_id=case_data['client_id'],
                attorney_id=case_data.get('attorney_id'),
                case_type=case_data.get('case_type'),
                priority=case_data.get('priority', 'medium'),
                practice_area=case_data.get('practice_area'),
                due_date=datetime.strptime(case_data['due_date'], '%Y-%m-%d') if case_data.get('due_date') else None,
                notes=case_data.get('notes', []),
                tags=case_data.get('tags', [])
            )
            
            self.db.session.add(case)
            self.db.session.commit()
            
            # Create initial court date if provided
            if case_data.get('court_date'):
                self.create_court_date({
                    'case_id': case.id,
                    'client_id': case.client_id,
                    'title': f'Initial hearing for {case.title}',
                    'description': 'Initial court hearing',
                    'court_location': case_data.get('court_location', 'TBD'),
                    'scheduled_date': case_data['court_date'],
                    'event_type': 'hearing'
                })
            
            return case.to_dict()
        except Exception as e:
            logger.error(f"Error creating case: {e}")
            self.db.session.rollback()
            raise e
    
    def get_lawyer_cases(self, lawyer_id):
        """Get all cases for a specific lawyer."""
        try:
            cases = Case.query.filter_by(attorney_id=lawyer_id).all()
            return [case.to_dict() for case in cases]
        except Exception as e:
            logger.error(f"Error getting lawyer cases: {e}")
            raise e
    
    def get_lawyer_tasks(self, lawyer_id):
        """Get all tasks for a specific lawyer."""
        try:
            tasks = Task.query.filter_by(assigned_to=lawyer_id).all()
            return [task.to_dict() for task in tasks]
        except Exception as e:
            logger.error(f"Error getting lawyer tasks: {e}")
            raise e
    
    def create_task(self, task_data):
        """Create a new task."""
        try:
            task = Task(
                title=task_data['title'],
                description=task_data.get('description'),
                task_type=task_data['task_type'],
                priority=task_data.get('priority', 'medium'),
                assigned_to=task_data['assigned_to'],
                assigned_by=task_data.get('assigned_by'),
                case_id=task_data.get('case_id'),
                intake_id=task_data.get('intake_id'),
                due_date=datetime.strptime(task_data['due_date'], '%Y-%m-%d %H:%M:%S') if task_data.get('due_date') else None,
                notes=task_data.get('notes'),
                metadata=task_data.get('metadata', {})
            )
            
            self.db.session.add(task)
            self.db.session.commit()
            
            return task.to_dict()
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            self.db.session.rollback()
            raise e
    
    # ==================== BONDSMAN OPERATIONS ====================
    
    def create_bail_bond(self, bond_data):
        """Create a new bail bond."""
        try:
            bond = BailBond(
                client_id=bond_data['client_id'],
                bondsman_id=bond_data.get('bondsman_id'),
                case_number=bond_data['case_number'],
                charges=bond_data['charges'],
                bond_amount=bond_data['bond_amount'],
                premium_amount=bond_data['premium_amount'],
                risk_level=bond_data.get('risk_level', 'medium'),
                court_location=bond_data.get('court_location'),
                court_date=datetime.strptime(bond_data['court_date'], '%Y-%m-%d') if bond_data.get('court_date') else None,
                cosigner_name=bond_data.get('cosigner_name'),
                cosigner_phone=bond_data.get('cosigner_phone'),
                cosigner_address=bond_data.get('cosigner_address'),
                notes=bond_data.get('notes'),
                metadata=bond_data.get('metadata', {})
            )
            
            self.db.session.add(bond)
            self.db.session.commit()
            
            # Create initial payment record
            self.create_payment({
                'client_id': bond.client_id,
                'bond_id': bond.id,
                'amount': bond.premium_amount,
                'payment_method': bond_data.get('payment_method', 'cash'),
                'payment_type': 'premium',
                'payment_date': datetime.utcnow(),
                'status': 'completed',
                'notes': 'Initial premium payment'
            })
            
            return bond.to_dict()
        except Exception as e:
            logger.error(f"Error creating bail bond: {e}")
            self.db.session.rollback()
            raise e
    
    def get_bondsman_bonds(self, bondsman_id=None):
        """Get all bail bonds, optionally filtered by bondsman."""
        try:
            query = BailBond.query
            if bondsman_id:
                query = query.filter_by(bondsman_id=bondsman_id)
            
            bonds = query.all()
            return [bond.to_dict() for bond in bonds]
        except Exception as e:
            logger.error(f"Error getting bail bonds: {e}")
            raise e
    
    def get_bondsman_payments(self, bondsman_id=None):
        """Get all payments, optionally filtered by bondsman."""
        try:
            query = Payment.query.join(BailBond)
            if bondsman_id:
                query = query.filter(BailBond.bondsman_id == bondsman_id)
            
            payments = query.all()
            return [payment.to_dict() for payment in payments]
        except Exception as e:
            logger.error(f"Error getting payments: {e}")
            raise e
    
    def create_payment(self, payment_data):
        """Create a new payment record."""
        try:
            payment = Payment(
                client_id=payment_data['client_id'],
                case_id=payment_data.get('case_id'),
                bond_id=payment_data.get('bond_id'),
                amount=payment_data['amount'],
                currency=payment_data.get('currency', 'USD'),
                payment_method=payment_data['payment_method'],
                payment_type=payment_data['payment_type'],
                status=payment_data.get('status', 'completed'),
                transaction_id=payment_data.get('transaction_id'),
                reference_number=payment_data.get('reference_number'),
                payment_date=datetime.strptime(payment_data['payment_date'], '%Y-%m-%d %H:%M:%S') if isinstance(payment_data.get('payment_date'), str) else payment_data.get('payment_date', datetime.utcnow()),
                due_date=datetime.strptime(payment_data['due_date'], '%Y-%m-%d %H:%M:%S') if payment_data.get('due_date') else None,
                notes=payment_data.get('notes'),
                metadata=payment_data.get('metadata', {})
            )
            
            self.db.session.add(payment)
            self.db.session.commit()
            
            return payment.to_dict()
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            self.db.session.rollback()
            raise e
    
    # ==================== COURT DATE OPERATIONS ====================
    
    def create_court_date(self, court_date_data):
        """Create a new court date."""
        try:
            court_date = CourtDate(
                case_id=court_date_data.get('case_id'),
                bond_id=court_date_data.get('bond_id'),
                client_id=court_date_data['client_id'],
                title=court_date_data['title'],
                description=court_date_data.get('description'),
                court_location=court_date_data['court_location'],
                court_room=court_date_data.get('court_room'),
                scheduled_date=datetime.strptime(court_date_data['scheduled_date'], '%Y-%m-%d %H:%M:%S') if isinstance(court_date_data.get('scheduled_date'), str) else court_date_data['scheduled_date'],
                duration_minutes=court_date_data.get('duration_minutes', 60),
                event_type=court_date_data['event_type'],
                reminder_days_before=court_date_data.get('reminder_days_before', 1),
                notes=court_date_data.get('notes'),
                metadata=court_date_data.get('metadata', {})
            )
            
            self.db.session.add(court_date)
            self.db.session.commit()
            
            return court_date.to_dict()
        except Exception as e:
            logger.error(f"Error creating court date: {e}")
            self.db.session.rollback()
            raise e
    
    def get_upcoming_court_dates(self, days_ahead=30):
        """Get upcoming court dates within specified days."""
        try:
            end_date = datetime.utcnow() + timedelta(days=days_ahead)
            court_dates = CourtDate.query.filter(
                and_(
                    CourtDate.scheduled_date >= datetime.utcnow(),
                    CourtDate.scheduled_date <= end_date,
                    CourtDate.status == 'scheduled'
                )
            ).order_by(asc(CourtDate.scheduled_date)).all()
            
            return [cd.to_dict() for cd in court_dates]
        except Exception as e:
            logger.error(f"Error getting upcoming court dates: {e}")
            raise e
    
    # ==================== NOTIFICATION OPERATIONS ====================
    
    def create_notification(self, notification_data):
        """Create a new notification."""
        try:
            notification = Notification(
                user_id=notification_data['user_id'],
                title=notification_data['title'],
                message=notification_data['message'],
                notification_type=notification_data.get('notification_type', 'info'),
                priority=notification_data.get('priority', 'medium'),
                is_read=notification_data.get('is_read', False),
                metadata=notification_data.get('metadata', {})
            )
            
            self.db.session.add(notification)
            self.db.session.commit()
            
            return notification.to_dict()
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            self.db.session.rollback()
            raise e
    
    def get_user_notifications(self, user_id, unread_only=False):
        """Get notifications for a user."""
        try:
            query = Notification.query.filter_by(user_id=user_id)
            if unread_only:
                query = query.filter_by(is_read=False)
            
            notifications = query.order_by(desc(Notification.created_at)).all()
            return [notif.to_dict() for notif in notifications]
        except Exception as e:
            logger.error(f"Error getting user notifications: {e}")
            raise e
    
    def mark_notification_read(self, notification_id):
        """Mark a notification as read."""
        try:
            notification = Notification.query.get(notification_id)
            if notification:
                notification.is_read = True
                self.db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            raise e
    
    # ==================== ANALYTICS OPERATIONS ====================
    
    def get_dashboard_analytics(self, user_role, user_id=None):
        """Get dashboard analytics based on user role."""
        try:
            analytics = {}
            
            if user_role == 'client':
                analytics = {
                    'total_cases': Case.query.filter_by(client_id=user_id).count(),
                    'active_cases': Case.query.filter(and_(Case.client_id == user_id, Case.status.in_(['open', 'in_progress']))).count(),
                    'upcoming_court_dates': CourtDate.query.filter(and_(CourtDate.client_id == user_id, CourtDate.scheduled_date >= datetime.utcnow())).count(),
                    'unread_notifications': Notification.query.filter(and_(Notification.user_id == user_id, Notification.is_read == False)).count()
                }
            elif user_role == 'lawyer':
                analytics = {
                    'total_cases': Case.query.filter_by(attorney_id=user_id).count(),
                    'active_cases': Case.query.filter(and_(Case.attorney_id == user_id, Case.status.in_(['open', 'in_progress']))).count(),
                    'pending_tasks': Task.query.filter(and_(Task.assigned_to == user_id, Task.status == 'pending')).count(),
                    'overdue_tasks': Task.query.filter(and_(Task.assigned_to == user_id, Task.due_date < datetime.utcnow(), Task.status != 'completed')).count()
                }
            elif user_role == 'bondsman':
                analytics = {
                    'total_bonds': BailBond.query.filter_by(bondsman_id=user_id).count(),
                    'active_bonds': BailBond.query.filter(and_(BailBond.bondsman_id == user_id, BailBond.status == 'active')).count(),
                    'total_payments': Payment.query.join(BailBond).filter(BailBond.bondsman_id == user_id).count(),
                    'pending_payments': Payment.query.join(BailBond).filter(and_(BailBond.bondsman_id == user_id, Payment.status == 'pending')).count()
                }
            
            return analytics
        except Exception as e:
            logger.error(f"Error getting dashboard analytics: {e}")
            raise e

# Create singleton instance
crm_service = CRMService()

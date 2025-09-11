"""
Immigration Workflow Service for SmartProBono
Handles specialized workflows for immigration cases.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from backend.database import db
from backend.models import Case, CourtDate, Document, Task, User
import logging
import json

logger = logging.getLogger(__name__)

class ImmigrationWorkflowService:
    """Service for managing immigration case workflows."""
    
    def __init__(self):
        self.immigration_forms = {
            'i485': 'Application to Register Permanent Residence or Adjust Status',
            'i130': 'Petition for Alien Relative',
            'i765': 'Application for Employment Authorization',
            'i131': 'Application for Travel Document',
            'n400': 'Application for Naturalization',
            'i90': 'Application to Replace Permanent Resident Card',
            'i751': 'Petition to Remove Conditions on Residence',
            'i821d': 'Consideration of Deferred Action for Childhood Arrivals'
        }
        
        self.immigration_statuses = [
            'initial_consultation',
            'document_collection',
            'form_preparation',
            'form_review',
            'filing',
            'receipt_notice',
            'biometrics_scheduled',
            'biometrics_completed',
            'interview_scheduled',
            'interview_completed',
            'decision_pending',
            'approved',
            'denied',
            'appeal_filed',
            'closed'
        ]
    
    def create_immigration_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new immigration case with specialized workflow."""
        try:
            # Create base case
            case = Case(
                title=case_data['title'],
                description=case_data['description'],
                client_id=case_data['client_id'],
                attorney_id=case_data.get('attorney_id'),
                case_type='immigration',
                practice_area='immigration',
                priority=case_data.get('priority', 'medium'),
                status='initial_consultation',
                notes=case_data.get('notes', [])
            )
            
            db.session.add(case)
            db.session.commit()
            
            # Create immigration-specific metadata
            immigration_metadata = {
                'immigration_form': case_data.get('immigration_form'),
                'current_status': 'initial_consultation',
                'priority_date': case_data.get('priority_date'),
                'receipt_number': None,
                'alien_number': case_data.get('alien_number'),
                'country_of_origin': case_data.get('country_of_origin'),
                'current_immigration_status': case_data.get('current_immigration_status'),
                'family_members': case_data.get('family_members', []),
                'work_history': case_data.get('work_history', []),
                'criminal_history': case_data.get('criminal_history', []),
                'medical_conditions': case_data.get('medical_conditions', []),
                'timeline': self._create_immigration_timeline(case_data.get('immigration_form'))
            }
            
            case.metadata = immigration_metadata
            db.session.commit()
            
            # Create initial tasks
            self._create_initial_immigration_tasks(case)
            
            return {
                'success': True,
                'case': case.to_dict(),
                'workflow_created': True
            }
            
        except Exception as e:
            logger.error(f"Error creating immigration case: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _create_immigration_timeline(self, form_type: str) -> Dict[str, Any]:
        """Create timeline based on immigration form type."""
        timelines = {
            'i485': {
                'initial_consultation': 0,
                'document_collection': 7,
                'form_preparation': 30,
                'form_review': 45,
                'filing': 60,
                'receipt_notice': 90,
                'biometrics_scheduled': 120,
                'interview_scheduled': 180,
                'decision_pending': 240,
                'approved': 300
            },
            'n400': {
                'initial_consultation': 0,
                'document_collection': 7,
                'form_preparation': 21,
                'form_review': 35,
                'filing': 45,
                'receipt_notice': 60,
                'biometrics_scheduled': 90,
                'interview_scheduled': 150,
                'decision_pending': 180,
                'approved': 210
            },
            'i130': {
                'initial_consultation': 0,
                'document_collection': 14,
                'form_preparation': 30,
                'form_review': 45,
                'filing': 60,
                'receipt_notice': 90,
                'decision_pending': 180,
                'approved': 240
            }
        }
        
        return timelines.get(form_type, timelines['i485'])
    
    def _create_initial_immigration_tasks(self, case: Case):
        """Create initial tasks for immigration case."""
        try:
            tasks = [
                {
                    'title': 'Initial Client Consultation',
                    'description': 'Conduct initial consultation with client to understand case details',
                    'task_type': 'consultation',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=3),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                },
                {
                    'title': 'Document Collection',
                    'description': 'Collect all required documents for immigration application',
                    'task_type': 'document_collection',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=14),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                },
                {
                    'title': 'Form Preparation',
                    'description': f'Prepare {case.metadata.get("immigration_form", "immigration")} form',
                    'task_type': 'form_preparation',
                    'priority': 'medium',
                    'due_date': datetime.utcnow() + timedelta(days=30),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                }
            ]
            
            for task_data in tasks:
                task = Task(
                    title=task_data['title'],
                    description=task_data['description'],
                    task_type=task_data['task_type'],
                    priority=task_data['priority'],
                    assigned_to=task_data['assigned_to'],
                    case_id=task_data['case_id'],
                    due_date=task_data['due_date']
                )
                db.session.add(task)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error creating initial immigration tasks: {e}")
    
    def update_immigration_status(self, case_id: int, new_status: str, notes: str = None) -> Dict[str, Any]:
        """Update immigration case status."""
        try:
            case = Case.query.get(case_id)
            if not case or case.case_type != 'immigration':
                return {'success': False, 'error': 'Immigration case not found'}
            
            if new_status not in self.immigration_statuses:
                return {'success': False, 'error': 'Invalid immigration status'}
            
            # Update case status
            old_status = case.status
            case.status = new_status
            
            # Update metadata
            if case.metadata:
                case.metadata['current_status'] = new_status
                case.metadata['status_history'] = case.metadata.get('status_history', [])
                case.metadata['status_history'].append({
                    'status': new_status,
                    'date': datetime.utcnow().isoformat(),
                    'notes': notes
                })
            
            db.session.commit()
            
            # Create status-specific tasks
            self._create_status_specific_tasks(case, new_status)
            
            return {
                'success': True,
                'case': case.to_dict(),
                'status_updated': True,
                'old_status': old_status,
                'new_status': new_status
            }
            
        except Exception as e:
            logger.error(f"Error updating immigration status: {e}")
            return {'success': False, 'error': str(e)}
    
    def _create_status_specific_tasks(self, case: Case, status: str):
        """Create tasks specific to immigration status."""
        try:
            task_templates = {
                'document_collection': {
                    'title': 'Collect Required Documents',
                    'description': 'Gather all necessary documents for immigration application',
                    'task_type': 'document_collection',
                    'priority': 'high',
                    'due_days': 14
                },
                'form_preparation': {
                    'title': 'Prepare Immigration Form',
                    'description': f'Complete {case.metadata.get("immigration_form", "immigration")} form',
                    'task_type': 'form_preparation',
                    'priority': 'high',
                    'due_days': 21
                },
                'filing': {
                    'title': 'File Immigration Application',
                    'description': 'Submit completed immigration application to USCIS',
                    'task_type': 'filing',
                    'priority': 'high',
                    'due_days': 7
                },
                'biometrics_scheduled': {
                    'title': 'Prepare for Biometrics Appointment',
                    'description': 'Prepare client for biometrics appointment',
                    'task_type': 'appointment_prep',
                    'priority': 'medium',
                    'due_days': 3
                },
                'interview_scheduled': {
                    'title': 'Prepare for Immigration Interview',
                    'description': 'Prepare client for immigration interview',
                    'task_type': 'interview_prep',
                    'priority': 'high',
                    'due_days': 7
                }
            }
            
            if status in task_templates:
                template = task_templates[status]
                task = Task(
                    title=template['title'],
                    description=template['description'],
                    task_type=template['task_type'],
                    priority=template['priority'],
                    assigned_to=case.attorney_id,
                    case_id=case.id,
                    due_date=datetime.utcnow() + timedelta(days=template['due_days'])
                )
                db.session.add(task)
                db.session.commit()
                
        except Exception as e:
            logger.error(f"Error creating status-specific tasks: {e}")
    
    def get_immigration_forms(self) -> Dict[str, Any]:
        """Get available immigration forms."""
        return {
            'success': True,
            'forms': self.immigration_forms
        }
    
    def get_immigration_statuses(self) -> Dict[str, Any]:
        """Get available immigration statuses."""
        return {
            'success': True,
            'statuses': self.immigration_statuses
        }
    
    def get_immigration_timeline(self, case_id: int) -> Dict[str, Any]:
        """Get immigration case timeline."""
        try:
            case = Case.query.get(case_id)
            if not case or case.case_type != 'immigration':
                return {'success': False, 'error': 'Immigration case not found'}
            
            timeline = case.metadata.get('timeline', {}) if case.metadata else {}
            status_history = case.metadata.get('status_history', []) if case.metadata else []
            
            return {
                'success': True,
                'timeline': timeline,
                'status_history': status_history,
                'current_status': case.status,
                'progress_percentage': self._calculate_progress_percentage(case)
            }
            
        except Exception as e:
            logger.error(f"Error getting immigration timeline: {e}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_progress_percentage(self, case: Case) -> int:
        """Calculate case progress percentage."""
        try:
            if not case.metadata or 'timeline' not in case.metadata:
                return 0
            
            timeline = case.metadata['timeline']
            current_status = case.status
            
            # Count completed statuses
            completed_statuses = 0
            total_statuses = len(timeline)
            
            for status, days in timeline.items():
                if status == current_status or self._is_status_completed(case, status):
                    completed_statuses += 1
            
            return int((completed_statuses / total_statuses) * 100) if total_statuses > 0 else 0
            
        except Exception as e:
            logger.error(f"Error calculating progress percentage: {e}")
            return 0
    
    def _is_status_completed(self, case: Case, status: str) -> bool:
        """Check if a status is completed."""
        if not case.metadata or 'status_history' not in case.metadata:
            return False
        
        status_history = case.metadata['status_history']
        return any(entry['status'] == status for entry in status_history)
    
    def get_required_documents(self, form_type: str) -> Dict[str, Any]:
        """Get required documents for immigration form."""
        document_requirements = {
            'i485': [
                'Passport photos',
                'Birth certificate',
                'Marriage certificate (if applicable)',
                'Divorce decree (if applicable)',
                'Employment authorization document',
                'I-94 arrival/departure record',
                'Medical examination form (I-693)',
                'Affidavit of support (I-864)',
                'Tax returns (3 years)',
                'Bank statements',
                'Employment verification letter'
            ],
            'n400': [
                'Passport photos',
                'Green card (front and back)',
                'Birth certificate',
                'Marriage certificate (if applicable)',
                'Divorce decree (if applicable)',
                'Tax returns (5 years)',
                'Bank statements',
                'Employment verification letter',
                'Civics test study materials',
                'English proficiency documentation'
            ],
            'i130': [
                'Passport photos',
                'Birth certificate',
                'Marriage certificate',
                'Divorce decree (if applicable)',
                'Evidence of bona fide marriage',
                'Joint bank statements',
                'Joint tax returns',
                'Photos together',
                'Affidavits from friends/family',
                'Lease agreements'
            ]
        }
        
        return {
            'success': True,
            'form_type': form_type,
            'required_documents': document_requirements.get(form_type, [])
        }
    
    def get_immigration_statistics(self, attorney_id: int = None) -> Dict[str, Any]:
        """Get immigration case statistics."""
        try:
            query = Case.query.filter_by(case_type='immigration')
            if attorney_id:
                query = query.filter_by(attorney_id=attorney_id)
            
            cases = query.all()
            
            # Status breakdown
            status_counts = {}
            for case in cases:
                status = case.status
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Form type breakdown
            form_counts = {}
            for case in cases:
                if case.metadata and 'immigration_form' in case.metadata:
                    form = case.metadata['immigration_form']
                    form_counts[form] = form_counts.get(form, 0) + 1
            
            # Average processing time
            completed_cases = [c for c in cases if c.status in ['approved', 'denied', 'closed']]
            avg_processing_time = 0
            if completed_cases:
                total_days = sum([
                    (c.updated_at - c.created_at).days for c in completed_cases
                ])
                avg_processing_time = total_days / len(completed_cases)
            
            return {
                'success': True,
                'total_cases': len(cases),
                'status_counts': status_counts,
                'form_counts': form_counts,
                'average_processing_time_days': round(avg_processing_time, 1),
                'active_cases': len([c for c in cases if c.status not in ['approved', 'denied', 'closed']])
            }
            
        except Exception as e:
            logger.error(f"Error getting immigration statistics: {e}")
            return {'success': False, 'error': str(e)}

# Create singleton instance
immigration_workflow_service = ImmigrationWorkflowService()

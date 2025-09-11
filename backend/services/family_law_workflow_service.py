"""
Family Law Workflow Service for SmartProBono
Handles specialized workflows for family law cases.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from backend.database import db
from backend.models import Case, CourtDate, Document, Task, User
import logging
import json

logger = logging.getLogger(__name__)

class FamilyLawWorkflowService:
    """Service for managing family law case workflows."""
    
    def __init__(self):
        self.family_law_case_types = {
            'divorce': 'Divorce Proceedings',
            'custody': 'Child Custody',
            'support': 'Child Support',
            'alimony': 'Spousal Support/Alimony',
            'adoption': 'Adoption',
            'guardianship': 'Guardianship',
            'prenup': 'Prenuptial Agreement',
            'postnup': 'Postnuptial Agreement',
            'domestic_violence': 'Domestic Violence Protection',
            'paternity': 'Paternity Establishment',
            'visitation': 'Visitation Rights',
            'modification': 'Order Modification'
        }
        
        self.family_law_statuses = [
            'initial_consultation',
            'case_evaluation',
            'mediation_scheduled',
            'mediation_completed',
            'discovery_phase',
            'negotiation_phase',
            'court_filing',
            'court_hearing_scheduled',
            'court_hearing_completed',
            'judgment_pending',
            'judgment_entered',
            'appeal_filed',
            'case_closed'
        ]
        
        self.mediation_phases = [
            'intake_assessment',
            'pre_mediation_preparation',
            'mediation_session_1',
            'mediation_session_2',
            'mediation_session_3',
            'agreement_drafting',
            'agreement_review',
            'agreement_signed',
            'court_approval'
        ]
    
    def create_family_law_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new family law case with specialized workflow."""
        try:
            # Create base case
            case = Case(
                title=case_data['title'],
                description=case_data['description'],
                client_id=case_data['client_id'],
                attorney_id=case_data.get('attorney_id'),
                case_type='family_law',
                practice_area='family_law',
                priority=case_data.get('priority', 'medium'),
                status='initial_consultation',
                notes=case_data.get('notes', [])
            )
            
            db.session.add(case)
            db.session.commit()
            
            # Create family law-specific metadata
            family_metadata = {
                'case_subtype': case_data.get('case_subtype', 'divorce'),
                'current_status': 'initial_consultation',
                'parties_involved': case_data.get('parties_involved', []),
                'children_involved': case_data.get('children_involved', []),
                'marriage_date': case_data.get('marriage_date'),
                'separation_date': case_data.get('separation_date'),
                'assets_value': case_data.get('assets_value', 0),
                'debt_value': case_data.get('debt_value', 0),
                'mediation_required': case_data.get('mediation_required', True),
                'contested_issues': case_data.get('contested_issues', []),
                'timeline': self._create_family_law_timeline(case_data.get('case_subtype', 'divorce'))
            }
            
            case.metadata = family_metadata
            db.session.commit()
            
            # Create initial tasks
            self._create_initial_family_law_tasks(case)
            
            return {
                'success': True,
                'case': case.to_dict(),
                'workflow_created': True
            }
            
        except Exception as e:
            logger.error(f"Error creating family law case: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _create_family_law_timeline(self, case_subtype: str) -> Dict[str, Any]:
        """Create timeline based on family law case subtype."""
        timelines = {
            'divorce': {
                'initial_consultation': 0,
                'case_evaluation': 7,
                'mediation_scheduled': 14,
                'mediation_completed': 60,
                'discovery_phase': 90,
                'negotiation_phase': 120,
                'court_filing': 150,
                'court_hearing_scheduled': 180,
                'judgment_entered': 210,
                'case_closed': 240
            },
            'custody': {
                'initial_consultation': 0,
                'case_evaluation': 7,
                'mediation_scheduled': 14,
                'mediation_completed': 45,
                'discovery_phase': 75,
                'court_filing': 90,
                'court_hearing_scheduled': 120,
                'judgment_entered': 150,
                'case_closed': 180
            },
            'adoption': {
                'initial_consultation': 0,
                'case_evaluation': 14,
                'discovery_phase': 30,
                'court_filing': 60,
                'court_hearing_scheduled': 90,
                'judgment_entered': 120,
                'case_closed': 150
            },
            'domestic_violence': {
                'initial_consultation': 0,
                'case_evaluation': 1,
                'court_filing': 3,
                'court_hearing_scheduled': 7,
                'judgment_entered': 14,
                'case_closed': 30
            }
        }
        
        return timelines.get(case_subtype, timelines['divorce'])
    
    def _create_initial_family_law_tasks(self, case: Case):
        """Create initial tasks for family law case."""
        try:
            case_subtype = case.metadata.get('case_subtype', 'divorce')
            
            tasks = [
                {
                    'title': 'Initial Family Law Consultation',
                    'description': 'Conduct initial consultation to understand family dynamics and legal issues',
                    'task_type': 'consultation',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=3),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                },
                {
                    'title': 'Case Evaluation and Strategy',
                    'description': 'Evaluate case merits and develop legal strategy',
                    'task_type': 'case_evaluation',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=7),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                }
            ]
            
            # Add mediation task if required
            if case.metadata.get('mediation_required', True):
                tasks.append({
                    'title': 'Schedule Mediation',
                    'description': 'Schedule mediation session with opposing party',
                    'task_type': 'mediation_scheduling',
                    'priority': 'medium',
                    'due_date': datetime.utcnow() + timedelta(days=14),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                })
            
            # Add case-specific tasks
            if case_subtype == 'divorce':
                tasks.extend([
                    {
                        'title': 'Asset and Debt Analysis',
                        'description': 'Analyze marital assets and debts for equitable distribution',
                        'task_type': 'financial_analysis',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=21),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    },
                    {
                        'title': 'Child Custody Evaluation',
                        'description': 'Evaluate child custody arrangements and best interests',
                        'task_type': 'custody_evaluation',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=28),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    }
                ])
            elif case_subtype == 'custody':
                tasks.append({
                    'title': 'Child Custody Investigation',
                    'description': 'Investigate child custody factors and living arrangements',
                    'task_type': 'custody_investigation',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=21),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                })
            
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
            logger.error(f"Error creating initial family law tasks: {e}")
    
    def update_family_law_status(self, case_id: int, new_status: str, notes: str = None) -> Dict[str, Any]:
        """Update family law case status."""
        try:
            case = Case.query.get(case_id)
            if not case or case.case_type != 'family_law':
                return {'success': False, 'error': 'Family law case not found'}
            
            if new_status not in self.family_law_statuses:
                return {'success': False, 'error': 'Invalid family law status'}
            
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
            logger.error(f"Error updating family law status: {e}")
            return {'success': False, 'error': str(e)}
    
    def _create_status_specific_tasks(self, case: Case, status: str):
        """Create tasks specific to family law status."""
        try:
            task_templates = {
                'mediation_scheduled': {
                    'title': 'Prepare for Mediation',
                    'description': 'Prepare client and gather documents for mediation session',
                    'task_type': 'mediation_prep',
                    'priority': 'high',
                    'due_days': 3
                },
                'discovery_phase': {
                    'title': 'Conduct Discovery',
                    'description': 'Gather evidence and conduct discovery process',
                    'task_type': 'discovery',
                    'priority': 'high',
                    'due_days': 30
                },
                'negotiation_phase': {
                    'title': 'Negotiate Settlement',
                    'description': 'Negotiate settlement terms with opposing counsel',
                    'task_type': 'negotiation',
                    'priority': 'high',
                    'due_days': 21
                },
                'court_filing': {
                    'title': 'File Court Documents',
                    'description': 'Prepare and file necessary court documents',
                    'task_type': 'court_filing',
                    'priority': 'high',
                    'due_days': 7
                },
                'court_hearing_scheduled': {
                    'title': 'Prepare for Court Hearing',
                    'description': 'Prepare client and evidence for court hearing',
                    'task_type': 'hearing_prep',
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
    
    def get_family_law_case_types(self) -> Dict[str, Any]:
        """Get available family law case types."""
        return {
            'success': True,
            'case_types': self.family_law_case_types
        }
    
    def get_family_law_statuses(self) -> Dict[str, Any]:
        """Get available family law statuses."""
        return {
            'success': True,
            'statuses': self.family_law_statuses
        }
    
    def get_required_documents(self, case_subtype: str) -> Dict[str, Any]:
        """Get required documents for family law case type."""
        document_requirements = {
            'divorce': [
                'Marriage certificate',
                'Birth certificates (children)',
                'Financial statements',
                'Tax returns (3 years)',
                'Bank statements',
                'Property deeds',
                'Vehicle titles',
                'Retirement account statements',
                'Insurance policies',
                'Credit card statements',
                'Loan documents',
                'Employment verification',
                'Pay stubs',
                'Business records (if applicable)',
                'Prenuptial agreement (if applicable)'
            ],
            'custody': [
                'Birth certificates (children)',
                'School records',
                'Medical records (children)',
                'Daycare records',
                'Photos with children',
                'Communication records',
                'Witness statements',
                'Police reports (if applicable)',
                'Drug test results (if applicable)',
                'Mental health records (if applicable)'
            ],
            'adoption': [
                'Birth certificates',
                'Marriage certificate (if married)',
                'Financial statements',
                'Employment verification',
                'Background check results',
                'Home study report',
                'Medical examinations',
                'Reference letters',
                'Criminal background check',
                'Child abuse clearance'
            ],
            'domestic_violence': [
                'Incident reports',
                'Police reports',
                'Medical records',
                'Photos of injuries',
                'Witness statements',
                'Text messages/emails',
                'Restraining order history',
                'Court records',
                '911 call records',
                'Hospital records'
            ]
        }
        
        return {
            'success': True,
            'case_subtype': case_subtype,
            'required_documents': document_requirements.get(case_subtype, [])
        }
    
    def get_family_law_statistics(self, attorney_id: int = None) -> Dict[str, Any]:
        """Get family law case statistics."""
        try:
            query = Case.query.filter_by(case_type='family_law')
            if attorney_id:
                query = query.filter_by(attorney_id=attorney_id)
            
            cases = query.all()
            
            # Status breakdown
            status_counts = {}
            for case in cases:
                status = case.status
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Case subtype breakdown
            subtype_counts = {}
            for case in cases:
                if case.metadata and 'case_subtype' in case.metadata:
                    subtype = case.metadata['case_subtype']
                    subtype_counts[subtype] = subtype_counts.get(subtype, 0) + 1
            
            # Mediation statistics
            mediation_cases = [c for c in cases if c.metadata and c.metadata.get('mediation_required', False)]
            mediation_success_rate = 0
            if mediation_cases:
                successful_mediations = len([c for c in mediation_cases if c.status in ['mediation_completed', 'case_closed']])
                mediation_success_rate = (successful_mediations / len(mediation_cases)) * 100
            
            # Average processing time
            completed_cases = [c for c in cases if c.status in ['case_closed', 'judgment_entered']]
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
                'subtype_counts': subtype_counts,
                'mediation_cases': len(mediation_cases),
                'mediation_success_rate': round(mediation_success_rate, 1),
                'average_processing_time_days': round(avg_processing_time, 1),
                'active_cases': len([c for c in cases if c.status not in ['case_closed', 'judgment_entered']])
            }
            
        except Exception as e:
            logger.error(f"Error getting family law statistics: {e}")
            return {'success': False, 'error': str(e)}

# Create singleton instance
family_law_workflow_service = FamilyLawWorkflowService()

"""
Criminal Defense Workflow Service for SmartProBono
Handles specialized workflows for criminal defense cases.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from backend.database import db
from backend.models import Case, CourtDate, Document, Task, User
import logging
import json

logger = logging.getLogger(__name__)

class CriminalDefenseWorkflowService:
    """Service for managing criminal defense case workflows."""
    
    def __init__(self):
        self.criminal_case_types = {
            'misdemeanor': 'Misdemeanor',
            'felony': 'Felony',
            'dui': 'DUI/DWI',
            'drug_possession': 'Drug Possession',
            'drug_trafficking': 'Drug Trafficking',
            'theft': 'Theft/Larceny',
            'burglary': 'Burglary',
            'assault': 'Assault',
            'domestic_violence': 'Domestic Violence',
            'white_collar': 'White Collar Crime',
            'traffic_violation': 'Traffic Violation',
            'probation_violation': 'Probation Violation',
            'parole_violation': 'Parole Violation',
            'appeal': 'Criminal Appeal'
        }
        
        self.criminal_statuses = [
            'initial_arrest',
            'bail_set',
            'arraignment_scheduled',
            'arraignment_completed',
            'discovery_phase',
            'investigation_phase',
            'plea_negotiation',
            'plea_agreement',
            'trial_preparation',
            'trial_scheduled',
            'trial_in_progress',
            'trial_completed',
            'sentencing_scheduled',
            'sentencing_completed',
            'appeal_filed',
            'case_closed'
        ]
        
        self.charge_severities = {
            'infraction': 'Infraction (Fine only)',
            'misdemeanor_class_c': 'Misdemeanor Class C (Fine up to $500)',
            'misdemeanor_class_b': 'Misdemeanor Class B (Fine up to $2,000, Jail up to 180 days)',
            'misdemeanor_class_a': 'Misdemeanor Class A (Fine up to $4,000, Jail up to 1 year)',
            'felony_3rd_degree': 'Felony 3rd Degree (2-10 years prison)',
            'felony_2nd_degree': 'Felony 2nd Degree (2-20 years prison)',
            'felony_1st_degree': 'Felony 1st Degree (5-99 years or life)',
            'capital_felony': 'Capital Felony (Life or Death Penalty)'
        }
    
    def create_criminal_defense_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new criminal defense case with specialized workflow."""
        try:
            # Create base case
            case = Case(
                title=case_data['title'],
                description=case_data['description'],
                client_id=case_data['client_id'],
                attorney_id=case_data.get('attorney_id'),
                case_type='criminal_defense',
                practice_area='criminal_defense',
                priority=self._determine_priority(case_data.get('charge_severity', 'misdemeanor_class_c')),
                status='initial_arrest',
                notes=case_data.get('notes', [])
            )
            
            db.session.add(case)
            db.session.commit()
            
            # Create criminal defense-specific metadata
            criminal_metadata = {
                'case_subtype': case_data.get('case_subtype', 'misdemeanor'),
                'current_status': 'initial_arrest',
                'charges': case_data.get('charges', []),
                'charge_severity': case_data.get('charge_severity', 'misdemeanor_class_c'),
                'arrest_date': case_data.get('arrest_date'),
                'arrest_location': case_data.get('arrest_location'),
                'arresting_officer': case_data.get('arresting_officer'),
                'case_number': case_data.get('case_number'),
                'bail_amount': case_data.get('bail_amount', 0),
                'bail_paid': case_data.get('bail_paid', False),
                'court_jurisdiction': case_data.get('court_jurisdiction'),
                'prosecutor': case_data.get('prosecutor'),
                'witnesses': case_data.get('witnesses', []),
                'evidence_items': case_data.get('evidence_items', []),
                'criminal_history': case_data.get('criminal_history', []),
                'timeline': self._create_criminal_defense_timeline(case_data.get('case_subtype', 'misdemeanor'))
            }
            
            case.metadata = criminal_metadata
            db.session.commit()
            
            # Create initial tasks
            self._create_initial_criminal_defense_tasks(case)
            
            return {
                'success': True,
                'case': case.to_dict(),
                'workflow_created': True
            }
            
        except Exception as e:
            logger.error(f"Error creating criminal defense case: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _determine_priority(self, charge_severity: str) -> str:
        """Determine case priority based on charge severity."""
        if charge_severity in ['capital_felony', 'felony_1st_degree']:
            return 'urgent'
        elif charge_severity in ['felony_2nd_degree', 'felony_3rd_degree']:
            return 'high'
        elif charge_severity in ['misdemeanor_class_a', 'misdemeanor_class_b']:
            return 'medium'
        else:
            return 'low'
    
    def _create_criminal_defense_timeline(self, case_subtype: str) -> Dict[str, Any]:
        """Create timeline based on criminal case subtype."""
        timelines = {
            'misdemeanor': {
                'initial_arrest': 0,
                'bail_set': 1,
                'arraignment_scheduled': 3,
                'arraignment_completed': 7,
                'discovery_phase': 14,
                'plea_negotiation': 30,
                'trial_preparation': 45,
                'trial_scheduled': 60,
                'trial_completed': 75,
                'sentencing_completed': 90,
                'case_closed': 105
            },
            'felony': {
                'initial_arrest': 0,
                'bail_set': 1,
                'arraignment_scheduled': 3,
                'arraignment_completed': 7,
                'discovery_phase': 30,
                'investigation_phase': 60,
                'plea_negotiation': 90,
                'trial_preparation': 120,
                'trial_scheduled': 180,
                'trial_completed': 210,
                'sentencing_completed': 240,
                'case_closed': 270
            },
            'dui': {
                'initial_arrest': 0,
                'bail_set': 1,
                'arraignment_scheduled': 7,
                'arraignment_completed': 14,
                'discovery_phase': 21,
                'plea_negotiation': 30,
                'trial_preparation': 45,
                'trial_scheduled': 60,
                'trial_completed': 75,
                'sentencing_completed': 90,
                'case_closed': 105
            }
        }
        
        return timelines.get(case_subtype, timelines['misdemeanor'])
    
    def _create_initial_criminal_defense_tasks(self, case: Case):
        """Create initial tasks for criminal defense case."""
        try:
            case_subtype = case.metadata.get('case_subtype', 'misdemeanor')
            charge_severity = case.metadata.get('charge_severity', 'misdemeanor_class_c')
            
            tasks = [
                {
                    'title': 'Initial Client Interview',
                    'description': 'Conduct detailed interview with client about charges and circumstances',
                    'task_type': 'client_interview',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=1),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                },
                {
                    'title': 'Bail Hearing Preparation',
                    'description': 'Prepare for bail hearing and gather supporting evidence',
                    'task_type': 'bail_preparation',
                    'priority': 'urgent' if charge_severity in ['capital_felony', 'felony_1st_degree'] else 'high',
                    'due_date': datetime.utcnow() + timedelta(days=2),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                },
                {
                    'title': 'Arraignment Preparation',
                    'description': 'Prepare client for arraignment and plea entry',
                    'task_type': 'arraignment_prep',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=5),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                }
            ]
            
            # Add case-specific tasks
            if case_subtype == 'dui':
                tasks.extend([
                    {
                        'title': 'DUI Investigation',
                        'description': 'Investigate DUI arrest circumstances and evidence',
                        'task_type': 'dui_investigation',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=7),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    },
                    {
                        'title': 'Breathalyzer Analysis',
                        'description': 'Analyze breathalyzer test results and procedures',
                        'task_type': 'evidence_analysis',
                        'priority': 'medium',
                        'due_date': datetime.utcnow() + timedelta(days=10),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    }
                ])
            elif case_subtype == 'felony':
                tasks.extend([
                    {
                        'title': 'Felony Investigation',
                        'description': 'Conduct comprehensive investigation of felony charges',
                        'task_type': 'felony_investigation',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=14),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    },
                    {
                        'title': 'Expert Witness Consultation',
                        'description': 'Consult with relevant expert witnesses',
                        'task_type': 'expert_consultation',
                        'priority': 'medium',
                        'due_date': datetime.utcnow() + timedelta(days=21),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    }
                ])
            
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
            logger.error(f"Error creating initial criminal defense tasks: {e}")
    
    def update_criminal_defense_status(self, case_id: int, new_status: str, notes: str = None) -> Dict[str, Any]:
        """Update criminal defense case status."""
        try:
            case = Case.query.get(case_id)
            if not case or case.case_type != 'criminal_defense':
                return {'success': False, 'error': 'Criminal defense case not found'}
            
            if new_status not in self.criminal_statuses:
                return {'success': False, 'error': 'Invalid criminal defense status'}
            
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
            logger.error(f"Error updating criminal defense status: {e}")
            return {'success': False, 'error': str(e)}
    
    def _create_status_specific_tasks(self, case: Case, status: str):
        """Create tasks specific to criminal defense status."""
        try:
            task_templates = {
                'discovery_phase': {
                    'title': 'Conduct Discovery',
                    'description': 'Request and review discovery materials from prosecution',
                    'task_type': 'discovery',
                    'priority': 'high',
                    'due_days': 14
                },
                'investigation_phase': {
                    'title': 'Case Investigation',
                    'description': 'Conduct independent investigation of charges',
                    'task_type': 'investigation',
                    'priority': 'high',
                    'due_days': 30
                },
                'plea_negotiation': {
                    'title': 'Plea Negotiation',
                    'description': 'Negotiate plea agreement with prosecution',
                    'task_type': 'plea_negotiation',
                    'priority': 'high',
                    'due_days': 21
                },
                'trial_preparation': {
                    'title': 'Trial Preparation',
                    'description': 'Prepare for trial including witness preparation and evidence review',
                    'task_type': 'trial_prep',
                    'priority': 'high',
                    'due_days': 14
                },
                'trial_scheduled': {
                    'title': 'Final Trial Preparation',
                    'description': 'Final preparation for trial including strategy review',
                    'task_type': 'trial_prep',
                    'priority': 'urgent',
                    'due_days': 3
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
    
    def get_criminal_case_types(self) -> Dict[str, Any]:
        """Get available criminal case types."""
        return {
            'success': True,
            'case_types': self.criminal_case_types
        }
    
    def get_criminal_statuses(self) -> Dict[str, Any]:
        """Get available criminal defense statuses."""
        return {
            'success': True,
            'statuses': self.criminal_statuses
        }
    
    def get_charge_severities(self) -> Dict[str, Any]:
        """Get available charge severities."""
        return {
            'success': True,
            'severities': self.charge_severities
        }
    
    def get_required_documents(self, case_subtype: str) -> Dict[str, Any]:
        """Get required documents for criminal defense case type."""
        document_requirements = {
            'misdemeanor': [
                'Arrest report',
                'Complaint/Information',
                'Bail bond documents',
                'Court appearance notices',
                'Police reports',
                'Witness statements',
                'Evidence photos',
                'Medical records (if applicable)',
                'Employment verification',
                'Character references'
            ],
            'felony': [
                'Arrest report',
                'Indictment/Information',
                'Bail bond documents',
                'Court appearance notices',
                'Police reports',
                'Witness statements',
                'Evidence photos',
                'Forensic reports',
                'Expert witness reports',
                'Medical records',
                'Employment verification',
                'Character references',
                'Criminal history records',
                'Probation/parole records'
            ],
            'dui': [
                'Arrest report',
                'Complaint/Information',
                'Bail bond documents',
                'Breathalyzer test results',
                'Field sobriety test results',
                'Blood alcohol test results',
                'Police dash cam footage',
                'Body cam footage',
                'Witness statements',
                'Medical records',
                'DMV records',
                'Driving record',
                'Insurance records'
            ],
            'domestic_violence': [
                'Arrest report',
                'Complaint/Information',
                'Bail bond documents',
                'Protection order',
                'Police reports',
                'Witness statements',
                'Medical records',
                'Photos of injuries',
                '911 call records',
                'Text messages/emails',
                'Social media evidence',
                'Character references'
            ]
        }
        
        return {
            'success': True,
            'case_subtype': case_subtype,
            'required_documents': document_requirements.get(case_subtype, [])
        }
    
    def get_criminal_defense_statistics(self, attorney_id: int = None) -> Dict[str, Any]:
        """Get criminal defense case statistics."""
        try:
            query = Case.query.filter_by(case_type='criminal_defense')
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
            
            # Charge severity breakdown
            severity_counts = {}
            for case in cases:
                if case.metadata and 'charge_severity' in case.metadata:
                    severity = case.metadata['charge_severity']
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Plea agreement statistics
            plea_cases = [c for c in cases if c.status in ['plea_agreement', 'case_closed']]
            plea_success_rate = 0
            if plea_cases:
                successful_pleas = len([c for c in plea_cases if c.status == 'plea_agreement'])
                plea_success_rate = (successful_pleas / len(plea_cases)) * 100
            
            # Average processing time
            completed_cases = [c for c in cases if c.status in ['case_closed', 'sentencing_completed']]
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
                'severity_counts': severity_counts,
                'plea_cases': len(plea_cases),
                'plea_success_rate': round(plea_success_rate, 1),
                'average_processing_time_days': round(avg_processing_time, 1),
                'active_cases': len([c for c in cases if c.status not in ['case_closed', 'sentencing_completed']])
            }
            
        except Exception as e:
            logger.error(f"Error getting criminal defense statistics: {e}")
            return {'success': False, 'error': str(e)}

# Create singleton instance
criminal_defense_workflow_service = CriminalDefenseWorkflowService()

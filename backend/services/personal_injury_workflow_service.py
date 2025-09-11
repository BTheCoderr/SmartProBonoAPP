"""
Personal Injury Workflow Service for SmartProBono
Handles specialized workflows for personal injury cases.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from backend.database import db
from backend.models import Case, CourtDate, Document, Task, User
import logging
import json

logger = logging.getLogger(__name__)

class PersonalInjuryWorkflowService:
    """Service for managing personal injury case workflows."""
    
    def __init__(self):
        self.personal_injury_case_types = {
            'car_accident': 'Car Accident',
            'motorcycle_accident': 'Motorcycle Accident',
            'truck_accident': 'Truck Accident',
            'pedestrian_accident': 'Pedestrian Accident',
            'bicycle_accident': 'Bicycle Accident',
            'slip_fall': 'Slip and Fall',
            'medical_malpractice': 'Medical Malpractice',
            'product_liability': 'Product Liability',
            'premises_liability': 'Premises Liability',
            'workplace_injury': 'Workplace Injury',
            'dog_bite': 'Dog Bite',
            'wrongful_death': 'Wrongful Death',
            'nursing_home_abuse': 'Nursing Home Abuse',
            'defective_drug': 'Defective Drug/Medical Device'
        }
        
        self.personal_injury_statuses = [
            'initial_consultation',
            'case_evaluation',
            'investigation_phase',
            'medical_treatment',
            'medical_clearance',
            'demand_letter',
            'settlement_negotiation',
            'litigation_filed',
            'discovery_phase',
            'mediation_scheduled',
            'mediation_completed',
            'trial_preparation',
            'trial_scheduled',
            'trial_completed',
            'settlement_reached',
            'case_closed'
        ]
        
        self.injury_types = {
            'soft_tissue': 'Soft Tissue Injuries',
            'broken_bones': 'Broken Bones/Fractures',
            'head_injury': 'Head Injury/Traumatic Brain Injury',
            'spinal_injury': 'Spinal Cord Injury',
            'burn_injury': 'Burn Injuries',
            'amputation': 'Amputation',
            'internal_injury': 'Internal Injuries',
            'emotional_distress': 'Emotional Distress',
            'death': 'Wrongful Death'
        }
    
    def create_personal_injury_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new personal injury case with specialized workflow."""
        try:
            # Create base case
            case = Case(
                title=case_data['title'],
                description=case_data['description'],
                client_id=case_data['client_id'],
                attorney_id=case_data.get('attorney_id'),
                case_type='personal_injury',
                practice_area='personal_injury',
                priority=self._determine_priority(case_data.get('injury_severity', 'moderate')),
                status='initial_consultation',
                notes=case_data.get('notes', [])
            )
            
            db.session.add(case)
            db.session.commit()
            
            # Create personal injury-specific metadata
            pi_metadata = {
                'case_subtype': case_data.get('case_subtype', 'car_accident'),
                'current_status': 'initial_consultation',
                'incident_date': case_data.get('incident_date'),
                'incident_location': case_data.get('incident_location'),
                'injury_types': case_data.get('injury_types', []),
                'injury_severity': case_data.get('injury_severity', 'moderate'),
                'medical_treatment': case_data.get('medical_treatment', []),
                'medical_providers': case_data.get('medical_providers', []),
                'insurance_companies': case_data.get('insurance_companies', []),
                'at_fault_party': case_data.get('at_fault_party'),
                'witnesses': case_data.get('witnesses', []),
                'police_report': case_data.get('police_report'),
                'property_damage': case_data.get('property_damage', 0),
                'lost_wages': case_data.get('lost_wages', 0),
                'medical_expenses': case_data.get('medical_expenses', 0),
                'pain_suffering': case_data.get('pain_suffering', 0),
                'timeline': self._create_personal_injury_timeline(case_data.get('case_subtype', 'car_accident'))
            }
            
            case.metadata = pi_metadata
            db.session.commit()
            
            # Create initial tasks
            self._create_initial_personal_injury_tasks(case)
            
            return {
                'success': True,
                'case': case.to_dict(),
                'workflow_created': True
            }
            
        except Exception as e:
            logger.error(f"Error creating personal injury case: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _determine_priority(self, injury_severity: str) -> str:
        """Determine case priority based on injury severity."""
        if injury_severity in ['severe', 'catastrophic', 'death']:
            return 'urgent'
        elif injury_severity in ['moderate', 'significant']:
            return 'high'
        else:
            return 'medium'
    
    def _create_personal_injury_timeline(self, case_subtype: str) -> Dict[str, Any]:
        """Create timeline based on personal injury case subtype."""
        timelines = {
            'car_accident': {
                'initial_consultation': 0,
                'case_evaluation': 7,
                'investigation_phase': 14,
                'medical_treatment': 30,
                'medical_clearance': 90,
                'demand_letter': 120,
                'settlement_negotiation': 150,
                'litigation_filed': 180,
                'discovery_phase': 240,
                'mediation_scheduled': 300,
                'trial_scheduled': 360,
                'settlement_reached': 420,
                'case_closed': 450
            },
            'medical_malpractice': {
                'initial_consultation': 0,
                'case_evaluation': 14,
                'investigation_phase': 30,
                'medical_treatment': 60,
                'medical_clearance': 120,
                'demand_letter': 180,
                'settlement_negotiation': 240,
                'litigation_filed': 300,
                'discovery_phase': 420,
                'mediation_scheduled': 540,
                'trial_scheduled': 720,
                'settlement_reached': 900,
                'case_closed': 1080
            },
            'slip_fall': {
                'initial_consultation': 0,
                'case_evaluation': 7,
                'investigation_phase': 14,
                'medical_treatment': 30,
                'medical_clearance': 90,
                'demand_letter': 120,
                'settlement_negotiation': 150,
                'litigation_filed': 180,
                'discovery_phase': 240,
                'mediation_scheduled': 300,
                'trial_scheduled': 360,
                'settlement_reached': 420,
                'case_closed': 450
            }
        }
        
        return timelines.get(case_subtype, timelines['car_accident'])
    
    def _create_initial_personal_injury_tasks(self, case: Case):
        """Create initial tasks for personal injury case."""
        try:
            case_subtype = case.metadata.get('case_subtype', 'car_accident')
            injury_severity = case.metadata.get('injury_severity', 'moderate')
            
            tasks = [
                {
                    'title': 'Initial Personal Injury Consultation',
                    'description': 'Conduct detailed consultation about incident and injuries',
                    'task_type': 'consultation',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=3),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                },
                {
                    'title': 'Case Evaluation and Merit Assessment',
                    'description': 'Evaluate case merits and potential damages',
                    'task_type': 'case_evaluation',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=7),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                },
                {
                    'title': 'Incident Investigation',
                    'description': 'Investigate incident circumstances and gather evidence',
                    'task_type': 'investigation',
                    'priority': 'high',
                    'due_date': datetime.utcnow() + timedelta(days=14),
                    'case_id': case.id,
                    'assigned_to': case.attorney_id
                }
            ]
            
            # Add case-specific tasks
            if case_subtype == 'car_accident':
                tasks.extend([
                    {
                        'title': 'Accident Scene Investigation',
                        'description': 'Investigate accident scene and gather evidence',
                        'task_type': 'scene_investigation',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=10),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    },
                    {
                        'title': 'Insurance Coverage Analysis',
                        'description': 'Analyze insurance coverage and policy limits',
                        'task_type': 'insurance_analysis',
                        'priority': 'medium',
                        'due_date': datetime.utcnow() + timedelta(days=21),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    }
                ])
            elif case_subtype == 'medical_malpractice':
                tasks.extend([
                    {
                        'title': 'Medical Records Review',
                        'description': 'Review medical records and treatment history',
                        'task_type': 'medical_review',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=21),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    },
                    {
                        'title': 'Expert Medical Consultation',
                        'description': 'Consult with medical experts for case evaluation',
                        'task_type': 'expert_consultation',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=45),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    }
                ])
            elif case_subtype == 'slip_fall':
                tasks.extend([
                    {
                        'title': 'Premises Investigation',
                        'description': 'Investigate premises conditions and safety violations',
                        'task_type': 'premises_investigation',
                        'priority': 'high',
                        'due_date': datetime.utcnow() + timedelta(days=10),
                        'case_id': case.id,
                        'assigned_to': case.attorney_id
                    },
                    {
                        'title': 'Property Owner Liability Analysis',
                        'description': 'Analyze property owner liability and insurance coverage',
                        'task_type': 'liability_analysis',
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
            logger.error(f"Error creating initial personal injury tasks: {e}")
    
    def update_personal_injury_status(self, case_id: int, new_status: str, notes: str = None) -> Dict[str, Any]:
        """Update personal injury case status."""
        try:
            case = Case.query.get(case_id)
            if not case or case.case_type != 'personal_injury':
                return {'success': False, 'error': 'Personal injury case not found'}
            
            if new_status not in self.personal_injury_statuses:
                return {'success': False, 'error': 'Invalid personal injury status'}
            
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
            logger.error(f"Error updating personal injury status: {e}")
            return {'success': False, 'error': str(e)}
    
    def _create_status_specific_tasks(self, case: Case, status: str):
        """Create tasks specific to personal injury status."""
        try:
            task_templates = {
                'medical_treatment': {
                    'title': 'Monitor Medical Treatment',
                    'description': 'Monitor client medical treatment and progress',
                    'task_type': 'medical_monitoring',
                    'priority': 'high',
                    'due_days': 7
                },
                'demand_letter': {
                    'title': 'Prepare Demand Letter',
                    'description': 'Prepare and send demand letter to insurance company',
                    'task_type': 'demand_letter',
                    'priority': 'high',
                    'due_days': 14
                },
                'settlement_negotiation': {
                    'title': 'Settlement Negotiation',
                    'description': 'Negotiate settlement with insurance company',
                    'task_type': 'settlement_negotiation',
                    'priority': 'high',
                    'due_days': 21
                },
                'litigation_filed': {
                    'title': 'File Lawsuit',
                    'description': 'File personal injury lawsuit in court',
                    'task_type': 'litigation_filing',
                    'priority': 'high',
                    'due_days': 7
                },
                'discovery_phase': {
                    'title': 'Conduct Discovery',
                    'description': 'Conduct discovery process including depositions',
                    'task_type': 'discovery',
                    'priority': 'high',
                    'due_days': 30
                },
                'mediation_scheduled': {
                    'title': 'Prepare for Mediation',
                    'description': 'Prepare client and case for mediation',
                    'task_type': 'mediation_prep',
                    'priority': 'high',
                    'due_days': 7
                },
                'trial_preparation': {
                    'title': 'Trial Preparation',
                    'description': 'Prepare for trial including witness preparation',
                    'task_type': 'trial_prep',
                    'priority': 'high',
                    'due_days': 14
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
    
    def get_personal_injury_case_types(self) -> Dict[str, Any]:
        """Get available personal injury case types."""
        return {
            'success': True,
            'case_types': self.personal_injury_case_types
        }
    
    def get_personal_injury_statuses(self) -> Dict[str, Any]:
        """Get available personal injury statuses."""
        return {
            'success': True,
            'statuses': self.personal_injury_statuses
        }
    
    def get_injury_types(self) -> Dict[str, Any]:
        """Get available injury types."""
        return {
            'success': True,
            'injury_types': self.injury_types
        }
    
    def get_required_documents(self, case_subtype: str) -> Dict[str, Any]:
        """Get required documents for personal injury case type."""
        document_requirements = {
            'car_accident': [
                'Police report',
                'Accident photos',
                'Vehicle damage photos',
                'Medical records',
                'Medical bills',
                'Insurance correspondence',
                'Witness statements',
                'Repair estimates',
                'Lost wage documentation',
                'Employment records',
                'Tax returns',
                'Bank statements'
            ],
            'medical_malpractice': [
                'Medical records',
                'Medical bills',
                'Expert medical opinions',
                'Hospital records',
                'Surgical reports',
                'Lab results',
                'Imaging studies',
                'Prescription records',
                'Insurance correspondence',
                'Lost wage documentation',
                'Employment records'
            ],
            'slip_fall': [
                'Incident photos',
                'Property inspection reports',
                'Maintenance records',
                'Security footage',
                'Witness statements',
                'Medical records',
                'Medical bills',
                'Lost wage documentation',
                'Employment records',
                'Insurance correspondence'
            ],
            'workplace_injury': [
                'Workers compensation claim',
                'Incident report',
                'Medical records',
                'Medical bills',
                'Lost wage documentation',
                'Employment records',
                'Safety inspection reports',
                'OSHA reports',
                'Witness statements',
                'Insurance correspondence'
            ]
        }
        
        return {
            'success': True,
            'case_subtype': case_subtype,
            'required_documents': document_requirements.get(case_subtype, [])
        }
    
    def calculate_case_value(self, case_id: int) -> Dict[str, Any]:
        """Calculate estimated case value based on damages."""
        try:
            case = Case.query.get(case_id)
            if not case or case.case_type != 'personal_injury':
                return {'success': False, 'error': 'Personal injury case not found'}
            
            if not case.metadata:
                return {'success': False, 'error': 'Case metadata not found'}
            
            # Get damage components
            property_damage = case.metadata.get('property_damage', 0)
            lost_wages = case.metadata.get('lost_wages', 0)
            medical_expenses = case.metadata.get('medical_expenses', 0)
            pain_suffering = case.metadata.get('pain_suffering', 0)
            injury_severity = case.metadata.get('injury_severity', 'moderate')
            
            # Calculate economic damages
            economic_damages = property_damage + lost_wages + medical_expenses
            
            # Calculate non-economic damages (pain and suffering multiplier)
            severity_multipliers = {
                'minor': 1.5,
                'moderate': 2.0,
                'significant': 3.0,
                'severe': 4.0,
                'catastrophic': 5.0,
                'death': 6.0
            }
            
            multiplier = severity_multipliers.get(injury_severity, 2.0)
            non_economic_damages = medical_expenses * multiplier
            
            # Total estimated value
            total_value = economic_damages + non_economic_damages
            
            return {
                'success': True,
                'economic_damages': economic_damages,
                'non_economic_damages': non_economic_damages,
                'total_estimated_value': total_value,
                'injury_severity': injury_severity,
                'multiplier_used': multiplier
            }
            
        except Exception as e:
            logger.error(f"Error calculating case value: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_personal_injury_statistics(self, attorney_id: int = None) -> Dict[str, Any]:
        """Get personal injury case statistics."""
        try:
            query = Case.query.filter_by(case_type='personal_injury')
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
            
            # Settlement statistics
            settled_cases = [c for c in cases if c.status in ['settlement_reached', 'case_closed']]
            settlement_rate = 0
            if cases:
                settlement_rate = (len(settled_cases) / len(cases)) * 100
            
            # Average case value
            total_value = 0
            cases_with_value = 0
            for case in cases:
                if case.metadata and 'property_damage' in case.metadata:
                    value = case.metadata.get('property_damage', 0) + \
                           case.metadata.get('lost_wages', 0) + \
                           case.metadata.get('medical_expenses', 0)
                    total_value += value
                    cases_with_value += 1
            
            avg_case_value = total_value / cases_with_value if cases_with_value > 0 else 0
            
            # Average processing time
            completed_cases = [c for c in cases if c.status in ['case_closed', 'settlement_reached']]
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
                'settlement_rate': round(settlement_rate, 1),
                'average_case_value': round(avg_case_value, 2),
                'average_processing_time_days': round(avg_processing_time, 1),
                'active_cases': len([c for c in cases if c.status not in ['case_closed', 'settlement_reached']])
            }
            
        except Exception as e:
            logger.error(f"Error getting personal injury statistics: {e}")
            return {'success': False, 'error': str(e)}

# Create singleton instance
personal_injury_workflow_service = PersonalInjuryWorkflowService()

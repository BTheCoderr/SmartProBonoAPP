"""
Client intake model for the SmartProBono application.
Handles the complete client intake process from initial contact to case assignment.
"""
from datetime import datetime
from database import db
import json

class ClientIntake(db.Model):
    """Client intake model for storing intake information."""
    __tablename__ = 'client_intakes'
    __table_args__ = {'extend_existing': True}
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Can be null for anonymous intakes
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    
    # Address Information
    street_address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), default='USA')
    
    # Legal Information
    legal_issue_type = db.Column(db.String(100), nullable=False)  # immigration, family, criminal, civil, etc.
    case_description = db.Column(db.Text, nullable=False)
    urgency_level = db.Column(db.String(20), default='medium')  # low, medium, high, emergency
    
    # Financial Information
    income_level = db.Column(db.String(50), nullable=True)  # low, medium, high
    can_afford_legal_fees = db.Column(db.Boolean, nullable=True)
    needs_pro_bono = db.Column(db.Boolean, default=False)
    
    # Case Details
    case_start_date = db.Column(db.Date, nullable=True)  # When the legal issue started
    previous_legal_representation = db.Column(db.Boolean, default=False)
    previous_attorney_name = db.Column(db.String(255), nullable=True)
    
    # Status and Processing
    status = db.Column(db.String(50), default='submitted')  # submitted, under_review, assigned, rejected, completed
    assigned_lawyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_paralegal_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # AI Analysis Results
    ai_analysis = db.Column(db.Text, nullable=True)  # JSON string with AI analysis
    recommended_actions = db.Column(db.Text, nullable=True)  # JSON string with recommendations
    risk_assessment = db.Column(db.String(20), nullable=True)  # low, medium, high
    
    # Dates
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    assigned_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional Information
    notes = db.Column(db.Text, nullable=True)
    _metadata = db.Column('metadata', db.Text, nullable=True)  # JSON for additional data
    _documents = db.Column('documents', db.Text, nullable=True)  # JSON array of document IDs
    
    @property
    def intake_metadata(self):
        """Get intake metadata as a dictionary."""
        if not self._metadata:
            return {}
        return json.loads(self._metadata)
        
    @intake_metadata.setter
    def intake_metadata(self, value):
        """Set intake metadata from a dictionary."""
        if isinstance(value, dict):
            self._metadata = json.dumps(value)
        else:
            self._metadata = None
    
    @property
    def documents(self):
        """Get associated document IDs as a list."""
        if not self._documents:
            return []
        return json.loads(self._documents)
        
    @documents.setter
    def documents(self, value):
        """Set associated document IDs from a list."""
        if isinstance(value, list):
            self._documents = json.dumps(value)
        else:
            self._documents = None
    
    def add_document(self, document_id):
        """Add a document ID to the intake."""
        current_docs = self.documents
        if document_id not in current_docs:
            current_docs.append(document_id)
            self.documents = current_docs
    
    def get_full_name(self):
        """Get the client's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def get_full_address(self):
        """Get the client's full address."""
        address_parts = [self.street_address, self.city, self.state, self.zip_code]
        return ", ".join([part for part in address_parts if part])
    
    def to_dict(self):
        """Convert intake to a dictionary."""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'full_address': self.get_full_address(),
            'legal_issue_type': self.legal_issue_type,
            'case_description': self.case_description,
            'urgency_level': self.urgency_level,
            'income_level': self.income_level,
            'can_afford_legal_fees': self.can_afford_legal_fees,
            'needs_pro_bono': self.needs_pro_bono,
            'case_start_date': self.case_start_date.isoformat() if self.case_start_date else None,
            'previous_legal_representation': self.previous_legal_representation,
            'previous_attorney_name': self.previous_attorney_name,
            'status': self.status,
            'assigned_lawyer_id': self.assigned_lawyer_id,
            'assigned_paralegal_id': self.assigned_paralegal_id,
            'ai_analysis': json.loads(self.ai_analysis) if self.ai_analysis else None,
            'recommended_actions': json.loads(self.recommended_actions) if self.recommended_actions else None,
            'risk_assessment': self.risk_assessment,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'metadata': self.intake_metadata,
            'documents': self.documents
        }

    def __repr__(self):
        return f'<ClientIntake {self.id}: {self.get_full_name()} - {self.legal_issue_type}>'


class Task(db.Model):
    """Task model for managing legal tasks and assignments."""
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    intake_id = db.Column(db.Integer, db.ForeignKey('client_intakes.id'), nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Task details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    task_type = db.Column(db.String(50), nullable=False)  # research, document_review, client_meeting, court_filing, etc.
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    
    # Status and tracking
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed, cancelled, overdue
    progress_percentage = db.Column(db.Integer, default=0)
    
    # Dates
    due_date = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional info
    notes = db.Column(db.Text, nullable=True)
    _metadata = db.Column('metadata', db.Text, nullable=True)
    
    @property
    def task_metadata(self):
        """Get task metadata as a dictionary."""
        if not self._metadata:
            return {}
        return json.loads(self._metadata)
        
    @task_metadata.setter
    def task_metadata(self, value):
        """Set task metadata from a dictionary."""
        if isinstance(value, dict):
            self._metadata = json.dumps(value)
        else:
            self._metadata = None
    
    def is_overdue(self):
        """Check if the task is overdue."""
        if not self.due_date or self.status in ['completed', 'cancelled']:
            return False
        return datetime.utcnow() > self.due_date
    
    def to_dict(self):
        """Convert task to a dictionary."""
        return {
            'id': self.id,
            'case_id': self.case_id,
            'intake_id': self.intake_id,
            'assigned_to': self.assigned_to,
            'assigned_by': self.assigned_by,
            'title': self.title,
            'description': self.description,
            'task_type': self.task_type,
            'priority': self.priority,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'metadata': self.task_metadata,
            'is_overdue': self.is_overdue()
        }

    def __repr__(self):
        return f'<Task {self.id}: {self.title} - {self.status}>'

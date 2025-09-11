"""
Payment model for the SmartProBono application.
Handles payments for both legal services and bail bonds.
"""
from datetime import datetime
from database import db
import json

class Payment(db.Model):
    """Payment model for storing payment information."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    bond_id = db.Column(db.Integer, db.ForeignKey('bail_bonds.id'), nullable=True)
    
    # Payment details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.String(50), nullable=False)  # cash, check, credit_card, bank_transfer
    payment_type = db.Column(db.String(50), nullable=False)  # premium, retainer, fee, bond_payment
    
    # Status and tracking
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed, refunded
    transaction_id = db.Column(db.String(255), nullable=True)
    reference_number = db.Column(db.String(100), nullable=True)
    
    # Dates
    payment_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional info
    notes = db.Column(db.Text, nullable=True)
    _metadata = db.Column('metadata', db.Text, nullable=True)  # JSON for additional data
    
    @property
    def metadata(self):
        """Get payment metadata as a dictionary."""
        if not self._metadata:
            return {}
        return json.loads(self._metadata)
        
    @metadata.setter
    def metadata(self, value):
        """Set payment metadata from a dictionary."""
        if isinstance(value, dict):
            self._metadata = json.dumps(value)
        else:
            self._metadata = None
    
    def to_dict(self):
        """Convert payment to a dictionary."""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'case_id': self.case_id,
            'bond_id': self.bond_id,
            'amount': float(self.amount),
            'currency': self.currency,
            'payment_method': self.payment_method,
            'payment_type': self.payment_type,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'reference_number': self.reference_number,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'metadata': self.metadata
        }

    def __repr__(self):
        return f'<Payment {self.id}: ${self.amount} - {self.status}>'


class BailBond(db.Model):
    """Bail bond model for bondsman management."""
    __tablename__ = 'bail_bonds'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bondsman_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Bond details
    case_number = db.Column(db.String(100), nullable=False)
    charges = db.Column(db.Text, nullable=False)
    bond_amount = db.Column(db.Numeric(10, 2), nullable=False)
    premium_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Status and tracking
    status = db.Column(db.String(50), default='active')  # active, forfeited, exonerated, pending
    risk_level = db.Column(db.String(20), default='medium')  # low, medium, high
    
    # Court information
    court_location = db.Column(db.String(255), nullable=True)
    court_date = db.Column(db.DateTime, nullable=True)
    
    # Co-signer information
    cosigner_name = db.Column(db.String(255), nullable=True)
    cosigner_phone = db.Column(db.String(20), nullable=True)
    cosigner_address = db.Column(db.Text, nullable=True)
    
    # Dates
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional info
    notes = db.Column(db.Text, nullable=True)
    _metadata = db.Column('metadata', db.Text, nullable=True)
    
    # Relationships
    payments = db.relationship('Payment', backref='bail_bond', lazy=True)
    
    @property
    def metadata(self):
        """Get bond metadata as a dictionary."""
        if not self._metadata:
            return {}
        return json.loads(self._metadata)
        
    @metadata.setter
    def metadata(self, value):
        """Set bond metadata from a dictionary."""
        if isinstance(value, dict):
            self._metadata = json.dumps(value)
        else:
            self._metadata = None
    
    def to_dict(self):
        """Convert bail bond to a dictionary."""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'bondsman_id': self.bondsman_id,
            'case_number': self.case_number,
            'charges': self.charges,
            'bond_amount': float(self.bond_amount),
            'premium_amount': float(self.premium_amount),
            'status': self.status,
            'risk_level': self.risk_level,
            'court_location': self.court_location,
            'court_date': self.court_date.isoformat() if self.court_date else None,
            'cosigner_name': self.cosigner_name,
            'cosigner_phone': self.cosigner_phone,
            'cosigner_address': self.cosigner_address,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'metadata': self.metadata,
            'payment_count': len(self.payments) if self.payments else 0
        }

    def __repr__(self):
        return f'<BailBond {self.id}: {self.case_number} - ${self.bond_amount}>'


class CourtDate(db.Model):
    """Court date model for tracking hearings and appointments."""
    __tablename__ = 'court_dates'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    bond_id = db.Column(db.Integer, db.ForeignKey('bail_bonds.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Court date details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    court_location = db.Column(db.String(255), nullable=False)
    court_room = db.Column(db.String(50), nullable=True)
    
    # Date and time
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    
    # Status and type
    status = db.Column(db.String(50), default='scheduled')  # scheduled, completed, cancelled, rescheduled
    event_type = db.Column(db.String(50), nullable=False)  # hearing, appointment, deadline, meeting
    
    # Notification settings
    reminder_sent = db.Column(db.Boolean, default=False)
    reminder_days_before = db.Column(db.Integer, default=1)
    
    # Dates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional info
    notes = db.Column(db.Text, nullable=True)
    _metadata = db.Column('metadata', db.Text, nullable=True)
    
    @property
    def metadata(self):
        """Get court date metadata as a dictionary."""
        if not self._metadata:
            return {}
        return json.loads(self._metadata)
        
    @metadata.setter
    def metadata(self, value):
        """Set court date metadata from a dictionary."""
        if isinstance(value, dict):
            self._metadata = json.dumps(value)
        else:
            self._metadata = None
    
    def to_dict(self):
        """Convert court date to a dictionary."""
        return {
            'id': self.id,
            'case_id': self.case_id,
            'bond_id': self.bond_id,
            'client_id': self.client_id,
            'title': self.title,
            'description': self.description,
            'court_location': self.court_location,
            'court_room': self.court_room,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'duration_minutes': self.duration_minutes,
            'status': self.status,
            'event_type': self.event_type,
            'reminder_sent': self.reminder_sent,
            'reminder_days_before': self.reminder_days_before,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'metadata': self.metadata
        }

    def __repr__(self):
        return f'<CourtDate {self.id}: {self.title} - {self.scheduled_date}>'

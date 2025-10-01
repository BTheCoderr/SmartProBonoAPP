"""
Simple Court Filing Service for SmartProBono
Provides basic court filing functionality
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

class DocumentType(Enum):
    COMPLAINT = "complaint"
    MOTION = "motion"
    BRIEF = "brief"
    NOTICE = "notice"
    ORDER = "order"
    JUDGMENT = "judgment"

class FilingStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    FILED = "filed"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class CourtRule:
    def __init__(self, jurisdiction: str, court: str, rule_number: str, title: str, description: str):
        self.jurisdiction = jurisdiction
        self.court = court
        self.rule_number = rule_number
        self.title = title
        self.description = description
        self.requirements = []
        self.deadlines = []
        self.fees = {}
        self.forms = []
        self.electronic_filing = True
        self.efiling_system = "court_efiling_system"

class FilingTemplate:
    def __init__(self, template_id: str, name: str, document_type: str, jurisdiction: str):
        self.template_id = template_id
        self.name = name
        self.document_type = document_type
        self.jurisdiction = jurisdiction
        self.description = f"Template for {name} in {jurisdiction}"
        self.required_fields = []
        self.optional_fields = []
        self.file_path = f"templates/{template_id}.docx"

class CourtFiling:
    def __init__(self, case_id: str, document_type: str, title: str, description: str):
        self.id = f"filing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.case_id = case_id
        self.document_type = DocumentType(document_type)
        self.title = title
        self.description = description
        self.status = FilingStatus.DRAFT
        self.court = "Superior Court"
        self.jurisdiction = "State"
        self.filing_date = None
        self.due_date = datetime.now() + timedelta(days=30)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.filed_by = "system"
        self.file_path = None
        self.court_reference = None
        self.fees_paid = 0.0
        self.rejection_reason = None
        self.amendments = []
        self.attachments = []

class SimpleCourtFilingService:
    """Simple court filing service"""
    
    def __init__(self):
        self.filings = {}
        self.rules = self._initialize_rules()
        self.templates = self._initialize_templates()
    
    def _initialize_rules(self) -> List[CourtRule]:
        """Initialize court rules"""
        rules = [
            CourtRule("State", "Superior Court", "Rule 1", "General Filing Requirements", 
                     "All documents must be filed electronically"),
            CourtRule("State", "Superior Court", "Rule 2", "Document Format", 
                     "Documents must be in PDF format"),
            CourtRule("State", "Superior Court", "Rule 3", "Filing Deadlines", 
                     "Documents must be filed by 5:00 PM on business days"),
            CourtRule("Federal", "District Court", "Rule 1", "Federal Filing Rules", 
                     "Federal court filing requirements"),
        ]
        return rules
    
    def _initialize_templates(self) -> List[FilingTemplate]:
        """Initialize filing templates"""
        templates = [
            FilingTemplate("complaint_civil", "Civil Complaint", "complaint", "State"),
            FilingTemplate("motion_summary", "Motion for Summary Judgment", "motion", "State"),
            FilingTemplate("notice_hearing", "Notice of Hearing", "notice", "State"),
            FilingTemplate("brief_appeal", "Appellate Brief", "brief", "State"),
        ]
        return templates
    
    def get_filing_statistics(self) -> Dict:
        """Get filing statistics"""
        return {
            "total_filings": len(self.filings),
            "draft_filings": len([f for f in self.filings.values() if f.status == FilingStatus.DRAFT]),
            "pending_filings": len([f for f in self.filings.values() if f.status == FilingStatus.PENDING]),
            "filed_filings": len([f for f in self.filings.values() if f.status == FilingStatus.FILED]),
            "rejected_filings": len([f for f in self.filings.values() if f.status == FilingStatus.REJECTED]),
            "total_rules": len(self.rules),
            "total_templates": len(self.templates)
        }
    
    def get_court_rules(self, jurisdiction: str = None, court: str = None) -> List[CourtRule]:
        """Get court rules"""
        filtered_rules = self.rules
        
        if jurisdiction:
            filtered_rules = [r for r in filtered_rules if r.jurisdiction.lower() == jurisdiction.lower()]
        
        if court:
            filtered_rules = [r for r in filtered_rules if r.court.lower() == court.lower()]
        
        return filtered_rules
    
    def get_filing_templates(self, document_type: str = None, jurisdiction: str = None) -> List[FilingTemplate]:
        """Get filing templates"""
        filtered_templates = self.templates
        
        if document_type:
            filtered_templates = [t for t in filtered_templates if t.document_type == document_type]
        
        if jurisdiction:
            filtered_templates = [t for t in filtered_templates if t.jurisdiction.lower() == jurisdiction.lower()]
        
        return filtered_templates
    
    def create_filing(self, data: Dict) -> CourtFiling:
        """Create a new filing"""
        filing = CourtFiling(
            case_id=data.get('case_id', 'unknown'),
            document_type=data.get('document_type', 'complaint'),
            title=data.get('title', 'Untitled Filing'),
            description=data.get('description', 'No description provided')
        )
        
        # Update with additional data
        if 'court' in data:
            filing.court = data['court']
        if 'jurisdiction' in data:
            filing.jurisdiction = data['jurisdiction']
        if 'filed_by' in data:
            filing.filed_by = data['filed_by']
        
        self.filings[filing.id] = filing
        return filing
    
    def get_filing(self, filing_id: str) -> Optional[CourtFiling]:
        """Get a filing by ID"""
        return self.filings.get(filing_id)
    
    def calculate_filing_fees(self, document_type: DocumentType, jurisdiction: str, court: str) -> Dict:
        """Calculate filing fees"""
        base_fees = {
            DocumentType.COMPLAINT: 150.0,
            DocumentType.MOTION: 50.0,
            DocumentType.BRIEF: 25.0,
            DocumentType.NOTICE: 10.0,
            DocumentType.ORDER: 0.0,
            DocumentType.JUDGMENT: 0.0
        }
        
        base_fee = base_fees.get(document_type, 50.0)
        
        # Add jurisdiction-specific fees
        if jurisdiction.lower() == "federal":
            base_fee += 25.0
        
        return {
            "base_fee": base_fee,
            "service_fee": 5.0,
            "total_fee": base_fee + 5.0,
            "currency": "USD",
            "document_type": document_type.value,
            "jurisdiction": jurisdiction,
            "court": court
        }
    
    def calculate_filing_deadlines(self, case_events: List[Dict]) -> Dict:
        """Calculate filing deadlines"""
        deadlines = []
        
        for event in case_events:
            event_date = datetime.fromisoformat(event.get('date', datetime.now().isoformat()))
            event_type = event.get('type', 'unknown')
            
            if event_type == 'complaint_filed':
                deadlines.append({
                    'event': 'Answer due',
                    'deadline': (event_date + timedelta(days=30)).isoformat(),
                    'days_remaining': 30
                })
            elif event_type == 'motion_filed':
                deadlines.append({
                    'event': 'Response due',
                    'deadline': (event_date + timedelta(days=14)).isoformat(),
                    'days_remaining': 14
                })
        
        return {
            'deadlines': deadlines,
            'total_deadlines': len(deadlines),
            'urgent_deadlines': [d for d in deadlines if d['days_remaining'] <= 7]
        }
    
    def file_document(self, filing_id: str, court_system: str = "efiling") -> bool:
        """File a document with the court"""
        filing = self.get_filing(filing_id)
        if not filing:
            return False
        
        # Simulate filing process
        filing.status = FilingStatus.FILED
        filing.filing_date = datetime.now()
        filing.court_reference = f"REF-{filing_id}"
        filing.updated_at = datetime.now()
        
        return True
    
    def validate_filing(self, filing_id: str) -> Dict:
        """Validate a filing"""
        filing = self.get_filing(filing_id)
        if not filing:
            return {
                'valid': False,
                'errors': ['Filing not found']
            }
        
        errors = []
        
        if not filing.title:
            errors.append('Title is required')
        
        if not filing.description:
            errors.append('Description is required')
        
        if not filing.case_id:
            errors.append('Case ID is required')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': []
        }

# Global court filing service instance
court_filing_service = SimpleCourtFilingService()

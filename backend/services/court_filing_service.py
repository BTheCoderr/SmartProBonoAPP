"""
Court Filing Assistance Service
Handles court document preparation, filing, and tracking
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

class FilingStatus(Enum):
    """Court filing status enumeration"""
    DRAFT = "draft"
    READY_TO_FILE = "ready_to_file"
    FILED = "filed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    AMENDED = "amended"
    WITHDRAWN = "withdrawn"

class DocumentType(Enum):
    """Court document types"""
    COMPLAINT = "complaint"
    ANSWER = "answer"
    MOTION = "motion"
    BRIEF = "brief"
    NOTICE = "notice"
    ORDER = "order"
    JUDGMENT = "judgment"
    APPEAL = "appeal"
    PETITION = "petition"
    AFFIDAVIT = "affidavit"

@dataclass
class CourtFiling:
    """Court filing data structure"""
    id: str
    case_id: str
    document_type: DocumentType
    title: str
    description: str
    status: FilingStatus
    court: str
    jurisdiction: str
    filing_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None
    filed_by: str = ""
    file_path: str = ""
    court_reference: str = ""
    fees_paid: float = 0.0
    rejection_reason: str = ""
    amendments: List[str] = None
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.amendments is None:
            self.amendments = []
        if self.attachments is None:
            self.attachments = []

@dataclass
class CourtRule:
    """Court rule data structure"""
    jurisdiction: str
    court: str
    rule_number: str
    title: str
    description: str
    requirements: List[str]
    deadlines: Dict[str, int]  # days from event
    fees: Dict[str, float]
    forms: List[str]
    electronic_filing: bool = False
    efiling_system: str = ""

@dataclass
class FilingTemplate:
    """Filing template data structure"""
    id: str
    name: str
    document_type: DocumentType
    jurisdiction: str
    court: str
    template_content: str
    required_fields: List[str]
    optional_fields: List[str]
    instructions: str
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

class CourtFilingService:
    """Service for handling court filing operations"""
    
    def __init__(self):
        self.filings: Dict[str, CourtFiling] = {}
        self.templates: Dict[str, FilingTemplate] = {}
        self.rules: Dict[str, CourtRule] = {}
        self.filing_counter = 0
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize service with sample court rules and templates"""
        
        # Sample court rules
        self.rules = {
            "ri_superior": CourtRule(
                jurisdiction="Rhode Island",
                court="Superior Court",
                rule_number="Civ. R. 5",
                title="Service and Filing of Pleadings",
                description="Rules for serving and filing court documents",
                requirements=[
                    "All pleadings must be filed with the clerk",
                    "Service must be made within 20 days of filing",
                    "Electronic filing is required for all documents",
                    "Filing fees must be paid at time of filing"
                ],
                deadlines={
                    "answer_to_complaint": 20,
                    "motion_response": 10,
                    "appeal_filing": 30
                },
                fees={
                    "complaint": 150.0,
                    "motion": 25.0,
                    "appeal": 200.0
                },
                forms=[
                    "Civil Cover Sheet",
                    "Summons",
                    "Certificate of Service"
                ],
                electronic_filing=True,
                efiling_system="Rhode Island eFiling"
            ),
            "ri_district": CourtRule(
                jurisdiction="Rhode Island",
                court="District Court",
                rule_number="Dist. R. 3",
                title="Filing Requirements",
                description="District Court filing requirements",
                requirements=[
                    "Documents must be filed in person or electronically",
                    "Filing fees vary by case type",
                    "Small claims have simplified procedures"
                ],
                deadlines={
                    "answer_to_complaint": 14,
                    "motion_response": 7,
                    "small_claims_response": 10
                },
                fees={
                    "complaint": 75.0,
                    "motion": 15.0,
                    "small_claims": 25.0
                },
                forms=[
                    "District Court Cover Sheet",
                    "Small Claims Form"
                ],
                electronic_filing=True,
                efiling_system="Rhode Island eFiling"
            )
        }
        
        # Sample filing templates
        self.templates = {
            "complaint_template": FilingTemplate(
                id="complaint_template",
                name="Civil Complaint Template",
                document_type=DocumentType.COMPLAINT,
                jurisdiction="Rhode Island",
                court="Superior Court",
                template_content=self._get_complaint_template(),
                required_fields=[
                    "plaintiff_name",
                    "defendant_name",
                    "cause_of_action",
                    "damages_sought",
                    "jurisdiction_facts"
                ],
                optional_fields=[
                    "attorney_info",
                    "exhibits",
                    "witnesses"
                ],
                instructions="Complete all required fields and file with the court clerk."
            ),
            "motion_template": FilingTemplate(
                id="motion_template",
                name="Motion Template",
                document_type=DocumentType.MOTION,
                jurisdiction="Rhode Island",
                court="Superior Court",
                template_content=self._get_motion_template(),
                required_fields=[
                    "motion_type",
                    "legal_basis",
                    "relief_sought",
                    "supporting_facts"
                ],
                optional_fields=[
                    "case_law",
                    "affidavits",
                    "exhibits"
                ],
                instructions="Specify the type of motion and provide legal basis for relief."
            )
        }
    
    def _get_complaint_template(self) -> str:
        """Get complaint template content"""
        return """
IN THE SUPERIOR COURT OF RHODE ISLAND

{plaintiff_name},                    )
Plaintiff,                          )    C.A. No. ______
v.                                  )
{defendant_name},                    )
Defendant.                          )

COMPLAINT

I. JURISDICTION AND VENUE
1. This Court has jurisdiction over this matter pursuant to R.I. Gen. Laws § 8-2-14.
2. Venue is proper in this county because {jurisdiction_facts}.

II. PARTIES
3. Plaintiff {plaintiff_name} is a {plaintiff_description}.
4. Defendant {defendant_name} is a {defendant_description}.

III. FACTUAL ALLEGATIONS
5. {factual_allegations}

IV. CAUSE OF ACTION
6. {cause_of_action}

V. DAMAGES
7. As a result of Defendant's conduct, Plaintiff has suffered damages in the amount of ${damages_sought}.

WHEREFORE, Plaintiff respectfully requests that this Court:
A. Enter judgment in favor of Plaintiff and against Defendant;
B. Award Plaintiff damages in the amount of ${damages_sought};
C. Award Plaintiff costs and attorney's fees; and
D. Grant such other relief as the Court deems just and proper.

Respectfully submitted,

{attorney_name}
{attorney_firm}
{attorney_address}
{attorney_phone}
{attorney_email}

Date: {filing_date}
"""
    
    def _get_motion_template(self) -> str:
        """Get motion template content"""
        return """
IN THE SUPERIOR COURT OF RHODE ISLAND

{plaintiff_name},                    )
Plaintiff,                          )    C.A. No. ______
v.                                  )
{defendant_name},                    )
Defendant.                          )

MOTION FOR {motion_type}

I. INTRODUCTION
1. {motion_introduction}

II. LEGAL BASIS
2. {legal_basis}

III. FACTUAL SUPPORT
3. {supporting_facts}

IV. RELIEF SOUGHT
4. {relief_sought}

WHEREFORE, {moving_party} respectfully requests that this Court:
A. {requested_relief_1};
B. {requested_relief_2}; and
C. Grant such other relief as the Court deems just and proper.

Respectfully submitted,

{attorney_name}
{attorney_firm}
{attorney_address}
{attorney_phone}
{attorney_email}

Date: {filing_date}
"""
    
    def create_filing(self, filing_data: Dict[str, Any]) -> CourtFiling:
        """Create a new court filing"""
        try:
            self.filing_counter += 1
            filing_id = f"filing_{self.filing_counter:06d}"
            
            # Create filing object
            filing = CourtFiling(
                id=filing_id,
                case_id=filing_data.get('case_id', ''),
                document_type=DocumentType(filing_data.get('document_type', 'complaint')),
                title=filing_data.get('title', ''),
                description=filing_data.get('description', ''),
                status=FilingStatus.DRAFT,
                court=filing_data.get('court', ''),
                jurisdiction=filing_data.get('jurisdiction', ''),
                due_date=filing_data.get('due_date'),
                filed_by=filing_data.get('filed_by', ''),
                file_path=filing_data.get('file_path', ''),
                fees_paid=filing_data.get('fees_paid', 0.0)
            )
            
            self.filings[filing_id] = filing
            
            logger.info(f"Created court filing: {filing_id}")
            return filing
            
        except Exception as e:
            logger.error(f"Error creating court filing: {e}")
            raise
    
    def get_filing(self, filing_id: str) -> Optional[CourtFiling]:
        """Get a court filing by ID"""
        return self.filings.get(filing_id)
    
    def update_filing(self, filing_id: str, updates: Dict[str, Any]) -> Optional[CourtFiling]:
        """Update a court filing"""
        try:
            filing = self.filings.get(filing_id)
            if not filing:
                return None
            
            # Update fields
            for key, value in updates.items():
                if hasattr(filing, key):
                    setattr(filing, key, value)
            
            filing.updated_at = datetime.now()
            
            logger.info(f"Updated court filing: {filing_id}")
            return filing
            
        except Exception as e:
            logger.error(f"Error updating court filing: {e}")
            raise
    
    def file_document(self, filing_id: str, court_system: str = "efiling") -> bool:
        """File a document with the court"""
        try:
            filing = self.filings.get(filing_id)
            if not filing:
                return False
            
            if filing.status != FilingStatus.READY_TO_FILE:
                logger.warning(f"Filing {filing_id} is not ready to file")
                return False
            
            # Simulate court filing
            if court_system == "efiling":
                success = self._simulate_efiling(filing)
            else:
                success = self._simulate_paper_filing(filing)
            
            if success:
                filing.status = FilingStatus.FILED
                filing.filing_date = datetime.now()
                filing.court_reference = f"REF-{filing_id}-{datetime.now().strftime('%Y%m%d')}"
                filing.updated_at = datetime.now()
                
                logger.info(f"Successfully filed document: {filing_id}")
                return True
            else:
                filing.status = FilingStatus.REJECTED
                filing.rejection_reason = "Court system rejected the filing"
                filing.updated_at = datetime.now()
                
                logger.warning(f"Court filing rejected: {filing_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error filing document: {e}")
            return False
    
    def _simulate_efiling(self, filing: CourtFiling) -> bool:
        """Simulate electronic filing process"""
        # Simulate API call to court e-filing system
        try:
            # In a real implementation, this would call the actual court API
            response = {
                "success": True,
                "filing_id": filing.id,
                "court_reference": f"REF-{filing.id}-{datetime.now().strftime('%Y%m%d')}",
                "filing_date": datetime.now().isoformat(),
                "status": "accepted"
            }
            
            return response.get("success", False)
            
        except Exception as e:
            logger.error(f"E-filing simulation error: {e}")
            return False
    
    def _simulate_paper_filing(self, filing: CourtFiling) -> bool:
        """Simulate paper filing process"""
        # Simulate physical filing process
        try:
            # In a real implementation, this would handle physical document submission
            return True
            
        except Exception as e:
            logger.error(f"Paper filing simulation error: {e}")
            return False
    
    def get_court_rules(self, jurisdiction: str = None, court: str = None) -> List[CourtRule]:
        """Get court rules for a jurisdiction and court"""
        rules = list(self.rules.values())
        
        if jurisdiction:
            rules = [rule for rule in rules if rule.jurisdiction.lower() == jurisdiction.lower()]
        
        if court:
            rules = [rule for rule in rules if rule.court.lower() == court.lower()]
        
        return rules
    
    def get_filing_templates(self, document_type: DocumentType = None, 
                           jurisdiction: str = None) -> List[FilingTemplate]:
        """Get filing templates"""
        templates = list(self.templates.values())
        
        if document_type:
            templates = [t for t in templates if t.document_type == document_type]
        
        if jurisdiction:
            templates = [t for t in templates if t.jurisdiction.lower() == jurisdiction.lower()]
        
        return templates
    
    def generate_document(self, template_id: str, data: Dict[str, Any]) -> str:
        """Generate a document from a template"""
        try:
            template = self.templates.get(template_id)
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            
            # Replace placeholders in template
            document_content = template.template_content
            
            for key, value in data.items():
                placeholder = "{" + key + "}"
                document_content = document_content.replace(placeholder, str(value))
            
            # Add current date if not provided
            if "{filing_date}" in document_content and "filing_date" not in data:
                document_content = document_content.replace("{filing_date}", datetime.now().strftime("%B %d, %Y"))
            
            return document_content
            
        except Exception as e:
            logger.error(f"Error generating document: {e}")
            raise
    
    def calculate_filing_fees(self, document_type: DocumentType, 
                            jurisdiction: str, court: str) -> float:
        """Calculate filing fees for a document"""
        try:
            rules = self.get_court_rules(jurisdiction, court)
            if not rules:
                return 0.0
            
            rule = rules[0]  # Use first matching rule
            return rule.fees.get(document_type.value, 0.0)
            
        except Exception as e:
            logger.error(f"Error calculating filing fees: {e}")
            return 0.0
    
    def get_filing_deadlines(self, case_events: List[Dict[str, Any]], 
                           jurisdiction: str, court: str) -> Dict[str, datetime]:
        """Calculate filing deadlines based on case events"""
        try:
            rules = self.get_court_rules(jurisdiction, court)
            if not rules:
                return {}
            
            rule = rules[0]
            deadlines = {}
            
            for event in case_events:
                event_type = event.get('type')
                event_date = event.get('date')
                
                if event_type in rule.deadlines and event_date:
                    event_dt = datetime.fromisoformat(event_date)
                    deadline_days = rule.deadlines[event_type]
                    deadline = event_dt + timedelta(days=deadline_days)
                    deadlines[event_type] = deadline
            
            return deadlines
            
        except Exception as e:
            logger.error(f"Error calculating filing deadlines: {e}")
            return {}
    
    def validate_filing(self, filing_id: str) -> Tuple[bool, List[str]]:
        """Validate a court filing for completeness and compliance"""
        try:
            filing = self.filings.get(filing_id)
            if not filing:
                return False, ["Filing not found"]
            
            errors = []
            
            # Check required fields
            if not filing.title:
                errors.append("Title is required")
            
            if not filing.court:
                errors.append("Court is required")
            
            if not filing.jurisdiction:
                errors.append("Jurisdiction is required")
            
            # Check court rules compliance
            rules = self.get_court_rules(filing.jurisdiction, filing.court)
            if rules:
                rule = rules[0]
                
                # Check if electronic filing is required
                if rule.electronic_filing and not filing.file_path:
                    errors.append("Electronic filing is required for this court")
                
                # Check filing fees
                required_fee = self.calculate_filing_fees(
                    filing.document_type, 
                    filing.jurisdiction, 
                    filing.court
                )
                if required_fee > 0 and filing.fees_paid < required_fee:
                    errors.append(f"Filing fee of ${required_fee} is required")
            
            # Check due date
            if filing.due_date and filing.due_date < datetime.now():
                errors.append("Filing is past due")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            logger.error(f"Error validating filing: {e}")
            return False, [f"Validation error: {str(e)}"]
    
    def get_filing_statistics(self) -> Dict[str, Any]:
        """Get filing statistics"""
        try:
            total_filings = len(self.filings)
            status_counts = {}
            
            for filing in self.filings.values():
                status = filing.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "total_filings": total_filings,
                "status_breakdown": status_counts,
                "templates_available": len(self.templates),
                "court_rules_available": len(self.rules)
            }
            
        except Exception as e:
            logger.error(f"Error getting filing statistics: {e}")
            return {}

# Global court filing service instance
court_filing_service = CourtFilingService()

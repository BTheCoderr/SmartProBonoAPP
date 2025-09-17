"""
Court Filing Service Tests
Tests for court document preparation and filing functionality
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.court_filing_service import (
    CourtFilingService, 
    CourtFiling, 
    FilingStatus, 
    DocumentType,
    CourtRule,
    FilingTemplate
)

class TestCourtFilingService:
    """Test Court Filing Service functionality"""
    
    @pytest.fixture
    def filing_service(self):
        """Create a court filing service instance for testing"""
        return CourtFilingService()
    
    def test_service_initialization(self, filing_service):
        """Test service initialization with sample data"""
        assert filing_service.filings is not None
        assert filing_service.templates is not None
        assert filing_service.rules is not None
        assert len(filing_service.rules) > 0
        assert len(filing_service.templates) > 0
    
    def test_create_filing(self, filing_service):
        """Test creating a new court filing"""
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Test Complaint',
            'description': 'Test filing description',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island',
            'filed_by': 'Test Attorney'
        }
        
        filing = filing_service.create_filing(filing_data)
        
        assert filing.id is not None
        assert filing.case_id == 'CASE-001'
        assert filing.document_type == DocumentType.COMPLAINT
        assert filing.title == 'Test Complaint'
        assert filing.status == FilingStatus.DRAFT
        assert filing.court == 'Superior Court'
        assert filing.jurisdiction == 'Rhode Island'
        assert filing.filed_by == 'Test Attorney'
        assert filing.created_at is not None
        assert filing.updated_at is not None
        
        # Check that filing was stored
        assert filing.id in filing_service.filings
    
    def test_create_filing_missing_data(self, filing_service):
        """Test creating filing with missing required data"""
        filing_data = {
            'case_id': 'CASE-001'
            # Missing required fields
        }
        
        with pytest.raises(Exception):
            filing_service.create_filing(filing_data)
    
    def test_get_filing(self, filing_service):
        """Test retrieving a filing by ID"""
        # Create a filing first
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Test Complaint',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island'
        }
        
        created_filing = filing_service.create_filing(filing_data)
        
        # Retrieve the filing
        retrieved_filing = filing_service.get_filing(created_filing.id)
        
        assert retrieved_filing is not None
        assert retrieved_filing.id == created_filing.id
        assert retrieved_filing.title == 'Test Complaint'
    
    def test_get_filing_not_found(self, filing_service):
        """Test retrieving a non-existent filing"""
        filing = filing_service.get_filing('nonexistent_id')
        assert filing is None
    
    def test_update_filing(self, filing_service):
        """Test updating a court filing"""
        # Create a filing first
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Test Complaint',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island'
        }
        
        created_filing = filing_service.create_filing(filing_data)
        
        # Update the filing
        updates = {
            'title': 'Updated Complaint',
            'status': FilingStatus.READY_TO_FILE,
            'description': 'Updated description'
        }
        
        updated_filing = filing_service.update_filing(created_filing.id, updates)
        
        assert updated_filing is not None
        assert updated_filing.title == 'Updated Complaint'
        assert updated_filing.status == FilingStatus.READY_TO_FILE
        assert updated_filing.description == 'Updated description'
        assert updated_filing.updated_at > created_filing.updated_at
    
    def test_update_filing_not_found(self, filing_service):
        """Test updating a non-existent filing"""
        updates = {'title': 'Updated Title'}
        result = filing_service.update_filing('nonexistent_id', updates)
        assert result is None
    
    def test_get_court_rules(self, filing_service):
        """Test getting court rules"""
        # Test getting all rules
        all_rules = filing_service.get_court_rules()
        assert len(all_rules) > 0
        
        # Test filtering by jurisdiction
        ri_rules = filing_service.get_court_rules('Rhode Island')
        assert len(ri_rules) > 0
        for rule in ri_rules:
            assert rule.jurisdiction == 'Rhode Island'
        
        # Test filtering by court
        superior_rules = filing_service.get_court_rules('Rhode Island', 'Superior Court')
        assert len(superior_rules) > 0
        for rule in superior_rules:
            assert rule.court == 'Superior Court'
    
    def test_get_filing_templates(self, filing_service):
        """Test getting filing templates"""
        # Test getting all templates
        all_templates = filing_service.get_filing_templates()
        assert len(all_templates) > 0
        
        # Test filtering by document type
        complaint_templates = filing_service.get_filing_templates(DocumentType.COMPLAINT)
        assert len(complaint_templates) > 0
        for template in complaint_templates:
            assert template.document_type == DocumentType.COMPLAINT
        
        # Test filtering by jurisdiction
        ri_templates = filing_service.get_filing_templates(jurisdiction='Rhode Island')
        assert len(ri_templates) > 0
        for template in ri_templates:
            assert template.jurisdiction == 'Rhode Island'
    
    def test_generate_document(self, filing_service):
        """Test generating a document from a template"""
        # Get a template
        templates = filing_service.get_filing_templates(DocumentType.COMPLAINT)
        assert len(templates) > 0
        
        template = templates[0]
        
        # Generate document with data
        data = {
            'plaintiff_name': 'John Doe',
            'defendant_name': 'Jane Smith',
            'cause_of_action': 'Breach of Contract',
            'damages_sought': '50000',
            'jurisdiction_facts': 'Defendant resides in this county'
        }
        
        document = filing_service.generate_document(template.id, data)
        
        assert document is not None
        assert 'John Doe' in document
        assert 'Jane Smith' in document
        assert 'Breach of Contract' in document
        assert '$50000' in document
        assert 'Defendant resides in this county' in document
    
    def test_generate_document_invalid_template(self, filing_service):
        """Test generating document with invalid template ID"""
        with pytest.raises(ValueError):
            filing_service.generate_document('invalid_template_id', {})
    
    def test_calculate_filing_fees(self, filing_service):
        """Test calculating filing fees"""
        # Test complaint fee
        fee = filing_service.calculate_filing_fees(
            DocumentType.COMPLAINT,
            'Rhode Island',
            'Superior Court'
        )
        
        assert fee > 0
        assert isinstance(fee, float)
        
        # Test motion fee
        motion_fee = filing_service.calculate_filing_fees(
            DocumentType.MOTION,
            'Rhode Island',
            'Superior Court'
        )
        
        assert motion_fee > 0
        assert isinstance(motion_fee, float)
    
    def test_calculate_filing_fees_no_rules(self, filing_service):
        """Test calculating fees when no rules exist"""
        fee = filing_service.calculate_filing_fees(
            DocumentType.COMPLAINT,
            'Nonexistent Jurisdiction',
            'Nonexistent Court'
        )
        
        assert fee == 0.0
    
    def test_get_filing_deadlines(self, filing_service):
        """Test calculating filing deadlines"""
        case_events = [
            {'type': 'complaint_filed', 'date': datetime.now().isoformat()},
            {'type': 'motion_response', 'date': (datetime.now() + timedelta(days=5)).isoformat()}
        ]
        
        deadlines = filing_service.get_filing_deadlines(
            case_events,
            'Rhode Island',
            'Superior Court'
        )
        
        assert len(deadlines) > 0
        assert 'complaint_filed' in deadlines or 'motion_response' in deadlines
        
        # Check that deadlines are in the future
        for deadline in deadlines.values():
            assert deadline > datetime.now()
    
    def test_get_filing_deadlines_no_rules(self, filing_service):
        """Test calculating deadlines when no rules exist"""
        case_events = [
            {'type': 'complaint_filed', 'date': datetime.now().isoformat()}
        ]
        
        deadlines = filing_service.get_filing_deadlines(
            case_events,
            'Nonexistent Jurisdiction',
            'Nonexistent Court'
        )
        
        assert len(deadlines) == 0
    
    def test_validate_filing(self, filing_service):
        """Test validating a court filing"""
        # Create a valid filing
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Valid Complaint',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island',
            'filed_by': 'Test Attorney'
        }
        
        filing = filing_service.create_filing(filing_data)
        
        # Validate the filing
        is_valid, errors = filing_service.validate_filing(filing.id)
        
        assert is_valid == True
        assert len(errors) == 0
    
    def test_validate_filing_missing_fields(self, filing_service):
        """Test validating a filing with missing required fields"""
        # Create a filing with missing title
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': '',  # Missing title
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island'
        }
        
        filing = filing_service.create_filing(filing_data)
        
        # Validate the filing
        is_valid, errors = filing_service.validate_filing(filing.id)
        
        assert is_valid == False
        assert len(errors) > 0
        assert any('Title is required' in error for error in errors)
    
    def test_validate_filing_not_found(self, filing_service):
        """Test validating a non-existent filing"""
        is_valid, errors = filing_service.validate_filing('nonexistent_id')
        
        assert is_valid == False
        assert len(errors) == 1
        assert 'Filing not found' in errors[0]
    
    @patch('services.court_filing_service.requests.post')
    def test_file_document_success(self, mock_post, filing_service):
        """Test successful document filing"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'filing_id': 'test_filing',
            'court_reference': 'REF-12345',
            'status': 'accepted'
        }
        mock_post.return_value = mock_response
        
        # Create a filing ready to file
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Test Complaint',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island'
        }
        
        filing = filing_service.create_filing(filing_data)
        filing.status = FilingStatus.READY_TO_FILE
        
        # File the document
        success = filing_service.file_document(filing.id, 'efiling')
        
        assert success == True
        assert filing.status == FilingStatus.FILED
        assert filing.filing_date is not None
        assert filing.court_reference is not None
    
    def test_file_document_not_ready(self, filing_service):
        """Test filing a document that's not ready"""
        # Create a draft filing
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Test Complaint',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island'
        }
        
        filing = filing_service.create_filing(filing_data)
        # Status is DRAFT by default
        
        # Try to file the document
        success = filing_service.file_document(filing.id)
        
        assert success == False
        assert filing.status == FilingStatus.DRAFT  # Status unchanged
    
    def test_file_document_not_found(self, filing_service):
        """Test filing a non-existent document"""
        success = filing_service.file_document('nonexistent_id')
        assert success == False
    
    def test_get_filing_statistics(self, filing_service):
        """Test getting filing statistics"""
        # Create some test filings
        for i in range(3):
            filing_data = {
                'case_id': f'CASE-{i:03d}',
                'document_type': 'complaint',
                'title': f'Test Complaint {i}',
                'court': 'Superior Court',
                'jurisdiction': 'Rhode Island'
            }
            filing_service.create_filing(filing_data)
        
        stats = filing_service.get_filing_statistics()
        
        assert stats['total_filings'] >= 3
        assert 'status_breakdown' in stats
        assert 'templates_available' in stats
        assert 'court_rules_available' in stats
        assert stats['templates_available'] > 0
        assert stats['court_rules_available'] > 0

class TestCourtFiling:
    """Test CourtFiling dataclass"""
    
    def test_court_filing_creation(self):
        """Test creating a court filing"""
        filing = CourtFiling(
            id='FILING-001',
            case_id='CASE-001',
            document_type=DocumentType.COMPLAINT,
            title='Test Complaint',
            description='Test filing description',
            status=FilingStatus.DRAFT,
            court='Superior Court',
            jurisdiction='Rhode Island',
            filed_by='Test Attorney'
        )
        
        assert filing.id == 'FILING-001'
        assert filing.case_id == 'CASE-001'
        assert filing.document_type == DocumentType.COMPLAINT
        assert filing.title == 'Test Complaint'
        assert filing.status == FilingStatus.DRAFT
        assert filing.court == 'Superior Court'
        assert filing.jurisdiction == 'Rhode Island'
        assert filing.filed_by == 'Test Attorney'
        assert filing.created_at is not None
        assert filing.updated_at is not None
        assert filing.amendments == []
        assert filing.attachments == []
    
    def test_court_filing_default_values(self):
        """Test court filing default values"""
        filing = CourtFiling(
            id='FILING-001',
            case_id='CASE-001',
            document_type=DocumentType.COMPLAINT,
            title='Test Complaint',
            description='Test description',
            status=FilingStatus.DRAFT,
            court='Superior Court',
            jurisdiction='Rhode Island'
        )
        
        assert filing.filing_date is None
        assert filing.due_date is None
        assert filing.filed_by == ""
        assert filing.file_path == ""
        assert filing.court_reference == ""
        assert filing.fees_paid == 0.0
        assert filing.rejection_reason == ""
        assert filing.amendments == []
        assert filing.attachments == []

class TestCourtRule:
    """Test CourtRule dataclass"""
    
    def test_court_rule_creation(self):
        """Test creating a court rule"""
        rule = CourtRule(
            jurisdiction='Rhode Island',
            court='Superior Court',
            rule_number='Civ. R. 5',
            title='Service and Filing',
            description='Rules for filing documents',
            requirements=['File with clerk', 'Serve within 20 days'],
            deadlines={'answer_to_complaint': 20},
            fees={'complaint': 150.0},
            forms=['Civil Cover Sheet'],
            electronic_filing=True,
            efiling_system='Rhode Island eFiling'
        )
        
        assert rule.jurisdiction == 'Rhode Island'
        assert rule.court == 'Superior Court'
        assert rule.rule_number == 'Civ. R. 5'
        assert rule.title == 'Service and Filing'
        assert len(rule.requirements) == 2
        assert rule.deadlines['answer_to_complaint'] == 20
        assert rule.fees['complaint'] == 150.0
        assert rule.electronic_filing == True
        assert rule.efiling_system == 'Rhode Island eFiling'

class TestFilingTemplate:
    """Test FilingTemplate dataclass"""
    
    def test_filing_template_creation(self):
        """Test creating a filing template"""
        template = FilingTemplate(
            id='complaint_template',
            name='Civil Complaint Template',
            document_type=DocumentType.COMPLAINT,
            jurisdiction='Rhode Island',
            court='Superior Court',
            template_content='This is a complaint template...',
            required_fields=['plaintiff_name', 'defendant_name'],
            optional_fields=['attorney_info'],
            instructions='Fill out all required fields'
        )
        
        assert template.id == 'complaint_template'
        assert template.name == 'Civil Complaint Template'
        assert template.document_type == DocumentType.COMPLAINT
        assert template.jurisdiction == 'Rhode Island'
        assert template.court == 'Superior Court'
        assert 'complaint template' in template.template_content
        assert len(template.required_fields) == 2
        assert len(template.optional_fields) == 1
        assert template.instructions == 'Fill out all required fields'
        assert template.created_at is not None
        assert template.updated_at is not None

class TestDocumentTypes:
    """Test DocumentType enumeration"""
    
    def test_document_type_values(self):
        """Test document type enumeration values"""
        assert DocumentType.COMPLAINT.value == 'complaint'
        assert DocumentType.ANSWER.value == 'answer'
        assert DocumentType.MOTION.value == 'motion'
        assert DocumentType.BRIEF.value == 'brief'
        assert DocumentType.NOTICE.value == 'notice'
        assert DocumentType.ORDER.value == 'order'
        assert DocumentType.JUDGMENT.value == 'judgment'
        assert DocumentType.APPEAL.value == 'appeal'
        assert DocumentType.PETITION.value == 'petition'
        assert DocumentType.AFFIDAVIT.value == 'affidavit'
    
    def test_document_type_from_string(self):
        """Test creating document type from string"""
        assert DocumentType('complaint') == DocumentType.COMPLAINT
        assert DocumentType('motion') == DocumentType.MOTION
        assert DocumentType('appeal') == DocumentType.APPEAL

class TestFilingStatus:
    """Test FilingStatus enumeration"""
    
    def test_filing_status_values(self):
        """Test filing status enumeration values"""
        assert FilingStatus.DRAFT.value == 'draft'
        assert FilingStatus.READY_TO_FILE.value == 'ready_to_file'
        assert FilingStatus.FILED.value == 'filed'
        assert FilingStatus.ACCEPTED.value == 'accepted'
        assert FilingStatus.REJECTED.value == 'rejected'
        assert FilingStatus.AMENDED.value == 'amended'
        assert FilingStatus.WITHDRAWN.value == 'withdrawn'
    
    def test_filing_status_from_string(self):
        """Test creating filing status from string"""
        assert FilingStatus('draft') == FilingStatus.DRAFT
        assert FilingStatus('filed') == FilingStatus.FILED
        assert FilingStatus('rejected') == FilingStatus.REJECTED

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

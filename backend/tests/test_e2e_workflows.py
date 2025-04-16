import pytest  # This import is resolved by pytest when running tests
import json
import os
from unittest.mock import patch, MagicMock
from io import BytesIO

class TestEndToEndWorkflows:
    """End-to-end tests for critical application workflows."""
    
    @pytest.fixture
    def login_user(self, client, sample_user):
        """Helper fixture to log in a user and get auth token."""
        # Mock the auth system for testing
        with patch('routes.auth.verify_password', return_value=True):
            with patch('routes.auth.get_user_by_email', return_value=sample_user):
                login_data = {
                    'email': sample_user.email,
                    'password': 'password123'
                }
                response = client.post('/login',
                                      headers={'Content-Type': 'application/json'},
                                      data=json.dumps(login_data))
                data = json.loads(response.data)
                token = data.get('access_token')
                return {'Authorization': f'Bearer {token}'}
    
    def test_complete_case_workflow(self, client, login_user, sample_user, sample_lawyer):
        """Test a complete case workflow from creation to closure."""
        # Step 1: Create a new case
        case_data = {
            'title': 'E2E Test Case',
            'description': 'This is an end-to-end test case',
            'case_type': 'IMMIGRATION',
            'status': 'NEW',
            'priority': 'MEDIUM'
        }
        
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            case_response = client.post('/api/cases',
                                       headers={**login_user, 'Content-Type': 'application/json'},
                                       data=json.dumps(case_data))
            case = json.loads(case_response.data)
            assert case_response.status_code == 201
            case_id = case['id']
            
            # Step 2: Assign a lawyer to the case
            assign_data = {
                'lawyer_id': sample_lawyer.id
            }
            
            assign_response = client.post(f'/api/cases/{case_id}/assign',
                                         headers={**login_user, 'Content-Type': 'application/json'},
                                         data=json.dumps(assign_data))
            updated_case = json.loads(assign_response.data)
            assert assign_response.status_code == 200
            assert updated_case['lawyer_id'] == sample_lawyer.id
            
            # Step 3: Add documents to the case
            document_data = {
                'title': 'E2E Test Document',
                'description': 'Document for E2E test case',
                'document_type': 'LEGAL_FORM',
                'status': 'DRAFT'
            }
            
            doc_response = client.post(f'/api/cases/{case_id}/documents',
                                      headers={**login_user, 'Content-Type': 'application/json'},
                                      data=json.dumps(document_data))
            document = json.loads(doc_response.data)
            assert doc_response.status_code == 201
            document_id = document['id']
            
            # Step 4: Add timeline events
            timeline_data = {
                'event_type': 'STATUS_CHANGE',
                'title': 'Case Review Started',
                'description': 'Initial review of case documents',
                'event_date': '2023-08-15T10:00:00'
            }
            
            timeline_response = client.post(f'/api/cases/{case_id}/timeline',
                                          headers={**login_user, 'Content-Type': 'application/json'},
                                          data=json.dumps(timeline_data))
            assert timeline_response.status_code == 201
            
            # Step 5: Update case status
            update_data = {
                'status': 'IN_PROGRESS'
            }
            
            update_response = client.put(f'/api/cases/{case_id}',
                                        headers={**login_user, 'Content-Type': 'application/json'},
                                        data=json.dumps(update_data))
            updated_case = json.loads(update_response.data)
            assert update_response.status_code == 200
            assert updated_case['status'] == 'IN_PROGRESS'
            
            # Step 6: Check case history
            history_response = client.get(f'/api/cases/{case_id}/timeline',
                                         headers=login_user)
            history = json.loads(history_response.data)
            assert history_response.status_code == 200
            assert isinstance(history, list)
            assert len(history) >= 1
            
            # Step 7: Update document status
            doc_update_data = {
                'status': 'FINAL'
            }
            
            doc_update_response = client.put(f'/api/cases/{case_id}/documents/{document_id}',
                                            headers={**login_user, 'Content-Type': 'application/json'},
                                            data=json.dumps(doc_update_data))
            updated_doc = json.loads(doc_update_response.data)
            assert doc_update_response.status_code == 200
            assert updated_doc['status'] == 'FINAL'
            
            # Step 8: Close the case
            close_data = {
                'status': 'CLOSED'
            }
            
            close_response = client.put(f'/api/cases/{case_id}',
                                       headers={**login_user, 'Content-Type': 'application/json'},
                                       data=json.dumps(close_data))
            closed_case = json.loads(close_response.data)
            assert close_response.status_code == 200
            assert closed_case['status'] == 'CLOSED'
    
    def test_document_generation_workflow(self, client, login_user, sample_user):
        """Test the document generation workflow."""
        # Mock the document template engine
        with patch('routes.document_generator.DocumentTemplateEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_engine.return_value = mock_instance
            
            # Configure mock to return expected values
            mock_instance.get_templates.return_value = [
                {
                    'id': 'immigration-form',
                    'name': 'Immigration Assistance Form',
                    'category': 'Immigration'
                }
            ]
            
            mock_instance.get_template_fields.return_value = {
                'sections': [
                    {'title': 'Personal Information'},
                    {'title': 'Immigration Status'}
                ],
                'required_fields': ['applicant_name', 'applicant_dob', 'current_status']
            }
            
            mock_instance.generate_document.return_value = {
                'filename': 'test_document.pdf',
                'path': '/tmp/test_document.pdf',
                'size': 12345
            }
            
            # Step 1: Get available templates
            with patch('routes.document_generator.get_current_user', return_value=sample_user):
                templates_response = client.get('/api/documents/templates',
                                            headers=login_user)
                templates = json.loads(templates_response.data)
                assert templates_response.status_code == 200
                assert len(templates) >= 1
                template_id = templates[0]['id']
                
                # Step 2: Get template fields
                fields_response = client.get(f'/api/documents/templates/{template_id}',
                                          headers=login_user)
                fields = json.loads(fields_response.data)
                assert fields_response.status_code == 200
                assert 'sections' in fields
                assert 'required_fields' in fields
                
                # Step 3: Generate document
                form_data = {
                    'template_id': template_id,
                    'data': {
                        'applicant_name': 'John Doe',
                        'applicant_dob': '1990-01-01',
                        'applicant_nationality': 'Canadian',
                        'current_status': 'Student Visa',
                        'entry_date': '2022-01-15',
                        'passport_number': 'AB123456',
                        'contact_phone': '123-456-7890',
                        'contact_email': 'john.doe@example.com',
                        'assistance_type': 'Visa Renewal'
                    }
                }
                
                generate_response = client.post('/api/documents/generate',
                                             headers={**login_user, 'Content-Type': 'application/json'},
                                             data=json.dumps(form_data))
                document = json.loads(generate_response.data)
                assert generate_response.status_code == 200
                assert 'document_id' in document
                document_id = document['document_id']
                
                # Step 4: Download the generated document
                mock_instance.get_document_path.return_value = '/tmp/test_document.pdf'
                
                # Mock open file
                with patch('builtins.open', return_value=BytesIO(b'PDF content')):
                    download_response = client.get(f'/api/documents/download/{document_id}',
                                              headers=login_user)
                    assert download_response.status_code == 200
                    assert download_response.mimetype == 'application/pdf'
    
    def test_legal_ai_workflow(self, client, login_user, sample_user):
        """Test the legal AI assistant workflow."""
        # Mock the legal assistant service
        with patch('routes.legal_ai.LegalAssistantService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            # Configure mock responses
            mock_instance.get_legal_response_with_citations.return_value = {
                'content': 'As a tenant in New York, you have several rights...',
                'citations': [
                    {'id': 'cite1', 'text': 'NY Tenant Law Sec. 123'}
                ],
                'confidence': 0.92
            }
            
            mock_instance.get_citation_details.return_value = {
                'id': 'cite1',
                'title': 'New York Tenant Law',
                'section': '123',
                'text': 'Tenants have the right to a habitable dwelling...',
                'url': 'https://example.com/ny-tenant-law'
            }
            
            mock_instance.get_legal_resources.return_value = [
                {'title': 'NY Tenant Rights Guide', 'url': 'https://example.com/guide'},
                {'title': 'Legal Aid Society', 'url': 'https://example.com/legal-aid'}
            ]
            
            # Step 1: Send a legal question
            with patch('routes.legal_ai.get_current_user', return_value=sample_user):
                question_data = {
                    'message': 'What are my rights as a tenant in New York?',
                    'jurisdiction': 'New York'
                }
                
                chat_response = client.post('/chat',
                                          headers={**login_user, 'Content-Type': 'application/json'},
                                          data=json.dumps(question_data))
                answer = json.loads(chat_response.data)
                assert chat_response.status_code == 200
                assert 'content' in answer
                assert 'citations' in answer
                citation_id = answer['citations'][0]['id']
                
                # Step 2: Get citation details
                citation_response = client.get(f'/citations/{citation_id}',
                                            headers=login_user)
                citation = json.loads(citation_response.data)
                assert citation_response.status_code == 200
                assert citation['id'] == citation_id
                assert 'title' in citation
                assert 'text' in citation
                
                # Step 3: Get legal resources
                resources_response = client.get('/resources?domain=Housing&jurisdiction=New York',
                                             headers=login_user)
                resources = json.loads(resources_response.data)
                assert resources_response.status_code == 200
                assert isinstance(resources, list)
                assert len(resources) >= 1 
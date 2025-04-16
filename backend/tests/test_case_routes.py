from unittest.mock import patch, MagicMock
import json

class TestCaseRoutes:
    """Test cases for the Case Routes API."""
    
    def test_get_cases(self, client, auth_headers, sample_user, sample_case):
        """Test getting all cases."""
        # Arrange
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.get('/api/cases', headers=auth_headers)
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 200
            assert isinstance(data, list)
            assert len(data) >= 1
            assert data[0]['id'] == sample_case.id
            assert data[0]['title'] == sample_case.title
    
    def test_get_case_by_id(self, client, auth_headers, sample_user, sample_case):
        """Test getting a specific case by ID."""
        # Arrange
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.get(f'/api/cases/{sample_case.id}', headers=auth_headers)
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 200
            assert data['id'] == sample_case.id
            assert data['title'] == sample_case.title
            assert data['client_id'] == sample_user.id
    
    def test_create_case(self, client, auth_headers, sample_user):
        """Test creating a new case."""
        # Arrange
        new_case_data = {
            'title': 'New Test Case',
            'description': 'This is a new test case',
            'case_type': 'FAMILY',
            'status': 'NEW',
            'priority': 'HIGH'
        }
        
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.post('/api/cases', 
                                  headers={**auth_headers, 'Content-Type': 'application/json'},
                                  data=json.dumps(new_case_data))
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 201
            assert data['title'] == new_case_data['title']
            assert data['case_type'] == new_case_data['case_type']
            assert data['client_id'] == sample_user.id
    
    def test_update_case(self, client, auth_headers, sample_user, sample_case):
        """Test updating an existing case."""
        # Arrange
        update_data = {
            'title': 'Updated Case Title',
            'status': 'IN_PROGRESS',
            'priority': 'LOW'
        }
        
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.put(f'/api/cases/{sample_case.id}',
                                 headers={**auth_headers, 'Content-Type': 'application/json'},
                                 data=json.dumps(update_data))
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 200
            assert data['id'] == sample_case.id
            assert data['title'] == update_data['title']
            assert data['status'] == update_data['status']
            assert data['priority'] == update_data['priority']
    
    def test_delete_case(self, client, auth_headers, sample_user, sample_case):
        """Test deleting a case."""
        # Arrange
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.delete(f'/api/cases/{sample_case.id}', headers=auth_headers)
            
            # Assert
            assert response.status_code == 204
            
            # Verify case no longer exists
            get_response = client.get(f'/api/cases/{sample_case.id}', headers=auth_headers)
            assert get_response.status_code == 404
    
    def test_add_timeline_event(self, client, auth_headers, sample_user, sample_case):
        """Test adding a timeline event to a case."""
        # Arrange
        timeline_data = {
            'event_type': 'NOTE',
            'title': 'Important Update',
            'description': 'This is an important update about the case',
            'event_date': '2023-08-15T14:30:00'
        }
        
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.post(f'/api/cases/{sample_case.id}/timeline',
                                  headers={**auth_headers, 'Content-Type': 'application/json'},
                                  data=json.dumps(timeline_data))
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 201
            assert data['case_id'] == sample_case.id
            assert data['event_type'] == timeline_data['event_type']
            assert data['title'] == timeline_data['title']
            assert data['created_by'] == sample_user.id
    
    def test_add_document(self, client, auth_headers, sample_user, sample_case):
        """Test adding a document to a case."""
        # Arrange
        document_data = {
            'title': 'Test Document',
            'description': 'Test document description',
            'document_type': 'LEGAL_FORM',
            'status': 'DRAFT'
        }
        
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.post(f'/api/cases/{sample_case.id}/documents',
                                  headers={**auth_headers, 'Content-Type': 'application/json'},
                                  data=json.dumps(document_data))
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 201
            assert data['title'] == document_data['title']
            assert data['case_id'] == sample_case.id
            assert data['created_by'] == sample_user.id
    
    def test_get_case_documents(self, client, auth_headers, sample_user, sample_case, sample_document):
        """Test getting documents for a case."""
        # Arrange
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.get(f'/api/cases/{sample_case.id}/documents', headers=auth_headers)
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 200
            assert isinstance(data, list)
            assert len(data) >= 1
            assert data[0]['id'] == sample_document.id
            assert data[0]['title'] == sample_document.title
            assert data[0]['case_id'] == sample_case.id
    
    def test_update_document(self, client, auth_headers, sample_user, sample_case, sample_document):
        """Test updating a document."""
        # Arrange
        update_data = {
            'title': 'Updated Document Title',
            'status': 'IN_REVIEW'
        }
        
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.put(f'/api/cases/{sample_case.id}/documents/{sample_document.id}',
                                 headers={**auth_headers, 'Content-Type': 'application/json'},
                                 data=json.dumps(update_data))
            data = json.loads(response.data)
            
            # Assert
            assert response.status_code == 200
            assert data['id'] == sample_document.id
            assert data['title'] == update_data['title']
            assert data['status'] == update_data['status']
    
    def test_delete_document(self, client, auth_headers, sample_user, sample_case, sample_document):
        """Test deleting a document."""
        # Arrange
        with patch('routes.case_routes.get_current_user', return_value=sample_user):
            # Act
            response = client.delete(f'/api/cases/{sample_case.id}/documents/{sample_document.id}', 
                                    headers=auth_headers)
            
            # Assert
            assert response.status_code == 204 
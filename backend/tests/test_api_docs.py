"""Tests for API documentation"""
import pytest
from backend.app import create_app
import json
from flask import url_for

@pytest.fixture
def swagger_json(client):
    """Get Swagger/OpenAPI specification"""
    response = client.get('/api/swagger.json')
    assert response.status_code == 200
    return response.get_json()

def test_swagger_ui_accessible(client):
    """Test Swagger UI is accessible"""
    response = client.get('/api/docs')
    assert response.status_code == 200
    assert b'swagger-ui' in response.data

def test_openapi_spec_valid(swagger_json):
    """Test OpenAPI specification is valid"""
    assert swagger_json['openapi'].startswith('3.')
    assert 'info' in swagger_json
    assert 'paths' in swagger_json
    assert 'components' in swagger_json

def test_required_api_info(swagger_json):
    """Test required API information is present"""
    info = swagger_json['info']
    assert 'title' in info
    assert 'version' in info
    assert 'description' in info

def test_security_schemes(swagger_json):
    """Test security schemes are properly defined"""
    components = swagger_json['components']
    assert 'securitySchemes' in components
    security_schemes = components['securitySchemes']
    assert 'bearerAuth' in security_schemes
    bearer_auth = security_schemes['bearerAuth']
    assert bearer_auth['type'] == 'http'
    assert bearer_auth['scheme'] == 'bearer'

def test_error_responses(swagger_json):
    """Test error responses are documented"""
    paths = swagger_json['paths']
    for path in paths.values():
        for method in path.values():
            assert 'responses' in method
            responses = method['responses']
            # Check common error responses
            assert any(code in responses for code in ['400', '401', '403', '404', '500'])

def test_template_endpoints(swagger_json):
    """Test template endpoints are documented"""
    paths = swagger_json['paths']
    
    # Test GET /api/templates
    assert '/api/templates' in paths
    templates_get = paths['/api/templates']['get']
    assert templates_get['summary']
    assert 'responses' in templates_get
    assert '200' in templates_get['responses']
    
    # Test POST /api/templates/{template_id}
    template_path = '/api/templates/{template_id}'
    assert template_path in paths
    template_post = paths[template_path]['post']
    assert template_post['summary']
    assert 'parameters' in template_post
    assert 'requestBody' in template_post
    assert 'responses' in template_post

def test_schema_definitions(swagger_json):
    """Test schema definitions are present"""
    components = swagger_json['components']
    assert 'schemas' in components
    schemas = components['schemas']
    
    # Check common schemas
    required_schemas = ['Template', 'User', 'Error']
    for schema in required_schemas:
        assert schema in schemas
        assert 'properties' in schemas[schema]

def test_api_tags(swagger_json):
    """Test API endpoints are properly tagged"""
    paths = swagger_json['paths']
    tags = {tag['name'] for tag in swagger_json.get('tags', [])}
    
    for path in paths.values():
        for method in path.values():
            if 'tags' in method:
                for tag in method['tags']:
                    assert tag in tags 
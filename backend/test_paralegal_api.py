import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = 'http://localhost:5003/api'
TOKEN = None  # You'll need to add a valid JWT token here to test authenticated endpoints

def print_response(response):
    """Print the response in a formatted way"""
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
    try:
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Body: {response.text}")
    print("-" * 80)

def test_create_case():
    """Test the create case endpoint"""
    print("\n==== Testing Create Case ====")
    
    if not TOKEN:
        print("No token provided. Skipping authenticated endpoint test.")
        return
    
    headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
    data = {
        'clientName': 'Test Client',
        'clientEmail': 'testclient@example.com',
        'clientPhone': '555-123-4567',
        'caseType': 'Tenant Rights',
        'description': 'This is a test case for API validation',
        'urgency': 'medium',
        'initialConsultDate': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.post(f'{BASE_URL}/paralegal/case', json=data, headers=headers)
        print_response(response)
        
        if response.status_code == 201:
            return response.json().get('case_id')
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def test_get_cases():
    """Test the get cases endpoint"""
    print("\n==== Testing Get Cases ====")
    
    if not TOKEN:
        print("No token provided. Skipping authenticated endpoint test.")
        return
    
    headers = {'Authorization': f'Bearer {TOKEN}'}
    
    try:
        response = requests.get(f'{BASE_URL}/paralegal/cases', headers=headers)
        print_response(response)
    except Exception as e:
        print(f"Error: {str(e)}")

def test_document_templates():
    """Test the document templates endpoint"""
    print("\n==== Testing Get Document Templates ====")
    
    if not TOKEN:
        print("No token provided. Skipping authenticated endpoint test.")
        return
    
    headers = {'Authorization': f'Bearer {TOKEN}'}
    
    try:
        response = requests.get(f'{BASE_URL}/paralegal/templates', headers=headers)
        print_response(response)
    except Exception as e:
        print(f"Error: {str(e)}")

def test_screening_questions():
    """Test the screening questions endpoint"""
    print("\n==== Testing Get Screening Questions ====")
    
    if not TOKEN:
        print("No token provided. Skipping authenticated endpoint test.")
        return
    
    headers = {'Authorization': f'Bearer {TOKEN}'}
    
    try:
        response = requests.get(f'{BASE_URL}/paralegal/screening-questions', headers=headers)
        print_response(response)
    except Exception as e:
        print(f"Error: {str(e)}")

def test_generate_document():
    """Test the generate document endpoint"""
    print("\n==== Testing Generate Document ====")
    
    if not TOKEN:
        print("No token provided. Skipping authenticated endpoint test.")
        return
    
    headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
    
    # First get template IDs
    try:
        response = requests.get(f'{BASE_URL}/paralegal/templates', headers=headers)
        templates = response.json().get('templates', [])
        
        if not templates:
            print("No templates found. Skipping test.")
            return
        
        template_id = templates[0].get('_id')
        data = {
            'clientName': 'Test Client',
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        response = requests.post(f'{BASE_URL}/paralegal/generate-document/{template_id}', 
                                json=data, headers=headers)
        print_response(response)
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Run all tests"""
    print("Starting Paralegal API Tests")
    print("============================")
    
    # Check if a token was provided
    if not TOKEN:
        print("WARNING: No JWT token provided. Authenticated endpoints will be skipped.")
        print("To test authenticated endpoints, add a valid JWT token to the TOKEN variable.")
    
    # Run tests
    case_id = test_create_case()
    test_get_cases()
    test_document_templates()
    test_screening_questions()
    test_generate_document()
    
    print("\nAPI Tests Completed")

if __name__ == "__main__":
    main()


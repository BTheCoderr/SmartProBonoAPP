#!/usr/bin/env python3
"""
Test CRM with Complete Data
Shows the CRM system working with proper data
"""
import requests
import json

def test_crm_with_complete_data():
    """Test CRM with complete, valid data"""
    base_url = "http://localhost:3001/api/v1/crm"
    
    print("🚀 SmartProBono CRM - Complete Data Test")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. 🏥 Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['message']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return
    
    # Test 2: Complete Client Intake
    print("\n2. 📝 Testing Complete Client Intake...")
    try:
        complete_intake_data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com",
            "phone": "555-1234",
            "legal_issue_type": "criminal",
            "case_description": "Need help with traffic violation case",
            "urgency": "medium",
            "address": "123 Main St, Anytown, USA",
            "date_of_birth": "1990-01-01",
            "emergency_contact": "Jane Doe - 555-5678"
        }
        
        response = requests.post(
            f"{base_url}/client/intake",
            json=complete_intake_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Client Intake Created Successfully!")
            print(f"   📋 Client ID: {data.get('id', 'N/A')}")
            print(f"   👤 Name: {data.get('first_name', '')} {data.get('last_name', '')}")
            print(f"   📧 Email: {data.get('email', '')}")
            print(f"   ⚖️ Case Type: {data.get('legal_issue_type', '')}")
            return data.get('id')
        else:
            data = response.json()
            print(f"   ❌ Client Intake Failed: {data.get('error', 'Unknown error')}")
            print(f"   📋 Status Code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Client Intake Error: {e}")
        return None
    
    # Test 3: Get Client Cases (if we have a client_id)
    client_id = test_crm_with_complete_data()
    if client_id:
        print(f"\n3. 📋 Testing Get Client Cases (ID: {client_id})...")
        try:
            response = requests.get(f"{base_url}/client/{client_id}/cases", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Retrieved {len(data)} cases for client")
            else:
                print(f"   ❌ Get client cases failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Get client cases error: {e}")

if __name__ == "__main__":
    test_crm_with_complete_data()

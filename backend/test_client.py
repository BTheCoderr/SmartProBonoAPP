import requests
import json
import sys
from routes.legal_ai import get_static_tenant_rights_response, get_fallback_response

def test_direct_tenant_rights():
    """Test the tenant rights fallback function directly"""
    print("\n=== Testing tenant rights fallback function ===")
    response = get_static_tenant_rights_response()
    print(response)
    
def test_direct_fallback():
    """Test the general fallback function directly"""
    print("\n=== Testing general fallback function ===")
    for _ in range(3):  # Show multiple random responses
        response = get_fallback_response()
        print(f"- {response}")

def test_server(message="What are my basic tenant rights?"):
    """Test sending a message to the server"""
    print(f"\n=== Testing server with message: '{message}' ===")
    url = 'http://localhost:5002/api/legal/chat'
    
    try:
        response = requests.post(
            url,
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS! Server responded with:")
            print(json.dumps(data, indent=2))
        else:
            print(f"ERROR: Server returned status code {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"ERROR: Could not connect to server: {e}")
        print("\nIs the server running? Start it with: python3 app.py")

if __name__ == "__main__":
    # Test the direct functions first (these should always work)
    test_direct_tenant_rights()
    test_direct_fallback()
    
    # If a command-line argument is provided, use it as the message
    if len(sys.argv) > 1:
        test_server(sys.argv[1])
    else:
        # Otherwise, use the default tenant rights query
        test_server() 
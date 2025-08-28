#!/usr/bin/env python3
"""
Test script for JWT authentication
"""
import requests
import json
import sys
import time
from typing import Dict, Any, Optional, Tuple, List

# Configuration
API_URL = "http://localhost:5000"
ENDPOINTS = {
    "register": "/api/auth/register",
    "login": "/api/auth/login",
    "me": "/api/auth/me",
    "refresh": "/api/auth/refresh",
    "logout": "/api/auth/logout",
    "test_auth": "/api/auth/test-auth",
    "test_admin": "/api/auth/test-admin",
}

# Test user data
TEST_USER = {
    "email": "test@example.com",
    "password": "Test1234!",
    "firstName": "Test",
    "lastName": "User",
    "role": "user"
}

TEST_ADMIN = {
    "email": "admin@example.com",
    "password": "Admin1234!",
    "firstName": "Admin",
    "lastName": "User",
    "role": "admin"
}

# Helper functions
def print_response(response: requests.Response) -> None:
    """Print formatted response"""
    print(f"Status: {response.status_code}")
    
    try:
        json_data = response.json()
        print("Response:")
        print(json.dumps(json_data, indent=2))
    except Exception:
        print("Raw response:", response.text)
    
    print("\n" + "-" * 50 + "\n")

def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None
) -> requests.Response:
    """Make HTTP request to the API"""
    url = f"{API_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if method.lower() == "get":
        response = requests.get(url, headers=headers)
    elif method.lower() == "post":
        response = requests.post(url, json=data, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return response

def test_register(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test user registration"""
    print(f"Registering user: {user_data['email']}")
    
    response = make_request("post", ENDPOINTS["register"], user_data)
    print_response(response)
    
    if response.status_code == 201:
        return response.json()
    return {}

def test_login(email: str, password: str) -> Dict[str, Any]:
    """Test user login"""
    print(f"Logging in as: {email}")
    
    response = make_request("post", ENDPOINTS["login"], {
        "email": email,
        "password": password
    })
    print_response(response)
    
    if response.status_code == 200:
        return response.json()
    return {}

def test_me(token: str) -> None:
    """Test get user profile"""
    print("Getting user profile")
    
    response = make_request("get", ENDPOINTS["me"], token=token)
    print_response(response)

def test_protected(token: str) -> None:
    """Test protected endpoint"""
    print("Testing protected endpoint")
    
    response = make_request("get", ENDPOINTS["test_auth"], token=token)
    print_response(response)

def test_admin_endpoint(token: str) -> None:
    """Test admin-only endpoint"""
    print("Testing admin-only endpoint")
    
    response = make_request("get", ENDPOINTS["test_admin"], token=token)
    print_response(response)

def test_refresh(refresh_token: str) -> Dict[str, Any]:
    """Test token refresh"""
    print("Testing token refresh")
    
    response = make_request("post", ENDPOINTS["refresh"], token=refresh_token)
    print_response(response)
    
    if response.status_code == 200:
        return response.json()
    return {}

def test_logout(token: str) -> None:
    """Test user logout"""
    print("Testing logout")
    
    response = make_request("post", ENDPOINTS["logout"], token=token)
    print_response(response)

def run_tests() -> None:
    """Run all authentication tests"""
    # Test user registration
    register_result = test_register(TEST_USER)
    
    if not register_result:
        print("Registration failed or user already exists. Trying login.")
        login_result = test_login(TEST_USER["email"], TEST_USER["password"])
    else:
        login_result = register_result
    
    if not login_result:
        print("Login failed. Cannot continue tests.")
        return
    
    # Extract tokens
    access_token = login_result.get("access_token")
    refresh_token = login_result.get("refresh_token")
    
    if not access_token or not refresh_token:
        print("Missing tokens. Cannot continue tests.")
        return
    
    # Test protected endpoints
    test_me(access_token)
    test_protected(access_token)
    
    # Test admin endpoint (should fail for regular user)
    test_admin_endpoint(access_token)
    
    # Test token refresh
    refresh_result = test_refresh(refresh_token)
    new_token = refresh_result.get("access_token")
    
    if new_token:
        print("Testing with refreshed token")
        test_protected(new_token)
    
    # Test admin registration and admin-only endpoint
    print("\nTesting admin user flow\n")
    admin_register = test_register(TEST_ADMIN)
    
    if not admin_register:
        print("Admin registration failed or admin already exists. Trying login.")
        admin_login = test_login(TEST_ADMIN["email"], TEST_ADMIN["password"])
    else:
        admin_login = admin_register
    
    if admin_login:
        admin_token = admin_login.get("access_token")
        if admin_token:
            test_admin_endpoint(admin_token)
    
    # Test logout
    test_logout(access_token)
    
    # Verify token is invalidated
    print("Verifying token is invalidated")
    test_protected(access_token)

if __name__ == "__main__":
    run_tests() 
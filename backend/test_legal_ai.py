#!/usr/bin/env python3
"""
Test Script for SmartProBono Legal AI Assistant
This script verifies that the Legal AI Assistant is functioning correctly.
"""

import argparse
import requests
import json
import time
import sys
import os
from pprint import pprint
from typing import Dict, Any, List, Optional
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init()

# Default server URL
DEFAULT_URL = "http://localhost:5000"

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}== {text}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}")
    
def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")
    
def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")
    
def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")
    
def print_info(text: str) -> None:
    """Print an info message."""
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")

class LegalAITester:
    """Tester for the Legal AI Assistant."""
    
    def __init__(self, base_url: str = DEFAULT_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.success_count = 0
        self.failure_count = 0
        self.warning_count = 0
        
    def test_jurisdictions(self) -> Dict[str, Any]:
        """Test getting available jurisdictions."""
        print_header("Testing jurisdictions endpoint")
        
        try:
            response = self.session.get(f"{self.base_url}/api/legal/jurisdictions")
            response.raise_for_status()
            result = response.json()
            
            print_success(f"Successfully retrieved {len(result['jurisdictions'])} jurisdictions")
            print_info("Sample jurisdictions: " + ", ".join(result['jurisdictions'][:5]))
            
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to get jurisdictions: {str(e)}")
            self.failure_count += 1
            return {"error": str(e), "jurisdictions": []}
            
    def test_domains(self) -> Dict[str, Any]:
        """Test getting legal domains."""
        print_header("Testing domains endpoint")
        
        try:
            response = self.session.get(f"{self.base_url}/api/legal/domains")
            response.raise_for_status()
            result = response.json()
            
            print_success(f"Successfully retrieved {len(result['domains'])} legal domains")
            print_info("Available domains: " + ", ".join(result['domains']))
            
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to get domains: {str(e)}")
            self.failure_count += 1
            return {"error": str(e), "domains": []}
            
    def test_models(self) -> Dict[str, Any]:
        """Test getting available models."""
        print_header("Testing models endpoint")
        
        try:
            response = self.session.get(f"{self.base_url}/api/legal/models")
            response.raise_for_status()
            result = response.json()
            
            print_success(f"Successfully retrieved {len(result['models'])} AI models")
            for model in result['models'][:3]:  # Show first 3 models
                print_info(f"Model: {model['name']} - {model['description']}")
            
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to get models: {str(e)}")
            self.failure_count += 1
            return {"error": str(e), "models": []}
            
    def test_analyze(self, query: str) -> Dict[str, Any]:
        """Test legal query analysis."""
        print_header("Testing analyze endpoint")
        print_info(f"Query: {query}")
        
        try:
            data = {"query": query}
            response = self.session.post(
                f"{self.base_url}/api/legal/analyze",
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            print_success("Successfully analyzed legal query")
            print_info(f"Detected domain: {result.get('domain', 'Unknown')}")
            print_info(f"Confidence: {result.get('confidence', 0):.2f}")
            if result.get('jurisdiction'):
                print_info(f"Detected jurisdiction: {result['jurisdiction']}")
            
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to analyze query: {str(e)}")
            self.failure_count += 1
            return {"error": str(e)}
            
    def test_chat(self, message: str, jurisdiction: Optional[str] = None, model_id: Optional[str] = None) -> Dict[str, Any]:
        """Test the legal chat endpoint."""
        print_header("Testing chat endpoint")
        print_info(f"Message: {message}")
        if jurisdiction:
            print_info(f"Jurisdiction: {jurisdiction}")
        if model_id:
            print_info(f"Model: {model_id}")
            
        try:
            data = {
                "message": message,
                "jurisdiction": jurisdiction,
                "model_id": model_id
            }
            
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            # Record start time
            start_time = time.time()
            
            response = self.session.post(
                f"{self.base_url}/api/legal/chat",
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            # Calculate response time
            elapsed_time = time.time() - start_time
            
            print_success(f"Successfully got response in {elapsed_time:.2f}s")
            
            # Show snippet of response
            if result.get('response'):
                response_text = result['response'].get('text', '')
                if len(response_text) > 200:
                    print_info(f"Response snippet: {response_text[:200]}...")
                else:
                    print_info(f"Response: {response_text}")
                    
            # Show citations if available
            citations = result.get('response', {}).get('citations', [])
            if citations:
                print_info(f"Retrieved {len(citations)} citations")
                for i, citation in enumerate(citations[:2]):  # Show first 2 citations
                    print_info(f"  Citation {i+1}: {citation.get('text', 'Unknown')}")
                    
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to get chat response: {str(e)}")
            self.failure_count += 1
            return {"error": str(e)}
            
    def test_resources(self, domain: str, jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        """Test getting legal resources."""
        print_header("Testing resources endpoint")
        print_info(f"Domain: {domain}")
        if jurisdiction:
            print_info(f"Jurisdiction: {jurisdiction}")
            
        try:
            params = {
                "domain": domain
            }
            if jurisdiction:
                params["jurisdiction"] = jurisdiction
                
            response = self.session.get(
                f"{self.base_url}/api/legal/resources",
                params=params
            )
            response.raise_for_status()
            result = response.json()
            
            print_success(f"Successfully retrieved {len(result['resources'])} resources")
            for i, resource in enumerate(result['resources'][:3]):  # Show first 3 resources
                print_info(f"  Resource {i+1}: {resource.get('name')} - {resource.get('description', '')[:50]}")
                
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to get resources: {str(e)}")
            self.failure_count += 1
            return {"error": str(e), "resources": []}

    def test_citation_details(self, citation_id: str) -> Dict[str, Any]:
        """Test getting citation details."""
        print_header("Testing citation details endpoint")
        print_info(f"Citation ID: {citation_id}")
        
        try:
            response = self.session.get(f"{self.base_url}/api/legal/citations/{citation_id}")
            response.raise_for_status()
            result = response.json()
            
            print_success("Successfully retrieved citation details")
            print_info(f"Citation text: {result.get('citation', {}).get('text', 'Unknown')}")
            print_info(f"Type: {result.get('citation', {}).get('type', 'Unknown')}")
            print_info(f"Jurisdiction: {result.get('citation', {}).get('jurisdiction', 'Unknown')}")
            
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to get citation details: {str(e)}")
            self.failure_count += 1
            return {"error": str(e)}
            
    def test_specialized_chat(self, message: str, domain: str, jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        """Test specialized legal chat."""
        print_header("Testing specialized chat endpoint")
        print_info(f"Message: {message}")
        print_info(f"Domain: {domain}")
        if jurisdiction:
            print_info(f"Jurisdiction: {jurisdiction}")
            
        try:
            data = {
                "message": message,
                "domain": domain
            }
            if jurisdiction:
                data["jurisdiction"] = jurisdiction
                
            # Record start time
            start_time = time.time()
            
            response = self.session.post(
                f"{self.base_url}/api/legal/chat/specialized",
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            # Calculate response time
            elapsed_time = time.time() - start_time
            
            print_success(f"Successfully got specialized response in {elapsed_time:.2f}s")
            
            # Show snippet of response
            if result.get('response'):
                response_text = result['response'].get('text', '')
                if len(response_text) > 200:
                    print_info(f"Response snippet: {response_text[:200]}...")
                else:
                    print_info(f"Response: {response_text}")
            
            # Check for cache hit
            if result.get('response', {}).get('metadata', {}).get('cache_hit'):
                print_info("Response was retrieved from cache")
                
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to get specialized chat response: {str(e)}")
            self.failure_count += 1
            return {"error": str(e)}
            
    def test_document_analysis(self, text: str) -> Dict[str, Any]:
        """Test legal document analysis."""
        print_header("Testing document analysis")
        print_info(f"Analyzing text: {text[:100]}...")
        
        try:
            data = {"text": text}
            
            response = self.session.post(
                f"{self.base_url}/api/legal/analyze/document",
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            print_success("Successfully analyzed document")
            print_info(f"Document type: {result.get('document_type', 'Unknown')}")
            print_info(f"Key entities: {', '.join(result.get('entities', [])[:5])}")
            
            self.success_count += 1
            return result
        except Exception as e:
            print_error(f"Failed to analyze document: {str(e)}")
            self.failure_count += 1
            return {"error": str(e)}
            
    def test_cache_performance(self, message: str) -> Dict[str, Any]:
        """Test caching performance by querying twice."""
        print_header("Testing cache performance")
        print_info(f"Message: {message}")
        
        try:
            # First request (should be uncached)
            start_time1 = time.time()
            response1 = self.session.post(
                f"{self.base_url}/api/legal/chat",
                json={"message": message}
            )
            response1.raise_for_status()
            result1 = response1.json()
            elapsed_time1 = time.time() - start_time1
            
            # Second request (should be cached)
            start_time2 = time.time()
            response2 = self.session.post(
                f"{self.base_url}/api/legal/chat",
                json={"message": message}
            )
            response2.raise_for_status()
            result2 = response2.json()
            elapsed_time2 = time.time() - start_time2
            
            cache_hit = result2.get('response', {}).get('metadata', {}).get('cache_hit', False)
            
            if cache_hit:
                print_success("Cache hit on second request")
                print_info(f"First request: {elapsed_time1:.2f}s")
                print_info(f"Second request: {elapsed_time2:.2f}s")
                print_info(f"Speed improvement: {(elapsed_time1/elapsed_time2):.1f}x faster")
                self.success_count += 1
            else:
                print_warning("Cache miss on second request")
                print_info(f"First request: {elapsed_time1:.2f}s")
                print_info(f"Second request: {elapsed_time2:.2f}s")
                self.warning_count += 1
                
            return {
                "first_request": result1,
                "second_request": result2,
                "first_time": elapsed_time1,
                "second_time": elapsed_time2,
                "cache_hit": cache_hit
            }
        except Exception as e:
            print_error(f"Failed to test cache: {str(e)}")
            self.failure_count += 1
            return {"error": str(e)}
            
    def run_all_tests(self, jurisdiction: Optional[str] = None):
        """Run all test cases."""
        print_header("STARTING COMPREHENSIVE LEGAL AI TESTS")
        print_info(f"Server URL: {self.base_url}")
        print_info(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Basic endpoints
        self.test_jurisdictions()
        self.test_domains()
        self.test_models()
        
        # Test analysis
        self.test_analyze("What are my rights as a tenant in California?")
        
        # Test chat
        chat_result = self.test_chat(
            "Can my landlord evict me without notice?", 
            jurisdiction=jurisdiction
        )
        
        # Get a citation from the response to test citation details
        citations = chat_result.get('response', {}).get('citations', [])
        if citations:
            citation_id = citations[0].get('id')
            if citation_id:
                self.test_citation_details(citation_id)
        
        # Test specialized chat
        self.test_specialized_chat(
            "What documents do I need for a green card application?",
            domain="immigration",
            jurisdiction=jurisdiction
        )
        
        # Test resources
        self.test_resources("tenant_rights", jurisdiction=jurisdiction)
        
        # Test document analysis
        sample_lease = """RESIDENTIAL LEASE AGREEMENT
        This Lease Agreement ("Lease") is entered into on January 1, 2023, by and between
        John Smith ("Landlord") and Jane Doe ("Tenant").
        
        1. PROPERTY: Landlord leases to Tenant the residential property located at
        123 Main Street, Apt 4B, Anytown, CA 90210 ("Premises").
        
        2. TERM: The lease term begins on January 1, 2023 and ends on December 31, 2023.
        
        3. RENT: Tenant agrees to pay $2,000 per month, due on the 1st of each month.
        """
        self.test_document_analysis(sample_lease)
        
        # Test cache performance 
        self.test_cache_performance("What is the eviction process in New York?")
        
        # Test specialized chat again to check caching
        self.test_specialized_chat(
            "What documents do I need for a green card application?",
            domain="immigration",
            jurisdiction=jurisdiction
        )
            
        # Summary results
        print_header("TEST SUMMARY")
        print_info(f"Tests run: {self.success_count + self.failure_count + self.warning_count}")
        print_success(f"Successful: {self.success_count}")
        print_warning(f"Warnings: {self.warning_count}")
        print_error(f"Failed: {self.failure_count}")
        
        if self.failure_count == 0:
            print_success("\nALL TESTS PASSED!")
        else:
            print_error(f"\n{self.failure_count} TESTS FAILED")

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Test the Legal AI Assistant")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"API server URL (default: {DEFAULT_URL})")
    parser.add_argument("--jurisdiction", help="Specify a jurisdiction for testing")
    parser.add_argument("--query", help="Specific query to test")
    parser.add_argument("--test", choices=[
        "all", "jurisdictions", "domains", "models", "analyze", 
        "chat", "specialized", "resources", "citations", "cache"
    ], default="all", help="Specific test to run")
    
    args = parser.parse_args()
    
    tester = LegalAITester(args.url)
    
    if args.test == "all":
        tester.run_all_tests(args.jurisdiction)
    elif args.test == "jurisdictions":
        tester.test_jurisdictions()
    elif args.test == "domains":
        tester.test_domains()
    elif args.test == "models":
        tester.test_models()
    elif args.test == "analyze":
        query = args.query or "What are my tenant rights in California?"
        tester.test_analyze(query)
    elif args.test == "chat":
        query = args.query or "Can a landlord enter my apartment without permission?"
        tester.test_chat(query, jurisdiction=args.jurisdiction)
    elif args.test == "specialized":
        query = args.query or "What are the requirements for filing for divorce?"
        tester.test_specialized_chat(query, domain="family", jurisdiction=args.jurisdiction)
    elif args.test == "resources":
        tester.test_resources("tenant_rights", jurisdiction=args.jurisdiction)
    elif args.test == "cache":
        query = args.query or "What are my rights as an employee?"
        tester.test_cache_performance(query)
        
    print_info(f"\nTests completed. {tester.success_count} passed, {tester.failure_count} failed.")

if __name__ == "__main__":
    main() 
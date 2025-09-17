#!/usr/bin/env python3
"""
Debug script to check what Flask routes are actually registered
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.combined_server import app

def list_routes():
    """List all registered Flask routes"""
    print("🔍 Registered Flask Routes:")
    print("=" * 50)
    
    routes = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        routes.append({
            'endpoint': rule.endpoint,
            'methods': methods,
            'rule': rule.rule
        })
    
    # Sort by rule
    routes.sort(key=lambda x: x['rule'])
    
    for route in routes:
        print(f"{route['methods']:<10} {route['rule']:<40} -> {route['endpoint']}")
    
    print(f"\n📊 Total routes: {len(routes)}")
    
    # Test some key routes
    print("\n🧪 Testing Key Routes:")
    print("-" * 30)
    
    test_routes = [
        '/api/health',
        '/api/scanner/health', 
        '/api/generator/health',
        '/api/analytics/user',
        '/api/voice/status',
        '/api/court-filing/rules'
    ]
    
    with app.test_client() as client:
        for route in test_routes:
            try:
                response = client.get(route)
                status = "✅" if response.status_code == 200 else f"❌ {response.status_code}"
                print(f"{status} {route}")
            except Exception as e:
                print(f"❌ {route} - Error: {e}")

if __name__ == "__main__":
    list_routes()

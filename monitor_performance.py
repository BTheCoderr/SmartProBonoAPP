#!/usr/bin/env python3
"""
SmartProBono Performance Monitor
Monitors system resources and prevents freezing
"""

import psutil
import time
import requests
import json
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.cpu_threshold = 80  # CPU usage threshold
        self.memory_threshold = 85  # Memory usage threshold
        self.response_time_threshold = 10  # Response time threshold in seconds
        
    def check_system_resources(self):
        """Check CPU and memory usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        status = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / (1024**3),
            'timestamp': datetime.now().isoformat()
        }
        
        # Check thresholds
        if cpu_percent > self.cpu_threshold:
            status['warning'] = f"High CPU usage: {cpu_percent}%"
        if memory.percent > self.memory_threshold:
            status['warning'] = f"High memory usage: {memory.percent}%"
            
        return status
    
    def check_ollama_performance(self):
        """Check Ollama response times"""
        try:
            start_time = time.time()
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:0.5b",
                    "prompt": "Hello",
                    "stream": False,
                    "options": {"num_predict": 10}
                },
                timeout=5
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'response_time': response_time,
                    'model_loaded': True
                }
            else:
                return {
                    'status': 'error',
                    'response_time': response_time,
                    'error': f"HTTP {response.status_code}"
                }
        except requests.exceptions.Timeout:
            return {
                'status': 'timeout',
                'response_time': 5.0,
                'error': 'Ollama timeout'
            }
        except Exception as e:
            return {
                'status': 'error',
                'response_time': 0,
                'error': str(e)
            }
    
    def check_backend_health(self):
        """Check backend API health"""
        try:
            start_time = time.time()
            response = requests.get("http://localhost:8081/api/health", timeout=3)
            response_time = time.time() - start_time
            
            return {
                'status': 'healthy' if response.status_code == 200 else 'error',
                'response_time': response_time,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'status': 'error',
                'response_time': 0,
                'error': str(e)
            }
    
    def get_recommendations(self, system_status, ollama_status, backend_status):
        """Get performance recommendations"""
        recommendations = []
        
        # System recommendations
        if system_status.get('cpu_percent', 0) > 80:
            recommendations.append("🔴 High CPU usage - Consider closing other applications")
        if system_status.get('memory_percent', 0) > 85:
            recommendations.append("🔴 High memory usage - Consider restarting services")
        
        # Ollama recommendations
        if ollama_status.get('status') == 'timeout':
            recommendations.append("🟡 Ollama timeout - Try using a smaller model like qwen2.5:0.5b")
        if ollama_status.get('response_time', 0) > 5:
            recommendations.append("🟡 Slow Ollama response - Model may need to be pre-loaded")
        
        # Backend recommendations
        if backend_status.get('status') == 'error':
            recommendations.append("🔴 Backend error - Check backend.log for details")
        
        if not recommendations:
            recommendations.append("✅ All systems performing well!")
        
        return recommendations
    
    def run_monitor(self):
        """Run the performance monitor"""
        print("🔍 SmartProBono Performance Monitor")
        print("=" * 50)
        
        while True:
            try:
                # Check all systems
                system_status = self.check_system_resources()
                ollama_status = self.check_ollama_performance()
                backend_status = self.check_backend_health()
                
                # Display status
                print(f"\n📊 Status at {datetime.now().strftime('%H:%M:%S')}")
                print(f"💻 CPU: {system_status['cpu_percent']:.1f}% | Memory: {system_status['memory_percent']:.1f}%")
                print(f"🤖 Ollama: {ollama_status['status']} ({ollama_status.get('response_time', 0):.2f}s)")
                print(f"🔧 Backend: {backend_status['status']} ({backend_status.get('response_time', 0):.2f}s)")
                
                # Show recommendations
                recommendations = self.get_recommendations(system_status, ollama_status, backend_status)
                for rec in recommendations:
                    print(f"   {rec}")
                
                # Check for critical issues
                if system_status.get('cpu_percent', 0) > 90 or system_status.get('memory_percent', 0) > 90:
                    print("🚨 CRITICAL: System resources exhausted!")
                    print("   Consider stopping some services or restarting")
                
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                print("\n👋 Performance monitor stopped")
                break
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    monitor.run_monitor()

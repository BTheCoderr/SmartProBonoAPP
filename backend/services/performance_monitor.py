import time
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from config.ai_config import MONITORING_CONFIG

class PerformanceMonitor:
    def __init__(self):
        self.config = MONITORING_CONFIG
        self.ensure_log_directory()

    def ensure_log_directory(self):
        """Ensure log directory exists"""
        if not os.path.exists(self.config['log_directory']):
            os.makedirs(self.config['log_directory'])

    def start_request(self) -> float:
        """Start timing a request"""
        return time.time()

    def log_request(self,
                   model: str,
                   task_type: str,
                   start_time: float,
                   response: Optional[str] = None,
                   error: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log request performance metrics
        """
        if not self.config['enabled']:
            return

        end_time = time.time()
        duration = end_time - start_time

        metrics = {
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'task_type': task_type,
            'response_time': duration,
            'success': error is None,
            'error': error if error else None,
            'token_count': len(response.split()) if response else 0,
            'metadata': metadata or {}
        }

        # Write to daily log file
        log_file = os.path.join(
            self.config['log_directory'],
            f"performance_{datetime.now().strftime('%Y%m%d')}.json"
        )

        try:
            existing_logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)
            
            existing_logs.append(metrics)
            
            with open(log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)

        except Exception as e:
            print(f"Error logging performance metrics: {str(e)}")

    def get_model_performance(self, model: str, timeframe: str = 'today') -> Dict[str, Any]:
        """
        Get performance metrics for a specific model
        """
        try:
            # Determine which log file to read based on timeframe
            if timeframe == 'today':
                log_file = os.path.join(
                    self.config['log_directory'],
                    f"performance_{datetime.now().strftime('%Y%m%d')}.json"
                )
            else:
                raise ValueError(f"Unsupported timeframe: {timeframe}")

            if not os.path.exists(log_file):
                return {
                    'average_response_time': 0,
                    'success_rate': 0,
                    'total_requests': 0,
                    'error_rate': 0
                }

            with open(log_file, 'r') as f:
                logs = json.load(f)

            # Filter logs for specific model
            model_logs = [log for log in logs if log['model'] == model]
            
            if not model_logs:
                return {
                    'average_response_time': 0,
                    'success_rate': 0,
                    'total_requests': 0,
                    'error_rate': 0
                }

            total_requests = len(model_logs)
            successful_requests = len([log for log in model_logs if log['success']])
            total_response_time = sum(log['response_time'] for log in model_logs)

            return {
                'average_response_time': total_response_time / total_requests,
                'success_rate': (successful_requests / total_requests) * 100,
                'total_requests': total_requests,
                'error_rate': ((total_requests - successful_requests) / total_requests) * 100
            }

        except Exception as e:
            print(f"Error getting model performance: {str(e)}")
            return {
                'average_response_time': 0,
                'success_rate': 0,
                'total_requests': 0,
                'error_rate': 0
            }

# Create singleton instance
performance_monitor = PerformanceMonitor() 
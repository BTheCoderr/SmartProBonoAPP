from typing import Dict, Any

ANALYTICS_CONFIG = {
    'google_analytics': {
        'property_id': 'YOUR_GA4_PROPERTY_ID',  # Format: G-XXXXXXXXXX
        'measurement_id': 'YOUR_MEASUREMENT_ID',
        'api_secret': 'YOUR_API_SECRET',
        'service_account_key_path': 'path/to/service-account-key.json',
        'sampling_rate': 100,  # Percentage of requests to track
        'retention_period_days': 14,
    },
    
    'custom_metrics': {
        'enabled': True,
        'log_directory': 'logs/metrics',
        'retention_period_days': 30,
    },
    
    'performance_thresholds': {
        'response_time_ms': 1000,  # Alert if response time > 1000ms
        'error_rate_percent': 5,    # Alert if error rate > 5%
        'memory_usage_percent': 80, # Alert if memory usage > 80%
        'cpu_usage_percent': 70,    # Alert if CPU usage > 70%
        'concurrent_users': 100,    # Alert if concurrent users > 100
    },
    
    'document_processing': {
        'generation_timeout_sec': 30,
        'max_retries': 3,
        'success_rate_threshold': 95,  # Alert if success rate < 95%
    },
    
    'custom_events': {
        'document_generation': {
            'sampling_rate': 100,
            'attributes': ['document_type', 'template_id', 'user_id', 'processing_time']
        },
        'form_submission': {
            'sampling_rate': 100,
            'attributes': ['form_type', 'completion_time', 'step_count']
        },
        'user_session': {
            'sampling_rate': 100,
            'attributes': ['duration', 'pages_visited', 'actions_performed']
        },
        'search_query': {
            'sampling_rate': 50,  # Track 50% of search queries
            'attributes': ['query_text', 'results_count', 'category']
        }
    },
    
    'alerts': {
        'email': {
            'enabled': True,
            'recipients': ['admin@smartprobono.com'],
            'cooldown_minutes': 15,  # Minimum time between similar alerts
        },
        'slack': {
            'enabled': False,
            'webhook_url': 'YOUR_SLACK_WEBHOOK_URL',
            'channel': '#monitoring-alerts'
        }
    }
} 
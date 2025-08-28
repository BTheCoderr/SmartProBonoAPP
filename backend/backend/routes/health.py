"""Health check endpoints for the application."""
from flask import Blueprint, jsonify, render_template_string, current_app, request
import platform
import psutil
import os
import sys
import logging
from datetime import datetime
import pkg_resources

logger = logging.getLogger(__name__)
bp = Blueprint('health', __name__, url_prefix='/api/health')

# HTML template for health dashboard
HEALTH_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartProBono API Health Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
            color: #333;
        }
        .dashboard {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-healthy {
            background-color: #2ecc71;
        }
        .status-degraded {
            background-color: #f39c12;
        }
        .status-unhealthy {
            background-color: #e74c3c;
        }
        .summary {
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #eee;
        }
        .summary-item {
            text-align: center;
        }
        .summary-item .value {
            font-size: 22px;
            font-weight: bold;
            margin: 5px 0;
        }
        .summary-item .label {
            font-size: 14px;
            color: #7f8c8d;
        }
        .section {
            padding: 20px;
            border-bottom: 1px solid #eee;
        }
        .section h2 {
            margin-top: 0;
            color: #2c3e50;
            font-size: 18px;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }
        .card {
            background: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .card h3 {
            margin-top: 0;
            font-size: 16px;
            color: #34495e;
        }
        .status-table {
            width: 100%;
            border-collapse: collapse;
        }
        .status-table th, .status-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        .status-table th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        .endpoint-list {
            list-style: none;
            padding: 0;
        }
        .endpoint-list li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .footer {
            text-align: center;
            padding: 15px;
            color: #7f8c8d;
            font-size: 13px;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-get {
            background-color: #3498db;
            color: white;
        }
        .badge-post {
            background-color: #2ecc71;
            color: white;
        }
        .badge-put {
            background-color: #f39c12;
            color: white;
        }
        .badge-delete {
            background-color: #e74c3c;
            color: white;
        }
        .refresh-button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .refresh-button:hover {
            background-color: #2980b9;
        }
        @media (max-width: 768px) {
            .summary {
                flex-direction: column;
            }
            .summary-item {
                margin-bottom: 15px;
            }
            .card-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>
                <span class="status-indicator {{ 'status-healthy' if status == 'healthy' else 'status-degraded' if status == 'degraded' else 'status-unhealthy' }}"></span>
                SmartProBono API Health Dashboard
            </h1>
            <p>Status: <strong>{{ status.upper() }}</strong></p>
        </div>
        
        <div class="summary">
            <div class="summary-item">
                <div class="label">Uptime</div>
                <div class="value">{{ system_info.uptime }}</div>
            </div>
            <div class="summary-item">
                <div class="label">CPU Usage</div>
                <div class="value">{{ system_info.cpu_usage }}%</div>
            </div>
            <div class="summary-item">
                <div class="label">Memory Usage</div>
                <div class="value">{{ system_info.memory_usage }}%</div>
            </div>
            <div class="summary-item">
                <div class="label">Python Version</div>
                <div class="value">{{ system_info.python_version }}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Service Status</h2>
            <table class="status-table">
                <thead>
                    <tr>
                        <th>Service</th>
                        <th>Status</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {% for service_name, service_status in services.items() %}
                    <tr>
                        <td>{{ service_name }}</td>
                        <td>
                            <span class="status-indicator {{ 'status-healthy' if service_status == 'healthy' else 'status-degraded' if service_status == 'degraded' else 'status-unhealthy' }}"></span>
                            {{ service_status }}
                        </td>
                        <td>
                            {% if service_name in details %}
                                {{ details[service_name] }}
                            {% else %}
                                -
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>System Information</h2>
            <div class="card-grid">
                <div class="card">
                    <h3>Environment</h3>
                    <p><strong>OS:</strong> {{ system_info.os }}</p>
                    <p><strong>Host:</strong> {{ system_info.hostname }}</p>
                    <p><strong>Python:</strong> {{ system_info.python_version }}</p>
                    <p><strong>Flask:</strong> {{ system_info.flask_version }}</p>
                </div>
                
                <div class="card">
                    <h3>Resources</h3>
                    <p><strong>CPU Cores:</strong> {{ system_info.cpu_count }}</p>
                    <p><strong>Memory Total:</strong> {{ system_info.memory_total }}</p>
                    <p><strong>Memory Available:</strong> {{ system_info.memory_available }}</p>
                    <p><strong>Disk Usage:</strong> {{ system_info.disk_usage }}%</p>
                </div>
                
                <div class="card">
                    <h3>Application</h3>
                    <p><strong>Environment:</strong> {{ system_info.environment }}</p>
                    <p><strong>Debug Mode:</strong> {{ "Yes" if system_info.debug else "No" }}</p>
                    <p><strong>Start Time:</strong> {{ system_info.start_time }}</p>
                    <p><strong>Current Time:</strong> {{ system_info.current_time }}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Available Endpoints</h2>
            <ul class="endpoint-list">
                {% for endpoint in endpoints %}
                <li>
                    <span class="badge badge-{{ endpoint.method|lower }}">{{ endpoint.method }}</span>
                    {{ endpoint.url }}
                    {% if endpoint.description %}
                    <div style="margin-left: 10px; color: #7f8c8d; font-size: 13px;">
                        {{ endpoint.description }}
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="footer">
            <p>Generated on {{ system_info.current_time }}</p>
            <button class="refresh-button" onclick="window.location.reload()">Refresh Dashboard</button>
        </div>
    </div>
</body>
</html>
"""

def get_system_info():
    """Get system information for health dashboard"""
    try:
        # Get memory info
        memory = psutil.virtual_memory()
        memory_total = f"{memory.total / (1024 * 1024 * 1024):.2f} GB"
        memory_available = f"{memory.available / (1024 * 1024 * 1024):.2f} GB"
        
        # Get disk info for current drive
        disk = psutil.disk_usage('/')
        
        # Get process info
        process = psutil.Process(os.getpid())
        process_start_time = datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
        
        # Calculate uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        days, seconds = uptime.days, uptime.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        
        # Get Flask version
        try:
            flask_version = pkg_resources.get_distribution('flask').version
        except:
            flask_version = "Unknown"
        
        return {
            'hostname': platform.node(),
            'os': f"{platform.system()} {platform.release()}",
            'python_version': platform.python_version(),
            'flask_version': flask_version,
            'cpu_count': psutil.cpu_count(),
            'cpu_usage': f"{psutil.cpu_percent(interval=0.1)}",
            'memory_total': memory_total,
            'memory_available': memory_available,
            'memory_usage': f"{memory.percent}",
            'disk_usage': f"{disk.percent}",
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'debug': current_app.debug,
            'start_time': process_start_time,
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'uptime': uptime_str
        }
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        return {
            'hostname': "Unknown",
            'os': "Unknown",
            'python_version': platform.python_version(),
            'flask_version': "Unknown",
            'cpu_count': "Unknown",
            'cpu_usage': "Unknown",
            'memory_total': "Unknown",
            'memory_available': "Unknown",
            'memory_usage': "Unknown",
            'disk_usage': "Unknown",
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'debug': current_app.debug,
            'start_time': "Unknown",
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'uptime': "Unknown"
        }

def get_registered_endpoints():
    """Get a list of registered endpoints in the application"""
    endpoints = []
    
    for rule in current_app.url_map.iter_rules():
        endpoints.append({
            'url': rule.rule,
            'method': list(rule.methods - {'HEAD', 'OPTIONS'})[0] if rule.methods else 'GET',
            'description': getattr(current_app.view_functions.get(rule.endpoint), '__doc__', None)
        })
    
    # Sort endpoints by URL
    return sorted(endpoints, key=lambda x: x['url'])

@bp.route('/', methods=['GET'])
def health_check():
    """Comprehensive health check endpoint that checks all critical services"""
    health_status = {
        'status': 'healthy',
        'services': {
            'api': 'healthy',
        },
        'details': {}
    }
    
    # Check database connections if possible
    try:
        from extensions import db
        db.session.execute('SELECT 1')
        health_status['services']['database'] = 'healthy'
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status['services']['database'] = 'unhealthy'
        health_status['details']['database'] = str(e)
        health_status['status'] = 'degraded'
    
    # Check MongoDB connection if possible
    try:
        from extensions import mongo
        mongo.db.command('ping')
        health_status['services']['mongodb'] = 'healthy'
    except Exception as e:
        logger.error(f"MongoDB health check failed: {str(e)}")
        health_status['services']['mongodb'] = 'unhealthy'
        health_status['details']['mongodb'] = str(e)
        health_status['status'] = 'degraded'
        
    # Get system info for dashboard
    system_info = get_system_info()
    endpoints = get_registered_endpoints()
    
    # Check if request wants JSON response
    if request.headers.get('Accept') == 'application/json':
        return jsonify({
            'status': health_status['status'],
            'services': health_status['services'],
            'details': health_status['details'],
            'system_info': system_info
        })
    
    # Otherwise render HTML dashboard
    return render_template_string(
        HEALTH_DASHBOARD_TEMPLATE,
        status=health_status['status'],
        services=health_status['services'],
        details=health_status['details'],
        system_info=system_info,
        endpoints=endpoints
    )

@bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint for basic connectivity check"""
    return jsonify({
        'status': 'ok',
        'message': 'pong',
        'timestamp': datetime.now().isoformat()
    }) 
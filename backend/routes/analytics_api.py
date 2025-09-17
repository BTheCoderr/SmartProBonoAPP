"""
Analytics API Routes
Provides endpoints for advanced analytics and reporting
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
try:
    from backend.services.analytics_service import create_analytics_service, TimeRange
    from backend.database import get_db_session
except ImportError:
    from services.analytics_service import create_analytics_service, TimeRange
    from database import get_db_session
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('analytics', __name__)

@bp.route('/analytics/user', methods=['GET'])
def get_user_analytics():
    """Get user analytics"""
    try:
        # Get query parameters
        time_range = request.args.get('time_range', 'day')
        user_id = request.args.get('user_id', type=int)
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            return jsonify({
                'error': 'Invalid time_range. Must be one of: hour, day, week, month, quarter, year',
                'success': False
            }), 400
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Get analytics
        analytics = analytics_service.get_user_analytics(time_range_enum, user_id)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        logger.error(f"Error getting user analytics: {e}")
        return jsonify({
            'error': f'Failed to get user analytics: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/performance', methods=['GET'])
def get_performance_analytics():
    """Get system performance analytics"""
    try:
        # Get query parameters
        time_range = request.args.get('time_range', 'day')
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            return jsonify({
                'error': 'Invalid time_range. Must be one of: hour, day, week, month, quarter, year',
                'success': False
            }), 400
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Get analytics
        analytics = analytics_service.get_system_performance_analytics(time_range_enum)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        logger.error(f"Error getting performance analytics: {e}")
        return jsonify({
            'error': f'Failed to get performance analytics: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/business', methods=['GET'])
def get_business_analytics():
    """Get business analytics and KPIs"""
    try:
        # Get query parameters
        time_range = request.args.get('time_range', 'day')
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            return jsonify({
                'error': 'Invalid time_range. Must be one of: hour, day, week, month, quarter, year',
                'success': False
            }), 400
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Get analytics
        analytics = analytics_service.get_business_analytics(time_range_enum)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        logger.error(f"Error getting business analytics: {e}")
        return jsonify({
            'error': f'Failed to get business analytics: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/security', methods=['GET'])
def get_security_analytics():
    """Get security analytics"""
    try:
        # Get query parameters
        time_range = request.args.get('time_range', 'day')
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            return jsonify({
                'error': 'Invalid time_range. Must be one of: hour, day, week, month, quarter, year',
                'success': False
            }), 400
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Get analytics
        analytics = analytics_service.get_security_analytics(time_range_enum)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        logger.error(f"Error getting security analytics: {e}")
        return jsonify({
            'error': f'Failed to get security analytics: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/comprehensive', methods=['GET'])
def get_comprehensive_analytics():
    """Get comprehensive analytics report"""
    try:
        # Get query parameters
        time_range = request.args.get('time_range', 'day')
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            return jsonify({
                'error': 'Invalid time_range. Must be one of: hour, day, week, month, quarter, year',
                'success': False
            }), 400
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Generate comprehensive report
        report = analytics_service.generate_comprehensive_report(time_range_enum)
        
        if not report:
            return jsonify({
                'error': 'Failed to generate comprehensive report',
                'success': False
            }), 500
        
        return jsonify({
            'success': True,
            'report': {
                'report_id': report.report_id,
                'report_type': report.report_type,
                'title': report.title,
                'description': report.description,
                'data': report.data,
                'generated_at': report.generated_at.isoformat(),
                'time_range': report.time_range.value,
                'filters': report.filters
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting comprehensive analytics: {e}")
        return jsonify({
            'error': f'Failed to get comprehensive analytics: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/track/activity', methods=['POST'])
def track_user_activity():
    """Track user activity for analytics"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'activity_type' not in data:
            return jsonify({
                'error': 'Missing required fields: user_id, activity_type',
                'success': False
            }), 400
        
        user_id = data['user_id']
        activity_type = data['activity_type']
        details = data.get('details', {})
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Track activity
        analytics_service.track_user_activity(user_id, activity_type, details)
        
        return jsonify({
            'success': True,
            'message': 'Activity tracked successfully'
        })
        
    except Exception as e:
        logger.error(f"Error tracking user activity: {e}")
        return jsonify({
            'error': f'Failed to track user activity: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/track/performance', methods=['POST'])
def track_system_performance():
    """Track system performance metrics"""
    try:
        data = request.get_json()
        
        if not data or 'metric_name' not in data or 'value' not in data:
            return jsonify({
                'error': 'Missing required fields: metric_name, value',
                'success': False
            }), 400
        
        metric_name = data['metric_name']
        value = data['value']
        dimensions = data.get('dimensions', {})
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Track performance metric
        analytics_service.track_system_performance(metric_name, value, dimensions)
        
        return jsonify({
            'success': True,
            'message': 'Performance metric tracked successfully'
        })
        
    except Exception as e:
        logger.error(f"Error tracking system performance: {e}")
        return jsonify({
            'error': f'Failed to track system performance: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/track/business', methods=['POST'])
def track_business_metric():
    """Track business metrics"""
    try:
        data = request.get_json()
        
        if not data or 'metric_name' not in data or 'value' not in data:
            return jsonify({
                'error': 'Missing required fields: metric_name, value',
                'success': False
            }), 400
        
        metric_name = data['metric_name']
        value = data['value']
        dimensions = data.get('dimensions', {})
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Track business metric
        analytics_service.track_business_metric(metric_name, value, dimensions)
        
        return jsonify({
            'success': True,
            'message': 'Business metric tracked successfully'
        })
        
    except Exception as e:
        logger.error(f"Error tracking business metric: {e}")
        return jsonify({
            'error': f'Failed to track business metric: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get dashboard data with key metrics"""
    try:
        # Get query parameters
        time_range = request.args.get('time_range', 'day')
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            return jsonify({
                'error': 'Invalid time_range. Must be one of: hour, day, week, month, quarter, year',
                'success': False
            }), 400
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Get all analytics
        user_analytics = analytics_service.get_user_analytics(time_range_enum)
        performance_analytics = analytics_service.get_system_performance_analytics(time_range_enum)
        business_analytics = analytics_service.get_business_analytics(time_range_enum)
        security_analytics = analytics_service.get_security_analytics(time_range_enum)
        
        # Create dashboard data
        dashboard_data = {
            'time_range': time_range,
            'key_metrics': {
                'total_users': business_analytics.get('total_users', 0),
                'new_users': business_analytics.get('new_users', 0),
                'total_activities': user_analytics.get('total_activities', 0),
                'system_health': performance_analytics.get('overall_health_score', 0),
                'security_score': security_analytics.get('security_score', 0),
                'critical_events': security_analytics.get('critical_events', 0)
            },
            'charts': {
                'user_activity': user_analytics.get('hourly_distribution', {}),
                'activity_types': user_analytics.get('activity_types', {}),
                'performance_metrics': performance_analytics.get('metrics_by_type', {}),
                'security_events': security_analytics.get('events_by_severity', {})
            },
            'alerts': {
                'performance_issues': performance_analytics.get('performance_issues', []),
                'security_events': security_analytics.get('events_by_type', {}),
                'system_health': performance_analytics.get('overall_health_score', 0) < 80
            }
        }
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        return jsonify({
            'error': f'Failed to get dashboard data: {str(e)}',
            'success': False
        }), 500

@bp.route('/analytics/export', methods=['GET'])
def export_analytics():
    """Export analytics data"""
    try:
        # Get query parameters
        time_range = request.args.get('time_range', 'day')
        format_type = request.args.get('format', 'json')  # json, csv, xlsx
        
        # Validate time range
        try:
            time_range_enum = TimeRange(time_range)
        except ValueError:
            return jsonify({
                'error': 'Invalid time_range. Must be one of: hour, day, week, month, quarter, year',
                'success': False
            }), 400
        
        # Get database session
        db_session = get_db_session()
        analytics_service = create_analytics_service(db_session)
        
        # Generate comprehensive report
        report = analytics_service.generate_comprehensive_report(time_range_enum)
        
        if not report:
            return jsonify({
                'error': 'Failed to generate report for export',
                'success': False
            }), 500
        
        # For now, return JSON format
        # In production, you would implement CSV/Excel export
        return jsonify({
            'success': True,
            'export_data': report.data,
            'format': format_type,
            'exported_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error exporting analytics: {e}")
        return jsonify({
            'error': f'Failed to export analytics: {str(e)}',
            'success': False
        }), 500

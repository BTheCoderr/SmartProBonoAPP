"""
Audit API endpoints for viewing and managing audit logs.
"""
import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.audit_service import audit_service
from models.audit import AuditEventType, AuditSeverity
from utils.audit_decorators import audit_route, security_audit, data_access_audit

logger = logging.getLogger(__name__)

# Create blueprint
audit_bp = Blueprint('audit', __name__, url_prefix='/api/audit')

@audit_bp.route('/logs', methods=['GET'])
@jwt_required()
@security_audit(action="VIEW_AUDIT_LOGS")
@audit_route(event_type=AuditEventType.SYSTEM, action="VIEW_AUDIT_LOGS")
def get_audit_logs():
    """Get audit logs with filtering options."""
    try:
        # Check admin permissions
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        # Parse query parameters
        event_type = request.args.get('event_type')
        user_id = request.args.get('user_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 100, type=int)
        severity = request.args.get('severity')
        
        # Convert date strings to datetime objects
        start_datetime = None
        end_datetime = None
        
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid start_date format"}), 400
        
        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid end_date format"}), 400
        
        # Convert string to enum
        event_type_enum = None
        if event_type:
            try:
                event_type_enum = AuditEventType(event_type)
            except ValueError:
                return jsonify({"error": "Invalid event_type"}), 400
        
        # Get audit logs
        logs = audit_service.get_audit_logs(
            event_type=event_type_enum,
            user_id=user_id,
            start_date=start_datetime,
            end_date=end_datetime,
            limit=limit
        )
        
        # Convert to JSON-serializable format
        logs_data = []
        for log in logs:
            logs_data.append({
                "id": log.id,
                "event_type": log.event_type.value,
                "severity": log.severity.value,
                "user_id": log.user_id,
                "session_id": log.session_id,
                "ip_address": log.ip_address,
                "endpoint": log.endpoint,
                "method": log.method,
                "status_code": log.status_code,
                "action": log.action,
                "description": log.description,
                "processing_time_ms": log.processing_time_ms,
                "resource_id": log.resource_id,
                "resource_type": log.resource_type,
                "error_message": log.error_message,
                "created_at": log.created_at.isoformat(),
                "metadata": log.metadata_dict,
                "request_data": log.request_data_dict,
                "response_data": log.response_data_dict
            })
        
        return jsonify({
            "status": "success",
            "data": logs_data,
            "count": len(logs_data),
            "filters": {
                "event_type": event_type,
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit,
                "severity": severity
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting audit logs: {str(e)}")
        return jsonify({"error": "Failed to retrieve audit logs"}), 500

@audit_bp.route('/security-events', methods=['GET'])
@jwt_required()
@security_audit(action="VIEW_SECURITY_EVENTS")
@audit_route(event_type=AuditEventType.SECURITY, action="VIEW_SECURITY_EVENTS")
def get_security_events():
    """Get security events with filtering options."""
    try:
        # Check admin permissions
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        # Parse query parameters
        severity = request.args.get('severity')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 100, type=int)
        
        # Convert date strings to datetime objects
        start_datetime = None
        end_datetime = None
        
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid start_date format"}), 400
        
        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid end_date format"}), 400
        
        # Convert string to enum
        severity_enum = None
        if severity:
            try:
                severity_enum = AuditSeverity(severity)
            except ValueError:
                return jsonify({"error": "Invalid severity"}), 400
        
        # Get security events
        events = audit_service.get_security_events(
            severity=severity_enum,
            start_date=start_datetime,
            end_date=end_datetime,
            limit=limit
        )
        
        # Convert to JSON-serializable format
        events_data = []
        for event in events:
            events_data.append({
                "id": event.id,
                "event_type": event.event_type,
                "severity": event.severity.value,
                "user_id": event.user_id,
                "ip_address": event.ip_address,
                "endpoint": event.endpoint,
                "attack_type": event.attack_type,
                "blocked": event.blocked,
                "reason": event.reason,
                "response_action": event.response_action,
                "created_at": event.created_at.isoformat(),
                "metadata": event.metadata_dict
            })
        
        return jsonify({
            "status": "success",
            "data": events_data,
            "count": len(events_data),
            "filters": {
                "severity": severity,
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting security events: {str(e)}")
        return jsonify({"error": "Failed to retrieve security events"}), 500

@audit_bp.route('/user-activities/<int:user_id>', methods=['GET'])
@jwt_required()
@security_audit(action="VIEW_USER_ACTIVITIES")
@audit_route(event_type=AuditEventType.USER_ACTIVITY, action="VIEW_USER_ACTIVITIES")
def get_user_activities(user_id):
    """Get user activities for a specific user."""
    try:
        # Check permissions - users can only view their own activities, admins can view all
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        if claims.get('role') != 'admin' and current_user_id != user_id:
            return jsonify({"error": "Access denied"}), 403
        
        # Parse query parameters
        activity_type = request.args.get('activity_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 100, type=int)
        
        # Convert date strings to datetime objects
        start_datetime = None
        end_datetime = None
        
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid start_date format"}), 400
        
        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid end_date format"}), 400
        
        # Get user activities
        activities = audit_service.get_user_activities(
            user_id=user_id,
            activity_type=activity_type,
            start_date=start_datetime,
            end_date=end_datetime,
            limit=limit
        )
        
        # Convert to JSON-serializable format
        activities_data = []
        for activity in activities:
            activities_data.append({
                "id": activity.id,
                "user_id": activity.user_id,
                "session_id": activity.session_id,
                "activity_type": activity.activity_type,
                "page_url": activity.page_url,
                "page_title": activity.page_title,
                "action": activity.action,
                "element_id": activity.element_id,
                "element_class": activity.element_class,
                "duration_seconds": activity.duration_seconds,
                "referrer": activity.referrer,
                "ip_address": activity.ip_address,
                "device_type": activity.device_type,
                "browser": activity.browser,
                "os": activity.os,
                "created_at": activity.created_at.isoformat(),
                "metadata": activity.metadata_dict
            })
        
        return jsonify({
            "status": "success",
            "data": activities_data,
            "count": len(activities_data),
            "user_id": user_id,
            "filters": {
                "activity_type": activity_type,
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting user activities: {str(e)}")
        return jsonify({"error": "Failed to retrieve user activities"}), 500

@audit_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@security_audit(action="VIEW_AUDIT_DASHBOARD")
@audit_route(event_type=AuditEventType.SYSTEM, action="VIEW_AUDIT_DASHBOARD")
def get_audit_dashboard_stats():
    """Get audit dashboard statistics."""
    try:
        # Check admin permissions
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        # Get time range (default to last 24 hours)
        hours = request.args.get('hours', 24, type=int)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # Import models for queries
        from models.audit import AuditLog, SecurityEvent, UserActivity, PerformanceMetric
        
        # Get basic statistics
        total_audit_logs = AuditLog.query.filter(
            AuditLog.created_at >= start_time
        ).count()
        
        total_security_events = SecurityEvent.query.filter(
            SecurityEvent.created_at >= start_time
        ).count()
        
        total_user_activities = UserActivity.query.filter(
            UserActivity.created_at >= start_time
        ).count()
        
        # Get security events by severity
        security_by_severity = {}
        for severity in AuditSeverity:
            count = SecurityEvent.query.filter(
                SecurityEvent.created_at >= start_time,
                SecurityEvent.severity == severity
            ).count()
            security_by_severity[severity.value] = count
        
        # Get audit events by type
        events_by_type = {}
        for event_type in AuditEventType:
            count = AuditLog.query.filter(
                AuditLog.created_at >= start_time,
                AuditLog.event_type == event_type
            ).count()
            events_by_type[event_type.value] = count
        
        # Get performance metrics
        avg_response_time = PerformanceMetric.query.filter(
            PerformanceMetric.created_at >= start_time,
            PerformanceMetric.metric_type == "response_time"
        ).with_entities(
            db.func.avg(PerformanceMetric.value)
        ).scalar() or 0
        
        # Get top endpoints by usage
        from database import db
        top_endpoints = db.session.query(
            AuditLog.endpoint,
            db.func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= start_time,
            AuditLog.endpoint.isnot(None)
        ).group_by(AuditLog.endpoint).order_by(
            db.func.count(AuditLog.id).desc()
        ).limit(10).all()
        
        return jsonify({
            "status": "success",
            "data": {
                "time_range": {
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "hours": hours
                },
                "totals": {
                    "audit_logs": total_audit_logs,
                    "security_events": total_security_events,
                    "user_activities": total_user_activities
                },
                "security_by_severity": security_by_severity,
                "events_by_type": events_by_type,
                "performance": {
                    "avg_response_time_ms": round(avg_response_time, 2)
                },
                "top_endpoints": [
                    {"endpoint": endpoint, "count": count}
                    for endpoint, count in top_endpoints
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting audit dashboard stats: {str(e)}")
        return jsonify({"error": "Failed to retrieve audit dashboard stats"}), 500

@audit_bp.route('/export', methods=['POST'])
@jwt_required()
@security_audit(action="EXPORT_AUDIT_LOGS")
@audit_route(event_type=AuditEventType.SYSTEM, action="EXPORT_AUDIT_LOGS")
def export_audit_logs():
    """Export audit logs to CSV format."""
    try:
        # Check admin permissions
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body required"}), 400
        
        # Parse export parameters
        event_type = data.get('event_type')
        user_id = data.get('user_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        format_type = data.get('format', 'csv')  # csv, json
        
        # Convert date strings to datetime objects
        start_datetime = None
        end_datetime = None
        
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid start_date format"}), 400
        
        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid end_date format"}), 400
        
        # Convert string to enum
        event_type_enum = None
        if event_type:
            try:
                event_type_enum = AuditEventType(event_type)
            except ValueError:
                return jsonify({"error": "Invalid event_type"}), 400
        
        # Get audit logs
        logs = audit_service.get_audit_logs(
            event_type=event_type_enum,
            user_id=user_id,
            start_date=start_datetime,
            end_date=end_datetime,
            limit=10000  # Large limit for export
        )
        
        if format_type == 'csv':
            # Generate CSV content
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'ID', 'Event Type', 'Severity', 'User ID', 'Session ID',
                'IP Address', 'Endpoint', 'Method', 'Status Code', 'Action',
                'Description', 'Processing Time (ms)', 'Resource ID',
                'Resource Type', 'Error Message', 'Created At'
            ])
            
            # Write data
            for log in logs:
                writer.writerow([
                    log.id, log.event_type.value, log.severity.value,
                    log.user_id, log.session_id, log.ip_address,
                    log.endpoint, log.method, log.status_code, log.action,
                    log.description, log.processing_time_ms, log.resource_id,
                    log.resource_type, log.error_message, log.created_at.isoformat()
                ])
            
            csv_content = output.getvalue()
            output.close()
            
            return jsonify({
                "status": "success",
                "data": {
                    "format": "csv",
                    "content": csv_content,
                    "count": len(logs),
                    "filename": f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                }
            })
        
        else:  # JSON format
            logs_data = []
            for log in logs:
                logs_data.append({
                    "id": log.id,
                    "event_type": log.event_type.value,
                    "severity": log.severity.value,
                    "user_id": log.user_id,
                    "session_id": log.session_id,
                    "ip_address": log.ip_address,
                    "endpoint": log.endpoint,
                    "method": log.method,
                    "status_code": log.status_code,
                    "action": log.action,
                    "description": log.description,
                    "processing_time_ms": log.processing_time_ms,
                    "resource_id": log.resource_id,
                    "resource_type": log.resource_type,
                    "error_message": log.error_message,
                    "created_at": log.created_at.isoformat(),
                    "metadata": log.metadata_dict
                })
            
            return jsonify({
                "status": "success",
                "data": {
                    "format": "json",
                    "content": logs_data,
                    "count": len(logs_data)
                }
            })
        
    except Exception as e:
        logger.error(f"Error exporting audit logs: {str(e)}")
        return jsonify({"error": "Failed to export audit logs"}), 500

@audit_bp.route('/alerts/configure', methods=['POST'])
@jwt_required()
@security_audit(action="CONFIGURE_AUDIT_ALERTS")
@audit_route(event_type=AuditEventType.SYSTEM, action="CONFIGURE_AUDIT_ALERTS")
def configure_audit_alerts():
    """Configure audit alert settings."""
    try:
        # Check admin permissions
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body required"}), 400
        
        # TODO: Implement alert configuration storage
        # This would typically store alert settings in a database table
        
        return jsonify({
            "status": "success",
            "message": "Alert configuration updated",
            "data": data
        })
        
    except Exception as e:
        logger.error(f"Error configuring audit alerts: {str(e)}")
        return jsonify({"error": "Failed to configure audit alerts"}), 500

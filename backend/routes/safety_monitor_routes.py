from flask import Blueprint, request, jsonify
import logging
import json
import os
import random
import time
from datetime import datetime
from services.priority_queue_service import priority_queue_service

# Create a blueprint for safety monitor routes
safety_monitor_bp = Blueprint('safety_monitor', __name__)
logger = logging.getLogger(__name__)

# Mock data store for safety status - in production this would be a database
SAFETY_STATUSES = {}
COMPANIONS = {}
SOS_ALERTS = {}
SAFETY_CHAT_MESSAGES = {}

@safety_monitor_bp.route('/status/<case_id>', methods=['GET'])
def get_safety_status(case_id):
    """Get safety status for a specific case"""
    if case_id not in SAFETY_STATUSES:
        SAFETY_STATUSES[case_id] = {
            "location_sharing": False,
            "current_location": None,
            "last_updated": datetime.now().isoformat(),
            "safety_level": "NORMAL",
            "active_sos": False
        }
    
    return jsonify(SAFETY_STATUSES[case_id])

@safety_monitor_bp.route('/status/<case_id>', methods=['POST'])
def update_safety_status(case_id):
    """Update safety status for a specific case"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Get current status or initialize
        if case_id not in SAFETY_STATUSES:
            SAFETY_STATUSES[case_id] = {
                "location_sharing": False,
                "current_location": None,
                "last_updated": datetime.now().isoformat(),
                "safety_level": "NORMAL",
                "active_sos": False
            }
        
        # Update fields provided in request
        for key in ["location_sharing", "current_location", "safety_level"]:
            if key in data:
                SAFETY_STATUSES[case_id][key] = data[key]
        
        # Always update the timestamp
        SAFETY_STATUSES[case_id]["last_updated"] = datetime.now().isoformat()
        
        # Log for audit
        log_safety_event(case_id, "STATUS_UPDATE", data.get("user_id", "unknown"), data)
        
        return jsonify(SAFETY_STATUSES[case_id])
    except Exception as e:
        logger.error(f"Error updating safety status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@safety_monitor_bp.route('/sos/<case_id>', methods=['POST'])
def trigger_sos(case_id):
    """Trigger an SOS alert for a specific case"""
    try:
        data = request.json or {}
        
        # Create SOS alert
        sos_id = f"SOS-{int(time.time())}-{random.randint(1000, 9999)}"
        
        SOS_ALERTS[sos_id] = {
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "location": data.get("location"),
            "message": data.get("message", "Client needs immediate assistance"),
            "user_id": data.get("user_id", "unknown"),
            "status": "ACTIVE"
        }
        
        # Update case safety status
        if case_id not in SAFETY_STATUSES:
            SAFETY_STATUSES[case_id] = {
                "location_sharing": False,
                "current_location": data.get("location"),
                "last_updated": datetime.now().isoformat(),
                "safety_level": "EMERGENCY",
                "active_sos": True
            }
        else:
            SAFETY_STATUSES[case_id]["safety_level"] = "EMERGENCY"
            SAFETY_STATUSES[case_id]["active_sos"] = True
            SAFETY_STATUSES[case_id]["last_updated"] = datetime.now().isoformat()
            if data.get("location"):
                SAFETY_STATUSES[case_id]["current_location"] = data.get("location")
        
        # Log for audit
        log_safety_event(case_id, "SOS_TRIGGERED", data.get("user_id", "unknown"), {
            "sos_id": sos_id,
            "message": data.get("message", "Client needs immediate assistance"),
            "location": data.get("location")
        })
        
        # In a real application, we would also:
        # 1. Send notifications to support team
        # 2. Escalate to emergency services if needed
        # 3. Notify companions
        
        return jsonify({
            "sos_id": sos_id,
            "status": "ACTIVE",
            "timestamp": datetime.now().isoformat(),
            "message": "SOS alert has been triggered. Support team has been notified."
        })
    except Exception as e:
        logger.error(f"Error triggering SOS alert: {str(e)}")
        return jsonify({"error": str(e)}), 500

@safety_monitor_bp.route('/sos/<case_id>/cancel', methods=['POST'])
def cancel_sos(case_id):
    """Cancel active SOS alerts for a specific case"""
    try:
        data = request.json or {}
        
        # Find active SOS alerts for this case
        active_sos = [sos_id for sos_id, sos in SOS_ALERTS.items() 
                     if sos["case_id"] == case_id and sos["status"] == "ACTIVE"]
        
        # Mark them as canceled
        for sos_id in active_sos:
            SOS_ALERTS[sos_id]["status"] = "CANCELED"
        
        # Update case safety status
        if case_id in SAFETY_STATUSES:
            SAFETY_STATUSES[case_id]["safety_level"] = "NORMAL"
            SAFETY_STATUSES[case_id]["active_sos"] = False
            SAFETY_STATUSES[case_id]["last_updated"] = datetime.now().isoformat()
        
        # Log for audit
        log_safety_event(case_id, "SOS_CANCELED", data.get("user_id", "unknown"), {
            "canceled_sos_count": len(active_sos)
        })
        
        return jsonify({
            "canceled_alerts": len(active_sos),
            "status": "CANCELED",
            "timestamp": datetime.now().isoformat(),
            "message": "All SOS alerts have been canceled."
        })
    except Exception as e:
        logger.error(f"Error canceling SOS alert: {str(e)}")
        return jsonify({"error": str(e)}), 500

@safety_monitor_bp.route('/companion/<case_id>', methods=['POST'])
def add_companion(case_id):
    """Add a safety companion for a specific case"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ["name", "phone", "relationship"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Initialize companions list if not exists
        if case_id not in COMPANIONS:
            COMPANIONS[case_id] = []
        
        # Generate companion ID
        companion_id = f"COMP-{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Add companion
        companion = {
            "id": companion_id,
            "name": data["name"],
            "phone": data["phone"],
            "relationship": data["relationship"],
            "email": data.get("email"),
            "added_at": datetime.now().isoformat(),
            "status": "ACTIVE"
        }
        
        COMPANIONS[case_id].append(companion)
        
        # Log for audit
        log_safety_event(case_id, "COMPANION_ADDED", data.get("user_id", "unknown"), {
            "companion_id": companion_id,
            "name": data["name"],
            "relationship": data["relationship"]
        })
        
        return jsonify({
            "companion_id": companion_id,
            "status": "added",
            "message": f"Companion {data['name']} has been added successfully."
        })
    except Exception as e:
        logger.error(f"Error adding companion: {str(e)}")
        return jsonify({"error": str(e)}), 500

@safety_monitor_bp.route('/companion/<case_id>', methods=['GET'])
def get_companions(case_id):
    """Get safety companions for a specific case"""
    companions = COMPANIONS.get(case_id, [])
    return jsonify({
        "companions": companions,
        "count": len(companions)
    })

@safety_monitor_bp.route('/companion/<case_id>/<companion_id>', methods=['DELETE'])
def remove_companion(case_id, companion_id):
    """Remove a safety companion"""
    if case_id not in COMPANIONS:
        return jsonify({"error": "Case not found"}), 404
    
    companions = COMPANIONS[case_id]
    for i, comp in enumerate(companions):
        if comp["id"] == companion_id:
            removed = companions.pop(i)
            
            # Log for audit
            log_safety_event(case_id, "COMPANION_REMOVED", request.args.get("user_id", "unknown"), {
                "companion_id": companion_id,
                "name": removed["name"]
            })
            
            return jsonify({
                "status": "removed",
                "message": f"Companion {removed['name']} has been removed."
            })
    
    return jsonify({"error": "Companion not found"}), 404

@safety_monitor_bp.route('/chat/<case_id>', methods=['GET'])
def get_messages(case_id):
    """Get safety chat messages for a specific case"""
    messages = SAFETY_CHAT_MESSAGES.get(case_id, [])
    return jsonify({
        "messages": messages,
        "count": len(messages)
    })

@safety_monitor_bp.route('/chat/<case_id>', methods=['POST'])
def send_message(case_id):
    """Send a message in the safety chat"""
    try:
        data = request.json
        
        if not data or "content" not in data:
            return jsonify({"error": "No message content provided"}), 400
        
        # Initialize messages list if not exists
        if case_id not in SAFETY_CHAT_MESSAGES:
            SAFETY_CHAT_MESSAGES[case_id] = []
        
        # Create message object
        message = {
            "id": f"MSG-{int(time.time())}-{random.randint(1000, 9999)}",
            "content": data["content"],
            "sender": data.get("sender", "client"),
            "sender_id": data.get("sender_id", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "type": data.get("type", "text")
        }
        
        # Add message
        SAFETY_CHAT_MESSAGES[case_id].append(message)
        
        # If this is a message from a client, generate a system/support response
        if data.get("sender", "client") == "client":
            # Wait a bit to simulate response time
            time.sleep(0.5)
            
            # Generate a mock response
            response = generate_safety_response(message["content"])
            
            response_msg = {
                "id": f"MSG-{int(time.time())}-{random.randint(1000, 9999)}",
                "content": response,
                "sender": "support",
                "sender_id": "support-team",
                "timestamp": datetime.now().isoformat(),
                "type": "text"
            }
            
            # Add response
            SAFETY_CHAT_MESSAGES[case_id].append(response_msg)
            
            # Return both messages
            return jsonify({
                "message": message,
                "response": response_msg
            })
        
        return jsonify({
            "message": message,
            "status": "sent"
        })
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return jsonify({"error": str(e)}), 500

@safety_monitor_bp.route('/audit/<case_id>', methods=['GET'])
def get_audit_logs(case_id):
    """Get safety audit logs for a specific case"""
    # In a real application, this would fetch from a database
    # For demo, we'll generate mock audit logs
    logs = generate_mock_audit_logs(case_id)
    return jsonify({
        "logs": logs,
        "count": len(logs)
    })

# Helper functions
def log_safety_event(case_id, event_type, user_id, details):
    """Log safety events for audit purposes"""
    # In a real application, this would write to a database
    logger.info(f"SAFETY EVENT: {event_type} | Case: {case_id} | User: {user_id} | Details: {json.dumps(details)}")

def generate_safety_response(message_content):
    """Generate a response from the support team"""
    # In a real application, this would be handled by real support staff
    # For demo, we'll use simple keyword matching
    message = message_content.lower()
    
    if "sos" in message or "emergency" in message or "help" in message:
        return "I understand you need urgent assistance. I've escalated this to our emergency response team. Is there anything specific you need right now?"
    
    if "location" in message:
        return "Your location has been received. The support team can now see where you are. Stay safe and keep us updated."
    
    if "scared" in message or "afraid" in message or "unsafe" in message:
        return "I understand you're feeling unsafe. Your safety is our priority. Would you like me to contact emergency services? Or is there someone from your contact list we should reach out to?"
    
    # Default response
    return "Thank you for your message. Our support team is monitoring your situation. Is there anything specific you need assistance with?"

def generate_mock_audit_logs(case_id):
    """Generate mock audit logs for demo purposes"""
    # In a real application, these would come from a database
    now = datetime.now()
    return [
        {
            "id": f"LOG-{i}",
            "timestamp": datetime.now().isoformat(),
            "event_type": event,
            "user_id": user,
            "details": details
        }
        for i, (event, user, details) in enumerate([
            ("SAFETY_MONITOR_ACTIVATED", "lawyer-1", {"initiated_by": "legal team"}),
            ("LOCATION_SHARING_ENABLED", "client-1", {"accuracy": "high"}),
            ("COMPANION_ADDED", "client-1", {"name": "Emergency Contact", "relationship": "Family"}),
            ("CHAT_MESSAGE_SENT", "client-1", {"message_count": 3}),
            ("CHAT_MESSAGE_SENT", "support-1", {"message_count": 2}),
            ("STATUS_UPDATE", "client-1", {"safety_level": "NORMAL"}),
            ("LOCATION_UPDATE", "client-1", {"accuracy": "medium"})
        ])
    ] 
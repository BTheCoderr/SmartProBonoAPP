from flask import Blueprint, request, jsonify
import logging
import json
import os
import random
import time
from datetime import datetime
from services.priority_queue_service import priority_queue_service

# Create a blueprint for emergency legal support routes
emergency_legal_support_bp = Blueprint('emergency_legal', __name__)
logger = logging.getLogger(__name__)

# Mock data for simulating lawyer availability - in production this would come from a database
MOCK_LAWYERS = [
    {"id": "L1001", "name": "Jane Smith", "specialties": ["criminal", "police_encounters"], "availability": True},
    {"id": "L1002", "name": "Robert Johnson", "specialties": ["housing", "eviction"], "availability": True},
    {"id": "L1003", "name": "Maria Rodriguez", "specialties": ["immigration", "deportation"], "availability": False},
    {"id": "L1004", "name": "David Kim", "specialties": ["civil_rights", "discrimination"], "availability": True},
    {"id": "L1005", "name": "Sarah Lee", "specialties": ["family", "domestic_violence"], "availability": False},
]

# Mock data for lawyer availability
lawyers = [
    {"id": 1, "name": "Jane Smith", "status": "available"},
    {"id": 2, "name": "John Doe", "status": "busy"},
    {"id": 3, "name": "Alice Johnson", "status": "offline"}
]

# Dictionary to store call status information
call_logs = {}

# Priority mapping for different situation types
SITUATION_PRIORITIES = {
    'police': 'URGENT',
    'rights': 'HIGH',
    'eviction': 'HIGH',
    'housing': 'HIGH',
    'immigration': 'MEDIUM',
    'legal_document': 'LOW',
    'court': 'MEDIUM',
    'other': 'MEDIUM'
}

@emergency_legal_support_bp.route('/availability', methods=['GET'])
def get_availability():
    """Get current availability of legal advocates"""
    # Get queue status for more accurate wait times
    queue_status = priority_queue_service.get_queue_status()
    
    # Calculate wait times based on queue status and mock lawyer data
    total_lawyers = len(MOCK_LAWYERS)
    available_lawyers = sum(1 for lawyer in MOCK_LAWYERS if lawyer["availability"])
    
    # Get priority breakdown from queue
    priority_breakdown = queue_status['priority_breakdown']
    
    # Calculate estimated wait times based on queue length and lawyer availability
    urgent_cases = priority_breakdown.get('URGENT', 0)
    high_cases = priority_breakdown.get('HIGH', 0)
    medium_cases = priority_breakdown.get('MEDIUM', 0)
    low_cases = priority_breakdown.get('LOW', 0)
    
    # Simple wait time calculation based on case load and lawyer availability
    wait_factor = max(1, (urgent_cases + high_cases + medium_cases + low_cases) / (available_lawyers or 1))
    
    wait_times = {
        "urgent": "1-3 minutes" if wait_factor <= 1 else "3-5 minutes",
        "high": "5-10 minutes" if wait_factor <= 1 else "10-15 minutes",
        "medium": "10-15 minutes" if wait_factor <= 1 else "15-30 minutes",
        "low": "15-30 minutes" if wait_factor <= 1 else "30-45 minutes"
    }
    
    return jsonify({
        "available_lawyers": available_lawyers,
        "total_lawyers": total_lawyers,
        "wait_times": wait_times,
        "queue_status": {
            "total_waiting": queue_status['total_cases'],
            "priority_breakdown": priority_breakdown
        },
        "last_updated": datetime.now().isoformat()
    })

@emergency_legal_support_bp.route('/triage', methods=['POST'])
def submit_triage():
    """Submit triage information and get connection details"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Required fields
        required_fields = ["situation", "description", "phoneNumber"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Generate a unique case ID
        case_id = f"EMG-{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Determine priority based on situation type
        situation_type = data["situation"]
        priority = SITUATION_PRIORITIES.get(situation_type, 'MEDIUM')
        
        # Add case to priority queue
        case = priority_queue_service.add_case(
            case_id=case_id,
            priority=priority,
            user_id=data.get('user_id', 'anonymous'),
            situation_type=situation_type,
            metadata={
                'description': data['description'],
                'phone_number': data['phoneNumber'],
                'location': data.get('location'),
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # Get estimated wait time from queue
        wait_time = priority_queue_service.get_estimated_wait_time(case_id)
        position = priority_queue_service.get_queue_position(case_id)
        
        # Find an appropriate lawyer based on situation
        available_lawyers = [l for l in MOCK_LAWYERS if l["availability"]]
        matched_lawyer = None
        
        if situation_type in ["police", "rights"]:
            for lawyer in available_lawyers:
                if "criminal" in lawyer["specialties"] or "police_encounters" in lawyer["specialties"]:
                    matched_lawyer = lawyer
                    break
        elif situation_type in ["eviction", "housing"]:
            for lawyer in available_lawyers:
                if "housing" in lawyer["specialties"] or "eviction" in lawyer["specialties"]:
                    matched_lawyer = lawyer
                    break
        elif situation_type in ["immigration"]:
            for lawyer in available_lawyers:
                if "immigration" in lawyer["specialties"]:
                    matched_lawyer = lawyer
                    break
        
        # If no specialty match, get any available lawyer
        if not matched_lawyer and available_lawyers:
            matched_lawyer = available_lawyers[0]
            
        # If we found a lawyer, assign the case
        if matched_lawyer:
            priority_queue_service.assign_case(case_id, matched_lawyer["id"])
        
        # Return connection information
        return jsonify({
            "case_id": case_id,
            "status": "accepted",
            "priority": priority,
            "queue_position": position,
            "estimated_wait_time": str(wait_time) if wait_time else "Unknown",
            "room_info": {
                "type": "jitsi",
                "room_name": case_id,
                "domain": "meet.jit.si",
                "is_secured": True
            }
        })
        
    except Exception as e:
        logger.error(f"Error in triage submission: {str(e)}")
        return jsonify({"error": "Server error processing triage information"}), 500

@emergency_legal_support_bp.route('/call/<case_id>/status', methods=['GET'])
def get_call_status(case_id):
    """Get the status of an ongoing or completed call"""
    # In production, this would query a database
    
    # For demonstration, find the call in our mock logs
    call = next((c for c in call_logs if c["case_id"] == case_id), None)
    
    if not call:
        return jsonify({"error": "Call not found"}), 404
    
    # Return the call status
    return jsonify({
        "case_id": case_id,
        "status": call["status"],
        "timestamp": call["timestamp"],
        "duration": "00:15:30" if call["status"] == "completed" else None,
        "lawyer": {
            "id": call["lawyer_id"],
            "name": next((l["name"] for l in MOCK_LAWYERS if l["id"] == call["lawyer_id"]), None)
        } if call["lawyer_id"] else None
    })

@emergency_legal_support_bp.route('/call/<case_id>/end', methods=['POST'])
def end_call(case_id):
    """End an ongoing call and update its status"""
    # In production, this would update a database record
    
    # For demonstration, find and update the call in our mock logs
    call = next((c for c in call_logs if c["case_id"] == case_id), None)
    
    if not call:
        return jsonify({"error": "Call not found"}), 404
    
    # Update the call status
    call["status"] = "completed"
    call["end_time"] = datetime.now().isoformat()
    
    # Return success
    return jsonify({
        "case_id": case_id,
        "status": "completed",
        "message": "Call successfully ended and recorded"
    })

@emergency_legal_support_bp.route('/call/<case_id>/recording', methods=['POST'])
def toggle_recording(case_id):
    """Start or stop recording for a call"""
    try:
        data = request.json
        
        if not data or "recording_action" not in data:
            return jsonify({"error": "Missing recording_action parameter"}), 400
            
        action = data["recording_action"]  # "start" or "stop"
        
        # In production, this would interface with Jitsi's recording API
        # or a custom recording service
        
        # Find the call in our mock logs
        call = next((c for c in call_logs if c["case_id"] == case_id), None)
        
        if not call:
            return jsonify({"error": "Call not found"}), 404
        
        # Update the recording status
        recording_status = "recording" if action == "start" else "not_recording"
        
        return jsonify({
            "case_id": case_id,
            "recording_status": recording_status,
            "message": f"Recording {action}ed successfully"
        })
        
    except Exception as e:
        logger.error(f"Error toggling recording: {str(e)}")
        return jsonify({"error": "Server error processing recording request"}), 500 
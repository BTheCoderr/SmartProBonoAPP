#!/usr/bin/env python3
"""
Mock backend for AI Virtual Paralegal testing
This provides the API endpoints without requiring a full database setup
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import random

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:3002'])

# Mock data
workflow_running = False
stats = {
    "clients": 0,
    "cases": 0,
    "tasks": 0,
    "documents": 0
}
activity_log = []

@app.route('/api/v1/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "AI Virtual Paralegal Mock Backend"})

@app.route('/api/v1/ai-virtual-paralegal/dashboard', methods=['GET'])
def get_dashboard():
    return jsonify({
        "success": True,
        "workflow_running": workflow_running,
        "stats": stats,
        "recent_activity": activity_log[-10:],
        "capabilities": [
            "Autonomous Workflow Management",
            "Client Case Processing", 
            "Document Generation",
            "Task Scheduling",
            "Deadline Monitoring",
            "Client Communication"
        ]
    })

@app.route('/api/v1/ai-virtual-paralegal/start', methods=['POST'])
def start_workflow():
    global workflow_running, stats, activity_log
    
    workflow_running = True
    
    # Simulate workflow steps
    steps = [
        "AI Virtual Paralegal workflow started",
        "Initializing client case processing...",
        "Setting up task scheduling system...",
        "Activating deadline monitoring...",
        "Analyzing 3 pending cases - identified 12 required actions",
        "Researched 47 relevant cases from CourtListener API",
        "Found 12 similar cases in local ChromaDB",
        "Generated I-485 Application Form with 95% accuracy",
        "Generated Divorce Petition with 95% accuracy",
        "Generated Custody Agreement with 95% accuracy",
        "Generated Financial Disclosure Form with 95% accuracy",
        "Scheduled: Schedule biometrics appointment for John Smith",
        "Scheduled: File divorce petition with court",
        "Scheduled: Prepare custody mediation documents",
        "Scheduled: Follow up on I-485 status",
        "Updated John Smith with case progress and next steps",
        "Updated Maria Garcia with case progress and next steps",
        "AI Virtual Paralegal completed workflow cycle"
    ]
    
    # Add steps to activity log
    for step in steps:
        activity_log.append({
            "timestamp": time.strftime("%H:%M:%S"),
            "message": step,
            "level": "info"
        })
    
    # Update stats
    stats = {
        "clients": 5,
        "cases": 12,
        "tasks": 8,
        "documents": 4
    }
    
    return jsonify({
        "success": True,
        "message": "AI workflow started successfully",
        "workflow_running": True,
        "stats": stats,
        "activity": activity_log[-5:]
    })

@app.route('/api/v1/ai-virtual-paralegal/stop', methods=['POST'])
def stop_workflow():
    global workflow_running, activity_log
    
    workflow_running = False
    
    # Add stop messages
    stop_messages = [
        "AI Virtual Paralegal workflow stopped",
        "Saving current state...",
        "Workflow paused successfully"
    ]
    
    for msg in stop_messages:
        activity_log.append({
            "timestamp": time.strftime("%H:%M:%S"),
            "message": msg,
            "level": "info"
        })
    
    return jsonify({
        "success": True,
        "message": "AI workflow stopped successfully",
        "workflow_running": False,
        "activity": activity_log[-5:]
    })

@app.route('/api/v1/ai-virtual-paralegal/status', methods=['GET'])
def get_status():
    return jsonify({
        "success": True,
        "workflow_running": workflow_running,
        "stats": stats,
        "activity": activity_log[-10:]
    })

if __name__ == '__main__':
    print("🚀 Starting AI Virtual Paralegal Mock Backend...")
    print("📡 Available endpoints:")
    print("  GET  /api/v1/health")
    print("  GET  /api/v1/ai-virtual-paralegal/dashboard")
    print("  POST /api/v1/ai-virtual-paralegal/start")
    print("  POST /api/v1/ai-virtual-paralegal/stop")
    print("  GET  /api/v1/ai-virtual-paralegal/status")
    print("🌐 Server running on http://localhost:3001")
    app.run(host='0.0.0.0', port=3001, debug=True)

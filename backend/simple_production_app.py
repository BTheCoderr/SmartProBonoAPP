"""Simple Production Flask application for testing without database models."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
CORS(app, origins=['*'])  # Allow all origins for production

# Set production configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'production-secret-key')

# Legal AI Chat endpoints
@app.route('/api/v1/legal/analyze', methods=['POST'])
def analyze_legal_query():
    """Analyze legal queries using AI."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        # Simple AI response simulation
        if 'business' in query.lower():
            response = {
                "success": True,
                "analysis": {
                    "query": query,
                    "response": "Starting a business involves several legal steps: 1) Choose a business structure (LLC, Corporation, etc.), 2) Register with your state, 3) Obtain necessary licenses and permits, 4) Get an EIN from the IRS, 5) Open a business bank account. I recommend consulting with a business attorney for specific guidance based on your industry and location.",
                    "confidence": 0.85,
                    "suggestions": [
                        "Consider forming an LLC for liability protection",
                        "Research local business licensing requirements",
                        "Consult with a business attorney for specific advice"
                    ]
                }
            }
        else:
            response = {
                "success": True,
                "analysis": {
                    "query": query,
                    "response": "I'd be happy to help with your legal question. Could you provide more specific details about your situation? This will help me give you more accurate and relevant legal guidance.",
                    "confidence": 0.7,
                    "suggestions": [
                        "Provide more specific details about your legal situation",
                        "Consider consulting with a qualified attorney for complex matters"
                    ]
                }
            }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to analyze query",
            "message": str(e)
        }), 500

@app.route('/api/v1/legal/chat', methods=['POST'])
def legal_chat():
    """Legal chat endpoint."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Simple chat response
        response = {
            "success": True,
            "response": f"I understand you're asking about: {message}. I'm here to help with your legal questions. Could you provide more specific details so I can assist you better?",
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Chat failed",
            "message": str(e)
        }), 500

# Document Generation endpoints
@app.route('/api/v1/documents/templates', methods=['GET'])
def get_templates():
    """Get available document templates"""
    templates = [
        {
            "id": "nda_template",
            "name": "Non-Disclosure Agreement",
            "description": "Standard NDA template for business agreements",
            "category": "Business",
            "fields": [
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "client_name", "label": "Client Name", "type": "text", "required": True},
                {"name": "effective_date", "label": "Effective Date", "type": "date", "required": True},
                {"name": "confidentiality_period", "label": "Confidentiality Period (years)", "type": "number", "required": True},
                {"name": "jurisdiction", "label": "Jurisdiction", "type": "text", "required": True}
            ]
        },
        {
            "id": "employment_contract",
            "name": "Employment Contract",
            "description": "Standard employment agreement template",
            "category": "Employment",
            "fields": [
                {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "position", "label": "Position", "type": "text", "required": True},
                {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
                {"name": "salary", "label": "Annual Salary", "type": "number", "required": True},
                {"name": "benefits", "label": "Benefits", "type": "textarea", "required": False}
            ]
        },
        {
            "id": "lease_agreement",
            "name": "Lease Agreement",
            "description": "Residential lease agreement template",
            "category": "Real Estate",
            "fields": [
                {"name": "landlord_name", "label": "Landlord Name", "type": "text", "required": True},
                {"name": "tenant_name", "label": "Tenant Name", "type": "text", "required": True},
                {"name": "property_address", "label": "Property Address", "type": "text", "required": True},
                {"name": "rent_amount", "label": "Monthly Rent", "type": "number", "required": True},
                {"name": "lease_start", "label": "Lease Start Date", "type": "date", "required": True},
                {"name": "lease_end", "label": "Lease End Date", "type": "date", "required": True}
            ]
        }
    ]
    return jsonify({
        "success": True,
        "templates": templates
    })

@app.route('/api/v1/documents/generate', methods=['POST'])
def generate_document():
    """Generate a document from template and form data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        template_id = data.get('template_id')
        form_data = data.get('form_data', {})
        
        if not template_id:
            return jsonify({
                "success": False,
                "error": "Template ID is required"
            }), 400
        
        # Simple document generation simulation
        document_id = f"{template_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return jsonify({
            "success": True,
            "document_id": document_id,
            "filename": f"{document_id}.html",
            "template_name": "Generated Document",
            "generated_at": datetime.now().isoformat(),
            "preview_url": f"/api/v1/documents/preview/{document_id}",
            "message": "Document generated successfully! This is a demo - in production, this would generate an actual document."
        })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Predictive Analytics endpoints
@app.route('/api/v1/analytics/predict', methods=['POST'])
def predict_case_outcome():
    """Predict case outcome using AI analytics"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        case_type = data.get("case_type", "general")
        factors = data.get("factors", {})
        
        # Simulate prediction based on factors
        evidence_strength = factors.get("evidence_strength", "moderate")
        legal_precedent = factors.get("legal_precedent", "neutral")
        client_cooperation = factors.get("client_cooperation", "average")
        
        # Calculate prediction score
        score = 0.5
        if evidence_strength == "strong":
            score += 0.2
        elif evidence_strength == "weak":
            score -= 0.2
        
        if legal_precedent == "favorable":
            score += 0.15
        elif legal_precedent == "unfavorable":
            score -= 0.15
        
        if client_cooperation == "excellent":
            score += 0.1
        elif client_cooperation == "poor":
            score -= 0.1
        
        score = max(0.0, min(1.0, score))
        
        # Generate outcome probabilities
        outcome_probability = {
            "favorable": score,
            "unfavorable": 1.0 - score,
            "settlement": min(0.8, score + 0.2),
            "trial": max(0.2, 1.0 - score - 0.2)
        }
        
        # Generate recommendations
        recommendations = []
        if evidence_strength == "weak":
            recommendations.append({
                "category": "Evidence",
                "priority": "high",
                "recommendation": "Gather additional evidence to strengthen your case",
                "action_items": ["Conduct thorough discovery", "Interview additional witnesses"]
            })
        
        if client_cooperation == "poor":
            recommendations.append({
                "category": "Client Management",
                "priority": "high",
                "recommendation": "Improve client communication and cooperation",
                "action_items": ["Schedule regular check-ins", "Provide clear expectations"]
            })
        
        # Estimate timeline
        base_duration = 120  # 4 months
        if case_type == "immigration":
            base_duration = 180
        elif case_type == "family_law":
            base_duration = 90
        elif case_type == "criminal_defense":
            base_duration = 150
        
        estimated_completion = datetime.now() + timedelta(days=base_duration)
        
        return jsonify({
            "success": True,
            "prediction": {
                "case_type": case_type,
                "outcome_probability": outcome_probability,
                "confidence_score": score,
                "timeline_estimate": {
                    "estimated_duration_days": base_duration,
                    "estimated_completion_date": estimated_completion.isoformat()
                },
                "success_probability": score,
                "recommended_strategy": "Focus on settlement negotiations" if score < 0.5 else "Aggressive litigation strategy"
            },
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/v1/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Get analytics dashboard data"""
    try:
        # Simulate analytics data
        success_rates = {
            "immigration": 0.72,
            "family_law": 0.85,
            "criminal_defense": 0.68,
            "personal_injury": 0.78,
            "business_law": 0.82,
            "civil_rights": 0.65
        }
        
        average_timelines = {
            "immigration": 180,
            "family_law": 90,
            "criminal_defense": 150,
            "personal_injury": 365,
            "business_law": 120,
            "civil_rights": 300
        }
        
        return jsonify({
            "success": True,
            "analytics": {
                "success_rates": success_rates,
                "average_timelines": average_timelines,
                "total_cases_analyzed": 1250,
                "recommendation_accuracy": 0.78,
                "client_satisfaction": 0.85,
                "case_completion_rate": 0.92
            },
            "insights": [
                "Family law cases show highest success rates (85%)",
                "Immigration cases average 6 months resolution time",
                "Client satisfaction has improved 15% this quarter",
                "Settlement rate increased to 68% across all case types"
            ],
            "generated_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Health check endpoint
@app.route('/api/v1/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "SmartProBono Backend",
        "version": "2.0.0",
        "message": "Backend is running successfully!"
    })

# CRM Demo endpoints
@app.route('/api/v1/crm/cases')
def get_cases():
    """Demo endpoint for cases."""
    return jsonify({
        "success": True,
        "cases": [
            {
                "id": 1,
                "title": "Immigration Case - I-485 Application",
                "client_name": "John Doe",
                "status": "in_progress",
                "case_type": "immigration",
                "priority": "high",
                "created_at": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "title": "Family Law - Divorce Proceedings",
                "client_name": "Jane Smith",
                "status": "pending",
                "case_type": "family_law",
                "priority": "medium",
                "created_at": "2024-01-20T14:15:00Z"
            },
            {
                "id": 3,
                "title": "Criminal Defense - DUI Case",
                "client_name": "Mike Johnson",
                "status": "active",
                "case_type": "criminal_defense",
                "priority": "urgent",
                "created_at": "2024-01-25T09:45:00Z"
            }
        ]
    })

@app.route('/api/v1/crm/clients')
def get_clients():
    """Demo endpoint for clients."""
    return jsonify({
        "success": True,
        "clients": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@email.com",
                "phone": "+1-555-0123",
                "case_count": 1,
                "status": "active"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@email.com",
                "phone": "+1-555-0124",
                "case_count": 1,
                "status": "active"
            },
            {
                "id": 3,
                "name": "Mike Johnson",
                "email": "mike.johnson@email.com",
                "phone": "+1-555-0125",
                "case_count": 1,
                "status": "active"
            }
        ]
    })

@app.route('/api/v1/crm/court-dates')
def get_court_dates():
    """Demo endpoint for court dates."""
    return jsonify({
        "success": True,
        "court_dates": [
            {
                "id": 1,
                "title": "Immigration Hearing",
                "client_name": "John Doe",
                "date": "2024-02-15T10:00:00Z",
                "location": "USCIS Field Office",
                "status": "scheduled"
            },
            {
                "id": 2,
                "title": "Divorce Mediation",
                "client_name": "Jane Smith",
                "date": "2024-02-20T14:00:00Z",
                "location": "Family Court",
                "status": "scheduled"
            },
            {
                "id": 3,
                "title": "DUI Arraignment",
                "client_name": "Mike Johnson",
                "date": "2024-02-25T09:00:00Z",
                "location": "Criminal Court",
                "status": "scheduled"
            }
        ]
    })

@app.route('/api/v1/crm/payments')
def get_payments():
    """Demo endpoint for payments."""
    return jsonify({
        "success": True,
        "payments": [
            {
                "id": 1,
                "client_name": "John Doe",
                "amount": 2500.00,
                "status": "completed",
                "payment_method": "credit_card",
                "date": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "client_name": "Jane Smith",
                "amount": 1500.00,
                "status": "pending",
                "payment_method": "bank_transfer",
                "date": "2024-01-20T14:15:00Z"
            }
        ]
    })

# Root endpoint
@app.route('/')
def root():
    return jsonify({
        "message": "SmartProBono Backend API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/v1/health",
            "cases": "/api/v1/crm/cases",
            "clients": "/api/v1/crm/clients",
            "court_dates": "/api/v1/crm/court-dates",
            "payments": "/api/v1/crm/payments"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Starting SmartProBono Backend on port {port}")
    app.run(host='127.0.0.1', port=port, debug=False)  # Fixed: localhost only for security

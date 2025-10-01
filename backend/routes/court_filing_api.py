"""
Court Filing Assistance API Routes
Handles court document preparation, filing, and tracking
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import logging
from datetime import datetime, timedelta
from services.simple_court_filing_service import (
    court_filing_service, 
    CourtFiling, 
    FilingStatus, 
    DocumentType,
    CourtRule,
    FilingTemplate
)
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Create blueprint
court_filing_bp = Blueprint('court_filing_api', __name__, url_prefix='/api/court-filing')

@court_filing_bp.route('/status', methods=['GET'])
def get_filing_status():
    """Get court filing service status"""
    try:
        stats = court_filing_service.get_filing_statistics()
        return jsonify({
            "success": True,
            "status": "available",
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting filing status: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/rules', methods=['GET'])
def get_court_rules():
    """Get court rules for a jurisdiction and court"""
    try:
        jurisdiction = request.args.get('jurisdiction')
        court = request.args.get('court')
        
        rules = court_filing_service.get_court_rules(jurisdiction, court)
        
        return jsonify({
            "success": True,
            "rules": [
                {
                    "jurisdiction": rule.jurisdiction,
                    "court": rule.court,
                    "rule_number": rule.rule_number,
                    "title": rule.title,
                    "description": rule.description,
                    "requirements": rule.requirements,
                    "deadlines": rule.deadlines,
                    "fees": rule.fees,
                    "forms": rule.forms,
                    "electronic_filing": rule.electronic_filing,
                    "efiling_system": rule.efiling_system
                }
                for rule in rules
            ],
            "count": len(rules)
        })
    except Exception as e:
        logger.error(f"Error getting court rules: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/templates', methods=['GET'])
def get_filing_templates():
    """Get filing templates"""
    try:
        document_type = request.args.get('document_type')
        jurisdiction = request.args.get('jurisdiction')
        
        doc_type = None
        if document_type:
            try:
                doc_type = DocumentType(document_type)
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": f"Invalid document type: {document_type}"
                }), 400
        
        templates = court_filing_service.get_filing_templates(doc_type, jurisdiction)
        
        return jsonify({
            "success": True,
            "templates": [
                {
                    "id": template.template_id,
                    "name": template.name,
                    "document_type": template.document_type if isinstance(template.document_type, str) else template.document_type.value,
                    "jurisdiction": template.jurisdiction,
                    "description": template.description,
                    "required_fields": template.required_fields,
                    "optional_fields": template.optional_fields,
                    "file_path": template.file_path
                }
                for template in templates
            ],
            "count": len(templates)
        })
    except Exception as e:
        logger.error(f"Error getting filing templates: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/templates/<template_id>', methods=['GET'])
def get_template_content(template_id):
    """Get template content for document generation"""
    try:
        template = court_filing_service.templates.get(template_id)
        if not template:
            return jsonify({
                "success": False,
                "error": "Template not found"
            }), 404
        
        return jsonify({
            "success": True,
            "template": {
                "id": template.id,
                "name": template.name,
                "document_type": template.document_type.value,
                "jurisdiction": template.jurisdiction,
                "court": template.court,
                "template_content": template.template_content,
                "required_fields": template.required_fields,
                "optional_fields": template.optional_fields,
                "instructions": template.instructions
            }
        })
    except Exception as e:
        logger.error(f"Error getting template content: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/generate', methods=['POST'])
def generate_document():
    """Generate a document from a template"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        template_id = data.get('template_id')
        document_data = data.get('data', {})
        
        if not template_id:
            return jsonify({
                "success": False,
                "error": "Template ID is required"
            }), 400
        
        # Generate document
        document_content = court_filing_service.generate_document(template_id, document_data)
        
        return jsonify({
            "success": True,
            "document_content": document_content,
            "template_id": template_id,
            "generated_at": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error generating document: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/filings', methods=['POST'])
def create_filing():
    """Create a new court filing"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Create filing
        filing = court_filing_service.create_filing(data)
        
        return jsonify({
            "success": True,
            "filing": {
                "id": filing.id,
                "case_id": filing.case_id,
                "document_type": filing.document_type.value,
                "title": filing.title,
                "description": filing.description,
                "status": filing.status.value,
                "court": filing.court,
                "jurisdiction": filing.jurisdiction,
                "filing_date": filing.filing_date.isoformat() if filing.filing_date else None,
                "due_date": filing.due_date.isoformat() if filing.due_date else None,
                "created_at": filing.created_at.isoformat(),
                "updated_at": filing.updated_at.isoformat(),
                "filed_by": filing.filed_by,
                "file_path": filing.file_path,
                "court_reference": filing.court_reference,
                "fees_paid": filing.fees_paid,
                "rejection_reason": filing.rejection_reason,
                "amendments": filing.amendments,
                "attachments": filing.attachments
            }
        }), 201
    except Exception as e:
        logger.error(f"Error creating filing: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/filings/<filing_id>', methods=['GET'])
def get_filing(filing_id):
    """Get a court filing by ID"""
    try:
        filing = court_filing_service.get_filing(filing_id)
        if not filing:
            return jsonify({
                "success": False,
                "error": "Filing not found"
            }), 404
        
        return jsonify({
            "success": True,
            "filing": {
                "id": filing.id,
                "case_id": filing.case_id,
                "document_type": filing.document_type.value,
                "title": filing.title,
                "description": filing.description,
                "status": filing.status.value,
                "court": filing.court,
                "jurisdiction": filing.jurisdiction,
                "filing_date": filing.filing_date.isoformat() if filing.filing_date else None,
                "due_date": filing.due_date.isoformat() if filing.due_date else None,
                "created_at": filing.created_at.isoformat(),
                "updated_at": filing.updated_at.isoformat(),
                "filed_by": filing.filed_by,
                "file_path": filing.file_path,
                "court_reference": filing.court_reference,
                "fees_paid": filing.fees_paid,
                "rejection_reason": filing.rejection_reason,
                "amendments": filing.amendments,
                "attachments": filing.attachments
            }
        })
    except Exception as e:
        logger.error(f"Error getting filing: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/filings/<filing_id>', methods=['PUT'])
def update_filing(filing_id):
    """Update a court filing"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Update filing
        filing = court_filing_service.update_filing(filing_id, data)
        if not filing:
            return jsonify({
                "success": False,
                "error": "Filing not found"
            }), 404
        
        return jsonify({
            "success": True,
            "filing": {
                "id": filing.id,
                "case_id": filing.case_id,
                "document_type": filing.document_type.value,
                "title": filing.title,
                "description": filing.description,
                "status": filing.status.value,
                "court": filing.court,
                "jurisdiction": filing.jurisdiction,
                "filing_date": filing.filing_date.isoformat() if filing.filing_date else None,
                "due_date": filing.due_date.isoformat() if filing.due_date else None,
                "created_at": filing.created_at.isoformat(),
                "updated_at": filing.updated_at.isoformat(),
                "filed_by": filing.filed_by,
                "file_path": filing.file_path,
                "court_reference": filing.court_reference,
                "fees_paid": filing.fees_paid,
                "rejection_reason": filing.rejection_reason,
                "amendments": filing.amendments,
                "attachments": filing.attachments
            }
        })
    except Exception as e:
        logger.error(f"Error updating filing: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/filings/<filing_id>/file', methods=['POST'])
def file_document(filing_id):
    """File a document with the court"""
    try:
        data = request.get_json() or {}
        court_system = data.get('court_system', 'efiling')
        
        # File document
        success = court_filing_service.file_document(filing_id, court_system)
        
        if success:
            filing = court_filing_service.get_filing(filing_id)
            return jsonify({
                "success": True,
                "message": "Document filed successfully",
                "filing": {
                    "id": filing.id,
                    "status": filing.status.value,
                    "filing_date": filing.filing_date.isoformat() if filing.filing_date else None,
                    "court_reference": filing.court_reference
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to file document"
            }), 400
    except Exception as e:
        logger.error(f"Error filing document: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/filings/<filing_id>/validate', methods=['POST'])
def validate_filing(filing_id):
    """Validate a court filing"""
    try:
        is_valid, errors = court_filing_service.validate_filing(filing_id)
        
        return jsonify({
            "success": True,
            "is_valid": is_valid,
            "errors": errors,
            "filing_id": filing_id
        })
    except Exception as e:
        logger.error(f"Error validating filing: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/fees', methods=['POST'])
def calculate_filing_fees():
    """Calculate filing fees for a document"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        document_type = data.get('document_type')
        jurisdiction = data.get('jurisdiction')
        court = data.get('court')
        
        if not all([document_type, jurisdiction, court]):
            return jsonify({
                "success": False,
                "error": "Document type, jurisdiction, and court are required"
            }), 400
        
        try:
            doc_type = DocumentType(document_type)
        except ValueError:
            return jsonify({
                "success": False,
                "error": f"Invalid document type: {document_type}"
            }), 400
        
        fees = court_filing_service.calculate_filing_fees(doc_type, jurisdiction, court)
        
        return jsonify({
            "success": True,
            "fees": fees,
            "document_type": document_type,
            "jurisdiction": jurisdiction,
            "court": court
        })
    except Exception as e:
        logger.error(f"Error calculating filing fees: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/deadlines', methods=['POST'])
def calculate_filing_deadlines():
    """Calculate filing deadlines based on case events"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        case_events = data.get('case_events', [])
        jurisdiction = data.get('jurisdiction')
        court = data.get('court')
        
        if not all([jurisdiction, court]):
            return jsonify({
                "success": False,
                "error": "Jurisdiction and court are required"
            }), 400
        
        deadlines = court_filing_service.get_filing_deadlines(case_events, jurisdiction, court)
        
        return jsonify({
            "success": True,
            "deadlines": {
                event_type: deadline.isoformat() 
                for event_type, deadline in deadlines.items()
            },
            "case_events": case_events,
            "jurisdiction": jurisdiction,
            "court": court
        })
    except Exception as e:
        logger.error(f"Error calculating filing deadlines: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/filings', methods=['GET'])
def list_filings():
    """List all court filings with optional filtering"""
    try:
        status = request.args.get('status')
        case_id = request.args.get('case_id')
        document_type = request.args.get('document_type')
        
        filings = list(court_filing_service.filings.values())
        
        # Apply filters
        if status:
            try:
                status_enum = FilingStatus(status)
                filings = [f for f in filings if f.status == status_enum]
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": f"Invalid status: {status}"
                }), 400
        
        if case_id:
            filings = [f for f in filings if f.case_id == case_id]
        
        if document_type:
            try:
                doc_type_enum = DocumentType(document_type)
                filings = [f for f in filings if f.document_type == doc_type_enum]
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": f"Invalid document type: {document_type}"
                }), 400
        
        return jsonify({
            "success": True,
            "filings": [
                {
                    "id": filing.id,
                    "case_id": filing.case_id,
                    "document_type": filing.document_type.value,
                    "title": filing.title,
                    "description": filing.description,
                    "status": filing.status.value,
                    "court": filing.court,
                    "jurisdiction": filing.jurisdiction,
                    "filing_date": filing.filing_date.isoformat() if filing.filing_date else None,
                    "due_date": filing.due_date.isoformat() if filing.due_date else None,
                    "created_at": filing.created_at.isoformat(),
                    "updated_at": filing.updated_at.isoformat(),
                    "filed_by": filing.filed_by,
                    "court_reference": filing.court_reference,
                    "fees_paid": filing.fees_paid
                }
                for filing in filings
            ],
            "count": len(filings)
        })
    except Exception as e:
        logger.error(f"Error listing filings: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@court_filing_bp.route('/download/<filing_id>', methods=['GET'])
def download_filing(filing_id):
    """Download a filed document"""
    try:
        filing = court_filing_service.get_filing(filing_id)
        if not filing:
            return jsonify({
                "success": False,
                "error": "Filing not found"
            }), 404
        
        if not filing.file_path or not os.path.exists(filing.file_path):
            return jsonify({
                "success": False,
                "error": "Document file not found"
            }), 404
        
        return send_file(
            filing.file_path,
            as_attachment=True,
            download_name=f"{filing.title}_{filing.id}.pdf"
        )
    except Exception as e:
        logger.error(f"Error downloading filing: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

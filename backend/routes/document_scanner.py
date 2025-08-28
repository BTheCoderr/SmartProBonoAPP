from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import os
import json
from datetime import datetime
import logging
import tempfile
from backend.services.auth_service import require_auth, get_current_user
from backend.services.ai_service import analyze_document, extract_text_from_document

bp = Blueprint('document_scanner', __name__)
logger = logging.getLogger(__name__)

@bp.route('/scan', methods=['POST'])
def scan_document():
    """Scan a document to extract information"""
    try:
        if 'file' not in request.files:
            raise BadRequest("No file part")
            
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("No selected file")
            
        # Get the document type if specified
        document_type = request.form.get('document_type', 'generic')
        
        # Check file type
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'docx'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            raise BadRequest("File type not allowed")
            
        # Save the file temporarily
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        file.save(temp_file_path)
        
        # Extract text from the document
        extracted_text = extract_text_from_document(temp_file_path)
        
        # Remove the temporary file
        os.remove(temp_file_path)
        
        if not extracted_text:
            return jsonify({
                "success": False,
                "error": "Could not extract text from document"
            }), 400
            
        # Return the extracted text
        return jsonify({
            "success": True,
            "extracted_text": extracted_text,
            "document_type": document_type
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error scanning document: {str(e)}")
        return jsonify({"error": "An error occurred while processing the document"}), 500

@bp.route('/analyze', methods=['POST'])
def analyze_document_route():
    """Analyze a document for legal information"""
    try:
        if 'file' not in request.files:
            raise BadRequest("No file part")
            
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("No selected file")
            
        # Get the document type if specified
        document_type = request.form.get('document_type', 'generic')
        
        # Check file type
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'docx'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            raise BadRequest("File type not allowed")
            
        # Save the file temporarily
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        file.save(temp_file_path)
        
        # Questions to answer about the document (if any)
        questions_json = request.form.get('questions', '[]')
        try:
            questions = json.loads(questions_json)
        except:
            questions = []
        
        # Analyze the document
        analysis = analyze_document(temp_file_path, document_type, questions)
        
        # Remove the temporary file
        os.remove(temp_file_path)
        
        # Return the analysis
        return jsonify({
            "success": True,
            "analysis": analysis,
            "document_type": document_type
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        return jsonify({"error": "An error occurred while analyzing the document"}), 500

@bp.route('/document-types', methods=['GET'])
def get_document_types():
    """Get list of recognizable document types"""
    try:
        document_types = [
            {
                "id": "eviction_notice",
                "name": "Eviction Notice",
                "description": "Notice of eviction from landlord",
                "analyzable_fields": ["notice_date", "eviction_date", "grounds", "landlord_info", "property_address"]
            },
            {
                "id": "court_summons",
                "name": "Court Summons",
                "description": "Legal summons to appear in court",
                "analyzable_fields": ["court_name", "case_number", "hearing_date", "parties_involved", "subject_matter"]
            },
            {
                "id": "lease_agreement",
                "name": "Lease Agreement",
                "description": "Residential or commercial lease contract",
                "analyzable_fields": ["start_date", "end_date", "rent_amount", "security_deposit", "landlord_info", "tenant_info", "property_address", "terms_conditions"]
            },
            {
                "id": "debt_collection",
                "name": "Debt Collection Notice",
                "description": "Notice of debt collection activities",
                "analyzable_fields": ["creditor", "debt_amount", "account_number", "date_of_notice", "collection_agency"]
            },
            {
                "id": "restraining_order",
                "name": "Restraining Order",
                "description": "Court order of protection",
                "analyzable_fields": ["court_name", "case_number", "protected_party", "restrained_party", "expiration_date", "restrictions"]
            },
            {
                "id": "generic",
                "name": "Generic Legal Document",
                "description": "Any legal document not covered by other types",
                "analyzable_fields": ["document_date", "parties_involved", "key_provisions", "deadlines", "contact_information"]
            }
        ]
        
        return jsonify({"document_types": document_types})
    except Exception as e:
        logger.error(f"Error getting document types: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/extract-form', methods=['POST'])
def extract_form_data():
    """Extract form fields from a document"""
    try:
        if 'file' not in request.files:
            raise BadRequest("No file part")
            
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("No selected file")
            
        # Get the form type if specified
        form_type = request.form.get('form_type', '')
        
        # Check file type
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            raise BadRequest("File type not allowed")
            
        # Save the file temporarily
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        file.save(temp_file_path)
        
        # In a real app, this would use OCR and AI to extract form fields
        # Mocked response for demonstration
        extracted_fields = {
            "form_type_detected": form_type or "unknown",
            "fields": {
                "name": "John Smith",
                "address": "123 Main St, Anytown, CA 12345",
                "date": "01/15/2023",
                # Other extracted fields would appear here
            },
            "confidence_score": 0.85
        }
        
        # Remove the temporary file
        os.remove(temp_file_path)
        
        return jsonify({
            "success": True,
            "extracted_data": extracted_fields
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error extracting form data: {str(e)}")
        return jsonify({"error": "An error occurred while extracting form data"}), 500

@bp.route('/scan-history', methods=['GET'])
@require_auth
def get_scan_history():
    """Get user's document scanning history"""
    try:
        user = get_current_user()
        
        # In a real app, this would fetch from a database
        # Mocked response for demonstration
        scan_history = [
            {
                "id": "scan_001",
                "filename": "eviction_notice.pdf",
                "document_type": "eviction_notice",
                "scan_date": "2023-11-10T14:30:00Z",
                "extracted_fields": 12,
                "file_size": 1240000
            },
            {
                "id": "scan_002",
                "filename": "lease_agreement.pdf",
                "document_type": "lease_agreement",
                "scan_date": "2023-11-09T10:15:00Z",
                "extracted_fields": 24,
                "file_size": 2350000
            }
        ]
        
        return jsonify({"scan_history": scan_history})
    except Exception as e:
        logger.error(f"Error getting scan history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/compare', methods=['POST'])
def compare_documents():
    """Compare two documents for differences"""
    try:
        if 'file1' not in request.files or 'file2' not in request.files:
            raise BadRequest("Two files are required")
            
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        if file1.filename == '' or file2.filename == '':
            raise BadRequest("Two files must be selected")
            
        # Check file types
        allowed_extensions = {'pdf', 'docx', 'txt'}
        if ('.' not in file1.filename or file1.filename.rsplit('.', 1)[1].lower() not in allowed_extensions or
            '.' not in file2.filename or file2.filename.rsplit('.', 1)[1].lower() not in allowed_extensions):
            raise BadRequest("File types not allowed")
            
        # Save the files temporarily
        temp_dir = tempfile.gettempdir()
        temp_file1_path = os.path.join(temp_dir, f"upload1_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        temp_file2_path = os.path.join(temp_dir, f"upload2_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        file1.save(temp_file1_path)
        file2.save(temp_file2_path)
        
        # In a real app, this would use document comparison algorithms
        # Mocked response for demonstration
        comparison_result = {
            "similarity_score": 0.75,
            "differences": [
                {
                    "section": "Payment Terms",
                    "original": "Payment due on the 1st of each month",
                    "modified": "Payment due on the 5th of each month"
                },
                {
                    "section": "Security Deposit",
                    "original": "$1,000",
                    "modified": "$1,500"
                }
            ],
            "added_sections": ["Late Fee Policy"],
            "removed_sections": []
        }
        
        # Remove the temporary files
        os.remove(temp_file1_path)
        os.remove(temp_file2_path)
        
        return jsonify({
            "success": True,
            "comparison": comparison_result
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error comparing documents: {str(e)}")
        return jsonify({"error": "An error occurred while comparing the documents"}), 500 
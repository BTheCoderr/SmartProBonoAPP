from flask import Blueprint, request, jsonify, current_app, send_file
from datetime import datetime
import re
from database import db
from models.document import Document
from models.user import User
from services.email_service import send_document_share_email
from flask_jwt_extended import jwt_required, get_jwt_identity
from document_service import DocumentService
from werkzeug.utils import secure_filename
import os
from bson import ObjectId
import logging
from database.mongo import mongo

# Import OCR services
from services.ocr_service import ocr_service
from services.ocr_storage_service import ocr_storage_service

bp = Blueprint('documents', __name__, url_prefix='/api/documents')
logger = logging.getLogger(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mongo_collection(collection_name: str):
    """Safely get a MongoDB collection."""
    try:
        if not hasattr(mongo, 'db'):
            logger.error("MongoDB connection not initialized")
            return None
        return getattr(mongo.db, collection_name, None)
    except Exception as e:
        logger.error(f"Error accessing MongoDB collection {collection_name}: {str(e)}")
        return None

@bp.route('/<document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    """Get a document by ID. Supports both integer and string IDs for MongoDB compatibility."""
    try:
        # Try to get document from MongoDB first
        if isinstance(document_id, str) and ObjectId.is_valid(document_id):
            collection = get_mongo_collection('documents')
            if collection:
                doc = collection.find_one({'_id': ObjectId(document_id)})
                if doc:
                    return jsonify(doc), 200
        
        # If not found or invalid ObjectId, try SQL database
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        return jsonify(document.to_dict())
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<document_id>', methods=['PUT'])
@jwt_required()
def update_document(document_id):
    try:
        data = request.get_json()
        
        # Get the current document
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        # Add current version to history if content changed
        if 'content' in data and data['content'] != document.content:
            document.add_version(document.content)
            document.content = data['content']
            
        # Update other fields
        if 'title' in data:
            document.title = data['title']
        if 'description' in data:
            document.description = data['description']
        if 'document_type' in data:
            document.document_type = data['document_type']
            
        document.updated_at = datetime.utcnow()
        
        # Commit changes
        db.session.commit()
            
        return jsonify(document.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_document():
    try:
        data = request.get_json()
        required_fields = ['title', 'content', 'file_url', 'file_type']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Get current user
        current_user_id = get_jwt_identity()
                
        # Create new document
        document = Document()
        document.title = data['title']
        document.content = data['content']
        document.file_url = data['file_url']
        document.file_type = data['file_type']
        document.document_type = data.get('document_type', 'case_document')
        document.description = data.get('description', '')
        document.cloudinary_public_id = data.get('cloudinary_public_id')
        document.uploaded_by = current_user_id
        document.case_id = data.get('case_id')
        
        # Add tags if provided
        if 'tags' in data and isinstance(data['tags'], list):
            document.tags = data['tags']
            
        db.session.add(document)
        db.session.commit()
            
        return jsonify(document.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:document_id>/versions', methods=['GET'])
@jwt_required()
def get_document_versions(document_id):
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        versions = document.history
        
        # Add current version
        versions.append({
            'content': document.content,
            'timestamp': document.updated_at.isoformat(),
            'version': len(versions) + 1,
            'isCurrent': True
        })
        
        return jsonify(versions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:document_id>/versions/<int:version>', methods=['POST'])
@jwt_required()
def revert_to_version(document_id, version):
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        history = document.history
        if version < 1 or version > len(history):
            return jsonify({'error': 'Invalid version number'}), 400
            
        # Get the content from the specified version
        target_version = history[version - 1]
        
        # Add current version to history
        document.add_version(document.content)
        
        # Update content with old version
        document.content = target_version['content']
        document.updated_at = datetime.utcnow()
        
        db.session.commit()
            
        return jsonify({'message': 'Document reverted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:document_id>/share', methods=['POST'])
@jwt_required()
def share_document(document_id):
    try:
        data = request.get_json()
        if 'users' not in data or not isinstance(data['users'], list):
            return jsonify({'error': 'Missing users to share with'}), 400
            
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        # TODO: Implement document sharing logic
        # This would typically involve creating share records in a separate table
        # For now, we'll just return success
            
        return jsonify({'message': 'Document shared successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:document_id>/share-via-email', methods=['POST'])
@jwt_required()
def share_document_via_email(document_id):
    try:
        data = request.get_json()
        required_fields = ['recipientEmail', 'subject', 'message', 'shareLink']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email format
        email = data['recipientEmail']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'error': 'Invalid email format'}), 400
            
        # Check if document exists
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Send email
        email_sent = send_document_share_email(
            recipient_email=data['recipientEmail'],
            subject=data['subject'],
            message=data['message'],
            document_title=document.title,
            share_link=data['shareLink']
        )
        
        if not email_sent:
            return jsonify({'error': 'Failed to send email'}), 500
            
        # Record the share
        document.add_email_share(data['recipientEmail'])
        db.session.commit()
            
        return jsonify({'message': 'Email sent successfully'}), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    """Delete a document by ID. Supports both integer and string IDs for MongoDB compatibility."""
    try:
        # Try to delete from MongoDB first
        if isinstance(document_id, str) and ObjectId.is_valid(document_id):
            collection = get_mongo_collection('documents')
            if collection:
                result = collection.delete_one({'_id': ObjectId(document_id)})
                if result.deleted_count > 0:
                    return jsonify({'message': 'Document deleted successfully'}), 200
        
        # If not found or invalid ObjectId, try SQL database
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'message': 'Document deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting document: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_document_history():
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Query documents owned by the user or shared with them
        # For now, we'll just return documents uploaded by the user
        documents = Document.query.filter_by(uploaded_by=current_user_id).all()
        
        # Convert to list of dictionaries
        document_list = [doc.to_dict() for doc in documents]
            
        return jsonify({'documents': document_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:document_id>/tags', methods=['PUT'])
@jwt_required()
def update_document_tags(document_id):
    try:
        data = request.get_json()
        
        if 'tags' not in data:
            return jsonify({'error': 'Missing tags field'}), 400
            
        # Check if document exists
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        # Update document tags
        document.tags = data['tags']
        document.updated_at = datetime.utcnow()
        
        db.session.commit()
            
        return jsonify({'message': 'Document tags updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/tags/common', methods=['GET'])
@jwt_required()
def get_common_tags():
    try:
        # This would be more efficient with a proper aggregation query
        # For simplicity, we'll just collect all tags and count them
        all_documents = Document.query.all()
        tag_counts = {}
        
        for doc in all_documents:
            for tag in doc.tags:
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1
                    
        # Sort by count and get top 20
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Format the results
        tags = [{"tag": tag, "count": count} for tag, count in top_tags]
        
        return jsonify({'tags': tags})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search/tags', methods=['POST'])
@jwt_required()
def search_documents_by_tags():
    try:
        data = request.get_json()
        
        if 'tags' not in data or not isinstance(data['tags'], list):
            return jsonify({'error': 'Missing or invalid tags field'}), 400
        
        # Get current user
        current_user_id = get_jwt_identity()
        
        # This is a simplified approach - in a production app, you'd want to use a more efficient query
        # For each tag, find documents containing that tag
        matching_documents = []
        for document in Document.query.filter_by(uploaded_by=current_user_id).all():
            document_tags = document.tags
            if any(tag in document_tags for tag in data['tags']):
                matching_documents.append(document.to_dict())
                
        return jsonify({'documents': matching_documents})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_document():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
            
        template = data.get('template')
        form_data = data.get('data')
        
        if not template:
            return jsonify({'error': 'Template is required'}), 400
            
        if not form_data:
            return jsonify({'error': 'Form data is required'}), 400
            
        # Initialize document service
        document_service = DocumentService()
        
        # Generate document based on template type
        if template == 'rental_agreement':
            result = document_service.generate_rental_agreement(form_data)
        elif template == 'deed_of_sale':
            result = document_service.generate_deed_of_sale(form_data)
        elif template == 'service_agreement':
            result = document_service.generate_service_agreement(form_data)
        elif template == 'employment_contract':
            result = document_service.generate_employment_contract(form_data)
        elif template == 'software_license':
            result = document_service.generate_software_license(form_data)
        elif template == 'healthcare_agreement':
            result = document_service.generate_healthcare_agreement(form_data)
        else:
            return jsonify({'error': f'Unknown template: {template}'}), 400
            
        # Return the result from document service
        return result
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/templates', methods=['GET'])
def get_templates():
    try:
        templates = [
            {
                'id': 'rental_agreement',
                'name': 'Rental Agreement',
                'description': 'Standard rental/lease agreement',
                'fields': [
                    {'name': 'landlord', 'label': 'Landlord Name', 'type': 'text', 'required': True},
                    {'name': 'tenant', 'label': 'Tenant Name', 'type': 'text', 'required': True},
                    {'name': 'propertyAddress', 'label': 'Property Address', 'type': 'text', 'required': True},
                    {'name': 'rentAmount', 'label': 'Monthly Rent', 'type': 'number', 'required': True},
                    {'name': 'term', 'label': 'Lease Term', 'type': 'text', 'required': True}
                ]
            },
            {
                'id': 'deed_of_sale',
                'name': 'Deed of Sale',
                'description': 'Property sale agreement',
                'fields': [
                    {'name': 'sellerName', 'label': 'Seller Name', 'type': 'text', 'required': True},
                    {'name': 'buyerName', 'label': 'Buyer Name', 'type': 'text', 'required': True},
                    {'name': 'propertyDescription', 'label': 'Property Description', 'type': 'textarea', 'required': True},
                    {'name': 'salePrice', 'label': 'Sale Price', 'type': 'number', 'required': True}
                ]
            },
            {
                'id': 'service_agreement',
                'name': 'Service Agreement',
                'description': 'Standard service contract',
                'fields': [
                    {'name': 'providerName', 'label': 'Service Provider', 'type': 'text', 'required': True},
                    {'name': 'clientName', 'label': 'Client Name', 'type': 'text', 'required': True},
                    {'name': 'serviceDetails', 'label': 'Service Details', 'type': 'textarea', 'required': True},
                    {'name': 'paymentTerms', 'label': 'Payment Terms', 'type': 'textarea', 'required': True}
                ]
            },
            {
                'id': 'employment_contract',
                'name': 'Employment Contract',
                'description': 'Standard employment agreement',
                'fields': [
                    {'name': 'employer', 'label': 'Employer Name', 'type': 'text', 'required': True},
                    {'name': 'employee', 'label': 'Employee Name', 'type': 'text', 'required': True},
                    {'name': 'position', 'label': 'Position/Title', 'type': 'text', 'required': True},
                    {'name': 'salary', 'label': 'Annual Salary', 'type': 'number', 'required': True},
                    {'name': 'startDate', 'label': 'Start Date', 'type': 'date', 'required': True}
                ]
            },
            {
                'id': 'software_license',
                'name': 'Software License Agreement',
                'description': 'Software licensing terms',
                'fields': [
                    {'name': 'licensor', 'label': 'Licensor Name', 'type': 'text', 'required': True},
                    {'name': 'licensee', 'label': 'Licensee Name', 'type': 'text', 'required': True},
                    {'name': 'softwareDescription', 'label': 'Software Description', 'type': 'textarea', 'required': True},
                    {'name': 'licenseTerms', 'label': 'License Terms', 'type': 'textarea', 'required': True}
                ]
            },
            {
                'id': 'healthcare_agreement',
                'name': 'Healthcare Agreement',
                'description': 'Healthcare service agreement',
                'fields': [
                    {'name': 'provider', 'label': 'Healthcare Provider', 'type': 'text', 'required': True},
                    {'name': 'patient', 'label': 'Patient Name', 'type': 'text', 'required': True},
                    {'name': 'serviceDescription', 'label': 'Service Description', 'type': 'textarea', 'required': True},
                    {'name': 'paymentTerms', 'label': 'Payment Terms', 'type': 'textarea', 'required': True}
                ]
            }
        ]
        return jsonify(templates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/scan', methods=['POST'])
def scan_document():
    """
    Process an uploaded document image using OCR
    
    Expected payload: 
    - file: The image file to process
    - documentType: Type of document (general, identification, immigration, legal)
    - userId: Optional user ID for the document owner
    
    Returns OCR processing results and extracted data
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Get document type and user ID from form data
        document_type = request.form.get('documentType', 'general')
        user_id = request.form.get('userId')
        
        # Get current user ID from JWT if available
        try:
            current_user_id = get_jwt_identity()
            if not user_id and current_user_id:
                user_id = current_user_id
        except Exception:
            # User not authenticated - that's okay for this endpoint
            pass
        
        # Store the document image
        storage_result = ocr_storage_service.store_document(file, user_id, document_type)
        
        # Process the document with OCR
        ocr_result = ocr_service.process_image(file, document_type)
        
        # Combine results
        result = {
            **ocr_result,
            "fileUrl": storage_result.get("url") or storage_result.get("secure_url"),
            "fileId": storage_result.get("file_id"),
            "publicId": storage_result.get("public_id"),
            "timestamp": datetime.utcnow().isoformat(),
            "documentType": document_type
        }
        
        # Log the operation
        logging.info(f"Document scanned: {file.filename}, type: {document_type}, user: {user_id}")
        
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error scanning document: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/upload/<case_id>', methods=['POST'])
@jwt_required()
def upload_document(case_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if case exists and user has access
        cases_collection = get_mongo_collection('cases')
        if cases_collection:
            case = cases_collection.find_one({'_id': ObjectId(case_id)})
            if not case:
                return jsonify({'error': 'Case not found'}), 404
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not file or not allowed_file(file.filename or ''):
            return jsonify({'error': 'Invalid file type'}), 400
            
        # Ensure we have a valid filename before calling secure_filename
        filename = file.filename
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        filename = secure_filename(filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Create document record
        document = {
            'filename': unique_filename,
            'original_filename': filename,
            'file_path': file_path,
            'uploaded_by': ObjectId(current_user_id),
            'case_id': ObjectId(case_id),
            'upload_date': datetime.utcnow(),
            'file_type': filename.rsplit('.', 1)[1].lower(),
            'file_size': os.path.getsize(file_path),
            'description': request.form.get('description', '')
        }
        
        # Insert document record
        result = mongo.get_collection('documents').insert_one(document)
        
        # Update case with document reference
        mongo.get_collection('cases').update_one(
            {'_id': ObjectId(case_id)},
            {
                '$push': {'documents': result.inserted_id},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        logger.error(f"Document upload error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/case/<case_id>', methods=['GET'])
@jwt_required()
def get_case_documents(case_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Get case
        case = mongo.get_collection('cases').find_one({'_id': ObjectId(case_id)})
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        # Get documents
        documents = list(mongo.get_collection('documents')
                        .find({'case_id': ObjectId(case_id)})
                        .sort('upload_date', -1))
        
        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            doc['_id'] = str(doc['_id'])
            doc['case_id'] = str(doc['case_id'])
            doc['uploaded_by'] = str(doc['uploaded_by'])
            # Remove file_path from response for security
            doc.pop('file_path', None)
        
        return jsonify({'documents': documents}), 200
        
    except Exception as e:
        logger.error(f"Get case documents error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 
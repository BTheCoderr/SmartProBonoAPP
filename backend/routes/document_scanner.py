# Standard library imports
from datetime import datetime
import functools
import logging
import math
import os
import pathlib
import shutil
import tempfile
import time
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party imports
import bson
from bson import ObjectId
from bson.errors import InvalidId
import cv2
import numpy as np
from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    request,
)
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    verify_jwt_in_request,
)
import pdf2image
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename

# Local imports
from database.mongo_utils import (
    MongoDBError,
    safe_count_documents,
    safe_find,
    safe_insert_one,
)
from utils.mongo import (
    get_mongo_collection,
    get_mongo_db,
)
from database.mongo import mongo

import fitz  # PyMuPDF

def conditional_jwt_required(fn):
    """Decorator to conditionally require JWT based on configuration."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_app.config.get('TESTING') or current_app.config.get('JWT_REQUIRED', True):
            verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper

# Initialize blueprint
scanner_bp = Blueprint('scanner', __name__, url_prefix='/api/scanner')
logger = logging.getLogger(__name__)

class ScannerConfig:
    """Configuration class for document scanner."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'pdf'}
    
    def __init__(self, base_dir: str):
        self.upload_folder = Path(base_dir) / 'scans'
        self.upload_folder.mkdir(parents=True, exist_ok=True)
    
    def get_file_path(self, filename: str) -> Path:
        """Get full path for a file."""
        return self.upload_folder / filename

# Initialize configuration
config = ScannerConfig(os.path.dirname(os.path.dirname(__file__)))

def allowed_file(filename: str) -> bool:
    """
    Check if the file extension is allowed.
    
    Args:
        filename: Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ScannerConfig.ALLOWED_EXTENSIONS

def process_image(image_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Process an image file using OCR.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dict containing OCR results and metadata
    
    Raises:
        ValueError: If image processing fails
        IOError: If file cannot be read
    """
    try:
        # Read image using PIL
        with Image.open(str(image_path)) as img:
            # Convert to RGB if necessary
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')
            
            # Convert to grayscale
            gray = img.convert('L')
            
            # Convert to numpy array for OpenCV processing
            gray_np = np.array(gray)
            
            # Apply Otsu's thresholding
            _, binary = cv2.threshold(gray_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Convert back to PIL Image for Tesseract
            binary_img = Image.fromarray(binary)

            # Perform OCR with error handling
            try:
                text = pytesseract.image_to_string(binary_img)
                ocr_data = pytesseract.image_to_data(binary_img, output_type=pytesseract.Output.DICT)
                
                # Calculate confidence only for valid scores
                confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                
                return {
                    'text': text.strip(),
                    'confidence': round(avg_confidence, 2),
                    'word_count': len(text.split())
                }
            except pytesseract.TesseractError as e:
                logger.error(f"Tesseract OCR error: {str(e)}")
                raise ValueError(f"OCR processing failed: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {str(e)}")
        raise

def process_pdf(pdf_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Process a PDF file using OCR.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dict containing OCR results and metadata
    
    Raises:
        ValueError: If PDF processing fails
    """
    try:
        # Convert PDF to images with error handling
        try:
            images = convert_from_path(str(pdf_path))
        except Exception as e:
            logger.error(f"PDF conversion error: {str(e)}")
            raise ValueError(f"Failed to convert PDF: {str(e)}")

        results: List[Dict[str, Any]] = []
        for i, image in enumerate(images):
            # Process each page
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            try:
                text = pytesseract.image_to_string(gray)
                ocr_data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
                
                confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                
                results.append({
                    'page': i + 1,
                    'text': text,
                    'confidence': round(avg_confidence, 2)
                })
            except pytesseract.TesseractError as e:
                logger.error(f"Tesseract OCR error on page {i+1}: {str(e)}")
                results.append({
                    'page': i + 1,
                    'error': f"OCR failed: {str(e)}",
                    'confidence': 0
                })
        
        return {
            'pages': results,
            'total_pages': len(results),
            'average_confidence': round(
                sum(page.get('confidence', 0) for page in results) / len(results), 2
            ) if results else 0
        }
        
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
        raise

def save_processed_file(temp_path: str, original_filename: str) -> Tuple[str, str]:
    """
    Save a processed file to permanent storage.
    
    Args:
        temp_path: Path to temporary file
        original_filename: Original name of the file
        
    Returns:
        Tuple of (file_id, file_path)
    """
    # Generate unique filename using timestamp
    now = datetime.utcnow()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    secure_name = secure_filename(original_filename)
    base, ext = os.path.splitext(secure_name)
    unique_filename = f"{base}_{timestamp}{ext}"

    # Create year/month subdirectories
    year_month = now.strftime('%Y/%m')
    save_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], year_month)
    os.makedirs(save_dir, exist_ok=True)
    
    # Generate full file path
    file_path = os.path.join(save_dir, unique_filename)
    
    # Copy temp file to final location
    shutil.copy2(temp_path, file_path)
    
    return unique_filename, file_path

@scanner_bp.route('/scan', methods=['POST'])
@jwt_required()
def scan_document():
    """Scan a document using OCR and return extracted text."""
    tmp_path = None
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided', 'success': False}), 400
            
        file = request.files['file']
        if not file.filename or file.filename == '':
            return jsonify({'error': 'No file selected', 'success': False}), 400
            
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed', 'success': False}), 400
        
        # Generate a unique temporary filename to avoid conflicts in concurrent requests
        unique_suffix = str(int(time.time() * 1000)) + '_' + str(os.getpid())
        tmp_path = os.path.join(tempfile.gettempdir(), 
                               f"scan_{unique_suffix}_{secure_filename(file.filename)}")
        file.save(tmp_path)
        
        try:
            # Process the file based on type
            if file.filename.lower().endswith('.pdf'):
                results = process_pdf(tmp_path)
            else:
                results = process_image(tmp_path)
                
            # Add the document to the database if processing successful
            document_type = request.form.get('document_type', 'general')
            case_id = request.form.get('case_id')
            
            # Get user ID from JWT token
            user_id = get_jwt_identity()
            
            # Create document record in MongoDB
            document = {
                'user_id': user_id,
                'filename': file.filename,
                'document_type': document_type,
                'processed_at': datetime.utcnow(),
                'results': results,
                'file_size': os.path.getsize(tmp_path),
                'mime_type': file.content_type
            }
            
            if case_id:
                document['case_id'] = case_id
                
            try:
                # Get MongoDB collection
                db = mongo.db
                if db is not None:
                    document_id = db.scanned_documents.insert_one(document).inserted_id
                    document['_id'] = str(document_id)
            except Exception as e:
                logger.warning(f"Failed to save document to database: {str(e)}")
            
            return jsonify({
                'success': True,
                'results': results
            })
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return jsonify({
                'error': f'Could not process file: {str(e)}',
                'success': False
            }), 400
        finally:
            # Clean up the temporary file
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception as e:
                    logger.warning(f"Failed to remove temporary file {tmp_path}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Scan document error: {str(e)}")
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'success': False
        }), 500

@scanner_bp.route('/capture', methods=['POST'])
@jwt_required()
def capture_image() -> Tuple[Response, int]:
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image data provided', 'success': False}), 400
            
        image_file = request.files['image']
        if not image_file or not image_file.filename:
            return jsonify({'error': 'No image selected', 'success': False}), 400
            
        # Save and process the captured image
        user_id = get_jwt_identity()
        
        filename = secure_filename(f"capture_{user_id}_{int(time.time())}.jpg")
        file_path = config.get_file_path(filename)
        
        try:
            image_file.save(file_path)
            results = process_image(file_path)
            
            # Try to store in MongoDB using our safe wrapper
            try:
                doc_id = safe_insert_one('scanned_documents', {
                    'filename': filename,
                    'upload_date': datetime.utcnow(),
                    'uploaded_by': user_id,
                    'file_type': 'jpg',
                    'processing_results': results
                })
                
                return jsonify({
                    'success': True,
                    'document_id': str(doc_id),
                    'results': results
                }), 200
            except MongoDBError as e:
                logger.warning(f"Failed to store document in MongoDB: {str(e)}")
                return jsonify({
                    'success': True,
                    'results': results,
                    'warning': 'Document metadata not stored'
                }), 200
                
        finally:
            # Clean up temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
        
    except ValueError as e:
        return jsonify({
            'error': 'Processing error',
            'details': str(e),
            'success': False
        }), 400
    except Exception as e:
        logger.error(f"Error in capture_image: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e),
            'success': False
        }), 500

@scanner_bp.route('/documents', methods=['GET'])
@jwt_required()
def get_documents():
    """Get scanned documents with pagination and filtering."""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({
                'error': 'Invalid pagination parameters. Page must be >= 1 and per_page must be between 1 and 100.',
                'success': False
            }), 400
        
        # Get filter parameters
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        document_type = request.args.get('type')
        case_id = request.args.get('case_id')
        
        # Build filter query
        query = {}
        if date_from or date_to:
            date_query = {}
            if date_from:
                try:
                    date_query['$gte'] = datetime.fromisoformat(date_from)
                except ValueError:
                    return jsonify({'error': 'Invalid date_from format. Use ISO format (YYYY-MM-DD).', 'success': False}), 400
            if date_to:
                try:
                    date_query['$lte'] = datetime.fromisoformat(date_to)
                except ValueError:
                    return jsonify({'error': 'Invalid date_to format. Use ISO format (YYYY-MM-DD).', 'success': False}), 400
            query['created_at'] = date_query
        
        if document_type:
            query['document_type'] = document_type
            
        if case_id:
            query['case_id'] = case_id
        
        # Add user_id to query for security (only show user's documents)
        user_id = get_jwt_identity()
        query['user_id'] = user_id
        
        try:
            # Get documents collection
            db = mongo.db
            if db is None:
                return jsonify({'error': 'Database service unavailable', 'success': False}), 503
                
            # Get total count
            total = db.scanned_documents.count_documents(query)
            
            # Get paginated documents
            skip = (page - 1) * per_page
            documents = list(db.scanned_documents.find(query)
                             .sort('processed_at', -1)
                             .skip(skip)
                             .limit(per_page))
            
            # Convert ObjectId to string for JSON serialization
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            return jsonify({
                'documents': documents,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': math.ceil(total / per_page),
                'success': True
            }), 200
        except Exception as e:
            logger.error(f"Database error in get_documents: {str(e)}")
            return jsonify({'error': f'Database error: {str(e)}', 'success': False}), 500
    
    except Exception as e:
        logger.error(f"Error in get_documents: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}', 'success': False}), 500

@scanner_bp.route('/documents/<document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    """Get a specific document by ID."""
    try:
        # Validate ObjectId
        try:
            doc_id = ObjectId(document_id)
        except InvalidId:
            return jsonify({'error': 'Invalid document ID format', 'success': False}), 400
        
        # Get document
        user_id = get_jwt_identity()
        
        try:
            # Get documents collection
            db = mongo.db
            if db is None:
                return jsonify({'error': 'Database service unavailable', 'success': False}), 503
                
            # Find document and check ownership
            document = db.scanned_documents.find_one({
                '_id': doc_id,
                'user_id': user_id
            })
            
            if not document:
                return jsonify({'error': 'Document not found', 'success': False}), 404
            
            # Convert ObjectId to string for JSON serialization
            if '_id' in document:
                document['_id'] = str(document['_id'])
            
            return jsonify({
                'document': document,
                'success': True
            })
            
        except Exception as e:
            logger.error(f"Database error in get_document: {str(e)}")
            return jsonify({'error': f'Database error: {str(e)}', 'success': False}), 500
    
    except Exception as e:
        logger.error(f"Error in get_document: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}', 'success': False}), 500 
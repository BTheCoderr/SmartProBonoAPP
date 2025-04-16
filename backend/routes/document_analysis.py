from flask import Blueprint, request, jsonify, current_app
import os
import json
import logging
from typing import Optional
from werkzeug.utils import secure_filename
from ai.document_analyzer import DocumentAnalyzer
from utils.auth import require_auth
import PyPDF2
import docx
import io

# Configure logging
logger = logging.getLogger(__name__)

# Create the document analysis blueprint
document_analysis_bp = Blueprint('document_analysis', __name__, url_prefix='/api/document-analysis')

# Initialize the document analyzer
analyzer = DocumentAnalyzer()

# Configure upload settings
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size

def allowed_file(filename: Optional[str]) -> bool:
    """Check if file extension is allowed."""
    if not filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_file_content(file) -> Optional[str]:
    """Extract text content from different file types."""
    filename = file.filename.lower()
    content = None
    
    try:
        if filename.endswith('.txt'):
            content = file.read().decode('utf-8')
        elif filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
        elif filename.endswith(('.doc', '.docx')):
            doc = docx.Document(io.BytesIO(file.read()))
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return content.strip() if content else None
    except Exception as e:
        logger.error(f"Error extracting content from file {filename}: {str(e)}")
        return None

@document_analysis_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_document():
    """
    Analyze a document using AI.
    
    Accepts either direct text content or file upload.
    
    Request body (JSON):
        - document_text: The text content of the document (optional if file uploaded)
        - document_type: Optional document type hint
        
    Request files:
        - file: Document file (optional if text provided)
        
    Returns:
        JSON response with analysis results
    """
    try:
        # Get document type from either form data or JSON
        document_type = None
        if request.form:
            document_type = request.form.get('document_type')
        elif request.is_json and request.json:
            document_type = request.json.get('document_type')

        document_text = None

        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                document_text = extract_file_content(file)
                if not document_text:
                    return jsonify({
                        "error": "Could not extract text from file",
                        "allowed_types": list(ALLOWED_EXTENSIONS)
                    }), 400
            else:
                return jsonify({
                    "error": "Invalid file type",
                    "allowed_types": list(ALLOWED_EXTENSIONS)
                }), 400
        # Handle direct text input
        elif request.is_json and request.json:
            document_text = request.json.get('document_text')
        
        if not document_text:
            return jsonify({"error": "No document content provided"}), 400

        # Analyze the document
        try:
            result = analyzer.analyze_document(document_text, document_type)
            return jsonify({
                "success": True,
                "analysis": result
            })
        except ValueError as ve:
            logger.warning(f"Validation error in document analysis: {str(ve)}")
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return jsonify({"error": "Failed to analyze document"}), 500

    except Exception as e:
        logger.error(f"Unexpected error in analyze_document endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@document_analysis_bp.route('/supported-types', methods=['GET'])
def get_supported_document_types():
    """Get a list of supported document types and their descriptions."""
    supported_types = {
        "contract": {
            "name": "Contract/Agreement",
            "description": "Legal agreements between parties",
            "supported_formats": list(ALLOWED_EXTENSIONS)
        },
        "legal_brief": {
            "name": "Legal Brief",
            "description": "Court documents and legal arguments",
            "supported_formats": list(ALLOWED_EXTENSIONS)
        },
        "immigration_form": {
            "name": "Immigration Form",
            "description": "Immigration and visa-related documents",
            "supported_formats": list(ALLOWED_EXTENSIONS)
        },
        "unknown": {
            "name": "Other Legal Document",
            "description": "General legal document analysis",
            "supported_formats": list(ALLOWED_EXTENSIONS)
        }
    }
    
    return jsonify({
        "supported_types": supported_types,
        "max_file_size": MAX_CONTENT_LENGTH,
        "allowed_extensions": list(ALLOWED_EXTENSIONS)
    })

@document_analysis_bp.route('/sample', methods=['GET'])
def get_sample_analysis():
    """
    Get a sample document analysis result.
    
    Query parameters:
    - type: The type of document sample to return (contract, legal_brief, immigration_form)
    
    Returns:
        JSON response with a sample analysis
    """
    document_type = request.args.get('type', 'contract')
    
    # Sample contract text
    if document_type == 'contract':
        sample_text = """
        AGREEMENT
        
        This Agreement is made on April 15, 2023, between ABC Corporation, a Delaware corporation ("Company"), and John Smith, an individual ("Consultant").
        
        1. SERVICES
        Consultant shall provide marketing consulting services to Company as described in Exhibit A.
        
        2. TERM
        This Agreement shall commence on April 20, 2023 and continue until October 20, 2023, unless terminated earlier.
        
        3. COMPENSATION
        Company shall pay Consultant $5,000 per month for services rendered.
        
        4. CONFIDENTIALITY
        Consultant shall maintain all confidential information in strict confidence.
        
        5. INDEMNIFICATION
        Consultant shall indemnify and hold Company harmless from any claims arising from Consultant's performance.
        
        6. TERMINATION
        Either party may terminate this Agreement with 30 days written notice.
        
        IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
        
        ABC Corporation
        By: Jane Doe, CEO
        
        John Smith
        """
    elif document_type == 'legal_brief':
        sample_text = """
        IN THE UNITED STATES DISTRICT COURT
        FOR THE NORTHERN DISTRICT OF CALIFORNIA
        
        Case No. CV-2023-12345
        
        JOHN DOE,
        Plaintiff,
        
        v.
        
        ACME CORPORATION,
        Defendant.
        
        PLAINTIFF'S MOTION FOR SUMMARY JUDGMENT
        
        INTRODUCTION
        
        Plaintiff John Doe respectfully moves this Court for summary judgment pursuant to Rule 56 of the Federal Rules of Civil Procedure.
        
        STATEMENT OF FACTS
        
        On January 15, 2023, Plaintiff was injured while using Defendant's product...
        
        ARGUMENT
        
        I. DEFENDANT BREACHED ITS DUTY OF CARE
        
        Defendant had a duty to design and manufacture safe products. As established in Smith v. Jones, 123 U.S. 456 (2019), manufacturers must...
        
        II. PLAINTIFF IS ENTITLED TO DAMAGES
        
        Under California law, Plaintiff is entitled to compensatory damages...
        
        CONCLUSION
        
        For the foregoing reasons, Plaintiff respectfully requests that this Court grant summary judgment in his favor.
        
        Respectfully submitted,
        
        Jane Smith
        Attorney for Plaintiff
        """
    else:  # immigration form
        sample_text = """
        FORM I-589
        APPLICATION FOR ASYLUM AND WITHHOLDING OF REMOVAL
        
        Full Name: Maria Garcia
        Date of Birth: 05/12/1985
        Nationality: Honduras
        Passport Number: H12345678
        Visa Type: B-2
        
        Travel History:
        01/15/2023 to 01/20/2023 Mexico
        01/21/2023 to Present United States
        
        Purpose of Application:
        Applicant seeks asylum based on political persecution in home country...
        
        Supporting Documents:
        • Passport
        • Birth Certificate
        • Police Reports
        • Witness Statements
        • Medical Records
        
        Declaration:
        I, Maria Garcia, declare under penalty of perjury that the foregoing is true and correct...
        """
    
    # Analyze the sample document
    result = analyzer.analyze_document(sample_text, document_type)
    
    return jsonify({
        "sample_type": document_type,
        "sample_text": sample_text[:200] + "...",  # First 200 chars for preview
        "analysis_result": result
    })

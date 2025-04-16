from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

app = Flask(__name__)
CORS(app)

# Set up Swagger UI
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/api/swagger.json'  # Our API url (can be a local file or url)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "SmartProBonoAPP API Documentation",
        'validatorUrl': None,  # Disable validator
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Route to serve the Swagger JSON file
@app.route('/api/swagger.json')
def swagger_json():
    with open('swagger.json') as f:
        return jsonify(json.load(f))

# Sample document templates
templates = [
    {
        "id": 1,
        "name": "Eviction Appeal",
        "description": "Template for appealing an eviction notice",
        "category": "Housing",
        "required_fields": ["appellant_name", "appellant_address", "case_number", "eviction_date"]
    },
    {
        "id": 2,
        "name": "Small Claims Complaint",
        "description": "Template for filing a small claims court complaint",
        "category": "Consumer",
        "required_fields": ["plaintiff_name", "defendant_name", "claim_amount", "claim_description"]
    },
    {
        "id": 3,
        "name": "Record Expungement",
        "description": "Template for requesting criminal record expungement",
        "category": "Criminal",
        "required_fields": ["petitioner_name", "case_numbers", "conviction_dates", "request_reason"]
    },
    {
        "id": 4,
        "name": "Child Custody Agreement",
        "description": "Template for establishing child custody arrangements",
        "category": "Family Law",
        "required_fields": ["parent1_name", "parent2_name", "children_names", "custody_schedule"]
    },
    {
        "id": 5,
        "name": "Divorce Petition",
        "description": "Template for filing for divorce",
        "category": "Family Law",
        "required_fields": ["petitioner_name", "respondent_name", "marriage_date", "separation_date"]
    },
    {
        "id": 6,
        "name": "DACA Renewal Application",
        "description": "Template for renewing DACA status",
        "category": "Immigration",
        "required_fields": ["applicant_name", "a_number", "daca_expiration_date", "current_address"]
    },
    {
        "id": 7,
        "name": "Employment Discrimination Complaint",
        "description": "Template for filing an employment discrimination complaint",
        "category": "Employment",
        "required_fields": ["complainant_name", "employer_name", "discrimination_basis", "incident_dates"]
    }
]

@app.route('/')
def home():
    return 'SmartProBono API is running!'

@app.route('/api/test')
def test():
    return jsonify({
        'message': 'API is working',
        'status': 'success'
    })

@app.route('/api/document-generator/templates', methods=['GET'])
def get_templates():
    """Returns a list of available document templates"""
    return jsonify(templates)

@app.route('/api/document-generator/generate', methods=['POST'])
def generate_document():
    """Generates a document based on the provided template and data"""
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.json
    template_id = data.get('templateId')
    form_data = data.get('data')
    
    if not template_id or not form_data:
        return jsonify({'error': 'Missing required fields: templateId and data'}), 400
    
    # Find the template
    template = next((t for t in templates if t['id'] == template_id), None)
    if not template:
        return jsonify({'error': f'Template with ID {template_id} not found'}), 404
    
    # Check if all required fields are provided
    missing_fields = [field for field in template['required_fields'] if field not in form_data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # In a real app, we would generate the document here
    # For now, we'll just return a mock response
    document_id = f"doc_{template_id}_{form_data.get('appellant_name', 'user')}".replace(" ", "_")
    
    return jsonify({
        'documentId': document_id,
        'downloadUrl': f'/api/document-generator/download/{document_id}',
        'message': 'Document generated successfully'
    })

@app.route('/api/document-generator/download/<document_id>', methods=['GET'])
def download_document(document_id):
    """Returns a mock download response for a generated document"""
    # In a real app, we would return the actual document
    return jsonify({
        'document_id': document_id,
        'status': 'ready',
        'download_url': f'http://localhost:5003/api/document-generator/download/{document_id}/file'
    })

if __name__ == '__main__':
    print("Starting SmartProBono API server on port 5003")
    app.run(debug=True, port=5003) 
"""
Document Generation Service for SmartProBono
Handles automated generation of legal documents using templates and AI
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DocumentGenerationService:
    """Service for generating legal documents from templates"""
    
    def __init__(self):
        self.templates_dir = "backend/templates"
        self.output_dir = "backend/generated_documents"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available document templates"""
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
            },
            {
                "id": "power_of_attorney",
                "name": "Power of Attorney",
                "description": "General power of attorney document",
                "category": "Estate Planning",
                "fields": [
                    {"name": "principal_name", "label": "Principal Name", "type": "text", "required": True},
                    {"name": "agent_name", "label": "Agent Name", "type": "text", "required": True},
                    {"name": "effective_date", "label": "Effective Date", "type": "date", "required": True},
                    {"name": "powers", "label": "Powers Granted", "type": "textarea", "required": True},
                    {"name": "witness_name", "label": "Witness Name", "type": "text", "required": True}
                ]
            },
            {
                "id": "divorce_petition",
                "name": "Divorce Petition",
                "description": "Petition for dissolution of marriage",
                "category": "Family Law",
                "fields": [
                    {"name": "petitioner_name", "label": "Petitioner Name", "type": "text", "required": True},
                    {"name": "respondent_name", "label": "Respondent Name", "type": "text", "required": True},
                    {"name": "marriage_date", "label": "Date of Marriage", "type": "date", "required": True},
                    {"name": "separation_date", "label": "Date of Separation", "type": "date", "required": True},
                    {"name": "grounds", "label": "Grounds for Divorce", "type": "text", "required": True},
                    {"name": "children", "label": "Number of Children", "type": "number", "required": True}
                ]
            }
        ]
        return templates
    
    def generate_document(self, template_id: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a document from template and form data"""
        try:
            templates = self.get_available_templates()
            template = next((t for t in templates if t["id"] == template_id), None)
            
            if not template:
                return {"success": False, "error": "Template not found"}
            
            # Validate required fields
            missing_fields = []
            for field in template["fields"]:
                if field["required"] and field["name"] not in form_data:
                    missing_fields.append(field["label"])
            
            if missing_fields:
                return {
                    "success": False, 
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                }
            
            # Generate document content
            document_content = self._generate_document_content(template, form_data)
            
            # Create document metadata
            document_id = f"{template_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename = f"{document_id}.html"
            filepath = os.path.join(self.output_dir, filename)
            
            # Save document
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(document_content)
            
            return {
                "success": True,
                "document_id": document_id,
                "filename": filename,
                "filepath": filepath,
                "template_name": template["name"],
                "generated_at": datetime.now().isoformat(),
                "preview_url": f"/api/v1/documents/preview/{document_id}"
            }
            
        except Exception as e:
            logger.error(f"Error generating document: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _generate_document_content(self, template: Dict[str, Any], form_data: Dict[str, Any]) -> str:
        """Generate HTML content for the document"""
        template_id = template["id"]
        
        if template_id == "nda_template":
            return self._generate_nda_content(form_data)
        elif template_id == "employment_contract":
            return self._generate_employment_contract_content(form_data)
        elif template_id == "lease_agreement":
            return self._generate_lease_agreement_content(form_data)
        elif template_id == "power_of_attorney":
            return self._generate_power_of_attorney_content(form_data)
        elif template_id == "divorce_petition":
            return self._generate_divorce_petition_content(form_data)
        else:
            return self._generate_generic_content(template, form_data)
    
    def _generate_nda_content(self, data: Dict[str, Any]) -> str:
        """Generate NDA document content"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Non-Disclosure Agreement</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 20px; }}
        .signature-section {{ margin-top: 40px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>NON-DISCLOSURE AGREEMENT</h1>
    </div>
    
    <div class="section">
        <p>This Non-Disclosure Agreement ("Agreement") is entered into on {data.get('effective_date', '')} between {data.get('company_name', '')} ("Disclosing Party") and {data.get('client_name', '')} ("Receiving Party").</p>
    </div>
    
    <div class="section">
        <h2>1. Definition of Confidential Information</h2>
        <p>For purposes of this Agreement, "Confidential Information" shall include all information, whether written, oral, or in any other form, that is disclosed by the Disclosing Party to the Receiving Party.</p>
    </div>
    
    <div class="section">
        <h2>2. Obligations of Receiving Party</h2>
        <p>The Receiving Party agrees to:</p>
        <ul>
            <li>Hold and maintain the Confidential Information in strict confidence</li>
            <li>Not disclose the Confidential Information to any third parties</li>
            <li>Use the Confidential Information solely for the purpose of evaluating potential business opportunities</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>3. Term</h2>
        <p>This Agreement shall remain in effect for a period of {data.get('confidentiality_period', '')} years from the effective date.</p>
    </div>
    
    <div class="section">
        <h2>4. Governing Law</h2>
        <p>This Agreement shall be governed by and construed in accordance with the laws of {data.get('jurisdiction', '')}.</p>
    </div>
    
    <div class="signature-section">
        <p><strong>Disclosing Party:</strong> {data.get('company_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
        
        <p><strong>Receiving Party:</strong> {data.get('client_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
    </div>
</body>
</html>
        """
    
    def _generate_employment_contract_content(self, data: Dict[str, Any]) -> str:
        """Generate Employment Contract document content"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Employment Contract</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>EMPLOYMENT AGREEMENT</h1>
    </div>
    
    <div class="section">
        <p>This Employment Agreement is entered into between {data.get('company_name', '')} ("Company") and {data.get('employee_name', '')} ("Employee") effective {data.get('start_date', '')}.</p>
    </div>
    
    <div class="section">
        <h2>1. Position and Duties</h2>
        <p>Employee shall serve as {data.get('position', '')} and shall perform such duties as may be assigned by the Company.</p>
    </div>
    
    <div class="section">
        <h2>2. Compensation</h2>
        <p>Employee shall receive an annual salary of ${data.get('salary', '')} payable in accordance with the Company's standard payroll practices.</p>
    </div>
    
    <div class="section">
        <h2>3. Benefits</h2>
        <p>{data.get('benefits', 'Standard benefits package as outlined in the employee handbook.')}</p>
    </div>
    
    <div class="section">
        <h2>4. At-Will Employment</h2>
        <p>This is an at-will employment relationship, meaning either party may terminate this agreement at any time with or without cause.</p>
    </div>
    
    <div class="section">
        <p><strong>Company:</strong> {data.get('company_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
        
        <p><strong>Employee:</strong> {data.get('employee_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
    </div>
</body>
</html>
        """
    
    def _generate_lease_agreement_content(self, data: Dict[str, Any]) -> str:
        """Generate Lease Agreement document content"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Lease Agreement</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>RESIDENTIAL LEASE AGREEMENT</h1>
    </div>
    
    <div class="section">
        <p>This Lease Agreement is entered into between {data.get('landlord_name', '')} ("Landlord") and {data.get('tenant_name', '')} ("Tenant") for the property located at {data.get('property_address', '')}.</p>
    </div>
    
    <div class="section">
        <h2>1. Term of Lease</h2>
        <p>The lease term shall begin on {data.get('lease_start', '')} and end on {data.get('lease_end', '')}.</p>
    </div>
    
    <div class="section">
        <h2>2. Rent</h2>
        <p>Tenant agrees to pay monthly rent of ${data.get('rent_amount', '')} due on the first day of each month.</p>
    </div>
    
    <div class="section">
        <h2>3. Security Deposit</h2>
        <p>Tenant shall provide a security deposit equal to one month's rent upon execution of this agreement.</p>
    </div>
    
    <div class="section">
        <h2>4. Use of Premises</h2>
        <p>The premises shall be used solely for residential purposes and shall not be used for any illegal activities.</p>
    </div>
    
    <div class="section">
        <p><strong>Landlord:</strong> {data.get('landlord_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
        
        <p><strong>Tenant:</strong> {data.get('tenant_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
    </div>
</body>
</html>
        """
    
    def _generate_power_of_attorney_content(self, data: Dict[str, Any]) -> str:
        """Generate Power of Attorney document content"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Power of Attorney</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>POWER OF ATTORNEY</h1>
    </div>
    
    <div class="section">
        <p>I, {data.get('principal_name', '')}, hereby appoint {data.get('agent_name', '')} as my attorney-in-fact to act in my name, place, and stead in any way which I myself could do, if I were personally present, with respect to the following matters:</p>
    </div>
    
    <div class="section">
        <h2>Powers Granted</h2>
        <p>{data.get('powers', '')}</p>
    </div>
    
    <div class="section">
        <h2>Effective Date</h2>
        <p>This Power of Attorney shall become effective on {data.get('effective_date', '')}.</p>
    </div>
    
    <div class="section">
        <h2>Witness</h2>
        <p>This document was signed in the presence of {data.get('witness_name', '')}.</p>
    </div>
    
    <div class="section">
        <p><strong>Principal:</strong> {data.get('principal_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
        
        <p><strong>Agent:</strong> {data.get('agent_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
        
        <p><strong>Witness:</strong> {data.get('witness_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
    </div>
</body>
</html>
        """
    
    def _generate_divorce_petition_content(self, data: Dict[str, Any]) -> str:
        """Generate Divorce Petition document content"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Divorce Petition</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>PETITION FOR DISSOLUTION OF MARRIAGE</h1>
    </div>
    
    <div class="section">
        <p>Petitioner: {data.get('petitioner_name', '')}</p>
        <p>Respondent: {data.get('respondent_name', '')}</p>
    </div>
    
    <div class="section">
        <h2>1. Marriage Information</h2>
        <p>The parties were married on {data.get('marriage_date', '')} and separated on {data.get('separation_date', '')}.</p>
    </div>
    
    <div class="section">
        <h2>2. Grounds for Divorce</h2>
        <p>The grounds for this dissolution are: {data.get('grounds', '')}</p>
    </div>
    
    <div class="section">
        <h2>3. Children</h2>
        <p>The parties have {data.get('children', '0')} minor children.</p>
    </div>
    
    <div class="section">
        <h2>4. Relief Requested</h2>
        <p>Petitioner requests that the Court:</p>
        <ul>
            <li>Dissolve the marriage between the parties</li>
            <li>Determine custody and support of minor children</li>
            <li>Divide marital property and debts</li>
        </ul>
    </div>
    
    <div class="section">
        <p><strong>Petitioner:</strong> {data.get('petitioner_name', '')}</p>
        <p>Signature: _________________________ Date: ___________</p>
    </div>
</body>
</html>
        """
    
    def _generate_generic_content(self, template: Dict[str, Any], data: Dict[str, Any]) -> str:
        """Generate generic document content for unknown templates"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{template.get('name', 'Document')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{template.get('name', 'Document')}</h1>
        <p>{template.get('description', '')}</p>
    </div>
    
    <div class="section">
        <h2>Document Information</h2>
        {self._format_form_data(data)}
    </div>
</body>
</html>
        """
    
    def _format_form_data(self, data: Dict[str, Any]) -> str:
        """Format form data as HTML"""
        html = "<ul>"
        for key, value in data.items():
            html += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>"
        html += "</ul>"
        return html
    
    def get_document_preview(self, document_id: str) -> Optional[str]:
        """Get document preview content"""
        try:
            filename = f"{document_id}.html"
            filepath = os.path.join(self.output_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            logger.error(f"Error getting document preview: {str(e)}")
            return None

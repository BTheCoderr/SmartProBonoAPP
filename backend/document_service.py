from flask import jsonify
import os
from jinja2 import Environment, FileSystemLoader

class DocumentService:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # Try to import pdfkit, but don't fail if it's not available
        try:
            import pdfkit
            self.pdfkit = pdfkit
            self.pdf_enabled = True
        except (ImportError, OSError):
            self.pdf_enabled = False
    
    def generate_rental_agreement(self, data):
        return self._generate_document('rental_agreement.html', {
            'landlord': data.get('landlord'),
            'tenant': data.get('tenant'),
            'property_address': data.get('propertyAddress'),
            'rent_amount': data.get('rentAmount'),
            'term': data.get('term', '12 months')
        })

    def generate_deed_of_sale(self, data):
        return self._generate_document('deed_of_sale.html', {
            'seller': data.get('sellerName'),
            'buyer': data.get('buyerName'),
            'property_description': data.get('propertyDescription'),
            'sale_price': data.get('salePrice')
        })

    def generate_service_agreement(self, data):
        return self._generate_document('service_agreement.html', {
            'provider': data.get('providerName'),
            'client': data.get('clientName'),
            'service_details': data.get('serviceDetails'),
            'payment_terms': data.get('paymentTerms')
        })

    def generate_employment_contract(self, data):
        return self._generate_document('employment_contract.html', {
            'employer': data.get('employer'),
            'employee': data.get('employee'),
            'position': data.get('position'),
            'salary': data.get('salary'),
            'start_date': data.get('startDate')
        })

    def generate_software_license(self, data):
        return self._generate_document('software_license.html', {
            'licensor': data.get('licensor'),
            'licensee': data.get('licensee'),
            'software_description': data.get('softwareDescription'),
            'license_terms': data.get('licenseTerms')
        })

    def generate_healthcare_agreement(self, data):
        return self._generate_document('healthcare_agreement.html', {
            'provider': data.get('provider'),
            'patient': data.get('patient'),
            'service_description': data.get('serviceDescription'),
            'payment_terms': data.get('paymentTerms')
        })

    def _generate_document(self, template_name, data):
        try:
            template = self.env.get_template(template_name)
            html = template.render(**data)
            
            if not self.pdf_enabled:
                return jsonify({
                    'status': 'warning',
                    'message': 'PDF generation is currently disabled. Please install wkhtmltopdf to enable this feature.',
                    'html': html
                }), 200
            
            output_path = os.path.join('generated_docs', template_name.replace('.html', '.pdf'))
            os.makedirs('generated_docs', exist_ok=True)
            
            self.pdfkit.from_string(html, output_path)
            return jsonify({
                'status': 'success',
                'file_path': output_path
            }), 200
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500 
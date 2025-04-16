"""
PDF Generator module for SmartProBono
Provides functionality to generate legal documents as PDFs
"""
import os
import json
import datetime
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

class PDFGenerator:
    """Class for generating PDF documents based on templates and user data"""
    
    def __init__(self, output_dir: str = 'data/generated_pdfs'):
        """Initialize the PDF Generator
        
        Args:
            output_dir: Directory to save generated PDFs
        """
        self.output_dir = output_dir
        self.templates_dir = 'data/templates'
        self.styles = getSampleStyleSheet()
        self._create_dirs()
        self._init_custom_styles()
        
    def _create_dirs(self):
        """Create necessary directories if they don't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            
    def _init_custom_styles(self):
        """Initialize custom paragraph styles"""
        # Check if the style already exists and update it instead of adding a new one
        if 'Title' in self.styles:
            self.styles['Title'].fontSize = 16
            self.styles['Title'].alignment = TA_CENTER
            self.styles['Title'].spaceAfter = 20
        else:
            self.styles.add(ParagraphStyle(
                name='Title',
                parent=self.styles['Heading1'],
                fontSize=16,
                alignment=TA_CENTER,
                spaceAfter=20
            ))
        
        # Check if the style already exists and update it instead of adding a new one
        if 'Subtitle' in self.styles:
            self.styles['Subtitle'].fontSize = 14
        else:
            self.styles.add(ParagraphStyle(
                name='Subtitle',
                parent=self.styles['Heading2'],
                fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        # Check if the style already exists and update it instead of adding a new one
        if 'Normal_Justified' in self.styles:
            self.styles['Normal_Justified'].alignment = TA_JUSTIFY
            self.styles['Normal_Justified'].spaceAfter = 10
        else:
            self.styles.add(ParagraphStyle(
                name='Normal_Justified',
                parent=self.styles['Normal'],
                alignment=TA_JUSTIFY,
                spaceAfter=10
            ))
        
        # Check if the style already exists and update it instead of adding a new one
        if 'Section' in self.styles:
            self.styles['Section'].fontSize = 12
            self.styles['Section'].spaceAfter = 8
        else:
            self.styles.add(ParagraphStyle(
                name='Section',
                parent=self.styles['Heading3'],
                fontSize=12,
                spaceAfter=8
            ))
        
        # Check if the style already exists and update it instead of adding a new one
        if 'Footer' in self.styles:
            self.styles['Footer'].fontSize = 8
        else:
            self.styles.add(ParagraphStyle(
                name='Footer',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.gray,
                alignment=TA_CENTER
            ))
        
    def generate_document(self, 
                         template_type: str, 
                         user_data: Dict[str, Any], 
                         document_data: Dict[str, Any],
                         filename: Optional[str] = None) -> str:
        """Generate a PDF document based on a template and user data
        
        Args:
            template_type: Type of document to generate (e.g., 'eviction_appeal', 'small_claims')
            user_data: User information to include in the document
            document_data: Specific data for the document
            filename: Optional custom filename
            
        Returns:
            Path to the generated PDF file
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{template_type}_{timestamp}.pdf"
            
        output_path = os.path.join(self.output_dir, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Generate content based on template type
        if template_type == "eviction_appeal":
            content = self._generate_eviction_appeal(user_data, document_data)
        elif template_type == "small_claims":
            content = self._generate_small_claims(user_data, document_data)
        elif template_type == "expungement":
            content = self._generate_expungement(user_data, document_data)
        elif template_type == "lease_agreement":
            content = self._generate_lease_agreement(user_data, document_data)
        elif template_type == "child_custody":
            content = self._generate_child_custody(user_data, document_data)
        elif template_type == "discrimination_complaint":
            content = self._generate_discrimination_complaint(user_data, document_data)
        elif template_type == "daca_renewal":
            content = self._generate_daca_renewal(user_data, document_data)
        elif template_type == "divorce_petition":
            content = self._generate_divorce_petition(user_data, document_data)
        else:
            content = self._generate_generic_document(user_data, document_data)
            
        # Build the PDF
        doc.build(content, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        return output_path
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        # Save the state of the canvas
        canvas.saveState()
        
        # Footer with page number
        footer_text = f"Generated by SmartProBono - Page {doc.page} - {datetime.datetime.now().strftime('%Y-%m-%d')}"
        footer = Paragraph(footer_text, self.styles['Footer'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, 0.5 * inch)
        
        # Restore the state of the canvas
        canvas.restoreState()
    
    def _generate_eviction_appeal(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for an eviction appeal document"""
        content = []
        
        # Title
        title = Paragraph("NOTICE OF APPEAL - EVICTION PROCEEDING", self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Court Information
        court_info = f"IN THE {document_data.get('court_name', 'SUPERIOR COURT')}"
        court_para = Paragraph(court_info, self.styles['Subtitle'])
        content.append(court_para)
        
        # Case Information
        case_info = [
            [Paragraph("<b>Case Number:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('case_number', ''), self.styles['Normal'])],
            [Paragraph("<b>Plaintiff/Landlord:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('plaintiff_name', ''), self.styles['Normal'])],
            [Paragraph("<b>Defendant/Tenant:</b>", self.styles['Normal']), 
             Paragraph(f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}", self.styles['Normal'])]
        ]
        
        case_table = Table(case_info, colWidths=[2*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(Spacer(1, 0.25 * inch))
        content.append(case_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Notice of Appeal
        notice_title = Paragraph("NOTICE OF APPEAL", self.styles['Section'])
        content.append(notice_title)
        
        notice_text = f"""
        NOTICE IS HEREBY GIVEN that {user_data.get('first_name', '')} {user_data.get('last_name', '')}, 
        Defendant in the above-entitled action, appeals to the {document_data.get('appeal_court', 'Appellate Division')} 
        from the judgment entered on {document_data.get('judgment_date', '[DATE]')} in the 
        {document_data.get('court_name', 'Superior Court')}.
        """
        
        notice_para = Paragraph(notice_text, self.styles['Normal_Justified'])
        content.append(notice_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Grounds for Appeal
        grounds_title = Paragraph("GROUNDS FOR APPEAL", self.styles['Section'])
        content.append(grounds_title)
        
        grounds_text = document_data.get('grounds_for_appeal', '')
        grounds_para = Paragraph(grounds_text, self.styles['Normal_Justified'])
        content.append(grounds_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature
        date_text = f"Dated: {datetime.datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        content.append(date_para)
        content.append(Spacer(1, 0.5 * inch))
        
        signature_line = Paragraph("_______________________________", self.styles['Normal'])
        content.append(signature_line)
        
        signature_name = Paragraph(f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}", self.styles['Normal'])
        content.append(signature_name)
        
        signature_title = Paragraph("Defendant/Appellant", self.styles['Normal'])
        content.append(signature_title)
        
        return content
    
    def _generate_small_claims(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for a small claims document"""
        content = []
        
        # Title
        title = Paragraph("SMALL CLAIMS COURT COMPLAINT", self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Court Information
        court_info = f"IN THE {document_data.get('court_name', 'SMALL CLAIMS COURT')}"
        court_para = Paragraph(court_info, self.styles['Subtitle'])
        content.append(court_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Plaintiff and Defendant Information
        party_info = [
            [Paragraph("<b>PLAINTIFF:</b>", self.styles['Normal']), 
             Paragraph(f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}", self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), 
             Paragraph(user_data.get('address', ''), self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), 
             Paragraph(f"{user_data.get('city', '')}, {user_data.get('state', '')} {user_data.get('zip', '')}", self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), 
             Paragraph(f"Phone: {user_data.get('phone', '')}", self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), 
             Paragraph(f"Email: {user_data.get('email', '')}", self.styles['Normal'])],
            [Paragraph("<b>DEFENDANT:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('defendant_name', ''), self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), 
             Paragraph(document_data.get('defendant_address', ''), self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), 
             Paragraph(f"{document_data.get('defendant_city', '')}, {document_data.get('defendant_state', '')} {document_data.get('defendant_zip', '')}", self.styles['Normal'])]
        ]
        
        party_table = Table(party_info, colWidths=[1.5*inch, 4.5*inch])
        party_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        content.append(party_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Complaint
        complaint_title = Paragraph("COMPLAINT", self.styles['Section'])
        content.append(complaint_title)
        
        complaint_text = f"""
        1. Plaintiff claims defendant owes ${document_data.get('claim_amount', '0.00')} 
        plus court costs for the following reasons:
        
        {document_data.get('claim_reason', '')}
        
        2. This claim arose on or about {document_data.get('claim_date', '[DATE]')}.
        
        WHEREFORE, Plaintiff demands judgment against Defendant in the sum of 
        ${document_data.get('claim_amount', '0.00')}, plus court costs and any other relief 
        the Court deems just and proper.
        """
        
        complaint_para = Paragraph(complaint_text, self.styles['Normal_Justified'])
        content.append(complaint_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature
        date_text = f"Dated: {datetime.datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        content.append(date_para)
        content.append(Spacer(1, 0.5 * inch))
        
        signature_line = Paragraph("_______________________________", self.styles['Normal'])
        content.append(signature_line)
        
        signature_name = Paragraph(f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}", self.styles['Normal'])
        content.append(signature_name)
        
        signature_title = Paragraph("Plaintiff", self.styles['Normal'])
        content.append(signature_title)
        
        return content
    
    def _generate_expungement(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for an expungement request document"""
        content = []
        
        # Title
        title = Paragraph("PETITION FOR EXPUNGEMENT OF CRIMINAL RECORD", self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Court Information
        court_info = f"IN THE {document_data.get('court_name', 'CIRCUIT COURT')}"
        court_para = Paragraph(court_info, self.styles['Subtitle'])
        content.append(court_para)
        
        jurisdiction = f"{document_data.get('jurisdiction', '')}"
        jurisdiction_para = Paragraph(jurisdiction, self.styles['Subtitle'])
        content.append(jurisdiction_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Case Information
        case_info = [
            [Paragraph("<b>In the Matter of:</b>", self.styles['Normal'])],
            [Paragraph(f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}", self.styles['Normal'])],
            [Paragraph("Petitioner", self.styles['Normal'])],
            [Paragraph(f"DOB: {user_data.get('date_of_birth', '')}", self.styles['Normal'])],
            [Paragraph(f"Case No(s): {document_data.get('case_numbers', '')}", self.styles['Normal'])]
        ]
        
        case_table = Table(case_info, colWidths=[6*inch])
        case_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(case_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Petition
        petition_title = Paragraph("PETITION FOR EXPUNGEMENT OF RECORDS", self.styles['Section'])
        content.append(petition_title)
        
        petition_text = f"""
        COMES NOW the Petitioner, {user_data.get('first_name', '')} {user_data.get('last_name', '')}, 
        and moves this Honorable Court for an Order expunging all official records relating to:
        
        1. The Petitioner's arrest on {document_data.get('arrest_date', '[DATE]')} by the 
        {document_data.get('arresting_agency', '[AGENCY]')};
        
        2. The charge(s) of {document_data.get('charges', '[CHARGES]')};
        
        3. All court proceedings related to these charges.
        
        In support of this Petition, the Petitioner states as follows:
        
        1. That the Petitioner is eligible for expungement under {document_data.get('statute', '[STATUTE]')}.
        
        2. {document_data.get('eligibility_reason', '')}
        
        3. That the expungement of the Petitioner's record would be in the interest of justice and would not pose 
        a risk to public safety.
        
        WHEREFORE, the Petitioner respectfully requests that this Court grant this Petition and order the 
        expungement of all records relating to the Petitioner's arrest, charges, and court proceedings 
        described above.
        """
        
        petition_para = Paragraph(petition_text, self.styles['Normal_Justified'])
        content.append(petition_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature
        date_text = f"Dated: {datetime.datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        content.append(date_para)
        content.append(Spacer(1, 0.5 * inch))
        
        signature_line = Paragraph("_______________________________", self.styles['Normal'])
        content.append(signature_line)
        
        signature_name = Paragraph(f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}", self.styles['Normal'])
        content.append(signature_name)
        
        signature_title = Paragraph("Petitioner", self.styles['Normal'])
        content.append(signature_title)
        
        return content
    
    def _generate_lease_agreement(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for a residential lease agreement document"""
        content = []
        
        # Title
        title = Paragraph("RESIDENTIAL LEASE AGREEMENT", self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Introduction
        intro_text = f"This Residential Lease Agreement (\"Agreement\") is made and entered into on {datetime.datetime.now().strftime('%B %d, %Y')} by and between:"
        intro = Paragraph(intro_text, self.styles['Normal_Justified'])
        content.append(intro)
        content.append(Spacer(1, 0.25 * inch))
        
        # Landlord and Tenant Information
        landlord_text = f"<b>LANDLORD:</b> {document_data.get('landlord_name', '')}, with a mailing address of {document_data.get('landlord_address', '')}, hereinafter referred to as \"LANDLORD\","
        landlord = Paragraph(landlord_text, self.styles['Normal_Justified'])
        content.append(landlord)
        content.append(Spacer(1, 0.15 * inch))
        
        tenant_text = f"<b>TENANT(S):</b> {document_data.get('tenant_name', '')}, hereinafter referred to as \"TENANT\"."
        tenant = Paragraph(tenant_text, self.styles['Normal_Justified'])
        content.append(tenant)
        content.append(Spacer(1, 0.25 * inch))
        
        # Property
        property_title = Paragraph("1. PROPERTY", self.styles['Section'])
        content.append(property_title)
        
        property_text = f"LANDLORD hereby leases to TENANT and TENANT hereby leases from LANDLORD for residential purposes only, the premises known and designated as {document_data.get('tenant_address', '')}, hereinafter referred to as the \"PREMISES\"."
        property_para = Paragraph(property_text, self.styles['Normal_Justified'])
        content.append(property_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Lease Term
        term_title = Paragraph("2. LEASE TERM", self.styles['Section'])
        content.append(term_title)
        
        lease_start = document_data.get('lease_start_date', '')
        lease_end = document_data.get('lease_end_date', '')
        
        term_text = f"The term of this Agreement shall be for a period commencing on {lease_start} and ending on {lease_end}, unless otherwise terminated as provided herein."
        term_para = Paragraph(term_text, self.styles['Normal_Justified'])
        content.append(term_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Rent
        rent_title = Paragraph("3. RENT", self.styles['Section'])
        content.append(rent_title)
        
        monthly_rent = document_data.get('monthly_rent', '')
        payment_due_date = document_data.get('payment_due_date', '1st')
        late_fee = document_data.get('late_fee', '')
        
        rent_text = f"TENANT agrees to pay, without demand, to LANDLORD as rent for the PREMISES, the sum of ${monthly_rent} per month, payable in advance on the {payment_due_date} day of each month. Rent shall be payable to LANDLORD or as LANDLORD may designate. TENANT understands that rent payments not received by the LANDLORD by the {payment_due_date} day of each month will be subject to a late fee of ${late_fee}."
        rent_para = Paragraph(rent_text, self.styles['Normal_Justified'])
        content.append(rent_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Security Deposit
        deposit_title = Paragraph("4. SECURITY DEPOSIT", self.styles['Section'])
        content.append(deposit_title)
        
        security_deposit = document_data.get('security_deposit', '')
        
        deposit_text = f"Upon execution of this Agreement, TENANT shall deposit with LANDLORD the sum of ${security_deposit} as a security deposit, which shall be held as security for the faithful performance by TENANT of all the terms, covenants, and conditions of this Agreement. The security deposit shall be returned to TENANT, without interest, and less any deduction for damages to the PREMISES beyond ordinary wear and tear, unpaid rent, and other charges due under this Agreement, within 30 days after the termination of this Agreement."
        deposit_para = Paragraph(deposit_text, self.styles['Normal_Justified'])
        content.append(deposit_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Pets
        pets_title = Paragraph("5. PETS", self.styles['Section'])
        content.append(pets_title)
        
        pets_allowed = document_data.get('pets_allowed', False)
        pet_deposit = document_data.get('pet_deposit', '0')
        
        if pets_allowed:
            pets_text = f"TENANT is permitted to keep pets on the PREMISES with prior written approval from LANDLORD. TENANT shall pay an additional pet deposit of ${pet_deposit}. TENANT is responsible for any damages caused by pets."
        else:
            pets_text = "No pets shall be kept on the PREMISES without prior written consent of the LANDLORD."
            
        pets_para = Paragraph(pets_text, self.styles['Normal_Justified'])
        content.append(pets_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Additional Terms
        if document_data.get('additional_terms'):
            add_title = Paragraph("6. ADDITIONAL TERMS", self.styles['Section'])
            content.append(add_title)
            
            add_text = document_data.get('additional_terms', '')
            add_para = Paragraph(add_text, self.styles['Normal_Justified'])
            content.append(add_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Signatures
        content.append(Spacer(1, 0.5 * inch))
        
        signature_text = "IN WITNESS WHEREOF, the parties have executed this Agreement on the date first above written."
        signature_para = Paragraph(signature_text, self.styles['Normal'])
        content.append(signature_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature lines
        landlord_sign = Paragraph("________________________________", self.styles['Normal'])
        content.append(landlord_sign)
        landlord_name = Paragraph(f"LANDLORD: {document_data.get('landlord_name', '')}", self.styles['Normal'])
        content.append(landlord_name)
        content.append(Spacer(1, 0.5 * inch))
        
        tenant_sign = Paragraph("________________________________", self.styles['Normal'])
        content.append(tenant_sign)
        tenant_name = Paragraph(f"TENANT: {document_data.get('tenant_name', '')}", self.styles['Normal'])
        content.append(tenant_name)
        
        return content
    
    def _generate_generic_document(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for a generic legal document"""
        content = []
        
        # Title
        title = Paragraph(document_data.get('title', 'LEGAL DOCUMENT'), self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Document body
        if 'sections' in document_data:
            for section in document_data['sections']:
                section_title = Paragraph(section.get('title', ''), self.styles['Section'])
                content.append(section_title)
                
                section_text = section.get('content', '')
                section_para = Paragraph(section_text, self.styles['Normal_Justified'])
                content.append(section_para)
                content.append(Spacer(1, 0.25 * inch))
        else:
            body_text = document_data.get('body', '')
            body_para = Paragraph(body_text, self.styles['Normal_Justified'])
            content.append(body_para)
            
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature
        date_text = f"Dated: {datetime.datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        content.append(date_para)
        content.append(Spacer(1, 0.5 * inch))
        
        signature_line = Paragraph("_______________________________", self.styles['Normal'])
        content.append(signature_line)
        
        signature_name = Paragraph(f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}", self.styles['Normal'])
        content.append(signature_name)
        
        return content

    def _generate_child_custody(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for a child custody agreement document"""
        content = []
        
        # Title
        title = Paragraph("CHILD CUSTODY AGREEMENT", self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Court Information
        court_info = f"IN THE {document_data.get('court_name', 'FAMILY COURT')}"
        court_para = Paragraph(court_info, self.styles['Subtitle'])
        content.append(court_para)
        
        # Case Information (if applicable)
        if document_data.get('case_number'):
            case_info = f"CASE NO. {document_data.get('case_number', '')}"
            case_para = Paragraph(case_info, self.styles['Normal'])
            content.append(case_para)
        
        content.append(Spacer(1, 0.25 * inch))
        
        # Introduction
        intro_text = f"This Child Custody Agreement (\"Agreement\") is made and entered into on {datetime.datetime.now().strftime('%B %d, %Y')} by and between:"
        intro = Paragraph(intro_text, self.styles['Normal_Justified'])
        content.append(intro)
        content.append(Spacer(1, 0.25 * inch))
        
        # Parents Information
        parent1_text = f"<b>Parent 1:</b> {document_data.get('parent1_name', '')}, residing at {document_data.get('parent1_address', '')}, hereinafter referred to as \"Parent 1\","
        parent1 = Paragraph(parent1_text, self.styles['Normal_Justified'])
        content.append(parent1)
        content.append(Spacer(1, 0.15 * inch))
        
        parent2_text = f"<b>Parent 2:</b> {document_data.get('parent2_name', '')}, residing at {document_data.get('parent2_address', '')}, hereinafter referred to as \"Parent 2\"."
        parent2 = Paragraph(parent2_text, self.styles['Normal_Justified'])
        content.append(parent2)
        content.append(Spacer(1, 0.25 * inch))
        
        # Children Information
        children_title = Paragraph("1. CHILDREN", self.styles['Section'])
        content.append(children_title)
        
        children_text = f"This Agreement concerns the following minor child(ren):\n{document_data.get('child_names', '')}"
        children_para = Paragraph(children_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
        content.append(children_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Legal and Physical Custody
        custody_title = Paragraph("2. LEGAL AND PHYSICAL CUSTODY", self.styles['Section'])
        content.append(custody_title)
        
        custody_type = document_data.get('custody_type', '')
        primary_residence = document_data.get('primary_residence', '')
        
        custody_text = f"The parties agree that the legal and physical custody of the child(ren) shall be: {custody_type}."
        custody_para = Paragraph(custody_text, self.styles['Normal_Justified'])
        content.append(custody_para)
        content.append(Spacer(1, 0.15 * inch))
        
        residence_text = f"The primary residence of the child(ren) shall be with: {primary_residence}."
        residence_para = Paragraph(residence_text, self.styles['Normal_Justified'])
        content.append(residence_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Visitation Schedule
        visitation_title = Paragraph("3. VISITATION SCHEDULE", self.styles['Section'])
        content.append(visitation_title)
        
        visitation_text = document_data.get('visitation_schedule', '')
        visitation_para = Paragraph(visitation_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
        content.append(visitation_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Holiday Schedule
        holiday_title = Paragraph("4. HOLIDAY SCHEDULE", self.styles['Section'])
        content.append(holiday_title)
        
        holiday_text = document_data.get('holiday_schedule', '')
        holiday_para = Paragraph(holiday_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
        content.append(holiday_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Transportation
        if document_data.get('transportation'):
            transport_title = Paragraph("5. TRANSPORTATION ARRANGEMENTS", self.styles['Section'])
            content.append(transport_title)
            
            transport_text = document_data.get('transportation', '')
            transport_para = Paragraph(transport_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(transport_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Communication
        comm_section = 5 if not document_data.get('transportation') else 6
        if document_data.get('communication'):
            comm_title = Paragraph(f"{comm_section}. COMMUNICATION BETWEEN PARENTS", self.styles['Section'])
            content.append(comm_title)
            
            comm_text = document_data.get('communication', '')
            comm_para = Paragraph(comm_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(comm_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Special Provisions
        special_section = comm_section + (1 if document_data.get('communication') else 0)
        if document_data.get('special_provisions'):
            special_title = Paragraph(f"{special_section}. SPECIAL PROVISIONS", self.styles['Section'])
            content.append(special_title)
            
            special_text = document_data.get('special_provisions', '')
            special_para = Paragraph(special_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(special_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Signatures
        content.append(Spacer(1, 0.5 * inch))
        
        signature_text = "IN WITNESS WHEREOF, the parties have executed this Agreement on the date first above written."
        signature_para = Paragraph(signature_text, self.styles['Normal'])
        content.append(signature_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature lines
        parent1_sign = Paragraph("________________________________", self.styles['Normal'])
        content.append(parent1_sign)
        parent1_name = Paragraph(f"Parent 1: {document_data.get('parent1_name', '')}", self.styles['Normal'])
        content.append(parent1_name)
        content.append(Spacer(1, 0.5 * inch))
        
        parent2_sign = Paragraph("________________________________", self.styles['Normal'])
        content.append(parent2_sign)
        parent2_name = Paragraph(f"Parent 2: {document_data.get('parent2_name', '')}", self.styles['Normal'])
        content.append(parent2_name)
        
        return content

    def _generate_discrimination_complaint(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for an employment discrimination complaint document"""
        content = []
        
        # Title
        title = Paragraph("EMPLOYMENT DISCRIMINATION COMPLAINT", self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Complainant Information
        complainant_title = Paragraph("COMPLAINANT INFORMATION", self.styles['Section'])
        content.append(complainant_title)
        
        complainant_info = [
            [Paragraph("<b>Name:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('complainant_name', ''), self.styles['Normal'])],
            [Paragraph("<b>Address:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('complainant_address', ''), self.styles['Normal'])],
            [Paragraph("<b>Phone:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('complainant_phone', ''), self.styles['Normal'])],
            [Paragraph("<b>Email:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('complainant_email', ''), self.styles['Normal'])]
        ]
        
        complainant_table = Table(complainant_info, colWidths=[2*inch, 4*inch])
        complainant_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(complainant_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Employer Information
        employer_title = Paragraph("EMPLOYER INFORMATION", self.styles['Section'])
        content.append(employer_title)
        
        employer_info = [
            [Paragraph("<b>Name:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('employer_name', ''), self.styles['Normal'])],
            [Paragraph("<b>Address:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('employer_address', ''), self.styles['Normal'])],
            [Paragraph("<b>Phone:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('employer_phone', ''), self.styles['Normal'])],
            [Paragraph("<b>Your Position/Title:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('position_title', ''), self.styles['Normal'])],
            [Paragraph("<b>Date of Hire:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('hire_date', ''), self.styles['Normal'])]
        ]
        
        employer_table = Table(employer_info, colWidths=[2*inch, 4*inch])
        employer_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(employer_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Discrimination Information
        discrim_title = Paragraph("DISCRIMINATION INFORMATION", self.styles['Section'])
        content.append(discrim_title)
        
        discrim_info = [
            [Paragraph("<b>Type of Discrimination:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('discrimination_type', ''), self.styles['Normal'])],
            [Paragraph("<b>Date(s) of Discrimination:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('incident_date', ''), self.styles['Normal'])]
        ]
        
        discrim_table = Table(discrim_info, colWidths=[2*inch, 4*inch])
        discrim_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(discrim_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Details of Discrimination
        details_title = Paragraph("DETAILS OF DISCRIMINATORY ACTS", self.styles['Section'])
        content.append(details_title)
        
        details_text = document_data.get('details', '')
        details_para = Paragraph(details_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
        content.append(details_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Witnesses
        if document_data.get('witnesses'):
            witnesses_title = Paragraph("WITNESSES", self.styles['Section'])
            content.append(witnesses_title)
            
            witnesses_text = document_data.get('witnesses', '')
            witnesses_para = Paragraph(witnesses_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(witnesses_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Reporting to Employer
        report_title = Paragraph("PREVIOUS REPORTING", self.styles['Section'])
        content.append(report_title)
        
        reported = document_data.get('reported', 'No')
        report_text = f"Did you report this discrimination to your employer? {reported}"
        report_para = Paragraph(report_text, self.styles['Normal'])
        content.append(report_para)
        content.append(Spacer(1, 0.15 * inch))
        
        if reported == 'Yes' and document_data.get('report_details'):
            report_details_text = document_data.get('report_details', '')
            report_details_para = Paragraph(report_details_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(report_details_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Remedy Sought
        remedy_title = Paragraph("REMEDY SOUGHT", self.styles['Section'])
        content.append(remedy_title)
        
        remedy_text = document_data.get('remedy_sought', '')
        remedy_para = Paragraph(remedy_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
        content.append(remedy_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Declaration
        declaration_title = Paragraph("DECLARATION", self.styles['Section'])
        content.append(declaration_title)
        
        declaration_text = "I declare under penalty of perjury that the foregoing is true and correct to the best of my knowledge and belief."
        declaration_para = Paragraph(declaration_text, self.styles['Normal_Justified'])
        content.append(declaration_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature
        date_text = f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        content.append(date_para)
        content.append(Spacer(1, 0.25 * inch))
        
        signature_line = Paragraph("_______________________________", self.styles['Normal'])
        content.append(signature_line)
        
        signature_name = Paragraph(f"Signature of {document_data.get('complainant_name', '')}", self.styles['Normal'])
        content.append(signature_name)
        
        return content

    def _generate_daca_renewal(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for a DACA renewal application document"""
        content = []
        
        # Title
        title = Paragraph("DEFERRED ACTION FOR CHILDHOOD ARRIVALS (DACA)", self.styles['Title'])
        content.append(title)
        subtitle = Paragraph("RENEWAL REQUEST", self.styles['Subtitle'])
        content.append(subtitle)
        content.append(Spacer(1, 0.25 * inch))
        
        # Notice
        notice_text = "THIS IS NOT AN OFFICIAL GOVERNMENT FORM. This document is intended to help you prepare information for your DACA renewal application (Form I-821D). You must submit your renewal request to USCIS using the official government forms."
        notice = Paragraph(notice_text, self.styles['Normal'])
        content.append(notice)
        content.append(Spacer(1, 0.25 * inch))
        
        # Applicant Information
        app_title = Paragraph("PART 1. INFORMATION ABOUT YOU", self.styles['Section'])
        content.append(app_title)
        
        applicant_info = [
            [Paragraph("<b>Full Legal Name:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('full_name', ''), self.styles['Normal'])],
            [Paragraph("<b>Other Names Used (if any):</b>", self.styles['Normal']), 
             Paragraph(document_data.get('other_names', ''), self.styles['Normal'])],
            [Paragraph("<b>Date of Birth:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('dob', ''), self.styles['Normal'])],
            [Paragraph("<b>Country of Birth:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('country_of_birth', ''), self.styles['Normal'])],
            [Paragraph("<b>Current Address:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('current_address', ''), self.styles['Normal'])],
            [Paragraph("<b>Mailing Address (if different):</b>", self.styles['Normal']), 
             Paragraph(document_data.get('mailing_address', ''), self.styles['Normal'])]
        ]
        
        applicant_table = Table(applicant_info, colWidths=[2.5*inch, 3.5*inch])
        applicant_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(applicant_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # DACA Information
        daca_title = Paragraph("PART 2. DACA INFORMATION", self.styles['Section'])
        content.append(daca_title)
        
        daca_info = [
            [Paragraph("<b>Current DACA Expiration Date:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('current_daca_expires', ''), self.styles['Normal'])],
            [Paragraph("<b>Alien Registration Number (A-Number):</b>", self.styles['Normal']), 
             Paragraph(document_data.get('alien_registration_number', ''), self.styles['Normal'])],
            [Paragraph("<b>Social Security Number:</b>", self.styles['Normal']), 
             Paragraph(document_data.get('social_security_number', ''), self.styles['Normal'])],
            [Paragraph("<b>USCIS Online Account Number (if any):</b>", self.styles['Normal']), 
             Paragraph(document_data.get('uscis_online_account_number', ''), self.styles['Normal'])]
        ]
        
        daca_table = Table(daca_info, colWidths=[2.5*inch, 3.5*inch])
        daca_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(daca_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Residence Information
        residence_title = Paragraph("PART 3. RESIDENCE INFORMATION", self.styles['Section'])
        content.append(residence_title)
        
        continuous_residence = document_data.get('continuous_residence', 'No')
        residence_text = f"Do you confirm continuous residence in the United States since your last approved DACA request? {continuous_residence}"
        residence_para = Paragraph(residence_text, self.styles['Normal'])
        content.append(residence_para)
        content.append(Spacer(1, 0.15 * inch))
        
        if document_data.get('residence_changes'):
            changes_title = Paragraph("Address Changes Since Last Application:", self.styles['Normal'])
            content.append(changes_title)
            
            changes_text = document_data.get('residence_changes', '')
            changes_para = Paragraph(changes_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(changes_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Travel Information
        travel_title = Paragraph("PART 4. TRAVEL INFORMATION", self.styles['Section'])
        content.append(travel_title)
        
        travel = document_data.get('travel_outside_us', 'No')
        travel_text = f"Have you traveled outside the United States since your last approved DACA request? {travel}"
        travel_para = Paragraph(travel_text, self.styles['Normal'])
        content.append(travel_para)
        content.append(Spacer(1, 0.15 * inch))
        
        if travel == 'Yes' and document_data.get('travel_details'):
            travel_details_title = Paragraph("Travel Details:", self.styles['Normal'])
            content.append(travel_details_title)
            
            travel_details_text = document_data.get('travel_details', '')
            travel_details_para = Paragraph(travel_details_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(travel_details_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Criminal History Information
        criminal_title = Paragraph("PART 5. CRIMINAL HISTORY", self.styles['Section'])
        content.append(criminal_title)
        
        criminal = document_data.get('criminal_history', 'No')
        criminal_text = f"Have you been arrested for, charged with, or convicted of a felony or misdemeanor in the United States since your last approved DACA request? {criminal}"
        criminal_para = Paragraph(criminal_text, self.styles['Normal'])
        content.append(criminal_para)
        content.append(Spacer(1, 0.15 * inch))
        
        if criminal == 'Yes' and document_data.get('criminal_details'):
            criminal_details_title = Paragraph("Criminal History Details:", self.styles['Normal'])
            content.append(criminal_details_title)
            
            criminal_details_text = document_data.get('criminal_details', '')
            criminal_details_para = Paragraph(criminal_details_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(criminal_details_para)
            content.append(Spacer(1, 0.25 * inch))
        
        # Declaration
        declaration_title = Paragraph("DECLARATION", self.styles['Section'])
        content.append(declaration_title)
        
        declaration_text = "I certify, under penalty of perjury under the laws of the United States of America, that the foregoing is true and correct. I understand that any false statements made on this form may result in denial of my DACA request, revocation of my DACA, and/or removal from the United States."
        declaration_para = Paragraph(declaration_text, self.styles['Normal_Justified'])
        content.append(declaration_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature
        date_text = f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        content.append(date_para)
        content.append(Spacer(1, 0.25 * inch))
        
        signature_line = Paragraph("_______________________________", self.styles['Normal'])
        content.append(signature_line)
        
        signature_name = Paragraph(f"Signature of {document_data.get('full_name', '')}", self.styles['Normal'])
        content.append(signature_name)
        
        return content

    def _generate_divorce_petition(self, user_data: Dict[str, Any], document_data: Dict[str, Any]) -> List:
        """Generate content for a divorce petition document"""
        content = []
        
        # Title
        title = Paragraph("PETITION FOR DISSOLUTION OF MARRIAGE", self.styles['Title'])
        content.append(title)
        content.append(Spacer(1, 0.25 * inch))
        
        # Court Information
        court_info = f"IN THE {document_data.get('court_name', 'CIRCUIT COURT')} FOR {document_data.get('county', 'COUNTY')}"
        court_para = Paragraph(court_info, self.styles['Subtitle'])
        content.append(court_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Party Information
        party_title = Paragraph("IN RE: THE MARRIAGE OF", self.styles['Section'])
        content.append(party_title)
        
        petitioner_text = f"<b>Petitioner:</b> {document_data.get('petitioner_name', '')}"
        petitioner = Paragraph(petitioner_text, self.styles['Normal'])
        content.append(petitioner)
        content.append(Spacer(1, 0.15 * inch))
        
        respondent_text = f"<b>Respondent:</b> {document_data.get('respondent_name', '')}"
        respondent = Paragraph(respondent_text, self.styles['Normal'])
        content.append(respondent)
        content.append(Spacer(1, 0.25 * inch))
        
        # Introduction
        intro_text = f"COMES NOW the Petitioner, {document_data.get('petitioner_name', '')}, and petitions this Court for a dissolution of marriage from the Respondent, {document_data.get('respondent_name', '')}, and in support thereof states as follows:"
        intro = Paragraph(intro_text, self.styles['Normal_Justified'])
        content.append(intro)
        content.append(Spacer(1, 0.25 * inch))
        
        # Jurisdiction
        jurisdiction_title = Paragraph("1. JURISDICTION AND VENUE", self.styles['Section'])
        content.append(jurisdiction_title)
        
        jurisdiction_text = f"Petitioner resides at {document_data.get('petitioner_address', '')}, and Respondent resides at {document_data.get('respondent_address', '')}. Petitioner has been a resident of this county and state for more than six months immediately prior to the filing of this Petition."
        jurisdiction_para = Paragraph(jurisdiction_text, self.styles['Normal_Justified'])
        content.append(jurisdiction_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Marriage Information
        marriage_title = Paragraph("2. MARRIAGE INFORMATION", self.styles['Section'])
        content.append(marriage_title)
        
        marriage_date = document_data.get('marriage_date', '')
        marriage_place = document_data.get('marriage_place', '')
        separation_date = document_data.get('separation_date', '')
        
        marriage_text = f"The parties were married on {marriage_date} in {marriage_place}. The parties separated on or about {separation_date} and have remained living separate and apart since that date."
        marriage_para = Paragraph(marriage_text, self.styles['Normal_Justified'])
        content.append(marriage_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Children
        children_title = Paragraph("3. MINOR CHILDREN", self.styles['Section'])
        content.append(children_title)
        
        children = document_data.get('children', 'No')
        if children == 'Yes' and document_data.get('children_details'):
            children_text = f"The parties have the following minor children of the marriage:\n{document_data.get('children_details', '')}"
            children_para = Paragraph(children_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(children_para)
        else:
            children_text = "There are no minor children of the marriage."
            children_para = Paragraph(children_text, self.styles['Normal_Justified'])
            content.append(children_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Grounds for Divorce
        grounds_title = Paragraph("4. GROUNDS FOR DIVORCE", self.styles['Section'])
        content.append(grounds_title)
        
        grounds = document_data.get('grounds', '')
        grounds_details = document_data.get('grounds_details', '')
        
        if grounds == 'Other' and grounds_details:
            grounds_text = f"The marriage of the parties is irretrievably broken on the grounds of {grounds_details}."
        else:
            grounds_text = f"The marriage of the parties is irretrievably broken on the grounds of {grounds}."
            
        grounds_para = Paragraph(grounds_text, self.styles['Normal_Justified'])
        content.append(grounds_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Property Division
        property_title = Paragraph("5. PROPERTY DIVISION", self.styles['Section'])
        content.append(property_title)
        
        property_text = document_data.get('property_division', '')
        property_para = Paragraph(property_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
        content.append(property_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Debt Division
        debt_title = Paragraph("6. DEBT DIVISION", self.styles['Section'])
        content.append(debt_title)
        
        debt_text = document_data.get('debt_division', '')
        debt_para = Paragraph(debt_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
        content.append(debt_para)
        content.append(Spacer(1, 0.25 * inch))
        
        # Additional Sections
        section_count = 7
        
        # Spousal Support
        if document_data.get('spousal_support'):
            support_title = Paragraph(f"{section_count}. SPOUSAL SUPPORT", self.styles['Section'])
            content.append(support_title)
            
            support_text = document_data.get('spousal_support', '')
            support_para = Paragraph(support_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(support_para)
            content.append(Spacer(1, 0.25 * inch))
            section_count += 1
        
        # Child Custody
        if children == 'Yes' and document_data.get('child_custody'):
            custody_title = Paragraph(f"{section_count}. CHILD CUSTODY", self.styles['Section'])
            content.append(custody_title)
            
            custody_text = document_data.get('child_custody', '')
            custody_para = Paragraph(custody_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(custody_para)
            content.append(Spacer(1, 0.25 * inch))
            section_count += 1
        
        # Child Support
        if children == 'Yes' and document_data.get('child_support'):
            support_title = Paragraph(f"{section_count}. CHILD SUPPORT", self.styles['Section'])
            content.append(support_title)
            
            support_text = document_data.get('child_support', '')
            support_para = Paragraph(support_text.replace('\n', '<br/>'), self.styles['Normal_Justified'])
            content.append(support_para)
            content.append(Spacer(1, 0.25 * inch))
            section_count += 1
        
        # Name Change
        if document_data.get('name_change') == 'Yes' and document_data.get('previous_name'):
            name_title = Paragraph(f"{section_count}. NAME CHANGE", self.styles['Section'])
            content.append(name_title)
            
            name_text = f"Petitioner requests that their name be restored to their former name: {document_data.get('previous_name', '')}."
            name_para = Paragraph(name_text, self.styles['Normal_Justified'])
            content.append(name_para)
            content.append(Spacer(1, 0.25 * inch))
            section_count += 1
        
        # Prayer for Relief
        relief_title = Paragraph(f"{section_count}. PRAYER FOR RELIEF", self.styles['Section'])
        content.append(relief_title)
        
        relief_text = "WHEREFORE, Petitioner prays that this Court grant a decree of dissolution of marriage, and for such other and further relief as this Court deems just and proper."
        relief_para = Paragraph(relief_text, self.styles['Normal_Justified'])
        content.append(relief_para)
        content.append(Spacer(1, 0.5 * inch))
        
        # Signature
        signature_text = "Respectfully submitted,"
        signature_para = Paragraph(signature_text, self.styles['Normal'])
        content.append(signature_para)
        content.append(Spacer(1, 0.5 * inch))
        
        date_text = f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        content.append(date_para)
        content.append(Spacer(1, 0.25 * inch))
        
        signature_line = Paragraph("_______________________________", self.styles['Normal'])
        content.append(signature_line)
        
        signature_name = Paragraph(f"{document_data.get('petitioner_name', '')}, Petitioner", self.styles['Normal'])
        content.append(signature_name)
        
        return content

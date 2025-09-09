"""Enhanced AI service for legal analysis and document processing with safety features"""
import logging
import random
import requests
import json
import re
from datetime import datetime
from PyPDF2 import PdfReader

# PDF generation imports
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    import base64
    import io
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Safety and compliance patterns
ADVICE_PATTERNS = [
    r"\b(i advise|i recommend|you should|you must|you need to)\b",
    r"\b(file .* by|plead .*|sign .*|submit form)\b",
    r"\b(this constitutes legal advice|this is legal advice)\b",
    r"\b(you are required to|you must do|you should do)\b",
    r"\b(hire a lawyer|get a lawyer|contact an attorney)\b",
]

UNCERTAINTY_PATTERNS = [
    r"\b(i am not sure|i don't know|unclear|uncertain)\b",
    r"\b(consult.*attorney|speak.*lawyer|get.*legal.*help)\b",
    r"\b(this.*complex|this.*complicated|this.*difficult)\b",
]

logger = logging.getLogger(__name__)

class SimpleAIService:
    """Simple service for AI-based legal assistance and document analysis"""
    
    @staticmethod
    def analyze_document(document_path, document_type="generic", questions=None):
        """
        Analyze a legal document using real text extraction
        
        Args:
            document_path (str): Path to the document file
            document_type (str): The type of document
            questions (list, optional): Specific questions to answer about the document
            
        Returns:
            dict: The analysis results
        """
        try:
            # Extract text from the document
            extracted_text = SimpleAIService.extract_text_from_document(document_path)
            
            if not extracted_text:
                return {
                    "error": "Could not extract text from document",
                    "document_type": document_type,
                    "confidence": 0.0
                }
            
            # Analyze the extracted text
            analysis = SimpleAIService._analyze_extracted_text(extracted_text, document_type)
            
            # Add extracted text to the analysis
            analysis["extracted_text"] = extracted_text
            analysis["text_length"] = len(extracted_text)
            analysis["word_count"] = len(extracted_text.split())
            
            # If questions were provided, add answers based on extracted text
            if questions:
                analysis["answers"] = {}
                for question in questions:
                    analysis["answers"][question] = SimpleAIService._answer_question_from_text(extracted_text, question)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return {
                "error": "An error occurred while analyzing the document",
                "created_at": datetime.now().isoformat()
            }
    
    @staticmethod
    def extract_text_from_document(document_path):
        """
        Extract text from a document
        
        Args:
            document_path (str): Path to the document
            
        Returns:
            str: The extracted text
        """
        try:
            import os
            
            # Check if file exists
            if not os.path.exists(document_path):
                logger.error(f"Document file not found: {document_path}")
                return None
            
            # Get file extension
            file_ext = os.path.splitext(document_path)[1].lower()
            
            if file_ext == '.pdf':
                # Extract text from PDF using PyPDF2
                reader = PdfReader(document_path)
                text = ""
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {str(e)}")
                        continue
                
                if text.strip():
                    logger.info(f"Successfully extracted {len(text)} characters from PDF")
                    return text.strip()
                else:
                    logger.warning("No text could be extracted from PDF")
                    return None
                    
            else:
                # For other file types, return a placeholder
                logger.warning(f"File type {file_ext} not supported for text extraction")
                return f"Text extraction not supported for {file_ext} files"
                
        except Exception as e:
            logger.error(f"Error extracting text from document: {str(e)}")
            return None

    @staticmethod
    def _analyze_extracted_text(text, document_type="generic"):
        """
        Analyze extracted text to identify legal document characteristics
        
        Args:
            text (str): The extracted text from the document
            document_type (str): The type of document
            
        Returns:
            dict: Analysis results
        """
        try:
            # Convert to lowercase for analysis
            text_lower = text.lower()
            
            # Basic document analysis
            analysis = {
                "document_type": document_type,
                "confidence": 0.85,
                "analysis_date": datetime.now().isoformat(),
                "client_summary": "",
                "parties": [],
                "key_dates": [],
                "monetary_amounts": [],
                "legal_terms": [],
                "potential_issues": [],
                "recommendations": [],
                "action_items": [],
                "risk_level": "medium"
            }
            
            # Extract parties with better patterns
            parties = []
            
            # Look for specific party patterns
            party_patterns = [
                # Landlord/Tenant patterns with colon
                r'(?:landlord|lessor)\s*:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
                r'(?:tenant|lessee)\s*:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
                # Plaintiff/Defendant patterns with colon
                r'(?:plaintiff)\s*:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
                r'(?:defendant)\s*:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
                # Between patterns
                r'between\s+([A-Z][a-z]+\s+[A-Z][a-z]+)\s+and\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
                # Direct name patterns after labels
                r'(?:landlord|tenant|plaintiff|defendant|buyer|seller)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            ]
            
            for pattern in party_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        for name in match:
                            clean_name = name.strip().rstrip('.,')
                            if len(clean_name) > 2 and len(clean_name.split()) <= 3:
                                parties.append(clean_name)
                    else:
                        clean_name = match.strip().rstrip('.,')
                        if len(clean_name) > 2 and len(clean_name.split()) <= 3:
                            parties.append(clean_name)
            
            # Clean up and deduplicate parties
            analysis["parties"] = []
            seen = set()
            for party in parties:
                party_lower = party.lower()
                if party_lower not in seen and not any(word in party_lower for word in ['party', 'plaintiff', 'defendant', 'landlord', 'tenant', 'agreement', 'document']):
                    analysis["parties"].append(party)
                    seen.add(party_lower)
            
            # Extract dates
            date_patterns = [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                analysis["key_dates"].extend(matches)
            
            # Extract monetary amounts
            money_patterns = [
                r'\$[\d,]+\.?\d*',
                r'\b\d+\.\d{2}\s*(?:dollars?|USD)\b',
                r'\b(?:amount|total|sum|payment|rent|deposit|fee|cost|price)\s*:?\s*\$?[\d,]+\.?\d*\b'
            ]
            
            for pattern in money_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                analysis["monetary_amounts"].extend(matches)
            
            # Identify legal terms and concepts
            legal_terms = [
                'agreement', 'contract', 'lease', 'notice', 'complaint', 'petition',
                'warrant', 'injunction', 'damages', 'liability', 'indemnification',
                'breach', 'termination', 'renewal', 'assignment', 'subletting',
                'security deposit', 'rent', 'utilities', 'maintenance', 'repair',
                'eviction', 'possession', 'quiet enjoyment', 'habitability'
            ]
            
            for term in legal_terms:
                if term in text_lower:
                    analysis["legal_terms"].append(term)
            
            # Analyze document type based on content
            if 'eviction' in text_lower or 'notice to quit' in text_lower:
                analysis["document_type"] = "eviction_notice"
                analysis["confidence"] = 0.9
            elif 'lease' in text_lower or 'rental agreement' in text_lower:
                analysis["document_type"] = "lease_agreement"
                analysis["confidence"] = 0.9
            elif 'complaint' in text_lower or 'plaintiff' in text_lower:
                analysis["document_type"] = "legal_complaint"
                analysis["confidence"] = 0.9
            elif 'contract' in text_lower or 'agreement' in text_lower:
                analysis["document_type"] = "contract"
                analysis["confidence"] = 0.8
            
            # Generate potential issues and recommendations
            analysis["potential_issues"] = SimpleAIService._identify_potential_issues(text, analysis["document_type"])
            analysis["recommendations"] = SimpleAIService._generate_recommendations(text, analysis["document_type"])
            
            # Generate client-friendly summary
            analysis["client_summary"] = SimpleAIService._generate_client_summary(analysis, text)
            
            # Generate action items
            analysis["action_items"] = SimpleAIService._generate_action_items(analysis)
            
            # Determine risk level
            analysis["risk_level"] = SimpleAIService._assess_risk_level(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in _analyze_extracted_text: {str(e)}")
            return {
                "document_type": document_type,
                "confidence": 0.0,
                "error": str(e)
            }
    
    @staticmethod
    def _identify_potential_issues(text, doc_type):
        """Identify potential legal issues in the document"""
        issues = []
        text_lower = text.lower()
        
        # Check for concerning clauses
        concerning_patterns = [
            (r'waive.*right.*jury.*trial', 'Waiver of jury trial rights may be unenforceable'),
            (r'enter.*without.*notice', 'Entry without notice may violate privacy rights'),
            (r'automatic.*renewal', 'Automatic renewal clauses can be problematic'),
            (r'penalty.*late.*payment', 'Late payment penalties should be reasonable'),
            (r'one.sided.*indemnification', 'One-sided indemnification may be unenforceable')
        ]
        
        for pattern, issue in concerning_patterns:
            if re.search(pattern, text_lower):
                issues.append(issue)
        
        return issues
    
    @staticmethod
    def _generate_recommendations(text, doc_type):
        """Generate recommendations based on document analysis"""
        recommendations = []
        
        if doc_type == "eviction_notice":
            recommendations.extend([
                "Verify the notice period complies with local law",
                "Check if the grounds for eviction are valid",
                "Consider consulting with a tenant rights organization"
            ])
        elif doc_type == "lease_agreement":
            recommendations.extend([
                "Review all terms carefully before signing",
                "Ensure security deposit terms comply with local laws",
                "Consider having the document reviewed by an attorney"
            ])
        else:
            recommendations.extend([
                "Have this document reviewed by an attorney",
                "Request clarification on any terms you don't understand",
                "Ensure all parties understand their obligations"
            ])
        
        return recommendations
    
    @staticmethod
    def _answer_question_from_text(text, question):
        """Answer a specific question based on the extracted text"""
        # Simple keyword-based answering
        text_lower = text.lower()
        question_lower = question.lower()
        
        if 'deadline' in question_lower or 'due date' in question_lower:
            # Look for dates in the text
            dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
            if dates:
                return f"Based on the document, relevant dates found: {', '.join(dates[:3])}"
        
        if 'notarization' in question_lower or 'notary' in question_lower:
            if 'notar' in text_lower:
                return "Yes, this document appears to require notarization."
            else:
                return "The document doesn't clearly mention notarization requirements."
        
        if 'penalty' in question_lower or 'late payment' in question_lower:
            if 'penalty' in text_lower or 'late' in text_lower:
                return "The document contains penalty provisions. Please review the specific terms."
            else:
                return "No specific penalty terms were found in the document."
        
        return "The document doesn't clearly address this question. Please review the full text for relevant information."
    
    @staticmethod
    def _generate_client_summary(analysis, text):
        """Generate a clear, plain-language summary for clients"""
        doc_type = analysis.get("document_type", "document")
        parties = analysis.get("parties", [])
        monetary_amounts = analysis.get("monetary_amounts", [])
        key_dates = analysis.get("key_dates", [])
        
        summary_parts = []
        
        # Document type explanation
        if doc_type == "lease_agreement":
            summary_parts.append("This is a lease agreement - a contract between a landlord and tenant for renting property.")
        elif doc_type == "eviction_notice":
            summary_parts.append("This is an eviction notice - a legal document that tells a tenant they must leave the property.")
        elif doc_type == "legal_complaint":
            summary_parts.append("This is a legal complaint - a document that starts a lawsuit.")
        else:
            summary_parts.append(f"This appears to be a {doc_type.replace('_', ' ')} - a legal document.")
        
        # Parties involved
        if parties:
            if len(parties) == 1:
                summary_parts.append(f"The main party involved is: {parties[0]}")
            elif len(parties) == 2:
                summary_parts.append(f"The parties involved are: {parties[0]} and {parties[1]}")
            else:
                summary_parts.append(f"The parties involved include: {', '.join(parties[:3])}{' and others' if len(parties) > 3 else ''}")
        
        # Key financial information
        if monetary_amounts:
            amounts = [amt for amt in monetary_amounts if '$' in amt][:3]
            if amounts:
                summary_parts.append(f"Key financial amounts mentioned: {', '.join(amounts)}")
        
        # Important dates
        if key_dates:
            summary_parts.append(f"Important dates: {', '.join(key_dates[:3])}")
        
        # Risk assessment - more empowering
        risk_level = analysis.get("risk_level", "medium")
        if risk_level == "high":
            summary_parts.append("⚠️ This document has some concerning elements, but now you know what to watch out for and can protect yourself.")
        elif risk_level == "low":
            summary_parts.append("✅ This document appears to have standard terms - you're in good shape!")
        else:
            summary_parts.append("⚠️ This document has some areas to review, but you now have the knowledge to handle them.")
        
        return " ".join(summary_parts)
    
    @staticmethod
    def _generate_action_items(analysis):
        """Generate specific action items for the client"""
        action_items = []
        doc_type = analysis.get("document_type", "")
        potential_issues = analysis.get("potential_issues", [])
        monetary_amounts = analysis.get("monetary_amounts", [])
        
        # Document-specific actions - more empowering
        if doc_type == "lease_agreement":
            action_items.extend([
                "You now understand the rent and deposit terms - negotiate if needed",
                "Check if the lease term works for you - you can request changes",
                "Verify utility responsibilities - this affects your monthly costs",
                "Look for any unusual clauses - you have the right to question them"
            ])
        elif doc_type == "eviction_notice":
            action_items.extend([
                "Check if the notice period meets your state's legal requirements",
                "Verify the eviction grounds - you may have defenses",
                "Contact tenant rights organizations for free help and support",
                "Document everything - you're building your case"
            ])
        
        # Issue-specific actions
        if potential_issues:
            action_items.append("Address the potential issues identified in the analysis")
        
        # Financial actions
        if monetary_amounts:
            action_items.append("Verify all financial amounts and payment terms")
        
        # General actions - more DIY focused
        action_items.extend([
            "Review our analysis carefully - you now understand the key terms",
            "Use our recommendations to negotiate better terms if needed",
            "Keep a copy of this document and our analysis for your records"
        ])
        
        return action_items[:6]  # Limit to 6 most important items
    
    @staticmethod
    def _assess_risk_level(analysis):
        """Assess the overall risk level of the document"""
        potential_issues = analysis.get("potential_issues", [])
        legal_terms = analysis.get("legal_terms", [])
        
        risk_score = 0
        
        # High-risk terms
        high_risk_terms = ['waiver', 'penalty', 'forfeit', 'automatic', 'binding']
        for term in high_risk_terms:
            if any(term in legal_term.lower() for legal_term in legal_terms):
                risk_score += 2
        
        # Potential issues
        risk_score += len(potential_issues) * 2
        
        # Document type risk
        doc_type = analysis.get("document_type", "")
        if doc_type == "eviction_notice":
            risk_score += 3
        elif doc_type == "legal_complaint":
            risk_score += 2
        
        if risk_score >= 5:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"

    @staticmethod
    def generate_pdf_document(document_type, content, title="Generated Document", parties=None, additional_info=None):
        """
        Generate a PDF document based on user input
        
        Args:
            document_type (str): The type of document to generate
            content (dict): The content data for the document
            title (str): The title of the document
            parties (list): List of parties involved
            additional_info (dict): Additional information
            
        Returns:
            str: Base64 encoded PDF data
        """
        try:
            if not PDF_AVAILABLE:
                logger.error("ReportLab not available for PDF generation")
                return None
            
            # Create a buffer to hold the PDF
            buffer = io.BytesIO()
            
            # Create the PDF document
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # Document type specific content
            if document_type == 'lease_agreement':
                story.extend(SimpleAIService._generate_lease_content(content, parties, styles))
            elif document_type == 'service_contract':
                story.extend(SimpleAIService._generate_service_contract_content(content, parties, styles))
            elif document_type == 'nda':
                story.extend(SimpleAIService._generate_nda_content(content, parties, styles))
            elif document_type == 'employment_contract':
                story.extend(SimpleAIService._generate_employment_contract_content(content, parties, styles))
            else:
                # Generic document
                story.extend(SimpleAIService._generate_generic_content(content, styles))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF data
            pdf_data = buffer.getvalue()
            buffer.close()
            
            # Encode as base64 for transmission
            return base64.b64encode(pdf_data).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error generating PDF document: {str(e)}")
            return None
    
    @staticmethod
    def _generate_lease_content(content, parties, styles):
        """Generate lease agreement content"""
        story = []
        
        # Parties section
        story.append(Paragraph("<b>RESIDENTIAL LEASE AGREEMENT</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        if parties and len(parties) >= 2:
            story.append(Paragraph(f"<b>Landlord:</b> {parties[0]}", styles['Normal']))
            story.append(Paragraph(f"<b>Tenant:</b> {parties[1]}", styles['Normal']))
        else:
            story.append(Paragraph(f"<b>Landlord:</b> {content.get('landlord_name', '_________________')}", styles['Normal']))
            story.append(Paragraph(f"<b>Tenant:</b> {content.get('tenant_name', '_________________')}", styles['Normal']))
        
        story.append(Spacer(1, 12))
        
        # Property details
        story.append(Paragraph(f"<b>Property Address:</b> {content.get('property_address', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Lease Term:</b> {content.get('lease_term', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Monthly Rent:</b> ${content.get('rent_amount', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Security Deposit:</b> ${content.get('security_deposit', '_________________')}", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Terms and conditions
        story.append(Paragraph("<b>TERMS AND CONDITIONS:</b>", styles['Heading3']))
        story.append(Paragraph("1. The tenant agrees to pay rent on the 1st of each month.", styles['Normal']))
        story.append(Paragraph("2. The landlord may enter the property with 24 hours notice.", styles['Normal']))
        story.append(Paragraph("3. No pets allowed without written permission.", styles['Normal']))
        story.append(Paragraph("4. This agreement is governed by the laws of the state where the property is located.", styles['Normal']))
        
        return story
    
    @staticmethod
    def _generate_service_contract_content(content, parties, styles):
        """Generate service contract content"""
        story = []
        
        story.append(Paragraph("<b>SERVICE AGREEMENT</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        if parties and len(parties) >= 2:
            story.append(Paragraph(f"<b>Service Provider:</b> {parties[0]}", styles['Normal']))
            story.append(Paragraph(f"<b>Client:</b> {parties[1]}", styles['Normal']))
        else:
            story.append(Paragraph(f"<b>Service Provider:</b> {content.get('service_provider', '_________________')}", styles['Normal']))
            story.append(Paragraph(f"<b>Client:</b> {content.get('client_name', '_________________')}", styles['Normal']))
        
        story.append(Spacer(1, 12))
        
        story.append(Paragraph(f"<b>Service Description:</b> {content.get('service_description', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Payment Terms:</b> {content.get('payment_terms', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Duration:</b> {content.get('duration', '_________________')}", styles['Normal']))
        
        return story
    
    @staticmethod
    def _generate_nda_content(content, parties, styles):
        """Generate NDA content"""
        story = []
        
        story.append(Paragraph("<b>NON-DISCLOSURE AGREEMENT</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        if parties and len(parties) >= 2:
            story.append(Paragraph(f"<b>Disclosing Party:</b> {parties[0]}", styles['Normal']))
            story.append(Paragraph(f"<b>Receiving Party:</b> {parties[1]}", styles['Normal']))
        else:
            story.append(Paragraph(f"<b>Disclosing Party:</b> {content.get('disclosing_party', '_________________')}", styles['Normal']))
            story.append(Paragraph(f"<b>Receiving Party:</b> {content.get('receiving_party', '_________________')}", styles['Normal']))
        
        story.append(Spacer(1, 12))
        
        story.append(Paragraph(f"<b>Confidential Information:</b> {content.get('confidential_info', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Duration:</b> {content.get('duration', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Purpose:</b> {content.get('purpose', '_________________')}", styles['Normal']))
        
        return story
    
    @staticmethod
    def _generate_employment_contract_content(content, parties, styles):
        """Generate employment contract content"""
        story = []
        
        story.append(Paragraph("<b>EMPLOYMENT CONTRACT</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        if parties and len(parties) >= 2:
            story.append(Paragraph(f"<b>Employer:</b> {parties[0]}", styles['Normal']))
            story.append(Paragraph(f"<b>Employee:</b> {parties[1]}", styles['Normal']))
        else:
            story.append(Paragraph(f"<b>Employer:</b> {content.get('employer', '_________________')}", styles['Normal']))
            story.append(Paragraph(f"<b>Employee:</b> {content.get('employee_name', '_________________')}", styles['Normal']))
        
        story.append(Spacer(1, 12))
        
        story.append(Paragraph(f"<b>Position:</b> {content.get('position', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Salary:</b> ${content.get('salary', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Start Date:</b> {content.get('start_date', '_________________')}", styles['Normal']))
        story.append(Paragraph(f"<b>Benefits:</b> {content.get('benefits', '_________________')}", styles['Normal']))
        
        return story
    
    @staticmethod
    def _generate_generic_content(content, styles):
        """Generate generic document content"""
        story = []
        
        for key, value in content.items():
            story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", styles['Normal']))
            story.append(Spacer(1, 6))
        
        return story

    @staticmethod
    def needs_escalation(text: str) -> bool:
        """
        Check if text contains unauthorized legal advice or needs escalation
        """
        if not text:
            return True
        
        text_lower = text.lower()
        
        # Check for unauthorized legal advice patterns
        for pattern in ADVICE_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        
        # Check for uncertainty patterns (good to escalate)
        for pattern in UNCERTAINTY_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        
        # Check for specific legal action words
        legal_action_words = [
            'sue', 'lawsuit', 'litigation', 'file', 'plead', 'defend',
            'prosecute', 'charge', 'arrest', 'convict', 'sentence'
        ]
        
        if any(word in text_lower for word in legal_action_words):
            return True
        
        return False

    @staticmethod
    def sanitize_response(text: str) -> str:
        """
        Sanitize response to remove potentially problematic language
        """
        if not text:
            return text
        
        # Replace problematic phrases
        replacements = {
            'i advise': 'i suggest',
            'you should': 'you might consider',
            'you must': 'you may need to',
            'this is legal advice': 'this is general information',
        }
        
        sanitized = text
        for old, new in replacements.items():
            sanitized = sanitized.replace(old, new)
        
        return sanitized

    @staticmethod
    def add_disclaimer(text: str) -> str:
        """
        Add legal disclaimer to response
        """
        disclaimer = "\n\n⚠️ **Important**: This is general legal information, not legal advice. For specific legal matters, please consult with a qualified attorney."
        
        if "disclaimer" not in text.lower() and "not legal advice" not in text.lower():
            return text + disclaimer
        
        return text

    @staticmethod
    def analyze_with_safety(text: str, document_type: str = "generic") -> dict:
        """
        Analyze text with safety checks and compliance features
        """
        # Basic analysis
        analysis = SimpleAIService._analyze_extracted_text(text, document_type)
        
        # Add safety features
        client_summary = analysis.get("client_summary", "")
        recommendations = analysis.get("recommendations", [])
        
        # Check if escalation is needed
        needs_escalation = SimpleAIService.needs_escalation(client_summary)
        
        # Sanitize response
        if client_summary:
            analysis["client_summary"] = SimpleAIService.sanitize_response(client_summary)
        
        # Add disclaimer if needed
        if needs_escalation:
            analysis["client_summary"] = SimpleAIService.add_disclaimer(analysis["client_summary"])
            analysis["escalation_needed"] = True
        else:
            analysis["escalation_needed"] = False
        
        # Add safety recommendations
        if needs_escalation:
            analysis["recommendations"].append("Consider consulting with a qualified attorney for specific legal advice")
            analysis["recommendations"].append("This analysis is for informational purposes only")
        
        return analysis

# Convenience functions
def analyze_document(document_path, document_type="generic", questions=None):
    return SimpleAIService.analyze_document(document_path, document_type, questions)

def extract_text_from_document(document_path):
    return SimpleAIService.extract_text_from_document(document_path)

def generate_pdf_document(document_type, content, title="Generated Document", parties=None, additional_info=None):
    return SimpleAIService.generate_pdf_document(document_type, content, title, parties, additional_info)

def analyze_with_safety(text: str, document_type: str = "generic") -> dict:
    return SimpleAIService.analyze_with_safety(text, document_type)

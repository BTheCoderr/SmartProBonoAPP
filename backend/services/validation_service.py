"""
Validation service for form inputs and document data.
"""
import re
import json
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from flask import request, jsonify

class ValidationService:
    """Service for validating input data across the application."""
    
    def __init__(self):
        """Initialize validation service with common validators."""
        # Common validation patterns
        self.patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[0-9]{10,15}$',
            'zip_code': r'^\d{5}(-\d{4})?$',
            'date': r'^\d{4}-\d{2}-\d{2}$',
            'url': r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',
            'alphanumeric': r'^[a-zA-Z0-9]+$',
            'numeric': r'^\d+$',
            'alphabetic': r'^[a-zA-Z]+$',
            'ssn': r'^\d{3}-\d{2}-\d{4}$',
            'ein': r'^\d{2}-\d{7}$'
        }
        
        # Document type specific validators
        self.document_validators = {
            'contract': self.validate_contract,
            'court_filing': self.validate_court_filing,
            'immigration_form': self.validate_immigration_form,
            'small_claims': self.validate_small_claims,
            'legal_letter': self.validate_legal_letter
        }
    
    def validate_document(self, document_type: str, document_data: Dict[str, Any]) -> Tuple[bool, Optional[List[str]]]:
        """
        Validate a document based on its type.
        
        Args:
            document_type: The type of document to validate
            document_data: The document data to validate
            
        Returns:
            Tuple[bool, Optional[List[str]]]: (is_valid, error_messages)
        """
        if document_type not in self.document_validators:
            return False, ["Unknown document type"]
            
        return self.document_validators[document_type](document_data)
    
    def validate_contract(self, data: Dict[str, Any]) -> Tuple[bool, Optional[List[str]]]:
        """Validate contract document data."""
        required_fields = ['title', 'parties', 'effective_date', 'terms']
        errors = self._check_required_fields(data, required_fields)
        
        if 'parties' in data and isinstance(data['parties'], list):
            for i, party in enumerate(data['parties']):
                if not isinstance(party, dict) or 'name' not in party:
                    errors.append(f"Party {i+1} must include a name")
        
        if 'effective_date' in data:
            if not self._is_valid_date(data['effective_date']):
                errors.append("Effective date must be a valid date in YYYY-MM-DD format")
        
        return len(errors) == 0, errors if errors else None
    
    def validate_court_filing(self, data: Dict[str, Any]) -> Tuple[bool, Optional[List[str]]]:
        """Validate court filing document data."""
        required_fields = ['case_number', 'court_name', 'filing_type', 'parties', 'filing_date']
        errors = self._check_required_fields(data, required_fields)
        
        if 'case_number' in data and not self._is_valid_pattern(data['case_number'], r'^[A-Za-z0-9-]+$'):
            errors.append("Case number must be alphanumeric")
            
        if 'filing_date' in data and not self._is_valid_date(data['filing_date']):
            errors.append("Filing date must be a valid date in YYYY-MM-DD format")
        
        return len(errors) == 0, errors if errors else None
    
    def validate_immigration_form(self, data: Dict[str, Any]) -> Tuple[bool, Optional[List[str]]]:
        """Validate immigration form data."""
        required_fields = ['form_type', 'applicant_name', 'applicant_dob', 'country_of_birth']
        errors = self._check_required_fields(data, required_fields)
        
        if 'applicant_dob' in data and not self._is_valid_date(data['applicant_dob']):
            errors.append("Date of birth must be a valid date in YYYY-MM-DD format")
            
        if 'alien_number' in data and not self._is_valid_pattern(data['alien_number'], r'^A\d{8,9}$'):
            errors.append("Alien number must be in format A followed by 8 or 9 digits")
        
        return len(errors) == 0, errors if errors else None
    
    def validate_small_claims(self, data: Dict[str, Any]) -> Tuple[bool, Optional[List[str]]]:
        """Validate small claims form data."""
        required_fields = ['plaintiff_name', 'defendant_name', 'claim_amount', 'claim_reason']
        errors = self._check_required_fields(data, required_fields)
        
        if 'claim_amount' in data:
            try:
                amount = float(data['claim_amount'])
                if amount <= 0:
                    errors.append("Claim amount must be greater than zero")
            except (ValueError, TypeError):
                errors.append("Claim amount must be a valid number")
        
        return len(errors) == 0, errors if errors else None
    
    def validate_legal_letter(self, data: Dict[str, Any]) -> Tuple[bool, Optional[List[str]]]:
        """Validate legal letter data."""
        required_fields = ['sender', 'recipient', 'letter_date', 'subject', 'body']
        errors = self._check_required_fields(data, required_fields)
        
        if 'letter_date' in data and not self._is_valid_date(data['letter_date']):
            errors.append("Letter date must be a valid date in YYYY-MM-DD format")
        
        return len(errors) == 0, errors if errors else None
    
    def _check_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """Check if all required fields are present and not empty."""
        errors = []
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"{field.replace('_', ' ').title()} is required")
        return errors
    
    def _is_valid_pattern(self, value: str, pattern: str) -> bool:
        """Check if a value matches a regex pattern."""
        if not isinstance(value, str):
            return False
        return bool(re.match(pattern, value))
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Check if a string is a valid date in YYYY-MM-DD format."""
        if not isinstance(date_str, str):
            return False
            
        if not re.match(self.patterns['date'], date_str):
            return False
            
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def validate_email(self, email: str) -> bool:
        """Validate an email address."""
        return self._is_valid_pattern(email, self.patterns['email'])
    
    def validate_phone(self, phone: str) -> bool:
        """Validate a phone number."""
        return self._is_valid_pattern(phone, self.patterns['phone'])
    
    def validate_input(self, 
                      data: Dict[str, Any], 
                      schema: Dict[str, Dict[str, Any]]) -> Tuple[bool, Optional[Dict[str, List[str]]]]:
        """
        Validate input data against a schema.
        
        Args:
            data: The data to validate
            schema: The validation schema
            
        Returns:
            Tuple[bool, Optional[Dict[str, List[str]]]]: (is_valid, field_errors)
        """
        errors = {}
        
        for field, field_schema in schema.items():
            field_errors = []
            
            # Check required fields
            if field_schema.get('required', False) and (field not in data or data[field] is None or data[field] == ''):
                field_errors.append("This field is required")
                errors[field] = field_errors
                continue
                
            # Skip if field is not in data and not required
            if field not in data:
                continue
                
            value = data[field]
            
            # Check type
            expected_type = field_schema.get('type')
            if expected_type and not self._check_type(value, expected_type):
                field_errors.append(f"Must be a {expected_type.__name__}")
            
            # Check pattern
            pattern = field_schema.get('pattern')
            if pattern and isinstance(value, str) and not self._is_valid_pattern(value, pattern):
                field_errors.append(field_schema.get('error', "Invalid format"))
            
            # Check min/max for strings
            if isinstance(value, str):
                min_length = field_schema.get('minLength')
                if min_length is not None and len(value) < min_length:
                    field_errors.append(f"Must be at least {min_length} characters")
                    
                max_length = field_schema.get('maxLength')
                if max_length is not None and len(value) > max_length:
                    field_errors.append(f"Must be at most {max_length} characters")
            
            # Check min/max for numbers
            if isinstance(value, (int, float)):
                minimum = field_schema.get('minimum')
                if minimum is not None and value < minimum:
                    field_errors.append(f"Must be at least {minimum}")
                    
                maximum = field_schema.get('maximum')
                if maximum is not None and value > maximum:
                    field_errors.append(f"Must be at most {maximum}")
            
            # Check enum values
            enum_values = field_schema.get('enum')
            if enum_values is not None and value not in enum_values:
                field_errors.append(f"Must be one of: {', '.join(str(v) for v in enum_values)}")
            
            # Custom validator
            validator = field_schema.get('validator')
            if validator and callable(validator):
                try:
                    result = validator(value)
                    if result is not True:
                        field_errors.append(result if isinstance(result, str) else "Invalid value")
                except Exception as e:
                    field_errors.append(str(e))
            
            if field_errors:
                errors[field] = field_errors
        
        return len(errors) == 0, errors if errors else None
    
    def _check_type(self, value: Any, expected_type: Union[type, str]) -> bool:
        """Check if a value is of the expected type."""
        if expected_type == 'array':
            return isinstance(value, list)
        elif expected_type == 'object':
            return isinstance(value, dict)
        elif expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'number':
            return isinstance(value, (int, float))
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'null':
            return value is None
        else:
            return isinstance(value, expected_type)

# Create a singleton instance
validation_service = ValidationService() 
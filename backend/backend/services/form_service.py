from marshmallow import Schema, fields, validate, ValidationError

# Form validation schemas
class SmallClaimsSchema(Schema):
    court_county = fields.Str(required=True)
    court_state = fields.Str(required=True)
    plaintiff_name = fields.Str(required=True)
    plaintiff_address = fields.Str(required=True)
    defendant_name = fields.Str(required=True)
    defendant_address = fields.Str(required=True)
    claim_amount = fields.Float(required=True, validate=validate.Range(min=0, max=10000))
    claim_description = fields.Str(required=True, validate=validate.Length(min=20))
    case_number = fields.Str(allow_none=True)
    incident_location = fields.Str(allow_none=True)
    incident_date = fields.Date(required=True)
    filing_date = fields.Date(required=True)
    filing_fee = fields.Float(allow_none=True, validate=validate.Range(min=0))
    fact_1 = fields.Str(required=True)
    fact_2 = fields.Str(allow_none=True)
    fact_3 = fields.Str(allow_none=True)
    evidence_list = fields.Str(allow_none=True)
    witness_list = fields.Str(allow_none=True)

class EvictionResponseSchema(Schema):
    case_number = fields.Str(required=True)
    tenant_name = fields.Str(required=True)
    tenant_address = fields.Str(required=True)
    landlord_name = fields.Str(required=True)
    landlord_address = fields.Str(required=True)
    property_address = fields.Str(required=True)
    response_date = fields.Date(required=True)
    defense_explanation = fields.Str(required=True, validate=validate.Length(min=50))
    rent_details = fields.Str(allow_none=True)
    maintenance_issues = fields.Str(allow_none=True)
    additional_facts = fields.Str(allow_none=True)

class FeeWaiverSchema(Schema):
    applicant_name = fields.Str(required=True)
    case_number = fields.Str(allow_none=True)
    court_name = fields.Str(required=True)
    filing_date = fields.Date(required=True)
    monthly_income = fields.Float(required=True, validate=validate.Range(min=0))
    household_size = fields.Int(required=True, validate=validate.Range(min=1))
    public_benefits = fields.List(fields.Str(), allow_none=True)
    expenses = fields.Dict(keys=fields.Str(), values=fields.Float(), allow_none=True)
    hardship_explanation = fields.Str(allow_none=True)

# Map form types to their schemas
FORM_SCHEMAS = {
    'small_claims': SmallClaimsSchema,
    'eviction_response': EvictionResponseSchema,
    'fee_waiver': FeeWaiverSchema
}

def validate_form_data(form_type, data):
    """
    Validate form data against its schema.
    
    Args:
        form_type (str): Type of form to validate
        data (dict): Form data to validate
    
    Returns:
        dict: Dictionary of validation errors, or None if validation passes
    """
    schema_class = FORM_SCHEMAS.get(form_type)
    if not schema_class:
        return {'error': f'Unknown form type: {form_type}'}
    
    try:
        schema = schema_class()
        schema.load(data)
        return None
    except ValidationError as err:
        return err.messages

def get_form_schema(form_type):
    """Get the schema for a form type."""
    return FORM_SCHEMAS.get(form_type) 
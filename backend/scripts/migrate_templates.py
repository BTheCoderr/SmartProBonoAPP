"""Script to migrate existing templates to the database"""
from backend.extensions import db
from backend.models.template import Template

# Initial templates data
INITIAL_TEMPLATES = {
    'g28': {
        'template_id': 'g28',
        'name': 'Form G-28',
        'title': 'Notice of Entry of Appearance as Attorney',
        'fields': ['attorney_name', 'client_name', 'date']
    },
    'i589': {
        'template_id': 'i589',
        'name': 'Form I-589',
        'title': 'Application for Asylum',
        'fields': ['applicant_name', 'nationality', 'entry_date']
    },
    'cover_letter': {
        'template_id': 'cover_letter',
        'name': 'Cover Letter',
        'title': 'Immigration Application Cover Letter',
        'fields': ['recipient', 'applicant_name', 'application_type', 'date']
    }
}

def migrate_templates():
    """Migrate templates to database"""
    print("Starting template migration...")
    
    for template_data in INITIAL_TEMPLATES.values():
        existing = Template.query.filter_by(template_id=template_data['template_id']).first()
        if not existing:
            template = Template.from_dict(template_data)
            db.session.add(template)
            print(f"Added template: {template_data['name']}")
    
    try:
        db.session.commit()
        print("Template migration completed successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error during migration: {str(e)}")
        raise

if __name__ == '__main__':
    from backend.app import create_app
    app = create_app()
    with app.app_context():
        migrate_templates() 
from models.database import db
from models.user import User
from models.case import Case
from models.document import Document
from models.attorney_request import AttorneyRequest
from datetime import datetime, timedelta
import json

def seed_demo_data():
    # Create demo users
    demo_attorneys = [
        User(
            email="sarah.martinez@smartprobono.org",
            password="demo123",
            role="attorney",
            first_name="Sarah",
            last_name="Martinez",
            practice_areas="Immigration,Family Law",
            years_of_experience=8,
            languages="English,Spanish",
            state="CA",
            availability=json.dumps([
                {"day": "Monday", "hours": ["9:00", "10:00", "11:00", "14:00", "15:00"]},
                {"day": "Wednesday", "hours": ["13:00", "14:00", "15:00", "16:00"]},
                {"day": "Friday", "hours": ["9:00", "10:00", "11:00"]}
            ]),
            is_verified=True
        ),
        User(
            email="david.kim@smartprobono.org",
            password="demo123",
            role="attorney",
            first_name="David",
            last_name="Kim",
            practice_areas="Criminal Law,Civil Rights",
            years_of_experience=12,
            languages="English,Korean",
            state="NY",
            availability=json.dumps([
                {"day": "Tuesday", "hours": ["10:00", "11:00", "14:00", "15:00"]},
                {"day": "Thursday", "hours": ["9:00", "10:00", "11:00", "13:00", "14:00"]}
            ]),
            is_verified=True
        ),
        User(
            email="maria.rodriguez@smartprobono.org",
            password="demo123",
            role="attorney",
            first_name="Maria",
            last_name="Rodriguez",
            practice_areas="Immigration,Employment Law",
            years_of_experience=5,
            languages="English,Spanish,Portuguese",
            state="FL",
            availability=json.dumps([
                {"day": "Monday", "hours": ["13:00", "14:00", "15:00"]},
                {"day": "Wednesday", "hours": ["9:00", "10:00", "11:00"]},
                {"day": "Friday", "hours": ["14:00", "15:00", "16:00"]}
            ]),
            is_verified=True
        )
    ]
    
    demo_clients = [
        User(
            email="john.smith@example.com",
            password="demo123",
            role="client",
            first_name="John",
            last_name="Smith",
            languages="English",
            state="CA",
            legal_issue_type="Immigration",
            case_description="Need assistance with visa application"
        ),
        User(
            email="alice.wong@example.com",
            password="demo123",
            role="client",
            first_name="Alice",
            last_name="Wong",
            languages="English,Korean",
            state="NY",
            legal_issue_type="Civil Rights",
            case_description="Workplace discrimination case"
        ),
        User(
            email="carlos.garcia@example.com",
            password="demo123",
            role="client",
            first_name="Carlos",
            last_name="Garcia",
            languages="Spanish",
            state="FL",
            legal_issue_type="Employment Law",
            case_description="Wrongful termination dispute"
        )
    ]
    
    db.session.add_all(demo_attorneys + demo_clients)
    db.session.commit()

    # Create sample cases
    cases = [
        Case(
            title="Immigration Asylum Application",
            description="Assistance needed with asylum application and documentation.",
            case_type="IMMIGRATION",
            status="IN_PROGRESS",
            priority="HIGH",
            client_id=demo_clients[0].id,
            lawyer_id=demo_attorneys[0].id,
            created=datetime.utcnow() - timedelta(days=5),
            updated=datetime.utcnow() - timedelta(hours=2)
        ),
        Case(
            title="Workplace Discrimination Case",
            description="Support required for discrimination case.",
            case_type="CIVIL_RIGHTS",
            status="NEW",
            priority="URGENT",
            client_id=demo_clients[1].id,
            lawyer_id=demo_attorneys[1].id,
            created=datetime.utcnow() - timedelta(days=2)
        ),
        Case(
            title="Employment Dispute",
            description="Wrongful termination case.",
            case_type="EMPLOYMENT",
            status="NEW",
            priority="HIGH",
            client_id=demo_clients[2].id,
            created=datetime.utcnow() - timedelta(days=1)
        )
    ]
    
    db.session.add_all(cases)
    db.session.commit()

    # Add sample documents
    documents = [
        Document(
            title="Asylum Application Form",
            description="Completed I-589 form for asylum application",
            document_type="LEGAL_FORM",
            status="IN_REVIEW",
            case_id=cases[0].id,
            created_by=demo_attorneys[0].id,
            created=datetime.utcnow() - timedelta(days=3)
        ),
        Document(
            title="Evidence Documentation",
            description="Collection of evidence for discrimination case",
            document_type="EVIDENCE",
            status="DRAFT",
            case_id=cases[1].id,
            created_by=demo_clients[1].id,
            created=datetime.utcnow() - timedelta(days=1)
        )
    ]
    
    db.session.add_all(documents)
    db.session.commit()

    # Add sample attorney requests
    requests = [
        AttorneyRequest(
            client_id=demo_clients[2].id,
            attorney_id=demo_attorneys[2].id,
            status="pending",
            message="Need help with employment law case",
            legal_issue_type="Employment Law",
            case_description="Wrongful termination dispute, seeking legal representation",
            created_at=datetime.utcnow() - timedelta(hours=12)
        ),
        AttorneyRequest(
            client_id=demo_clients[0].id,
            attorney_id=demo_attorneys[0].id,
            status="accepted",
            message="Immigration case assistance needed",
            legal_issue_type="Immigration",
            case_description="Need help with visa application process",
            created_at=datetime.utcnow() - timedelta(days=6)
        )
    ]
    
    db.session.add_all(requests)
    db.session.commit()

if __name__ == "__main__":
    seed_demo_data() 
# SmartProBono

SmartProBono is a comprehensive legal assistance platform designed to connect clients in need with volunteer attorneys and provide essential legal resources. The platform facilitates case management, document generation, client-attorney communication, and more.

## Features

- **Legal Document Generation**: Create professional legal documents with templates for power of attorney, rental agreements, wills, and more.
- **Case Management**: Track cases, assign attorneys, manage documents, and monitor progress.
- **Legal AI Assistance**: Get preliminary legal advice and guidance through AI-powered chat.
- **Client-Attorney Matching**: Sophisticated system to pair clients with appropriate volunteer attorneys.
- **Safety Monitoring**: Enhanced safety features for clients in sensitive situations.
- **Priority Queue System**: Ensures urgent cases receive immediate attention.

## Document Templates

The platform includes a variety of professional legal document templates across multiple legal domains:

### Housing
- **Rental Agreement**: Standard residential lease agreement.
- **Eviction Defense Form**: Form for responding to an eviction notice and asserting tenant rights.
- **Eviction Appeal**: Document to appeal an eviction decision.

### Family Law
- **Child Custody Agreement**: Legal agreement establishing custody arrangements between parents.
- **Child Support Calculation**: Form to determine appropriate child support obligations.
- **Divorce Petition**: Initial document to file for divorce proceedings.
- **Child Custody Form**: Form to establish or modify child custody arrangements.

### Employment
- **Employment Contract**: Standard employment agreement template.
- **Discrimination Complaint**: Form for filing workplace discrimination complaints.
- **ADA Accommodation Request**: Document to request reasonable accommodations.
- **Civil Rights Assertion**: Form asserting civil rights in employment contexts.

### Immigration
- **Immigration Assistance Form**: For requesting immigration legal assistance.
- **DACA Renewal Application**: Form to prepare Deferred Action for Childhood Arrivals renewal.

### Business
- **LLC Formation**: Documents for forming a Limited Liability Company.
- **Non-Disclosure Agreement**: Confidentiality agreement for business relationships.

### Estate Planning
- **Last Will and Testament**: Create a legally-sound will to express your wishes.
- **Medical Power of Attorney**: Designate someone to make healthcare decisions if you're incapacitated.
- **General Power of Attorney**: For authorizing someone to act on your behalf.

### Other
- **Demand Letter**: For formal legal claims or disputes.
- **Small Claims**: Documents for filing in small claims court.

## Automated Testing

SmartProBono includes a comprehensive testing infrastructure:

- **Unit Tests**: Tests for individual components and functions.
- **Integration Tests**: Tests for API endpoints and service interactions.
- **End-to-End Tests**: Tests for complete user workflows from start to finish.

Tests can be run locally or through the CI/CD pipeline.

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js and npm
- PostgreSQL database
- Redis (for message queuing)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables (copy .env.example to .env and modify):
   ```
   cp .env.example .env
   ```

5. Initialize the database:
   ```
   python run.py --setup-db --migrate
   ```

6. Start the backend server:
   ```
   python run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

### Running Tests

1. Install test dependencies:
   ```
   pip install pytest pytest-cov pytest-asyncio
   ```

2. Run the tests:
   ```
   cd backend
   pytest
   ```

## Document Generation

The enhanced document generation system supports multiple document formats and templates. To use:

1. Navigate to the Document Generator section
2. Select a template category
3. Choose a specific document template
4. Fill in the required fields
5. Generate and download your completed document

## Contributing

We welcome contributions to SmartProBono! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

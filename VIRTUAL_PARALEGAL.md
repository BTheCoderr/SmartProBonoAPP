# Virtual Paralegal Assistant

The Virtual Paralegal Assistant is an AI-powered feature of Smart Pro Bono designed to help lawyers and legal aid organizations streamline their workflow, automate client intake, and manage cases more efficiently.

## Features

- **Client Intake Automation**: Multi-step forms for capturing client information efficiently
- **Document Automation**: Generate and customize legal documents from templates
- **Client Screening**: Pre-screen potential clients with customizable questionnaires
- **Self-Service Legal Resources**: Provide resources for clients you can't take on

## Use Cases

### Solo Practitioners
Solo attorneys can use the Virtual Paralegal Assistant to handle more client inquiries without hiring additional staff. The system automates routine administrative tasks, freeing up valuable time for billable work.

### Small Law Firms
Small firms can standardize their client intake process, ensuring consistent data collection across all attorneys. This reduces administrative costs and improves efficiency.

### Legal Aid Organizations
Legal aid organizations can serve more clients with limited resources by automating eligibility screening and providing self-service resources for cases they can't handle directly.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MongoDB (v4.4 or higher)

### Installation

1. Clone the SmartProBono repository:
```
git clone https://github.com/yourusername/SmartProBono.git
cd SmartProBono
```

2. Install frontend dependencies:
```
cd frontend
npm install
```

3. Install backend dependencies:
```
cd ../backend
pip install -r requirements.txt
```

4. Initialize the database collections:
```
python setup_paralegal_collections.py
```

5. Start the servers:
```
cd ..
./start_servers.sh
```

## API Endpoints

The Virtual Paralegal Assistant provides the following API endpoints:

### `GET /api/paralegal/`
Get documentation for all paralegal API routes.

### `POST /api/paralegal/case`
Create a new case with client information.
- Requires authentication
- Required fields: `clientName`, `clientEmail`, `caseType`

### `GET /api/paralegal/cases`
Get all cases for the current user.
- Requires authentication
- Optional query parameters: `status`, `case_type`

### `GET /api/paralegal/case/:caseId`
Get a specific case by ID.
- Requires authentication

### `PUT /api/paralegal/case/:caseId`
Update a specific case.
- Requires authentication

### `GET /api/paralegal/templates`
Get all document templates.
- Requires authentication
- Optional query parameter: `type`

### `GET /api/paralegal/screening-questions`
Get screening questions.
- Requires authentication
- Optional query parameter: `category`

### `POST /api/paralegal/generate-document/:templateId`
Generate a document from a template with case data.
- Requires authentication

## Testing

### Backend API Testing

You can test the API endpoints using the included test script:

```
cd backend
python test_paralegal_api.py
```

Note: For authenticated endpoints, you'll need to add a valid JWT token to the script.

### Frontend Testing

Navigate to the application in your browser at `http://localhost:3100/virtual-paralegal` to test the UI.

## Demo Mode

The Virtual Paralegal Assistant includes a demo mode that activates automatically when the backend is not available. This allows users to explore the features without a functioning backend connection.

## Implementation Details

### Frontend

The Virtual Paralegal Assistant is implemented in React with Material-UI components. The main component is `VirtualParalegalPage.js` which includes:

- Multi-step form for client intake
- Document template browsing and generation
- Screening question management
- Connection status indicator

### Backend

The backend is implemented in Flask and provides API endpoints for:

- Case management
- Document templates
- Screening questions
- Document generation

Data is stored in MongoDB collections for flexibility and scalability.

## Future Enhancements

- **AI-powered document analysis**: Add capability to analyze uploaded legal documents
- **Calendar integration**: Connect with calendar apps for scheduling consultations
- **Client portal**: Allow clients to track their case status and communicate securely
- **Advanced reporting**: Provide insights and analytics on case management
- **Mobile app**: Develop a companion mobile app for on-the-go case management

## Contributing

Contributions to improve the Virtual Paralegal Assistant are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The legal professionals who provided feedback on feature requirements
- The open-source community for the tools and libraries used in this project 
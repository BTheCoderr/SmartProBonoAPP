# SmartProBono MVP Routes

This document provides a list of the fully functional, demo-ready pages in the SmartProBono platform.

## Working MVP Pages

| Route | Description | Status |
|-------|-------------|--------|
| `/` | Home/Landing Page | ✅ Working |
| `/legal-chat` | AI Legal Assistant | ✅ Working |
| `/beta` | Beta Signup Page | ✅ Working |
| `/documents` | Document Management | ✅ Working |
| `/expert-help` | Pro Bono Attorney Connection | ✅ Working |
| `/about` | About the Platform | ✅ Working |
| `/login` | User Login | ✅ Working (Demo) |
| `/register` | User Registration | ✅ Working (Demo) |

## Demo Instructions

### 1. Legal Chat
- Navigate to `/legal-chat`
- Use the model selector to choose different AI models (Mistral, LlaMA, DeepSeek, etc.)
- Try some example legal questions:
  - "How do I respond to a court summons?"
  - "What steps should I take after a car accident?"
  - "How can I dispute a credit report error?"

### 2. Document Management
- Navigate to `/documents`
- Use the "Upload Document" button to add new documents
- View document history and download existing documents
- Try uploading the sample document created by `create_sample_pdf.py`

### 3. Expert Help
- Navigate to `/expert-help`
- Browse attorney profiles
- Use the search filters to find attorneys by specialty
- View attorney ratings and contact information

## Non-Working Pages (In Development)
The following pages have UI components but backend functionality is still in development:

- `/virtual-paralegal` - Virtual paralegal service
- `/immigration` - Immigration assistance tools
- `/forms-dashboard` - Legal forms dashboard
- `/admin` - Admin panel

## How to Run the MVP Demo
1. Start the backend server: `./run_with_email_alt.sh`
2. Start the frontend: `cd frontend && npm start`
3. Open your browser to `http://localhost:3000`
4. Follow the demo instructions above 
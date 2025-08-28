# SmartProBono Platform Testing Checklist

## Prerequisites
- Start backend server: `./run_with_email_alt.sh`
- Start frontend server: `cd frontend && npm start`

## Document Functionality Testing

### Backend Tests
- [ ] Run `python test_documents.py sample_document.pdf` to verify all document API endpoints
- [ ] Check server logs for successful document API responses

### Frontend Document Management
- [ ] Navigate to http://localhost:3000/documents
- [ ] Click "Upload Document" button
- [ ] Select a PDF file (use `sample_document.pdf` created by `create_sample_pdf.py`)
- [ ] Enter document title and select category
- [ ] Click "Upload Document" and verify success message
- [ ] Verify uploaded document appears in document list
- [ ] Open a document and verify content is displayed
- [ ] Try document comparison feature with two documents
- [ ] Try creating a document from template
- [ ] Delete a document and verify it's removed from the list

## Expert Help Page Testing
- [ ] Navigate to http://localhost:3000/expert-help
- [ ] Verify attorney profiles are displayed properly
- [ ] Test search functionality with legal topics
- [ ] Click on a topic chip and verify filtering works
- [ ] Switch between the tabs (Available Attorneys, How It Works, FAQ)
- [ ] Click on "Request Help" for an attorney and verify the UI feedback
- [ ] Click on "Talk to AI Assistant" button and verify navigation to /legal-chat

## Legal Chat Testing
- [ ] Navigate to http://localhost:3000/legal-chat
- [ ] Test sending a legal question (e.g., "What should I do if I receive a court summons?")
- [ ] Switch between different AI models using the model selector
- [ ] Verify responses are generated for each model
- [ ] Test feedback submission at the bottom of the chat
- [ ] Try different legal topics and verify appropriate responses

## Email Functionality Testing
- [ ] Test beta signup with email: bferrell514@gmail.com
- [ ] Verify confirmation email is received
- [ ] Verify admin notification is sent to info@smartprobono.org
- [ ] Check email formatting and content

## General UI/UX Testing
- [ ] Test responsive design by resizing browser window
- [ ] Verify navigation between pages works without errors
- [ ] Check for any console errors in browser developer tools

## Linting and Import Fixes
- [ ] Run `cd frontend && npm run lint` to verify linting errors are reduced
- [ ] Check if backend import errors are resolved

## Known Issues and Limitations
- TinyMCE editor requires API key (visible in template creation)
- Document generation from template is not fully implemented
- Some advanced document features like sharing and versioning are stubbed but not fully functional
- Authentication system is referenced but not fully implemented

Please report any additional issues or bugs you encounter while testing the platform. 
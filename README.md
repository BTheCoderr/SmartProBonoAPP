# SmartProBono

SmartProBono is a legal-tech platform designed to assist with pro bono legal services.

## AI-Powered Legal Assistance

SmartProBono leverages advanced AI models to provide intelligent legal assistance:

- **Legal Q&A**: Get answers to common legal questions using natural language
- **Document Analysis**: AI-powered analysis of legal documents and contracts
- **Document Generation**: Draft legal documents based on requirements and templates
- **Rights Research**: Research legal rights and requirements across different jurisdictions

## Document Management Features

The document management system within SmartProBono offers robust functionality for legal professionals:

### Core Features

- **Document Storage & Organization**: Upload, organize, and securely store legal documents
- **Template System**: Create and manage reusable document templates with variable placeholders
- **Document Generation**: Generate new documents from templates by filling in variables
- **Version Control**: Track document changes with full version history and revert capabilities

### Advanced Features

- **Document Sharing**: Share documents with specific users directly or via email
- **Document Tagging**: Categorize documents with custom tags for better organization
- **Document Comparison**: Side-by-side or unified comparison of documents with change highlighting
- **Collaborative Editing**: Real-time collaboration on document editing

### Security

- User-based permissions
- Secure document storage
- Access control and audit trails

## Immigration Services

SmartProBono provides comprehensive immigration assistance features:

- **Immigration Intake Form**: Collect and process client information for immigration cases
- **Document Generation**: Create necessary immigration documents based on client information
- **Case Tracking**: Follow case progress through the immigration system
- **Resource Library**: Access guides and information about immigration processes

### Immigration Dashboard (New Feature)

The new Immigration Dashboard provides a centralized location for users to:

- **Track Case Status**: View the status and progress of all immigration cases
- **Manage Forms**: Access and manage all submitted immigration intake forms
- **View Upcoming Events**: See deadlines, appointments, and other important events
- **Start New Applications**: Easily initiate new immigration applications

The dashboard includes:
- Status cards showing numbers of active cases, pending forms, completed cases, and upcoming deadlines
- Tabs to toggle between viewing active cases and forms
- A timeline of upcoming events and deadlines
- Mobile-responsive design for access on any device

## Recent Improvements

### UI/UX Enhancements (July 2023)
- Fixed dropdown menu functionality in the Immigration Intake Form
- Improved navigation between resource pages and document sections
- Enhanced mobile responsiveness across all form components
- Pre-filling of form fields based on selected immigration service type
- Added Immigration Dashboard for case tracking and management

### Performance Optimizations
- Implemented debounce mechanisms to prevent excessive API calls
- Increased backend rate limits for auth endpoints to prevent 429 errors
- Improved error handling and user feedback for form submissions
- Added token refresh handling with retry logic for better authentication flow
- Optimized context providers to reduce unnecessary re-renders

### Documentation and Testing
- Added comprehensive manual testing guides
- Improved form validation with clear error messaging
- Enhanced accessibility for all interactive components
- Added mobile-specific optimizations for touch interfaces

## Development

### Frontend

The frontend is built with React and Material-UI for a modern, responsive user interface.

### Backend

The backend is powered by Flask and MongoDB, providing a robust API for document management.

### Installation

```bash
npm run install-all
```

### Running the Application

```bash
npm start
```

### Testing

For manual testing instructions, see the [testing guide](tests/manual-testing.md).

#### Testing New Features

To test the new features added in the latest update:

1. **Immigration Form Dropdowns**
   - Navigate to `/immigration`
   - Click "Get Help" on any service card
   - Verify all dropdown menus display options and work correctly

2. **Mobile-Optimized Forms**
   - Access the application on a mobile device or use browser dev tools to simulate a mobile view
   - Open the Immigration Intake Form
   - Verify the form is properly formatted for mobile screens
   - Test all interaction elements for touch-friendliness

3. **Immigration Dashboard**
   - Login to the application
   - Navigate to `/immigration-dashboard`
   - Verify that the dashboard shows case statistics, form information, and upcoming events
   - Test the tab navigation between "Active Cases" and "Forms"
   - Try clicking the "New Application" button to start a new immigration form

4. **Performance Improvements**
   - Monitor network requests in browser dev tools
   - Verify no excessive API calls during authentication
   - Test authentication persistence after page reloads

## License

[MIT License](LICENSE)

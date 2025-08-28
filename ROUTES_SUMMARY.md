# SmartProBono Platform Routes Summary

This document provides a comprehensive overview of all the available routes in the SmartProBono platform, both frontend and backend.

## Frontend Routes

| Path | Component | Status | Description |
|------|-----------|--------|-------------|
| `/` | BetaLandingPage | ✅ Working | Main landing page with beta signup |
| `/home` | HomePage | ✅ Working | Alternative home page with more features |
| `/about` | About | ❓ Unknown | Information about SmartProBono |
| `/login` | LoginPage | ❓ Unknown | User login |
| `/register` | RegisterPage | ❓ Unknown | User registration |
| `/dashboard` | Dashboard | ❓ Unknown | Main user dashboard |
| `/admin-dashboard` | AdminDashboard | ❓ Unknown | Administrative dashboard |
| `/lawyer-dashboard` | LawyerDashboard | ❓ Unknown | Dashboard for attorneys |
| `/forms-dashboard` | FormsDashboard | ❓ Unknown | Form management |
| `/analytics-dashboard` | AnalyticsDashboard | ❓ Unknown | Usage analytics |
| `/immigration-dashboard` | ImmigrationDashboard | ❓ Unknown | Immigration case management |
| `/admin-notifications` | AdminNotificationDashboard | ❓ Unknown | Admin notifications |
| `/documents` | DocumentsPage | ✅ Fixed | Document management |
| `/contracts` | ContractsPage | ❓ Unknown | Contract templates |
| `/virtual-paralegal` | VirtualParalegalPage | ❓ Unknown | AI paralegal assistant |
| `/profile` | ProfilePage | ❓ Unknown | User profile management |
| `/expungement` | ExpungementPage | ❓ Unknown | Criminal record expungement |
| `/forms` | FormsIndexPage | ❓ Unknown | Available legal forms |
| `/resources` | Resources | ❓ Unknown | Legal resources |
| `/services` | Services | ❓ Unknown | Services offered |
| `/rights` | RightsPage | ❓ Unknown | Legal rights information |
| `/procedures` | ProceduresPage | ❓ Unknown | Legal procedures |
| `/contact` | Contact | ❓ Unknown | Contact information |
| `/legal-chat` | LegalAIChat | ✅ Working | Legal AI chat interface |
| `/expert-help` | ExpertHelpPage | ✅ Fixed | Pro bono attorney connection |
| `/beta/confirm/:token` | BetaConfirm | ❓ Unknown | Beta signup confirmation |
| `/business-model` | BusinessModel | ❓ Unknown | Platform business model |
| `/thank-you` | ThankYouPage | ❓ Unknown | Submission confirmation |
| `/reset-password` | ResetPasswordPage | ❓ Unknown | Password reset |
| `/forgot-password` | ForgotPasswordPage | ❓ Unknown | Forgot password |
| `/unauthorized` | UnauthorizedPage | ✅ Working | Access denied |
| `/not-found` | NotFoundPage | ✅ Working | 404 page |

## Backend API Endpoints (Currently Active)

| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/api/health` | GET | ✅ Working | API health check |
| `/api/beta/signup` | POST | ✅ Working | Beta program signup with email |
| `/api/legal/chat` | POST | ✅ Working | AI-powered legal chat interface |
| `/api/feedback` | POST | ✅ Working | User feedback submission |
| `/api/documents/history` | GET | ✅ Fixed | Get document history |
| `/api/documents/templates` | GET | ✅ Fixed | Get document templates |
| `/api/uploads/signature` | GET | ✅ Fixed | Get upload signature for documents |
| `/api/documents` | POST | ✅ Fixed | Save a new document |
| `/api/documents/:id` | GET | ✅ Fixed | Get a specific document |
| `/api/documents/:id` | DELETE | ✅ Fixed | Delete a document |

## What's Working & What's Fixed

1. **Working Components**:
   - Beta signup via email with DKIM authentication
   - Legal AI chat with multiple model options
   - Model switching via the ModelSelector component
   - Feedback submission
   - Health check endpoint
   - Email notifications
   
2. **Fixed Components**:
   - Document upload functionality on the `/documents` page
   - Document templates listing
   - Document history retrieval
   - Document storage and retrieval
   - Expert help page that was previously showing 404

## Potential Future Routes

The following routes are referenced in the code but may not be fully implemented yet:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/documents/scan` | POST | Scan uploaded documents for key information |
| `/api/documents/generate` | POST | Generate documents from templates |
| `/api/documents/preview` | POST | Preview document before generating |
| `/api/documents/:id/file` | GET | Get the actual file for a document |
| `/api/documents/:id/versions` | GET | Get version history for a document |
| `/api/documents/:id/versions/:version` | POST | Revert to a specific document version |
| `/api/documents/:id/share` | POST | Share a document with other users |
| `/api/documents/:id/tags` | PUT | Update document tags |
| `/api/documents/:id/category` | PUT | Update document category |
| `/api/documents/categories` | GET | Get available document categories |
| `/api/documents/search/tags` | POST | Search documents by tags |
| `/api/documents/tags/common` | GET | Get commonly used tags |

## Current Limitations & Next Steps

1. **Document Storage**:
   - Currently using a simple file-based storage
   - In production, should use a database and proper cloud storage (Cloudinary)

2. **Authentication**:
   - User authentication is referenced in code but not fully implemented
   - Many routes likely require authentication to work properly

3. **Beta Program**:
   - Email confirmation flow is working but UI may need refinement

4. **Document Management**:
   - Basic document operations are working
   - Advanced features like sharing, versioning, and templates need further implementation

5. **Expert Help**:
   - Page UI is implemented but backend integration needs development
   - Pro bono attorney connection workflow needs implementation 
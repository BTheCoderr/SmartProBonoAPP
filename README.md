# SmartProBono Platform

An AI-powered legal platform providing accessible legal assistance for pro bono cases.

## MVP Status

SmartProBono now has a functioning MVP with the following key features:

- ✅ **Legal AI Chat** with multiple model options (fixed model selection)
- ✅ **Document Management** for uploading and organizing legal documents
- ✅ **Expert Help** interface for connecting with pro bono attorneys
- ✅ **Email System** with Zoho integration and DKIM authentication
- ✅ **User Management** for beta signup and demo accounts

For detailed documentation on available routes and features, see:
- [MVP_ROUTES.md](MVP_ROUTES.md) - List of working MVP routes
- [MVP_NEXT_STEPS.md](MVP_NEXT_STEPS.md) - Current status and future development plans
- [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) - Testing guidance

## Recent Fixes

### Model Selection Fix
- Fixed model selection persistence in the legal chat
- Added clearer indication of which model is being used
- Fixed UI inconsistencies in model display
- Added test script `test_model_selection.py` to verify model selection

### UI Improvements
- Fixed testimonial styling issues in the landing page
- Cleaned up unused imports across multiple components
- Improved error handling in document upload

## Running the Platform

### Backend
```bash
./run_with_email_alt.sh
```

### Frontend
```bash
cd frontend
npm start
```

### Testing Model Selection
```bash
./test_model_selection.py
```

## Demo Routes

- Home: http://localhost:3000/
- Legal Chat: http://localhost:3000/legal-chat
- Documents: http://localhost:3000/documents
- Expert Help: http://localhost:3000/expert-help

## Project Structure

- `backend/` - Flask backend API
- `frontend/` - React frontend application
- `scripts/` - Utility scripts for the platform
- `templates/` - Email and document templates

## Next Steps

See [MVP_NEXT_STEPS.md](MVP_NEXT_STEPS.md) for the detailed roadmap of future development.

## Key Features

- **AI-powered Legal Chat**: Get answers to common legal questions
- **Document Generation**: Create legal documents based on your needs
- **Expert Guidance**: Connect with pro bono lawyers when needed
- **Email Notifications**: Receive confirmation emails and updates

## Development

### Code Quality

To maintain code quality in the project:

1. We use ESLint for code linting. Run the following commands in the frontend directory:
   ```bash
   # Check for linting issues
   npm run lint
   
   # Automatically fix simple issues
   npm run lint:fix
   ```

2. See [LINTING_GUIDE.md](LINTING_GUIDE.md) for information on:
   - Common linting issues and how to fix them
   - Best practices for clean code
   - Maintenance scripts for code cleanup

## Getting Started

Follow these steps to set up and run the SmartProBono platform:

### Prerequisites

- Node.js (v14+) and npm (v6+)
- Python 3.8+
- Virtual environment tool (venv)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/SmartProBono.git
   cd SmartProBono
   ```

2. **Set up Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up frontend dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure email (optional but recommended)**:
   ```bash
   ./setup_email.sh
   ```
   Follow the prompts to configure your email settings. This enables email notifications for signups.

### Running the Application

#### Option 1: Using the deployment script (recommended)

This will start both the frontend and backend with proper configuration:

```bash
./deploy.sh
```

#### Option 2: Manual start

1. **Start the backend API**:
   ```bash
   # With email configuration:
   source load_email_config.sh
   python fix_api.py
   
   # Without email:
   python fix_api.py
   ```

2. **Start the frontend development server** (in a separate terminal):
   ```bash
   cd frontend
   npm start
   ```

### Testing

#### Test Email Configuration

To verify your email setup is working correctly:

```bash
# Make sure your email config is loaded
source load_email_config.sh

# Send a test email
python test_email.py your-email@example.com
```

#### Test Legal Chat API

To test the legal chat functionality:

```bash
# Test all models and questions
./test_legal_chat.py

# Test specific model and question
./test_legal_chat.py deepseek "What are my tenant rights?"
```

## System Architecture

- **Frontend**: React.js with Material UI
- **Backend API**: Flask with REST endpoints
- **Email System**: SMTP-based email notifications
- **Storage**: File-based storage for beta (database for production)

## Deployment

For production deployment, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## Email Notification System

The platform includes an email notification system that:

1. Sends confirmation emails to users who sign up
2. Notifies administrators about new signups
3. Provides professional-looking HTML emails

See [EMAIL_CAPTURE_README.md](EMAIL_CAPTURE_README.md) for details on the email system.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact info@smartprobono.org

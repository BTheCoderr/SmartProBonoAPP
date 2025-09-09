# 🚀 SmartProBono Quick Start Guide

## One-Command Startup

### Start Everything:
```bash
./start_smartprobono_complete.sh
```

### Stop Everything:
```bash
./stop_smartprobono.sh
```

## What Gets Started

### Backend (Port 3001)
- ✅ Enhanced Flask server with safety features
- ✅ Document scanner with UPL prevention
- ✅ PDF generator with templates
- ✅ Contact form with email integration
- ✅ Health monitoring and status checks

### Frontend (Port 3002)
- ✅ React application with Material-UI
- ✅ Document scanner interface
- ✅ PDF generator interface
- ✅ AI legal chat (placeholder)
- ✅ Contact form interface

## Access Your Application

- **Main App**: http://localhost:3002
- **API Health**: http://localhost:3001/api/health
- **Scanner Health**: http://localhost:3001/api/scanner/health
- **Generator Health**: http://localhost:3001/api/generator/health

## Features

### 🛡️ Safety & Compliance
- UPL (Unauthorized Practice of Law) prevention
- Automatic legal disclaimers
- Escalation detection for complex matters
- Response sanitization

### 📄 Document Processing
- PDF text extraction
- AI-powered analysis
- Party identification
- Key terms extraction
- Risk assessment
- Action item generation

### ✍️ PDF Generation
- Lease agreements
- Service contracts
- Non-disclosure agreements
- Employment contracts
- Custom document creation

### 📧 Communication
- Contact form with Resend API
- Email notifications
- Professional templates

## Troubleshooting

### If ports are in use:
```bash
./stop_smartprobono.sh
# Wait a few seconds
./start_smartprobono_complete.sh
```

### If you see errors:
1. Make sure you're in the SmartProBono-main directory
2. Ensure virtual environment is activated
3. Check that all dependencies are installed

### Manual startup (if needed):
```bash
# Terminal 1 - Backend
cd backend
source ../venv/bin/activate
export RESEND_API_KEY=re_N7YNzBXp_HyNzVsWjuLNqxqUQr8oxaxvf
python combined_server.py

# Terminal 2 - Frontend
cd frontend
npm start
```

## System Requirements

- Python 3.8+
- Node.js 16+
- Virtual environment activated
- Internet connection (for email API)

## Support

The system includes comprehensive health monitoring. Check the terminal output for status updates and any error messages.

Happy coding! 🎉

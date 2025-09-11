# SmartProBono - Complete Legal Platform

A comprehensive legal assistance platform with AI-powered features, role-based dashboards, and real-time case management.

## 🚀 Core Features

### 🤖 AI-Powered Features
- **AI Virtual Paralegal**: Autonomous AI system for case research and document generation
- **Legal AI Chat**: Instant legal assistance and guidance
- **Document Scanner**: Upload and analyze legal documents with AI insights
- **PDF Generator**: Create professional legal documents from templates
- **Case Law Research**: Real-time access to CourtListener API for case law research

### 👥 Role-Based Dashboards
- **Client Portal**: Case tracking, progress monitoring, document access
- **Lawyer Dashboard**: Case management, client communication, analytics
- **Bondsman Dashboard**: Bail bond management, payment tracking, risk assessment
- **Admin Dashboard**: System management, user analytics, compliance monitoring

### 🔄 Real-Time Features
- **Live Notifications**: Real-time updates on case progress and deadlines
- **WebSocket Integration**: Instant communication and updates
- **Progress Tracking**: Visual progress bars and status updates
- **Document Collaboration**: Real-time document sharing and editing

### ⚖️ Legal Tools
- **Document Analysis**: AI-powered legal document review
- **Form Generation**: Automated legal form creation
- **Compliance Scanner**: Legal compliance checking
- **Risk Assessment**: Automated risk analysis for cases

## 🛠️ Quick Start

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
cd backend
export RESEND_API_KEY=your_api_key_here
python combined_server.py
```

### Frontend Setup
```bash
# Install dependencies
npm install

# Start frontend
npm start
```

## 📁 Project Structure

```
SmartProBono-main/
├── backend/
│   ├── combined_server.py      # Main Flask server
│   ├── simple_ai_service.py   # AI document processing
│   └── routes/                 # API endpoints
├── frontend/
│   ├── src/
│   │   ├── pages/             # React pages
│   │   └── components/        # React components
│   └── public/                # Static assets
└── requirements.txt           # Python dependencies
```

## 🔧 API Endpoints

### Document Processing
- `GET /api/scanner/health` - Document scanner health check
- `POST /api/scanner/analyze` - Analyze uploaded documents
- `GET /api/generator/templates` - Get document templates
- `POST /api/generator/create` - Generate PDF documents

### AI Virtual Paralegal
- `POST /api/v1/ai-virtual-paralegal/start` - Start AI workflow
- `GET /api/v1/ai-virtual-paralegal/status` - Get AI status
- `GET /api/v1/ai-virtual-paralegal/logs` - Get activity logs
- `POST /api/v1/ai-virtual-paralegal/search-cases` - Search CourtListener API
- `POST /api/v1/ai-virtual-paralegal/similar-cases` - Find similar cases
- `GET /api/v1/ai-virtual-paralegal/recent-cases` - Get recent cases
- `POST /api/v1/ai-virtual-paralegal/generate-document` - Generate documents
- `GET /api/v1/ai-virtual-paralegal/dashboard` - Get dashboard data

### Enhanced API (v2)
- `GET /api/v2/` - API documentation and root
- `GET /api/v2/cases/` - List cases with pagination
- `POST /api/v2/cases/` - Create new case
- `GET /api/v2/cases/{id}/` - Get specific case
- `PUT /api/v2/cases/{id}/` - Update case
- `DELETE /api/v2/cases/{id}/` - Delete case
- `GET /api/v2/users/` - List users
- `GET /api/v2/documents/` - List documents
- `GET /api/v2/health/` - Health check

### Contact & Support
- `POST /api/contact/submit` - Submit contact form

## 🌐 Access

### Main Application
- **Frontend**: http://localhost:3002
- **Backend**: http://localhost:3001

### User Dashboards
- **Client Portal**: http://localhost:3002/client-portal
- **Lawyer Dashboard**: http://localhost:3002/lawyer-dashboard
- **Bondsman Dashboard**: http://localhost:3002/bondsman-dashboard
- **Admin Dashboard**: http://localhost:3002/admin

### AI Features
- **AI Virtual Paralegal**: http://localhost:3002/ai-virtual-paralegal
- **Legal AI Chat**: http://localhost:3002/legal-chat
- **Virtual Paralegal**: http://localhost:3002/virtual-paralegal

### Legal Tools
- **Legal Tools**: http://localhost:3002/legal-tools
- **Document Scanner**: http://localhost:3002/document-scanner
- **Document Generator**: http://localhost:3002/generate-document
- **Safety Check**: http://localhost:3002/safety-check

### API Documentation
- **Enhanced API**: http://localhost:3001/api/v2/
- **API Health**: http://localhost:3001/api/v2/health/

## 📝 License

MIT License - see LICENSE file for details
# SmartProBono - Legal Help Made Simple

A streamlined legal assistance platform with AI-powered document analysis and generation.

## 🚀 Features

- **Document Scanner**: Upload and analyze legal documents with AI insights
- **PDF Generator**: Create professional legal documents from templates
- **AI Legal Chat**: Get instant legal assistance (coming soon)

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

- `GET /api/scanner/health` - Document scanner health check
- `POST /api/scanner/analyze` - Analyze uploaded documents
- `GET /api/generator/templates` - Get document templates
- `POST /api/generator/create` - Generate PDF documents
- `POST /api/contact/submit` - Submit contact form

## 🌐 Access

- Frontend: http://localhost:3002
- Backend: http://localhost:3001
- Legal Tools: http://localhost:3002/legal-tools

## 📝 License

MIT License - see LICENSE file for details
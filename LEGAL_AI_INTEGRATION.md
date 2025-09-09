# Legal AI Integration Guide

This guide explains how to use the integrated Legal AI system in SmartProBono, which combines LangGraph-based legal analysis with your existing frontend and backend.

## 🏗️ Architecture Overview

The Legal AI system consists of three main components:

1. **Legal AI Backend** (`legal_ai_backend/`) - LangGraph-based pipeline with specialized agents
2. **Main Backend** (`backend/`) - Flask API that integrates with the legal AI backend
3. **Frontend** (`frontend/`) - React interface for user interaction

## 🚀 Quick Start

### 1. Setup Legal AI Integration

```bash
# Run the setup script
./setup_legal_ai.sh
```

### 2. Configure API Keys

Edit `legal_ai_backend/.env`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the Services

```bash
# Terminal 1: Start Backend
cd backend
source ../venv/bin/activate
python combined_server.py

# Terminal 2: Start Frontend
cd frontend
npm start
```

### 4. Test the Integration

```bash
# Run the test suite
python test_legal_ai_integration.py
```

## 🔧 How It Works

### Legal AI Pipeline

The system uses a multi-agent LangGraph pipeline:

1. **Intake Agent** - Extracts legal topic, jurisdiction, and case details
2. **CourtListener Agent** - Searches live case law via CourtListener API
3. **Vector Agent** - Searches local case embeddings using ChromaDB
4. **Summarizer Agent** - Uses Claude to analyze and summarize findings
5. **Compliance Agent** - Adds legal disclaimers and compliance measures

### API Endpoints

- `POST /api/legal-analysis` - Main endpoint for legal analysis
- `POST /api/legal-ai/chat` - Basic chat interface (fallback)
- `GET /api/legal-ai/models` - Available AI models

### Frontend Integration

The frontend calls the integrated API at `http://localhost:3001/api/legal-analysis` and displays:
- Case analysis and summaries
- Key facts and legal rules
- Practical advice
- Compliance disclaimers and warnings
- Recommendations

## 📁 File Structure

```
SmartProBono-main/
├── legal_ai_backend/           # LangGraph-based legal AI system
│   ├── agents/                 # Specialized AI agents
│   │   ├── intake_agent.py
│   │   ├── courtlistener_agent.py
│   │   ├── vector_agent.py
│   │   ├── summarizer_agent.py
│   │   └── compliance_agent.py
│   ├── langgraph/
│   │   └── main_graph.py       # Main LangGraph pipeline
│   ├── case_sources/
│   │   └── courtlistener.py    # CourtListener API client
│   └── requirements.txt
├── backend/
│   ├── routes/
│   │   └── legal_ai.py         # Integrated API routes
│   └── requirements.txt        # Updated with legal AI deps
├── frontend/
│   └── src/
│       └── components/
│           └── ImprovedLegalAIChat.js  # Updated frontend component
└── test_legal_ai_integration.py       # Integration tests
```

## 🧪 Testing

### Manual Testing

1. Visit `http://localhost:3002/legal-chat`
2. Enter a legal question like: "I was charged with gun possession in Rhode Island"
3. Check the response for:
   - Case analysis
   - Legal disclaimers
   - Practical advice
   - Compliance warnings

### Automated Testing

```bash
python test_legal_ai_integration.py
```

This tests:
- Legal AI backend directly
- Backend API integration
- Frontend connectivity

## 🔧 Configuration

### Environment Variables

Required in `legal_ai_backend/.env`:
- `ANTHROPIC_API_KEY` - For Claude AI analysis
- `OPENAI_API_KEY` - Optional, for OpenAI models

### Jurisdiction Support

Currently supports:
- Rhode Island (ri) - Default
- Massachusetts (ma)
- Connecticut (ct)
- New York (ny)
- California (ca)

### Case Types

The system handles:
- Criminal cases
- Civil cases
- Family law
- Immigration
- Business law

## 🚨 Troubleshooting

### Common Issues

1. **"Legal AI backend not available"**
   - Check that dependencies are installed: `pip install -r legal_ai_backend/requirements.txt`
   - Verify API keys are set in `.env`

2. **"Analysis temporarily unavailable"**
   - Check Anthropic API key
   - Verify internet connection for CourtListener API

3. **Frontend shows "Analysis failed"**
   - Check backend is running on port 3001
   - Verify API endpoint is correct

### Debug Mode

Enable debug logging in `backend/routes/legal_ai.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Fallback System

The system includes robust fallbacks:

1. **Primary**: LangGraph pipeline with full legal analysis
2. **Secondary**: Basic AI service with Ollama
3. **Tertiary**: Static response with disclaimers

## 📈 Performance

- **Response Time**: 5-15 seconds for full analysis
- **Fallback Time**: 2-5 seconds for basic responses
- **Concurrent Users**: Supports multiple simultaneous requests

## 🔒 Compliance

The system includes:
- Legal disclaimers on all responses
- Jurisdiction-specific warnings
- Urgency-based compliance levels
- Attorney consultation recommendations

## 🚀 Next Steps

1. **Add More Jurisdictions**: Extend jurisdiction support
2. **Enhance Vector Store**: Add more case law embeddings
3. **Improve Agents**: Add specialized legal domain agents
4. **Add Caching**: Cache frequent queries for better performance
5. **User Authentication**: Track user queries and history

## 📞 Support

For issues with the Legal AI integration:
1. Check the troubleshooting section above
2. Run the test suite to identify specific problems
3. Check backend logs for error details
4. Verify all dependencies are properly installed

---

**Note**: This system provides legal information, not legal advice. Always consult with a qualified attorney for specific legal matters.

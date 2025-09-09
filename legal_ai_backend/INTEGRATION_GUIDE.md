# Legal AI Backend Integration Guide

## 🚀 Quick Start

### 1. Start the New Backend

```bash
cd legal_ai_backend
./start_backend.sh
```

The backend will start on `http://localhost:5000`

### 2. Update Frontend Configuration

The frontend AI chat component has been updated to use the new backend. No additional configuration needed.

### 3. Test the Integration

1. Start the frontend: `cd frontend && npm start`
2. Navigate to the AI chat page
3. Ask a legal question like "I was charged with gun possession, what should I do?"

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `legal_ai_backend` directory:

```bash
ANTHROPIC_API_KEY=sk-your-claude-key
OPENAI_API_KEY=sk-your-openai-key
DEBUG=True
```

### API Endpoints

- `POST /api/legal-analysis` - Complete legal analysis
- `POST /api/case-search` - Case law search only
- `GET /api/vector-stats` - Vector store statistics
- `GET /health` - Health check

## 🧪 Testing

### Test Individual Components

```bash
cd legal_ai_backend
python test_pipeline.py
```

### Test API Endpoints

```bash
curl -X POST http://localhost:5000/api/legal-analysis \
  -H "Content-Type: application/json" \
  -d '{"query": "I was charged with gun possession, what should I do?"}'
```

## 🔄 Migration from Old System

The new system is designed to be a drop-in replacement for the existing AI chat. The frontend component has been updated to:

1. Call the new LangGraph backend instead of the old AI service
2. Display structured legal analysis with disclaimers and warnings
3. Show case law research results
4. Provide compliance-enhanced responses

## 🚨 Troubleshooting

### Common Issues

1. **Backend not starting**: Check that all dependencies are installed
2. **API errors**: Verify the Claude API key is set correctly
3. **No case results**: Ensure the vector store is seeded with case data
4. **Frontend not connecting**: Check that the backend is running on port 5000

### Debug Mode

Enable debug mode by setting `DEBUG=True` in the `.env` file.

## 📊 Performance

- **Response Time**: 3-6 seconds for complete analysis
- **Case Search**: 500ms for CourtListener + 200ms for vector search
- **Claude Analysis**: 2-5 seconds depending on complexity

## 🔒 Legal Compliance

The new system includes comprehensive legal disclaimers and compliance measures:

- All responses include "Not Legal Advice" disclaimers
- Urgency warnings for criminal cases
- Attorney consultation recommendations
- Jurisdiction-specific guidance

## 🚀 Production Deployment

For production deployment:

1. Set up proper environment variables
2. Use a production WSGI server (Gunicorn)
3. Set up proper logging and monitoring
4. Configure reverse proxy (Nginx)
5. Set up SSL certificates

## 📈 Monitoring

Monitor the system using:

- Health check endpoint: `GET /health`
- Vector store stats: `GET /api/vector-stats`
- Application logs
- API response times

## 🔮 Future Enhancements

- Real-time case law updates
- Multi-language support
- Advanced legal reasoning
- Document analysis
- Court filing assistance

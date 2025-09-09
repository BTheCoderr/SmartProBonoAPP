# 🚀 VSCode Setup for Legal AI Backend

Complete setup guide for running the CourtListener + Claude Legal AI pipeline in VSCode.

## 🎯 Quick Start

### 1. Open VSCode Workspace
```bash
code SmartProBono.code-workspace
```

### 2. Run Setup Task
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type "Tasks: Run Task"
- Select "Setup Legal AI Backend"

### 3. Configure API Keys
Edit `legal_ai_backend/.env`:
```bash
ANTHROPIC_API_KEY=sk-your-actual-claude-key-here
OPENAI_API_KEY=sk-your-openai-key-here  # Optional
```

### 4. Start the Backend
- Press `F5` or use "Legal AI Backend" launch configuration
- Or run task: "Start Legal AI Backend"

## 🏗️ Architecture Overview

```
User Input → Intake Agent → CourtListener Agent → Summarizer Agent → Compliance Agent
                    ↓              ↓                    ↓
              Vector Agent → ChromaDB → Claude API → Final Result
```

## 🔧 VSCode Features

### Multi-Root Workspace
- **SmartProBono Root**: Main project directory
- **Legal AI Backend**: LangGraph + Claude pipeline
- **Frontend**: React application

### Python Environment
- **Interpreter**: `legal_ai_backend/.venv/bin/python`
- **Auto-activation**: Virtual environment activates automatically
- **IntelliSense**: Full code completion and error detection

### Tasks (Ctrl+Shift+P → Tasks: Run Task)
- **Setup Legal AI Backend**: Complete environment setup
- **Start Legal AI Backend**: Start API server on port 5000
- **Test Legal AI Pipeline**: Run comprehensive tests
- **Seed Case Law Data**: Populate vector store with case law
- **Start Frontend**: Start React development server

### Launch Configurations (F5)
- **Legal AI Backend**: Start API server with debugging
- **Test Legal AI Pipeline**: Run pipeline tests with debugging
- **Seed Case Law Data**: Seed vector store with debugging

## 🧪 Testing the Pipeline

### 1. Run Demo Script
```bash
cd legal_ai_backend
python3 demo_pipeline.py
```

### 2. Test Individual Agents
```python
from agents.intake_agent import intake
result = intake("I was charged with gun possession in Boston")
print(result)
```

### 3. Test Complete Pipeline
```python
from langgraph.main_graph import run_pipeline
result = run_pipeline("I was charged with gun possession, what should I do?")
print(result)
```

### 4. Test API Endpoints
```bash
curl -X POST http://localhost:5000/api/legal-analysis \
  -H "Content-Type: application/json" \
  -d '{"query": "I was charged with gun possession, what should I do?"}'
```

## 🔍 Debugging

### Python Debugging
1. Set breakpoints in any Python file
2. Press `F5` to start debugging
3. Use VSCode debugger controls

### API Debugging
1. Start backend with "Legal AI Backend" configuration
2. Set breakpoints in `api_server.py`
3. Make API calls to trigger breakpoints

### Pipeline Debugging
1. Use "Test Legal AI Pipeline" configuration
2. Set breakpoints in agent files
3. Step through the complete pipeline

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

### Vector Store Stats
```bash
curl http://localhost:5000/api/vector-stats
```

### API Logs
- Backend logs appear in VSCode terminal
- Use `Ctrl+Shift+P` → "Terminal: Clear" to clear logs

## 🚀 Development Workflow

### 1. Start Development
```bash
# Terminal 1: Backend
cd legal_ai_backend
./quick_start.sh

# Terminal 2: Frontend
cd frontend
npm start
```

### 2. Make Changes
- Edit agent files in `legal_ai_backend/agents/`
- Modify pipeline in `legal_ai_backend/langgraph/`
- Update frontend in `frontend/src/`

### 3. Test Changes
- Use VSCode tasks to run tests
- Use F5 to debug specific components
- Use demo script to test complete pipeline

### 4. Deploy
- Use VSCode tasks for production builds
- Use launch configurations for production deployment

## 🔧 Configuration

### Environment Variables
```bash
# Required
ANTHROPIC_API_KEY=sk-your-claude-key

# Optional
OPENAI_API_KEY=sk-your-openai-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
DEBUG=True
LOG_LEVEL=INFO
```

### VSCode Settings
- **Python Interpreter**: Auto-detected from virtual environment
- **Linting**: Flake8 enabled
- **Formatting**: Black formatter
- **Testing**: Pytest enabled

## 🐛 Troubleshooting

### Common Issues

#### 1. Virtual Environment Not Active
```bash
cd legal_ai_backend
source .venv/bin/activate
```

#### 2. Dependencies Not Installed
```bash
cd legal_ai_backend
pip install -r requirements.txt
```

#### 3. API Key Not Configured
- Edit `legal_ai_backend/.env`
- Replace placeholder keys with actual keys

#### 4. Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

#### 5. Vector Store Not Seeded
```bash
cd legal_ai_backend
python3 ../scripts/seed_harvard_cases.py
```

### Debug Commands

#### Check Python Environment
```bash
cd legal_ai_backend
python3 -c "import sys; print(sys.executable)"
```

#### Check Dependencies
```bash
cd legal_ai_backend
pip list | grep -E "(langgraph|chromadb|anthropic)"
```

#### Check API Keys
```bash
cd legal_ai_backend
python3 -c "import os; print('Claude:', bool(os.getenv('ANTHROPIC_API_KEY')))"
```

## 📈 Performance

### Expected Response Times
- **Intake Processing**: ~100ms
- **Case Search**: ~500ms (CourtListener) + ~200ms (Vector)
- **Claude Analysis**: ~2-5s
- **Total Pipeline**: ~3-6s

### Optimization Tips
- Use vector store for fast local searches
- Cache CourtListener results
- Optimize Claude prompts
- Use async processing for multiple requests

## 🔒 Security

### API Key Management
- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly

### Legal Compliance
- All responses include disclaimers
- No specific legal advice provided
- Always recommend attorney consultation

## 🚀 Production Deployment

### Using VSCode
1. Configure production environment variables
2. Use "Production" launch configuration
3. Deploy using VSCode tasks

### Manual Deployment
```bash
cd legal_ai_backend
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [CourtListener API](https://www.courtlistener.com/api/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test using VSCode tasks
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Happy coding! 🚀**

For questions or issues, please create an issue in the repository or contact the development team.

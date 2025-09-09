# Legal AI Backend - LangGraph + Claude Integration

A sophisticated legal AI system using LangGraph for agent orchestration, ChromaDB for vector storage, and Claude for legal analysis.

## 🏗️ Architecture

```
User Input → Intake Agent → CourtListener Agent → Summarizer Agent → Compliance Agent
                    ↓              ↓                    ↓
              Vector Agent → ChromaDB → Claude API → Final Result
```

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Install system dependencies
brew install git python node
pip install virtualenv
npm install -g pnpm

# Install Python dependencies
cd legal_ai_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Setup

Create `.env` file:

```bash
# Legal AI Backend Configuration
ANTHROPIC_API_KEY=sk-your-claude-key
OPENAI_API_KEY=sk-your-openai-key

# Database Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Vector Store Configuration
CHROMA_PERSIST_DIRECTORY=./vectorstore/chroma_data

# Development Settings
DEBUG=True
LOG_LEVEL=INFO
```

### 3. Seed Case Law Data

```bash
# Seed Harvard case law data
python scripts/seed_harvard_cases.py
```

### 4. Test the System

```bash
# Run test suite
python test_pipeline.py

# Start API server
python api_server.py
```

## 🤖 Agents

### Intake Agent
- **Purpose**: Extracts legal topic, jurisdiction, and case details
- **Input**: Raw user input
- **Output**: Structured legal information
- **Features**: Keyword extraction, urgency detection, charge suggestions

### CourtListener Agent
- **Purpose**: Searches live case law via CourtListener API
- **Input**: Legal context from intake
- **Output**: Recent case law results
- **Features**: Real-time case search, jurisdiction filtering

### Vector Agent
- **Purpose**: Searches local case embeddings using ChromaDB
- **Input**: Legal context from intake
- **Output**: Similar case results from vector store
- **Features**: Semantic search, similarity scoring

### Summarizer Agent
- **Purpose**: Analyzes cases using Claude AI
- **Input**: Case data from search agents
- **Output**: Legal analysis and explanations
- **Features**: Case law analysis, practical advice, legal explanations

### Compliance Agent
- **Purpose**: Adds legal disclaimers and compliance measures
- **Input**: Legal analysis from summarizer
- **Output**: Compliance-enhanced results
- **Features**: Legal disclaimers, urgency warnings, attorney recommendations

## 🔧 API Endpoints

### POST `/api/legal-analysis`
Complete legal analysis pipeline.

**Request:**
```json
{
  "query": "I was charged with gun possession, what should I do?",
  "jurisdiction": "ri"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "case_summary": "Analysis of relevant cases...",
    "key_facts": ["Fact 1", "Fact 2"],
    "legal_rules": ["Rule 1", "Rule 2"],
    "practical_advice": ["Advice 1", "Advice 2"]
  },
  "disclaimers": ["Not legal advice", "Consult attorney"],
  "warnings": ["Urgent: Contact attorney immediately"],
  "recommendations": ["Contact qualified attorney"],
  "compliance_level": "high"
}
```

### POST `/api/case-search`
Case law search only (without full analysis).

### GET `/api/vector-stats`
Vector store statistics.

## 📊 Data Sources

### CourtListener API
- **Source**: Free tier access to court opinions
- **Coverage**: Federal and state court decisions
- **Update**: Real-time access to recent cases

### Harvard Case.Law
- **Source**: Harvard Law School case database
- **Coverage**: Historical case law
- **Storage**: Local ChromaDB vector store

### Vector Store
- **Database**: ChromaDB
- **Embeddings**: Sentence Transformers
- **Storage**: Local persistent storage

## 🧪 Testing

```bash
# Test individual agents
python -c "from agents.intake_agent import intake; print(intake('I was charged with gun possession'))"

# Test complete pipeline
python test_pipeline.py

# Test API endpoints
curl -X POST http://localhost:5000/api/legal-analysis \
  -H "Content-Type: application/json" \
  -d '{"query": "I was charged with gun possession, what should I do?"}'
```

## 🔒 Legal Compliance

The system includes comprehensive legal disclaimers:

- ⚠️ **Not Legal Advice**: All outputs are informational only
- ⚖️ **Consult Attorney**: Always recommend qualified legal counsel
- 📅 **Case Law Changes**: Acknowledge that laws may have changed
- 🔍 **Unique Circumstances**: Each case is unique
- 🏛️ **Jurisdiction Specific**: Laws vary by location
- ⏰ **Time Sensitive**: Legal deadlines may apply

## 🚀 Deployment

### Local Development
```bash
python api_server.py
```

### Production
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app

# Using Docker
docker build -t legal-ai-backend .
docker run -p 5000:5000 legal-ai-backend
```

## 📈 Performance

- **Intake Processing**: ~100ms
- **Case Search**: ~500ms (CourtListener) + ~200ms (Vector)
- **Claude Analysis**: ~2-5s
- **Total Pipeline**: ~3-6s

## 🔧 Configuration

### Environment Variables
- `ANTHROPIC_API_KEY`: Claude API key
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `CHROMA_PERSIST_DIRECTORY`: Vector store location
- `DEBUG`: Enable debug mode

### Agent Configuration
- Modify agent parameters in individual agent files
- Adjust search limits and similarity thresholds
- Customize legal disclaimers and warnings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Additional case law sources
- [ ] Real-time case updates
- [ ] Advanced legal reasoning
- [ ] Integration with legal databases
- [ ] Mobile app support
- [ ] Voice interface
- [ ] Document analysis
- [ ] Legal form generation
- [ ] Court filing assistance

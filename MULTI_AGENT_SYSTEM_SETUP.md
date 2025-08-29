# 🚀 SmartProBono Multi-Agent System - Complete Setup

## ✅ **What We've Built**

A **REAL multi-agent AI system** using:
- **LangGraph**: Multi-agent orchestration with explicit state management
- **Haystack 2.x**: RAG pipeline with document retrieval and generation
- **Supabase**: PostgreSQL with pgvector for document storage
- **FastAPI**: Production-ready API server
- **Ollama**: Local AI models (or can use OpenAI/Anthropic)

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  Supabase DB    │
│                 │    │                  │    │                 │
│  - Material UI  │◄──►│  - LangGraph     │◄──►│  - PostgreSQL   │
│  - Chat Interface│    │  - Haystack RAG  │    │  - pgvector     │
│  - Document Upload│    │  - Multi-Agents  │    │  - RLS Security │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Ollama AI      │
                       │                  │
                       │  - llama3:8b     │
                       │  - Local Models  │
                       └──────────────────┘
```

## 🤖 **Multi-Agent System**

### **4 Specialized Agents:**

1. **Intake Agent**
   - Normalizes user questions
   - Extracts jurisdiction (state/federal)
   - Determines complexity level

2. **Research Agent**
   - Searches legal documents using Haystack RAG
   - Finds relevant statutes and case law
   - Provides accurate citations

3. **Drafting Agent**
   - Generates clear legal responses
   - Uses plain English when possible
   - Includes proper disclaimers

4. **Safety Agent**
   - Prevents unauthorized legal advice
   - Ensures compliance with legal ethics
   - Flags responses needing attorney review

## 📁 **Project Structure**

```
smartprobono_backend/
├── api/
│   └── main.py              # FastAPI application
├── graph/
│   ├── state.py             # LangGraph state definition
│   ├── nodes.py             # Agent node implementations
│   └── build.py             # Graph builder
├── rag/
│   ├── store.py             # Supabase pgvector store
│   └── pipelines.py         # Haystack RAG pipelines
├── utils/
│   ├── safety.py            # UPL guard and safety checks
│   └── prompts.py           # Agent prompt templates
├── requirements.txt         # Dependencies
└── .env                     # Environment variables
```

## 🚀 **How to Run**

### **1. Start the Multi-Agent System:**
```bash
./start_multi_agent_system.sh
```

### **2. Test the API:**
```bash
# Health check
curl http://localhost:8000/api/health

# Simple query (RAG only)
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my rights if I get arrested?"}'

# Multi-agent assist
curl -X POST http://localhost:8000/api/assist \
  -H "Content-Type: application/json" \
  -d '{"query": "I need help with immigration law in California"}'
```

### **3. Upload Documents:**
```bash
curl -X POST http://localhost:8000/api/ingest/pdf \
  -F "files=@legal_document.pdf"
```

## 🔧 **Configuration**

### **Environment Variables:**
```bash
# Database
PG_CONN_STR=postgresql://user:pass@host:port/db?sslmode=require

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_key

# AI Models
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b

# Optional: OpenAI/Anthropic
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## 🧪 **Testing the System**

### **Test Different Agent Types:**

```bash
# Greeting (Intake Agent)
curl -X POST http://localhost:8000/api/assist \
  -d '{"query": "hello"}'

# Immigration (Research + Drafting Agents)
curl -X POST http://localhost:8000/api/assist \
  -d '{"query": "I need help with a visa application"}'

# Family Law (All Agents)
curl -X POST http://localhost:8000/api/assist \
  -d '{"query": "What are the custody laws in Massachusetts?"}'

# Complex Legal (Safety Agent will flag)
curl -X POST http://localhost:8000/api/assist \
  -d '{"query": "Should I file a lawsuit against my employer?"}'
```

## 🔒 **Safety Features**

### **Unauthorized Practice of Law (UPL) Guard:**
- Detects advice-giving language
- Flags complex legal matters
- Routes to human attorney when needed
- Adds appropriate disclaimers

### **Compliance Features:**
- All responses include disclaimers
- Clear separation of information vs. advice
- Audit trail for all interactions
- Jurisdiction-aware responses

## 🌐 **Frontend Integration**

### **Update your React frontend to use the new API:**

```javascript
// In your React component
const askQuestion = async (question) => {
  const response = await fetch('http://localhost:8000/api/assist', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: question })
  });
  
  const result = await response.json();
  
  return {
    answer: result.answer,
    escalate: result.escalate,
    citations: result.citations,
    jurisdiction: result.jurisdiction
  };
};
```

## 🚀 **Production Deployment**

### **1. Update render.yaml:**
```yaml
services:
  - type: web
    name: smartProBonoMultiAgent
    env: python
    pythonVersion: "3.11"
    buildCommand: cd smartprobono_backend && pip install -r requirements.txt
    startCommand: cd smartprobono_backend && python -m uvicorn api.main:app --host 0.0.0.0 --port 10000
    envVars:
      - key: PG_CONN_STR
        value: your_supabase_connection_string
      - key: SUPABASE_URL
        value: your_supabase_url
      - key: SUPABASE_SERVICE_KEY
        value: your_service_key
```

### **2. Deploy to Render:**
```bash
git add .
git commit -m "Add multi-agent system with LangGraph + Haystack"
git push origin main
```

## 🎯 **What Makes This Different**

### **vs. Previous "Multi-Agent" System:**
- ❌ **Before**: Hardcoded if/else statements
- ✅ **Now**: Real AI models with LangGraph orchestration

### **vs. Simple RAG:**
- ❌ **Before**: Single response generation
- ✅ **Now**: Multi-step agent workflow with safety checks

### **vs. Basic Chat:**
- ❌ **Before**: No document retrieval
- ✅ **Now**: Haystack RAG with Supabase pgvector storage

## 🎉 **Ready for Production!**

Your SmartProBono MVP now has:
- ✅ **Real multi-agent AI system** with LangGraph
- ✅ **Professional RAG pipeline** with Haystack
- ✅ **Scalable database** with Supabase pgvector
- ✅ **Safety and compliance** features
- ✅ **Production-ready API** with FastAPI

**This is a REAL, production-ready multi-agent legal AI system!** 🚀

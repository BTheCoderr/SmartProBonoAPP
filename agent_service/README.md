# SmartProBono LangGraph Service

This is the LangGraph orchestration service for SmartProBono, providing AI-powered case intake and processing workflows.

## 🏗️ Architecture

```
Frontend (React) → LangGraph Service (FastAPI) → Supabase
```

- **Frontend**: React app with LangGraph integration
- **LangGraph Service**: FastAPI + LangGraph for AI orchestration
- **Supabase**: Database and authentication

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd agent_service
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export SUPABASE_URL="https://ewtcvsohdgkthuyajyyk.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Run the Service

```bash
uvicorn agent_service.main:app --reload --port 8010
```

### 4. Test the Service

```bash
# Health check
curl http://localhost:8010/health

# Test intake
curl -X POST http://localhost:8010/intake/run \
  -H "Content-Type: application/json" \
  -d '{"user_id": null, "full_text": "I need help with a landlord dispute", "meta": {}}'
```

## 📊 Database Setup

Run the SQL in `../sql/langgraph_tables.sql` in your Supabase SQL editor:

```sql
-- Creates case_intakes and lawyer_profiles tables
-- Includes sample lawyer data for testing
```

## 🧩 Current Features

### ✅ Implemented
- **Case Intake**: Accept raw legal case descriptions
- **AI Summarization**: Extract key legal details using GPT-4o-mini
- **Supabase Integration**: Store intake records and summaries
- **Health Monitoring**: Service health check endpoint

### 🚧 Next Steps
- **Lawyer Matching**: AI-powered case assignment
- **Conflict Checking**: Automated conflict detection
- **Human Review**: Pause for admin approval
- **Notifications**: Email/SMS case updates
- **Streaming**: Real-time progress updates

## 🔧 API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{"ok": true}
```

### `POST /intake/run`
Process a legal case intake.

**Request:**
```json
{
  "user_id": "optional-user-id",
  "full_text": "I need help with a landlord dispute...",
  "meta": {"source": "webform"}
}
```

**Response:**
```json
{
  "result": {
    "intake_id": "uuid",
    "user_id": "optional-user-id",
    "raw_text": "original text",
    "summary": "AI-generated summary",
    "status": "summarized",
    "meta": {"source": "webform"}
  }
}
```

## 🎯 Frontend Integration

The React frontend includes:

- **LangGraph API Client** (`frontend/src/api/langgraph.ts`)
- **Intake Component** (`frontend/src/components/LangGraphIntake.js`)
- **Demo Page** (`frontend/src/pages/LangGraphDemo.js`)

Access the demo at: `http://localhost:3002/langgraph-demo`

## 🔍 Development

### Project Structure
```
agent_service/
├── main.py              # FastAPI app
├── graph.py             # LangGraph workflow
├── schemas.py           # Pydantic models
├── supabase_client.py   # Supabase integration
├── nodes/
│   ├── types.py         # Node context
│   └── summarize.py     # AI summarization
└── requirements.txt     # Dependencies
```

### Adding New Nodes

1. Create a new node in `nodes/`
2. Add it to the graph in `graph.py`
3. Define the workflow edges
4. Test with the API

### Environment Variables

Required:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key for database access
- `OPENAI_API_KEY`: OpenAI API key for LLM calls

## 🐛 Troubleshooting

### Service Won't Start
- Check environment variables are set
- Verify Supabase credentials
- Check OpenAI API key is valid

### Database Errors
- Ensure Supabase tables are created
- Check service role key permissions
- Verify network connectivity

### AI Errors
- Check OpenAI API key and credits
- Verify model availability
- Check rate limits

## 📝 Logs

- Service logs: `langgraph.log`
- Installation logs: `langgraph_install.log`
- Check logs for detailed error information

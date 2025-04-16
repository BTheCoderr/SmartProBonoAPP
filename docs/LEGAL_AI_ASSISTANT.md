# SmartProBono AI Legal Assistant

## Overview

The SmartProBono AI Legal Assistant provides automated legal information and guidance across various legal domains and jurisdictions. It leverages fine-tuned language models and vector databases to deliver accurate, citation-backed legal information to users.

## Features

- **Domain-specific legal expertise**: Specialized knowledge in tenant rights, employment law, immigration, family law, and more
- **Jurisdiction-specific responses**: Tailored legal information for different states and federal jurisdictions
- **Citation support**: References to relevant case law, statutes, and regulations
- **Resource recommendations**: Links to appropriate legal aid organizations and resources
- **Multi-model support**: Different AI models optimized for various legal domains
- **Legal document analysis**: Ability to extract key information from uploaded legal documents

## Architecture

The Legal AI Assistant consists of several integrated components:

1. **Data Collection Pipeline**: Gathers and processes legal information from various sources
2. **Model Fine-tuning System**: Specializes AI models for legal domains and jurisdictions
3. **Vector Database**: Stores embeddings of legal information for efficient retrieval
4. **API Layer**: Provides endpoints for interacting with the assistant
5. **Frontend Interface**: User-friendly chat interface for asking legal questions

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL database
- Node.js 16+ (for frontend)
- [Ollama](https://ollama.ai/) for local model inference (optional)

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```
4. Setup the database:
   ```
   cd backend
   python init_db.py
   ```
5. Run the automated setup for the Legal AI Assistant:
   ```
   cd backend
   ./setup_legal_ai.sh
   ```

### Configuration

The Legal AI Assistant can be configured by modifying the following files:

- `backend/config/ai_config.py`: Model configuration and routing
- `backend/ai/config/local_config.json`: Vector database and model paths
- `.env`: API keys and database connection information

## Usage Instructions

### API Endpoints

The Legal AI Assistant exposes the following endpoints:

#### Chat

`POST /api/legal/chat`

Request body:
```json
{
  "message": "What are my rights as a tenant in California?",
  "jurisdiction": "california",
  "model_id": "tenant-rights-model" // Optional
}
```

Response:
```json
{
  "response": "As a tenant in California, you have several important rights...",
  "citations": [
    {
      "text": "Cal. Civ. Code § 1941.1",
      "type": "Statute",
      "jurisdiction": "California"
    }
  ],
  "domain": "tenant_rights",
  "jurisdiction": "california",
  "resources": [
    {
      "name": "California Department of Consumer Affairs",
      "url": "https://www.dca.ca.gov/publications/landlordbook/",
      "description": "Guide to landlord-tenant law in California"
    }
  ],
  "model_used": "tenant-rights-model",
  "timestamp": "2023-04-12T15:30:22.123Z"
}
```

#### Analyze Query

`POST /api/legal/analyze`

Request body:
```json
{
  "query": "What are my rights as a tenant in California?"
}
```

Response:
```json
{
  "domain": "tenant_rights",
  "domain_confidence": 0.85,
  "jurisdiction": "california",
  "citations": [],
  "timestamp": "2023-04-12T15:30:22.123Z"
}
```

#### Get Legal Domains

`GET /api/legal/domains`

Response:
```json
{
  "domains": [
    {
      "id": "tenant_rights",
      "name": "Tenant Rights",
      "keywords": ["tenant", "landlord", "lease", "rent", "eviction"],
      "description": "Laws governing landlord-tenant relationships",
      "hasSpecializedModel": true
    },
    // Other domains...
  ],
  "jurisdictions": ["federal", "california", "new_york", "texas", "..."]
}
```

#### Get Jurisdictions

`GET /api/legal/jurisdictions`

Response:
```json
{
  "jurisdictions": [
    {
      "id": "federal",
      "name": "Federal",
      "hasSpecificLaws": true
    },
    {
      "id": "california",
      "name": "California",
      "hasSpecificLaws": true
    },
    // Other jurisdictions...
  ],
  "default": "federal"
}
```

#### Get Models

`GET /api/legal/models`

Response:
```json
{
  "models": [
    {
      "id": "general-legal-assistant",
      "name": "General Legal Assistant",
      "description": "Balanced model for all legal questions"
    },
    {
      "id": "tenant-rights-legal-assistant",
      "name": "Tenant Rights Specialist",
      "description": "Specialized for housing and tenant rights"
    },
    // Other models...
  ],
  "default": "general-legal-assistant"
}
```

#### Get Citation Details

`GET /api/legal/citations/<citation_id>`

Response:
```json
{
  "id": "cal-civ-1941",
  "text": "Cal. Civ. Code § 1941.1",
  "type": "Statute",
  "jurisdiction": "California",
  "title": "Civil Code",
  "section": "1941.1",
  "content": "...",
  "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1941.1",
  "year": "2020"
}
```

#### Get Legal Resources

`GET /api/legal/resources?domain=tenant_rights&jurisdiction=california`

Response:
```json
{
  "resources": [
    {
      "name": "California Department of Consumer Affairs",
      "url": "https://www.dca.ca.gov/publications/landlordbook/",
      "description": "Guide to landlord-tenant law in California"
    },
    // Other resources...
  ]
}
```

#### Specialized Chat

`POST /api/legal/chat/specialized`

Request body:
```json
{
  "message": "What is the eviction process in California?",
  "domain": "tenant_rights",
  "jurisdiction": "california"
}
```

Response: Similar to the standard chat endpoint

### Frontend Integration

The Legal Assistant can be accessed through:

- `/chat/legal-assistant` - Dedicated Legal AI Assistant page

## Extending the Legal AI Assistant

### Adding New Legal Domains

1. Update `backend/services/legal_assistant_service.py` to add the new domain and keywords
2. Collect domain-specific data using `scripts/collect_legal_data.py`
3. Fine-tune a domain-specific model using `scripts/fine_tune_legal_model.py`
4. Build a vector database for the domain using `scripts/build_vector_db.py`
5. Update the `legal_domains` dictionary in `legal_assistant_service.py`

### Adding New Jurisdictions

1. Add the jurisdiction to the `jurisdictions` list in `legal_assistant_service.py`
2. Collect jurisdiction-specific data using `scripts/collect_legal_data.py`
3. Fine-tune jurisdiction-specific models using `scripts/fine_tune_legal_model.py`
4. Update vector database indexes to include jurisdiction filtering

## Testing

Test the Legal AI Assistant using the test script:

```
python backend/test_legal_ai.py
```

For specific message testing:

```
python backend/test_legal_ai.py --message "What are my rights as a tenant in California?" --jurisdiction california --verbose
```

## Future Enhancements

Planned enhancements for the Legal AI Assistant include:

- Multi-language support for legal assistance
- Document generation based on user inputs
- Interactive decision trees for common legal processes
- Integration with case management system
- Real-time updates from legal databases
- Voice interface for accessibility

## Troubleshooting

Common issues and solutions:

- **Slow response times**: Check vector database indexing or consider using a smaller, faster model
- **Missing citations**: Ensure vector database has been populated with relevant legal sources
- **Incorrect jurisdiction detection**: Add more jurisdiction-specific keywords to improve detection
- **Model loading errors**: Verify Ollama is running or API keys are correctly configured

For further assistance, please contact the development team. 

# Ollama Model Configuration
# Generated automatically based on available models

OLLAMA_BEST_MODEL = "gemma2:2b"
OLLAMA_CHAT_MODEL = "gemma2:2b"
OLLAMA_LEGAL_MODEL = "gemma2:2b"
OLLAMA_RESEARCH_MODEL = "gemma2:2b"

# Model mapping for different tasks
MODEL_TASK_MAPPING = {
    "chat": "gemma2:2b",
    "legal_qa": "gemma2:2b",
    "document_drafting": "gemma2:2b",
    "legal_research": "gemma2:2b",
    "default": "gemma2:2b"
}

# Disable paid services
OPENAI_ENABLED = False
CLAUDE_ENABLED = False
ANTHROPIC_ENABLED = False

# Enable Ollama
OLLAMA_ENABLED = True
OLLAMA_URL = "http://localhost:11434"

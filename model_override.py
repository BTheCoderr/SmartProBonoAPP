
# Model Override for Free Models
import os

# Force Ollama usage
os.environ['AI_MODEL'] = 'tinyllama:1.1b'
os.environ['OLLAMA_ENABLED'] = 'true'
os.environ['OPENAI_ENABLED'] = 'false'

# Override model selection
def get_best_model(task_type="chat"):
    """Get the best available free model for the task"""
    if task_type in ["chat", "legal_qa", "rights_explanation"]:
        return "tinyllama:1.1b"
    elif task_type in ["document_drafting", "contract_generation"]:
        return "gemma2:2b"
    elif task_type in ["legal_research", "case_analysis"]:
        return "qwen2.5:0.5b"
    else:
        return "tinyllama:1.1b"  # Default to fastest

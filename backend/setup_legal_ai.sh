#!/bin/bash
# Setup script for SmartProBono Legal AI Enhancements
# This script automates the process of collecting data, training models,
# building vector databases, and setting up the enhanced legal assistant.

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create necessary directories
echo "Creating directories..."
mkdir -p ai/data/{raw,processed,training,domains}
mkdir -p ai/vector_db
mkdir -p ai/training/{models,eval}

# Make scripts executable
chmod +x scripts/collect_legal_data.py
chmod +x scripts/fine_tune_legal_model.py
chmod +x scripts/build_vector_db.py

# Install required packages if not already installed
echo "Checking requirements..."
pip install -r requirements.txt

# Step 1: Collect legal data
echo "Step 1: Collecting legal data..."
python scripts/collect_legal_data.py \
  --jurisdictions federal california new_york texas \
  --case-limit 100

# Step 2: Fine-tune models on select domains
echo "Step 2: Fine-tuning legal models..."
python scripts/fine_tune_legal_model.py \
  --domains tenant_rights employment general \
  --jurisdictions federal california \
  --data-dir ai/data

# Step 3: Build vector databases
echo "Step 3: Building vector databases..."
python scripts/build_vector_db.py \
  --domains tenant_rights employment general \
  --jurisdictions federal california \
  --data-dir ai/data \
  --vector-db-dir ai/vector_db

# Step 4: Configure Ollama with the fine-tuned models
echo "Step 4: Setting up Ollama models..."
OLLAMA_MODELS_DIR="$SCRIPT_DIR/ai/training/models"

if command -v ollama &> /dev/null; then
    echo "Ollama found, setting up models..."
    
    # Check if any models were created
    if [ -d "$OLLAMA_MODELS_DIR" ]; then
        # Find all Modelfiles and create models
        find "$OLLAMA_MODELS_DIR" -name "Modelfile" | while read -r modelfile; do
            model_dir=$(dirname "$modelfile")
            model_name=$(basename "$model_dir")
            echo "Creating Ollama model: legal-$model_name"
            ollama create "legal-$model_name" -f "$modelfile"
        done
    else
        echo "No model directories found in $OLLAMA_MODELS_DIR"
    fi
else
    echo "Ollama not found. Please install Ollama and manually import the models from:"
    echo "$OLLAMA_MODELS_DIR"
fi

# Step 5: Update local configuration
echo "Step 5: Updating configuration..."
cat > ai/config/local_config.json << EOL
{
    "vector_db_path": "${SCRIPT_DIR}/ai/vector_db",
    "fine_tuned_models": {
        "tenant_rights": "tenant-rights-legal-assistant",
        "employment": "employment-legal-assistant",
        "general": "general-legal-assistant"
    },
    "default_model": "general-legal-assistant",
    "enable_citations": true,
    "default_jurisdiction": "federal"
}
EOL

echo ""
echo "Legal AI enhancement setup complete!"
echo ""
echo "Next steps:"
echo "1. Restart the backend server"
echo "2. Make sure Ollama is running (if using local models)"
echo "3. Test the enhanced legal assistant endpoints"
echo ""
echo "You can test the system with:"
echo "curl -X POST http://localhost:5000/api/legal/chat -H 'Content-Type: application/json' -d '{\"message\":\"What are my tenant rights in California?\", \"jurisdiction\":\"california\"}'"
echo "" 
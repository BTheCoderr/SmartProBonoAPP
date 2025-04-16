#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Build vector database for all domains and jurisdictions
echo "Building vector database..."
python3 backend/scripts/build_vector_db.py --domain all --jurisdiction all

# Fine-tune models for specific legal domains
echo "Fine-tuning models for immigration law..."
python3 backend/scripts/fine_tune_legal_model.py --domain immigration

echo "Fine-tuning models for tenant rights..."
python3 backend/scripts/fine_tune_legal_model.py --domain tenant_rights

echo "Fine-tuning models for employment law..."
python3 backend/scripts/fine_tune_legal_model.py --domain employment

echo "Legal AI setup complete!" 
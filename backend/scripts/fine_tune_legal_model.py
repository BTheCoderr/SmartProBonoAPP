#!/usr/bin/env python3
"""
Fine-tune Legal Models Script for SmartProBono

This script performs fine-tuning of LLM models on legal datasets with
domain specialization and jurisdiction awareness.
"""

import os
import json
import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.model_trainer import LegalModelTrainer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("legal_model_training.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define constants
DEFAULT_DATA_DIR = Path(__file__).parent.parent / 'ai' / 'data'
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / 'ai' / 'training' / 'models'
DEFAULT_EVAL_DIR = Path(__file__).parent.parent / 'ai' / 'training' / 'eval'

# Define domain-specific training configurations
TRAINING_CONFIGS = {
    'tenant_rights': {
        'description': 'A legal assistant specialized in tenant rights and housing law',
        'base_model': 'mistralai/Mistral-7B-Instruct-v0.3',
        'epochs': 3,
        'learning_rate': 2e-5,
        'batch_size': 4,
        'lora_r': 8,
        'lora_alpha': 16,
        'lora_dropout': 0.05,
        'model_output_name': 'tenant-rights-legal-assistant'
    },
    'employment': {
        'description': 'A legal assistant specialized in employment law and workplace rights',
        'base_model': 'mistralai/Mistral-7B-Instruct-v0.3',
        'epochs': 3,
        'learning_rate': 2e-5,
        'batch_size': 4,
        'lora_r': 8,
        'lora_alpha': 16,
        'lora_dropout': 0.05,
        'model_output_name': 'employment-legal-assistant'
    },
    'family_law': {
        'description': 'A legal assistant specialized in family law matters',
        'base_model': 'meta-llama/Llama-3-8b-chat',
        'epochs': 3,
        'learning_rate': 2e-5,
        'batch_size': 4,
        'lora_r': 8,
        'lora_alpha': 16,
        'lora_dropout': 0.05,
        'model_output_name': 'family-law-assistant'
    },
    'immigration': {
        'description': 'A legal assistant specialized in immigration law and procedures',
        'base_model': 'meta-llama/Llama-3-8b-chat',
        'epochs': 3,
        'learning_rate': 2e-5,
        'batch_size': 4,
        'lora_r': 8,
        'lora_alpha': 16,
        'lora_dropout': 0.05,
        'model_output_name': 'immigration-legal-assistant'
    },
    'consumer_protection': {
        'description': 'A legal assistant specialized in consumer rights and protection laws',
        'base_model': 'deepseek-ai/deepseek-coder-6.7b-instruct',
        'epochs': 3,
        'learning_rate': 2e-5,
        'batch_size': 4,
        'lora_r': 8,
        'lora_alpha': 16,
        'lora_dropout': 0.05,
        'model_output_name': 'consumer-rights-assistant'
    },
    'civil_rights': {
        'description': 'A legal assistant specialized in civil rights and liberties',
        'base_model': 'tiiuae/falcon-7b-instruct',
        'epochs': 3,
        'learning_rate': 2e-5,
        'batch_size': 4,
        'lora_r': 8,
        'lora_alpha': 16,
        'lora_dropout': 0.05,
        'model_output_name': 'civil-rights-assistant'
    },
    'general': {
        'description': 'A general legal assistant with broad knowledge across domains',
        'base_model': 'mistralai/Mistral-7B-Instruct-v0.3',
        'epochs': 3,
        'learning_rate': 2e-5,
        'batch_size': 4,
        'lora_r': 8,
        'lora_alpha': 16,
        'lora_dropout': 0.05,
        'model_output_name': 'general-legal-assistant'
    }
}

# Define jurisdiction filters
JURISDICTIONS = [
    'federal',
    'california',
    'new_york',
    'texas',
    'florida',
    'illinois'
]

def filter_dataset_by_domain(input_file: Path, domain: str, output_file: Path):
    """
    Filter a dataset file to contain only entries related to a specific domain.
    
    Args:
        input_file: Path to the input JSONL dataset
        domain: Domain to filter for
        output_file: Path to save the filtered dataset
    
    Returns:
        Count of filtered entries
    """
    logger.info(f"Filtering dataset for domain: {domain}")
    
    domain_keywords = {
        'tenant_rights': ['tenant', 'landlord', 'lease', 'rent', 'eviction', 'housing', 'apartment'],
        'employment': ['employee', 'employer', 'work', 'job', 'labor', 'paycheck', 'discrimination', 'termination'],
        'family_law': ['divorce', 'custody', 'child support', 'alimony', 'adoption', 'marriage'],
        'immigration': ['visa', 'citizenship', 'green card', 'deportation', 'asylum', 'immigration'],
        'consumer_protection': ['consumer', 'product', 'warranty', 'fraud', 'debt', 'refund', 'contract'],
        'civil_rights': ['discrimination', 'rights', 'equal', 'constitutional', 'liberty', 'freedom'],
        'general': []  # Empty list means no filtering
    }
    
    selected_keywords = domain_keywords.get(domain, [])
    
    if not selected_keywords:
        # If no keywords (general domain), just copy the file
        if input_file != output_file:
            import shutil
            shutil.copy(input_file, output_file)
        
        # Count lines in the file
        with open(input_file, 'r') as f:
            count = sum(1 for _ in f)
        
        return count
    
    # Filter the dataset
    filtered_count = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line)
            question = data.get('question', '').lower()
            answer = data.get('answer', '').lower()
            
            # Check if any keyword matches
            if any(keyword.lower() in question or keyword.lower() in answer 
                   for keyword in selected_keywords):
                outfile.write(line)
                filtered_count += 1
    
    logger.info(f"Filtered {filtered_count} entries for domain: {domain}")
    return filtered_count

def filter_dataset_by_jurisdiction(input_file: Path, jurisdiction: str, output_file: Path):
    """
    Filter a dataset file to contain only entries related to a specific jurisdiction.
    
    Args:
        input_file: Path to the input JSONL dataset
        jurisdiction: Jurisdiction to filter for
        output_file: Path to save the filtered dataset
    
    Returns:
        Count of filtered entries
    """
    logger.info(f"Filtering dataset for jurisdiction: {jurisdiction}")
    
    filtered_count = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line)
            question = data.get('question', '').lower()
            answer = data.get('answer', '').lower()
            
            # Check if jurisdiction is mentioned
            if (jurisdiction.lower() in question or 
                jurisdiction.lower() in answer or
                jurisdiction.replace('_', ' ').lower() in question or
                jurisdiction.replace('_', ' ').lower() in answer):
                outfile.write(line)
                filtered_count += 1
    
    logger.info(f"Filtered {filtered_count} entries for jurisdiction: {jurisdiction}")
    return filtered_count

def prepare_domain_datasets(data_dir: Path, domains: List[str], jurisdictions: Optional[List[str]] = None):
    """
    Prepare domain-specific and jurisdiction-specific datasets for training.
    
    Args:
        data_dir: Base data directory
        domains: List of domains to prepare datasets for
        jurisdictions: Optional list of jurisdictions to filter by
    
    Returns:
        Dictionary mapping domain names to dataset file paths
    """
    logger.info(f"Preparing domain-specific datasets for: {', '.join(domains)}")
    
    training_dir = data_dir / 'training'
    domain_dir = data_dir / 'domains'
    domain_dir.mkdir(exist_ok=True)
    
    # Find all training files
    main_dataset = training_dir / 'legal_qa_pairs.jsonl'
    if not main_dataset.exists():
        logger.error(f"Main dataset not found: {main_dataset}")
        return {}
    
    domain_datasets = {}
    
    # Process each domain
    for domain in domains:
        logger.info(f"Processing domain: {domain}")
        
        # Create domain-specific dataset
        domain_file = domain_dir / f"{domain}_qa_pairs.jsonl"
        count = filter_dataset_by_domain(main_dataset, domain, domain_file)
        
        if count == 0:
            logger.warning(f"No entries found for domain: {domain}")
            continue
        
        domain_datasets[domain] = str(domain_file)
        
        # If jurisdictions are specified, create jurisdiction-specific datasets for this domain
        if jurisdictions:
            for jurisdiction in jurisdictions:
                jurisdiction_file = domain_dir / f"{domain}_{jurisdiction}_qa_pairs.jsonl"
                jur_count = filter_dataset_by_jurisdiction(domain_file, jurisdiction, jurisdiction_file)
                
                if jur_count > 0:
                    domain_datasets[f"{domain}_{jurisdiction}"] = str(jurisdiction_file)
                    logger.info(f"Created dataset for {domain} in {jurisdiction}: {jur_count} entries")
    
    return domain_datasets

def fine_tune_model(config: Dict[str, Any], dataset_file: str, output_dir: Path):
    """
    Fine-tune a model according to the given configuration.
    
    Args:
        config: Training configuration
        dataset_file: Path to the dataset file
        output_dir: Output directory for the model
    
    Returns:
        True if successful, False otherwise
    """
    model_name = config['model_output_name']
    logger.info(f"Fine-tuning model: {model_name} using {config['base_model']}")
    
    # Create model trainer
    trainer = LegalModelTrainer(
        base_model=config['base_model'],
        output_dir=str(output_dir),
        use_lora=True,
        use_8bit=True
    )
    
    # Train the model
    success = trainer.train(
        dataset_file=dataset_file,
        output_name=model_name,
        epochs=config['epochs'],
        batch_size=config['batch_size'],
        learning_rate=config['learning_rate']
    )
    
    if success:
        logger.info(f"Successfully fine-tuned model: {model_name}")
        
        # Export model for Ollama
        ollama_export_success = trainer.export_model_for_ollama(
            model_dir=str(output_dir / model_name),
            ollama_model_name=f"legal-{model_name}",
            description=config['description']
        )
        
        if ollama_export_success:
            logger.info(f"Successfully exported model for Ollama: legal-{model_name}")
        else:
            logger.error(f"Failed to export model for Ollama: {model_name}")
    else:
        logger.error(f"Failed to fine-tune model: {model_name}")
    
    return success

def main():
    """Main function to run the fine-tuning process."""
    parser = argparse.ArgumentParser(description='Fine-tune legal models')
    parser.add_argument('--data-dir', type=str, default=str(DEFAULT_DATA_DIR),
                        help='Directory containing training data')
    parser.add_argument('--output-dir', type=str, default=str(DEFAULT_OUTPUT_DIR),
                        help='Output directory for fine-tuned models')
    parser.add_argument('--domains', type=str, nargs='+', 
                        default=['tenant_rights', 'employment', 'general'],
                        help='Legal domains to fine-tune models for')
    parser.add_argument('--jurisdictions', type=str, nargs='+',
                        default=['federal', 'california'],
                        help='Jurisdictions to include in fine-tuning')
    parser.add_argument('--skip-dataset-prep', action='store_true',
                        help='Skip dataset preparation step (use existing)')
    parser.add_argument('--eval-only', action='store_true',
                        help='Only evaluate existing models, no training')
    
    args = parser.parse_args()
    
    # Convert to Path objects
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Prepare domain-specific datasets
    domain_datasets = {}
    if not args.skip_dataset_prep:
        domain_datasets = prepare_domain_datasets(data_dir, args.domains, args.jurisdictions)
        if not domain_datasets:
            logger.error("Failed to prepare domain datasets")
            return
    else:
        # Use existing datasets
        domain_dir = data_dir / 'domains'
        for domain in args.domains:
            domain_file = domain_dir / f"{domain}_qa_pairs.jsonl"
            if domain_file.exists():
                domain_datasets[domain] = str(domain_file)
                
                # Check jurisdiction files too
                for jurisdiction in args.jurisdictions:
                    jur_file = domain_dir / f"{domain}_{jurisdiction}_qa_pairs.jsonl"
                    if jur_file.exists():
                        domain_datasets[f"{domain}_{jurisdiction}"] = str(jur_file)
    
    # Print available datasets
    logger.info(f"Available domain datasets: {list(domain_datasets.keys())}")
    
    # Skip training if eval only
    if args.eval_only:
        logger.info("Skipping training (eval-only mode)")
        return
    
    # Fine-tune models for each domain
    successful_models = []
    failed_models = []
    
    for domain_key, dataset_file in domain_datasets.items():
        # Get the base domain (without jurisdiction)
        base_domain = domain_key.split('_')[0]
        
        # Get training config for this domain
        if base_domain in TRAINING_CONFIGS:
            config = TRAINING_CONFIGS[base_domain].copy()
        else:
            logger.warning(f"No training config found for domain: {base_domain}, using general config")
            config = TRAINING_CONFIGS['general'].copy()
        
        # Customize model name for jurisdiction-specific models
        if '_' in domain_key and domain_key != base_domain:
            jurisdiction = '_'.join(domain_key.split('_')[1:])
            config['model_output_name'] = f"{config['model_output_name']}-{jurisdiction}"
            config['description'] += f" with specialization in {jurisdiction.replace('_', ' ')} law"
        
        # Fine-tune the model
        success = fine_tune_model(config, dataset_file, output_dir)
        
        if success:
            successful_models.append(config['model_output_name'])
        else:
            failed_models.append(config['model_output_name'])
    
    # Print summary
    logger.info("\n===== FINE-TUNING COMPLETE =====")
    logger.info(f"Successfully trained models: {len(successful_models)}")
    for model in successful_models:
        logger.info(f"  - {model}")
    
    if failed_models:
        logger.info(f"Failed models: {len(failed_models)}")
        for model in failed_models:
            logger.info(f"  - {model}")

if __name__ == "__main__":
    main() 
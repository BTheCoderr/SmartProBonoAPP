"""
Model Trainer for SmartProBono
This module handles the fine-tuning of LLM models on legal datasets.
"""

import os
import json
import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import Dataset, load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalModelTrainer:
    """
    Handles fine-tuning LLM models on legal datasets for improved performance
    on legal tasks such as question answering, document drafting, and legal analysis.
    """
    
    def __init__(self, 
                 base_model: str = 'mistralai/Mistral-7B-Instruct-v0.3',
                 output_dir: str = 'ai/training/models',
                 data_dir: str = 'ai/data/training',
                 use_lora: bool = True,
                 use_8bit: bool = True):
        """
        Initialize the model trainer.
        
        Args:
            base_model: Name or path of the base model to fine-tune
            output_dir: Directory to save fine-tuned models
            data_dir: Directory containing training data
            use_lora: Whether to use LoRA (parameter-efficient fine-tuning)
            use_8bit: Whether to use 8-bit quantization
        """
        self.base_model = base_model
        self.output_dir = output_dir
        self.data_dir = data_dir
        self.use_lora = use_lora
        self.use_8bit = use_8bit
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Model and tokenizer will be loaded during training
        self.model = None
        self.tokenizer = None
        
    def prepare_qa_dataset(self, input_file: str) -> Dataset:
        """
        Prepare a question-answering dataset for training.
        
        Args:
            input_file: Path to input JSON Lines file with QA pairs
            
        Returns:
            HuggingFace dataset
        """
        logger.info(f"Preparing QA dataset from {input_file}")
        
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return None
            
        try:
            # Load data
            df = pd.read_json(input_file, lines=True)
            
            # Format as instruction dataset
            formatted_data = []
            
            for _, row in df.iterrows():
                question = row['question']
                answer = row['answer']
                jurisdiction = row.get('jurisdiction', '')
                
                # Instruction format for instruction-tuned models
                instruction = f"Answer the following legal question"
                if jurisdiction:
                    instruction += f" for {jurisdiction}"
                instruction += ":\n\n"
                
                # Format as a full prompt
                prompt = f"{instruction}{question}"
                
                formatted_data.append({
                    'instruction': instruction,
                    'input': question,
                    'output': answer,
                    'text': f"{prompt}\n\n{answer}",
                    'jurisdiction': jurisdiction
                })
                
            # Create Dataset object
            dataset = Dataset.from_pandas(pd.DataFrame(formatted_data))
            
            logger.info(f"Created dataset with {len(dataset)} examples")
            return dataset
            
        except Exception as e:
            logger.error(f"Error preparing dataset: {str(e)}")
            return None
            
    def load_model_and_tokenizer(self):
        """
        Load the base model and tokenizer.
        """
        logger.info(f"Loading model and tokenizer for {self.base_model}")
        
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.base_model,
                use_fast=True
            )
            
            # Set padding token if not already set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            # Load model with quantization if enabled
            if self.use_8bit:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.base_model,
                    load_in_8bit=True,
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.base_model,
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
                
            # Apply LoRA configuration if enabled
            if self.use_lora:
                # Prepare model for PEFT training
                if self.use_8bit:
                    self.model = prepare_model_for_kbit_training(self.model)
                    
                # Configure LoRA
                lora_config = LoraConfig(
                    r=16,                  # Rank of the update matrices
                    lora_alpha=32,         # Parameter for scaling
                    lora_dropout=0.05,     # Dropout probability
                    bias="none",           # Don't train bias terms
                    task_type="CAUSAL_LM"  # Task type for LLM
                )
                
                # Apply LoRA to model
                self.model = get_peft_model(self.model, lora_config)
                
            logger.info("Successfully loaded model and tokenizer")
            
        except Exception as e:
            logger.error(f"Error loading model and tokenizer: {str(e)}")
            self.model = None
            self.tokenizer = None
            
    def preprocess_dataset(self, dataset: Dataset) -> Dataset:
        """
        Preprocess the dataset for training (tokenize).
        
        Args:
            dataset: Input dataset
            
        Returns:
            Tokenized dataset
        """
        logger.info("Preprocessing dataset")
        
        if self.tokenizer is None:
            logger.error("Tokenizer not loaded")
            return None
            
        try:
            # Define preprocessing function
            def tokenize_function(examples):
                # Tokenize the text
                tokenized = self.tokenizer(
                    examples['text'],
                    padding="max_length",
                    truncation=True,
                    max_length=2048  # Adjust based on model and compute resources
                )
                
                # Create labels (same as input_ids for causal LM)
                tokenized['labels'] = tokenized['input_ids'].copy()
                
                return tokenized
                
            # Tokenize the dataset
            tokenized_dataset = dataset.map(
                tokenize_function,
                batched=True,
                remove_columns=['instruction', 'input', 'output', 'text', 'jurisdiction']
            )
            
            logger.info("Successfully preprocessed dataset")
            return tokenized_dataset
            
        except Exception as e:
            logger.error(f"Error preprocessing dataset: {str(e)}")
            return None
            
    def train(self, 
             dataset_file: str,
             output_name: str = 'legal-finetuned',
             epochs: int = 3,
             batch_size: int = 4,
             learning_rate: float = 2e-5,
             warmup_steps: int = 500,
             save_steps: int = 1000) -> bool:
        """
        Fine-tune the model on a legal dataset.
        
        Args:
            dataset_file: Path to the dataset file
            output_name: Name for the output model
            epochs: Number of training epochs
            batch_size: Batch size for training
            learning_rate: Learning rate
            warmup_steps: Number of warmup steps
            save_steps: Save checkpoint every N steps
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Starting training with {self.base_model}")
        
        # Prepare dataset
        dataset = self.prepare_qa_dataset(dataset_file)
        if dataset is None:
            return False
            
        # Split dataset into train and validation
        train_test_split = dataset.train_test_split(test_size=0.1)
        train_dataset = train_test_split['train']
        val_dataset = train_test_split['test']
        
        # Load model and tokenizer
        self.load_model_and_tokenizer()
        if self.model is None or self.tokenizer is None:
            return False
            
        # Preprocess dataset
        train_dataset = self.preprocess_dataset(train_dataset)
        val_dataset = self.preprocess_dataset(val_dataset)
        if train_dataset is None or val_dataset is None:
            return False
            
        # Set up training arguments
        output_path = os.path.join(self.output_dir, output_name)
        training_args = TrainingArguments(
            output_dir=output_path,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=warmup_steps,
            learning_rate=learning_rate,
            logging_dir=os.path.join(output_path, 'logs'),
            logging_steps=100,
            save_strategy="steps",
            save_steps=save_steps,
            evaluation_strategy="steps",
            eval_steps=save_steps,
            load_best_model_at_end=True,
            save_total_limit=3,
            fp16=True,
            gradient_accumulation_steps=4,
            gradient_checkpointing=True,
            report_to="none"  # Disable wandb, etc.
        )
        
        # Create data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # Causal language modeling
        )
        
        # Create trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator
        )
        
        try:
            # Start training
            logger.info("Starting training")
            trainer.train()
            
            # Save model
            logger.info(f"Saving model to {output_path}")
            trainer.save_model(output_path)
            self.tokenizer.save_pretrained(output_path)
            
            # Log training complete
            logger.info(f"Training complete, model saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            return False
            
    def export_model_for_ollama(self, 
                               model_dir: str,
                               ollama_model_name: str = 'legal-mistral',
                               description: str = 'Legal fine-tuned model') -> bool:
        """
        Export a trained model for use with Ollama.
        
        Args:
            model_dir: Directory containing the model
            ollama_model_name: Name to use in Ollama
            description: Model description
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Exporting model from {model_dir} for Ollama")
        
        if not os.path.exists(model_dir):
            logger.error(f"Model directory not found: {model_dir}")
            return False
            
        try:
            # Create Modelfile
            modelfile_content = f"""
FROM {self.base_model}
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 50
PARAMETER num_ctx 4096
PARAMETER stop "Human:"
PARAMETER stop "Assistant:"
PARAMETER stop "</s>"

# Description of the model
SYSTEM """

            modelfile_content += description
            
            # Write Modelfile
            modelfile_path = os.path.join(model_dir, 'Modelfile')
            with open(modelfile_path, 'w', encoding='utf-8') as f:
                f.write(modelfile_content)
                
            # Log command to run
            logger.info(f"Modelfile created at {modelfile_path}")
            logger.info(f"To create Ollama model, run: ollama create {ollama_model_name} -f {modelfile_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error exporting model for Ollama: {str(e)}")
            return False
            
# Load environment-specific configuration (if needed)
def get_training_config():
    """Get configuration for model training from environment variables."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    return {
        'base_model': os.environ.get('FINETUNE_BASE_MODEL', 'mistralai/Mistral-7B-Instruct-v0.3'),
        'output_dir': os.environ.get('FINETUNE_OUTPUT_DIR', 'ai/training/models'),
        'data_dir': os.environ.get('FINETUNE_DATA_DIR', 'ai/data/training'),
        'use_lora': os.environ.get('FINETUNE_USE_LORA', 'true').lower() == 'true',
        'use_8bit': os.environ.get('FINETUNE_USE_8BIT', 'true').lower() == 'true'
    }

# Example usage
if __name__ == "__main__":
    config = get_training_config()
    
    # Initialize trainer
    trainer = LegalModelTrainer(**config)
    
    # Train model
    dataset_file = os.path.join(config['data_dir'], 'legal_qa_pairs.jsonl')
    trainer.train(
        dataset_file=dataset_file,
        output_name='legal-mistral-lora',
        epochs=1,  # For demonstration; increase for better results
        batch_size=4,
        learning_rate=2e-5
    )
    
    # Export model for Ollama
    trainer.export_model_for_ollama(
        model_dir=os.path.join(config['output_dir'], 'legal-mistral-lora'),
        ollama_model_name='legal-mistral',
        description='Legal fine-tuned Mistral model with knowledge of cases and statutes'
    ) 
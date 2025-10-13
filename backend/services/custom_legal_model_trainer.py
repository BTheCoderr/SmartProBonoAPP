"""
Custom Legal Model Trainer
Allows training/fine-tuning legal models on your specific data
"""

import logging
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import Dataset

logger = logging.getLogger(__name__)

class CustomLegalModelTrainer:
    """Service for training custom legal models on your data"""
    
    def __init__(self):
        self.base_model = "isaacus/open-australian-legal-gpt2"  # Start with legal base
        self.custom_models_dir = "models/custom_legal"
        self.training_data_dir = "training_data/legal"
        
        # Create directories if they don't exist
        os.makedirs(self.custom_models_dir, exist_ok=True)
        os.makedirs(self.training_data_dir, exist_ok=True)
        
        logger.info("Custom Legal Model Trainer initialized")
    
    def prepare_training_data(self, 
                            conversations: List[Dict[str, str]],
                            output_file: str = None) -> str:
        """
        Prepare conversational training data from your legal consultations
        
        Args:
            conversations: List of dicts with 'question' and 'answer' keys
            output_file: Optional custom output filename
            
        Returns:
            Path to prepared training data file
        """
        try:
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"{self.training_data_dir}/training_data_{timestamp}.json"
            
            # Format data for training
            training_examples = []
            for conv in conversations:
                # Create a formatted training example
                text = f"Legal Question: {conv['question']}\nLegal Answer: {conv['answer']}"
                training_examples.append({"text": text})
            
            # Save to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(training_examples, f, indent=2)
            
            logger.info(f"Prepared {len(training_examples)} training examples")
            logger.info(f"Saved to: {output_file}")
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            raise
    
    def train_custom_model(self,
                          training_data_path: str,
                          model_name: str = "smartprobono-legal-v1",
                          epochs: int = 3,
                          batch_size: int = 4,
                          learning_rate: float = 2e-5,
                          max_length: int = 512) -> Dict[str, Any]:
        """
        Train a custom legal model on your data
        
        Args:
            training_data_path: Path to training data JSON file
            model_name: Name for your custom model
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate for training
            max_length: Maximum sequence length
            
        Returns:
            Dict with training results and model path
        """
        try:
            logger.info(f"Starting training for {model_name}")
            logger.info(f"Base model: {self.base_model}")
            
            # Load training data
            with open(training_data_path, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
            
            logger.info(f"Loaded {len(training_data)} training examples")
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(self.base_model)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            model = AutoModelForCausalLM.from_pretrained(
                self.base_model,
                torch_dtype=torch.float32
            )
            
            # Prepare dataset
            dataset = Dataset.from_list(training_data)
            
            def tokenize_function(examples):
                return tokenizer(
                    examples["text"],
                    truncation=True,
                    max_length=max_length,
                    padding="max_length"
                )
            
            tokenized_dataset = dataset.map(
                tokenize_function,
                batched=True,
                remove_columns=dataset.column_names
            )
            
            # Set up training arguments
            output_dir = f"{self.custom_models_dir}/{model_name}"
            training_args = TrainingArguments(
                output_dir=output_dir,
                num_train_epochs=epochs,
                per_device_train_batch_size=batch_size,
                learning_rate=learning_rate,
                save_steps=100,
                save_total_limit=2,
                logging_steps=10,
                report_to="none",  # Disable wandb/tensorboard
                push_to_hub=False,
                fp16=False,  # CPU training
            )
            
            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=tokenizer,
                mlm=False
            )
            
            # Create trainer
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=tokenized_dataset,
                data_collator=data_collator,
            )
            
            # Train!
            logger.info("Starting training...")
            train_result = trainer.train()
            
            # Save the model
            trainer.save_model(output_dir)
            tokenizer.save_pretrained(output_dir)
            
            logger.info(f"Training complete! Model saved to: {output_dir}")
            
            return {
                "success": True,
                "model_name": model_name,
                "model_path": output_dir,
                "training_examples": len(training_data),
                "epochs": epochs,
                "final_loss": float(train_result.training_loss),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def load_custom_model(self, model_name: str) -> tuple:
        """
        Load a custom trained model
        
        Args:
            model_name: Name of the custom model
            
        Returns:
            Tuple of (tokenizer, model)
        """
        try:
            model_path = f"{self.custom_models_dir}/{model_name}"
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found: {model_path}")
            
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float32
            )
            
            logger.info(f"Loaded custom model: {model_name}")
            
            return tokenizer, model
            
        except Exception as e:
            logger.error(f"Error loading custom model: {e}")
            raise
    
    def list_custom_models(self) -> List[Dict[str, Any]]:
        """List all available custom trained models"""
        try:
            if not os.path.exists(self.custom_models_dir):
                return []
            
            models = []
            for model_name in os.listdir(self.custom_models_dir):
                model_path = os.path.join(self.custom_models_dir, model_name)
                if os.path.isdir(model_path):
                    # Check if it's a valid model directory
                    if os.path.exists(os.path.join(model_path, "config.json")):
                        models.append({
                            "name": model_name,
                            "path": model_path,
                            "modified": datetime.fromtimestamp(
                                os.path.getmtime(model_path)
                            ).isoformat()
                        })
            
            return models
            
        except Exception as e:
            logger.error(f"Error listing custom models: {e}")
            return []
    
    def export_conversations_for_training(self, 
                                         db_path: str = None) -> str:
        """
        Export conversations from database for training
        
        Args:
            db_path: Path to database (if not using default)
            
        Returns:
            Path to exported training data
        """
        try:
            # TODO: Connect to your actual database
            # For now, create a sample dataset
            
            sample_conversations = [
                {
                    "question": "What is a lease agreement?",
                    "answer": "A lease agreement is a legal contract between a landlord and tenant that outlines the terms of renting property, including rent amount, duration, and responsibilities of each party."
                },
                {
                    "question": "How do I respond to a lawsuit?",
                    "answer": "To respond to a lawsuit, you must file an answer with the court within the time specified in the summons (usually 20-30 days). Your answer should address each claim made against you."
                },
                {
                    "question": "What are my rights during a police stop?",
                    "answer": "During a police stop, you have the right to remain silent, the right to refuse searches without a warrant, and the right to an attorney. Always remain calm and respectful."
                }
            ]
            
            return self.prepare_training_data(sample_conversations)
            
        except Exception as e:
            logger.error(f"Error exporting conversations: {e}")
            raise

# Global instance
custom_legal_trainer = CustomLegalModelTrainer()


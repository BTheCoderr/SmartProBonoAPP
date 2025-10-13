"""
Model Configuration Service
Manages AI model generation parameters for quality tuning
"""

import logging
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelConfigService:
    """Service for managing model configuration and performance tuning"""
    
    def __init__(self):
        self.config_file = "config/model_config.json"
        self.default_config = {
            "generation_params": {
                "max_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 50,
                "repetition_penalty": 1.2,
                "no_repeat_ngram_size": 2
            },
            "task_specific_params": {
                "legal": {
                    "temperature": 0.6,
                    "max_tokens": 200,
                    "top_p": 0.85
                },
                "research": {
                    "temperature": 0.4,
                    "max_tokens": 300,
                    "top_p": 0.9
                },
                "chat": {
                    "temperature": 0.8,
                    "max_tokens": 150,
                    "top_p": 0.95
                },
                "draft": {
                    "temperature": 0.5,
                    "max_tokens": 400,
                    "top_p": 0.85
                }
            },
            "quality_settings": {
                "enable_grammar_check": True,
                "enable_legal_terminology": True,
                "citation_style": "bluebook",
                "verbosity_level": "balanced"  # terse, balanced, detailed
            }
        }
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        # Load or create config
        self.config = self.load_config()
        
        logger.info("Model Configuration Service initialized")
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info("Loaded model configuration from file")
                return config
            else:
                # Save default config
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info("Saved model configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get_generation_params(self, task_type: str = "chat", **overrides) -> Dict[str, Any]:
        """
        Get generation parameters for a specific task type
        
        Args:
            task_type: Type of task (legal, research, chat, draft)
            **overrides: Any parameter overrides
            
        Returns:
            Dict of generation parameters
        """
        # Start with default params
        params = self.config.get("generation_params", {}).copy()
        
        # Apply task-specific params
        task_params = self.config.get("task_specific_params", {}).get(task_type, {})
        params.update(task_params)
        
        # Apply overrides
        params.update(overrides)
        
        return params
    
    def update_generation_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update generation parameters
        
        Args:
            params: New parameter values
            
        Returns:
            Updated configuration
        """
        try:
            self.config["generation_params"].update(params)
            self.save_config(self.config)
            
            return {
                "success": True,
                "updated_params": params,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error updating params: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_task_params(self, task_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update parameters for a specific task type
        
        Args:
            task_type: Type of task
            params: New parameter values
            
        Returns:
            Updated configuration
        """
        try:
            if task_type not in self.config.get("task_specific_params", {}):
                self.config["task_specific_params"][task_type] = {}
            
            self.config["task_specific_params"][task_type].update(params)
            self.save_config(self.config)
            
            return {
                "success": True,
                "task_type": task_type,
                "updated_params": params,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error updating task params: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_quality_settings(self) -> Dict[str, Any]:
        """Get quality settings"""
        return self.config.get("quality_settings", {})
    
    def update_quality_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update quality settings
        
        Args:
            settings: New quality settings
            
        Returns:
            Updated configuration
        """
        try:
            self.config["quality_settings"].update(settings)
            self.save_config(self.config)
            
            return {
                "success": True,
                "updated_settings": settings,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error updating quality settings: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def reset_to_defaults(self) -> Dict[str, Any]:
        """Reset configuration to defaults"""
        try:
            self.config = self.default_config.copy()
            self.save_config(self.config)
            
            return {
                "success": True,
                "message": "Configuration reset to defaults",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error resetting config: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_full_config(self) -> Dict[str, Any]:
        """Get complete configuration"""
        return self.config.copy()
    
    def get_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get predefined quality presets"""
        return {
            "fast": {
                "max_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9,
                "description": "Fast responses, shorter outputs"
            },
            "balanced": {
                "max_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "description": "Balanced speed and quality"
            },
            "quality": {
                "max_tokens": 250,
                "temperature": 0.5,
                "top_p": 0.85,
                "description": "Higher quality, more detailed responses"
            },
            "creative": {
                "max_tokens": 200,
                "temperature": 0.9,
                "top_p": 0.95,
                "description": "More creative and varied responses"
            },
            "precise": {
                "max_tokens": 150,
                "temperature": 0.3,
                "top_p": 0.8,
                "description": "Focused and precise responses"
            }
        }
    
    def apply_preset(self, preset_name: str) -> Dict[str, Any]:
        """
        Apply a predefined preset
        
        Args:
            preset_name: Name of preset to apply
            
        Returns:
            Updated configuration
        """
        try:
            presets = self.get_presets()
            
            if preset_name not in presets:
                return {
                    "success": False,
                    "error": f"Preset '{preset_name}' not found"
                }
            
            preset = presets[preset_name].copy()
            preset.pop('description', None)  # Remove description
            
            self.config["generation_params"].update(preset)
            self.save_config(self.config)
            
            return {
                "success": True,
                "preset": preset_name,
                "applied_params": preset,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error applying preset: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Global instance
model_config_service = ModelConfigService()


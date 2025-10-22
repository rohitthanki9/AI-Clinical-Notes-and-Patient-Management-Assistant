"""
Configuration Manager for AI Clinical Notes Assistant
Handles application settings, paths, and configuration
"""
import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.assets_dir = self.base_dir / "assets"
        self.prompts_dir = self.base_dir / "prompts"

        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)
        self.prompts_dir.mkdir(exist_ok=True)

        # Configuration file
        self.config_file = self.data_dir / "config.json"
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "ollama_url": "http://localhost:11434",
            "ollama_model": "llama3",
            "whisper_model": "base",
            "db_path": str(self.data_dir / "patients.db"),
            "encryption_key_path": str(self.data_dir / ".encryption.key"),
            "theme": "flatly",
            "clinic_name": "Medical Clinic",
            "audio_sample_rate": 16000,
            "audio_channels": 1
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")

        return default_config

    def save_config(self):
        """Save current configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set configuration value and save"""
        self.config[key] = value
        self.save_config()

    def get_prompt_template(self, template_name):
        """Load a prompt template"""
        template_path = self.prompts_dir / f"{template_name}_template.txt"
        if template_path.exists():
            with open(template_path, 'r') as f:
                return f.read()
        return None

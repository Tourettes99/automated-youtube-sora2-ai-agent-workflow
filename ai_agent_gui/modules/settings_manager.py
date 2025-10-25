"""
Settings Manager
Handles persistent storage of application settings
"""

import json
from pathlib import Path
from typing import Any, Dict


class SettingsManager:
    """Manages application settings with JSON persistence"""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = Path(__file__).parent.parent / settings_file
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from JSON file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.get_default_settings()
        return self.get_default_settings()
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default settings"""
        return {
            "openai_api_key": "",
            "gemini_api_key": "",
            "youtube_api_key": "",
            "youtube_client_secrets": "client_secrets.json",
            "agent_instructions": "Generate engaging, high-quality videos suitable for YouTube. Focus on trending topics, educational content, or entertainment. Keep videos between 30-60 seconds.",
            "video_duration": 30,
            "video_resolution": "1080p",
            "weekly_schedule": {},
            "output_directory": "output",
            "temp_directory": "temp"
        }
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def update(self, settings_dict: Dict[str, Any]):
        """Update multiple settings at once"""
        self.settings.update(settings_dict)
        self.save_settings()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings"""
        return self.settings.copy()


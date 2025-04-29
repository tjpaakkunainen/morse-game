import json
import os
import copy

class ConfigManager:
    def __init__(self, config_path='resources/config.json'):

    # Default configuration values, should not be modified
        self.default_config = {
            "general": {
                "input_timeout_ms": 1000
            },
            "receive_game": {
                "character_count_placeholder": 3
            }
        }

        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                return self.merge_with_defaults(user_config)
            except (json.JSONDecodeError, IOError):
                return copy.deepcopy(self.default_config)
        else:
            config = copy.deepcopy(self.default_config)
            self.config = config
            self.save_config()
            return config

    def save_config(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)

    def get_config_value(self, path, default=None):
        """Get a config value using dot notation path (e.g., 'receive_game.character_count')"""
        keys = path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_config_value(self, path, value):
        """Set a config value using dot notation path (e.g., 'receive_game.character_count')"""
        keys = path.split('.')
        config = self.config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value
        self.save_config()
    
    def get_input_timeout(self):
        return self.get_config_value('general.input_timeout_ms', 1000)
    
    def set_input_timeout(self, timeout_ms):
        timeout_ms = max(100, min(5000, timeout_ms))
        self.set_config_value('general.input_timeout_ms', timeout_ms)

    def reset_to_default(self, section=None):
        """Reset entire config or a specific section to default values"""
        defaults = copy.deepcopy(self.default_config)
        if section:
            if section in defaults:
                self.config[section] = defaults[section]
            else:
                raise ValueError(f"Section '{section}' not found in default config.")
        else:
            self.config = defaults
        self.save_config()
        return True

    def merge_with_defaults(self, user_config):
        result = copy.deepcopy(self.default_config)

        def merge_dict(default, user):
            for key, value in user.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    merge_dict(default[key], value)
                else:
                    default[key] = value
                    
        merge_dict(result, user_config)
        return result

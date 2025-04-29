# tests/unit/test_config_manager.py
import pytest
import json
import os
import tempfile
from src.config_manager import ConfigManager

@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
        temp_file.write(b'{}')  # Start with empty JSON
        temp_path = temp_file.name
    
    yield temp_path  # Provide the path to the test
    
    # Clean up after the test
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def config_with_custom_data(temp_config_file):
    """Create a config file with custom test data."""
    test_data = {
        "general": {
            "input_timeout_ms": 2000
        },
        "receive_game": {
            "character_count_placeholder": 5
        },
        "custom_section": {
            "test_value": "hello"
        }
    }
    
    with open(temp_config_file, 'w') as f:
        json.dump(test_data, f)
    
    return temp_config_file

def test_init_with_default_config(temp_config_file):
    """Test that ConfigManager initializes with default config when file is empty."""
    config_manager = ConfigManager(temp_config_file)
    
    assert config_manager.get_config_value('general.input_timeout_ms') == 1000
    assert config_manager.get_config_value('receive_game.character_count_placeholder') == 3

def test_load_existing_config(config_with_custom_data):
    """Test loading an existing config file."""
    config_manager = ConfigManager(config_with_custom_data)
    
    assert config_manager.get_config_value('general.input_timeout_ms') == 2000
    assert config_manager.get_config_value('receive_game.character_count_placeholder') == 5
    assert config_manager.get_config_value('custom_section.test_value') == "hello"

def test_save_config(temp_config_file):
    """Test saving changes to the config file."""
    # Create and modify config
    config_manager = ConfigManager(temp_config_file)
    config_manager.set_config_value('new_section.new_value', 42)
    
    # Load config again from file and verify changes were saved
    new_config_manager = ConfigManager(temp_config_file)
    assert new_config_manager.get_config_value('new_section.new_value') == 42

def test_get_nonexistent_value(temp_config_file):
    """Test getting a value that doesn't exist."""
    config_manager = ConfigManager(temp_config_file)
    
    # Should return the default value
    assert config_manager.get_config_value('nonexistent.path', 'default') == 'default'
    
    # Should return None if no default specified
    assert config_manager.get_config_value('nonexistent.path') is None

def test_set_nested_value(temp_config_file):
    """Test setting a deeply nested value."""
    config_manager = ConfigManager(temp_config_file)
    
    # Set a deeply nested value
    config_manager.set_config_value('a.b.c.d.e', 'nested')
    
    # Verify it was set correctly
    assert config_manager.get_config_value('a.b.c.d.e') == 'nested'
    
    # Load config again to verify it was saved
    new_config_manager = ConfigManager(temp_config_file)
    assert new_config_manager.get_config_value('a.b.c.d.e') == 'nested'

def test_convenience_methods(temp_config_file):
    """Test the convenience methods for common settings."""
    config_manager = ConfigManager(temp_config_file)
    
    # Test getter
    assert config_manager.get_input_timeout() == 1000
    
    # Test setter
    config_manager.set_input_timeout(1500)
    assert config_manager.get_input_timeout() == 1500
    
    # Test validation in setter
    config_manager.set_input_timeout(10000)  # Should be capped at 5000
    assert config_manager.get_input_timeout() == 5000
    
    config_manager.set_input_timeout(50)  # Should be increased to 100
    assert config_manager.get_input_timeout() == 100

def test_reset_to_default_section(config_with_custom_data):
    """Test resetting a specific section to default."""
    config_manager = ConfigManager(config_with_custom_data)
    
    # Verify custom values are loaded
    assert config_manager.get_config_value('general.input_timeout_ms') == 2000
    
    # Reset just the general section
    config_manager.reset_to_default('general')
    
    # Verify general is reset but other sections remain
    assert config_manager.get_config_value('general.input_timeout_ms') == 1000
    assert config_manager.get_config_value('receive_game.character_count_placeholder') == 5
    assert config_manager.get_config_value('custom_section.test_value') == "hello"

def test_reset_to_default_all(config_with_custom_data):
    """Test resetting the entire config to default."""
    config_manager = ConfigManager(config_with_custom_data)
    
    # Reset entire config
    config_manager.reset_to_default()
    
    # Verify everything is reset
    assert config_manager.get_config_value('general.input_timeout_ms') == 1000
    assert config_manager.get_config_value('receive_game.character_count_placeholder') == 3
    assert config_manager.get_config_value('custom_section.test_value') is None

def test_reset_nonexistent_section(temp_config_file):
    """Test resetting a section that doesn't exist in defaults."""
    config_manager = ConfigManager(temp_config_file)
    
    # Should raise ValueError
    with pytest.raises(ValueError):
        config_manager.reset_to_default('nonexistent_section')

def test_merge_with_defaults():
    """Test the merge_with_defaults method."""
    config_manager = ConfigManager()
    
    user_config = {
        "general": {
            "new_setting": "value"
        },
        "new_section": {
            "key": "value"
        }
    }
    
    merged = config_manager.merge_with_defaults(user_config)
    
    # Verify default values remain
    assert merged['general']['input_timeout_ms'] == 1000
    assert merged['receive_game']['character_count_placeholder'] == 3
    
    # Verify user values are merged
    assert merged['general']['new_setting'] == "value"
    assert merged['new_section']['key'] == "value"

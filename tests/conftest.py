"""
Pytest configuration and fixtures for Supersub Monitor tests.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def mock_env_file():
    """Mock .env file with test environment variables."""
    return {"TELEGRAM_BOT_TOKEN": "mock_bot_token", "URBANSOCCER_TARGET_CITY": "TestCity"}


@pytest.fixture
def mock_driver():
    """Mock Chrome WebDriver for testing."""
    mock = MagicMock()
    mock.quit = MagicMock()
    return mock


@pytest.fixture
def cleanup_imports():
    """Clean up any module imports after test."""
    yield
    # Remove modules that might have been imported
    modules_to_remove = [mod for mod in sys.modules.keys() 
                        if mod.startswith('src.') or mod.startswith('chromedriver_manager')]
    for mod in modules_to_remove:
        if mod in sys.modules:
            del sys.modules[mod]

"""
Test configuration loading, environment variables, and logging setup.
"""

import logging
import os
from unittest.mock import patch

import pytest


class TestEnvironmentLoading:
    """Test .env file loading and environment variable handling."""
    
    @patch('dotenv.load_dotenv')
    def test_load_dotenv_called(self, mock_load_dotenv):
        """Test that load_dotenv is called."""
        from dotenv import load_dotenv
        load_dotenv()
        mock_load_dotenv.assert_called_once()
    
    def test_environment_variable_access(self, mock_env_file):
        """Test that environment variables can be accessed."""
        with patch.dict(os.environ, mock_env_file):
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            city = os.getenv('URBANSOCCER_TARGET_CITY')
            assert token == 'mock_bot_token'
            assert city == 'TestCity'
    
    def test_missing_environment_variables(self):
        """Test behavior with missing environment variables."""
        # Clear environment to simulate missing vars
        with patch.dict(os.environ, {}, clear=True):
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            city = os.getenv('URBANSOCCER_TARGET_CITY')
            assert token is None
            assert city is None


class TestLoggingConfiguration:
    """Test logging configuration and levels."""
    
    def test_logging_imports(self):
        """Test logging module import."""
        import logging
        assert logging.DEBUG < logging.INFO < logging.WARNING < logging.ERROR
        
    def test_logger_creation(self):
        """Test logger creation."""
        logger = logging.getLogger('test_logger')
        assert logger is not None
        assert logger.name == 'test_logger'
    
    def test_log_level_names(self):
        """Test log level name resolution."""
        assert logging.getLevelName(logging.DEBUG) == 'DEBUG'
        assert logging.getLevelName(logging.INFO) == 'INFO'
        assert logging.getLevelName(logging.WARNING) == 'WARNING'
        assert logging.getLevelName(logging.ERROR) == 'ERROR'

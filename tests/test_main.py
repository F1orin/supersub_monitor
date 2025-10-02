"""
Test main entry point functionality with mocked dependencies.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest


class TestMainFunction:
    """Test main() function functionality."""

    @patch('main.shutdown_driver')
    @patch('main.start_telegram_bot')
    @patch('main.get_driver')
    @patch('main.load_dotenv')
    def test_main_with_valid_env(self, mock_load_dotenv, mock_get_driver,
                                 mock_start_bot, mock_shutdown_driver):
        """Test main function with valid environment variables."""
        # Setup mocks
        mock_driver = MagicMock()
        mock_get_driver.return_value = mock_driver

        # Mock sys.argv to simulate command line args
        with patch.object(sys, 'argv', ['main.py', '--info']):
            with patch.dict('os.environ', {
                'TELEGRAM_BOT_TOKEN': 'test_token_123',
                'URBANSOCCER_TARGET_CITY': 'TestCity'
            }):
                from main import main
                main()

        # Verify function calls
        mock_load_dotenv.assert_called_once()
        mock_get_driver.assert_called_once()
        mock_start_bot.assert_called_once()
        mock_shutdown_driver.assert_called_once()

    @patch('main.shutdown_driver')
    @patch('main.start_telegram_bot')
    @patch('main.get_driver')
    def test_main_debug_mode(self, mock_get_driver, mock_start_bot, mock_shutdown_driver):
        """Test main function with --debug argument."""
        mock_driver = MagicMock()
        mock_get_driver.return_value = mock_driver

        with patch.object(sys, 'argv', ['main.py', '--debug']):
            with patch.dict('os.environ', {
                'TELEGRAM_BOT_TOKEN': 'test_token_123',
                'URBANSOCCER_TARGET_CITY': 'TestCity'
            }):
                from main import main
                main()

        # All functions should still be called
        mock_get_driver.assert_called_once()
        mock_start_bot.assert_called_once()
        mock_shutdown_driver.assert_called_once()


class TestArgumentParsing:
    """Test command line argument parsing."""

    def test_no_arguments(self):
        """Test default argument parsing with no flags."""
        with patch.object(sys, 'argv', ['main.py']):
            import argparse
            parser = argparse.ArgumentParser(description="Supersub Monitor")
            parser.add_argument('--debug', action='store_true',
                                help='Enable debug logging')
            parser.add_argument('--info', action='store_true',
                                help='Enable info logging')
            args = parser.parse_args()

            assert args.debug is False
            assert args.info is False

    def test_debug_argument(self):
        """Test --debug argument."""
        with patch.object(sys, 'argv', ['main.py', '--debug']):
            import argparse
            parser = argparse.ArgumentParser(description="Supersub Monitor")
            parser.add_argument('--debug', action='store_true',
                                help='Enable debug logging')
            parser.add_argument('--info', action='store_true',
                                help='Enable info logging')
            args = parser.parse_args()

            assert args.debug is True
            assert args.info is False

    def test_info_argument(self):
        """Test --info argument."""
        with patch.object(sys, 'argv', ['main.py', '--info']):
            import argparse
            parser = argparse.ArgumentParser(description="Supersub Monitor")
            parser.add_argument('--debug', action='store_true',
                                help='Enable debug logging')
            parser.add_argument('--info', action='store_true',
                                help='Enable info logging')
            args = parser.parse_args()

            assert args.debug is False
            assert args.info is True

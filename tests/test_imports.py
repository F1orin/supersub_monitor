"""
Test that all required dependencies and modules can be imported successfully.
"""

import pytest


class TestDependencies:
    """Test external dependencies."""

    def test_selenium_import(self):
        """Test Selenium imports."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        assert webdriver is not None
        assert Options is not None
        assert Service is not None

    def test_telegram_import(self):
        """Test python-telegram-bot imports."""
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        assert Update is not None
        assert Application is not None
        assert CommandHandler is not None
        assert ContextTypes is not None

    def test_webdriver_manager_import(self):
        """Test webdriver-manager import."""
        from webdriver_manager.chrome import ChromeDriverManager
        assert ChromeDriverManager is not None

    def test_other_dependencies(self):
        """Test other required dependencies."""
        from dotenv import load_dotenv
        import logging
        import argparse
        from datetime import time, timezone
        from functools import partial

        assert load_dotenv is not None
        assert logging is not None
        assert argparse is not None
        assert time is not None
        assert timezone is not None
        assert partial is not None


class TestInternalModules:
    """Test internal module imports."""

    def test_main_module(self):
        """Test main module import."""
        import main
        assert main is not None
        assert hasattr(main, 'main')

    def test_chromedriver_manager(self):
        """Test chromedriver_manager module import."""
        import chromedriver_manager
        assert chromedriver_manager is not None
        assert hasattr(chromedriver_manager, 'get_driver')
        assert hasattr(chromedriver_manager, 'shutdown_driver')

    def test_supersub_module(self):
        """Test supersub module import."""
        import supersub
        assert supersub is not None
        assert hasattr(supersub, 'parse_available_matches')

    def test_telegram_handler(self):
        """Test telegram_handler module import."""
        import telegram_handler
        assert telegram_handler is not None
        assert hasattr(telegram_handler, 'start_telegram_bot')

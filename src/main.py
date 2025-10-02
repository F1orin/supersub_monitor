"""
Supersub Monitor entry point.
Handles argument parsing, logging setup, environment loading, and starts the Telegram bot.
"""

import argparse
import logging
import os

from dotenv import load_dotenv

from chromedriver_manager import get_driver, shutdown_driver
from telegram_handler import start_telegram_bot

log = logging.getLogger(__name__)


def main():
    """
    Parse command-line arguments, configure logging, load environment variables,
    and start the Telegram bot.
    """
    parser = argparse.ArgumentParser(description="Supersub Monitor")
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--info', action='store_true',
                        help='Enable info logging')
    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    elif args.info:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    logging.basicConfig(level=log_level)

    log.info("Logging configured at %s", logging.getLevelName(log_level))

    log.debug("Loading .env file")
    load_dotenv()
    log.debug("Environment variables loaded")

    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    city = os.getenv('URBANSOCCER_TARGET_CITY')

    log.info(f'Target city set to {city}')

    try:
        chrome_driver = get_driver()
    except Exception:
        log.exception("Failed to initialize ChromeDriver")
        return

    log.info("ChromeDriver ready")
    try:
        log.info(f'Starting Telegram bot for city {city}')
        start_telegram_bot(telegram_token, city, chrome_driver)
    finally:
        log.info("Shutting down ChromeDriver")
        shutdown_driver()


if __name__ == "__main__":
    main()

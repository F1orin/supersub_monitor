"""
Supersub Monitor entry point.
Handles argument parsing, logging setup, environment loading, and starts the Telegram bot.
"""

import argparse
import logging
import os

from dotenv import load_dotenv
from telegram_handler import start_telegram_bot


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

    load_dotenv()

    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    city = os.getenv('URBANSOCCER_TARGET_CITY')

    if not telegram_token or not city:
        logging.error("Required environment variables are missing.")
        return

    start_telegram_bot(telegram_token, city)


if __name__ == "__main__":
    main()

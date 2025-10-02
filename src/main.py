import logging
import os
import argparse
from dotenv import load_dotenv
from telegram_handler import start_telegram_bot


def main():
    parser = argparse.ArgumentParser(description="Supersub Monitor")
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    load_dotenv()

    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    city = os.getenv('URBANSOCCER_TARGET_CITY')

    start_telegram_bot(telegram_token, city)


if __name__ == "__main__":
    main()

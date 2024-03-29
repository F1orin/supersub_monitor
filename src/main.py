import logging
import os
from dotenv import load_dotenv
from telegram_handler import start_telegram_bot


def main():
    logging.basicConfig(level=logging.WARNING)

    load_dotenv()

    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    city = os.getenv('URBANSOCCER_TARGET_CITY')

    start_telegram_bot(telegram_token, city)


if __name__ == "__main__":
    main()

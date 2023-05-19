import os
import requests
import supersub
from dotenv import load_dotenv


def prepare_message(matches: list) -> str:
    result = str(matches)
    return result


def main():
    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    matches = supersub.parse_available_matches()

    message = prepare_message(matches)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    print(requests.get(url).json())


if __name__ == "__main__":
    main()

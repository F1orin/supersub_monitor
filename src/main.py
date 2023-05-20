import os
import requests
import supersub
from dotenv import load_dotenv


def prepare_message(city: str, matches: list) -> str:
    "[['20/05 - Sam.', '(2)'],\
    ['21/05 - Dim.', '(1)'],\
    ['22/05 - Lun.', '(0)'],\
    ['23/05 - Mar.', '(0)'],\
    ['24/05 - Mer.', '(1)']]"
    result = f'These are the matches available in {city}:\n'
    for day_data in matches:
        line = f'{day_data[0]} - {day_data[1].strip("()")}\n'
        result += line
    return result


def main():
    load_dotenv()
    CITY = os.getenv('URBANSOCCER_TARGET_CITY')
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    matches = supersub.parse_available_matches(CITY)

    message = prepare_message(CITY, matches)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    print(requests.get(url).json())


if __name__ == "__main__":
    main()

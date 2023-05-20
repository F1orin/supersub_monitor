import os
import supersub
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


load_dotenv()
CITY = os.getenv('URBANSOCCER_TARGET_CITY')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def prepare_message(city: str, matches: list) -> str:
    result = f'These are the matches available in {city}:\n'
    for day_data in matches:
        line = f'{day_data[0]} - {day_data[1].strip("()")}\n'
        result += line
    return result


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check for available Supersub matches when the command /check is issued."""
    matches = supersub.parse_available_matches(CITY)
    message = prepare_message(CITY, matches)
    await update.message.reply_text(message)


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("check", check_command))
    application.run_polling()


if __name__ == "__main__":
    main()

import logging
import selenium
import supersub
from functools import partial
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

log = logging.getLogger(__name__)


def prepare_message(city: str, matches: list) -> str:
    result = f'These are the matches available in {city}:\n'
    for day_data in matches:
        line = f'{day_data[0]} - {day_data[1].strip("()")}\n'
        result += line
    return result


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Type /check to search for matches.')


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE, city: str) -> None:
    """Check for available Supersub matches when the command /check is issued."""
    telegram_message = await update.message.reply_text('Checking available matches...')
    try:
        matches_data = supersub.parse_available_matches(city)
        matches_message = prepare_message(city, matches_data)
        await telegram_message.edit_text(matches_message)
    except supersub.UnsupportedOSError as os_error:
        log.exception('Unsupported OS exceptions occured')
        await telegram_message.edit_text(f'Error occured: {os_error}')
    except selenium.common.exceptions.WebDriverException as driver_error:
        log.exception('Selenium WebDriverException occured')
        await telegram_message.edit_text(f'Selenium WebDriverException occured')


def start_telegram_bot(token, city):
    application = Application.builder().token(token).build()

    check_command_with_city = partial(check_command, city=city)

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("check", check_command_with_city))

    application.run_polling()

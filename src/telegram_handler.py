import supersub
from functools import partial
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


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
    matches = supersub.parse_available_matches(city)
    message = prepare_message(city, matches)
    await update.message.reply_text(message)


def start_telegram_bot(token, city):
    application = Application.builder().token(token).build()

    check_command_with_city = partial(check_command, city=city)

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("check", check_command_with_city))

    application.run_polling()

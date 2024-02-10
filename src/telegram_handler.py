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
    help_message = 'Type /check to search for matches.\n\n' \
        + 'Type /subscribe to receive updates every day.\n\n' \
        + 'Type /unsubscribe to stop receiving regular updates.\n\n'
    await update.message.reply_text(help_message)


async def check_command(city: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def send_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text='qwe')


def remove_jobs(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove all jobs from the queue."""
    current_jobs = context.job_queue.jobs()
    for job in current_jobs:
        job.schedule_removal()


async def start_recurring_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start regular checks for SuperSub matches."""
    chat_id = update.effective_message.chat_id
    context.job_queue.run_repeating(send_message, interval=5, chat_id=chat_id)
    text = 'Recurring updates started'
    await update.message.reply_text(text)


async def stop_recurring_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop regular checks for SuperSub matches."""
    remove_jobs(context)
    text = 'Recurring updates stopped'
    await update.message.reply_text(text)


def start_telegram_bot(token, city):
    application = Application.builder().token(token).build()

    check_command_with_city = partial(check_command, city=city)

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("check", check_command_with_city))
    application.add_handler(CommandHandler(
        "subscribe", start_recurring_command))
    application.add_handler(CommandHandler(
        "unsubscribe", stop_recurring_command))

    application.run_polling()

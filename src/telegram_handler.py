import logging
import selenium
import supersub
from functools import partial
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time, timezone

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


def remove_jobs(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove all jobs from the queue."""
    current_jobs = context.job_queue.jobs()
    for job in current_jobs:
        job.schedule_removal()


async def start_recurring_command(update: Update, context: ContextTypes.DEFAULT_TYPE, city: str) -> None:
    """
    Start regular checks for SuperSub matches.
    The checks run every day at 12:00 and 19:00 UTC.
    """
    chat_id = update.effective_message.chat_id

    async def check_wrapper(context: ContextTypes.DEFAULT_TYPE):
        await check_command(update, context, city)

    # 13h check
    time_day = time(hour=12, tzinfo=timezone.utc)
    context.job_queue.run_daily(
        check_wrapper, time=time_day, chat_id=chat_id, name=f'day_{chat_id}')
    text_day = 'Recurring updates for 13h00 started'
    await update.message.reply_text(text_day)

    # 20h check
    time_evening = time(hour=19, tzinfo=timezone.utc)
    context.job_queue.run_daily(
        check_wrapper, time=time_evening, chat_id=chat_id, name=f'evening_{chat_id}')
    text_evening = 'Recurring updates for 20h00 started'
    await update.message.reply_text(text_evening)


async def stop_recurring_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop regular checks for SuperSub matches."""
    remove_jobs(context)
    text = 'Recurring updates stopped'
    await update.message.reply_text(text)


def start_telegram_bot(token, city):
    application = Application.builder().token(token).build()

    check_command_with_city = partial(
        check_command, city=city)
    start_recurring_command_with_city = partial(
        start_recurring_command, city=city)

    application.add_handler(CommandHandler(
        "help", help_command))
    application.add_handler(CommandHandler(
        "check", check_command_with_city))
    application.add_handler(CommandHandler(
        "subscribe", start_recurring_command_with_city))
    application.add_handler(CommandHandler(
        "unsubscribe", stop_recurring_command))

    application.run_polling()

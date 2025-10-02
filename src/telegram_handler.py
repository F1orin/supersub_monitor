"""
Telegram handler for Supersub Monitor bot.
Handles Telegram commands, scheduling, and message formatting.
"""

import logging

from datetime import time, timezone
from functools import partial
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

import supersub


log = logging.getLogger(__name__)


def prepare_message(city: str, matches: list) -> str:
    """
    Format the list of matches for a given city into a message string.
    """
    lines = [f'These are the matches available in {city}:']
    for day_data in matches:
        lines.append(f'{day_data[0]} - {day_data[1].strip("()")}')
    return '\n'.join(lines) + '\n'


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send a message when the command /help is issued.
    """
    help_message = (
        'Type /check to search for matches.\n\n'
        'Type /subscribe to receive updates every day.\n\n'
        'Type /unsubscribe to stop receiving regular updates.\n\n'
    )
    await update.message.reply_text(help_message)


async def check_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    city: str,
    driver: WebDriver,
) -> None:
    """
    Check for available Supersub matches when the command /check is issued.
    """
    telegram_message = await update.message.reply_text('Checking available matches...')
    try:
        matches_data = supersub.parse_available_matches(driver, city)
        matches_message = prepare_message(city, matches_data)
        await telegram_message.edit_text(matches_message)
    except WebDriverException:
        log.exception('Selenium WebDriverException occurred')
        await telegram_message.edit_text('Selenium WebDriverException occurred')


def remove_jobs(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Remove all jobs from the queue.
    """
    current_jobs = context.job_queue.jobs()
    for job in current_jobs:
        job.schedule_removal()


async def start_recurring_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    city: str,
    driver: WebDriver,
) -> None:
    """
    Start regular checks for SuperSub matches.
    The checks run every day at 12:00 and 19:00 UTC.
    """
    chat_id = update.effective_message.chat_id

    async def check_wrapper(context: ContextTypes.DEFAULT_TYPE) -> None:
        await check_command(update, context, city, driver)

    # 13h check
    time_day = time(hour=12, tzinfo=timezone.utc)
    context.job_queue.run_daily(
        check_wrapper, time=time_day, chat_id=chat_id, name=f'day_{chat_id}')
    await update.message.reply_text('Recurring updates for 13h00 started')

    # 20h check
    time_evening = time(hour=19, tzinfo=timezone.utc)
    context.job_queue.run_daily(
        check_wrapper, time=time_evening, chat_id=chat_id, name=f'evening_{chat_id}')
    await update.message.reply_text('Recurring updates for 20h00 started')


async def stop_recurring_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Stop regular checks for SuperSub matches.
    """
    remove_jobs(context)
    await update.message.reply_text('Recurring updates stopped')


def start_telegram_bot(token: str, city: str, driver: WebDriver) -> None:
    """
    Start the Telegram bot application and register command handlers.
    """
    application = Application.builder().token(token).build()

    check_command_with_city = partial(
        check_command, city=city, driver=driver
    )
    start_recurring_command_with_city = partial(
        start_recurring_command, city=city, driver=driver
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )
    application.add_handler(
        CommandHandler("check", check_command_with_city)
    )
    application.add_handler(
        CommandHandler("subscribe", start_recurring_command_with_city)
    )
    application.add_handler(
        CommandHandler("unsubscribe", stop_recurring_command)
    )

    application.run_polling()

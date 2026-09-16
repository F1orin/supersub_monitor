"""Authentication failure behavior across the scraper and Telegram boundary."""

import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from selenium.common.exceptions import TimeoutException, WebDriverException

import supersub
from errors import UrbanSoccerAuthenticationError
from telegram_handler import check_command


def test_parse_available_matches_reports_login_redirect_as_expired_authentication():
    """A redirect to the login page must not surface as a generic timeout."""
    driver = MagicMock()
    driver.find_elements.return_value = []

    def poll_until_redirect(condition):
        driver.current_url = "https://myurban.fr/supersub/findMatch"
        assert not condition(driver)
        driver.current_url = "https://myurban.fr/login?returnUrl=%2Fsupersub%2FfindMatch"
        return condition(driver)

    with (
        patch.dict(
            "os.environ",
            {
                "URBANSOCCER_AUTH_USERID": "test-user",
                "URBANSOCCER_AUTH_TOKEN": "expired-token",
            },
        ),
        patch("supersub.WebDriverWait") as wait_class,
    ):
        wait_class.return_value.until.side_effect = poll_until_redirect

        with pytest.raises(supersub.UrbanSoccerAuthenticationError):
            supersub.parse_available_matches(driver, "Nantes")


def test_parse_available_matches_does_not_treat_foreign_login_as_expired_token():
    """Only UrbanSoccer's login redirect is evidence of an expired token."""
    driver = MagicMock()
    driver.current_url = "https://network-login.example/login"
    driver.find_elements.return_value = []

    def time_out_unless_ready(condition):
        if condition(driver):
            return True
        raise TimeoutException

    with patch("supersub.WebDriverWait") as wait_class:
        wait_class.return_value.until.side_effect = time_out_unless_ready

        with pytest.raises(TimeoutException):
            supersub.parse_available_matches(driver, "Nantes")


def test_check_command_explains_expired_authentication_to_user(caplog):
    """Expired authentication must produce actionable Telegram and log messages."""
    update = MagicMock()
    telegram_message = MagicMock()
    telegram_message.edit_text = AsyncMock()
    update.message.reply_text = AsyncMock(return_value=telegram_message)

    with (
        patch(
            "telegram_handler.supersub.parse_available_matches",
            side_effect=UrbanSoccerAuthenticationError,
        ),
        caplog.at_level(logging.WARNING, logger="telegram_handler"),
    ):
        asyncio.run(
            check_command(
                update=update,
                context=MagicMock(),
                city="Nantes",
                driver=MagicMock(),
            )
        )

    telegram_message.edit_text.assert_awaited_once_with(
        "Your UrbanSoccer session has expired. "
        "Please update the authentication token."
    )
    assert [record.getMessage() for record in caplog.records] == [
        "UrbanSoccer authentication has expired"
    ]


def test_check_command_preserves_generic_webdriver_error_handling(caplog):
    """Non-authentication Selenium failures keep the existing fallback."""
    update = MagicMock()
    telegram_message = MagicMock()
    telegram_message.edit_text = AsyncMock()
    update.message.reply_text = AsyncMock(return_value=telegram_message)

    with (
        patch(
            "telegram_handler.supersub.parse_available_matches",
            side_effect=WebDriverException,
        ),
        caplog.at_level(logging.ERROR, logger="telegram_handler"),
    ):
        asyncio.run(
            check_command(
                update=update,
                context=MagicMock(),
                city="Nantes",
                driver=MagicMock(),
            )
        )

    telegram_message.edit_text.assert_awaited_once_with(
        "Selenium WebDriverException occurred"
    )
    assert [record.getMessage() for record in caplog.records] == [
        "Selenium WebDriverException occurred"
    ]

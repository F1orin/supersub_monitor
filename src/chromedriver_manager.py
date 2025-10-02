"""
ChromeDriver manager for Supersub Monitor.
"""

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

_driver: webdriver.Chrome | None = None

log = logging.getLogger(__name__)


def create_driver() -> webdriver.Chrome:
    """
    Create a new Chrome WebDriver instance.
    """
    log.debug("Creating new Chrome WebDriver instance")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        log.debug("Chrome WebDriver created successfully")
        return driver
    except Exception as e:
        log.exception("Failed to create Chrome WebDriver")
        raise


def get_driver() -> webdriver.Chrome:
    """
    Return the shared Chrome WebDriver instance, creating it if needed.
    """
    global _driver
    if _driver is None:
        log.info("Creating new Chrome WebDriver instance")
        _driver = create_driver()
    else:
        log.debug("Reusing existing Chrome WebDriver instance")
    return _driver


def shutdown_driver() -> None:
    """
    Shut down the shared WebDriver if it exists.
    """
    global _driver
    if _driver is not None:
        log.info("Shutting down Chrome WebDriver")
        try:
            _driver.quit()
            log.debug("Chrome WebDriver shut down successfully")
        except Exception as e:
            log.warning("Error occurred while shutting down Chrome WebDriver: %s", e)
        finally:
            _driver = None
    else:
        log.debug("No Chrome WebDriver to shut down")

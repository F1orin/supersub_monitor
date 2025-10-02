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
    Create a new ChromeDriver instance.
    """
    log.debug("Creating new ChromeDriver instance")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        log.debug("ChromeDriver created successfully")
        return driver
    except Exception as e:
        log.exception("Failed to create ChromeDriver")
        raise


def get_driver() -> webdriver.Chrome:
    """
    Return the shared ChromeDriver instance, creating it if needed.
    """
    global _driver
    if _driver is None:
        log.info("Creating new ChromeDriver instance")
        _driver = create_driver()
    else:
        log.debug("Reusing existing ChromeDriver instance")
    return _driver


def shutdown_driver() -> None:
    """
    Shut down the shared WebDriver if it exists.
    """
    global _driver
    if _driver is not None:
        log.info("Shutting down ChromeDriver")
        try:
            _driver.quit()
            log.debug("ChromeDriver shut down successfully")
        except Exception as e:
            log.warning("Error occurred while shutting down ChromeDriver: %s", e)
        finally:
            _driver = None
    else:
        log.debug("No ChromeDriver to shut down")

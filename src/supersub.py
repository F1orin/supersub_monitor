"""
Supersub: Selenium-based UrbanSoccer match parser and ChromeDriver manager.
"""

import logging
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Constants
SYSTEM_DARWIN = 'Darwin'
SYSTEM_LINUX = 'Linux'
CHROMEDRIVER_NAME_MAC = 'chromedriver_macos'
CHROMEDRIVER_NAME_LINUX = 'chromedriver_linux'
CHROME_PATH_MAC = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROME_PATH_LINUX = '/usr/bin/google-chrome-stable'

log = logging.getLogger(__name__)

load_dotenv()


def parse_available_matches(driver: webdriver.Chrome, city: str) -> list:
    """
    Parse available matches for the given city using Selenium.

    Args:
        city (str): The city to select in the UI.

    Returns:
        list: A list of matches found.
    """
    userid = os.getenv('URBANSOCCER_AUTH_USERID')
    token = os.getenv('URBANSOCCER_AUTH_TOKEN')

    driver.get('https://my.urbansoccer.fr/')

    log.debug('Loading auth credentials...')
    driver.execute_script(
        f"localStorage.setItem('auth-userid', '{userid}');")
    driver.execute_script(
        f"localStorage.setItem('auth-token', '{token}');")
    log.debug('Auth credentials loaded successfully.')

    driver.get('https://my.urbansoccer.fr/')
    driver.get('https://my.urbansoccer.fr/supersub/findMatch')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="centerPicker"]/option[text()="Nantes"]')))
    log.debug('List of cities has loaded')

    element = driver.find_element(By.ID, 'centerPicker')
    select = Select(element)
    select.select_by_visible_text(city)
    log.debug('City selected in the list.')

    time.sleep(1)
    dates = driver.find_elements(
        By.XPATH, '//article[contains(@class, "o-day") and contains(@class, "disabled")]')
    matches = []
    for date in dates:
        spans = date.find_elements(By.XPATH, './span')
        matches_per_day = [None] * 2
        for i, span in enumerate(spans):
            matches_per_day[i] = span.text
        matches.append(matches_per_day)
    log.debug(f'Matches found: {matches}')

    return matches

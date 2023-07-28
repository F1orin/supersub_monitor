import logging
import os
import platform
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)

load_dotenv()

SYSTEM_DARWIN = 'Darwin'
SYSTEM_LINUX = 'Linux'

CHROMEDRIVER_NAME_MAC = 'chromedriver_macos'
CHROMEDRIVER_NAME_LINUX = 'chromedriver_linux'

CHROME_PATH_MAC = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROME_PATH_LINUX = '/usr/bin/google-chrome-stable'


class UnsupportedOSError(Exception):
    pass


def get_driver_path():
    path_prefix = './drivers/'
    path = None
    system = platform.system()
    if system == SYSTEM_DARWIN:
        log.info('Selecting chromedriver for MacOS')
        path = path_prefix + CHROMEDRIVER_NAME_MAC
    elif system == SYSTEM_LINUX:
        log.info('Selecting chromedriver for Linux')
        path = path_prefix + CHROMEDRIVER_NAME_LINUX
    else:
        raise UnsupportedOSError(
            f'Unsupported operating system detected: {system}')
    return path


def get_chrome_path():
    path = None
    current_os = os.getenv('OS')
    if current_os == SYSTEM_DARWIN:
        path = CHROME_PATH_MAC
    elif current_os == SYSTEM_LINUX:
        path = CHROME_PATH_LINUX
    else:
        raise UnsupportedOSError(
            f'Unsupported operating system specified in env: {current_os}')
    return path


def get_driver():
    time.sleep(3)

    try:
        chrome_driver_path = get_driver_path()
    except UnsupportedOSError as driver_error:
        log.error(f'Could not get Chromedriver path: {driver_error}')
        raise

    chrome_service = Service(chrome_driver_path)
    chrome_options = Options()

    try:
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    except UnsupportedOSError as chrome_error:
        log.error(f'Could not get Chrome path: {chrome_error}')
        raise

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver


def parse_available_matches(city: str) -> list:
    try:
        driver = get_driver()
    except UnsupportedOSError as error:
        log.error(f'Could not get Chromedriver: {error}')
        raise

    userid = os.getenv('URBANSOCCER_AUTH_USERID')
    token = os.getenv('URBANSOCCER_AUTH_TOKEN')

    driver.get('https://my.urbansoccer.fr/')

    log.debug('Loading auth creads...')
    driver.execute_script(f"localStorage.setItem('auth-userid', '{userid}');")
    driver.execute_script(f"localStorage.setItem('auth-token', '{token}');")
    log.debug('...auth creds loaded successfully')

    driver.get('https://my.urbansoccer.fr/')
    driver.get('https://my.urbansoccer.fr/supersub/findMatch')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="centerPicker"]/option[text()="Nantes"]')))
    log.debug('List of cities has loaded')

    element = driver.find_element(By.ID, 'centerPicker')
    select = Select(element)
    select.select_by_visible_text(city)
    log.debug('City is selected in the list')

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
    log.debug(f'These are the matches found: {matches}')

    driver.quit()

    return matches

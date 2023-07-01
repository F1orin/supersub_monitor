import logging
import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)

SYSTEM_DARWIN = 'Darwin'
SYSTEM_LINUX = 'Linux'

CHROMEDRIVER_MAC = 'chromedriver_macos'
CHROMEDRIVER_LINUX = 'chromedriver_linux'


def get_driver_path():
    path_prefix = './drivers/'
    path = None
    system = platform.system()
    if system == SYSTEM_DARWIN:
        log.info('Selecting chromedriver for MacOS')
        path = path_prefix + CHROMEDRIVER_MAC
    elif system == SYSTEM_LINUX:
        log.info('Selecting chromedriver for Linux')
        path = path_prefix + CHROMEDRIVER_LINUX
    else:
        raise RuntimeError(f'Unsupported operating system detected: {system}')

    if not os.path.exists(path):
        raise RuntimeError(f'Chromedriver not found by path: {path}')

    return path


def get_driver():
    time.sleep(3)
    chrome_driver_path = get_driver_path()
    chrome_service = Service(chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver


def parse_available_matches(city: str) -> list:

    log.debug('Getting driver...')
    driver = get_driver()
    log.debug('...driver loaded successfully')

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

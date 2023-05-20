import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def parse_available_matches(city: str) -> list:

    chrome_driver_path = './drivers/chromedriver'  # Update with the correct path
    chrome_service = Service(chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    userid = os.getenv('URBANSOCCER_AUTH_USERID')
    token = os.getenv('URBANSOCCER_AUTH_TOKEN')

    driver.get('https://my.urbansoccer.fr/')

    driver.execute_script(f"localStorage.setItem('auth-userid', '{userid}');")
    driver.execute_script(f"localStorage.setItem('auth-token', '{token}');")

    driver.get('https://my.urbansoccer.fr/')
    driver.get('https://my.urbansoccer.fr/supersub/findMatch')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="centerPicker"]/option[text()="Nantes"]')))

    element = driver.find_element(By.ID, 'centerPicker')
    select = Select(element)
    select.select_by_visible_text(city)

    time.sleep(1)
    dates = driver.find_elements(
        By.XPATH, '//article[contains(@class, "o-day") and contains(@class, "disableed")]')
    matches = []
    for date in dates:
        spans = date.find_elements(By.XPATH, './span')
        matches_per_day = [None] * 2
        for i, span in enumerate(spans):
            matches_per_day[i] = span.text
        matches.append(matches_per_day)

    driver.quit()

    return matches

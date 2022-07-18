import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys
sys.path.append("..\\include")
from settings import*
from Browser import Browser

def check_for_plugin(driver):
    driver.get(AUTHORIZATION_PAGE_URL)
    wait = WebDriverWait(driver, 5)
    try:
        element_title = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".description__title")))
        if (element_title.text == "Расширение для браузера"):
            raise Exception("Rutoken plugin is missing")
    except TimeoutException:
        return

def check_for_token(driver):
    driver.get(AUTHORIZATION_PAGE_URL)
    wait = WebDriverWait(driver, 5)
    try:
        element_title = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".aboutservice__title")))
        if (element_title.text == "Не удается обнаружить токен или смарт-карту"):
            raise Exception("The token is missing")
    except TimeoutException:
        return

def is_browser_ready(driver):
    check_for_plugin(driver)
    check_for_token(driver)

@pytest.fixture(scope="session", params=SUPPORTED_BROWSERS)
def get_browser_driver(request):
    match request.param:
        case "chrome":
            options = chrome_options()
            options.add_argument("--load-extension={}".format(RARUTOKEN_PLUGIN_PATH))
            #driver = webdriver.Chrome(CHROME_DRIVER_EXECUTABLE_PATH, options=options)
            driver = webdriver.Chrome(service=Service(
            CHROME_DRIVER_EXECUTABLE_PATH), options=options)
        case "yandex":
            pass
        case "firefox":
            pass

    is_browser_ready(driver)

    yield driver
    driver.quit()

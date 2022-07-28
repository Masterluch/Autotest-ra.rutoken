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
from settings import *
from Browser import Browser

from loguru import logger
logger.remove()
logger.add("../logs/tests.log", format="{time} | {level} | {message}")

@pytest.fixture(scope="session", params=SUPPORTED_BROWSERS)
def get_browser(request):
    browser = Browser(request.param)

    logger.info(f"Начало тестирования в браузере {request.param}")

    yield browser
    browser.driver.quit()

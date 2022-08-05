from loguru import logger
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
import sys

sys.path.append("..\\include")
from Browser import Browser
from settings import *

logger.remove()
logger.add("../logs/tests.log",
    format="{level} | {module} | {function} | {message}")


def test_authorization(get_browser):
    browser = get_browser
    browser.authorization()
    logger.debug("Произведена авторизация")

    element_button_create_new_key = browser.get_element_by(
        By.CSS_SELECTOR, ".add__button")
    logger.debug("Найдена кнопка 'Создать ключ'")

    assert(bool(element_button_create_new_key))

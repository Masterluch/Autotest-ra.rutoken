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

@pytest.fixture(scope="session")
def get_algorithms_list(get_browser):
    browser = get_browser
    browser.authorization()

    # Нажимаем кнопку "Создать ключ"
    browser.click_on_element_by(By.XPATH, "//span[contains(text(), '{}')]".format("Создать ключ"))
    logger.debug("Нажата кнопка 'Создать ключ'")

    # Находим все доступные алгоритмы
    element_algorithms = browser.get_element_by(By.CSS_SELECTOR, "div.form__fieldradio:nth-child(6) > div:nth-child(2)")
    list_algorithms = element_algorithms.text.split("\n")
    for alg in list_algorithms:
        if "—" in alg:
            list_algorithms.remove(alg)
    logger.debug("Обнаружены алгоритмы")

    # Открываем домашнюю страницу
    browser.click_on_element_by(By.CSS_SELECTOR, ".keys__back")
    logger.debug("Нажата кнопка 'К сертификатам и ключам'")

    return list_algorithms

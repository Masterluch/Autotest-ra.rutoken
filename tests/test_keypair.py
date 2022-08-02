import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import sys
sys.path.append("..\\include")
from settings import*
from Browser import Browser
from KeyPair import KeyPair
import time

from loguru import logger
logger.remove()
logger.add("../logs/tests.log", format="{level} | {module} | {function} | {message}")

class TestKeyPair:
    list_keys = []

    # @logger.catch
    def test_creating(self, get_browser, get_algorithms_list):
        logger.info(f"Тест test_creation начинает работу")

        # Очищаем список ключей для проведения тестов в разных браузерах
        self.list_keys.clear()

        browser = get_browser
        list_algorithms = get_algorithms_list
        browser.authorization()
        logger.debug("Авторизация выполнена")
        
        # Создаём ключи
        for i in range(len(list_algorithms)):
            self.list_keys.append(KeyPair(browser, f"{browser.browser_name}Key{i}", list_algorithms[i]))
            logger.debug(f"Создали ключ {browser.browser_name}Key{i}")

        # Проверяем ключи
        for key in self.list_keys:
            if not (key.is_created):
                logger.error(f"Поле is_created ключа {browser.browser_name}Key{i} = False")
                assert(False)

        # Проверка того, что ключей было создано столько же сколько и алгоритмов
        assert(len(self.list_keys) == len(list_algorithms))

    def test_deleting(self, get_browser):
        logger.info(f"Тест test_deleting начинает работу")
        
        browser = get_browser
        logger.debug(f"len(self.list_keys) = {len(self.list_keys)}")
        for key in self.list_keys:
            key.delete(browser)

        # Проверяем ключи
        for key in self.list_keys:
            if (key.is_created):
                logger.error(f"Поле is_created ключа {key.id} = True")
                assert(False)

        assert(True)

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

    @logger.catch
    def test_creation(self, get_browser):
        logger.info(f"Тест test_creation начинает работу")

        browser = get_browser
        browser.authorization()
        logger.debug("Авторизация выполнена")
        
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
        
        # Создаём ключи
        self.list_keys.clear()
        for i in range(len(list_algorithms)):
            self.list_keys.append(KeyPair(browser, f"key{i}", list_algorithms[i]))
            logger.debug(f"Создали ключ key{i}")

        # Проверяем ключи
        for key in self.list_keys:
            if not (key.is_created):
                logger.error(f"Поле is_created ключа {key.id} = False")
                assert(False)
        assert(True)

    def test_deleting(self, get_browser):
        logger.info(f"Тест test_deleting начинает работу")
        
        browser = get_browser
        logger.debug(f"len(self.list_keys) = {len(self.list_keys)}")
        for key in self.list_keys:
            key.delete(browser)

        # try:
        #     element_key_container = browser.get_element_by(By.CSS_SELECTOR, ".key__container")
        # except TimeoutException:
        #     assert(True)
        # assert(False)

        
        
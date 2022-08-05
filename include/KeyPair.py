import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time

from loguru import logger
logger.remove()
logger.add("../logs/tests.log",
           format="{level} | {module} | {function} | {message}")


class KeyPair():
    def __init__(self, browser, id: str, algorithm: str):
        self.is_created = False
        self.id = id
        logger.debug(f"Начало создания ключа {self.id}")

        browser.click_on_element_by(
            By.XPATH, "//span[contains(text(), '{}')]".format("Создать ключ"))
        logger.debug("Нажата кнопка 'Создать ключ'")

        # Заполняем поле "Идентификатор"
        browser.get_element_by(By.CSS_SELECTOR, "#id").send_keys(self.id)
        logger.debug("Заполнен идентификатор")

        # Выбираем алгоритм
        browser.click_on_element_by(
            By.XPATH, f"//*[contains(text(), '{algorithm}')]")
        logger.debug(f"Выбран алгоритм {algorithm}")

        # Нажимаем кнопку "Сгенерировать ключи"
        browser.click_on_element_by(By.CSS_SELECTOR, ".right__bg")
        logger.debug("Нажата кнопка 'Сгенерировать ключи'")

        # Проверяем создания ключа
        try:
            element_text = browser.get_element_by(
                By.XPATH, "//*[contains(text(), 'Ключи созданы!')]")
            logger.debug("Найдена надпись 'Ключи созданы!'")
            logger.debug(f"Ключ {self.id} успешно сгенерирован")
            self.is_created = True
        except TimeoutException:
            logger.error(f"Ключ {self.id} НЕ сгенерирован")

        # Открываем домашнюю страницу
        browser.click_on_element_by(By.CSS_SELECTOR, ".keys__back")
        logger.debug("Нажата кнопка '<- К сертификатам и ключам'")

    def delete(self, browser):
        logger.debug(f"Начало удаления ключа {self.id}")

        # Нажимаем кнопку "Прочитать хранилища устройств заново"
        browser.click_on_element_by(By.CSS_SELECTOR, ".img__reload")
        logger.debug("Нажата кнопка 'Reload'")
        # Нажимаем кнопку корзины
        browser.click_on_element_by(
            By.XPATH, f"//*[contains(text(), '{self.id}')]/../../../../div[1]/div[3]/span[@class = 'img__trash']")
        logger.debug("Нажата кнопка 'Корзина'")
        # Нажимаем на кнопку "Удалить"
        browser.click_on_element_by(
            By.XPATH, f"//*[contains(text(), 'Удалить')]")
        logger.debug("Нажата кнопка 'Удалить'")

        self.is_created = False

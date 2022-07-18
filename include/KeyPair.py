import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time


class KeyPair():
    def __init__(self, driver, id, algorithm):
        self.is_created = False
        wait = WebDriverWait(driver, 10)

        # Нажимаем кнопку для создания нового ключа
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".add__button"))).click()

        # Заполняем поле "Идентификатор"
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#id"))).send_keys(id)

        # Выбираем алгоритм
        element_alg = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), '{}')]".format(algorithm)))).click()

        # Нажимаем кнопку "Сгенерировать ключ"
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".right__bg"))).click()

        # Проверим создание ключа
        try:
            element_text = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".bg__title")))
            if (element_text.text == "Ключи созданы!"):
                self.is_created = True
        except TimeoutException:
            pass

        # Открываем домашнюю страницу
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".keys__back"))).click()
        time.sleep(5)

        
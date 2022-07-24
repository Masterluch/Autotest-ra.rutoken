import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time


class KeyPair():
    def __init__(self, browser, id, algorithm):
        self.is_created = False
        self.id = id
        
        browser.get_element_by(By.XPATH, "//span[contains(text(), '{}')]".format("Создать ключ")).click() # div/button
   
        # Заполняем поле "Идентификатор"
        browser.get_element_by(By.CSS_SELECTOR, "#id").send_keys(self.id)

        # Выбираем алгоритм
        browser.get_element_by(By.XPATH, "//*[contains(text(), '{}')]".format(algorithm)).click()

        # Нажимаем кнопку "Сгенерировать ключи"
        browser.get_element_by(By.CSS_SELECTOR, ".right__bg").click()

        # Проверим создание ключа
        try:
            element_text = browser.get_element_by(By.CSS_SELECTOR, ".bg__title")
            if (element_text.text == "Ключи созданы!"):
                self.is_created = True
        except TimeoutException:
            pass

        # Открываем домашнюю страницу
        browser.get_element_by(By.CSS_SELECTOR, ".keys__back").click()

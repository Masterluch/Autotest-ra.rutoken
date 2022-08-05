from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import xerox
from KeyPair import KeyPair

from loguru import logger
logger.remove()
logger.add("../logs/tests.log",
           format="{level} | {module} | {function} | {message}")


class CertificateRequest:
    def __init__(self, browser, key_id: str, alrorithm: str):
        self.is_created = False
        self.key = KeyPair(browser, key_id, alrorithm)

        # Создадим запрос на сертификат из главного меню
        browser.click_on_element_by(
            By.XPATH, f"//*[contains(text(), '{key_id}')]/../../../..//button[contains(text(), 'Создать заявку на сертификат')]")
        # Заполняем поле 'Общее имя'
        element_input = browser.get_element_by(By.XPATH, "//input[@name = 'commonName']")
        element_input.clear()
        element_input.send_keys(f"{browser.browser_name}CertificateRequest")
        # Нажимаем кнопку создать запрос
        browser.click_on_element_by(
            By.XPATH, "//*[contains(text(), 'Создать запрос')]")

        # Проверяем создание запроса
        try:
            element_text = browser.get_element_by(
                By.XPATH, "//*[contains(text(), 'Запрос создан и подписан!')]")
            logger.debug("Найдена надпись 'Запрос создан и подписан!'")
            logger.debug(f"Запрос для ключа {key_id} успешно сгенерирован")
            self.is_created = True
        except TimeoutException:
            logger.error(f"Запрос для ключа {key_id} НЕ сгенерирован")

        # Нажимаем кнопку 'Скопировать в буфер обмена'
        browser.click_on_element_by(
            By.XPATH, "//*[contains(text(), 'Скопировать в буфер обмена')]")
        # Запоминаем значение из буфера обмена
        self.value = xerox.paste()

        # Открываем домашнюю страницу
        browser.click_on_element_by(By.CSS_SELECTOR, ".keys__back")
        logger.debug("Нажата кнопка '<- К сертификатам и ключам'")

    def delete(self, browser) -> None:
        self.key.delete(browser)
        self.is_created = False

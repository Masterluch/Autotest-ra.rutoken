from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from KeyPair import KeyPair
from CertificateRequest import CertificateRequest
from Browser import Browser
import time
import urllib

from loguru import logger
logger.remove()
logger.add("../logs/tests.log",
           format="{level} | {module} | {function} | {message}")


class Certificate:
    def __init__(self, browser: Browser, key_id: str, alrorithm: str, is_test_mode: bool = True):
        self.is_test_mode = is_test_mode
        self.is_created = False

        if (is_test_mode):
            self.key = KeyPair(browser, key_id, alrorithm)
            browser.click_on_element_by(
                By.XPATH, f"//*[contains(text(), '{key_id}')]/../../../..//button[contains(text(), 'Добавить тестовый сертификат')]")
            # Заполняем поле 'Общее имя'
            element_input = browser.get_element_by(
                By.XPATH, "//input[@name = 'commonName']")
            element_input.clear()
            element_input.send_keys(f"{browser.browser_name}TestCertificate")
            # Нажимаем кнопку создать запрос
            browser.click_on_element_by(
                By.XPATH, "//*[contains(text(), 'Создать запрос')]")

            # Проверяем создание тестового сетификата
            try:
                element_text = browser.get_element_by(
                    By.XPATH, f"//*[contains(text(), '{key_id}')]/../../..//a[contains(text(), 'Показать всю информацию')]")
                logger.debug("Найдена надпись 'Запрос создан и подписан!'")
                logger.debug(f"Запрос для ключа {key_id} успешно сгенерирован")
                self.is_created = True
            except TimeoutException:
                logger.error(f"Запрос для ключа {key_id} НЕ сгенерирован")

        else:
            '''
            Создание запроса и получение сертификата на тестовых УЦ Крипто-ПРО
            '''
            self.cert_req = CertificateRequest(browser, key_id, alrorithm)
            cert_value = self.__get_cryptopro_certificate_value(
                browser, self.cert_req).decode('utf-8')

            '''
            Начинаем добавлять полученный сертификат
            '''
            browser.authorization()
            # Нажимаем кнопку 'Добавить сертификат'
            browser.click_on_element_by(
                By.XPATH, f"//*[contains(text(), '{key_id}')]/../../../..//button[contains(text(), 'Добавить сертификат')]")
            # Выбираем вариант 'Данные из буфера обмена'
            browser.click_on_element_by(
                By.XPATH, "//*[contains(text(), 'Данные из буфера обмена')]")
            # Вводим данные сертификата
            browser.get_element_by(
                By.XPATH, f"//*[@class = 'p-1']").send_keys(cert_value)
            # Нажимаем кнопку 'Связать'
            browser.click_on_element_by(
                By.XPATH, "//*[contains(text(), 'Связать')]")

            # Проверяем создание связки
            try:
                element_text = browser.get_element_by(
                    By.XPATH, "//*[contains(text(), 'Сертификат импортирован!')]")
                logger.debug("Найдена надпись 'Сертификат импортирован!'")
                logger.debug(
                    f"Сертификат для ключа {key_id} успешно сгенерирован")
                self.is_created = True
            except TimeoutException:
                logger.error(f"Сертификат для ключа {key_id} НЕ сгенерирован")

            # Открываем домашнюю страницу
            browser.click_on_element_by(By.CSS_SELECTOR, ".keys__back")
            logger.debug("Нажата кнопка '<- К сертификатам и ключам'")

    def delete(self, browser: Browser) -> None:
        if (self.is_test_mode):
            self.key.delete(browser)
        else:
            self.cert_req.delete(browser)
        self.is_created = False

    def __get_cryptopro_certificate_value(self, browser: Browser, certificate_request: str) -> str:
        browser.open_page("https://www.cryptopro.ru/certsrv/certrqxt.asp")
        browser.get_element_by(By.CSS_SELECTOR, "#locTaRequest").send_keys(
            certificate_request.value)
        browser.click_on_element_by(By.CSS_SELECTOR, "#btnSubmit")
        str = 'Get the requested cert\n\tfunction handleGetCert() {\n\t\tlocation="'
        pos1 = browser.driver.page_source.find(str) + len(str)
        pos2 = browser.driver.page_source.find('"', pos1)
        location = browser.driver.page_source[pos1:pos2]
        link = "https://www.cryptopro.ru/certsrv/" + location + "Enc=b64"
        cert_value = urllib.request.urlopen(link).read()

        return cert_value

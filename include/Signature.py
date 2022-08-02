from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Certificate import Certificate
from os.path import abspath

import time

class Signature:
    def __init__(self, browser, key_id: str, algorithm: str, is_attached_mode: bool = True):
        self.is_created = False
        self.certificate = Certificate(browser, key_id, algorithm)

        # Нажимаем на кнопку
        browser.click_on_element_by(By.XPATH, f"//*[contains(text(), '{key_id}')]/../../../..//button[contains(text(), 'Подписать')]")
        
        '''
        Данный вариант реализовывать нет нужды

        # Выбираем вариант 'Данные из буфера обмена'
        browser.click_on_element_by(By.XPATH, f"//*[contains(text(), 'Данные из буфера обмена')]")
        # Вводим данные для подписи
        browser.click_on_element_by(By.XPATH, f"//*[@class = 'p-1']").send_keys(data_for_signature)
        # Нажимаем кнопку 'Подписать'
        browser.click_on_element_by(By.XPATH, f"//button[contains(text(), 'Подписать')]")
        '''
        
        # Выбираем, в каком виде хотим видеть результат
        if (is_attached_mode):
            # Выбираем вариант 'Подпись объединена с документом'
            browser.click_on_element_by(By.XPATH, "//*[contains(text(), 'Подпись объединена с документом')]")
        else:
            # Выбираем вариант 'Подпись в отдельном файле'
            browser.click_on_element_by(By.XPATH, "//*[contains(text(), 'Подпись в отдельном файле')]")
        # Отправляем файл data_for_signature.txt для подписи
        data_path = abspath("data/data_for_signature.txt")
        browser.get_element_by(By.CSS_SELECTOR, "input[type=file]", is_visible=False).send_keys(data_path)
        # Нажимаем кнопку 'Подписать'
        browser.click_on_element_by(By.XPATH, "//*[contains(text(), 'Подписать')]")
        # Проверяем создание подписи
        browser.get_element_by(By.XPATH, "//*[contains(text(), 'data_for_signature.txt')]")
        self.is_created = True
        # Открываем домашнюю страницу
        browser.click_on_element_by(By.CSS_SELECTOR, ".keys__back")

    def delete(self, browser):
        '''
        Удаление необходимо произвести два раза
        сначала удаляется тестовый сетификат, затем - сам ключ
        '''
        self.certificate.delete(browser)
        self.certificate.delete(browser)
        self.is_created = False

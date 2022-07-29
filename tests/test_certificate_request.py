from selenium.webdriver.common.by import By
import sys
sys.path.append("..\\include")
from settings import *
from Browser import Browser
from KeyPair import KeyPair
from CertificateRequest import CertificateRequest

from loguru import logger
logger.remove()
logger.add("../logs/tests.log", format="{level} | {module} | {function} | {message}")

def test_certificate_request(get_browser):
    browser = get_browser

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
    list_certificate_requests = []
    for i in range(len(list_algorithms)):
        list_certificate_requests.append(CertificateRequest(browser, f"{browser.browser_name}Key{i}", list_algorithms[i]))
        logger.debug(f"Создали запрос для {browser.browser_name}Key{i}")

    # Проверяем запросы
    for cr in list_certificate_requests:
            if not (cr.is_created):
                logger.error(f"Поле is_created запроса для {browser.browser_name}Key{i} = False")
                assert(False)

    # Удаляем ключи
    for cr in list_certificate_requests:
        cr.delete(browser)

    assert(len(list_certificate_requests) == len(list_algorithms))

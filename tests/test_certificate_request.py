from loguru import logger
from CertificateRequest import CertificateRequest
from selenium.webdriver.common.by import By
import sys

sys.path.append("..\\include")
from KeyPair import KeyPair
from Browser import Browser
from settings import *

logger.remove()
logger.add("../logs/tests.log",
    format="{level} | {module} | {function} | {message}")


def test_certificate_request(get_browser, get_algorithms_list):
    logger.info(f"Тест test_creation начинает работу")

    browser = get_browser
    list_algorithms = get_algorithms_list
    browser.authorization()
    logger.debug("Авторизация выполнена")

    # Создаём запросы на сертификаты
    list_certificate_requests = []
    for i in range(len(list_algorithms)):
        list_certificate_requests.append(CertificateRequest(
            browser, f"{browser.browser_name}Key{i}", list_algorithms[i]))
        logger.debug(f"Создали запрос для {browser.browser_name}Key{i}")

    # Проверяем запросы
    for cr in list_certificate_requests:
        if not (cr.is_created):
            logger.error(
                f"Поле is_created запроса для {browser.browser_name}Key{i} = False")
            assert(False)

    # Удаляем ключи
    for cr in list_certificate_requests:
        cr.delete(browser)

    assert(len(list_certificate_requests) == len(list_algorithms))

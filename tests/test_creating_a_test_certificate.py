from loguru import logger
from selenium.webdriver.common.by import By
import sys

sys.path.append("..\\include")
from Certificate import Certificate
from KeyPair import KeyPair
from Browser import Browser
from settings import *

logger.remove()
logger.add("../logs/tests.log",
    format="{level} | {module} | {function} | {message}")

def test_creating_a_test_certificate(get_browser, get_algorithms_list):
    logger.info(f"Тест test_creating_a_test_certificate начинает работу")

    browser = get_browser
    list_algorithms = get_algorithms_list
    browser.authorization()
    logger.debug("Авторизация выполнена")

    # Создаём сертификаты
    list_certificates = []
    for i in range(len(list_algorithms)):
        list_certificates.append(Certificate(
            browser, f"{browser.browser_name}Key{i}", list_algorithms[i]))
        logger.debug(f"Создали запрос для {browser.browser_name}Key{i}")

    # Проверяем запросы
    for cert in list_certificates:
        if not (cert.is_created):
            logger.error(
                f"Поле is_created запроса для {browser.browser_name}Key{i} = False")
            assert(False)

    # Удаление сертификатов
    '''
    Удаление необходимо произвести два раза
    сначала удаляется тестовый сетификат, затем - сам ключ
    '''
    for cert in list_certificates:
        cert.delete(browser)
        cert.delete(browser)

    assert(len(list_certificates) == len(list_algorithms))

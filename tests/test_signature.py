from msilib.schema import Signature
from selenium.webdriver.common.by import By
import sys
sys.path.append("..\\include")
from settings import *
from Browser import Browser
from KeyPair import KeyPair
from Certificate import Certificate
from Signature import Signature

from loguru import logger
logger.remove()
logger.add("../logs/tests.log", format="{level} | {module} | {function} | {message}")

def test_signature(get_browser, get_algorithms_list):
    logger.info(f"Тест test_creating_a_test_certificate начинает работу")

    browser = get_browser
    list_algorithms = get_algorithms_list
    browser.authorization()
    logger.debug("Авторизация выполнена")

    # Создаём подписи
    list_signatures = []
    for i in range(len(list_algorithms)):
        list_signatures.append(Signature(browser, f"{browser.browser_name}Key{i}", list_algorithms[i], is_attached_mode=False))
        logger.debug(f"Создали подпись для ключа {browser.browser_name}Key{i}")
    
    # Проверяем подписи
    for sign in list_signatures:
            if not (sign.is_created):
                logger.error(f"Поле is_created запроса для {browser.browser_name}Key{i} = False")
                assert(False)

    # Удаление сертификатов и ключей
    for sign in list_signatures:
        sign.delete(browser)

    assert(len(list_signatures) == len(list_algorithms))
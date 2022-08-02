import urllib
import time
import sys
from selenium.webdriver.common.by import By

sys.path.append("..\\include")
from settings import *
from CertificateRequest import CertificateRequest
from Certificate import Certificate

from loguru import logger
logger.remove()
logger.add("../logs/tests.log", format="{message}")

def test_getting_certificate_by_cryptopro(get_browser, get_algorithms_list):
    browser = get_browser
    browser.authorization()
    list_algorithms = get_algorithms_list
    
    
    # Создаём сертификаты
    list_certificates = []
    for i in range(len(list_algorithms)):
        list_certificates.append(Certificate(browser, f"{browser.browser_name}Key{i}", list_algorithms[i], is_test_mode=False))
        logger.debug(f"Создали сертификат для ключа {browser.browser_name}Key{i}")
    
    # Проверяем запросы
    for cert in list_certificates:
        if not (cert.is_created):
            logger.error(f"Поле is_created сертификата для {browser.browser_name}Key{i} = False")
            assert(False)

    # Удаление сертификатов
    '''
    Удаление необходимо произвести два раза
    сначала удаляется тестовый сетификат, затем - сам ключ
    '''
    for cert in list_certificates:
        cert.delete(browser)
        cert.delete(browser)
    
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
import sys
sys.path.append("..\\include")
from settings import*
from Browser import Browser
from KeyPair import KeyPair
import time

def test_keypair_creation(get_browser):
    browser = get_browser
    
    # Нажимаем кнопку "Создать ключ"
    browser.get_element_by(By.XPATH, "//span[contains(text(), '{}')]".format("Создать ключ")).click()
    
    # Находим все доступные алгоритмы
    element_algorithms = browser.get_element_by(By.CSS_SELECTOR, "div.form__fieldradio:nth-child(6) > div:nth-child(2)")
    list_algorithms = element_algorithms.text.split("\n")
    for alg in list_algorithms:
        if "—" in alg:
           list_algorithms.remove(alg)

    # Открываем домашнюю страницу
    browser.get_element_by(By.CSS_SELECTOR, ".keys__back").click()
    
    # Создаём ключи
    list_keys = []
    for i in range(len(list_algorithms)):
        list_keys.append(KeyPair(browser, "key{}".format(i), list_algorithms[i]))

    # Проверяем ключи
    for key in list_keys:
        if not (key.is_created):
            assert(False)
    assert(True)
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

def test_keypair_creation(get_browser_driver):
    driver = get_browser_driver
    # driver.get(AUTHORIZATION_PAGE_URL)

    wait = WebDriverWait(driver, 5)
    
    element_button_create_new_key = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".add__button")))
    element_button_create_new_key.click()
    time.sleep(5)
    
    # Находим все доступные алгоритмы
    element_algorithms = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.form__fieldradio:nth-child(6) > div:nth-child(2)")))
    list_algorithms = element_algorithms.text.split("\n")
    for alg in list_algorithms:
        if "—" in alg:
           list_algorithms.remove(alg)

    for alg in list_algorithms:
        print()
        print(alg)

    # Открываем домашнюю страницу
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".keys__back"))).click()
    
    # Создаём ключи
    list_keys = []
    for i in range(len(list_algorithms)):
        list_keys.append(KeyPair(driver, "key{}".format(i), list_algorithms[i]))

    # Проверяем ключи
    for key in list_keys:
        if not (key.is_created):
            assert(False)
    assert(True)
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
import sys
sys.path.append("..\\include")
from settings import *
from Browser import Browser

def test_authorization(get_browser):
    browser = get_browser
    browser.open_page(AUTHORIZATION_PAGE_URL)

    browser.get_element_by(By.CSS_SELECTOR, "#pin").send_keys("12345678")
    browser.get_element_by(By.CSS_SELECTOR, ".right__bg").click()

    element_button_create_new_key = browser.get_element_by(By.CSS_SELECTOR, ".add__button")
    assert(element_button_create_new_key)

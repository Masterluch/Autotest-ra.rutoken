import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec


def test_authorization(get_browser_driver):
    driver = get_browser_driver
    url = "https://ra.rutoken.ru/"
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    element_password_field = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "#pin")))
    element_password_field.send_keys("12345678")
    element_button_entry = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".right__bg")))
    element_button_entry.click()
    
    element_button_create_new_key = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".keys__title")))
    assert(element_button_create_new_key)

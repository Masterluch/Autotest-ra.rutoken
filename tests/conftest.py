import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.chrome.service import Service
from settings import*


@pytest.fixture
def get_browser_driver():
    options = chrome_options()
    options.add_argument("--load-extension={}".format(RARUTOKEN_PLUGIN_PATH))
    #driver = webdriver.Chrome(CHROME_DRIVER_EXECUTABLE_PATH, options=options)
    driver = webdriver.Chrome(service=Service(
        CHROME_DRIVER_EXECUTABLE_PATH), options=options)

    yield driver

    driver.quit()

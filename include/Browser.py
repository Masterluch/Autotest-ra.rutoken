from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options
from selenium.webdriver.chrome.service import Service as chrome_service
from selenium.webdriver.firefox.service import Service as firefox_service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from settings import *

from webdriver_manager.firefox import GeckoDriverManager

class Browser:
    WAITING_TIME = 20

    def __init__(self, browser_name):
        # Настройка драйвера
        match browser_name:
            case "chrome":
                options = chrome_options()
                options.add_argument("--load-extension={}".format(CHROME_RARUTOKEN_PLUGIN_PATH))
                self.driver = webdriver.Chrome(
                    service = chrome_service(CHROME_DRIVER_EXECUTABLE_PATH),
                    options = options)
                
            case "yandex":
                pass
            case "firefox":
                options = firefox_options()
                # options.add_argument("--load-extension={}".format(FIREFOX_RARUTOKEN_PLAGIN_PATH))
                self.driver = webdriver.Firefox(
                    service = firefox_service(GeckoDriverManager().install()),
                    options = options)
                self.driver.install_addon(FIREFOX_RARUTOKEN_PLAGIN_PATH, temporary=True)

        self.wait = WebDriverWait(self.driver, self.WAITING_TIME)
        self.__is_browser_ready()

    # Проверка наличия плагина
    def __check_for_plugin(self) -> None:
        try:
            element_title = self.get_element_by(
                By.CSS_SELECTOR, ".description__title")
            if (element_title.text == "Расширение для браузера"):
                raise Exception("Rutoken plugin is missing")
        except TimeoutException:
            return

    # Проверка наличия токена
    def __check_for_token(self) -> None:
        try:
            element_title = self.get_element_by(
                By.CSS_SELECTOR, ".aboutservice__title")
            if (element_title.text == "Не удается обнаружить токен или смарт-карту"):
                raise Exception("The token is missing")
        except TimeoutException:
            return

    # Проверяем наличие плагина и токена
    def __is_browser_ready(self) -> None:
        self.open_page(AUTHORIZATION_PAGE_URL)
        self.__check_for_plugin()
        self.__check_for_token()

    def get_element_by(self, method: str, value: str): #webdriver.remote.webelement.WebElement
        return self.wait.until(ec.visibility_of_element_located((method, value)))

    def open_page(self, url: str) -> None:
        self.driver.get(url)

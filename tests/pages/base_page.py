from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

class BasePage:
    def __init__(self, driver, base_url: str =None , timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base_url = base_url

    def open(self, url: str):
        if not url.startswith("http"):
            # if not self.base_url:
            #     raise ValueError("Base URL is not set in BasePage")
            url = self.base_url + url
        self.driver.get(url)

    def find(self, by, value):

        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_all(self, by, value):
        ""
        return self.wait.until(lambda d: d.find_elements(by, value))

    def find_clickable(self, by, value):

        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def click(self, element_or_locator):

        if isinstance(element_or_locator, tuple):

            element = self.find(*element_or_locator)
        else:
            element = element_or_locator

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, element, text):

        element.clear()
        element.send_keys(text)

    def get_current_url(self):

        return self.driver.current_url

    def wait_for_url(self, url_part: str):

        self.wait.until(lambda d: url_part in d.current_url)

    def wait_for_url_match(self, pattern, timeout=None):


        if timeout:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, timeout).until(EC.url_matches(pattern))
        else:
            self.wait.until(EC.url_matches(pattern))
        return self.driver.current_url
    def refreshPage(self):
        self.driver.refresh()
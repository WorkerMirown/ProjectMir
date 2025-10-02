from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        """Открывает страницу по URL"""
        self.driver.get(url)

    def find(self, by, value):
        """Находит элемент на странице"""
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_all(self, by, value):
        """Находит список элементов"""
        return self.wait.until(lambda d: d.find_elements(by, value))

    def find_clickable(self, by, value):
        """Ожидает, пока элемент станет кликабельным"""
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def click(self, element_or_locator):
        """Кликает по WebElement или по локатору"""
        if isinstance(element_or_locator, tuple):
            # если передан локатор вида (By.XPATH, "locator")
            element = self.find(*element_or_locator)
        else:
            element = element_or_locator  # WebElement

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, element, text):
        """Вводит текст в поле"""
        element.clear()
        element.send_keys(text)

    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url

    def wait_for_url(self, url_part: str):
        """Ожидает, пока URL будет содержать часть строки"""
        self.wait.until(lambda d: url_part in d.current_url)

    def wait_for_url_match(self, pattern, timeout=None):
        """
        Ожидает, что текущий URL совпадёт с переданным регулярным выражением.
        :param pattern: строка (regex), например r".*/defect/\d+(/.*)?"
        :param timeout: кастомный timeout (по умолчанию общий из self.wait)
        """
        if timeout:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, timeout).until(EC.url_matches(pattern))
        else:
            self.wait.until(EC.url_matches(pattern))
        return self.driver.current_url
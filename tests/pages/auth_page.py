import time

import allure
from selenium.webdriver.common.by import By
from ..pages.base_page import BasePage


class AuthPage(BasePage):

    EMAIL = (By.CSS_SELECTOR, '#field-email-5e954ef1842b8d480aef9b541930f0cb444c24cb')
    PASSWORD = (By.CSS_SELECTOR, '#field-password-6e375a8c5cee60d33bd060d76dc97dca59fb6920')
    LOGIN_BUTTON = (By.ID, "button-login")


    @allure.step("Авторизация:")
    def login(self, email: str, password: str):

        self.open("https://carsrv-test.st.tech/login")
        self.send_keys(self.find(*self.EMAIL), email)
        self.send_keys(self.find(*self.PASSWORD), password)
        self.click(self.find_clickable(*self.LOGIN_BUTTON))
        try:
            self.wait_for_url("/profile")
            if self.get_current_url().endswith("/profile") or self.get_current_url().endswith("/main"):
                allure.attach(
                    "Авторизация успешна",
                    attachment_type=allure.attachment_type.TEXT
                )
            self.open("https://carsrv-test.st.tech/main")
        except Exception as e:
            allure.attach(
                f"Авторизация не прошла. Ошибка: {str(e)}",
                name="Авторизация",
                attachment_type=allure.attachment_type.TEXT
            )
        time.sleep(1)

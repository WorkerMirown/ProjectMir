import re
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..helpers import select_custom_dropdown

@allure.feature("Создание заявки клиентом")
@allure.story("Авторизация и создание новой заявки")
def test_login_and_create_request(driver):
    wait = WebDriverWait(driver, 15)

    with allure.step("Авторизация клиента"):
        driver.get("https://carsrv-test.st.tech/login")
        driver.find_element(By.CSS_SELECTOR, '#field-email-5e954ef1842b8d480aef9b541930f0cb444c24cb') \
              .send_keys("clientautomationtester@mail.ru")
        driver.find_element(By.CSS_SELECTOR, '#field-password-6e375a8c5cee60d33bd060d76dc97dca59fb6920') \
              .send_keys("Test123!!#@")
        driver.find_element(By.ID, "button-login").click()
        wait.until(lambda d: d.current_url.endswith("/profile") or d.current_url.endswith("/main"))
        assert driver.current_url.endswith("/profile") or driver.current_url.endswith("/main")
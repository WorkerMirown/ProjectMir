import re
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from ..helpers import select_custom_dropdown

def load_request_id():
    with open("request_id.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

@allure.feature("Перевод заявки менеджером СТТ")
@allure.story("Авторизация и поиск заявки")
def test_find_request_by_id(driver):
    wait = WebDriverWait(driver, 15)
    request_id = load_request_id()

    with allure.step("Авторизация менеджера СТТ"):
        driver.get("https://carsrv-test.st.tech/login")
        driver.find_element(
            By.CSS_SELECTOR, '#field-email-5e954ef1842b8d480aef9b541930f0cb444c24cb'
        ).send_keys("managersttautomationtester@mail.ru")
        driver.find_element(
            By.CSS_SELECTOR, '#field-password-6e375a8c5cee60d33bd060d76dc97dca59fb6920'
        ).send_keys("Test123!!#@")
        driver.find_element(By.ID, "button-login").click()
        wait.until(lambda d: d.current_url.endswith("/profile") or d.current_url.endswith("/main"))
        assert driver.current_url.endswith("/profile") or driver.current_url.endswith("/main")

    with allure.step("Переход в список заявок"):
        driver.get("https://carsrv-test.st.tech/main")

    with allure.step(f"Поиск заявки по ID {request_id}"):
        # раскрытие фильтра
        select_custom_dropdown(
            driver,
            '//*[@id="primary-group"]/div[1]/div/div',
            "//div[contains(@class,'option') and text()='ID заявки']"
        )

        # вводим ID заявки в поле поиска
        id_input = driver.find_element(By.ID, "field-id-1c88e9e6b511a67cf1aee1b95f3bb9abe0b170fd")
        id_input.clear()
        id_input.send_keys(request_id)

        # жмём кнопку "Поиск"
        search_button = driver.find_element(
            By.XPATH, "//div[@id='primary-group']/fieldset/div/div[5]/div/div/button"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        driver.execute_script("arguments[0].click();", search_button)

    with allure.step("Проверка, что заявка найдена"):
        link = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//table//a[contains(@href,'/requests/{request_id}/edit')]")
            )
        )
        assert request_id in link.get_attribute("href"), f"Заявка {request_id} не найдена"
        allure.attach(link.get_attribute("href"), name="Ссылка на заявку", attachment_type=allure.attachment_type.TEXT)

        # Переход внутрь заявки
        driver.execute_script("arguments[0].click();", link)

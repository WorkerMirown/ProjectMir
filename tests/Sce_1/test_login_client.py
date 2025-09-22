# test_login_client.py
import re
import time
import allure
from pathlib import Path
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..helpers import select_custom_dropdown

@allure.feature("Создание заявки клиентом")
@allure.story("Авторизация и создание новой заявки")
def test_login_and_create_request(driver, save_request_id_file):
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

    with allure.step("Переход на форму создания заявки"):
        driver.get("https://carsrv-test.st.tech/requests/request_form")

    with allure.step("Выбор филиала"):
        select_custom_dropdown(
            driver,
            '//*[@id="088fa587fbac295705e7e561d778761bd353d683"]/fieldset[1]/div[2]/div/fieldset/div/div[2]/div[2]/div/div',
            "//div[contains(@class,'option') and normalize-space(text())='Филиал тест']"
        )
        time.sleep(1)

    with allure.step("Заполнение информации об автомобиле"):
        select_custom_dropdown(
            driver,
            '//*[@id="088fa587fbac295705e7e561d778761bd353d683"]/fieldset[2]/div[2]/div/fieldset/div/div[1]/div/div/div/div/div[1]',
            "//div[contains(@class,'option ') and normalize-space(text())='777']"
        )

        driver.find_element(By.ID, "field-mileage-fb852198353ae70c02bfba57c5263d5a61ed9f8d").send_keys("5991")
        comment_input = driver.find_element(By.ID, "field-client-comment-107dc7759a96af90d7ce96daa7ebdb5a7e95bf6f")
        comment_input.clear()
        comment_input.send_keys("Тест")
        time.sleep(1)

    # with allure.step("Выбор состояния ТС"):
    #     select_custom_dropdown(
    #         driver,
    #         '//*[@id="088fa587fbac295705e7e561d778761bd353d683"]/fieldset/div[2]/div/fieldset/div/div[3]/div[1]/div/div/div/div[1]',
    #         "//div[contains(@class,'option') and normalize-space(text())='Эксплуатируется']"
    #     )

    with allure.step("Сохранение заявки"):
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Сохранить']]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)

    with allure.step("Ожидание редиректа и получение ID заявки"):
        wait.until(EC.url_matches(r".*/requests/\d+/edit"))
        current_url = driver.current_url
        match = re.search(r"/requests/(\d+)/edit", current_url)
        request_id = match.group(1) if match else None

        allure.attach(current_url, name="URL заявки", attachment_type=allure.attachment_type.TEXT)
        allure.attach(request_id or "Не найдено", name="ID заявки", attachment_type=allure.attachment_type.TEXT)
        print("ID заявки:", request_id)

        if request_id:
            save_request_id_file(request_id)

        DATA_DIR = Path(__file__).resolve().parents[1] / "data"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        REQUEST_FILE = DATA_DIR / "request_id.txt"

        REQUEST_FILE.write_text(request_id or "", encoding="utf-8")
        print(f"Request id saved to: {REQUEST_FILE}")


        button = wait.until(EC.element_to_be_clickable((By.ID, "notifyModalClose")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)
    with allure.step("Направление заявки в СТТ"):
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Направить заявку в СТТ']]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)

        button = wait.until(EC.element_to_be_clickable((By.ID, "submit-modal-sendToSTT")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)

        button = wait.until(EC.element_to_be_clickable((By.ID, "notifyModalClose")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)
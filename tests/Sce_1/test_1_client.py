
import re
import time
import allure
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..helpers import select_custom_dropdown
from ..pages.auth_page import AuthPage
from ..pages.request_form_page import RequestFormPage
from ..pages.request_page import RequestPage

@allure.feature("Создание заявки клиентом")
@allure.story("Авторизация и создание новой заявки")
def test_login_and_create_request(driver, save_request_id_file):
    wait = WebDriverWait(driver, 15)
    auth_page = AuthPage(driver)
    request_page_form = RequestFormPage(driver)
    request_page = RequestPage(driver)

    auth_page.login(
        email ="clientautomationtester@mail.ru",
        password ="Test123!!#@"
    )

    request_page_form.open_form()
    request_page_form.select_filial()
    request_page_form.select_car()
    request_page_form.fill_car_info(mileage="5991", comment="Тест")
    request_page_form.add_file_request_form()

    request_page_form.save_request()

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
    time.sleep(1)
    request_page_form.close_notification()

    request_page.send_to_stt()






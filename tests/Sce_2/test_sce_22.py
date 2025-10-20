
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
from ..pages.main_page import MainPage
from ..pages.request_page import RequestPage


def load_request_id():
    data_file = Path(__file__).parent.parent / "data" / "request_id.txt"
    return data_file.read_text(encoding="utf-8").strip()

@allure.feature("Создание заявки клиентом")
@allure.story("Авторизация под клиентом и создание новой заявки")
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
    request_page_form.status_tc_change("operated")

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


@allure.feature("Обработка заявки Сервис менеджером")
@allure.story("Создание 1го дефектов и комплекса мероприятий")
def test_servicemanager_defect_1(driver):
    request_id = load_request_id()
    main_page = MainPage(driver)
    request_page = RequestPage(driver)
    auth_page = AuthPage(driver)

    try:
        auth_page.login(email="workerismirown@gmail.com", password="eA123!@#")

        main_page.search_request(request_id)
        main_page.open_request_by_id(request_id)

        request_page.create_defect(request_id)

        request_page.send_to_sto(request_id)
        request_page.open_first_defect(request_id)
        request_page.create_event("diagnostics",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "diagnostics")
        #
        request_page.create_event("repair",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "repair")


        print("Тест пройден успешно")

    except Exception as e:
        allure.attach(f"Ошибка выполнения теста: {str(e)}",
                      name="Ошибка теста",
                      attachment_type=allure.attachment_type.TEXT)
        raise


@allure.story("Создание 2го дефектов и комплекса мероприятий")
def test_servicemanager_defect_2(driver):
    request_id = load_request_id()
    main_page = MainPage(driver)
    request_page = RequestPage(driver)
    auth_page = AuthPage(driver)

    try:
        auth_page.login(email="workerismirown@gmail.com", password="eA123!@#")

        main_page.search_request(request_id)
        main_page.open_request_by_id(request_id)

        request_page.create_defect(request_id)

        request_page.open_first_defect(request_id)
        request_page.create_event("diagnostics",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "diagnostics")
        #
        request_page.create_event("delivery_car_by_sto",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "delivery_car_by_sto")

        request_page.create_event("order_parts",
                                  '//*[@id="field-sur-datetime-519f29cf8d6cd0bceddcf4285d0f142c78218f3b"]',
                                  '//*[@id="field-end-plan-datetime-f65c59615574e969b8f35ff422028f241d6ce294"]',
                                  "order_parts",
                                )

        request_page.create_event("repair_car_sto",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "repair_car_sto")
        request_page.create_event("delivery_car_to_client",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "delivery_car_to_client")


        print("Тест пройден успешно")

    except Exception as e:
        allure.attach(f"Ошибка выполнения теста: {str(e)}",
                      name="Ошибка теста",
                      attachment_type=allure.attachment_type.TEXT)
        raise


@allure.story("Создание дефекта и комплекса мероприятий пользователем managerSTT")
def test_managerSTT_defect_1(driver):
    request_id = load_request_id()
    main_page = MainPage(driver)
    request_page = RequestPage(driver)
    auth_page = AuthPage(driver)

    try:

        auth_page.login(email="managersttautomationtester@mail.ru", password="Test123!!#@")

        main_page.search_request(request_id)
        main_page.open_request_by_id(request_id)

        request_page.open_first_defect(request_id)


        request_page.create_event("diagnostics",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "diagnostics")
        request_page.close_event("diagnostics", "//input[starts-with(@id,'field-start-fact-datetime')]",
                             "//input[starts-with(@id,'field-end-fact-datetime')]",)

        request_page.create_event("repair",
                                  "//input[starts-with(@id,'field-start-plan-datetime')]",
                                  "//input[starts-with(@id,'field-end-plan-datetime')]",
                                  "repair")
        request_page.close_event("repair", "//input[starts-with(@id,'field-start-fact-datetime')]",
                             "//input[starts-with(@id,'field-end-fact-datetime')]",)

        print("Тест managerSTT_defect_1 пройден успешно")

    except Exception as e:
        allure.attach(f"Ошибка выполнения теста: {str(e)}",
                      name="Ошибка теста",
                      attachment_type=allure.attachment_type.TEXT)
        raise


@allure.story("Создание 2-го дефекта и комплекса мероприятий для managerSTT")
def test_managerstt_defect_2(driver):
    request_id = load_request_id()
    main_page = MainPage(driver)
    request_page = RequestPage(driver)
    auth_page = AuthPage(driver)

    try:
        auth_page.login(email="managersttautomationtester@mail.ru", password="Test123!!#@")
        main_page.search_request(request_id)
        main_page.open_request_by_id(request_id)
        request_page.open_first_defect(request_id)
        driver.get('https://carsrv-test.st.tech/defect/1853/view')
        events = [
             ("delivery_car_by_sto", "//input[starts-with(@id,'field-start-plan-datetime')]", "//input[starts-with(@id,'field-end-plan-datetime')]"),
             ("diagnostic_sto", "//input[starts-with(@id,'field-start-plan-datetime')]", "//input[starts-with(@id,'field-end-plan-datetime')]"),
            ("repair_car_sto", "//input[starts-with(@id,'field-start-plan-datetime')]", "//input[starts-with(@id,'field-end-plan-datetime')]"),
        ]

        checkboxes = ["//input[@id='checkbox1']", "//input[@id='checkbox2']"]
        for event_name, start_xpath, end_xpath in events:
             with allure.step(f"Создание мероприятия: {event_name}"):
                request_page.create_event(event_name, start_xpath, end_xpath, event_name)
                time.sleep(1)
             with allure.step(f"Закрытие мероприятия: {event_name}"):
                 request_page.close_event(event_name, "//input[starts-with(@id,'field-start-fact-datetime')]", "//input[starts-with(@id,'field-end-fact-datetime')]", checkboxes)
                 time.sleep(1)
        time.sleep(5)
        print("Тест managerSTT_defect_2 пройден успешно")

    except Exception as e:
        allure.attach(f"Ошибка выполнения теста: {str(e)}",
                      name="Ошибка теста",
                      attachment_type=allure.attachment_type.TEXT)
        raise
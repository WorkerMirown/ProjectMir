import time
import allure
from pathlib import Path


from ..pages.auth_page import AuthPage
from ..pages.main_page import MainPage
from ..pages.request_page import RequestPage

def load_request_id():
    data_file = Path(__file__).parent.parent / "data" / "request_id.txt"
    return data_file.read_text(encoding="utf-8").strip()

@allure.feature("Обработка заявки Сервис менеджером")
@allure.story("Авторизация и поиск заявки")
def test_servicemanager(driver):
        request_id = load_request_id()
        main_page = MainPage(driver)
        request_page = RequestPage(driver)
        auth_page = AuthPage(driver)

        try:
            auth_page.login(email="workerismirown@gmail.com", password="eA123!@#")

            main_page.search_request(request_id)
            main_page.open_request_by_id(request_id)

            request_page.create_defect(request_id)
            # Отправка заявки в СТТ
            request_page.send_to_sto(request_id)
            request_page.open_first_defect(request_id)
            request_page.create_event("Диагностика",
                                      "field-start-plan-datetime-27880608c1ce3a90b7d6f71f284bd7c1784f5864",
                                      "field-end-plan-datetime-52a0ba72e1d162883a9abb0d62033daf3380b0d4",
                                      "diagnostic_sto")
            request_page.close_event("Диагностика",
                                     "field-start-fact-datetime-00495780d10df3b9335245635c754fc567320b9d",
                                     "field-end-fact-datetime-ea53c49d1be0dbd9d90d113c86c536348297b934",
                                     [
                                         '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[1]/div/div/div/label[2]',
                                         '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[2]/div/div/div/label[2]'])

            print("Тест пройден успешно")

        except Exception as e:
            allure.attach(f"Ошибка выполнения теста: {str(e)}",
                          name="Ошибка теста",
                          attachment_type=allure.attachment_type.TEXT)
            raise

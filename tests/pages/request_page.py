import time
import allure
from pathlib import Path
from selenium.webdriver.common.by import By
from ..pages.base_page import BasePage


class RequestPage(BasePage):

    # --- Локаторы ---
    # Уведомления / модальные окна
    SEND_TO_STT_BUTTON_XPATH = "//button[.//span[text()='Направить заявку в СТТ']]"
    SUBMIT_MODAL_BUTTON_ID = "submit-modal-sendToSTT"
    NOTIFY_MODAL_CLOSE_ID = "notifyModalClose"
    ERROR_MODAL_TEXT = (By.CSS_SELECTOR, ".notify-modal-text")

    # Дефект
    DEFECT_BUTTON_XPATH = '//button[contains(text(), "Добавить дефект")]'
    DEFECT_TITLE_ID = 'field-title-ebf918a9a9e04da5679f0433b2244bba9f4238eb'
    SERVICE_POINT_CONTAINER_XPATH = '//*[@id="post-form"]/fieldset/div/div[5]/div/div/div[1]'
    SERVICE_POINT_OPTION_XPATH = '//div[contains(@class,"ts-dropdown-content")]//div[@data-value="1"]'
    DEFECT_LINK_CSS = "tbody tr td a"

    # Локаторы
    SEND_STO_BUTTON_XPATH = '//button[.//span[contains(text(), "Направить в СТО")]]'
    EVENT_TYPE_XPATH = '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div'
    EVENT_OPTION_DIAGNOSTIC_XPATH = '//div[@role="option" and @data-value="diagnostic_sto"]'
    START_DATE_ID = "field-start-plan-datetime-27880608c1ce3a90b7d6f71f284bd7c1784f5864"
    END_DATE_ID = "field-end-plan-datetime-52a0ba72e1d162883a9abb0d62033daf3380b0d4"

    CALENDAR_CSS = ".flatpickr-calendar.open"
    TODAY_CSS = ".flatpickr-day.today"
    #Локаторы Ивента
    EVENT_BUTTON_XPATH = "//a[@class='btn  btn-success'][.//span[normalize-space(text())='Создать мероприятие']]"
    SAVE_BUTTON_XPATH = '//*[@id="post-form"]/fieldset/div/div/button[2]'
    CONFIRM_BTN_XPATH = '//*[@id="confirmBtnModalSend"]'
    NOTIFY_CLOSE_XPATH = '//*[@id="notifyModalClose"]'
    EVENT_TYPES = {
        "diagnostics": "Выезд в парк для диагностики (ремонта)",
        "delivery_car_to_sto": "Предоставление ТС на СТО",
        "delivery_car_by_sto": "Эвакуация ТС на СТО силами СТО",
        "diagnostic_sto": "Диагностика ТС на СТО",
        "order_parts": "Заказ запасных частей",
        "request_for_approval_of_repair": "Согласование статуса ремонта",
        "repair": "Выезд в парк для проведения ремонта",
        "repair_car_sto": "Ремонт ТС на СТО",
        "delivery_car_to_client": "Выдача ТС клиенту"
    }
    # Файлы
    FILE_INPUT_ID = "field-doc-files-df1bd9fe0dd490dfc71e27f75d7be3a830e73b8b"
    @allure.step("Закрываем уведомление")
    def close_notification(self):
        try:
            button = self.find_clickable(By.ID, self.NOTIFY_MODAL_CLOSE_ID)
            self.click(button)
        except Exception as e:
            allure.attach(f"Ошибка при закрытии уведомления: {str(e)}",
                          name="Ошибка закрытия уведомления", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Направляем заявку в СТТ")
    def send_to_stt(self):
        try:

            button = self.find_clickable(By.XPATH, self.SEND_TO_STT_BUTTON_XPATH)
            self.click(button)

            # submit_button = self.find_clickable(By.ID, self.SUBMIT_MODAL_BUTTON_ID)
            # self.click(submit_button)

            try:
                error_modal = self.wait(self.driver, 3).until(
                    self.find((By.CSS_SELECTOR, ".notify-modal-text"))
                )
                error_text = error_modal.text
                allure.attach(error_text, name="Ошибка модального окна", attachment_type=allure.attachment_type.TEXT)
                self.close_notification()

                print(f"[WARN] Появилась ошибка при направлении заявки в СТТ: {error_text}")

            except Exception:
                if self.find(By.ID, self.NOTIFY_MODAL_CLOSE_ID):
                    self.close_notification()
                    print('Успешное отправление заявки ')

        except Exception as e:
            allure.attach(f"Ошибка при направлении заявки в СТТ: {str(e)}",
                          name="Ошибка направления в СТТ", attachment_type=allure.attachment_type.TEXT)
            raise e
    @allure.step("Создаем дефект в заявке")
    def create_defect(self, request_id,  defect_name="TestDefectAuto"):
        try:

            self.driver.get(f"https://carsrv-test.st.tech/requests/{request_id}/defects")
            time.sleep(1.2)
            defect_button = self.find(By.XPATH, self.DEFECT_BUTTON_XPATH)
            defect_button.click()

            title_input = self.find(By.ID, self.DEFECT_TITLE_ID)
            title_input.click()
            title_input.clear()
            title_input.send_keys(defect_name)

            service_point_container = self.find_clickable(By.XPATH, self.SERVICE_POINT_CONTAINER_XPATH)
            self.click(service_point_container)
            print(f"SERVICE_POINT_OPTION_XPATH: {self.SERVICE_POINT_OPTION_XPATH}")

            service_point = self.find_clickable(By.XPATH, self.SERVICE_POINT_OPTION_XPATH)
            service_point.click()
            self.find(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/nav/ul/li[2]/div/button').click()
            allure.attach(f"Дефект '{defect_name}' создан", name="Успех", attachment_type=allure.attachment_type.TEXT)
            self.close_notification()

        except Exception as e:
            allure.attach(f"Ошибка при создании дефекта: {str(e)}",
                          name="Ошибка создания дефекта", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Отправляем в СТО")
    def send_to_sto(self, request_id):
        self.driver.get(f"https://carsrv-test.st.tech/requests/{request_id}/edit")
        button = self.find(By.XPATH, self.SEND_STO_BUTTON_XPATH)
        self.click(button)
        self.close_notification()
        time.sleep(1)

    @allure.step("Открываем первый дефект в заявке")
    def open_first_defect(self, request_id: str):
        self.driver.get(f'https://carsrv-test.st.tech/requests/{request_id}/defects')
        table = self.find(By.CSS_SELECTOR, "table")
        defect_links = table.find_elements(By.CSS_SELECTOR, self.DEFECT_LINK_CSS)
        if not defect_links:
            raise Exception("Нет дефектов в таблице")
        defect_link = defect_links[-1]
        self.click(defect_link)
        self.wait_for_url_match(r".*/defect/\d+(/.*)?")
        allure.attach(self.driver.current_url, "URL дефекта")

    def pick_today_date(self, by, locator, retries=3):
        for attempt in range(1, retries + 1):
            date_box = self.find_clickable(by, locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", date_box)
            date_box.click()
            time.sleep(0.5)

            calendar = self.find(By.CSS_SELECTOR, ".flatpickr-calendar.open")
            today = calendar.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", today)
            time.sleep(0.5)
            today.click()
            time.sleep(0.5)
            date_box = self.find_clickable(by, locator)
            value = date_box.get_attribute("value")
            if value.strip():
                return value

            self.driver.execute_script("arguments[0].value = '';", date_box)
            time.sleep(0.3)

        raise Exception(f"Не удалось выбрать today в календаре после {retries} попыток")

    @allure.step("Создаём мероприятие")
    def create_event(self, event_type: str, plan_start_id: str, plan_end_id: str, option_value: str, sur_number: str = None):

        # if event_type not in self.EVENT_TYPES:
        #     raise ValueError(f"Unknown event_type '{event_type}'. Allowed: {list(self.EVENT_TYPES.keys())}")

        option_value = event_type
        option_name = self.EVENT_TYPES[event_type]
        with allure.step(f"Создание мероприятия: {option_name}"):

            self.click(self.find_clickable(By.XPATH, self.EVENT_BUTTON_XPATH))
            dropdown = self.find_clickable(By.XPATH,
                                           '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div')
            dropdown.click()

            option = self.find_clickable(By.XPATH, f'//div[@role="option" and @data-value="{option_value}"]')
            self.click(option)

            if option_value == "order_parts":
                    self.fill_order_parts(plan_start_id, plan_end_id, sur_number)
                    time.sleep(1)
            else:
                self.pick_today_date(By.XPATH, plan_start_id)
                self.pick_today_date(By.XPATH, plan_end_id)

            self.click(self.find(By.XPATH, self.SAVE_BUTTON_XPATH))
            self.close_notification()
            allure.attach(event_type, "Мероприятие создано")

    @allure.step("Закрываем мероприятие")
    def close_event(self, event_type: str, fact_start_id: str, fact_end_id: str, checkbox_xpaths: list):
        option_name = self.EVENT_TYPES[event_type]

        with allure.step(f"Закрытие мероприятия: {option_name}"):
            # Находим таблицу на странице дефекта
            table = self.find(By.CSS_SELECTOR, "div.table-responsive table")
            rows = table.find_elements(By.TAG_NAME, "tr")

            event_link = None
            for row in rows:
                try:
                    event_cell = row.find_element(By.CSS_SELECTOR, "td[data-column='type'] span")
                    if event_cell.text.strip() == option_name:
                        event_link = row.find_element(By.CSS_SELECTOR, "td[data-column='type'] a")
                        break
                except Exception:
                    continue

            if not event_link:
                raise Exception(f"Мероприятие '{option_name}' не найдено в таблице")

            # Переход на страницу редактирования события
            self.driver.execute_script("arguments[0].scrollIntoView(true);", event_link)
            event_link.click()
            self.wait_for_url_match(r".*/event/\d+/edit")
            print("Открыто мероприятие:", self.driver.current_url)

            # Теперь ставим даты и галочки
            self.pick_today_date(By.XPATH, fact_start_id)
            self.pick_today_date(By.XPATH, fact_end_id)

            for xpath in checkbox_xpaths:
                self.click(self.find(By.XPATH, xpath))

            self.click(self.find(By.XPATH, self.SAVE_BUTTON_XPATH))
            self.click(self.find(By.XPATH, self.CONFIRM_BTN_XPATH))
            self.close_notification()
            allure.attach(event_type, "Мероприятие закрыто")

    #Ивентовые методы

    def fill_order_parts(self, plan_start_id1: str, plan_end_id1: str, sur_number: str = None):

        radio_button = self.find(By.ID, "field-self-bought-parts-9f8f15a79557533ed9e84b3be152ce6ced3de0fa")
        sur_number_field = self.find(By.ID, "field-sur-number-d1bc07b7546eabd54cedf42d5aa88edc4cc7e691")
        self.pick_today_date(By.XPATH, plan_end_id1)

        if sur_number is None:
            if not radio_button.is_selected():
                radio_button.click()

            time.sleep(0.5)
        else:
            sur_number_field.clear()
            sur_number_field.send_keys(sur_number)
            self.pick_today_date(By.XPATH, plan_start_id1)
            self.pick_today_date(By.XPATH, plan_end_id1)
            time.sleep(0.5)

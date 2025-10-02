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

    # Локаторы
    SEND_STO_BUTTON_XPATH = '//button[.//span[contains(text(), "Направить в СТО")]]'
    EVENT_BUTTON_XPATH = '//*[@id="app"]/div/div/div[1]/div/nav/ul/li[2]/div/a'
    EVENT_TYPE_XPATH = '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div'
    EVENT_OPTION_DIAGNOSTIC_XPATH = '//div[@role="option" and @data-value="diagnostic_sto"]'
    START_DATE_ID = "field-start-plan-datetime-27880608c1ce3a90b7d6f71f284bd7c1784f5864"
    END_DATE_ID = "field-end-plan-datetime-52a0ba72e1d162883a9abb0d62033daf3380b0d4"
    SAVE_BUTTON_XPATH = '//*[@id="post-form"]/fieldset/div/div/button[2]'

    CALENDAR_CSS = ".flatpickr-calendar.open"
    TODAY_CSS = ".flatpickr-day.today"

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
    @allure.step("Создаём событие диагностики")
    def create_diagnostic_event(self):
        try:
            self.click(By.XPATH, self.EVENT_BUTTON_XPATH)
            self.click(By.XPATH, self.EVENT_TYPE_XPATH)
            self.click(By.XPATH, self.EVENT_OPTION_DIAGNOSTIC_XPATH)

            # Дата начала
            self.click(By.ID, self.START_DATE_ID)
            calendar_begin = self.find(By.CSS_SELECTOR, self.CALENDAR_CSS)
            calendar_begin.find_element(By.CSS_SELECTOR, self.TODAY_CSS).click()

            # Дата окончания
            self.click(By.ID, self.END_DATE_ID)
            calendar_end = self.find(By.CSS_SELECTOR, self.CALENDAR_CSS)
            calendar_end.find_element(By.CSS_SELECTOR, self.TODAY_CSS).click()

            # Сохранение
            self.click(By.XPATH, self.SAVE_BUTTON_XPATH)

            allure.attach("Событие диагностики успешно создано",
                          name="Создание события",
                          attachment_type=allure.attachment_type.TEXT)
            return self
        except Exception as e:
            allure.attach(f"Ошибка при создании события диагностики: {str(e)}",
                          name="Ошибка события",
                          attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Открытие дефекта")
    def open_defects_page(self, request_id):
        self.driver.get(f'https://carsrv-test.st.tech/requests/{request_id}/defects')


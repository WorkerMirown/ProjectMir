import time
import allure
from pathlib import Path
from selenium.webdriver.common.by import By
from ..pages.base_page import BasePage
from ..helpers import select_custom_dropdown


class RequestFormPage(BasePage):


    BRANCH_DROPDOWN_XPATH = '//*[@id="088fa587fbac295705e7e561d778761bd353d683"]/fieldset[1]/div[2]/div/fieldset/div/div[2]/div[2]/div/div'
    BRANCH_OPTION_XPATH = "//div[contains(@class,'option') and normalize-space(text())='Филиал тест']"

    CAR_DROPDOWN_XPATH = '//*[@id="088fa587fbac295705e7e561d778761bd353d683"]/fieldset[2]/div[2]/div/fieldset/div/div[1]/div/div/div/div/div[1]'
    CAR_OPTION_XPATH = "//div[@data-value='436']"

    MILEAGE_ID = "field-mileage-fb852198353ae70c02bfba57c5263d5a61ed9f8d"
    COMMENT_ID = "field-client-comment-107dc7759a96af90d7ce96daa7ebdb5a7e95bf6f"

    SAVE_BUTTON_XPATH = "//button[@type='submit' and .//span[text()='Сохранить']]"
    ERROR_MESSAGE_XPATH = "//div[contains(@class,'error-message')]"

    NOTIFY_MODAL_CLOSE_ID = '//*[@id="notifyModalClose"]'

    @allure.step("Открываем форму создания заявки")
    def open_form(self):
        try:
            self.open("https://carsrv-test.st.tech/requests/request_form")
        except Exception as e:
            allure.attach(f"Ошибка при открытии формы: {str(e)}",
                          name="Ошибка", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Выбираем филиал: 'Филиал тест'")
    def select_filial(self):
        try:
            select_custom_dropdown(self.driver, self.BRANCH_DROPDOWN_XPATH, self.BRANCH_OPTION_XPATH)
            time.sleep(1)
        except Exception as e:
            allure.attach(f"Ошибка при выборе филиала: {str(e)}",
                          name="Ошибка выбора филиала", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Выбираем автомобиль")
    def select_car(self):
        try:
            select_custom_dropdown(self.driver, self.CAR_DROPDOWN_XPATH, self.CAR_OPTION_XPATH)
        except Exception as e:
            allure.attach(f"Ошибка при выборе автомобиля: {str(e)}",
                          name="Ошибка выбора автомобиля", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Заполняем информацию об автомобиле")
    def fill_car_info(self, mileage: str, comment: str):
        try:
            self.find(By.ID, self.MILEAGE_ID).send_keys(mileage)
            comment_input = self.driver.find_element(By.ID, self.COMMENT_ID)
            comment_input.clear()
            comment_input.send_keys(comment)
            time.sleep(1)
        except Exception as e:
            allure.attach(f"Ошибка при заполнении информации об автомобиле: {str(e)}",
                          name="Ошибка заполнения авто", attachment_type=allure.attachment_type.TEXT)
            raise

    # with allure.step("Выбор состояния ТС"):
    #     select_custom_dropdown(
    #         driver,
    #         '//*[@id="088fa587fbac295705e7e561d778761bd353d683"]/fieldset/div[2]/div/fieldset/div/div[3]/div[1]/div/div/div/div[1]',
    #         "//div[@data-value='operated']"
    #     )
    @allure.step("Прикрепляем файл в заявку")
    def add_file_request_form(self):
        try:
            file_path = Path("tests/files/autotest_file.txt").resolve()
            assert file_path.exists(), f"Файл не найден: {file_path}"

            file_input = self.driver.find_element(By.XPATH,
                                                  '//*[@id="field-doc-files-df1bd9fe0dd490dfc71e27f75d7be3a830e73b8b"]')
            file_input.send_keys(str(file_path))
            time.sleep(1)

            files_count = self.driver.execute_script(
                "return arguments[0].files.length;", file_input
            )
            allure.attach(
                f"Файлов прикреплено: {files_count}",
                name="Результат загрузки",
                attachment_type=allure.attachment_type.TEXT
            )
            assert files_count > 0, "Файл не прикрепился!"

        except Exception as e:
            allure.attach(f"Ошибка при загрузке файла: {str(e)}",
                      name="Ошибка загрузки файла",
                       attachment_type=allure.attachment_type.TEXT
                       )
            raise e

    @allure.step("Сохраняем заявку")
    def save_request(self):
        try:
            button = self.find_clickable(By.XPATH, self.SAVE_BUTTON_XPATH)
            self.click(button)
        except Exception as e:
            allure.attach(f"Ошибка при сохранении заявки: {str(e)}",
                          name="Ошибка сохранения", attachment_type=allure.attachment_type.TEXT)
            raise e
        time.sleep(4)

    @allure.step("Закрываем уведомление")
    def close_notification(self):
        try:
            button = self.find_clickable(By.XPATH, self.NOTIFY_MODAL_CLOSE_ID)
            self.click(button)
        except Exception as e:
            allure.attach(f"Ошибка при закрытии уведомления: {str(e)}",
                          name="Ошибка закрытия уведомления", attachment_type=allure.attachment_type.TEXT)

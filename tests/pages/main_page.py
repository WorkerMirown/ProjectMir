import time

import allure
from selenium.webdriver.common.by import By
from ..pages.base_page import BasePage

class MainPage(BasePage):
    # --- Локаторы ---
    CLEAR_FILTERS_XPATH = '//button/span[text()="Сбросить фильтры"]'
    SEARCH_CONTAIBER_CSS = "#primary-group > div:nth-child(1) > div > div > div"

    SEARCH_BUTTON_CSS = "#d4d99a6b8c3c6f215e76b62117a1a9f361af5913 button"
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url

    @allure.step("Сброс фильтров")
    def clear_filters(self):
        try:
            button_clean = self.find_clickable(By.XPATH, '//button/span[text()="Сбросить фильтры"]')
            button_clean.click()
            time.sleep(2)
            return self
        except Exception as e:
            allure.attach(f"Ошибка при сбросе фильтров: {str(e)}",
                          name="Ошибка clear_filters",
                          attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Поиск заявки по ID")
    def search_request(self, request_id):

        try:
            self.clear_filters()
            search_container = self.find(By.CSS_SELECTOR, self.SEARCH_CONTAIBER_CSS)
            search_container.click()
            time.sleep(1)
            search_input = search_container.find_element(By.TAG_NAME, "input")
            search_input.send_keys(request_id)
            time.sleep(1)
            option = self.find_clickable(By.XPATH,
                                         f'//div[contains(@class,"ts-dropdown")]//div[@data-value="{request_id}"]')
            option.click()
            search_button = self.find(By.CSS_SELECTOR, self.SEARCH_BUTTON_CSS)
            self.click(search_button)

            return self
        except Exception as e:
            allure.attach(f"Ошибка при поиске заявки {request_id}: {str(e)}",
                          name="Ошибка search_request",
                          attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Открываем заявку по ID")
    def open_request_by_id(self, request_id):
        try:
            expected_href = f"/requests/{request_id}/edit"
            link = self.find_clickable(By.XPATH, f"//table//a[contains(@href,'/requests/{request_id}/edit')]")
            href = link.get_attribute("href")
            assert href == expected_href, f"Ожидали ссылку {expected_href}, но получили {href}"
            link.click()

            self.wait_for_url(expected_href)
            assert self.driver.current_url == expected_href

            return self
        except Exception as e:
            allure.attach(f"Ошибка при открытии заявки {request_id}: {str(e)}",
                          name="Ошибка open_request_by_id",
                          attachment_type=allure.attachment_type.TEXT)
            raise

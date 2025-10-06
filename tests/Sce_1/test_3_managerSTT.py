import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..pages.auth_page import AuthPage
from ..pages.main_page import MainPage
from ..pages.request_page import RequestPage

def load_request_id():
    with open("tests/data/request_id.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


@allure.feature("Перевод заявки менеджером СТТ")
@allure.story("Авторизация и поиск заявки")
def test_managerSTT_stuff(driver):

    main_page = MainPage(driver)
    request_page = RequestPage(driver)
    auth_page = AuthPage(driver)

    wait = WebDriverWait(driver, 15)
    request_id = load_request_id()

    with allure.step("Авторизация менеджера СТТ"):
        auth_page.login(email="managersttautomationtester@mail.ru", password="Test123!!#@")

    with allure.step(f"Поиск заявки по ID {request_id}"):

        main_page.search_request(request_id)
        main_page.open_request_by_id(request_id)
        request_page.open_first_defect(request_id)

    request_page.create_event("diagnostic_sto", "//input[starts-with(@id,'field-start-plan-datetime')]",
                              "//input[starts-with(@id,'field-end-plan-datetime')]", "diagnostic_sto")
    request_page.close_event("diagnostic_sto",
                             "//input[starts-with(@id,'field-start-fact-datetime')]",
                             "//input[starts-with(@id,'field-end-fact-datetime')]",
                             [
                                 '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[1]/div/div/div/label[2]',
                                 '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[2]/div/div/div/label[2]'])

    request_page.create_event("repair_car_sto",
                              "//input[starts-with(@id,'field-start-plan-datetime')]",
                              "//input[starts-with(@id,'field-end-plan-datetime')]", "repair_car_sto")
    request_page.close_event("repair_car_sto",
                             "//input[starts-with(@id,'field-start-fact-datetime')]",
                             "//input[starts-with(@id,'field-end-fact-datetime')]",
                             [
                                 '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div/div/label[2]'])
    # with allure.step("Закрытие мероприятия Диагностика"):
    #     table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
    #
    #     first_defect_link = table.find_element(By.CSS_SELECTOR, "tbody tr td a")
    #     driver.execute_script("arguments[0].scrollIntoView(true);", first_defect_link)
    #     driver.execute_script("arguments[0].click();", first_defect_link)
    #
    #     wait.until(EC.url_matches(r".*/defect/\d+(/.*)?"))
    #     print("Открыли дефект:", driver.current_url)
    #     fact_date_begin_box = wait.until(EC.element_to_be_clickable((
    #             By.ID, "field-start-fact-datetime-00495780d10df3b9335245635c754fc567320b9d"
    #         )))
    #     fact_date_begin_box.click()
    #
    #     calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
    #     today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
    #     today_begin.click()
    #
    #     fact_date_end_box = wait.until(EC.element_to_be_clickable((
    #         By.ID, "field-end-fact-datetime-ea53c49d1be0dbd9d90d113c86c536348297b934"
    #     )))
    #     fact_date_end_box.click()
    #
    #     calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
    #     today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
    #     today_end.click()
    #     driver.find_element(By.XPATH, '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[1]/div/div/div/label[2]').click()
    #     driver.find_element(By.XPATH, '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[2]/div/div/div/label[2]').click()
    #     driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
    #     button_end_event = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmBtnModalSend"]')))
    #     button_end_event.click()
    #     driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
    #     print("Мероприятие Диагностика завершено:")
    #     time.sleep(4)
    #
    # with allure.step("Ремонт ТС на СТО"):
    #     event_button = wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, "//a[@class='btn  btn-success'][.//span[normalize-space(text())='Создать мероприятие']]")))
    #     event_button.click()
    #     #driver.find_element(By.XPATH, '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div').click()
    #
    #     dropdown = wait.until(EC.element_to_be_clickable((
    #         By.XPATH, '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div'
    #     )))
    #     dropdown.click()
    #
    #     even_container_repair = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="option" and @data-value="repair_car_sto"]')))
    #     driver.execute_script("arguments[0].scrollIntoView(true);", even_container_repair)
    #     time.sleep(0.5)
    #     even_container_repair.click()
    #
    #     plane_date_begin_box = wait.until(EC.element_to_be_clickable((
    #         By.ID, "field-start-plan-datetime-925e03aea49a5862299682d6d5f8912b13992af2"
    #     )))
    #     plane_date_begin_box.click()
    #
    #     calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
    #     today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
    #     today_begin.click()
    #
    #     plane_date_end_box = wait.until(EC.element_to_be_clickable((
    #         By.ID, "field-end-plan-datetime-de7d93c5a575e5d6ebaa4ea1db086b1081576b5b"
    #     )))
    #     plane_date_end_box.click()
    #
    #     calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
    #     today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
    #     today_end.click()
    #     driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
    #     driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
    #     print("Создано мероприятие:")
    #
    #
    # with allure.step("Ремонт ТС на СТО"):
    #
    #     table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
    #     first_defect_link = table.find_element(By.CSS_SELECTOR, "tbody tr td a")
    #     driver.execute_script("arguments[0].scrollIntoView(true);", first_defect_link)
    #     driver.execute_script("arguments[0].click();", first_defect_link)
    #
    #     wait.until(EC.url_matches(r".*/defect/\d+(/.*)?"))
    #     print("Открыли дефект:", driver.current_url)
    #     fact_date_begin_box = wait.until(EC.element_to_be_clickable((
    #             By.ID, "field-start-fact-datetime-00495780d10df3b9335245635c754fc567320b9d"
    #         )))
    #     fact_date_begin_box.click()
    #     time.sleep(0.5)
    #
    #     calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
    #     today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
    #     today_begin.click()
    #
    #     fact_date_end_box = wait.until(EC.element_to_be_clickable((
    #         By.ID, "field-end-fact-datetime-ea53c49d1be0dbd9d90d113c86c536348297b934"
    #     )))
    #     fact_date_end_box.click()
    #     calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
    #     today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
    #     today_end.click()
    #     driver.find_element(By.XPATH, '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div/div/label[2]').click()
    #     driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
    #     button_end_event = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmBtnModalSend"]')))
    #     button_end_event.click()
    #     driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
    #     print("Мероприятие Ремонт завершено:")
    #
    #     driver.get(f'https://carsrv-test.st.tech/requests/{request_id}')
    #     time.sleep(4)
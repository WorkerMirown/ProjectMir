import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def load_request_id():
    with open("tests/data/request_id.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


@allure.feature("Перевод заявки менеджером СТТ")
@allure.story("Авторизация и поиск заявки")
def test_managerSTT_stuff(driver):
    wait = WebDriverWait(driver, 15)
    request_id = load_request_id()

    with allure.step("Авторизация менеджера СТТ"):
        driver.get("https://carsrv-test.st.tech/login")
        driver.find_element(
            By.XPATH, '//*[@id="field-email-5e954ef1842b8d480aef9b541930f0cb444c24cb"]'
        ).send_keys("managersttautomationtester@mail.ru")
        driver.find_element(
            By.XPATH, '//*[@id="field-password-6e375a8c5cee60d33bd060d76dc97dca59fb6920"]'
        ).send_keys("Test123!!#@")
        driver.find_element(By.ID, "button-login").click()
        wait.until(lambda d: d.current_url.endswith("/profile") or d.current_url.endswith("/main"))
        assert driver.current_url.endswith("/profile") or driver.current_url.endswith("/main")

    with allure.step("Переход в список заявок"):
        driver.get("https://carsrv-test.st.tech/main")
    time.sleep(2)

    with allure.step(f"Поиск заявки по ID {request_id}"):

        clearFilterButton = driver.find_element(By.XPATH,'//*[@id="d4d99a6b8c3c6f215e76b62117a1a9f361af5913"]//button/span[text()="Сбросить фильтры"]')
        clearFilterButton.click()
        time.sleep(2)

        search_container = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary-group > div:nth-child(1) > div > div > div"))
        )
        search_input = search_container.find_element(By.TAG_NAME, "input")
        search_input.send_keys(request_id)

        option = wait.until(
            EC.visibility_of_element_located((By.XPATH, f'//div[contains(@class,"ts-dropdown")]//div[@data-value="{request_id}"]')))
        option.click()

        search_button = driver.find_element(By.CSS_SELECTOR, "#d4d99a6b8c3c6f215e76b62117a1a9f361af5913 button")
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        driver.execute_script("arguments[0].click();", search_button)


    with allure.step("Проверка, что заявка найдена и открыта"):

        expected_href = f"https://carsrv-test.st.tech/requests/{request_id}/edit"
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//table//a[contains(@href,'/requests/{request_id}/edit')]")
            )
        )
        href = link.get_attribute("href")

        assert href == expected_href, f"Ожидали ссылку {expected_href}, но получили {href}"
        print("Ссылка совпала:", href)

        link.click()
        WebDriverWait(driver, 10).until(EC.url_to_be(expected_href))
        assert driver.current_url == expected_href
        print("Переход успешен:", driver.current_url)

    with allure.step("Открыли дефект"):
        driver.get(f'https://carsrv-test.st.tech/requests/{request_id}/defects')

        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

        first_defect_link = table.find_element(By.CSS_SELECTOR, "tbody tr td a")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_defect_link)
        driver.execute_script("arguments[0].click();", first_defect_link)

        wait.until(EC.url_matches(r".*/defect/\d+(/.*)?"))
        print("Открыли дефект:", driver.current_url)

    with allure.step("Создание мероприятия Диагностика"):

        event_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn  btn-success'][.//span[normalize-space(text())='Создать мероприятие']]")))
        event_button.click()
        driver.find_element(By.XPATH, '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div').click()

        even_container_diagnostic = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="option" and @data-value="diagnostic_sto"]')))
        even_container_diagnostic.click()

        plane_date_begin_box = wait.until(EC.element_to_be_clickable((
            By.ID, "field-start-plan-datetime-27880608c1ce3a90b7d6f71f284bd7c1784f5864"
        )))
        plane_date_begin_box.click()

        calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_begin.click()

        plane_date_end_box = wait.until(EC.element_to_be_clickable((
            By.ID, "field-end-plan-datetime-52a0ba72e1d162883a9abb0d62033daf3380b0d4"
        )))
        plane_date_end_box.click()

        calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_end.click()
        driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
        driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
        print("Создано мероприятие:")

    with allure.step("Закрытие мероприятия Диагностика"):
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

        first_defect_link = table.find_element(By.CSS_SELECTOR, "tbody tr td a")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_defect_link)
        driver.execute_script("arguments[0].click();", first_defect_link)

        wait.until(EC.url_matches(r".*/defect/\d+(/.*)?"))
        print("Открыли дефект:", driver.current_url)
        fact_date_begin_box = wait.until(EC.element_to_be_clickable((
                By.ID, "field-start-fact-datetime-00495780d10df3b9335245635c754fc567320b9d"
            )))
        fact_date_begin_box.click()

        calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_begin.click()

        fact_date_end_box = wait.until(EC.element_to_be_clickable((
            By.ID, "field-end-fact-datetime-ea53c49d1be0dbd9d90d113c86c536348297b934"
        )))
        fact_date_end_box.click()

        calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_end.click()
        driver.find_element(By.XPATH, '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[1]/div/div/div/label[2]').click()
        driver.find_element(By.XPATH, '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div[2]/div/div/div/label[2]').click()
        driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
        button_end_event = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmBtnModalSend"]')))
        button_end_event.click()
        driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
        print("Мероприятие Диагностика завершено:")
        time.sleep(4)

    with allure.step("Ремонт ТС на СТО"):
        event_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='btn  btn-success'][.//span[normalize-space(text())='Создать мероприятие']]")))
        event_button.click()
        #driver.find_element(By.XPATH, '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div').click()

        dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div'
        )))
        dropdown.click()

        even_container_repair = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="option" and @data-value="repair_car_sto"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", even_container_repair)
        time.sleep(0.5)
        even_container_repair.click()

        plane_date_begin_box = wait.until(EC.element_to_be_clickable((
            By.ID, "field-start-plan-datetime-925e03aea49a5862299682d6d5f8912b13992af2"
        )))
        plane_date_begin_box.click()

        calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_begin.click()

        plane_date_end_box = wait.until(EC.element_to_be_clickable((
            By.ID, "field-end-plan-datetime-de7d93c5a575e5d6ebaa4ea1db086b1081576b5b"
        )))
        plane_date_end_box.click()

        calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_end.click()
        driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
        driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
        print("Создано мероприятие:")


    with allure.step("Ремонт ТС на СТО"):

        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
        first_defect_link = table.find_element(By.CSS_SELECTOR, "tbody tr td a")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_defect_link)
        driver.execute_script("arguments[0].click();", first_defect_link)

        wait.until(EC.url_matches(r".*/defect/\d+(/.*)?"))
        print("Открыли дефект:", driver.current_url)
        fact_date_begin_box = wait.until(EC.element_to_be_clickable((
                By.ID, "field-start-fact-datetime-00495780d10df3b9335245635c754fc567320b9d"
            )))
        fact_date_begin_box.click()
        time.sleep(0.5)

        calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_begin.click()

        fact_date_end_box = wait.until(EC.element_to_be_clickable((
            By.ID, "field-end-fact-datetime-ea53c49d1be0dbd9d90d113c86c536348297b934"
        )))
        fact_date_end_box.click()
        calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        today_end.click()
        driver.find_element(By.XPATH, '//*[@id="33b64acde690b1edfa20240b3ece4b9ef519cc23"]/fieldset[2]/div/div[6]/div/div/label[2]').click()
        driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
        button_end_event = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmBtnModalSend"]')))
        button_end_event.click()
        driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
        print("Мероприятие Ремонт завершено:")

        driver.get(f'https://carsrv-test.st.tech/requests/{request_id}')
        time.sleep(4)
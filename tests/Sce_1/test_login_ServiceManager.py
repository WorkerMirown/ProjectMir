import time
import allure
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_request_id():
    data_file = Path(__file__).parent.parent / "data" / "request_id.txt"
    return data_file.read_text(encoding="utf-8").strip()
@allure.feature("Перевод заявки Сервис менеджер")
@allure.story("Авторизация и поиск заявки")
def test_find_request_by_id(driver):
    wait = WebDriverWait(driver, 15)
    request_id = load_request_id()

    with allure.step("Авторизация Сервис менеджер"):
        driver.get("https://carsrv-test.st.tech/login")
        driver.find_element(
            By.XPATH, '//*[@id="field-email-5e954ef1842b8d480aef9b541930f0cb444c24cb"]'
        ).send_keys("workerismirown@gmail.com")
        driver.find_element(
            By.XPATH, '//*[@id="field-password-6e375a8c5cee60d33bd060d76dc97dca59fb6920"]'
        ).send_keys("eA123!@#")
        driver.find_element(By.ID, "button-login").click()
        wait.until(lambda d: d.current_url.endswith("/profile") or d.current_url.endswith("/main"))
        assert driver.current_url.endswith("/profile") or driver.current_url.endswith("/main")

    with allure.step("Переход в список заявок"):
        driver.get("https://carsrv-test.st.tech/main")
    time.sleep(2)

    with allure.step(f"Поиск заявки по ID {request_id}"):
        clearFilterButton = driver.find_element(By.XPATH,
                                                '//*[@id="d4d99a6b8c3c6f215e76b62117a1a9f361af5913"]//button/span[text()="Сбросить фильтры"]')
        clearFilterButton.click()
        time.sleep(2)

        search_container = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary-group > div:nth-child(1) > div > div > div"))
        )
        search_input = search_container.find_element(By.TAG_NAME, "input")
        search_input.send_keys(request_id)

        option = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//div[contains(@class,"ts-dropdown")]//div[@data-value="{request_id}"]')))
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
        driver.get(f'https://carsrv-test.st.tech/requests/{request_id}/defects')
        defect_button = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="post-form"]/fieldset/div/div[1]/div/div/button[2]')
            )
        )
        defect_button.click()
        defect_name = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="field-title-ebf918a9a9e04da5679f0433b2244bba9f4238eb"]')))
        defect_name.click()
        defect_name.send_keys('TestDefectAuto')
        service_point_container = driver.find_element(
            By.XPATH, '//*[@id="post-form"]/fieldset/div/div[5]/div/div/div[1]'
        )
        service_point_container.click()
        time.sleep(1)

        service_point = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="field-id-sto-644af5b32c759451a3cc0904a19e334488a267a4-opt-2"]')
            )
        )
        service_point.click()

        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/nav/ul/li[2]/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()
        driver.get('https://carsrv-test.st.tech/requests/2122/defects')
        print('Дефект создан, отправлен на СТО')
        time.sleep(3)
        #driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/nav/ul/li/div/button')

        #driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/nav/ul/li/div/button').click()
        #driver.find_element(By.XPATH, '//*[@id="notifyModalClose"]').click()

        # event_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/div/nav/ul/li[2]/div/a')))
        # event_button.click()
        # driver.find_element(By.XPATH, '//*[@id="c245bdf8c7f876a95ffe440dd8494ce0a2fa0453"]/fieldset/div/div[3]/div[1]/div').click()
        #
        # even_container_diagnostic = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="option" and @data-value="diagnostic_sto"]')))
        # even_container_diagnostic.click()
        #
        # plane_date_begin_box = wait.until(EC.element_to_be_clickable((
        #     By.ID, "field-start-plan-datetime-27880608c1ce3a90b7d6f71f284bd7c1784f5864"
        # )))
        # plane_date_begin_box.click()
        #
        # calendar_begin = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        # today_begin = calendar_begin.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        # today_begin.click()
        #
        # plane_date_end_box = wait.until(EC.element_to_be_clickable((
        #     By.ID, "field-end-plan-datetime-52a0ba72e1d162883a9abb0d62033daf3380b0d4"
        # )))
        # plane_date_end_box.click()
        #
        # calendar_end = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flatpickr-calendar.open")))
        # today_end = calendar_end.find_element(By.CSS_SELECTOR, ".flatpickr-day.today")
        # today_end.click()
        #
        # driver.find_element(By.XPATH, '//*[@id="post-form"]/fieldset/div/div/button[2]').click()
        # time.sleep(4)
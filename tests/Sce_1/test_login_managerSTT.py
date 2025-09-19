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
def test_find_request_by_id(driver):
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

        # Жмём кнопку "Поиск"
        search_button = driver.find_element(By.CSS_SELECTOR, "#d4d99a6b8c3c6f215e76b62117a1a9f361af5913 button")
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        driver.execute_script("arguments[0].click();", search_button)


    with allure.step("Проверка, что заявка найдена и открыта"):
        # ждём, пока ссылка на единственную заявку появится
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//table//a[contains(@href,'/requests/{request_id}/edit')]")
            )
        )

        # получаем href для проверки
        href = link.get_attribute("href")

        # проверяем, что href содержит нужный request_id
        assert f"/requests/{request_id}/edit" in href, f"Ссылка на заявку неправильная: {href}"
        time.sleep(3)
        # кликаем на ссылку через JS (на случай overlay'ей или проблем с кликабельностью)
        driver.execute_script("arguments[0].click();", link)
        time.sleep(3)
        # проверяем, что текущий URL соответствует ожиданиям
        WebDriverWait(driver, 10).until(lambda d: d.current_url.endswith(f"/requests/{request_id}/edit"))
        assert driver.current_url.endswith(
            f"/requests/{request_id}/edit"), f"Не перешли на страницу заявки {request_id}"

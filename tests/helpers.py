# helpers.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def select_custom_dropdown(driver, dropdown_xpath, option_xpath, timeout=15):
    """
    Выбирает опцию из кастомного дропдауна (не <select>) по XPATH.
    dropdown_xpath - XPATH элемента дропдауна для клика
    option_xpath   - XPATH нужной опции внутри дропдауна
    """
    wait = WebDriverWait(driver, timeout)

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    dropdown.click()

    option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
    driver.execute_script("arguments[0].scrollIntoView(true);", option)
    option.click()

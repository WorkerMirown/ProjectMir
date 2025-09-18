import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def request_storage(tmp_path_factory):
    file = tmp_path_factory.mktemp("data") / "request_id.txt"
    return file

@pytest.fixture
def save_request_id(request_storage):
    def _save(request_id: str):
        request_storage.write_text(request_id)
    return _save

@pytest.fixture
def load_request_id(request_storage):
    def _load():
        return request_storage.read_text().strip()
    return _load
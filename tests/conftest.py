import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

BASE = Path(__file__).parent            # это tests/
DATA_DIR = BASE / "data"
REQUEST_FILE = DATA_DIR / "request_id.txt"

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="session", autouse=False)
def data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR

@pytest.fixture
def save_request_id_file(data_dir):
    def _save(request_id: str, name: str = "request"):
        p = data_dir / f"request_id_{name}.txt"
        p.write_text(request_id, encoding="utf-8")
        return p
    return _save

@pytest.fixture
def load_request_id_file(data_dir):
    def _load(name: str = "request"):
        p = data_dir / f"request_id_{name}.txt"
        if not p.exists():
            raise FileNotFoundError(f"{p} not found. Run producer test first.")
        return p.read_text(encoding="utf-8").strip()
    return _load

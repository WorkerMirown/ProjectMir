import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE = Path(__file__).parent            # это tests/
DATA_DIR = BASE / "data"
REQUEST_FILE = DATA_DIR / "request_id.txt"

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="test",
        help="Environment to run tests against: test/stage/prod"
    )


@pytest.fixture
def driver(pytestconfig):
    chrome_options = Options()
    if pytestconfig.getoption("--headless"):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(10)

    # maximize не нужен в headless
    if not pytestconfig.getoption("--headless"):
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


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    env = pytestconfig.getoption("--base-url")
    urls = {
        "test": "https://carsrv-test.st.tech",
        "stage": "https://carsrv-stage.st.tech",
    }

    if env not in urls:
        raise ValueError(f"Unknown environment: {env}. Choose from {', '.join(urls.keys())}")

    return urls[env]
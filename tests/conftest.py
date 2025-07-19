import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import config
from utils.helpers import TestHelpers
from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def browser_setup():
    """Setup browser driver"""
    if config.BROWSER.lower() == "firefox":
        options = FirefoxOptions()
        if config.HEADLESS:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:  # Default to Chrome
        options = ChromeOptions()
        if config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    driver.implicitly_wait(config.IMPLICIT_WAIT)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

@pytest.fixture
def driver(browser_setup):
    """Provide driver instance for each test"""
    yield browser_setup

@pytest.fixture
def login_page(driver):
    """Provide login page instance"""
    return LoginPage(driver)

@pytest.fixture(autouse=True)
def test_setup_teardown(request, driver):
    """Setup and teardown for each test"""
    # Setup
    test_name = request.node.name
    print(f"\n--- Starting test: {test_name} ---")
    
    yield
    
    # Teardown
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        if config.SCREENSHOT_ON_FAILURE:
            TestHelpers.take_screenshot(driver, f"FAILED_{test_name}")
    
    print(f"--- Finished test: {test_name} ---")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
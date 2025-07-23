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
from pages.transaction_page import TransactionPage
from utils.test_data import TestData
import time

def get_browser():
    """Helper function to create a new browser instance"""
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
        # Basic Chrome options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # GPU related options to prevent errors
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        # Additional options to reduce errors and warnings
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-notifications")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    driver.implicitly_wait(config.IMPLICIT_WAIT)
    driver.maximize_window()
    return driver

@pytest.fixture(scope="class")
def login_driver(request):
    """Dedicated driver for login tests"""
    driver = get_browser()
    request.cls.driver = driver  # Attach driver to test class
    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def transaction_driver(request):
    """Dedicated driver for transaction tests"""
    driver = get_browser()
    request.cls.driver = driver  # Attach driver to test class
    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def login_page(login_driver):
    """Provide login page instance"""
    return LoginPage(login_driver)

@pytest.fixture(scope="class")
def transaction_page(transaction_driver):
    """Provide transaction page instance with login handled"""
    # Create login page with the transaction driver
    login_page = LoginPage(transaction_driver)
    
    # Perform login
    login_page.navigate_to_login()
    credentials = TestData.VALID_USER
    login_page.login(credentials.username, credentials.password)
    
    # Wait for login to complete
    assert login_page.is_login_successful(), "Login failed, cannot proceed to transaction page"
    time.sleep(2)  # Allow time for redirect
    
    # Return transaction page instance
    return TransactionPage(transaction_driver)

@pytest.fixture(autouse=True)
def test_setup_teardown(request):
    """Setup and teardown for each test"""
    # Setup
    test_name = request.node.name
    print(f"\n--- Starting test: {test_name} ---")
    
    try:
        yield
    finally:
        try:
            # Get the appropriate driver based on the test
            driver = None
            if hasattr(request, 'fixturenames'):
                if 'login_page' in request.fixturenames:
                    driver = request.getfixturevalue('login_driver')
                elif 'transaction_page' in request.fixturenames:
                    driver = request.getfixturevalue('transaction_driver')
            
            # Take screenshot if test failed
            if driver and hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                if config.SCREENSHOT_ON_FAILURE:
                    try:
                        TestHelpers.take_screenshot(driver, f"FAILED_{test_name}")
                    except Exception as e:
                        print(f"Failed to take screenshot: {str(e)}")
        except Exception as e:
            print(f"Error in test teardown: {str(e)}")
        finally:
            print(f"--- Finished test: {test_name} ---")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
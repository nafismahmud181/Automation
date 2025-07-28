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
import signal
import threading

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("ChromeDriver download timed out")

def get_browser_with_timeout(timeout=120):  # 2 minutes timeout
    """Helper function to create a new browser instance with timeout"""
    
    def create_driver():
        if config.BROWSER.lower() == "firefox":
            options = FirefoxOptions()
            if config.HEADLESS:
                options.add_argument("--headless")
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
        else:
            options = ChromeOptions()
            if config.HEADLESS:
                options.add_argument("--headless")
            
            # Enhanced Chrome options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-extensions")
            options.add_argument("--remote-debugging-port=9222")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Try multiple approaches
            try:
                # First try: specific stable version
                print("Attempting to use ChromeDriver version 135.0.6930.71...")
                service = Service(ChromeDriverManager(version="135.0.6930.71").install())
                return webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"Specific version failed: {e}")
                try:
                    # Second try: latest version with timeout
                    print("Attempting to use latest ChromeDriver...")
                    service = Service(ChromeDriverManager().install())
                    return webdriver.Chrome(service=service, options=options)
                except Exception as e2:
                    print(f"Latest version failed: {e2}")
                    # Third try: Let Selenium Manager handle it
                    print("Falling back to Selenium Manager...")
                    return webdriver.Chrome(options=options)
    
    # Use threading to implement timeout
    driver = None
    exception = None
    
    def driver_creation():
        nonlocal driver, exception
        try:
            driver = create_driver()
        except Exception as e:
            exception = e
    
    thread = threading.Thread(target=driver_creation)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        print(f"ChromeDriver creation timed out after {timeout} seconds")
        # Force kill any hanging processes
        import subprocess
        try:
            subprocess.run(["taskkill", "/f", "/im", "chromedriver.exe"], 
                         capture_output=True, check=False)
        except:
            pass
        raise TimeoutError(f"ChromeDriver creation timed out after {timeout} seconds")
    
    if exception:
        raise exception
    
    if driver:
        driver.implicitly_wait(config.IMPLICIT_WAIT)
        driver.maximize_window()
        return driver
    else:
        raise Exception("Failed to create driver")

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
        
        try:
            # Try using a stable ChromeDriver version (135.x)
            print("Attempting to use ChromeDriver version 135.0.6930.71...")
            service = Service(ChromeDriverManager(version="135.0.6930.71").install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Specific version failed, trying Selenium Manager: {e}")
            # Fallback to Selenium Manager (no webdriver-manager)
            driver = webdriver.Chrome(options=options)
    
    driver.implicitly_wait(config.IMPLICIT_WAIT)
    driver.maximize_window()
    return driver

# Rest of the fixtures remain the same...
@pytest.fixture(scope="class")
def login_driver(request):
    """Dedicated driver for login tests"""
    driver = get_browser()
    request.cls.driver = driver
    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def transaction_driver(request):
    """Dedicated driver for transaction tests"""
    driver = get_browser()
    request.cls.driver = driver
    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def login_page(login_driver):
    """Provide login page instance"""
    return LoginPage(login_driver)

@pytest.fixture(scope="class")
def transaction_page(transaction_driver):
    """Provide transaction page instance with login handled"""
    login_page = LoginPage(transaction_driver)
    login_page.navigate_to_login()
    credentials = TestData.VALID_USER
    login_page.login(credentials.username, credentials.password)
    assert login_page.is_login_successful(), "Login failed, cannot proceed to transaction page"
    time.sleep(2)
    return TransactionPage(transaction_driver)

@pytest.fixture(autouse=True)
def test_setup_teardown(request):
    """Setup and teardown for each test"""
    test_name = request.node.name
    print(f"\n--- Starting test: {test_name} ---")
    
    try:
        yield
    finally:
        try:
            driver = None
            if hasattr(request, 'fixturenames'):
                if 'login_page' in request.fixturenames:
                    driver = request.getfixturevalue('login_driver')
                elif 'transaction_page' in request.fixturenames:
                    driver = request.getfixturevalue('transaction_driver')
            
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
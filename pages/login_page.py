from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    USERNAME_INPUT = (By.XPATH, "//input[@id='login-username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='login-password']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Sign in']")
    
    # Error message locators
    ERROR_MESSAGE = (By.XPATH, "//div[@class='alert-body']//p")

    # Page title locator
    PAGE_TITLE = (By.XPATH, "//h2[normalize-space()='Welcome to Data Definitions Editor']")
    
    # Field validation error locators
    USERNAME_VALIDATION_ERROR = (By.XPATH, "//small[normalize-space()='The Username field is required']")
    PASSWORD_VALIDATION_ERROR = (By.XPATH, "//small[normalize-space()='The Password field is required']")
    
    # Generic validation error locators (more flexible)
    USERNAME_ERROR_GENERIC = (By.XPATH, "//input[@id='login-username']/following-sibling::small[@class='text-danger']")
    PASSWORD_ERROR_GENERIC = (By.XPATH, "//input[@id='login-password']/../..//small[@class='text-danger']")
    
    # All validation errors at once
    ALL_VALIDATION_ERRORS = (By.XPATH, "//small[@class='text-danger']")
    
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    LOADING_SPINNER = (By.CLASS_NAME, "loading-spinner")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{config.BASE_URL}/login"
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.driver.get(self.url)
    
    def enter_username(self, username: str):
        """Enter username"""
        self.send_keys(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str):
        """Enter password"""
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """Get general error message text (for invalid credentials)"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_username_validation_error(self) -> str:
        """Get username field validation error"""
        if self.is_element_present(self.USERNAME_VALIDATION_ERROR):
            return self.get_text(self.USERNAME_VALIDATION_ERROR)
        return ""
    
    def get_password_validation_error(self) -> str:
        """Get password field validation error"""
        if self.is_element_present(self.PASSWORD_VALIDATION_ERROR):
            return self.get_text(self.PASSWORD_VALIDATION_ERROR)
        return ""
    
    def get_all_validation_errors(self) -> list:
        """Get all validation error messages"""
        errors = []
        elements = self.find_elements(self.ALL_VALIDATION_ERRORS)
        for element in elements:
            errors.append(element.text)
        return errors

    
    def has_validation_errors(self) -> bool:
        """Check if any validation errors are present"""
        return len(self.get_all_validation_errors()) > 0
    
    def get_any_error_message(self) -> str:
        """Get any error message (validation or general)"""

        validation_errors = self.get_all_validation_errors()
        if validation_errors:
            return "; ".join(validation_errors)

        return self.get_error_message()
    
    def get_page_title_element_text(self) -> str:
        """Get the page title from h2 element"""
        if self.is_element_present(self.PAGE_TITLE):
            return self.get_text(self.PAGE_TITLE)
        return ""
    
    def get_page_title(self) -> str:
        """Get browser page title (from <title> tag)"""
        return self.driver.title
    
    def get_page_heading(self) -> str:
        """Get page heading text"""
        return self.get_page_title_element_text()
    
    def login(self, username: str, password: str, remember_me: bool = False):
        """Perform complete login action"""
        self.enter_username(username)
        self.enter_password(password)
        
        if remember_me:
            self.check_remember_me()
        
        self.click_login_button()
    
    def is_login_successful(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[normalize-space()='Transactions']"))
            )
            return True
        except:
            return False
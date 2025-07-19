from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import config


class LoginPage(BasePage):
    # Locators - UPDATE THESE TO MATCH YOUR APPLICATION
    # Example locator options:
    
    # Option 1: Using ID (most reliable)
    USERNAME_INPUT = (By.ID, "username")  # Change "username" to your field's ID
    PASSWORD_INPUT = (By.ID, "password")  # Change "password" to your field's ID
    LOGIN_BUTTON = (By.ID, "login-button")  # Change to your button's ID
    
    # Option 2: Using XPath (if no ID available)
    # USERNAME_INPUT = (By.XPATH, "//input[@name='username']")
    # PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    # LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    # LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")
    
    # Option 3: Using CSS Selector
    # USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    # PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    # LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login-btn")
    
    # Option 4: Using Name attribute
    # USERNAME_INPUT = (By.NAME, "username")
    # PASSWORD_INPUT = (By.NAME, "password")
    
    # Other elements - update these too
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    # Alternative: REMEMBER_ME_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")
    
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    # Alternative: FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Forgot')]")
    
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    # Alternative: ERROR_MESSAGE = (By.XPATH, "//div[@class='error-message']")
    # Alternative: ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    
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
    
    def check_remember_me(self):
        """Check remember me checkbox"""
        checkbox = self.find_element(self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
    
    def click_forgot_password(self):
        """Click forgot password link"""
        self.click(self.FORGOT_PASSWORD_LINK)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_success_message(self) -> str:
        """Get success message text"""
        if self.is_element_present(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    def is_loading_spinner_visible(self) -> bool:
        """Check if loading spinner is visible"""
        return self.is_element_present(self.LOADING_SPINNER, timeout=2)
    
    def login(self, username: str, password: str, remember_me: bool = False):
        """Perform complete login action"""
        self.enter_username(username)
        self.enter_password(password)
        
        if remember_me:
            self.check_remember_me()
        
        self.click_login_button()
    
    def is_login_successful(self) -> bool:
        """Check if login was successful by checking URL change or success message"""
        try:
            # Wait for either success message or URL change
            return (self.is_element_present(self.SUCCESS_MESSAGE) or 
                   "dashboard" in self.get_current_url().lower())
        except:
            return False
    
    def get_username_field_value(self) -> str:
        """Get current value in username field"""
        element = self.find_element(self.USERNAME_INPUT)
        return element.get_attribute("value")
    
    def get_password_field_value(self) -> str:
        """Get current value in password field"""
        element = self.find_element(self.PASSWORD_INPUT)
        return element.get_attribute("value")
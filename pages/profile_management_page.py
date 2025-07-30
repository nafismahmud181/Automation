import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import config
from selenium.common.exceptions import TimeoutException

class ProfileManagementPage(BasePage):
    # Navigation Menu Locators
    TRANSACTION_MENU = (By.XPATH, "//*[@data-id='nav-group-toggle-home']")
    
    # Profile Management Links
    MANAGE_PROFILE_LINK = (By.XPATH, "//*[@data-id='nav-group-item-profile-management']/a")
    # MANAGE_PROFILES_LINK = (By.LINK_TEXT, "Manage Profiles")
    # VIEW_PROFILES_LINK = (By.LINK_TEXT, "View Profiles")
    
    # Create Profile Page Elements
    
    PROFILE_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@name='description' or @id='description']")
    PROFILE_TYPE_DROPDOWN = (By.XPATH, "//select[@name='profile_type' or @id='profile-type']")
    
    # Form Buttons
    SAVE_PROFILE_BUTTON = (By.XPATH, "//button[normalize-space()='Save Profile' or normalize-space()='Save']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space()='Reset']")
    
    # Success/Error Messages
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'alert-success') or contains(@class, 'success')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'alert-danger') or contains(@class, 'error')]")
    VALIDATION_ERRORS = (By.XPATH, "//small[@class='text-danger'] | //div[@class='invalid-feedback']")
    
    # Page Title/Header
    # PAGE_TITLE = (By.XPATH, "//h2[normalize-space()='Profile Management']")
    PROFILE_MANAGEMENT_HEADER = (By.XPATH, "//h1[normalize-space()='Create Profile'] | //h2[normalize-space()='Create Profile']")
    
    # Loading Elements
    LOADING_SPINNER = (By.CLASS_NAME, "loading-spinner")
    LOADING_OVERLAY = (By.XPATH, "//div[contains(@class, 'loading')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{config.BASE_URL}/profiles" 
        self.action = ActionChains(driver)

    def navigate_to_transaction_menu(self):
        """Navigate to and hover over the transaction menu"""
        try:
            # Wait for the transaction menu to be present
            wait = WebDriverWait(self.driver, 100)
            transaction_menu = wait.until(
                EC.presence_of_element_located(self.TRANSACTION_MENU)
            )
            
            # Hover over the transaction menu to reveal submenu
            self.action.move_to_element(transaction_menu).perform()
            time.sleep(2)  # Allow submenu to appear
            
            return True
        except TimeoutException:
            return False

    def click_profile_management(self):
        """Click on Create Profile link from the menu"""
        try:
            # First navigate to transaction menu
            if not self.navigate_to_transaction_menu():
                raise Exception("Failed to access transaction menu")
            
            # Wait for Create Profile link to be clickable
            wait = WebDriverWait(self.driver, 100)
            profile_management_link = wait.until(
                EC.element_to_be_clickable(self.MANAGE_PROFILE_LINK)
            )
            
            # Click the Create Profile link
            profile_management_link.click()
            time.sleep(2)  # Allow page to load
            
            return True
        except TimeoutException:
            return False

    def navigate_to_profile_management_page(self):
        """Complete navigation to Create Profile page"""
        success = self.click_profile_management()
        if success:
            # Wait for create profile page to load
            self.wait_for_page_load()
        return success

    def wait_for_page_load(self, timeout=30):
        """Wait for the profile page to fully load"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            # Wait for either page title or form elements to be present
            wait.until(lambda driver: any([
                # self.is_element_present(self.PAGE_TITLE),
                self.is_element_present(self.PROFILE_MANAGEMENT_HEADER),
            ]))
            return True
        except TimeoutException:
            return False

    def is_profile_amanagement_page_loaded(self):
        """Check if Create Profile page is loaded"""
        return any([
            self.is_element_present(self.PROFILE_MANAGEMENT_HEADER),
            "create" in self.driver.current_url.lower() or "profiles" in self.driver.current_url.lower()
        ])

    # def fill_profile_name(self, profile_name: str):
    #     """Fill the profile name field"""
    #     try:
    #         wait = WebDriverWait(self.driver, 10)
    #         name_input = wait.until(EC.element_to_be_clickable(self.PROFILE_NAME_INPUT))
    #         name_input.clear()
    #         name_input.send_keys(profile_name)
    #         return True
    #     except TimeoutException:
    #         return False

    # def fill_profile_description(self, description: str):
    #     """Fill the profile description field"""
    #     try:
    #         wait = WebDriverWait(self.driver, 10)
    #         desc_input = wait.until(EC.element_to_be_clickable(self.PROFILE_DESCRIPTION_INPUT))
    #         desc_input.clear()
    #         desc_input.send_keys(description)
    #         return True
    #     except TimeoutException:
    #         return False

    # def select_profile_type(self, profile_type: str):
    #     """Select profile type from dropdown"""
    #     try:
    #         from selenium.webdriver.support.ui import Select
    #         wait = WebDriverWait(self.driver, 10)
    #         dropdown = wait.until(EC.element_to_be_clickable(self.PROFILE_TYPE_DROPDOWN))
    #         select = Select(dropdown)
    #         select.select_by_visible_text(profile_type)
    #         return True
    #     except (TimeoutException, Exception):
    #         return False

    # def click_save_profile(self):
    #     """Click the Save Profile button"""
    #     try:
    #         wait = WebDriverWait(self.driver, 10)
    #         save_button = wait.until(EC.element_to_be_clickable(self.SAVE_PROFILE_BUTTON))
    #         save_button.click()
    #         return True
    #     except TimeoutException:
    #         return False

    # def click_cancel_button(self):
    #     """Click the Cancel button"""
    #     try:
    #         wait = WebDriverWait(self.driver, 10)
    #         cancel_button = wait.until(EC.element_to_be_clickable(self.CANCEL_BUTTON))
    #         cancel_button.click()
    #         return True
    #     except TimeoutException:
    #         return False

    def get_success_message(self) -> str:
        """Get success message text"""
        if self.is_element_present(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""

    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def get_validation_errors(self) -> list:
        """Get all validation error messages"""
        errors = []
        try:
            elements = self.find_elements(self.VALIDATION_ERRORS)
            for element in elements:
                if element.text.strip():
                    errors.append(element.text.strip())
        except:
            pass
        return errors

    def has_validation_errors(self) -> bool:
        """Check if any validation errors are present"""
        return len(self.get_validation_errors()) > 0

    def get_any_message(self) -> str:
        """Get any message (success, error, or validation)"""
        # Check success message first
        success_msg = self.get_success_message()
        if success_msg:
            return success_msg
            
        # Check error message
        error_msg = self.get_error_message()
        if error_msg:
            return error_msg
            
        # Check validation errors
        validation_errors = self.get_validation_errors()
        if validation_errors:
            return "; ".join(validation_errors)
            
        return ""

    def wait_for_loading_complete(self, timeout=30):
        """Wait for any loading indicators to complete"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            # Wait for loading elements to disappear if they exist
            if self.is_element_present(self.LOADING_SPINNER):
                wait.until(EC.invisibility_of_element_located(self.LOADING_SPINNER))
            if self.is_element_present(self.LOADING_OVERLAY):
                wait.until(EC.invisibility_of_element_located(self.LOADING_OVERLAY))
        except TimeoutException:
            pass

    def is_profile_saved_successfully(self):
        """Check if profile was saved successfully"""
        self.wait_for_loading_complete()
        return bool(self.get_success_message()) and not self.has_validation_errors()


    # def get_page_title(self) -> str:
    #     """Get the current page title"""
    #     if self.is_element_present(self.PAGE_TITLE):
    #         return self.get_text(self.PAGE_TITLE)
    #     return self.driver.title

    def get_current_page_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
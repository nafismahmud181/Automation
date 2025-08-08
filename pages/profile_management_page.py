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

    
    PROFILE_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@name='description' or @id='description']")
    PROFILE_TYPE_DROPDOWN = (By.XPATH, "//select[@name='profile_type' or @id='profile-type']")

    #Input fields for Profile management details
    PROFILE_NAME_FIELD = (By.XPATH, "//*[@data-id='profiles-search-name']")

    CUSTOMER_NAME_FIELD = (By.XPATH, "//*[@data-id='profiles-search-customer-name']")
    CUSTOMER_NAME_RESULTS = (By.XPATH, "//td[contains(@data-id, 'profile-customer')]")

    EMAIL_SUBJECT_FIELD = (By.XPATH, "//*[@data-id='profiles-search-email-subject-match-text']")
    EMAIL_SUBJECT_RESULT = (By.XPATH, "//td[contains(@data-id, 'profile-email-subject')]")

    PROJECT_FIELD = (By.XPATH, "//*[@data-id='profiles-search-project']")
    PROJECT_FIELD_RESULT = (By.XPATH, "//td[contains(@data-id, 'profile-project')]")

    COUNTRY_FIELD = (By.XPATH, "//*[@data-id='profiles-search-country']")
    COUNTRY_FIELD_RESULT = (By.XPATH, "//td[contains(@data-id, 'profile-country')]")

    MODE_OF_TRANSPORT_FIELD = (By.XPATH, "//*[@data-id='profiles-search-mode-of-transport']")
    MODE_OF_TRANSPORT_RESULT = (By.XPATH, "//td[contains(@data-id, 'profile-transport')]")

    # Column Headers for sorting
    PROFILE_NAME_COLUMN_HEADER = (By.XPATH, "//*[@data-id='profiles-header-sort-name']")
    CUSTOMER_NAME_COLUMN_HEADER = (By.XPATH, "//*[@data-id='profiles-header-sort-customer_name']")
    EMAIL_SUBJECT_COLUMN_HEADER = (By.XPATH, "//*[@data-id='profiles-header-sort-email_subject_match_text']")
    PROJECT_COLUMN_HEADER = (By.XPATH, "//*[@data-id='profiles-header-sort-project']")
    COUNTRY_COLUMN_HEADER = (By.XPATH, "//*[@data-id='profiles-header-sort-country']")
    MODE_OF_TRANSPORT_COLUMN_HEADER = (By.XPATH, "//*[@data-id='profiles-header-sort-mode_of_transport']")
    UPDATED_DATE_COLUMN_HEADER = (By.XPATH, "//*[@data-id='profiles-header-sort-updated_at']")
    
    # Form Buttons
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//*[@data-id='profiles-button-clear-search']")

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

    def search_by_profile_name(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.PROFILE_NAME_FIELD))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_customer_name(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.CUSTOMER_NAME_FIELD))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_email_subject(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.EMAIL_SUBJECT_FIELD))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_project(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.PROJECT_FIELD))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_country(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.COUNTRY_FIELD))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_mode_of_transport(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.MODE_OF_TRANSPORT_FIELD))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def click_name_column_header(self):
        wait = WebDriverWait(self.driver, 10)
        name_header = wait.until(EC.element_to_be_clickable(self.PROFILE_NAME_COLUMN_HEADER))
        name_header.click()
        time.sleep(2)

    def click_curstomer_name_column_header(self):
        wait = WebDriverWait(self.driver, 10)
        name_header = wait.until(EC.element_to_be_clickable(self.CUSTOMER_NAME_COLUMN_HEADER))
        name_header.click()
        time.sleep(2)
   
    def click_email_subject_column_header(self):
        wait = WebDriverWait(self.driver, 10)
        name_header = wait.until(EC.element_to_be_clickable(self.EMAIL_SUBJECT_COLUMN_HEADER))
        name_header.click()
        time.sleep(2)
      
    def click_project_column_header(self):
        wait = WebDriverWait(self.driver, 10)
        name_header = wait.until(EC.element_to_be_clickable(self.PROJECT_COLUMN_HEADER))
        name_header.click()
        time.sleep(2)
       
    def click_country_column_header(self):
        wait = WebDriverWait(self.driver, 10)
        name_header = wait.until(EC.element_to_be_clickable(self.COUNTRY_COLUMN_HEADER))
        name_header.click()
        time.sleep(2)

    def click_mode_of_transport_column_header(self):
        wait = WebDriverWait(self.driver, 10)
        name_header = wait.until(EC.element_to_be_clickable(self.MODE_OF_TRANSPORT_COLUMN_HEADER))
        name_header.click()
        time.sleep(2)

    def click_updated_date_column_header(self):
        wait = WebDriverWait(self.driver, 10)
        name_header = wait.until(EC.element_to_be_clickable(self.UPDATED_DATE_COLUMN_HEADER))
        name_header.click()
        time.sleep(2)

    def is_search_successful(self) -> bool:
        """Check if a profile search returned a row with all required data-id fields"""
        required_fields = [
            "profile-name",
            "profile-customer",
            "profile-email-subject",
            "profile-project",
            "profile-country",
            "profile-transport",
        ]
        try:
            wait = WebDriverWait(self.driver, 10)
            # Wait for row to appear
            row = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-id^='profile-row']")))

            for field in required_fields:
                if not row.find_elements(By.CSS_SELECTOR, f"[data-id^='{field}']"):
                    print(f"Missing field: {field}")
                    return False
            return True
        except Exception as e:
            print(f"Search validation failed: {e}")
            return False

    def get_customer_name_results(self):
        """
        Get all customer names from search results
        Returns a list of customer names found in the search results.
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.CUSTOMER_NAME_RESULTS))
        return [el.text.strip() for el in elements]

    def get_email_subject_results(self):
        """
        Get all email subjects from search results
        Returns a list of email subjects found in the search results.
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.EMAIL_SUBJECT_RESULT))
        return [el.text.strip() for el in elements]

    def get_project_results(self):
        """
        Get all project names from search results
        Returns a list of project names found in the search results.
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.PROJECT_FIELD_RESULT))
        return [el.text.strip() for el in elements]

    def get_country_results(self):
        """
        Get all countries from search results
        Returns a list of countries found in the search results.
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.COUNTRY_FIELD_RESULT))
        return [el.text.strip() for el in elements]

    def get_mode_of_transport_results(self):
        """
        Get all mode of transport from search results
        Returns a list of mode of transport found in the search results.
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.MODE_OF_TRANSPORT_RESULT))
        return [el.text.strip() for el in elements]
    
    def get_profile_name_column_header_results(self):
        """"""
        

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
            self.action.move_by_offset(0, 0).perform()  # Adjust cursor position
            
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

    def get_current_page_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def click_clear_search_button(self):
        """
        Click the Go Back button after test is done
        """
        wait = WebDriverWait(self.driver, 10)
        clear_search_button = wait.until(EC.element_to_be_clickable(self.CLEAR_SEARCH_BUTTON))
        clear_search_button.click()

    def is_no_results_displayed(self):
            """
            Check if no results message is displayed by finding .text-center class
            """
            try:
                no_results_locator = (By.CSS_SELECTOR, ".text-center")
                result = self.is_element_present(no_results_locator)
                time.sleep(5)  # Wait for 5 seconds after finding no results
                return result
            except TimeoutException:
                return False
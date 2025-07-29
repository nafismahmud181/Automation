import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import config
from selenium.common.exceptions import TimeoutException

class TransactionPage(BasePage):
    # Search Locators
    ID_SEARCH_INPUT = (By.XPATH, "//*[@data-id='email-batches search id']")
    EMAIL_FROM_SEARCH_INPUT = (By.XPATH, "//*[@data-id='email-batches search email-from']")
    EMAIL_FROM_RESULTS = (By.XPATH, "//td[contains(@data-id, 'email-from')]")
    EMAIL_SUBJECT_INPUT = (By.XPATH, "//*[@data-id='email-batches search email-subject']")
    MATCHED_PROFILE = (By.XPATH, "//*[@data-id='email-batches search matched-profile']")
    CONFIRMATION_NUMBER = (By.XPATH, "//*[@data-id='']")
    STATUS_SEARCH_INPUT = (By.XPATH, "//*[@data-id='email-batches sort status']")
    SEARCH_RESULTS = (By.XPATH, "//div[@class='search-results']")
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(text(),'No results found')]")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[@data-id='email-batch-clearSearch']")
    
    # Upload Locators
    UPLOAD_BUTTON = (By.XPATH, "//button[normalize-space()='Upload Transaction']")
    FILE_INPUT = (By.CSS_SELECTOR, ".custom-file-input")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Upload']")
    UPLOAD_SUCCESS_MESSAGE = (By.XPATH, "//h5[normalize-space()='Transaction saved to disk']")
    UPLOAD_ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'alert-error') or contains(@class, 'alert-danger')]")
    INVALID_ZIP_ERROR = (By.XPATH, "//p[contains(text(),'Invalid Zip file. Zip should contain db_data.json ')]")

    def __init__(self, driver):
        super().__init__(driver)
        # Main page URL after successful login
        self.url = f"{config.BASE_URL}/"  

    def search_by_id(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.ID_SEARCH_INPUT))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)
        
    def search_by_email_from(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.EMAIL_FROM_SEARCH_INPUT))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_email(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.EMAIL_SUBJECT_INPUT))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_status(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.STATUS_SEARCH_INPUT))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def get_ID_search_results(self, search_text=None):
        """
        Get search result text using the dynamic search text
        """
        try:
            if search_text:
                # Use the same dynamic XPath as is_search_successful
                dynamic_locator = (By.XPATH, f'//*[@data-id="email-batch {search_text} id"]')
                results = self.find_element(dynamic_locator)
                return results.text
            return ""
        except TimeoutException:
            return ""
               
    def get_email_from_results(self):
        """
        Get all email from search results
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.EMAIL_FROM_RESULTS))
        return [el.text.strip() for el in elements]

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
    
    def is_search_successful(self, search_text=None):
        """
        Check if search was successful by verifying the element with dynamic search text is found
        """
        try:
            if search_text:
                # Dynamic XPath based on search text
                dynamic_locator = (By.XPATH, f'//*[@data-id="email-batch {search_text} id"]')
                return self.is_element_present(dynamic_locator)
            return self.is_element_present(self.SEARCH_RESULTS)
        except TimeoutException:
            return False
        
    def click_clear_search_button(self):
        """
        Click the Go Back button after test is done
        """
        wait = WebDriverWait(self.driver, 10)
        clear_search_button = wait.until(EC.element_to_be_clickable(self.CLEAR_SEARCH_BUTTON))
        clear_search_button.click()

        # wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))


    def click_upload_button(self):
        """
        Click the Upload Transaction button and wait for file input to be present
        """
        # Wait for upload button to be clickable and click it
        wait = WebDriverWait(self.driver, 10)
        upload_button = wait.until(EC.element_to_be_clickable(self.UPLOAD_BUTTON))
        upload_button.click()

    def upload_file(self, file_path: str):
        """
        Upload a file using the file input field
        Args:
            file_path: Absolute path to the file to upload
        """
        # Wait for the file input to become present in the DOM
        wait = WebDriverWait(self.driver, 10)
        file_input = wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        
        # Send the file path
        file_input.send_keys(file_path)
        
        # Wait a moment for the file to be processed
        time.sleep(1)

    def click_submit_button(self):
        """
        Click the Submit button to submit the uploaded file
        """
        # Wait for submit button to be clickable
        wait = WebDriverWait(self.driver, 10)
        submit_button = wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_button.click()

    def wait_for_element(self, locator, timeout=10):
        """
        Wait for an element to be visible on the page
        Args:
            locator: The locator tuple (By.XX, "locator string")
            timeout: Maximum time to wait in seconds
        Returns:
            The web element if found
        Raises:
            TimeoutException if element is not found within timeout
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def is_upload_successful(self):
        """
        Check if upload was successful by looking for success message
        """
        try:
            self.wait_for_element(self.UPLOAD_SUCCESS_MESSAGE, timeout=30)
            return True
        except TimeoutException:
            return False

    def get_upload_message(self, timeout=5):
        """
        Get the upload result message (success or error)
        Args:
            timeout: Time to wait for any message to appear
        Returns:
            The message text or empty string if no message found
        """
        try:
            # Create a single wait instance
            wait = WebDriverWait(self.driver, timeout)
            
            # Try each message type with minimal delay
            for locator in [self.UPLOAD_SUCCESS_MESSAGE, self.INVALID_ZIP_ERROR, self.UPLOAD_ERROR_MESSAGE]:
                try:
                    element = wait.until(EC.presence_of_element_located(locator))
                    return element.text
                except TimeoutException:
                    continue
            return ""
        except TimeoutException:
            return ""

    def perform_batch_upload(self, file_path: str):
        """
        Complete batch upload workflow: click upload button, select file, and submit
        Args:
            file_path: Absolute path to the file to upload
        """
        try:
            # Step 1: Click upload button and wait for file input
            self.click_upload_button()
            
            # Step 2: Upload the file
            self.upload_file(file_path)
            
            # Step 3: Submit the upload
            self.click_submit_button()
            
            # Step 4: Wait for either success or error message
            wait = WebDriverWait(self.driver, 30)
            wait.until(lambda driver: any([
                self.is_element_present(self.UPLOAD_SUCCESS_MESSAGE),
                self.is_element_present(self.INVALID_ZIP_ERROR),
                self.is_element_present(self.UPLOAD_ERROR_MESSAGE)
            ]))
            
        except TimeoutException as e:
            raise TimeoutException(f"Failed to upload file: No success or error message appeared after 30 seconds")
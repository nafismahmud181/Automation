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
    EMAIL_SUBJECT_RESULTS = (By.XPATH, "//td[contains(@data-id, 'email-subject')]")
    
    MATCHED_PROFILE = (By.XPATH, "//*[@data-id='email-batches search matched-profile']")
    MATCHED_PROFILE_RESULTS = (By.XPATH, "//td[contains(@data-id, 'profile-name')]")

    CONFIRMATION_NUMBER = (By.XPATH, "//*[@data-id='email-batches search confirmation-numbers']")
    CONFIRMATION_NUMBER_RESULTS = (By.XPATH, "//td[contains(@data-id, 'confirmation-numbers')]")
    
    LINKED_BATCHES_SEARCH_INPUT = (By.XPATH, "//input[@data-id='email-batches search linked-batches']")
    
    SHOW_ENTRY_SEARCH_INPUT = (By.XPATH, "//div[@id='vs2__combobox']//input[@type='search']")
    
    STATUS_SEARCH_INPUT = (By.XPATH, "//*[@data-id='email-batches sort status']")  # I have to think about this one

    BATCH_DELETE_BUTTON = (By.XPATH, "//button[@data-id='email-batch delete']")
    
    SEARCH_RESULTS = (By.XPATH, "//div[@class='search-results']")
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(text(),'No results found')]")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[@data-id='email-batch-clearSearch']")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space()='Delete']")
    DELETE_SUCCESS_MESSAGE = (By.XPATH, "//h5[normalize-space()='Email Batch deleted sucessfully']")
    
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

    def search_by_email_subject(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.EMAIL_SUBJECT_INPUT))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_matched_profile(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.MATCHED_PROFILE))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_confirmation_number(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.CONFIRMATION_NUMBER))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_status(self, text: str):
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.STATUS_SEARCH_INPUT))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_linked_batches(self, text: str):
        """Search by linked batches"""
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.LINKED_BATCHES_SEARCH_INPUT))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def search_by_show_entry(self, text: str):
        """Search by entry"""
        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(EC.element_to_be_clickable(self.SHOW_ENTRY_SEARCH_INPUT))
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
               
    def get_email_subject_results(self):
        """
        Get all email subject search results
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.EMAIL_SUBJECT_RESULTS))
        return [el.text.strip() for el in elements]
               
    def get_matched_profile_results(self):
        """
        Get all matched profile search results
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.MATCHED_PROFILE_RESULTS))
        return [el.text.strip() for el in elements]
               
    def get_confirmation_number_results(self):
        """
        Get all confirmation number search results
        """
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located(self.CONFIRMATION_NUMBER_RESULTS))
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

    def is_linked_batches_search_successful(self, search_text: str):
        """
        Check if linked-batches search was successful by verifying the element with dynamic search text is found
        """
        try:
            if search_text:
                # Dynamic XPath based on search text
                dynamic_locator = (By.XPATH, f'//*[@data-id="email-batch {search_text} id"]')
                return self.is_element_present(dynamic_locator)
            return False
        except TimeoutException:
            return False

    def is_show_entry_search_successful(self, search_text: str):
        """
        Check if combobox search was successful by verifying the element with the complex XPath is found
        """
        try:
            if search_text:
                # Wait a moment for search results to load
                time.sleep(2)
                
                print(f"Searching for text: '{search_text}'")
                
                # Method 1: Try the complex XPath as specified in requirements
                complex_xpath = "//*[@data-id and starts-with(@data-id, 'email-batch ') and contains(@data-id, ' id') and not(contains(@data-id, 'link')) and not(contains(@data-id, 'sort')) and not(contains(@data-id, 'search'))]"
                
                # Find all elements matching the complex XPath
                elements = self.driver.find_elements(By.XPATH, complex_xpath)
                print(f"Found {len(elements)} elements with complex XPath")
                
                # Check if any element contains the search text in its data-id or text content
                for element in elements:
                    data_id = element.get_attribute('data-id')
                    element_text = element.text
                    
                    print(f"Element data-id: {data_id}, text: {element_text}")
                    
                    # Check if search text is in data-id or element text
                    if data_id and search_text in data_id:
                        print(f"Found match in data-id: {data_id}")
                        return True
                    if element_text and search_text in element_text:
                        print(f"Found match in text: {element_text}")
                        return True
                
                # Method 2: Try a simpler approach - look for any element with data-id containing the search text
                simple_xpath = f"//*[contains(@data-id, '{search_text}')]"
                simple_elements = self.driver.find_elements(By.XPATH, simple_xpath)
                print(f"Found {len(simple_elements)} elements with simple XPath")
                
                if simple_elements:
                    print("Found match with simple XPath")
                    return True
                
                # Method 3: Look for elements with text content containing the search text
                text_xpath = f"//*[contains(text(), '{search_text}')]"
                text_elements = self.driver.find_elements(By.XPATH, text_xpath)
                print(f"Found {len(text_elements)} elements with text XPath")
                
                if text_elements:
                    print("Found match with text XPath")
                    return True
                
                print("No matches found with any method")
                return False
            return False
        except Exception as e:
            print(f"Error in is_combobox_search_successful: {e}")
            return False
        
    def click_clear_search_button(self):
        """
        Click the Go Back button after test is done
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            clear_search_button = wait.until(EC.element_to_be_clickable(self.CLEAR_SEARCH_BUTTON))
            clear_search_button.click()
        except TimeoutException:
            print("Clear search button not found, skipping clear operation")
            pass


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

    def click_download_transaction_by_batch_id(self, batch_id: str):
        """Click the download transaction action for the given batch ID.
        Locator pattern: //span[@data-id="email-batch {batch_id} action download-transaction"]
        """
        dynamic_locator = (
            By.XPATH,
            f"//span[@data-id='email-batch {batch_id} action download-transaction']",
        )
        wait = WebDriverWait(self.driver, 20)
        element = wait.until(EC.element_to_be_clickable(dynamic_locator))
        try:
            element.click()
        except Exception:
            # Fallback to JavaScript click if standard click fails due to overlays
            self.driver.execute_script("arguments[0].click();", element)

    def click_delete_transaction_by_batch_id(self, batch_id: str):
        """Click the delete action for the given batch ID.
        Locator pattern: //span[@data-id="email-batch {batch_id} action delete"]
        """
        dynamic_locator = (
            By.XPATH,
            f"//span[@data-id='email-batch {batch_id} action delete']",
        )
        wait = WebDriverWait(self.driver, 20)
        element = wait.until(EC.element_to_be_clickable(dynamic_locator))
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def confirm_delete(self):
        """Confirm deletion in the popup dialog by clicking Delete button"""
        wait = WebDriverWait(self.driver, 20)
        button = wait.until(EC.element_to_be_clickable(self.DELETE_CONFIRM_BUTTON))
        try:
            button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", button)

    def is_delete_successful(self, timeout: int = 30) -> bool:
        """Return True if delete success message appears"""
        try:
            self.wait_for_element(self.DELETE_SUCCESS_MESSAGE, timeout=timeout)
            return True
        except TimeoutException:
            return False

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
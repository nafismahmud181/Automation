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
  TRANSACTION_MENU = (By.XPATH, "//*[@data-id='nav-group-toggle-home']")
  CREATE_PROFILE_LINK = (By.XPATH, "//li[@data-id='nav-group-item-create-profile']/a")
  CREATE_PROFILE_HEADER = (By.XPATH, "//h2[normalize-space()='Create Profile']")
  CUSTOMER_NAME_INPUT = (By.XPATH, "//*[@data-id='profile-create customer-name']")
  PROJECT_SEARCH_INPUT = (By.XPATH, "//*[@data-id='project-search-input']")
  CUSTOMER_NAME_ERROR = (By.XPATH, "//*[@data-id='customer-name-error']")
  PROJECT_SELECTED = (By.XPATH, "//*[@data-id='profile-create project']//span[@class='vs__selected'][1]")
  DOCUMENT_0_DOC_TYPE_INPUT = (By.XPATH, "//*[@data-id='profile-create document-0 doc-type-input']")
  NO_PROJECT_DOC_TYPE_ERROR = (By.XPATH, "//small[normalize-space()='Please select a \"Project\" to view document types']")
  NONE_SPAN = (By.XPATH, "//span[normalize-space()='None']")
  NAME_MATCHING_TEXT_DISABLED_INPUT = (By.XPATH, "//input[@data-id='profile-create document-0 name-matching-text' and @disabled]")

  def __init__(self, driver):
    super().__init__(driver)
    self.url = f"{config.BASE_URL}/profiles/create" 
    self.action = ActionChains(driver)

  def force_close_transaction_menu(self):
        """Force close the transaction menu by clicking elsewhere and using keyboard navigation"""
        try:
            # Try to click on the page header to close any open menus
            try:
                header = self.driver.find_element(*self.CREATE_PROFILE_HEADER)
                header.click()
                time.sleep(0.5)
            except:
                pass
            
            # Use Tab key to move focus away from any active elements
            body_element = self.driver.find_element(By.TAG_NAME, "body")
            body_element.send_keys(Keys.TAB)
            time.sleep(0.5)
            
            # Use Escape key multiple times to ensure all dropdowns are closed
            for _ in range(3):
                body_element.send_keys(Keys.ESCAPE)
                time.sleep(0.3)
            
            # Click on body to clear any active states
            self.driver.execute_script("arguments[0].click();", body_element)
            time.sleep(0.5)
            
            print("Transaction menu force closed")
        except Exception as e:
            print(f"Error force closing transaction menu: {e}")

  def navigate_to_create_profile_page(self):
        """Complete navigation to Create Profile page"""
        success = self.click_create_profile()
        if success:
            self.wait_for_page_load()
        return success
  
  def wait_for_page_load(self, timeout=30):
    """Wait for the profile page to fully load"""
    try:
        wait = WebDriverWait(self.driver, timeout)
        # Wait for either page title or form elements to be present
        wait.until(lambda driver: any([
            # self.is_element_present(self.PAGE_TITLE),
            self.is_element_present(self.CREATE_PROFILE_HEADER),
        ]))
        return True
    except TimeoutException:
        print(f"Page load timeout after {timeout} seconds")
        return False
    except Exception as e:
        print(f"Error waiting for page load: {e}")
        return False

  def click_create_profile(self):
    """ Click the Create Profile link in the transaction menu """
    try:
        if not self.navigate_to_transaction_menu():
            print("Failed to navigate to transaction menu")
            return False

        wait = WebDriverWait(self.driver, 20)
        
        try:
            create_profile_link = wait.until(
                EC.visibility_of_element_located(self.CREATE_PROFILE_LINK)
            )
        except TimeoutException:
            print("Create Profile link not visible after hovering over transaction menu")
            return False

        self.driver.execute_script("arguments[0].scrollIntoView(true);", create_profile_link)
        time.sleep(1)

        try:
            create_profile_link.click()
        except Exception as e:
            print(f"Normal click failed, trying JavaScript click: {e}")
            try:
                self.driver.execute_script("arguments[0].click();", create_profile_link)
            except Exception as js_error:
                print(f"JavaScript click also failed: {js_error}")
                return False

        time.sleep(2)
        
        return True

    except Exception as e:
        print(f"Error in click_create_profile: {e}")
        return False

        
  def navigate_to_transaction_menu(self):
        """Navigate to and hover over the transaction menu"""
        try:
            wait = WebDriverWait(self.driver, 20)
            transaction_menu = wait.until(
                EC.presence_of_element_located(self.TRANSACTION_MENU)
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", transaction_menu)
            time.sleep(1)
            
            self.action.move_to_element(transaction_menu).perform()
            time.sleep(2)
            
            self.action.move_by_offset(0, 10).perform()
            time.sleep(1)
            
            return True
        except TimeoutException:
            print("Transaction menu not found within timeout")
            return False
        except Exception as e:
            print(f"Error navigating to transaction menu: {e}")
            return False
        
  def is_create_profile_page_loaded(self):
        """Check if Create Profile page is loaded"""
        try:

            if self.is_element_present(self.CREATE_PROFILE_HEADER):
                return True
            
            current_url = self.driver.current_url.lower()
            if "create" in current_url or "profiles" in current_url:
                return True
                
            return False
        except Exception as e:
            print(f"Error checking if create profile page is loaded: {e}")
            return False
        

  def get_current_page_url(self) -> str:
    """Get current page URL"""
    return self.driver.current_url

  def test_customer_name_validation_error(self):
    """Test that customer name validation error appears when clicking customer name input then project search input"""
    try:
      # Wait for elements to be present and clickable
      wait = WebDriverWait(self.driver, 10)
      
      # First click on customer name input field
      customer_name_field = wait.until(
        EC.presence_of_element_located(self.CUSTOMER_NAME_INPUT)
      )
      
      # Scroll the element into view
      self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", customer_name_field)
      time.sleep(1)
      
      # Try multiple click strategies
      click_success = False
      
      # Strategy 1: Normal click
      try:
        customer_name_field.click()
        click_success = True
        print("Normal click successful on customer name field")
      except Exception as e:
        print(f"Normal click failed: {e}")
        
        # Strategy 2: JavaScript click
        try:
          self.driver.execute_script("arguments[0].click();", customer_name_field)
          click_success = True
          print("JavaScript click successful on customer name field")
        except Exception as js_e:
          print(f"JavaScript click failed: {js_e}")
          
          # Strategy 3: ActionChains click
          try:
            actions = ActionChains(self.driver)
            actions.move_to_element(customer_name_field).click().perform()
            click_success = True
            print("ActionChains click successful on customer name field")
          except Exception as ac_e:
            print(f"ActionChains click failed: {ac_e}")
      
      if not click_success:
        print("All click strategies failed for customer name field")
        return False
      
      time.sleep(2)
      
      # Then click on project search input field
      project_search_field = wait.until(
        EC.presence_of_element_located(self.PROJECT_SEARCH_INPUT)
      )
      
      # Scroll the element into view
      self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", project_search_field)
      time.sleep(1)
      
      # Try multiple click strategies for project search field
      click_success = False
      
      # Strategy 1: Normal click
      try:
        project_search_field.click()
        click_success = True
        print("Normal click successful on project search field")
      except Exception as e:
        print(f"Normal click failed: {e}")
        
        # Strategy 2: JavaScript click
        try:
          self.driver.execute_script("arguments[0].click();", project_search_field)
          click_success = True
          print("JavaScript click successful on project search field")
        except Exception as js_e:
          print(f"JavaScript click failed: {js_e}")
          
          # Strategy 3: ActionChains click
          try:
            actions = ActionChains(self.driver)
            actions.move_to_element(project_search_field).click().perform()
            click_success = True
            print("ActionChains click successful on project search field")
          except Exception as ac_e:
            print(f"ActionChains click failed: {ac_e}")
      
      if not click_success:
        print("All click strategies failed for project search field")
        return False
      
      time.sleep(3)  # Wait longer for validation to trigger
      
      # Check if customer name error appears
      try:
        error_element = wait.until(
          EC.presence_of_element_located(self.CUSTOMER_NAME_ERROR)
        )
        return error_element.is_displayed()
      except TimeoutException:
        print("Customer name error element not found within timeout")
        return False
        
    except Exception as e:
      print(f"Error in test_customer_name_validation_error: {e}")
      return False

  def test_document_type_validation_without_project(self):
    """Test that document type validation error appears when no project is selected"""
    try:
      # Wait for elements to be present
      wait = WebDriverWait(self.driver, 10)
      
      # First check if a project is already selected
      try:
        project_selected = self.driver.find_element(*self.PROJECT_SELECTED)
        if project_selected.is_displayed():
          print("Project is already selected, aborting test")
          return "ABORTED"
      except:
        # No project selected, continue with test
        pass
      
      # Click on document type input field
      doc_type_input = wait.until(
        EC.element_to_be_clickable(self.DOCUMENT_0_DOC_TYPE_INPUT)
      )
      
      # Try normal click first, fallback to JavaScript click
      try:
        doc_type_input.click()
      except Exception as e:
        print(f"Normal click failed, trying JavaScript click: {e}")
        self.driver.execute_script("arguments[0].click();", doc_type_input)
      
      time.sleep(2)  # Wait for validation to trigger
      
      # Check if the error message appears
      try:
        error_element = wait.until(
          EC.presence_of_element_located(self.NO_PROJECT_DOC_TYPE_ERROR)
        )
        return error_element.is_displayed()
      except TimeoutException:
        print("Document type error element not found within timeout")
        return False
        
    except Exception as e:
      print(f"Error in test_document_type_validation_without_project: {e}")
      return False

  def check_name_matching_text_disabled(self):
    """Check if 'None' span exists and name matching text input is disabled"""
    try:
      wait = WebDriverWait(self.driver, 10)
      
      # First check if the 'None' span exists
      try:
        none_span = self.driver.find_element(*self.NONE_SPAN)
        if not none_span.is_displayed():
          print("'None' span exists but is not displayed")
          return False
        print("'None' span found and is displayed")
      except:
        print("'None' span not found")
        return False
      
      # Then check if the name matching text input exists and is disabled
      try:
        disabled_input = self.driver.find_element(*self.NAME_MATCHING_TEXT_DISABLED_INPUT)
        if not disabled_input.is_displayed():
          print("Name matching text input exists but is not displayed")
          return False
        
        # Check if the input is actually disabled
        if not disabled_input.get_attribute("disabled"):
          print("Name matching text input is not disabled")
          return False
        
        print("Name matching text input found, displayed, and disabled")
        return True
        
      except:
        print("Name matching text input not found or not disabled")
        return False
        
    except Exception as e:
      print(f"Error in check_name_matching_text_disabled: {e}")
      return False
        

 
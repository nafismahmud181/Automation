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
  
  # New locators for project status and manual validation
  PROJECT_IS_EMPTY = (By.XPATH, "//div[@data-id='profile-create project']//div[@class='vs__selected-options' and not(span[@class='vs__selected'])]")
  PROJECT_IS_SELECTED = (By.XPATH, "//div[@data-id='profile-create project']//div[@class='vs__selected-options']/span[@class='vs__selected']")
  
  # Switch locators
  MANUAL_VALIDATION_SWITCH = (By.XPATH, "//input[@data-id='profile-create manual-validation']")
  MULTI_SHIPMENT_SWITCH = (By.XPATH, "//input[@data-id='profile-create multi-shipment']")
  SEND_TIME_STAMP_SWITCH = (By.XPATH, "//input[@data-id='profile-create send-time-stamp']")
  PARSE_DOCUMENT_SWITCH = (By.XPATH, "//input[@data-id='profile-create parse-document']")
  IGNORE_DENSE_PAGES_SWITCH = (By.XPATH, "//input[@data-id='profile-create ignore-dense-pages']")
  EXCEPTIONAL_EXCEL_SWITCH = (By.XPATH, "//input[@data-id='profile-create exceptional-excel']")

  # Add these locators with the existing ones
  SUBMIT_BUTTON = (By.XPATH, "//button[@data-id='profile-create submit']")

  # Error locators for submit validation
  CUSTOMER_NAME_ERROR = (By.XPATH, "//small[@data-id='customer-name-error']")
  PROJECT_ERROR = (By.XPATH, "//small[@data-id='project-error']")
  COUNTRY_CODE_ERROR = (By.XPATH, "//small[@data-id='country-code-error']")
  TRANSPORT_ERROR = (By.XPATH, "//small[@data-id='transport-error']")
  DOC_TYPE_ERROR = (By.XPATH, "//small[@data-id='doc-type-error']")
  EMAIL_DOMAINS_ERROR = (By.XPATH, "//small[@data-id='email-domains-error']")
  EMAIL_FROM_ERROR = (By.XPATH, "//small[@data-id='email-from-error']")
  EMAIL_SUBJECT_TEXT_ERROR = (By.XPATH, "//small[@data-id='email-subject-text-error']")

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

  def test_manual_validation_switch_when_project_empty(self):
    """Test that manual validation switch is turned on when project is empty"""
    try:
      wait = WebDriverWait(self.driver, 10)
      
      # First check if project is empty or selected
      project_is_empty = False
      project_is_selected = False
      
      try:
        empty_project = self.driver.find_element(*self.PROJECT_IS_EMPTY)
        if empty_project.is_displayed():
          project_is_empty = True
          print("Project is empty")
      except:
        print("Project empty element not found")
      
      try:
        selected_project = self.driver.find_element(*self.PROJECT_IS_SELECTED)
        if selected_project.is_displayed():
          project_is_selected = True
          print("Project is selected")
      except:
        print("Project selected element not found")
      
      # If project is not empty (i.e., project is selected), skip the test
      if not project_is_empty or project_is_selected:
        print("Project is selected or not in empty state, test not applicable")
        return "SKIPPED"
      
      # If project is empty, check if manual validation switch is turned on
      try:
        manual_validation_switch = wait.until(
          EC.presence_of_element_located(self.MANUAL_VALIDATION_SWITCH)
        )
        
        # Scroll the element into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manual_validation_switch)
        time.sleep(1)
        
        # Check if the switch is checked (turned on)
        is_checked = manual_validation_switch.is_selected()
        
        if is_checked:
          print("Manual validation switch is turned on")
          return True
        else:
          print("Manual validation switch is turned off")
          return False
          
      except TimeoutException:
        print("Manual validation switch not found within timeout")
        return False
        
    except Exception as e:
      print(f"Error in test_manual_validation_switch_when_project_empty: {e}")
      return False

  def test_project_search_and_manual_validation_switch(self):
    """Test project search with 'Shipmentcreate' and verify manual validation switch is turned off"""
    try:
      wait = WebDriverWait(self.driver, 10)
      
      # First check if project is empty or selected
      project_is_empty = False
      project_is_selected = False
      
      try:
        empty_project = self.driver.find_element(*self.PROJECT_IS_EMPTY)
        if empty_project.is_displayed():
          project_is_empty = True
          print("Project is empty")
      except:
        print("Project empty element not found")
      
      try:
        selected_project = self.driver.find_element(*self.PROJECT_IS_SELECTED)
        if selected_project.is_displayed():
          project_is_selected = True
          print("Project is selected")
      except:
        print("Project selected element not found")
      
      # If project is not empty (i.e., project is selected), skip the test
      if not project_is_empty or project_is_selected:
        print("Project is selected or not in empty state, test not applicable")
        return "SKIPPED"
      
      # If project is empty, proceed with project search
      try:
        # Click on project search input field
        project_search_field = wait.until(
          EC.element_to_be_clickable(self.PROJECT_SEARCH_INPUT)
        )
        
        # Scroll the element into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", project_search_field)
        time.sleep(1)
        
        # Try multiple click strategies
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
        
        time.sleep(1)
        
        # Clear any existing text and input "Shipmentcreate"
        project_search_field.clear()
        project_search_field.send_keys("Shipmentcreate")
        print("Entered 'Shipmentcreate' in project search field")
        time.sleep(1)
        
        # Press Enter key
        project_search_field.send_keys(Keys.ENTER)
        print("Pressed Enter key")
        time.sleep(3)  # Wait for the search results and any UI updates
        
        # Now check if manual validation switch is turned off
        manual_validation_switch = wait.until(
          EC.presence_of_element_located(self.MANUAL_VALIDATION_SWITCH)
        )
        
        # Scroll the element into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manual_validation_switch)
        time.sleep(1)
        
        # Check if the switch is checked (turned off means not selected)
        is_checked = manual_validation_switch.is_selected()
        
        if not is_checked:
          print("Manual validation switch is turned off - Test successful")
          return True
        else:
          print("Manual validation switch is turned on - Test failed")
          return False
          
      except TimeoutException:
        print("Element not found within timeout during project search test")
        return False
        
    except Exception as e:
      print(f"Error in test_project_search_and_manual_validation_switch: {e}")
      return False
    
  def test_all_switches_toggle_functionality(self):
    """Test that all 6 switches can be toggled on/off regardless of their initial state"""
    try:
        wait = WebDriverWait(self.driver, 10)
        
        # Define all switches with their names and locators
        switches = [
            ("Manual Validation", self.MANUAL_VALIDATION_SWITCH),
            ("Multi Shipment", self.MULTI_SHIPMENT_SWITCH),
            ("Send Time Stamp", self.SEND_TIME_STAMP_SWITCH),
            ("Parse Document", self.PARSE_DOCUMENT_SWITCH),
            ("Ignore Dense Pages", self.IGNORE_DENSE_PAGES_SWITCH),
            ("Exceptional Excel", self.EXCEPTIONAL_EXCEL_SWITCH)
        ]
        
        print("=" * 80)
        print("TESTING ALL 6 SWITCHES TOGGLE FUNCTIONALITY")
        print("=" * 80)
        
        failed_switches = []
        
        for switch_name, switch_locator in switches:
            print(f"\n--- Testing {switch_name} Switch ---")
            
            try:
                # Find the switch element
                switch_element = wait.until(
                    EC.presence_of_element_located(switch_locator)
                )
                
                # Scroll the element into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", switch_element)
                time.sleep(1)
                
                # Get the initial state of the switch
                initial_state = switch_element.is_selected()
                print(f"Initial state of {switch_name}: {'ON' if initial_state else 'OFF'}")
                
                # First toggle: Change the state
                success = self._toggle_switch(switch_element, switch_name)
                if not success:
                    failed_switches.append(f"{switch_name} - Failed to perform first toggle")
                    continue
                    
                # Verify the state changed
                time.sleep(1)  # Wait for UI to update
                first_toggle_state = switch_element.is_selected()
                
                if first_toggle_state == initial_state:
                    print(f"ERROR: {switch_name} state did not change after first toggle. Still: {'ON' if first_toggle_state else 'OFF'}")
                    failed_switches.append(f"{switch_name} - State did not change after first toggle")
                    continue
                
                print(f"After first toggle: {'ON' if first_toggle_state else 'OFF'} - State changed successfully")
                
                # Second toggle: Return to original state
                success = self._toggle_switch(switch_element, switch_name)
                if not success:
                    failed_switches.append(f"{switch_name} - Failed to perform second toggle")
                    continue
                    
                # Verify the state returned to original
                time.sleep(1)  # Wait for UI to update
                final_state = switch_element.is_selected()
                
                if final_state != initial_state:
                    print(f"ERROR: {switch_name} did not return to original state. Expected: {'ON' if initial_state else 'OFF'}, Got: {'ON' if final_state else 'OFF'}")
                    failed_switches.append(f"{switch_name} - Did not return to original state")
                    continue
                
                print(f"After second toggle: {'ON' if final_state else 'OFF'} - Successfully returned to original state")
                print(f"✅ {switch_name} switch toggle test PASSED")
                
            except TimeoutException:
                print(f"❌ {switch_name} switch not found within timeout")
                failed_switches.append(f"{switch_name} - Element not found")
            except Exception as e:
                print(f"❌ Error testing {switch_name} switch: {e}")
                failed_switches.append(f"{switch_name} - Exception: {str(e)}")
        
        print("\n" + "=" * 80)
        print("FINAL RESULTS")
        print("=" * 80)
        
        if failed_switches:
            print(f"❌ {len(failed_switches)} switches failed:")
            for failure in failed_switches:
                print(f"   - {failure}")
            print(f"✅ {6 - len(failed_switches)} switches passed")
            return False
        else:
            print("✅ All 6 switches toggle functionality tests PASSED!")
            return True
            
    except Exception as e:
        print(f"Error in test_all_switches_toggle_functionality: {e}")
        return False

  def _toggle_switch(self, switch_element, switch_name):
    """Helper method to toggle a switch using multiple strategies - optimized for custom switches"""
    try:
        try:
            self.driver.execute_script("arguments[0].click();", switch_element)
            print(f"Successfully clicked {switch_name} switch using JavaScript click")
            return True
        except Exception as e:
            print(f"JavaScript click failed on {switch_name} switch: {e}")
        
        try:
            switch_id = switch_element.get_attribute("id")
            if switch_id:
                label = self.driver.find_element(By.XPATH, f"//label[@for='{switch_id}']")
                label.click()
                print(f"Successfully clicked {switch_name} switch label using normal click")
                return True
        except Exception as e:
            print(f"Label click failed on {switch_name} switch: {e}")
        
        try:
            switch_id = switch_element.get_attribute("id")
            if switch_id:
                label = self.driver.find_element(By.XPATH, f"//label[@for='{switch_id}']")
                self.driver.execute_script("arguments[0].click();", label)
                print(f"Successfully clicked {switch_name} switch label using JavaScript click")
                return True
        except Exception as e:
            print(f"JavaScript label click failed on {switch_name} switch: {e}")
        
        try:
            switch_element.click()
            print(f"Successfully clicked {switch_name} switch using normal click")
            return True
        except Exception as e:
            print(f"Normal click failed on {switch_name} switch: {e}")
        
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(switch_element).click().perform()
            print(f"Successfully clicked {switch_name} switch using ActionChains")
            return True
        except Exception as e:
            print(f"ActionChains click failed on {switch_name} switch: {e}")
        
        print(f"All click strategies failed for {switch_name} switch")
        return False
        
    except Exception as e:
        print(f"Error in _toggle_switch for {switch_name}: {e}")
        return False
    
  # Add this method at the end of the class
  def test_submit_button_validation_errors(self):
    """Test that all validation errors appear when clicking submit button without filling required fields"""
    try:
        # First refresh the page
        print("Refreshing the page...")
        self.driver.refresh()
        time.sleep(3)  # Wait for page to reload
        
        # Wait for the page to be fully loaded
        wait = WebDriverWait(self.driver, 20)
        
        # Wait for submit button to be present and clickable
        submit_button = wait.until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON)
        )
        
        print("Page refreshed, now clicking submit button...")
        
        # Scroll the submit button into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        time.sleep(1)
        
        # Click the submit button using multiple strategies
        click_success = False
        
        # Strategy 1: Normal click
        try:
            submit_button.click()
            click_success = True
            print("Normal click successful on submit button")
        except Exception as e:
            print(f"Normal click failed: {e}")
            
            # Strategy 2: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", submit_button)
                click_success = True
                print("JavaScript click successful on submit button")
            except Exception as js_e:
                print(f"JavaScript click failed: {js_e}")
                
                # Strategy 3: ActionChains click
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(submit_button).click().perform()
                    click_success = True
                    print("ActionChains click successful on submit button")
                except Exception as ac_e:
                    print(f"ActionChains click failed: {ac_e}")
        
        if not click_success:
            print("All click strategies failed for submit button")
            return False
        
        time.sleep(3)  # Wait for validation errors to appear
        
        # Define all error elements to check
        error_elements = [
            ("Customer Name Error", self.CUSTOMER_NAME_ERROR),
            ("Project Error", self.PROJECT_ERROR),
            ("Country Code Error", self.COUNTRY_CODE_ERROR),
            ("Transport Error", self.TRANSPORT_ERROR),
            ("Doc Type Error", self.DOC_TYPE_ERROR),
            ("Email Domains Error", self.EMAIL_DOMAINS_ERROR),
            ("Email From Error", self.EMAIL_FROM_ERROR),
            ("Email Subject Text Error", self.EMAIL_SUBJECT_TEXT_ERROR)
        ]
        
        print("\n" + "=" * 80)
        print("CHECKING VALIDATION ERRORS AFTER SUBMIT BUTTON CLICK")
        print("=" * 80)
        
        displayed_errors = []
        missing_errors = []
        
        for error_name, error_locator in error_elements:
            try:
                error_element = self.driver.find_element(*error_locator)
                if error_element.is_displayed():
                    print(f"✅ {error_name}: DISPLAYED")
                    displayed_errors.append(error_name)
                else:
                    print(f"❌ {error_name}: PRESENT but NOT DISPLAYED")
                    missing_errors.append(error_name)
            except Exception as e:
                print(f"❌ {error_name}: NOT FOUND - {e}")
                missing_errors.append(error_name)
        
        print("\n" + "=" * 80)
        print("VALIDATION ERRORS SUMMARY")
        print("=" * 80)
        print(f"Total errors displayed: {len(displayed_errors)}")
        print(f"Total errors missing: {len(missing_errors)}")
        
        if displayed_errors:
            print("\nDisplayed errors:")
            for error in displayed_errors:
                print(f"   - {error}")
        
        if missing_errors:
            print("\nMissing errors:")
            for error in missing_errors:
                print(f"   - {error}")
        
        # Return True if all errors are displayed
        all_errors_displayed = len(missing_errors) == 0
        
        if all_errors_displayed:
            print("\n✅ All validation errors are displayed correctly!")
        else:
            print(f"\n❌ {len(missing_errors)} validation errors are missing!")
        
        return all_errors_displayed
        
    except Exception as e:
        print(f"Error in test_submit_button_validation_errors: {e}")
        return False  
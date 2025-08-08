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
  customer_name_input = (By.XPATH, "//*[@data-id='profile-create customer-name']")
  CREATE_PROFILE_HEADER = (By.XPATH, "//h2[normalize-space()='Create Profile']")

  def __init__(self, driver):
    super().__init__(driver)
    self.url = f"{config.BASE_URL}/profiles/create" 
    self.action = ActionChains(driver)

  def clear_hover_state(self):
        """Clear any active hover states by using keyboard and clicking"""
        try:
            # Method 1: Press Escape key to clear any active states
            body_element = self.driver.find_element(By.TAG_NAME, "body")
            body_element.send_keys(Keys.ESCAPE)
            time.sleep(0.5)
            
            # Method 2: Click on a neutral area (body element) to clear any hover states
            self.driver.execute_script("arguments[0].click();", body_element)
            time.sleep(0.5)
            
            # Reset the action chains
            self.action = ActionChains(self.driver)
        except Exception as e:
            print(f"Error clearing hover state: {e}")

  def navigate_to_create_profile_page(self):
        """Complete navigation to Create Profile page"""
        success = self.click_create_profile()
        if success:
            self.wait_for_page_load()
            # Clear any remaining hover states
            self.clear_hover_state()
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
        
        # Wait for the submenu to appear and the Create Profile link to be visible
        try:
            create_profile_link = wait.until(
                EC.visibility_of_element_located(self.CREATE_PROFILE_LINK)
            )
        except TimeoutException:
            print("Create Profile link not visible after hovering over transaction menu")
            return False

        # Scroll to the element to ensure it's visible
        self.driver.execute_script("arguments[0].scrollIntoView(true);", create_profile_link)
        time.sleep(1)

        # Try to click the element
        try:
            create_profile_link.click()
        except Exception as e:
            print(f"Normal click failed, trying JavaScript click: {e}")
            # Fallback if normal click is intercepted
            try:
                self.driver.execute_script("arguments[0].click();", create_profile_link)
            except Exception as js_error:
                print(f"JavaScript click also failed: {js_error}")
                return False

        time.sleep(2)
        
        # Clear hover state after successful click
        self.clear_hover_state()
        
        return True

    except Exception as e:
        print(f"Error in click_create_profile: {e}")
        return False

        
  def navigate_to_transaction_menu(self):
        """Navigate to and hover over the transaction menu"""
        try:
            # Wait for the transaction menu to be present with a shorter timeout
            wait = WebDriverWait(self.driver, 20)
            transaction_menu = wait.until(
                EC.presence_of_element_located(self.TRANSACTION_MENU)
            )
            
            # Scroll to the element to ensure it's visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", transaction_menu)
            time.sleep(1)
            
            # Hover over the transaction menu to reveal submenu
            self.action.move_to_element(transaction_menu).perform()
            time.sleep(2)  # Allow submenu to appear
            
            # Try to move slightly to ensure hover is maintained
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
            # Check for the header first
            if self.is_element_present(self.CREATE_PROFILE_HEADER):
                return True
            
            # Check URL as fallback
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

  
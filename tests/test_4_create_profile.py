import pytest
import time
from utils.test_data import TestData
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.profile
@pytest.mark.usefixtures("profile_driver")
class TestProfileManagement:
  """Test suite for Create Profile page functionalities"""

  @pytest.mark.smoke
  def test_navigate_to_create_profile_page(self, create_profile_page):
      """Test navigation to Profile management page"""
      logger.info("Testing navigation to Create Profile page")
      
      success = create_profile_page.navigate_to_create_profile_page()
      assert success, "Failed to navigate to Profile Management page"
      logger.info("navigate_to_create_profile_page executed successfully")

      # Verify we're on the correct page
      assert create_profile_page.is_create_profile_page_loaded(), "Create Profile page not loaded properly"
      
      current_url = create_profile_page.get_current_page_url()
      logger.info(f"Successfully navigated to: {current_url}")

  @pytest.mark.smoke
  def test_customer_name_validation_error(self, create_profile_page):
      """Test that customer name validation error appears when clicking customer name input then project search input"""
      logger.info("Testing customer name validation error scenario")
      
      # First navigate to create profile page
      success = create_profile_page.navigate_to_create_profile_page()
      assert success, "Failed to navigate to Create Profile page"
      
      # Verify we're on the correct page
      assert create_profile_page.is_create_profile_page_loaded(), "Create Profile page not loaded properly"
      
      # Test the validation error scenario
      error_appears = create_profile_page.test_customer_name_validation_error()
      assert error_appears, "Customer name validation error did not appear as expected"
      
      logger.info("Customer name validation error test completed successfully")

      
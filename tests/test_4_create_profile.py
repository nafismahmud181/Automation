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
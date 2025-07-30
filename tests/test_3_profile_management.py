import pytest
import time
from utils.test_data import TestData
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.profile
@pytest.mark.usefixtures("profile_driver")
class TestProfileManagement:
    """Test suite for Profile Management functionality"""

    @pytest.mark.smoke
    def test_navigate_to_create_profile_page(self, profile_page):
        """Test navigation to Create Profile page"""
        logger.info("Testing navigation to Create Profile page")
        
        success = profile_page.navigate_to_profile_management_page()
        assert success, "Failed to navigate to Profile Management page"
        logger.info("navigate_to_profile_management_page executed successfully")

        # Verify we're on the correct page
        assert profile_page.is_profile_amanagement_page_loaded(), "Create Profile page not loaded properly"
        
        current_url = profile_page.get_current_page_url()
        logger.info(f"Successfully navigated to: {current_url}")
        
    
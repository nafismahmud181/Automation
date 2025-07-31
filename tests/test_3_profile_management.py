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
    def test_navigate_to_profile_management_page(self, profile_management_page):
        """Test navigation to Create Profile page"""
        logger.info("Testing navigation to Create Profile page")
        
        success = profile_management_page.navigate_to_profile_management_page()
        assert success, "Failed to navigate to Profile Management page"
        logger.info("navigate_to_profile_management_page executed successfully")

        # Verify we're on the correct page
        assert profile_management_page.is_profile_amanagement_page_loaded(), "Create Profile page not loaded properly"
        
        current_url = profile_management_page.get_current_page_url()
        logger.info(f"Successfully navigated to: {current_url}")
        
    @pytest.mark.regression
    def test_search_profile_and_verify_fields(self, profile_management_page):
        """Test searching for a profile and verifying expected fields are present"""
        logger.info("Testing profile search and field verification")
        
        # Navigate to page first
        assert profile_management_page.navigate_to_profile_management_page(), "Navigation failed"

        # Perform search
        search_text = TestData.PROFILE_NAME_VALID_SEARCH_TEXT
        logger.info(f"Searching for profile with name: {search_text}")
        profile_management_page.search_by_profile_name(search_text)
        time.sleep(2)  # Let results load (you can replace with wait if needed)

        # Validate result
        assert profile_management_page.is_search_successful(), "Search result missing expected fields"
        logger.info("Profile search returned valid row with expected fields")
        profile_management_page.click_clear_search_button()
        logger.info("Search completed and cleared successfully")

    def test_invalid_profile_search(self, profile_management_page):
        """Test ID search with invalid text"""
        logger.info("Testing ID search with invalid text")

        search_text = TestData.PROFILE_NAME_INVALID_SEARCH_TEXT
        profile_management_page.search_by_profile_name(search_text)

        assert profile_management_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        profile_management_page.click_clear_search_button()

        logger.info("Invalid ID search test completed successfully")


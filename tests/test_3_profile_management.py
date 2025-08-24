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
        """Test navigation to Profile management page"""
        logger.info("Testing navigation to Create Profile page")
        
        success = profile_management_page.navigate_to_profile_management_page()
        assert success, "Failed to navigate to Profile Management page"
        logger.info("navigate_to_profile_management_page executed successfully")

        assert profile_management_page.is_profile_amanagement_page_loaded(), "Create Profile page not loaded properly"
        
        current_url = profile_management_page.get_current_page_url()
        logger.info(f"Successfully navigated to: {current_url}")
        
    @pytest.mark.regression
    def test_search_profile_and_verify_fields(self, profile_management_page):
        """Test searching for a profile and verifying expected fields are present"""
        logger.info("Testing profile search and field verification")
        
        assert profile_management_page.navigate_to_profile_management_page(), "Navigation failed"

        search_text = TestData.PROFILE_NAME_VALID_SEARCH_TEXT
        logger.info(f"Searching for profile with name: {search_text}")
        profile_management_page.search_by_profile_name(search_text)
        time.sleep(2)

        assert profile_management_page.is_search_successful(), "Search result missing expected fields"
        logger.info("Profile search returned valid row with expected fields")
        profile_management_page.click_clear_search_button()
        logger.info("Search completed and cleared successfully")

    def test_invalid_profile_search(self, profile_management_page):
        """Test searching for a profile with invalid text"""
        logger.info("Testing invalid profile search")

        search_text = TestData.PROFILE_NAME_INVALID_SEARCH_TEXT
        profile_management_page.search_by_profile_name(search_text)

        assert profile_management_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        profile_management_page.click_clear_search_button()

        logger.info("Invalid profile search test completed successfully")

    @pytest.mark.smoke
    def test_customer_name_valid_search(self, profile_management_page):
        logger.info("Testing customer name search with valid text")

        search_text = TestData.CUSTOMER_NAME_VALID_SEARCH_TEXT
        profile_management_page.search_by_customer_name(search_text)

        customer_name_result = profile_management_page.get_customer_name_results()

        logger.info(f"Found {len(customer_name_result)} customer name entries after search")

        assert customer_name_result, f"No customer name results found for '{search_text}'"

        for name in customer_name_result:
            assert search_text.lower() in name.lower(), \
                f"Expected '{search_text}' to be in result '{name}'"

        profile_management_page.click_clear_search_button()
        logger.info("Valid customer name search test completed successfully")


    def test_customer_name_invalid_search(self, profile_management_page):
        """Test customer name search with invalid text"""
        logger.info("Testing customer name search with invalid text")

        search_text = TestData.CUSTOMER_NAME_INVALID_SEARCH_TEXT
        profile_management_page.search_by_customer_name(search_text)

        assert profile_management_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        profile_management_page.click_clear_search_button()
        logger.info("Invalid customer name search test completed successfully")

    @pytest.mark.smoke
    def test_email_subject_valid_search(self, profile_management_page):
        logger.info("Testing email subject search with valid text")

        search_text = TestData.EMAIL_SUBJECT_VALID_SEARCH_TEXT
        logger.info(f"Searching for email subject with text: {search_text}")
        profile_management_page.search_by_email_subject(search_text)

        email_subject_result = profile_management_page.get_email_subject_results()

        logger.info(f"Found {len(email_subject_result)} email-subject entries after search")

        assert email_subject_result, f"No email-subject results found for '{search_text}'"

        for name in email_subject_result:
            assert search_text.lower() in name.lower(), \
                f"Expected '{search_text}' to be in result '{name}'"

        profile_management_page.click_clear_search_button()
        logger.info("Valid email subject search test completed successfully")


    def test_email_subject_invalid_search(self, profile_management_page):
        """Test email subject search with invalid text"""
        logger.info("Testing email subject search with invalid text")

        search_text = TestData.EMAIL_SUBJECT_INVALID_SEARCH_TEXT
        logger.info(f"Searching for email subject with text: {search_text}")
        profile_management_page.search_by_email_subject(search_text)

        assert profile_management_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        profile_management_page.click_clear_search_button()
        logger.info("Invalid email subject search test completed successfully")

        
    @pytest.mark.smoke
    def test_project_valid_search(self, profile_management_page):
        logger.info("Testing project name search with valid text")

        search_text = TestData.PROJECT_NAME_VALID_SEARCH_TEXT
        logger.info(f"Searching for project with name: {search_text}")
        profile_management_page.search_by_project(search_text)

        project_result = profile_management_page.get_project_results()

        logger.info(f"Found {len(project_result)} project entries after search")

        assert project_result, f"No project results found for '{search_text}'"

        for name in project_result:
            assert search_text.lower() in name.lower(), \
                f"Expected '{search_text}' to be in result '{name}'"

        profile_management_page.click_clear_search_button()
        logger.info("Valid customer name search test completed successfully")


    def test_project_invalid_search(self, profile_management_page):
        """Test project name search with invalid text"""
        logger.info("Testing project name search with invalid text")

        search_text = TestData.PROJECT_NAME_INVALID_SEARCH_TEXT
        logger.info(f"Searching for project with name: {search_text}")
        profile_management_page.search_by_project(search_text)

        assert profile_management_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        profile_management_page.click_clear_search_button()
        logger.info("Invalid project name search test completed successfully")

    @pytest.mark.smoke
    def test_country_valid_search(self, profile_management_page):
        logger.info("Testing country name search with valid text")

        search_text = TestData.COUNTRY_VALID_SEARCH_TEXT
        logger.info(f"Searching for country with name: {search_text}")
        profile_management_page.search_by_country(search_text)

        country_result = profile_management_page.get_country_results()

        logger.info(f"Found {len(country_result)} country entries after search")

        assert country_result, f"No country results found for '{search_text}'"

        for name in country_result:
            assert search_text.lower() in name.lower(), \
                f"Expected '{search_text}' to be in result '{name}'"

        profile_management_page.click_clear_search_button()
        logger.info("Valid country code search test completed successfully")


    def test_country_invalid_search(self, profile_management_page):
        """Test country name search with invalid text"""
        logger.info("Testing country name search with invalid text")

        search_text = TestData.COUNTRY_INVALID_SEARCH_TEXT
        logger.info(f"Searching for country with name: {search_text}")
        profile_management_page.search_by_country(search_text)

        assert profile_management_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        profile_management_page.click_clear_search_button()
        logger.info("Invalid country code search test completed successfully")

    @pytest.mark.smoke
    def test_mode_of_transport_valid_search(self, profile_management_page):
        logger.info("Testing mode_of_transport name search with valid text")

        search_text = TestData.MODE_OF_TRANSPORT_VALID_SEARCH_TEXT
        logger.info(f"Searching for mode_of_transport with name: {search_text}")
        profile_management_page.search_by_mode_of_transport(search_text)

        mode_of_transport_result = profile_management_page.get_mode_of_transport_results()

        logger.info(f"Found {len(mode_of_transport_result)} mode of transport entries after search")

        assert mode_of_transport_result, f"No mode of transport results found for '{search_text}'"

        for name in mode_of_transport_result:
            assert search_text.lower() in name.lower(), \
                f"Expected '{search_text}' to be in result '{name}'"

        profile_management_page.click_clear_search_button()
        logger.info("Valid mode of transport search test completed successfully")


    def test_mode_of_transport_invalid_search(self, profile_management_page):
        """Test mode_of_transport name search with invalid text"""
        logger.info("Testing mode_of_transport name search with invalid text")

        search_text = TestData.MODE_OF_TRANSPORT_INVALID_SEARCH_TEXT
        logger.info(f"Searching for mode_of_transport with name: {search_text}")
        profile_management_page.search_by_mode_of_transport(search_text)

        assert profile_management_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        profile_management_page.click_clear_search_button()
        logger.info("Invalid mode of transport name search test completed successfully")


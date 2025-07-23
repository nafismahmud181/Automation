import time
import pytest
from utils.test_data import TestData
from utils.helpers import TestHelpers
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.usefixtures("login_driver")
class TestLogin:
    """Test suite for login functionality"""

    # @pytest.mark.login
    # @pytest.mark.parametrize("credentials", TestData.INVALID_CREDENTIALS)
    # def test_invalid_login_credentials(self, login_page, credentials):
    #     """Test login with various invalid credentials"""
    #     logger.info(f"Testing login with invalid credentials: {credentials.username}")
        
    #     login_page.navigate_to_login()
    #     login_page.login(credentials.username, credentials.password)
    #     time.sleep(2)

    #     assert not login_page.is_login_successful(), f"Login should fail for {credentials.expected_result}"
    #     logger.info("Login failed as expected.")
        
    #     if credentials.username == "":
    #         error = login_page.get_username_validation_error()
    #         assert error == "The Username field is required", "Expected username validation error"
    #         logger.info(f"Username validation error shown: {error}")
    #     elif credentials.password == "":
    #         error = login_page.get_password_validation_error()
    #         assert error == "The Password field is required", "Expected password validation error"
    #         logger.info(f"Password validation error shown: {error}")
    #     else:
    #         error = login_page.get_error_message()
    #         assert error != "", "Expected general error message for invalid login"
    #         logger.info(f"General error message shown: {error}")


    # @pytest.mark.smoke
    # @pytest.mark.login
    # def test_empty_username_and_password(self, login_page):
    #   """Test login with empty username and password"""
    #   logger.info("Testing login with empty username and password")
      
    #   login_page.navigate_to_login()
    #   login_page.click_login_button()
      
    #   # Assert login should fail
    #   assert not login_page.is_login_successful(), "Login should fail with empty credentials"
      
    #   # Check for validation errors
    #   assert login_page.has_validation_errors(), "Validation errors should be displayed for empty fields"
      
    #   # Get specific validation error messages
    #   username_error = login_page.get_username_validation_error()
    #   password_error = login_page.get_password_validation_error()
      
    #   # Assert specific error messages
    #   assert username_error == "The Username field is required", f"Expected username error, got: {username_error}"
    #   assert password_error == "The Password field is required", f"Expected password error, got: {password_error}"
      
    #   # Log all errors found
    #   all_errors = login_page.get_all_validation_errors()
    #   logger.info(f"Validation errors displayed: {all_errors}")
      
    #   # Alternative: Use the general method to get any error
    #   any_error = login_page.get_any_error_message()
    #   logger.info(f"Any error message: {any_error}")


    # @pytest.mark.login
    # def test_login_page_elements_present(self, login_page):
    #     """Test that all login page elements are present"""
    #     logger.info("Testing presence of all login page elements")

    #     login_page.navigate_to_login()
        
    #     assert login_page.is_element_present(login_page.USERNAME_INPUT), "Username field should be present"
    #     assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password field should be present"
    #     assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login button should be present"
    #     logger.info("All required login page elements are present")

    # @pytest.mark.login
    # def test_login_page_title(self, login_page):
    #   """Test login page title/heading"""
    #   logger.info("Testing login page title/heading")
      
    #   login_page.navigate_to_login()
      
    #   # Option 1: Test the page heading (h2 element)
    #   page_heading = login_page.get_page_heading()
    #   expected_heading = "Welcome to Data Definitions Editor"
      
    #   assert page_heading == expected_heading, f"Page heading should be '{expected_heading}', got: '{page_heading}'"
    #   logger.info(f"Login page heading validated: {page_heading}")
      
    #   # Option 2: Also test browser title if needed
    #   browser_title = login_page.get_page_title()
    #   logger.info(f"Browser title: {browser_title}")


    # @pytest.mark.login
    # def test_login_page_heading_present(self, login_page):
    #     """Test that login page heading is present and visible"""
    #     logger.info("Testing login page heading presence")
        
    #     login_page.navigate_to_login()
        
    #     # Check if heading element is present
    #     assert login_page.is_element_present(login_page.PAGE_TITLE), "Page heading should be present"
        
    #     # Check if heading text is not empty
    #     heading_text = login_page.get_page_heading()
    #     assert heading_text != "", "Page heading text should not be empty"
    #     assert "Data Definitions Editor" in heading_text, f"Heading should contain 'Data Definitions Editor', got: {heading_text}"
        
    #     logger.info(f"Page heading is present and correct: {heading_text}")

    # @pytest.mark.login
    # def test_password_field_masking(self, login_page):
    #     """Test that password field masks input"""
    #     logger.info("Testing password field masking")
        
    #     login_page.navigate_to_login()
    #     test_password = "TestPassword123"
    #     login_page.enter_password(test_password)
        
    #     password_element = login_page.find_element(login_page.PASSWORD_INPUT)
    #     input_type = password_element.get_attribute("type")
        
    #     assert input_type == "password", "Password field should have type='password'"
    #     logger.info("Password field is properly masked")

    @pytest.mark.login
    @pytest.mark.regression
    def test_multiple_failed_login_attempts(self, login_page):
        """Test multiple failed login attempts (account lockout scenario)"""
        logger.info("Testing multiple failed login attempts")
        
        login_page.navigate_to_login()
        invalid_credentials = TestData.INVALID_CREDENTIALS[0]
        
        for i in range(3):
            logger.info(f"Attempt {i+1} with invalid credentials")
            login_page.login(invalid_credentials.username, invalid_credentials.password)

            time.sleep(1)
        
        error_message = login_page.get_error_message()
        assert error_message != "", "Error message should be displayed after multiple failed attempts"
        logger.info("Error message displayed after multiple failed attempts")

    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, login_page):
        """Test login with valid credentials"""
        logger.info("Testing login with valid credentials")
        
        login_page.navigate_to_login()
        credentials = TestData.VALID_USER
        login_page.login(credentials.username, credentials.password)

        current_url = login_page.get_current_url()
        logger.info(f"Redirected to URL: {current_url}")
        
        
        assert login_page.is_login_successful(), f"Login failed. Current URL: {current_url}"
        logger.info("Login successful with valid credentials")

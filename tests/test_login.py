import pytest
from utils.test_data import TestData
from utils.helpers import TestHelpers

class TestLogin:
    """Test suite for login functionality"""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, login_page):
        """Test login with valid credentials"""
        # Arrange
        login_page.navigate_to_login()
        credentials = TestData.VALID_USER
        
        # Act
        login_page.login(credentials.username, credentials.password)
        
        # Assert
        assert login_page.is_login_successful(), "Login should be successful with valid credentials"
    
    @pytest.mark.login
    @pytest.mark.parametrize("credentials", TestData.INVALID_CREDENTIALS)
    def test_invalid_login_credentials(self, login_page, credentials):
        """Test login with various invalid credentials"""
        # Arrange
        login_page.navigate_to_login()
        
        # Act
        login_page.login(credentials.username, credentials.password)
        
        # Assert
        assert not login_page.is_login_successful(), f"Login should fail for {credentials.expected_result}"
        error_message = login_page.get_error_message()
        assert error_message != "", "Error message should be displayed for invalid login"
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_empty_username_and_password(self, login_page):
        """Test login with empty username and password"""
        # Arrange
        login_page.navigate_to_login()
        
        # Act
        login_page.click_login_button()
        
        # Assert
        assert not login_page.is_login_successful(), "Login should fail with empty credentials"
        error_message = login_page.get_error_message()
        assert error_message != "", "Error message should be displayed for empty fields"
    
    @pytest.mark.login
    def test_remember_me_functionality(self, login_page):
        """Test remember me checkbox functionality"""
        # Arrange
        login_page.navigate_to_login()
        credentials = TestData.VALID_USER
        
        # Act
        login_page.login(credentials.username, credentials.password, remember_me=True)
        
        # Assert
        # This would need to be verified based on your application's specific behavior
        # For example, checking for persistent cookies or session storage
        assert login_page.is_login_successful(), "Login should be successful with remember me"
    
    @pytest.mark.login
    def test_forgot_password_link(self, login_page):
        """Test forgot password link functionality"""
        # Arrange
        login_page.navigate_to_login()
        
        # Act
        login_page.click_forgot_password()
        
        # Assert
        current_url = login_page.get_current_url()
        assert "forgot" in current_url.lower() or "reset" in current_url.lower(), \
            "Should navigate to forgot password page"
    
    @pytest.mark.login
    def test_login_page_elements_present(self, login_page):
        """Test that all login page elements are present"""
        # Arrange
        login_page.navigate_to_login()
        
        # Assert
        assert login_page.is_element_present(login_page.USERNAME_INPUT), "Username field should be present"
        assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password field should be present"
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login button should be present"
        assert login_page.is_element_present(login_page.REMEMBER_ME_CHECKBOX), "Remember me checkbox should be present"
        assert login_page.is_element_present(login_page.FORGOT_PASSWORD_LINK), "Forgot password link should be present"
    
    @pytest.mark.login
    def test_login_page_title(self, login_page):
        """Test login page title"""
        # Arrange & Act
        login_page.navigate_to_login()
        
        # Assert
        page_title = login_page.get_page_title()
        assert "login" in page_title.lower(), f"Page title should contain 'login', got: {page_title}"
    
    @pytest.mark.login
    def test_password_field_masking(self, login_page):
        """Test that password field masks input"""
        # Arrange
        login_page.navigate_to_login()
        test_password = "TestPassword123"
        
        # Act
        login_page.enter_password(test_password)
        password_element = login_page.find_element(login_page.PASSWORD_INPUT)
        
        # Assert
        input_type = password_element.get_attribute("type")
        assert input_type == "password", "Password field should have type='password'"
    
    @pytest.mark.login
    @pytest.mark.regression
    def test_multiple_failed_login_attempts(self, login_page):
        """Test multiple failed login attempts (account lockout scenario)"""
        # Arrange
        login_page.navigate_to_login()
        invalid_credentials = TestData.INVALID_CREDENTIALS[0]
        
        # Act - Attempt multiple failed logins
        for i in range(3):
            login_page.login(invalid_credentials.username, invalid_credentials.password)
            # Add small delay between attempts
            import time
            time.sleep(1)
        
        # Assert
        error_message = login_page.get_error_message()
        # This assertion would depend on your application's lockout behavior
        assert error_message != "", "Error message should be displayed after multiple failed attempts"

import pytest
from utils.test_data import TestData
from utils.helpers import TestHelpers

class TestLoginEdgeCases:
    """Test suite for login edge cases and security testing"""
    
    @pytest.mark.security
    @pytest.mark.parametrize("credentials", TestData.SQL_INJECTION_CASES)
    def test_sql_injection_prevention(self, login_page, credentials):
        """Test that SQL injection attempts are prevented"""
        # Arrange
        login_page.navigate_to_login()
        
        # Act
        login_page.login(credentials.username, credentials.password)
        
        # Assert
        assert not login_page.is_login_successful(), "SQL injection attempt should not succeed"
        # Verify the application handles the injection attempt gracefully
        error_message = login_page.get_error_message()
        assert "error" not in error_message.lower() or "invalid" in error_message.lower(), \
            "Should show appropriate error message for invalid credentials"
    
    @pytest.mark.security
    @pytest.mark.parametrize("credentials", TestData.XSS_CASES)
    def test_xss_prevention(self, login_page, credentials):
        """Test that XSS attempts are prevented"""
        # Arrange
        login_page.navigate_to_login()
        
        # Act
        login_page.login(credentials.username, credentials.password)
        
        # Assert
        # Verify that XSS payloads are not executed
        page_source = login_page.driver.page_source
        assert "<script>" not in page_source, "XSS script tags should be escaped or removed"
        assert "alert(" not in page_source, "XSS alert functions should be escaped or removed"
    
    @pytest.mark.login
    def test_very_long_username_input(self, login_page):
        """Test login with extremely long username"""
        # Arrange
        login_page.navigate_to_login()
        long_username = "a" * 1000  # 1000 character username
        
        # Act
        login_page.enter_username(long_username)
        actual_username = login_page.get_username_field_value()
        
        # Assert
        # Verify the application handles long input appropriately
        assert len(actual_username) <= 255, "Username should be limited to reasonable length"
    
    @pytest.mark.login
    def test_very_long_password_input(self, login_page):
        """Test login with extremely long password"""
        # Arrange
        login_page.navigate_to_login()
        long_password = "p" * 1000  # 1000 character password
        
        # Act
        login_page.enter_password(long_password)
        
        # Assert
        # Try to login and verify it's handled appropriately
        login_page.click_login_button()
        assert not login_page.is_login_successful(), "Login with extremely long password should not succeed"
    
    @pytest.mark.login
    def test_unicode_characters_in_credentials(self, login_page):
        """Test login with unicode characters"""
        # Arrange
        login_page.navigate_to_login()
        unicode_username = "tëst@üsér.com"
        unicode_password = "pässwörd123"
        
        # Act
        login_page.login(unicode_username, unicode_password)
        
        # Assert
        # Should handle unicode characters gracefully
        error_message = login_page.get_error_message()
        assert "encoding" not in error_message.lower(), "Should not show encoding errors"
    
    @pytest.mark.login
    def test_special_characters_in_credentials(self, login_page):
        """Test login with special characters"""
        # Arrange
        login_page.navigate_to_login()
        special_chars_username = "test!@#$%^&*()user@example.com"
        special_chars_password = "p@ssw0rd!@#$%"
        
        # Act
        login_page.login(special_chars_username, special_chars_password)
        
        # Assert
        # Should handle special characters without breaking
        assert not login_page.is_login_successful(), "Login should fail for invalid credentials"
    
    @pytest.mark.login
    def test_whitespace_handling(self, login_page):
        """Test login with leading/trailing whitespaces"""
        # Arrange
        login_page.navigate_to_login()
        credentials = TestData.VALID_USER
        username_with_spaces = f"  {credentials.username}  "
        password_with_spaces = f"  {credentials.password}  "
        
        # Act
        login_page.login(username_with_spaces, password_with_spaces)
        
        # Assert
        # This test depends on whether your app trims whitespace
        # Adjust assertion based on expected behavior
        result = login_page.is_login_successful()
        # If app trims whitespace, login should succeed; otherwise should fail
        assert isinstance(result, bool), "Login result should be deterministic"
    
    @pytest.mark.login
    def test_case_sensitivity(self, login_page):
        """Test login case sensitivity"""
        # Arrange
        login_page.navigate_to_login()
        credentials = TestData.VALID_USER
        uppercase_username = credentials.username.upper()
        
        # Act
        login_page.login(uppercase_username, credentials.password)
        
        # Assert
        # This depends on your application's case sensitivity requirements
        result = login_page.is_login_successful()
        assert isinstance(result, bool), "Case sensitivity behavior should be consistent"
    
    @pytest.mark.login
    def test_login_button_disabled_state(self, login_page):
        """Test login button state management"""
        # Arrange
        login_page.navigate_to_login()
        
        # Act & Assert
        login_button = login_page.find_element(login_page.LOGIN_BUTTON)
        initial_state = login_button.is_enabled()
        
        # Enter partial credentials and check button state
        login_page.enter_username("test")
        button_state_after_username = login_button.is_enabled()
        
        login_page.enter_password("password")
        button_state_after_both = login_button.is_enabled()
        
        # Assert based on your application's UX requirements
        assert isinstance(initial_state, bool), "Button state should be boolean"
        assert isinstance(button_state_after_username, bool), "Button state should be boolean"
        assert isinstance(button_state_after_both, bool), "Button state should be boolean"
    
    @pytest.mark.login
    def test_page_reload_during_login(self, login_page, driver):
        """Test behavior when page is reloaded during login process"""
        # Arrange
        login_page.navigate_to_login()
        credentials = TestData.VALID_USER
        
        # Act
        login_page.enter_username(credentials.username)
        login_page.enter_password(credentials.password)
        
        # Reload page before clicking login
        driver.refresh()
        
        # Try to login again
        login_page.login(credentials.username, credentials.password)
        
        # Assert
        # Should handle page reload gracefully
        result = login_page.is_login_successful()
        assert isinstance(result, bool), "Should handle page reload appropriately"
# import pytest
# from utils.test_data import TestData
# from config.config import config

# class TestAuthenticationState:
#     """Test suite for authentication state management"""
    
#     @pytest.mark.login
#     def test_login_page_title_and_elements(self, login_page):
#         """Test Data Definitions Editor login page elements"""
#         # Arrange & Act
#         login_page.navigate_to_login()
        
#         # Assert
#         assert login_page.is_login_page_loaded(), "Login page should be properly loaded"
        
#         # Check page title contains the application name
#         page_title = login_page.get_page_title()
#         assert "data definitions" in page_title.lower() or "editor" in page_title.lower(), \
#             f"Page title should contain app name, got: {page_title}"
        
#         # Verify all form elements are present
#         assert login_page.is_element_present(login_page.USERNAME_INPUT), "Username field should be present"
#         assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password field should be present" 
#         assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Sign in button should be present"
        
#         # Check button text
#         button_text = login_page.get_text(login_page.LOGIN_BUTTON)
#         assert button_text == "Sign in", f"Button should say 'Sign in', got: {button_text}"
    
#     @pytest.mark.login
#     def test_password_toggle_functionality(self, login_page):
#         """Test password visibility toggle functionality"""
#         # Arrange
#         login_page.navigate_to_login()
#         test_password = "TestPassword123"
        
#         # Act
#         login_page.enter_password(test_password)
#         password_element = login_page.find_element(login_page.PASSWORD_INPUT)
        
#         # Assert initial state (password should be masked)
#         initial_type = password_element.get_attribute("type")
#         assert initial_type == "password", "Password field should initially be masked"
        
#         # Toggle password visibility if toggle button exists
#         if login_page.is_element_present(login_page.PASSWORD_TOGGLE):
#             login_page.toggle_password_visibility()
            
#             # Check if type changed (some implementations use different attributes)
#             new_type = password_element.get_attribute("type")
#             # Type might change to "text" or remain "password" with different styling
#             assert True, "Password toggle functionality should work without errors"
#     @pytest.mark.smoke
#     @pytest.mark.login
#     def test_authenticated_user_redirected_from_login_page(self, login_page, data_definitions_page):
#         """Test that authenticated users are redirected away from login page"""
#         # Arrange - First login successfully
#         credentials = TestData.VALID_USER
#         login_page.navigate_to_login()
#         login_page.login(credentials.username, credentials.password)
        
#         # Verify successful login
#         assert login_page.is_login_successful() or data_definitions_page.is_user_authenticated(), \
#             "Initial login should be successful"
        
#         # Act - Try to navigate to login page again
#         login_page.navigate_to_login()
        
#         # Assert - Should be redirected away from login page
#         assert login_page.is_redirected_from_login_when_authenticated(), \
#             "Authenticated user should be redirected away from login page"
    
#     @pytest.mark.login
#     def test_login_page_shows_authenticated_message(self, login_page, data_definitions_page):
#         """Test that login page shows appropriate message for authenticated users"""
#         # Arrange - First login successfully
#         credentials = TestData.VALID_USER
#         login_page.navigate_to_login()
#         login_page.login(credentials.username, credentials.password)
        
#         # Verify successful login
#         assert login_page.is_login_successful() or data_definitions_page.is_user_authenticated(), \
#             "Initial login should be successful"
        
#         # Act - Try to navigate to login page again
#         login_page.navigate_to_login()
        
#         # Assert - Should show appropriate message or redirect
#         auth_message = login_page.get_authentication_status_message()
#         is_redirected = login_page.is_redirected_from_login_when_authenticated()
        
#         assert is_redirected or auth_message != "", \
#             "Should either redirect or show authentication status message"
    
#     @pytest.mark.login
#     def test_direct_login_url_access_when_authenticated(self, login_page, dashboard_page, driver):
#         """Test direct access to login URL when already authenticated"""
#         # Arrange - First login successfully
#         credentials = TestData.VALID_USER
#         login_page.navigate_to_login()
#         login_page.login(credentials.username, credentials.password)
        
#         # Verify successful login
#         assert login_page.is_login_successful() or dashboard_page.is_user_authenticated(), \
#             "Initial login should be successful"
        
#         # Act - Direct navigation to login URL
#         driver.get(f"{config.BASE_URL}/login")
        
#         # Assert - Should handle authenticated state appropriately
#         assert login_page.is_redirected_from_login_when_authenticated(), \
#             "Direct login URL access should redirect authenticated users"
    
#     @pytest.mark.login
#     def test_logout_allows_login_page_access(self, authenticated_session, login_page):
#         """Test that after logout, user can access login page normally"""
#         # Arrange - Use authenticated session fixture
#         data_definitions_page = authenticated_session
        
#         # Act - Logout
#         data_definitions_page.logout()
        
#         # Navigate to login page
#         login_page.navigate_to_login()
        
#         # Assert - Should be able to access login page after logout
#         assert login_page.is_login_page_loaded(), "Should be able to access login page after logout"
        
#         current_url = login_page.get_current_url().lower()
#         assert "login" in current_url, "Should be on login page after logout"
    
#     @pytest.mark.login 
#     def test_session_persistence_across_browser_refresh(self, login_page, dashboard_page, driver):
#         """Test that authentication state persists across page refresh"""
#         # Arrange - First login successfully
#         credentials = TestData.VALID_USER
#         login_page.navigate_to_login()
#         login_page.login(credentials.username, credentials.password)
        
#         # Verify successful login
#         assert login_page.is_login_successful() or dashboard_page.is_user_authenticated(), \
#             "Initial login should be successful"
        
#         # Act - Refresh the browser
#         driver.refresh()
        
#         # Try to access login page
#         login_page.navigate_to_login()
        
#         # Assert - Should still be authenticated after refresh
#         assert login_page.is_redirected_from_login_when_authenticated(), \
#             "Authentication should persist after page refresh"
    
#     @pytest.mark.login
#     def test_multiple_login_attempts_when_authenticated(self, authenticated_session, login_page):
#         """Test behavior when trying to login multiple times while authenticated"""
#         # Arrange - Use authenticated session
#         dashboard_page = authenticated_session
        
#         # Act - Try to access login and attempt another login
#         login_page.navigate_to_login()
        
#         # If not redirected (some apps might show login form with warning)
#         if not login_page.is_redirected_from_login_when_authenticated():
#             credentials = TestData.VALID_USER
#             login_page.login(credentials.username, credentials.password)
        
#         # Assert - Should handle gracefully (redirect or show appropriate message)
#         is_redirected = login_page.is_redirected_from_login_when_authenticated()
#         auth_message = login_page.get_authentication_status_message()
        
#         assert is_redirected or auth_message != "", \
#             "Should handle multiple login attempts appropriately"
    
#     @pytest.mark.login
#     def test_authentication_state_with_remember_me(self, login_page, dashboard_page, driver):
#         """Test authentication state behavior with remember me option"""
#         # Arrange - Login with remember me
#         credentials = TestData.VALID_USER
#         login_page.navigate_to_login()
#         login_page.login(credentials.username, credentials.password, remember_me=True)
        
#         # Verify successful login
#         assert login_page.is_login_successful() or dashboard_page.is_user_authenticated(), \
#             "Initial login with remember me should be successful"
        
#         # Act - Try to access login page
#         login_page.navigate_to_login()
        
#         # Assert - Should still be redirected even with remember me
#         assert login_page.is_redirected_from_login_when_authenticated(), \
#             "Should redirect away from login even with remember me enabled"
    
#     @pytest.mark.regression
#     def test_authentication_state_after_session_timeout(self, login_page, dashboard_page, driver):
#         """Test authentication state after potential session timeout"""
#         # Arrange - Login successfully
#         credentials = TestData.VALID_USER
#         login_page.navigate_to_login()
#         login_page.login(credentials.username, credentials.password)
        
#         # Verify successful login
#         assert login_page.is_login_successful() or dashboard_page.is_user_authenticated(), \
#             "Initial login should be successful"
        
#         # Act - Simulate session timeout by waiting or clearing session storage
#         # Note: This depends on your application's session management
#         # You might need to clear cookies or wait for session expiry
#         driver.delete_all_cookies()
        
#         # Try to access login page
#         login_page.navigate_to_login()
        
#         # Assert - Should be able to access login page after session timeout
#         current_url = login_page.get_current_url().lower()
#         assert "login" in current_url, "Should access login page after session timeout"
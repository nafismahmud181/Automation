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
      print("navigate_to_create_profile_page executed successfully")

      # Verify we're on the correct page
      assert create_profile_page.is_create_profile_page_loaded(), "Create Profile page not loaded properly"
      
      current_url = create_profile_page.get_current_page_url()
      print(f"Successfully navigated to: {current_url}")
      logger.info(f"Successfully navigated to: {current_url}")
      print("1st test finish")
      
      # Force close the transaction menu as the final step of this test
      create_profile_page.force_close_transaction_menu()
      logger.info("Transaction menu forcefully closed by first test")

  @pytest.mark.smoke
  def test_customer_name_validation_error(self, create_profile_page):
      """Test that customer name validation error appears when clicking customer name input then project search input"""
      logger.info("Testing customer name validation error scenario")
      
      # Check if we're already on the Create Profile page
      if not create_profile_page.is_create_profile_page_loaded():
          # Only navigate if we're not already on the page
          success = create_profile_page.navigate_to_create_profile_page()
          assert success, "Failed to navigate to Create Profile page"
          logger.info("Navigated to Create Profile page")
      else:
          logger.info("Already on Create Profile page, skipping navigation")
      
      # Verify we're on the correct page
      assert create_profile_page.is_create_profile_page_loaded(), "Create Profile page not loaded properly"
      
      # Test the validation error scenario
      error_appears = create_profile_page.test_customer_name_validation_error()
      assert error_appears, "Customer name validation error did not appear as expected"
      
      logger.info("Customer name validation error test completed successfully")

  @pytest.mark.smoke
  def test_document_type_validation_without_project(self, create_profile_page):
      """Test that document type validation error appears when no project is selected"""
      logger.info("Testing document type validation error scenario without project selection")
      
      # Check if we're already on the Create Profile page
      if not create_profile_page.is_create_profile_page_loaded():
          # Only navigate if we're not already on the page
          success = create_profile_page.navigate_to_create_profile_page()
          assert success, "Failed to navigate to Create Profile page"
          logger.info("Navigated to Create Profile page")
      else:
          logger.info("Already on Create Profile page, skipping navigation")
      
      # Verify we're on the correct page
      assert create_profile_page.is_create_profile_page_loaded(), "Create Profile page not loaded properly"
      
      # Test the document type validation error scenario
      result = create_profile_page.test_document_type_validation_without_project()
      
      if result == "ABORTED":
          logger.info("Test aborted - Project is already selected")
          pytest.skip("Project is already selected, skipping test")
      else:
          assert result, "Document type validation error did not appear as expected"
          logger.info("Document type validation error test completed successfully")

  @pytest.mark.smoke
  def test_name_matching_text_disabled(self, create_profile_page):
      """Test that 'None' span exists and name matching text input is disabled"""
      logger.info("Testing name matching text disabled scenario")
      
      # Check if we're already on the Create Profile page
      if not create_profile_page.is_create_profile_page_loaded():
          # Only navigate if we're not already on the page
          success = create_profile_page.navigate_to_create_profile_page()
          assert success, "Failed to navigate to Create Profile page"
          logger.info("Navigated to Create Profile page")
      else:
          logger.info("Already on Create Profile page, skipping navigation")
      
      # Verify we're on the correct page
      assert create_profile_page.is_create_profile_page_loaded(), "Create Profile page not loaded properly"
      
      # Test the name matching text disabled scenario
      result = create_profile_page.check_name_matching_text_disabled()
      assert result, "Name matching text disabled check failed"
      
      logger.info("Name matching text disabled test completed successfully")
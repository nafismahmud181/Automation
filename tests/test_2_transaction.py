import pytest
import time
import os
from utils.test_data import TestData
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.transaction
@pytest.mark.usefixtures("transaction_driver")
class TestTransactionPage:
    """Test suite for transaction search functionality"""

    # @pytest.mark.smoke
    # def test_ID_valid_search(self, transaction_page):
    #     logger.info("Testing ID search with valid text")

    #     search_text = TestData.ID_VALID_SEARCH_TEXT
    #     transaction_page.search_by_id(search_text)

    #     assert transaction_page.is_search_successful(search_text), \
    #         f"Search should find element with data-id='email-batch {search_text} id'"

    #     results = transaction_page.get_ID_search_results(search_text)
    #     assert results != "", f"No results found for search text '{search_text}'"
    #     assert search_text.lower() in results.lower(), f"Results should contain '{search_text}'"

    #     transaction_page.click_clear_search_button()
    #     logger.info("Valid ID search test completed successfully")


    # def test_ID_invalid_search(self, transaction_page):
    #     """Test ID search with invalid text"""
    #     logger.info("Testing ID search with invalid text")

    #     search_text = TestData.ID_INVALID_SEARCH_TEXT

    #     transaction_page.search_by_id(search_text)

    #     assert transaction_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

    #     transaction_page.click_clear_search_button()

    #     logger.info("Invalid ID search test completed successfully")
   
    # @pytest.mark.smoke
    # def test_email_from_valid_search(self, transaction_page):
    #     logger.info("Testing email-from search with valid text")

    #     search_text = TestData.EMAIL_FROM_VALID_SEARCH_TEXT
    #     transaction_page.search_by_email_from(search_text)

    #     # Wait and collect all email-from column results
    #     email_results = transaction_page.get_email_from_results()

    #     # Log the count of email-from entries
    #     logger.info(f"Found {len(email_results)} email-from entries after search")

    #     # Assert we received at least one result
    #     assert email_results, f"No email-from results found for '{search_text}'"

    #     # Assert each result contains the searched text (case-insensitive)
    #     for email in email_results:
    #         assert search_text.lower() in email.lower(), \
    #             f"Expected '{search_text}' to be in result '{email}'"

    #     transaction_page.click_clear_search_button()
    #     logger.info("Valid email-from search test completed successfully")


    # def test_email_from_invalid_search(self, transaction_page):
    #     """Test Email From search with invalid text"""
    #     logger.info("Testing ID search with invalid text")

    #     search_text = TestData.EMAIL_FROM_INVALID_SEARCH_TEXT

    #     # Use the clearly named method
    #     transaction_page.search_by_email_from(search_text)

    #     # Assert that the "No results found" message appears
    #     assert transaction_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

    #     # Optional: Clear the search box or go back to the main page if needed
    #     transaction_page.click_clear_search_button()
    #     logger.info("Invalid Email From search test completed successfully")
   
    # @pytest.mark.smoke
    # def test_email_subject_valid_search(self, transaction_page):
    #     logger.info("Testing email-subject search with valid text")

    #     search_text = TestData.EMAIL_SUBJECT_VALID_SEARCH_TEXT
    #     transaction_page.search_by_email_subject(search_text)

    #     # Wait and collect all email-subject column results
    #     email_results = transaction_page.get_email_subject_results()

    #     # Assert we received at least one result
    #     assert email_results, f"No email-subject results found for '{search_text}'"

    #     # Assert each result contains the searched text (case-insensitive)
    #     for email in email_results:
    #         assert search_text.lower() in email.lower(), \
    #             f"Expected '{search_text}' to be in result '{email}'"

    #     transaction_page.click_clear_search_button()
    #     logger.info("Valid email-subject search test completed successfully")


    # def test_email_subject_invalid_search(self, transaction_page):
    #     """Test Email subject search with invalid text"""
    #     logger.info("Testing ID search with invalid text")

    #     search_text = TestData.EMAIL_SUBJECT_INVALID_SEARCH_TEXT

    #     # Use the clearly named method
    #     transaction_page.search_by_email_subject(search_text)

    #     # Assert that the "No results found" message appears
    #     assert transaction_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

    #     # Optional: Clear the search box or go back to the main page if needed
    #     transaction_page.click_clear_search_button()
    #     logger.info("Invalid Email subject search test completed successfully")

   
    # @pytest.mark.smoke
    # def test_matched_profile_valid_search(self, transaction_page):
    #     logger.info("Testing matched profile search with valid text")

    #     search_text = TestData.MATCHED_PROFILE_VALID_SEARCH_TEXT
    #     transaction_page.search_by_matched_profile(search_text)

    #     # Wait and collect all matched_profile column results
    #     email_results = transaction_page.get_matched_profile_results()

    #     # Assert we received at least one result
    #     assert email_results, f"No matched_profile results found for '{search_text}'"

    #     # Assert each result contains the searched text (case-insensitive)
    #     for email in email_results:
    #         assert search_text.lower() in email.lower(), \
    #             f"Expected '{search_text}' to be in result '{email}'"

    #     transaction_page.click_clear_search_button()
    #     logger.info("Valid matched_profile search test completed successfully")



    # def test_matched_profile_invalid_search(self, transaction_page):
    #     """Test Matched Profile search with invalid text"""
    #     logger.info("Testing ID search with invalid text")

    #     search_text = TestData.MATCHED_PROFILE_INVALID_SEARCH_TEXT

    #     # Use the clearly named method
    #     transaction_page.search_by_matched_profile(search_text)

    #     # Assert that the "No results found" message appears
    #     assert transaction_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

    #     # Optional: Clear the search box or go back to the main page if needed
    #     transaction_page.click_clear_search_button()
    #     logger.info("Invalid Email subject search test completed successfully")


    # @pytest.mark.smoke
    # def test_confirmation_number_valid_search(self, transaction_page):
    #     logger.info("Testing matched profile search with valid text")

    #     search_text = TestData.CONFIRMATION_NUMBER_VALID_SEARCH_TEXT
    #     transaction_page.search_by_confirmation_number(search_text)

    #     # Wait and collect all confirmation_number column results
    #     email_results = transaction_page.get_confirmation_number_results()

    #     # Assert we received at least one result
    #     assert email_results, f"No confirmation_number results found for '{search_text}'"

    #     # Assert each result contains the searched text (case-insensitive)
    #     for email in email_results:
    #         assert search_text.lower() in email.lower(), \
    #             f"Expected '{search_text}' to be in result '{email}'"

    #     transaction_page.click_clear_search_button()
    #     logger.info("Valid confirmation_number search test completed successfully")



    # def test_confirmation_number_invalid_search(self, transaction_page):
    #     """Test Matched Profile search with invalid text"""
    #     logger.info("Testing ID search with invalid text")

    #     search_text = TestData.CONFIRMATION_NUMBER_INVALID_SEARCH_TEXT

    #     # Use the clearly named method
    #     transaction_page.search_by_confirmation_number(search_text)

    #     # Assert that the "No results found" message appears
    #     assert transaction_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

    #     # Optional: Clear the search box or go back to the main page if needed
    #     transaction_page.click_clear_search_button()
    #     logger.info("Invalid Email subject search test completed successfully")

   
    # def test_batch_upload_valid_file(self, transaction_page):
    #     """Test batch upload with nvalid ZIP file"""
    #     logger.info("Testing batch upload with nvalid ZIP file")
        
    #     valid_file_path = os.path.join(os.getcwd(), "assets", "20250723.U04246.zip")
        
    #     # Skip if test file not available
    #     if not os.path.exists(valid_file_path):
    #         pytest.skip(f"nvalid ZIP file not found: {valid_file_path}")
        
    #     # Perform batch upload with invalid file
    #     transaction_page.perform_batch_upload(valid_file_path)
        
    #     # Get upload result message
    #     message = transaction_page.get_upload_message(timeout=10)
        
    #     # Verify error message
    #     # assert "Invalid Zip file. Zip should contain db_data.json" in message, \
    #     #     f"Expected invalid ZIP error message, got: {message}"
        
    #     logger.info(f"Valid ZIP file upload test completed. Error: {message}")


    # def test_batch_upload_invalid_file(self, transaction_page):
    #     """Test batch upload with invalid ZIP file"""
    #     logger.info("Testing batch upload with invalid ZIP file")
        
    #     invalid_file_path = os.path.join(os.getcwd(), "assets", "invalid_file.zip")
        
    #     # Skip if test file not available
    #     if not os.path.exists(invalid_file_path):
    #         pytest.skip(f"Invalid ZIP file not found: {invalid_file_path}")
        
    #     # Perform batch upload with invalid file
    #     transaction_page.perform_batch_upload(invalid_file_path)
        
    #     # Get upload result message
    #     message = transaction_page.get_upload_message(timeout=10)
        
    #     # Verify error message
    #     assert "Invalid Zip file. Zip should contain db_data.json" in message, \
    #         f"Expected invalid ZIP error message, got: {message}"
        
    #     logger.info(f"Invalid ZIP file upload test completed. Error: {message}")

    @pytest.mark.smoke
    def test_linked_batches_valid_search(self, transaction_page):
        """Test linked-batches search with valid text"""
        logger.info("Testing linked-batches search with valid text")

        search_text = TestData.LINKED_BATCHES_VALID_SEARCH_TEXT
        transaction_page.search_by_linked_batches(search_text)

        # Check if the search was successful by looking for the element with data-id="email-batch {search_text} id"
        assert transaction_page.is_linked_batches_search_successful(search_text), \
            f"Search should find element with data-id='email-batch {search_text} id'"

        transaction_page.click_clear_search_button()
        logger.info("Valid linked-batches search test completed successfully")

    def test_linked_batches_invalid_search(self, transaction_page):
        """Test linked-batches search with invalid text"""
        logger.info("Testing linked-batches search with invalid text")

        search_text = TestData.LINKED_BATCHES_INVALID_SEARCH_TEXT
        transaction_page.search_by_linked_batches(search_text)

        # Assert that the "No results found" message appears
        assert transaction_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        transaction_page.click_clear_search_button()
        logger.info("Invalid linked-batches search test completed successfully")

    
    
import pytest
import time
import os
from utils.test_data import TestData
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.transaction
@pytest.mark.usefixtures("transaction_driver")
class TestTransactionSearch:
    """Test suite for transaction search functionality"""

    @pytest.mark.smoke
    def test_ID_valid_search(self, transaction_page):
        logger.info("Testing ID search with valid text")

        search_text = TestData.ID_VALID_SEARCH_TEXT
        transaction_page.search_by_id(search_text)

        assert transaction_page.is_search_successful(search_text), \
            f"Search should find element with data-id='email-batch {search_text} id'"

        results = transaction_page.get_search_results(search_text)
        assert results != "", f"No results found for search text '{search_text}'"
        assert search_text.lower() in results.lower(), f"Results should contain '{search_text}'"

        transaction_page.click_clear_search_button()
        logger.info("Valid ID search test completed successfully")


    def test_ID_invalid_search(self, transaction_page):
        """Test ID search with invalid text"""
        logger.info("Testing ID search with invalid text")

        search_text = TestData.ID_INVALID_SEARCH_TEXT

        # Use the clearly named method
        transaction_page.search_by_id(search_text)

        # Assert that the "No results found" message appears
        assert transaction_page.is_no_results_displayed(), "Expected 'No results found' message not displayed"

        # Optional: Clear the search box or go back to the main page if needed
        transaction_page.click_clear_search_button()
        # OR if you use a Go Back button instead:
        # transaction_page.click_go_back_button()

        logger.info("Invalid ID search test completed successfully")
   
    @pytest.mark.smoke
    def test_Email_From_valid_search(self, transaction_page):
        """Test search with valid text"""
        logger.info("Testing search with valid text")
        
        # Valid search text that should return results
        search_text = TestData.EMAIL_FROM_VALID_SEARCH_TEXT
        
        # Perform search
        transaction_page.search_text(search_text)
        
        # Verify search was successful using the dynamic search text
        assert transaction_page.is_search_successful(search_text), \
            f"Search should find element with data-id='email-batch {search_text} id'"
        
        # Verify results contain the search text
        results = transaction_page.get_search_results(search_text)
        assert results != "", f"No results found for search text '{search_text}'"
        assert search_text.lower() in results.lower(), f"Results should contain '{search_text}'"
        
        # Click clear search button after assertions
        transaction_page.click_clear_search_button()

        logger.info("Valid search test completed successfully")


    def test_Email_From_invalid_search(self, transaction_page):
        """Test search with invalid text"""
        logger.info("Testing search with invalid text")
        
        # Invalid search text that should return no results
        search_text = TestData.EMAIL_FROM_INVALID_SEARCH_TEXT
        
        # Perform search
        transaction_page.search_text(search_text)
        
        # Verify no results message is displayed
        assert transaction_page.is_no_results_displayed(), "No results message should be displayed"

        # Click clear search button after assertions
        transaction_page.click_clear_search_button()
        
        logger.info("Invalid search test completed successfully")

   
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

    
    
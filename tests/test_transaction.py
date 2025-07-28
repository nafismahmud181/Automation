import pytest
import os
from utils.test_data import TestData
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.transaction
@pytest.mark.usefixtures("transaction_driver")
class TestTransactionSearch:
    """Test suite for transaction search functionality"""

    @pytest.mark.smoke
    # def test_valid_search(self, transaction_page):
    #     """Test search with valid text"""
    #     logger.info("Testing search with valid text")
        
    #     # Valid search text that should return results
    #     search_text = TestData.VALID_SEARCH_TEXT
        
    #     # Perform search
    #     transaction_page.search_text(search_text)
        
    #     # Verify search was successful using the dynamic search text
    #     assert transaction_page.is_search_successful(search_text), f"Search should find element with data-id='email-batch {search_text} id'"
        
    #     # Verify results contain the search text
    #     results = transaction_page.get_search_results(search_text)
    #     assert results != "", f"No results found for search text '{search_text}'"
    #     assert search_text.lower() in results.lower(), f"Results should contain '{search_text}'"
        
    #     logger.info("Valid search test completed successfully")

    # def test_invalid_search(self, transaction_page):
    #     """Test search with invalid text"""
    #     logger.info("Testing search with invalid text")
        
    #     # Invalid search text that should return no results
    #     search_text = TestData.INVALID_SEARCH_TEXT
        
    #     # Perform search
    #     transaction_page.search_text(search_text)
        
    #     # Verify no results message is displayed
    #     assert transaction_page.is_no_results_displayed(), "No results message should be displayed"
        
    #     logger.info("Invalid search test completed successfully")

    # @pytest.mark.smoke
    # def test_batch_upload_success(self, transaction_page):
    #     """Test successful batch upload of ZIP file"""
    #     logger.info("Testing batch upload functionality")
        
    #     # Get upload data from test data
    #     upload_data = TestData.BATCH_UPLOAD_FILE
        
    #     # Verify file exists before attempting upload
    #     assert os.path.exists(upload_data.file_path), f"Upload file not found: {upload_data.file_path}"
        
    #     # Perform batch upload
    #     transaction_page.perform_batch_upload(upload_data.file_path)
        
    #     # Wait for upload to process
    #     transaction_page.wait_for_element(transaction_page.UPLOAD_SUCCESS_MESSAGE, timeout=30)
        
    #     # Verify upload was successful
    #     assert transaction_page.is_upload_successful(), "Upload should be successful"
        
    #     # Get and verify success message
    #     upload_message = transaction_page.get_upload_message()
    #     assert upload_message != "", "Upload success message should be displayed"
        
    #     logger.info(f"Batch upload test completed successfully. Message: {upload_message}")

    def test_batch_upload_invalid_file(self, transaction_page):
        """Test batch upload with invalid ZIP file"""
        logger.info("Testing batch upload with invalid ZIP file")
        
        invalid_file_path = os.path.join(os.getcwd(), "assets", "invalid_file.zip")
        
        # Skip if test file not available
        if not os.path.exists(invalid_file_path):
            pytest.skip(f"Invalid ZIP file not found: {invalid_file_path}")
        
        # Perform batch upload with invalid file
        transaction_page.perform_batch_upload(invalid_file_path)
        
        # Get upload result message
        message = transaction_page.get_upload_message(timeout=10)
        
        # Verify error message
        assert "Invalid Zip file. Zip should contain db_data.json" in message, \
            f"Expected invalid ZIP error message, got: {message}"
        
        logger.info(f"Invalid ZIP file upload test completed. Error: {message}")

    
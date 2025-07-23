import pytest
from utils.test_data import TestData
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.transaction
@pytest.mark.usefixtures("transaction_driver")
class TestTransactionSearch:
    """Test suite for transaction search functionality"""

    @pytest.mark.smoke
    def test_valid_search(self, transaction_page):
        """Test search with valid text"""
        logger.info("Testing search with valid text")
        
        # Valid search text that should return results
        search_text = "valid_search_term"  # Update with a valid search term
        
        # Perform search
        transaction_page.search_text(search_text)
        
        # Verify search was successful
        assert transaction_page.is_search_successful(), "Search should display results"
        
        # Verify results contain the search text
        results = transaction_page.get_search_results()
        assert search_text.lower() in results.lower(), f"Results should contain '{search_text}'"
        
        logger.info("Valid search test completed successfully")

    def test_invalid_search(self, transaction_page):
        """Test search with invalid text"""
        logger.info("Testing search with invalid text")
        
        # Invalid search text that should return no results
        search_text = "InvalidSearchThatShouldNotExist123!@#"
        
        # Perform search
        transaction_page.search_text(search_text)
        
        # Verify no results message is displayed
        assert transaction_page.is_no_results_displayed(), "No results message should be displayed"
        
        logger.info("Invalid search test completed successfully")

    def test_empty_search(self, transaction_page):
        """Test search with empty text"""
        logger.info("Testing search with empty text")
        
        # Perform empty search
        transaction_page.search_text("")
        
        # Verify appropriate behavior for empty search
        assert not transaction_page.is_search_successful(), "Empty search should not show results"
        
        logger.info("Empty search test completed successfully")

    def test_special_characters_search(self, transaction_page):
        """Test search with special characters"""
        logger.info("Testing search with special characters")
        
        # Search text with special characters
        search_text = "!@#$%^&*()"
        
        # Perform search
        transaction_page.search_text(search_text)
        
        # Verify appropriate handling of special characters
        assert transaction_page.is_no_results_displayed(), "Special characters should be handled gracefully"
        
        logger.info("Special characters search test completed successfully")

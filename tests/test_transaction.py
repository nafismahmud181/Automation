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
        search_text = "20250721.00005"
        
        # Perform search
        transaction_page.search_text(search_text)
        
        # Verify search was successful using the dynamic search text
        assert transaction_page.is_search_successful(search_text), f"Search should find element with data-id='email-batch {search_text} id'"
        
        # Verify results contain the search text
        results = transaction_page.get_search_results(search_text)
        assert results != "", f"No results found for search text '{search_text}'"
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

    

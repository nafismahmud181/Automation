import pytest
import time
from utils.test_data import TestData
from utils.logger import get_logger
from selenium.common.exceptions import TimeoutException

logger = get_logger(__name__)

@pytest.mark.batch_editor
@pytest.mark.usefixtures("batch_editor_driver")
class TestBatchEditorPage:
    """Test suite for batch editor functionality"""
    
    @pytest.mark.smoke
    def test_batch_editor_navigation_and_add_count_button(self, batch_editor_page):
        """Test navigation to batch editor and verify add-count-button is present"""
        logger.info("Testing batch editor navigation and add-count-button presence")
        
        # Navigate to the specific batch editor page
        batch_editor_page.navigate_to_batch_editor()
        
        # Wait for page to load and verify add-count-button is present
        assert batch_editor_page.is_add_count_button_present(timeout=20), \
            "Add count button should be present on the batch editor page"
        
        logger.info("Batch editor navigation test completed successfully - add-count-button found")
    
    @pytest.mark.smoke
    def test_add_count_button_clickable(self, batch_editor_page):
        """Test that the add-count-button is clickable after navigation"""
        logger.info("Testing add-count-button clickability")
        
        # Navigate to the batch editor page
        batch_editor_page.navigate_to_batch_editor()
        
        # Wait for the button to be clickable
        try:
            button = batch_editor_page.wait_for_add_count_button(timeout=20)
            assert button.is_enabled(), "Add count button should be enabled"
            logger.info("Add count button is clickable and enabled")
        except TimeoutException:
            pytest.fail("Add count button should be clickable within 20 seconds")

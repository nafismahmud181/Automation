import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestHelpers:
    @staticmethod
    def take_screenshot(driver, test_name: str) -> str:
        """Take screenshot and save with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        driver.save_screenshot(filename)
        return filename
    
    @staticmethod
    def wait_for_element(driver, locator: tuple, timeout: int = 10):
        """Wait for element to be present and visible"""
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    @staticmethod
    def wait_for_element_clickable(driver, locator: tuple, timeout: int = 10):
        """Wait for element to be clickable"""
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @staticmethod
    def clear_and_send_keys(element, text: str):
        """Clear element and send keys"""
        element.clear()
        element.send_keys(text)

    @staticmethod
    def get_download_dir() -> str:
        """Return absolute path to the test downloads directory"""
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)
        return os.path.abspath(download_dir)

    @staticmethod
    def clear_download_dir():
        """Remove all files in the download directory"""
        download_dir = TestHelpers.get_download_dir()
        for entry in os.listdir(download_dir):
            try:
                path = os.path.join(download_dir, entry)
                if os.path.isfile(path):
                    os.remove(path)
            except Exception:
                pass

    @staticmethod
    def wait_for_download_complete(timeout: int = 60, filename_contains: str | None = None) -> str:
        """Wait until a file is fully downloaded in the downloads directory.

        Returns the path to the downloaded file, or empty string on timeout.
        If filename_contains is provided, prefer a file containing that substring.
        """
        download_dir = TestHelpers.get_download_dir()
        start_time = time.time()

        def is_temp(name: str) -> bool:
            lower = name.lower()
            return lower.endswith(".crdownload") or lower.endswith(".tmp") or lower.endswith(".part")

        selected_path = ""
        while time.time() - start_time < timeout:
            try:
                entries = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
                # Exclude temp/in-progress files
                ready_files = [f for f in entries if not is_temp(f)]
                if filename_contains:
                    for f in ready_files:
                        if filename_contains in f:
                            return os.path.join(download_dir, f)
                if ready_files:
                    # Return the newest ready file
                    ready_files.sort(key=lambda f: os.path.getmtime(os.path.join(download_dir, f)), reverse=True)
                    selected_path = os.path.join(download_dir, ready_files[0])
                    return selected_path
            except Exception:
                pass
            time.sleep(0.5)
        return selected_path
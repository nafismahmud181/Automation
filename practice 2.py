from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

# --- Setup ---
driver = webdriver.Chrome()
driver.get("http://10.10.1.13/login")
driver.maximize_window()
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "login-password"))
)

# --- Step 2: Input username ---
driver.find_element(By.XPATH, "//input[@id='login-username']").send_keys("admin")  # Change locator

# --- Step 3: Input password ---
driver.find_element(By.XPATH, "//input[@id='login-password']").send_keys("admin")  # Change locator

# --- Step 4: Click login button ---
driver.find_element(By.XPATH, "//button[normalize-space()='Sign in']").click()  # Change locator

time.sleep(5)  # Wait for login

# --- Step 5: Hover a button ---
hover_button = driver.find_element(By.XPATH, "//a[@data-id='nav-group-toggle-home']")  # Change locator
ActionChains(driver).move_to_element(hover_button).perform()
time.sleep(1)

# --- Step 6: Click a button ---
driver.find_element(By.XPATH, "//li[@data-id='nav-group-item-create-profile']").click()  # Change locator


time.sleep(5)

# Locators
PROJECT_SELECTED = (By.XPATH, "//div[@data-id='profile-create project']//input[@type='search']")
MANUAL_VALIDATION_SWITCH = (By.XPATH, "//input[@data-id='profile-create manual-validation']")


def test_manual_validation_switch(driver):
    wait = WebDriverWait(driver, 10)

    # Step 1: Check if project field is displayed
    try:
        project_field = wait.until(EC.presence_of_element_located(PROJECT_SELECTED))
        if project_field.is_displayed():
            print("✅ PROJECT_SELECTED is displayed. Skipping switch check.")
            return  # Exit test if project field is already visible
    except:
        print("⚠️ PROJECT_SELECTED not found, continuing with switch logic.")

    # Step 2: Check if manual validation switch is selected
    switch = wait.until(EC.presence_of_element_located(MANUAL_VALIDATION_SWITCH))
    if switch.is_selected():
        print("ℹ️ Switch is ON, proceeding with project search.")

        # Step 3: Select project
        project_field = wait.until(EC.element_to_be_clickable(PROJECT_SELECTED))
        project_field.click()
        time.sleep(1)
        project_field.send_keys("ShipmentCreate")
        project_field.send_keys(u"\ue007")  # Press Enter

        time.sleep(2)  # allow UI to update

        # Step 4: Verify switch is now OFF
        if not switch.is_selected():
            print("✅ Test successful: Switch turned OFF after project selection.")
        else:
            pytest.fail("❌ Test failed: Switch is still ON after project selection.")
    else:
        pytest.fail("❌ Test failed: Switch was already OFF before selecting project.")

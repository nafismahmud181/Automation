from dataclasses import dataclass
from typing import List, Dict
import os

@dataclass
class LoginCredentials:
    username: str
    password: str
    expected_result: str

@dataclass
class UploadData:
    file_path: str
    file_name: str
    expected_result: str

class TestData:
    # Valid credentials
    VALID_USER = LoginCredentials(
        username="admin",
        password="admin",
        expected_result="success"
    )
    
    # Invalid credentials test cases
    INVALID_CREDENTIALS = [
        LoginCredentials("invalid@example.com", "wrongpass", "invalid_credentials"),
        LoginCredentials("", "password", "empty_username"),
        LoginCredentials("user@example.com", "", "empty_password"),
        LoginCredentials("", "", "empty_fields"),
        LoginCredentials("notanemail", "password", "invalid_email_format"),
        LoginCredentials("user@example.com", "123", "weak_password"),
    ]
    
    # SQL injection test cases
    SQL_INJECTION_CASES = [
        LoginCredentials("admin'; DROP TABLE users; --", "password", "sql_injection"),
        LoginCredentials("' OR '1'='1", "' OR '1'='1", "sql_injection"),
        LoginCredentials("admin'/*", "password", "sql_injection"),
    ]
    
    # XSS test cases
    XSS_CASES = [
        LoginCredentials("<script>alert('xss')</script>", "password", "xss_attempt"),
        LoginCredentials("user@example.com", "<img src=x onerror=alert(1)>", "xss_attempt"),
    ]
    
    # Upload test data
    BATCH_UPLOAD_FILE = UploadData(
        file_path=os.path.join(os.getcwd(), "assets", "20250723.U04246.zip"),
        file_name="20250723.U04246.zip",
        expected_result="success"
    )
    #Transaction Page Search test data
    #ID Search test data
    ID_VALID_SEARCH_TEXT = "20250721.00005"
    ID_INVALID_SEARCH_TEXT = "InvalidSearchThatShouldNotExist123!@#"

    # Email From Search test data
    EMAIL_FROM_VALID_SEARCH_TEXT = "ayushman.bokde@dhl.com"
    EMAIL_FROM_INVALID_SEARCH_TEXT = "InvalidEmailSearchThatShouldNotExist123!@#"

    # Email Subject Search test data
    EMAIL_SUBJECT_VALID_SEARCH_TEXT = "testing pdf msg eml"
    EMAIL_SUBJECT_INVALID_SEARCH_TEXT = "InvalidEmailSubjectSearchThatShouldNotExist123!@#"

    # Matched Profile Search test data
    MATCHED_PROFILE_VALID_SEARCH_TEXT = "JP_WEBBOOKING_SEA_ShipmentCreate"
    MATCHED_PROFILE_INVALID_SEARCH_TEXT = "InvalidMatchedProfileSearchThatShouldNotExist123!@#"

    # Confirmation Number Search test data
    CONFIRMATION_NUMBER_VALID_SEARCH_TEXT = "S2500057129"
    CONFIRMATION_NUMBER_INVALID_SEARCH_TEXT = "InvalidConfirmationNumberSearchThatShouldNotExist123!@#"

    # Linked Batches Search test data
    LINKED_BATCHES_VALID_SEARCH_TEXT = "20250807.100017"
    LINKED_BATCHES_INVALID_SEARCH_TEXT = "InvalidLinkedBatchesSearchThatShouldNotExist123!@#"

    # Combobox Search test data
    COMBOBOX_VALID_SEARCH_TEXT = "100"
    COMBOBOX_INVALID_SEARCH_TEXT = "InvalidComboboxSearchThatShouldNotExist123!@#"

    #Profile Management Page Search test data
    PROFILE_NAME_VALID_SEARCH_TEXT = "BD_NIPU_ALL_CreateCustomsJob (B+CIV)"
    PROFILE_NAME_INVALID_SEARCH_TEXT = "InvalidProfileSearchThatShouldNotExist123!@#"

    # Customer Name Search test data
    CUSTOMER_NAME_VALID_SEARCH_TEXT = "Nafis"
    CUSTOMER_NAME_INVALID_SEARCH_TEXT = "InvalidCustomerSearchThatShouldNotExist123!@#"
    
    # Email Subject Search test data
    EMAIL_SUBJECT_VALID_SEARCH_TEXT = "Meem12345678"
    EMAIL_SUBJECT_INVALID_SEARCH_TEXT = "InvalidEmailSubjectSearchThatShouldNotExist123!@#"

    # Project Name Search test data
    PROJECT_NAME_VALID_SEARCH_TEXT = "CreateCustomsJob (B+CIV)"
    PROJECT_NAME_INVALID_SEARCH_TEXT = "InvalidProjectSearchThatShouldNotExist123!@#"

    # Country Search test data
    COUNTRY_VALID_SEARCH_TEXT = "BD"
    COUNTRY_INVALID_SEARCH_TEXT = "InvalidCountrySearchThatShouldNotExist123!@#"

    # Mode of Transport Search test data
    MODE_OF_TRANSPORT_VALID_SEARCH_TEXT = "Air"
    MODE_OF_TRANSPORT_INVALID_SEARCH_TEXT = "InvalidTransportSearchThatShouldNotExist123!@#"


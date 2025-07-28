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
    
    # Search test data
    VALID_SEARCH_TEXT = "20250721.00005"
    INVALID_SEARCH_TEXT = "InvalidSearchThatShouldNotExist123!@#"
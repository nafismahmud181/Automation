import os
from dataclasses import dataclass

@dataclass
class TestConfig:
    BASE_URL: str = os.getenv('BASE_URL', 'http://10.10.1.10/login')
    BROWSER: str = os.getenv('BROWSER', 'chrome')
    HEADLESS: bool = os.getenv('HEADLESS', 'false').lower() == 'true'
    IMPLICIT_WAIT: int = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT: int = int(os.getenv('EXPLICIT_WAIT', '20'))
    SCREENSHOT_ON_FAILURE: bool = True
    
config = TestConfig()
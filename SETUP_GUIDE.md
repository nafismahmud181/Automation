# Setup Guide for Windows 11

This guide will help you set up and run the AIDB v6 pytest automation project on your Windows 11 laptop.

## Prerequisites

### 1. Python Installation
- **Download Python**: Go to [python.org](https://www.python.org/downloads/) and download Python 3.8 or higher
- **Install Python**: Run the installer and make sure to check "Add Python to PATH" during installation
- **Verify Installation**: Open Command Prompt and run:
  ```cmd
  python --version
  pip --version
  ```

### 2. Git Installation (if not already installed)
- **Download Git**: Go to [git-scm.com](https://git-scm.com/download/win) and download Git for Windows
- **Install Git**: Run the installer with default settings
- **Verify Installation**: Open Command Prompt and run:
  ```cmd
  git --version
  ```

## Project Setup

### 1. Clone or Download the Project
If you have the project files:
- Extract the ZIP file to a folder on your computer (e.g., `C:\Projects\AIDB-v6-pytest`)

If you need to clone from a repository:
```cmd
git clone <repository-url>
cd AIDB-v6-pytest
```

### 2. Open Command Prompt
- Press `Win + R`, type `cmd`, and press Enter
- Navigate to your project directory:
  ```cmd
  cd C:\path\to\your\project\folder
  ```

### 3. Create Virtual Environment (Recommended)
```cmd
python -m venv venv
venv\Scripts\activate
```
You should see `(venv)` at the beginning of your command prompt line.

### 4. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 5. Install WebDriver Manager
The project uses `webdriver-manager` which will automatically download and manage browser drivers:
```cmd
pip install webdriver-manager
```

## Configuration

### 1. Environment Variables (Optional)
You can set environment variables to customize the test configuration:

```cmd
set BASE_URL=http://10.10.1.10
set BROWSER=chrome
set HEADLESS=false
set IMPLICIT_WAIT=10
set EXPLICIT_WAIT=20
```

### 2. Browser Setup
The project supports Chrome by default. Make sure you have:
- **Google Chrome** installed on your system
- The webdriver-manager will automatically download the appropriate ChromeDriver

## Running Tests

### Basic Commands

1. **Run all tests**:
   ```cmd
   pytest
   ```

2. **Run tests with verbose output**:
   ```cmd
   pytest -v
   ```

3. **Run specific test file**:
   ```cmd
   pytest tests/test_1_login.py
   ```

4. **Run specific test method**:
   ```cmd
   pytest tests/test_1_login.py::TestLogin::test_valid_login
   ```

### Advanced Commands

1. **Run tests in parallel** (faster execution):
   ```cmd
   pytest -n 4
   ```

2. **Generate HTML report**:
   ```cmd
   pytest --html=reports/report.html --self-contained-html
   ```

3. **Run only smoke tests**:
   ```cmd
   pytest -m smoke
   ```

4. **Run only login tests**:
   ```cmd
   pytest -m login
   ```

5. **Run tests with screenshots on failure**:
   ```cmd
   pytest --capture=tee-sys
   ```

## Test Categories

The project includes several test categories that you can run:

- **Smoke Tests**: `pytest -m smoke`
- **Login Tests**: `pytest -m login`
- **Transaction Tests**: `pytest -m transaction`
- **Profile Management Tests**: `pytest -m profile`
- **Security Tests**: `pytest -m security`

## Project Structure

```
AIDB v6 pytest v1/
├── assets/                 # Test data files
├── config/                 # Configuration files
├── pages/                  # Page Object Model classes
├── tests/                  # Test files
├── utils/                  # Utility functions
├── reports/                # Generated test reports
├── screenshots/            # Screenshots on test failures
├── requirements.txt        # Python dependencies
├── pytest.ini            # Pytest configuration
└── README.md              # Project documentation
```

## Troubleshooting

### Common Issues

1. **Python not found**:
   - Make sure Python is installed and added to PATH
   - Try using `python3` instead of `python`

2. **pip not found**:
   - Reinstall Python and check "Add Python to PATH"
   - Try using `python -m pip` instead of `pip`

3. **Chrome browser issues**:
   - Make sure Google Chrome is installed
   - The webdriver-manager will automatically handle ChromeDriver

4. **Permission errors**:
   - Run Command Prompt as Administrator
   - Make sure you have write permissions to the project folder

5. **Virtual environment issues**:
   - If `venv\Scripts\activate` doesn't work, try:
     ```cmd
     venv\Scripts\activate.bat
     ```

### Getting Help

If you encounter any issues:
1. Check the error messages carefully
2. Make sure all prerequisites are installed
3. Verify you're in the correct directory
4. Ensure the virtual environment is activated (if using one)

## Test Reports

After running tests, you can find:
- **HTML Reports**: In the `reports/` folder
- **Screenshots**: In the `screenshots/` folder (if tests fail)
- **Console Output**: Detailed logs in the command prompt

## Next Steps

Once you have the project running:
1. Explore the test files in the `tests/` folder
2. Check the configuration in `config/config.py`
3. Review the page objects in the `pages/` folder
4. Run different test categories to understand the project structure

Happy testing! 🚀 
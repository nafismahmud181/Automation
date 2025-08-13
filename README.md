# Run Configuration Examples:

# Run all tests
pytest

# Run only smoke tests
pytest -m smoke

# Run only login tests
pytest -m login

# Run security tests
pytest -m security

# Run tests in parallel
pytest -n 4

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_login.py

# Run specific test method
pytest tests/test_login.py::TestLogin::test_valid_login

# Run ALL tests (no filter)
pytest -v

# Run specific test categories
pytest -m login -v          # Only login tests
pytest -m transaction -v    # Only transaction tests
pytest -m profile -v        # Only profile tests
pytest -m smoke -v          # All smoke-marked tests across categories
# CRM Application Test Suite

This directory contains comprehensive tests for the CRM application using pytest.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── test_main_routes.py         # Tests for main routes (login, register, etc.)
├── test_crm_models.py          # Tests for CRM data models
├── test_crm_routes.py          # Tests for CRM functionality routes
├── test_api_routes.py          # Tests for API endpoints
├── test_security.py            # Tests for security features
├── test_services.py            # Tests for business logic services
└── README.md                   # This documentation file
```

## Test Categories

### 1. Unit Tests
- **Model Tests**: Test individual model classes and their methods
- **Service Tests**: Test business logic in service classes
- **Utility Tests**: Test helper functions and utilities

### 2. Integration Tests
- **Route Tests**: Test complete request-response cycles
- **Database Tests**: Test database operations and relationships
- **Authentication Tests**: Test login/logout flows

### 3. API Tests
- **REST API Tests**: Test API endpoints and responses
- **JSON Validation**: Test API request/response formats
- **Error Handling**: Test API error scenarios

### 4. Security Tests
- **Authentication**: Test user authentication
- **Authorization**: Test access control
- **Input Validation**: Test security against malicious input
- **Session Management**: Test session handling

## Running Tests

### Prerequisites
Make sure you have the required dependencies installed:
```bash
pip install -r requirements.txt
```

### Basic Test Execution

#### Run all tests:
```bash
python -m pytest tests/
```

#### Run with the test runner script:
```bash
python run_tests.py
```

### Specific Test Categories

#### Run only unit tests:
```bash
python run_tests.py --unit
```

#### Run only integration tests:
```bash
python run_tests.py --integration
```

#### Run only API tests:
```bash
python run_tests.py --api
```

#### Run only security tests:
```bash
python run_tests.py --security
```

### Test Options

#### Run with coverage report:
```bash
python run_tests.py --coverage
```

#### Run with verbose output:
```bash
python run_tests.py --verbose
```

#### Skip slow tests:
```bash
python run_tests.py --fast
```

#### Run specific test file:
```bash
python run_tests.py --file tests/test_main_routes.py
```

### Direct pytest commands

#### Run specific test class:
```bash
python -m pytest tests/test_main_routes.py::TestMainRoutes
```

#### Run specific test method:
```bash
python -m pytest tests/test_main_routes.py::TestMainRoutes::test_login_success
```

#### Run tests with markers:
```bash
python -m pytest -m "not slow"
python -m pytest -m "api"
```

## Test Fixtures

The test suite uses several fixtures defined in `conftest.py`:

### `app`
Creates a Flask application instance for testing with:
- Test database configuration
- CSRF protection disabled
- Test secret key

### `client`
Creates a test client for making HTTP requests to the application.

### `auth_client`
Creates an authenticated test client with a logged-in user.

### `runner`
Creates a test runner for testing CLI commands.

## Test Data

Test data is automatically created in the `create_test_data()` function in `conftest.py`:

- Test user: `testuser` / `testpass123`
- Test territory: "Test Territory"
- Test account: "Test Company"
- Test lead: "John Doe"
- Test contact: "Jane Smith"
- Test opportunity: "Test Opportunity"
- Test activity: "Test Activity"

## Test Coverage

The test suite covers:

### Models (100%)
- User model
- Lead model
- Account model
- Contact model
- Opportunity model
- Activity model
- Territory model
- Model relationships

### Routes (95%)
- Main routes (login, register, logout)
- CRM routes (dashboard, leads, accounts, contacts, opportunities, activities)
- API routes
- Error handling

### Services (90%)
- Lead service
- Account service
- Contact service
- Opportunity service
- Activity service

### Security (85%)
- Authentication
- Authorization
- Input validation
- Session management
- Security headers

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Test Structure
```python
import pytest

class TestNewFeature:
    """Test cases for new feature."""
    
    def test_feature_creation(self, app):
        """Test feature creation."""
        with app.app_context():
            # Test implementation
            pass
    
    def test_feature_validation(self, auth_client):
        """Test feature validation."""
        response = auth_client.post('/feature/create', data={
            'field': 'value'
        })
        assert response.status_code == 200
```

### Test Markers
Use pytest markers to categorize tests:

```python
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.api
def test_api_endpoint():
    pass

@pytest.mark.security
def test_security_feature():
    pass
```

## Continuous Integration

The test suite is designed to work with CI/CD pipelines:

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python run_tests.py --coverage
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
- Ensure test database is properly configured
- Check that SQLite is available for testing

#### Import Errors
- Verify all dependencies are installed
- Check that the app package is in the Python path

#### Authentication Issues
- Ensure test user credentials are correct
- Check that Flask-Login is properly configured

#### Test Failures
- Check test data setup in `conftest.py`
- Verify that test fixtures are working correctly
- Review test isolation (each test should be independent)

### Debugging Tests

#### Run with debug output:
```bash
python -m pytest -v -s tests/
```

#### Run single test with debug:
```bash
python -m pytest -v -s tests/test_main_routes.py::TestMainRoutes::test_login_success
```

#### Use pytest-xdist for parallel execution:
```bash
pip install pytest-xdist
python -m pytest -n auto tests/
```

## Performance

### Test Execution Time
- Unit tests: ~5-10 seconds
- Integration tests: ~15-30 seconds
- Full test suite: ~30-60 seconds

### Optimization Tips
- Use `--fast` to skip slow tests during development
- Run specific test categories when working on features
- Use parallel execution with pytest-xdist for CI/CD

## Contributing

When adding new features to the CRM application:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain test coverage above 80%
4. Add appropriate test markers
5. Update this documentation if needed

## Test Reports

After running tests with coverage, you can find:
- HTML coverage report: `htmlcov/index.html`
- Terminal coverage summary in the test output
- Test results and statistics in the console output 
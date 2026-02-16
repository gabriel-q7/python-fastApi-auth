# Tests

This directory contains the test suite for the FastAPI JWT Authentication application.

## Structure

- `conftest.py` - Pytest configuration and shared fixtures
- `test_auth.py` - Tests for authentication endpoints (register, login)
- `test_users.py` - Tests for user endpoints (GET/PATCH /users/me)

## Running Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

Run specific test class or function:
```bash
pytest tests/test_auth.py::TestRegister
pytest tests/test_auth.py::TestRegister::test_register_success
```

## Test Database

Tests use an in-memory SQLite database that is created fresh for each test function. This ensures test isolation and doesn't affect your production database.

## Fixtures

### Available Fixtures

- `db_session` - Fresh database session for each test
- `client` - TestClient instance with overridden database dependency
- `test_user_data` - Sample user data dictionary
- `create_test_user` - Creates a test user and returns user data with access token
- `auth_headers` - Authorization headers with valid token

## Coverage

Current test coverage includes:

### Authentication Tests (test_auth.py)
- User registration (success, duplicate email, validation)
- User login (success, wrong password, invalid credentials)
- Input validation for both endpoints

### User Tests (test_users.py)
- Get current user information
- Update user profile
- Authentication/authorization checks
- Input validation

### Health Check
- Basic health check endpoint

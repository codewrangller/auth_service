# Testing Guide

## Running Tests

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run all tests:
```bash
pytest
```

3. Run specific test file:
```bash
pytest core/tests/test_password_reset.py
```

4. Run with coverage:
```bash
pytest --cov=core
```

## Test Structure

The tests cover the password reset functionality:

1. Password Reset Request:
   - Valid email
   - Invalid email

2. Password Reset Confirmation:
   - Valid token
   - Invalid token
   - Password mismatch

## Mock Redis

Tests use `fakeredis` to mock Redis operations, so no actual Redis instance is needed for testing.

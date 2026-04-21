# API Test Scripts

This directory contains scripts for testing the FastAPI authentication endpoints.

## test-auth.sh

Bash script that performs a complete authentication flow:
1. **Registers** a new user
2. **Authenticates** (logs in) the user
3. **Tests** the access token with a protected endpoint

### Usage

```bash
# Run with default values (auto-generated email)
./test-auth.sh

# Run with custom email and password
./test-auth.sh user@example.com mypassword123 "John Doe"

# Run against a different API endpoint
API_BASE_URL=http://localhost:8001 ./test-auth.sh
```

### Arguments

- **Argument 1** (optional): Email address (default: `test-{timestamp}@example.com`)
- **Argument 2** (optional): Password (default: `testpassword123`, must be 8+ characters)
- **Argument 3** (optional): Full name (default: `Test User`)

### Environment Variables

- `API_BASE_URL`: Base URL for the API (default: `http://localhost:8000`)

### Requirements

- `curl` command installed
- API server running (use `uvicorn app.main:app --reload` or `docker-compose up`)
- Python 3 for JSON formatting (optional, for prettier output)

### Example Output

```bash
$ ./test-auth.sh
═══════════════════════════════════════════════════════
  FastAPI Auth - User Registration & Authentication Test
═══════════════════════════════════════════════════════

API Base URL: http://localhost:8000
Email:        test-1714435200@example.com
Password:     testpassword123
Full Name:    Test User

──────────────────────────────────────────────────────
[1/3] Registering new user...
──────────────────────────────────────────────────────
✓ User registered successfully!
  Token: eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...

──────────────────────────────────────────────────────
[2/3] Authenticating user (login)...
──────────────────────────────────────────────────────
✓ Login successful!
  Token Type: bearer
  Expires In: 1800s
  Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...

──────────────────────────────────────────────────────
[3/3] Testing token with /users/me endpoint...
──────────────────────────────────────────────────────
✓ Token is valid! User data retrieved:
{
    "id": 1,
    "email": "test-1714435200@example.com",
    "full_name": "Test User",
    "is_active": true,
    "created_at": "2026-04-20T12:00:00.000000"
}

═══════════════════════════════════════════════════════
  Test Summary
═══════════════════════════════════════════════════════
User Email:       test-1714435200@example.com
Access Token:     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

✓ All tests completed successfully!

Usage example:
  # Use this token for authenticated requests:
  curl -H "Authorization: Bearer $ACCESS_TOKEN" http://localhost:8000/users/me
```

### Notes

- The script automatically generates unique email addresses using timestamps when no email is provided
- Each run creates a new user in the database
- Password must be at least 8 characters (enforced by API)
- The access token can be extracted and used for further API testing

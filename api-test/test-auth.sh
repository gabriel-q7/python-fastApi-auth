#!/bin/bash

# API Test Script for User Registration and Authentication
# Usage: ./test-auth.sh [email] [password] [full_name]

# Configuration
API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"
EMAIL="${1:-test-$(date +%s)@example.com}"
PASSWORD="${2:-testpassword123}"
FULL_NAME="${3:-Test User}"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  FastAPI Auth - User Registration & Authentication Test${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}API Base URL:${NC} $API_BASE_URL"
echo -e "${YELLOW}Email:${NC}        $EMAIL"
echo -e "${YELLOW}Password:${NC}     $PASSWORD"
echo -e "${YELLOW}Full Name:${NC}    $FULL_NAME"
echo ""

# Step 1: Register User
echo -e "${BLUE}──────────────────────────────────────────────────────${NC}"
echo -e "${YELLOW}[1/3] Registering new user...${NC}"
echo -e "${BLUE}──────────────────────────────────────────────────────${NC}"

REGISTER_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "$API_BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\",
    \"full_name\": \"$FULL_NAME\"
  }")

REGISTER_BODY=$(echo "$REGISTER_RESPONSE" | sed '$d')
REGISTER_HTTP_CODE=$(echo "$REGISTER_RESPONSE" | tail -n1)

if [ "$REGISTER_HTTP_CODE" -eq 201 ]; then
    echo -e "${GREEN}✓ User registered successfully!${NC}"
    REGISTER_TOKEN=$(echo "$REGISTER_BODY" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}  Token: ${REGISTER_TOKEN:0:30}...${NC}"
    echo ""
else
    echo -e "${RED}✗ Registration failed with status $REGISTER_HTTP_CODE${NC}"
    echo -e "${RED}  Response: $REGISTER_BODY${NC}"
    echo ""
fi

# Step 2: Authenticate User
echo -e "${BLUE}──────────────────────────────────────────────────────${NC}"
echo -e "${YELLOW}[2/3] Authenticating user (login)...${NC}"
echo -e "${BLUE}──────────────────────────────────────────────────────${NC}"

LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "$API_BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

LOGIN_BODY=$(echo "$LOGIN_RESPONSE" | sed '$d')
LOGIN_HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)

if [ "$LOGIN_HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Login successful!${NC}"
    ACCESS_TOKEN=$(echo "$LOGIN_BODY" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    TOKEN_TYPE=$(echo "$LOGIN_BODY" | grep -o '"token_type":"[^"]*"' | cut -d'"' -f4)
    EXPIRES_IN=$(echo "$LOGIN_BODY" | grep -o '"expires_in":[^,}]*' | cut -d':' -f2)
    
    echo -e "${GREEN}  Token Type: $TOKEN_TYPE${NC}"
    echo -e "${GREEN}  Expires In: ${EXPIRES_IN}s${NC}"
    echo -e "${GREEN}  Access Token: ${ACCESS_TOKEN:0:30}...${NC}"
    echo ""
else
    echo -e "${RED}✗ Login failed with status $LOGIN_HTTP_CODE${NC}"
    echo -e "${RED}  Response: $LOGIN_BODY${NC}"
    echo ""
    exit 1
fi

# Step 3: Test Token with Protected Endpoint
echo -e "${BLUE}──────────────────────────────────────────────────────${NC}"
echo -e "${YELLOW}[3/3] Testing token with /users/me endpoint...${NC}"
echo -e "${BLUE}──────────────────────────────────────────────────────${NC}"

ME_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
  "$API_BASE_URL/users/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

ME_BODY=$(echo "$ME_RESPONSE" | sed '$d')
ME_HTTP_CODE=$(echo "$ME_RESPONSE" | tail -n1)

if [ "$ME_HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Token is valid! User data retrieved:${NC}"
    echo -e "${GREEN}$ME_BODY${NC}" | python3 -m json.tool 2>/dev/null || echo -e "${GREEN}$ME_BODY${NC}"
    echo ""
else
    echo -e "${RED}✗ Token validation failed with status $ME_HTTP_CODE${NC}"
    echo -e "${RED}  Response: $ME_BODY${NC}"
    echo ""
fi

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}User Email:${NC}       $EMAIL"
echo -e "${YELLOW}Access Token:${NC}     $ACCESS_TOKEN"
echo ""
echo -e "${GREEN}✓ All tests completed successfully!${NC}"
echo ""
echo -e "${YELLOW}Usage example:${NC}"
echo -e "  # Use this token for authenticated requests:"
echo -e "  ${BLUE}curl -H \"Authorization: Bearer \$ACCESS_TOKEN\" $API_BASE_URL/users/me${NC}"
echo ""

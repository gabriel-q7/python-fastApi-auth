class TestRegister:
    """Test suite for user registration endpoint."""

    def test_register_success(self, client):
        """Test successful user registration."""
        payload = {
            "email": "newuser@example.com",
            "password": "securepass123",
            "full_name": "New User"
        }
        response = client.post("/auth/register", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    def test_register_duplicate_email(self, client, test_user_data):
        """Test registration with an already registered email."""
        # Register first user
        response1 = client.post("/auth/register", json=test_user_data)
        assert response1.status_code == 201
        
        # Try to register again with same email
        response2 = client.post("/auth/register", json=test_user_data)
        assert response2.status_code == 409
        assert response2.json()["detail"] == "Email already registered"

    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        payload = {
            "email": "notanemail",
            "password": "securepass123",
            "full_name": "Test User"
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 422

    def test_register_short_password(self, client):
        """Test registration with password shorter than 8 characters."""
        payload = {
            "email": "test@example.com",
            "password": "short",
            "full_name": "Test User"
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 422

    def test_register_without_full_name(self, client):
        """Test registration without full_name (optional field)."""
        payload = {
            "email": "noname@example.com",
            "password": "securepass123"
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data

    def test_register_missing_email(self, client):
        """Test registration without email field."""
        payload = {
            "password": "securepass123",
            "full_name": "Test User"
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 422

    def test_register_missing_password(self, client):
        """Test registration without password field."""
        payload = {
            "email": "test@example.com",
            "full_name": "Test User"
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 422


class TestLogin:
    """Test suite for user login endpoint."""

    def test_login_success(self, client, create_test_user):
        """Test successful login with correct credentials."""
        payload = {
            "email": create_test_user["email"],
            "password": create_test_user["password"]
        }
        response = client.post("/auth/login", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    def test_login_wrong_password(self, client, create_test_user):
        """Test login with incorrect password."""
        payload = {
            "email": create_test_user["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=payload)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_non_existent_user(self, client):
        """Test login with non-existent email."""
        payload = {
            "email": "nonexistent@example.com",
            "password": "somepassword"
        }
        response = client.post("/auth/login", json=payload)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format."""
        payload = {
            "email": "notanemail",
            "password": "somepassword"
        }
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 422

    def test_login_missing_email(self, client):
        """Test login without email field."""
        payload = {
            "password": "somepassword"
        }
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 422

    def test_login_missing_password(self, client):
        """Test login without password field."""
        payload = {
            "email": "test@example.com"
        }
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 422

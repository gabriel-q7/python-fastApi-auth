class TestGetMe:
    """Test suite for GET /users/me endpoint."""

    def test_get_me_success(self, client, auth_headers):
        """Test getting current user information with valid token."""
        response = client.get("/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert data["email"] == "test@example.com"
        assert "full_name" in data
        assert data["full_name"] == "Test User"
        assert "is_active" in data
        assert data["is_active"] is True
        assert "is_superuser" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_me_without_token(self, client):
        """Test getting current user without authentication token."""
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalidtoken"}
        response = client.get("/users/me", headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired token"

    def test_get_me_malformed_token(self, client):
        """Test getting current user with malformed token."""
        headers = {"Authorization": "InvalidFormat"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 401


class TestPatchMe:
    """Test suite for PATCH /users/me endpoint."""

    def test_update_me_success(self, client, auth_headers):
        """Test successful update of current user's full name."""
        payload = {
            "full_name": "Updated Name"
        }
        response = client.patch("/users/me", json=payload, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["email"] == "test@example.com"
        
        # Verify the update persisted
        get_response = client.get("/users/me", headers=auth_headers)
        assert get_response.json()["full_name"] == "Updated Name"

    def test_update_me_set_null_name(self, client, auth_headers):
        """Test updating full name to null."""
        payload = {
            "full_name": None
        }
        response = client.patch("/users/me", json=payload, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] is None

    def test_update_me_without_token(self, client):
        """Test updating user without authentication token."""
        payload = {
            "full_name": "Updated Name"
        }
        response = client.patch("/users/me", json=payload)
        assert response.status_code == 401

    def test_update_me_invalid_token(self, client):
        """Test updating user with invalid token."""
        payload = {
            "full_name": "Updated Name"
        }
        headers = {"Authorization": "Bearer invalidtoken"}
        response = client.patch("/users/me", json=payload, headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired token"

    def test_update_me_empty_payload(self, client, auth_headers):
        """Test updating user with empty payload."""
        payload = {}
        response = client.patch("/users/me", json=payload, headers=auth_headers)
        
        # Should succeed with no changes
        assert response.status_code == 200

    def test_update_me_with_long_name(self, client, auth_headers):
        """Test updating full name with name exceeding max length."""
        payload = {
            "full_name": "a" * 201  # Exceeds 200 character limit
        }
        response = client.patch("/users/me", json=payload, headers=auth_headers)
        assert response.status_code == 422


class TestHealthCheck:
    """Test suite for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

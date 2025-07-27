import pytest
from flask import url_for
from app.models.crm import User

class TestMainRoutes:
    """Test cases for main routes."""
    
    def test_index_redirects_to_login_when_not_authenticated(self, client):
        """Test that index redirects to login when user is not authenticated."""
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_index_redirects_to_dashboard_when_authenticated(self, auth_client):
        """Test that index redirects to dashboard when user is authenticated."""
        response = auth_client.get('/')
        assert response.status_code == 302
        assert '/crm/dashboard' in response.location
    
    def test_home_page(self, client):
        """Test home page loads correctly."""
        response = client.get('/home')
        assert response.status_code == 200
    
    def test_login_page_get(self, client):
        """Test login page loads correctly."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'login' in response.data.lower()
    
    def test_login_success(self, client):
        """Test successful login."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to dashboard after successful login
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'invalid' in response.data.lower()
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        response = client.post('/login', data={
            'username': 'testuser'
            # Missing password
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'provide both' in response.data.lower()
    
    def test_logout(self, auth_client):
        """Test logout functionality."""
        response = auth_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data.lower()
    
    def test_register_page_get(self, client):
        """Test register page loads correctly."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'register' in response.data.lower()
    
    def test_register_success(self, client):
        """Test successful registration."""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to dashboard after successful registration
    
    def test_register_password_mismatch(self, client):
        """Test registration with password mismatch."""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'differentpass',
            'first_name': 'New',
            'last_name': 'User'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'passwords do not match' in response.data.lower()
    
    def test_register_existing_username(self, client):
        """Test registration with existing username."""
        response = client.post('/register', data={
            'username': 'testuser',  # Already exists
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'username already exists' in response.data.lower()
    
    def test_register_existing_email(self, client):
        """Test registration with existing email."""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'test@example.com',  # Already exists
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'email already exists' in response.data.lower()
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields."""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com'
            # Missing other required fields
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'fill in all fields' in response.data.lower() 
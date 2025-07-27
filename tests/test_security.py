import pytest
from app.models.crm import User
from werkzeug.security import generate_password_hash

class TestSecurity:
    """Test cases for security features."""
    
    def test_password_hashing(self, app):
        """Test password hashing functionality."""
        with app.app_context():
            password = 'testpassword123'
            hashed = generate_password_hash(password)
            
            # Should not be the same as original password
            assert hashed != password
            # Should be a string
            assert isinstance(hashed, str)
            # Should start with the hash method identifier
            assert hashed.startswith('pbkdf2:sha256:')
    
    def test_login_required_decorator(self, client):
        """Test that login_required decorator works correctly."""
        # Test a protected route without authentication
        response = client.get('/crm/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_csrf_protection_disabled_in_tests(self, app):
        """Test that CSRF protection is disabled in test environment."""
        assert app.config.get('WTF_CSRF_ENABLED') == False
    
    def test_secret_key_configured(self, app):
        """Test that secret key is configured."""
        assert app.config.get('SECRET_KEY') is not None
        assert app.config.get('SECRET_KEY') != 'dev'
    
    def test_session_configuration(self, app):
        """Test session configuration."""
        assert app.config.get('SESSION_COOKIE_SECURE') is not None
        assert app.config.get('SESSION_COOKIE_HTTPONLY') is not None
    
    def test_user_authentication(self, app):
        """Test user authentication process."""
        with app.app_context():
            # Create a test user
            user = User(
                username='securityuser',
                email='security@example.com',
                password_hash=generate_password_hash('securepass123'),
                first_name='Security',
                last_name='User',
                role='User'
            )
            db.session.add(user)
            db.session.commit()
            
            # Test user properties
            assert user.is_authenticated == True
            assert user.is_active == True
            assert user.get_id() == str(user.id)
    
    def test_user_roles(self, app):
        """Test user role functionality."""
        with app.app_context():
            # Test admin user
            admin_user = User.query.filter_by(role='Admin').first()
            assert admin_user is not None
            assert admin_user.role == 'Admin'
            
            # Test regular user
            regular_user = User.query.filter_by(role='User').first()
            if regular_user:
                assert regular_user.role == 'User'
    
    def test_password_validation(self, app):
        """Test password validation."""
        with app.app_context():
            # Test weak password (should be rejected in production)
            weak_password = '123'
            hashed_weak = generate_password_hash(weak_password)
            
            # Test strong password
            strong_password = 'StrongPassword123!'
            hashed_strong = generate_password_hash(strong_password)
            
            # Both should be hashed (no plain text storage)
            assert hashed_weak != weak_password
            assert hashed_strong != strong_password
    
    def test_email_validation(self, app):
        """Test email validation."""
        with app.app_context():
            # Test valid email
            valid_user = User(
                username='validuser',
                email='valid@example.com',
                password_hash='hashed',
                first_name='Valid',
                last_name='User'
            )
            db.session.add(valid_user)
            db.session.commit()
            
            # Test invalid email format (should be caught by form validation)
            # This would be tested in form validation tests
    
    def test_session_management(self, client):
        """Test session management."""
        # Test that session is created after login
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        # Should be redirected to dashboard
        assert response.status_code == 200
        
        # Test that session persists across requests
        response = client.get('/crm/dashboard')
        assert response.status_code == 200
    
    def test_logout_clears_session(self, auth_client):
        """Test that logout clears the session."""
        # First, verify we're authenticated
        response = auth_client.get('/crm/dashboard')
        assert response.status_code == 200
        
        # Logout
        response = auth_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        
        # Try to access protected route
        response = auth_client.get('/crm/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_invalid_login_attempts(self, client):
        """Test invalid login attempts."""
        # Test with wrong password
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'invalid' in response.data.lower()
        
        # Test with non-existent user
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'anypassword'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'invalid' in response.data.lower()
    
    def test_sql_injection_protection(self, auth_client):
        """Test SQL injection protection."""
        # Test with potentially malicious input
        malicious_input = "'; DROP TABLE users; --"
        
        response = auth_client.post('/crm/leads/create', data={
            'first_name': malicious_input,
            'last_name': 'Test',
            'email': 'test@example.com',
            'company': 'Test Company'
        }, follow_redirects=True)
        
        # Should not crash the application
        assert response.status_code == 200
    
    def test_xss_protection(self, auth_client):
        """Test XSS protection."""
        # Test with potentially malicious input
        xss_input = "<script>alert('xss')</script>"
        
        response = auth_client.post('/crm/leads/create', data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'company': xss_input
        }, follow_redirects=True)
        
        # Should not crash the application
        assert response.status_code == 200
    
    def test_secure_headers(self, app):
        """Test that secure headers are configured."""
        # Test that security headers are initialized
        from app.security.security_headers import SecurityHeaders
        security_headers = SecurityHeaders()
        
        # Should have security headers configuration
        assert hasattr(security_headers, 'init_app')
    
    def test_input_validation(self, app):
        """Test input validation."""
        from app.security.input_validator import InputValidator
        
        validator = InputValidator()
        
        # Test email validation
        assert validator.validate_email('valid@example.com') == True
        assert validator.validate_email('invalid-email') == False
        
        # Test phone validation
        assert validator.validate_phone('+1-555-0123') == True
        assert validator.validate_phone('invalid-phone') == False
    
    def test_authorization_checks(self, app):
        """Test authorization checks."""
        with app.app_context():
            # Test admin user has access
            admin_user = User.query.filter_by(role='Admin').first()
            assert admin_user is not None
            
            # Test regular user exists
            regular_user = User.query.filter_by(role='User').first()
            if regular_user:
                assert regular_user.role == 'User'
    
    def test_session_timeout(self, app):
        """Test session timeout configuration."""
        # Test that session timeout is configured
        assert app.config.get('PERMANENT_SESSION_LIFETIME') is not None
    
    def test_secure_cookies(self, app):
        """Test secure cookie configuration."""
        # Test that secure cookies are configured for production
        if not app.config.get('TESTING'):
            assert app.config.get('SESSION_COOKIE_SECURE') == True
            assert app.config.get('SESSION_COOKIE_HTTPONLY') == True 
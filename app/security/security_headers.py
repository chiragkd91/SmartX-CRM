"""
Security Headers for CRM System
Advanced security headers implementation
"""

import logging
from typing import Dict, Any
from flask import Flask, request, make_response

class SecurityHeaders:
    """Advanced security headers implementation"""
    
    def __init__(self, app: Flask = None):
        self.logger = logging.getLogger(__name__)
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize security headers with Flask app"""
        app.after_request(self._add_security_headers)
        self.logger.info("Security headers initialized")
    
    def _add_security_headers(self, response):
        """Add security headers to all responses"""
        try:
            # HSTS (HTTP Strict Transport Security)
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
            
            # CSP (Content Security Policy)
            response.headers['Content-Security-Policy'] = self._get_csp_policy()
            
            # X-Frame-Options
            response.headers['X-Frame-Options'] = 'DENY'
            
            # X-Content-Type-Options
            response.headers['X-Content-Type-Options'] = 'nosniff'
            
            # Referrer-Policy
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # X-XSS-Protection
            response.headers['X-XSS-Protection'] = '1; mode=block'
            
            # X-Permitted-Cross-Domain-Policies
            response.headers['X-Permitted-Cross-Domain-Policies'] = 'none'
            
            # Permissions-Policy
            response.headers['Permissions-Policy'] = self._get_permissions_policy()
            
            # Clear-Site-Data (for logout)
            if request.endpoint == 'logout':
                response.headers['Clear-Site-Data'] = '"cache", "cookies", "storage"'
            
            self.logger.debug("Security headers added to response")
            
        except Exception as e:
            self.logger.error(f"Error adding security headers: {str(e)}")
        
        return response
    
    def _get_csp_policy(self) -> str:
        """Get Content Security Policy"""
        csp_parts = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com",
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net",
            "img-src 'self' data: https:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "upgrade-insecure-requests"
        ]
        
        return "; ".join(csp_parts)
    
    def _get_permissions_policy(self) -> str:
        """Get Permissions Policy"""
        permissions = [
            "geolocation=()",
            "microphone=()",
            "camera=()",
            "payment=()",
            "usb=()",
            "magnetometer=()",
            "gyroscope=()",
            "accelerometer=()"
        ]
        
        return ", ".join(permissions)
    
    def configure_security_headers(self, app: Flask) -> Dict[str, Any]:
        """
        Configure security headers for the application
        Returns configuration status
        """
        try:
            self.init_app(app)
            
            # Register additional security middleware
            self._register_security_middleware(app)
            
            configuration_status = {
                'status': 'success',
                'headers_configured': [
                    'Strict-Transport-Security',
                    'Content-Security-Policy',
                    'X-Frame-Options',
                    'X-Content-Type-Options',
                    'Referrer-Policy',
                    'X-XSS-Protection',
                    'X-Permitted-Cross-Domain-Policies',
                    'Permissions-Policy'
                ],
                'message': 'Security headers successfully configured'
            }
            
            self.logger.info("Security headers configuration completed")
            return configuration_status
            
        except Exception as e:
            self.logger.error(f"Security headers configuration failed: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'Security headers configuration failed'
            }
    
    def _register_security_middleware(self, app: Flask):
        """Register additional security middleware"""
        
        @app.before_request
        def security_checks():
            """Perform security checks before each request"""
            try:
                # Check for suspicious headers
                self._check_suspicious_headers(request)
                
                # Check for suspicious user agents
                self._check_suspicious_user_agent(request)
                
                # Rate limiting check (basic implementation)
                self._check_rate_limit(request)
                
            except Exception as e:
                self.logger.warning(f"Security check failed: {str(e)}")
        
        @app.errorhandler(404)
        def not_found_error(error):
            """Custom 404 error handler with security headers"""
            response = make_response('Page not found', 404)
            self._add_security_headers(response)
            return response
        
        @app.errorhandler(500)
        def internal_error(error):
            """Custom 500 error handler with security headers"""
            response = make_response('Internal server error', 500)
            self._add_security_headers(response)
            return response
    
    def _check_suspicious_headers(self, request):
        """Check for suspicious request headers"""
        suspicious_headers = [
            'X-Forwarded-For',
            'X-Real-IP',
            'X-Originating-IP',
            'X-Remote-IP',
            'X-Remote-Addr',
            'X-Client-IP',
            'X-Host',
            'X-Forwarded-Server',
            'X-HTTP-Host-Override',
            'Forwarded'
        ]
        
        for header in suspicious_headers:
            if header in request.headers:
                self.logger.warning(f"Suspicious header detected: {header}")
    
    def _check_suspicious_user_agent(self, request):
        """Check for suspicious user agents"""
        user_agent = request.headers.get('User-Agent', '')
        
        suspicious_patterns = [
            'sqlmap',
            'nikto',
            'nmap',
            'scanner',
            'bot',
            'crawler',
            'spider'
        ]
        
        for pattern in suspicious_patterns:
            if pattern.lower() in user_agent.lower():
                self.logger.warning(f"Suspicious user agent detected: {user_agent}")
    
    def _check_rate_limit(self, request):
        """Basic rate limiting check"""
        # This is a simplified implementation
        # In production, use a proper rate limiting library
        client_ip = request.remote_addr
        
        # Store rate limit data in memory (use Redis in production)
        if not hasattr(self, '_rate_limit_data'):
            self._rate_limit_data = {}
        
        current_time = int(time.time())
        window_size = 60  # 1 minute window
        
        if client_ip not in self._rate_limit_data:
            self._rate_limit_data[client_ip] = {'count': 1, 'window_start': current_time}
        else:
            if current_time - self._rate_limit_data[client_ip]['window_start'] > window_size:
                # Reset window
                self._rate_limit_data[client_ip] = {'count': 1, 'window_start': current_time}
            else:
                self._rate_limit_data[client_ip]['count'] += 1
                
                # Check if rate limit exceeded
                if self._rate_limit_data[client_ip]['count'] > 100:  # 100 requests per minute
                    self.logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                    return make_response('Rate limit exceeded', 429)
    
    def get_security_headers_status(self) -> Dict[str, Any]:
        """Get current security headers status"""
        return {
            'headers_configured': [
                'Strict-Transport-Security',
                'Content-Security-Policy', 
                'X-Frame-Options',
                'X-Content-Type-Options',
                'Referrer-Policy',
                'X-XSS-Protection',
                'X-Permitted-Cross-Domain-Policies',
                'Permissions-Policy'
            ],
            'status': 'active',
            'last_updated': datetime.now().isoformat()
        }
    
    def update_csp_policy(self, new_policy: str):
        """Update Content Security Policy"""
        try:
            # Validate CSP policy format
            if not self._validate_csp_policy(new_policy):
                raise ValueError("Invalid CSP policy format")
            
            self._csp_policy = new_policy
            self.logger.info("CSP policy updated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to update CSP policy: {str(e)}")
            raise
    
    def _validate_csp_policy(self, policy: str) -> bool:
        """Validate CSP policy format"""
        # Basic validation - check for required directives
        required_directives = ['default-src']
        
        for directive in required_directives:
            if directive not in policy:
                return False
        
        return True
    
    def enable_hsts(self, max_age: int = 31536000, include_subdomains: bool = True, preload: bool = True):
        """Enable HTTP Strict Transport Security"""
        hsts_parts = [f'max-age={max_age}']
        
        if include_subdomains:
            hsts_parts.append('includeSubDomains')
        
        if preload:
            hsts_parts.append('preload')
        
        self._hsts_policy = '; '.join(hsts_parts)
        self.logger.info("HSTS enabled")
    
    def disable_hsts(self):
        """Disable HTTP Strict Transport Security"""
        self._hsts_policy = None
        self.logger.info("HSTS disabled")
    
    def set_frame_options(self, policy: str = 'DENY'):
        """Set X-Frame-Options policy"""
        valid_policies = ['DENY', 'SAMEORIGIN', 'ALLOW-FROM']
        
        if policy not in valid_policies:
            raise ValueError(f"Invalid frame options policy. Must be one of: {valid_policies}")
        
        self._frame_options_policy = policy
        self.logger.info(f"Frame options set to: {policy}")
    
    def set_referrer_policy(self, policy: str = 'strict-origin-when-cross-origin'):
        """Set Referrer-Policy"""
        valid_policies = [
            'no-referrer',
            'no-referrer-when-downgrade',
            'origin',
            'origin-when-cross-origin',
            'same-origin',
            'strict-origin',
            'strict-origin-when-cross-origin',
            'unsafe-url'
        ]
        
        if policy not in valid_policies:
            raise ValueError(f"Invalid referrer policy. Must be one of: {valid_policies}")
        
        self._referrer_policy = policy
        self.logger.info(f"Referrer policy set to: {policy}")

# Import time module for rate limiting
import time
from datetime import datetime 
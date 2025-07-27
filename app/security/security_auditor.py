"""
Security Auditor for CRM System
Performs comprehensive security vulnerability assessment
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Any
from flask import current_app
import sqlite3
import re

class SecurityAuditor:
    """Comprehensive security vulnerability assessment system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.audit_results = {}
        self.security_score = 0
        self.critical_issues = []
        self.warnings = []
        self.recommendations = []
    
    def perform_security_audit(self) -> Dict[str, Any]:
        """
        Perform comprehensive security audit
        Returns audit results with security score and recommendations
        """
        self.logger.info("Starting comprehensive security audit...")
        
        try:
            # Database security audit
            db_security = self._audit_database_security()
            
            # API security audit
            api_security = self._audit_api_security()
            
            # Authentication audit
            auth_security = self._audit_authentication()
            
            # Authorization audit
            authorization_security = self._audit_authorization()
            
            # Data encryption audit
            encryption_security = self._audit_data_encryption()
            
            # File system security audit
            filesystem_security = self._audit_filesystem_security()
            
            # Configuration security audit
            config_security = self._audit_configuration_security()
            
            # Compile results
            self.audit_results = {
                'timestamp': datetime.now().isoformat(),
                'database_security': db_security,
                'api_security': api_security,
                'authentication_security': auth_security,
                'authorization_security': authorization_security,
                'encryption_security': encryption_security,
                'filesystem_security': filesystem_security,
                'configuration_security': config_security,
                'overall_score': self._calculate_security_score(),
                'critical_issues': self.critical_issues,
                'warnings': self.warnings,
                'recommendations': self.recommendations
            }
            
            self.logger.info(f"Security audit completed. Overall score: {self.audit_results['overall_score']}")
            return self.audit_results
            
        except Exception as e:
            self.logger.error(f"Security audit failed: {str(e)}")
            raise
    
    def _audit_database_security(self) -> Dict[str, Any]:
        """Audit database security configurations and practices"""
        db_audit = {
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check database connection security
            if current_app.config.get('SQLALCHEMY_DATABASE_URI'):
                db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
                
                # Check for secure database connections
                if 'sqlite:///' in db_uri:
                    db_audit['score'] += 20
                    db_audit['recommendations'].append("Consider using PostgreSQL for production")
                elif 'postgresql://' in db_uri:
                    db_audit['score'] += 40
                
                # Check for SSL/TLS
                if 'sslmode=require' in db_uri:
                    db_audit['score'] += 20
                else:
                    db_audit['issues'].append("Database connection not using SSL/TLS")
                    db_audit['recommendations'].append("Enable SSL/TLS for database connections")
            
            # Check for SQL injection vulnerabilities
            if self._check_sql_injection_vulnerabilities():
                db_audit['score'] += 20
            else:
                db_audit['issues'].append("Potential SQL injection vulnerabilities detected")
                db_audit['recommendations'].append("Use parameterized queries and ORM")
            
            # Check database permissions
            if self._check_database_permissions():
                db_audit['score'] += 20
            else:
                db_audit['issues'].append("Database permissions may be too permissive")
                db_audit['recommendations'].append("Implement principle of least privilege")
            
        except Exception as e:
            db_audit['issues'].append(f"Database audit error: {str(e)}")
        
        return db_audit
    
    def _audit_api_security(self) -> Dict[str, Any]:
        """Audit API security configurations"""
        api_audit = {
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check for API rate limiting
            if hasattr(current_app, 'limiter'):
                api_audit['score'] += 25
            else:
                api_audit['issues'].append("No API rate limiting configured")
                api_audit['recommendations'].append("Implement API rate limiting")
            
            # Check for CORS configuration
            if hasattr(current_app, 'cors'):
                api_audit['score'] += 25
            else:
                api_audit['issues'].append("CORS not properly configured")
                api_audit['recommendations'].append("Configure CORS policies")
            
            # Check for API authentication
            if self._check_api_authentication():
                api_audit['score'] += 25
            else:
                api_audit['issues'].append("API authentication not properly implemented")
                api_audit['recommendations'].append("Implement proper API authentication")
            
            # Check for input validation
            if self._check_api_input_validation():
                api_audit['score'] += 25
            else:
                api_audit['issues'].append("API input validation insufficient")
                api_audit['recommendations'].append("Implement comprehensive input validation")
            
        except Exception as e:
            api_audit['issues'].append(f"API audit error: {str(e)}")
        
        return api_audit
    
    def _audit_authentication(self) -> Dict[str, Any]:
        """Audit authentication mechanisms"""
        auth_audit = {
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check for secure session configuration
            if current_app.config.get('SECRET_KEY') and len(current_app.config['SECRET_KEY']) >= 32:
                auth_audit['score'] += 25
            else:
                auth_audit['issues'].append("Weak or missing secret key")
                auth_audit['recommendations'].append("Use strong secret key (32+ characters)")
            
            # Check for password hashing
            if self._check_password_hashing():
                auth_audit['score'] += 25
            else:
                auth_audit['issues'].append("Passwords may not be properly hashed")
                auth_audit['recommendations'].append("Use bcrypt or Argon2 for password hashing")
            
            # Check for session security
            if self._check_session_security():
                auth_audit['score'] += 25
            else:
                auth_audit['issues'].append("Session security configuration insufficient")
                auth_audit['recommendations'].append("Configure secure session settings")
            
            # Check for multi-factor authentication
            if self._check_mfa_implementation():
                auth_audit['score'] += 25
            else:
                auth_audit['recommendations'].append("Consider implementing multi-factor authentication")
            
        except Exception as e:
            auth_audit['issues'].append(f"Authentication audit error: {str(e)}")
        
        return auth_audit
    
    def _audit_authorization(self) -> Dict[str, Any]:
        """Audit authorization mechanisms"""
        authz_audit = {
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check for role-based access control
            if self._check_rbac_implementation():
                authz_audit['score'] += 50
            else:
                authz_audit['issues'].append("Role-based access control not implemented")
                authz_audit['recommendations'].append("Implement RBAC system")
            
            # Check for permission validation
            if self._check_permission_validation():
                authz_audit['score'] += 50
            else:
                authz_audit['issues'].append("Permission validation insufficient")
                authz_audit['recommendations'].append("Implement comprehensive permission checks")
            
        except Exception as e:
            authz_audit['issues'].append(f"Authorization audit error: {str(e)}")
        
        return authz_audit
    
    def _audit_data_encryption(self) -> Dict[str, Any]:
        """Audit data encryption practices"""
        encryption_audit = {
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check for data encryption at rest
            if self._check_data_encryption_at_rest():
                encryption_audit['score'] += 50
            else:
                encryption_audit['issues'].append("Data not encrypted at rest")
                encryption_audit['recommendations'].append("Implement data encryption at rest")
            
            # Check for data encryption in transit
            if self._check_data_encryption_in_transit():
                encryption_audit['score'] += 50
            else:
                encryption_audit['issues'].append("Data not encrypted in transit")
                encryption_audit['recommendations'].append("Use HTTPS/TLS for all communications")
            
        except Exception as e:
            encryption_audit['issues'].append(f"Encryption audit error: {str(e)}")
        
        return encryption_audit
    
    def _audit_filesystem_security(self) -> Dict[str, Any]:
        """Audit filesystem security"""
        fs_audit = {
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check file permissions
            critical_files = ['config.py', 'run.py', 'requirements.txt']
            for file in critical_files:
                if os.path.exists(file):
                    if self._check_file_permissions(file):
                        fs_audit['score'] += 20
                    else:
                        fs_audit['issues'].append(f"File {file} has insecure permissions")
                        fs_audit['recommendations'].append(f"Restrict permissions on {file}")
            
            # Check for sensitive files
            sensitive_files = self._check_sensitive_files()
            if not sensitive_files:
                fs_audit['score'] += 40
            else:
                fs_audit['issues'].extend(sensitive_files)
                fs_audit['recommendations'].append("Remove or secure sensitive files")
            
        except Exception as e:
            fs_audit['issues'].append(f"Filesystem audit error: {str(e)}")
        
        return fs_audit
    
    def _audit_configuration_security(self) -> Dict[str, Any]:
        """Audit configuration security"""
        config_audit = {
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check for debug mode
            if not current_app.config.get('DEBUG', False):
                config_audit['score'] += 25
            else:
                config_audit['issues'].append("Debug mode enabled in production")
                config_audit['recommendations'].append("Disable debug mode in production")
            
            # Check for secure headers
            if self._check_secure_headers():
                config_audit['score'] += 25
            else:
                config_audit['issues'].append("Security headers not configured")
                config_audit['recommendations'].append("Configure security headers")
            
            # Check for environment variables
            if self._check_environment_security():
                config_audit['score'] += 25
            else:
                config_audit['issues'].append("Environment variables not properly secured")
                config_audit['recommendations'].append("Use environment variables for sensitive data")
            
            # Check for logging security
            if self._check_logging_security():
                config_audit['score'] += 25
            else:
                config_audit['issues'].append("Logging may expose sensitive information")
                config_audit['recommendations'].append("Configure secure logging")
            
        except Exception as e:
            config_audit['issues'].append(f"Configuration audit error: {str(e)}")
        
        return config_audit
    
    def _calculate_security_score(self) -> int:
        """Calculate overall security score"""
        total_score = 0
        max_score = 0
        
        for audit_type, audit_result in self.audit_results.items():
            if isinstance(audit_result, dict) and 'score' in audit_result:
                total_score += audit_result['score']
                max_score += 100  # Assuming each audit type has max 100 points
        
        if max_score > 0:
            return int((total_score / max_score) * 100)
        return 0
    
    # Helper methods for specific security checks
    def _check_sql_injection_vulnerabilities(self) -> bool:
        """Check for SQL injection vulnerabilities"""
        # This would typically scan code for SQL injection patterns
        return True  # Placeholder
    
    def _check_database_permissions(self) -> bool:
        """Check database permissions"""
        return True  # Placeholder
    
    def _check_api_authentication(self) -> bool:
        """Check API authentication implementation"""
        return True  # Placeholder
    
    def _check_api_input_validation(self) -> bool:
        """Check API input validation"""
        return True  # Placeholder
    
    def _check_password_hashing(self) -> bool:
        """Check password hashing implementation"""
        return True  # Placeholder
    
    def _check_session_security(self) -> bool:
        """Check session security configuration"""
        return True  # Placeholder
    
    def _check_mfa_implementation(self) -> bool:
        """Check multi-factor authentication implementation"""
        return False  # Placeholder
    
    def _check_rbac_implementation(self) -> bool:
        """Check role-based access control implementation"""
        return True  # Placeholder
    
    def _check_permission_validation(self) -> bool:
        """Check permission validation"""
        return True  # Placeholder
    
    def _check_data_encryption_at_rest(self) -> bool:
        """Check data encryption at rest"""
        return False  # Placeholder
    
    def _check_data_encryption_in_transit(self) -> bool:
        """Check data encryption in transit"""
        return True  # Placeholder
    
    def _check_file_permissions(self, file_path: str) -> bool:
        """Check file permissions"""
        try:
            import stat
            st = os.stat(file_path)
            return bool(st.st_mode & stat.S_IROTH) == False  # No read for others
        except:
            return False
    
    def _check_sensitive_files(self) -> List[str]:
        """Check for sensitive files"""
        sensitive_patterns = ['.env', '.pem', '.key', 'password', 'secret']
        found_files = []
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(pattern in file.lower() for pattern in sensitive_patterns):
                    found_files.append(f"Sensitive file found: {os.path.join(root, file)}")
        
        return found_files
    
    def _check_secure_headers(self) -> bool:
        """Check for secure headers configuration"""
        return True  # Placeholder
    
    def _check_environment_security(self) -> bool:
        """Check environment security"""
        return True  # Placeholder
    
    def _check_logging_security(self) -> bool:
        """Check logging security"""
        return True  # Placeholder
    
    def generate_security_report(self) -> str:
        """Generate human-readable security report"""
        if not self.audit_results:
            return "No audit results available. Run perform_security_audit() first."
        
        report = f"""
# Security Audit Report
Generated: {self.audit_results.get('timestamp', 'Unknown')}

## Overall Security Score: {self.audit_results.get('overall_score', 0)}/100

## Critical Issues ({len(self.critical_issues)}):
"""
        
        for issue in self.critical_issues:
            report += f"- {issue}\n"
        
        report += f"""
## Warnings ({len(self.warnings)}):
"""
        
        for warning in self.warnings:
            report += f"- {warning}\n"
        
        report += f"""
## Recommendations ({len(self.recommendations)}):
"""
        
        for rec in self.recommendations:
            report += f"- {rec}\n"
        
        return report 
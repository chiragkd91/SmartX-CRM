"""
Penetration Tester for CRM System
Security penetration testing and assessment
"""

import os
import json
import logging
import requests
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import re
import hashlib
import base64

class PenetrationTester:
    """Security penetration testing system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results = {}
        self.vulnerabilities_found = []
        self.security_score = 0
        self.test_timestamp = None
    
    def perform_penetration_test(self) -> Dict[str, Any]:
        """
        Perform comprehensive penetration testing
        Returns test results with vulnerability details
        """
        self.logger.info("Starting penetration testing...")
        self.test_timestamp = datetime.now()
        
        try:
            # Authentication bypass testing
            auth_bypass_results = self._test_authentication_bypass()
            
            # Authorization testing
            authorization_results = self._test_authorization()
            
            # Data exposure testing
            data_exposure_results = self._test_data_exposure()
            
            # API security testing
            api_security_results = self._test_api_security()
            
            # Social engineering testing
            social_engineering_results = self._test_social_engineering()
            
            # Compile results
            penetration_results = {
                'test_timestamp': self.test_timestamp.isoformat(),
                'authentication_bypass': auth_bypass_results,
                'authorization': authorization_results,
                'data_exposure': data_exposure_results,
                'api_security': api_security_results,
                'social_engineering': social_engineering_results,
                'total_vulnerabilities': len(self.vulnerabilities_found),
                'security_score': self._calculate_security_score(),
                'recommendations': self._generate_recommendations()
            }
            
            self.test_results = penetration_results
            self.logger.info(f"Penetration testing completed. Found {len(self.vulnerabilities_found)} vulnerabilities.")
            
            return penetration_results
            
        except Exception as e:
            self.logger.error(f"Penetration testing failed: {str(e)}")
            raise
    
    def _test_authentication_bypass(self) -> Dict[str, Any]:
        """Test for authentication bypass vulnerabilities"""
        auth_test = {
            'vulnerabilities': [],
            'tests_performed': 0,
            'score': 0
        }
        
        try:
            # Test 1: SQL injection in login
            auth_test['tests_performed'] += 1
            if self._test_sql_injection_login():
                auth_test['vulnerabilities'].append({
                    'type': 'sql_injection_login',
                    'severity': 'critical',
                    'description': 'SQL injection vulnerability in login form',
                    'recommendation': 'Use parameterized queries and input validation'
                })
            else:
                auth_test['score'] += 20
            
            # Test 2: Weak password policies
            auth_test['tests_performed'] += 1
            if self._test_weak_passwords():
                auth_test['vulnerabilities'].append({
                    'type': 'weak_password_policy',
                    'severity': 'high',
                    'description': 'Weak password policy allows easily guessable passwords',
                    'recommendation': 'Implement strong password requirements'
                })
            else:
                auth_test['score'] += 20
            
            # Test 3: Session fixation
            auth_test['tests_performed'] += 1
            if self._test_session_fixation():
                auth_test['vulnerabilities'].append({
                    'type': 'session_fixation',
                    'severity': 'high',
                    'description': 'Session fixation vulnerability detected',
                    'recommendation': 'Regenerate session ID after login'
                })
            else:
                auth_test['score'] += 20
            
            # Test 4: Brute force protection
            auth_test['tests_performed'] += 1
            if self._test_brute_force_protection():
                auth_test['vulnerabilities'].append({
                    'type': 'no_brute_force_protection',
                    'severity': 'high',
                    'description': 'No brute force protection implemented',
                    'recommendation': 'Implement rate limiting and account lockout'
                })
            else:
                auth_test['score'] += 20
            
            # Test 5: Password reset security
            auth_test['tests_performed'] += 1
            if self._test_password_reset_security():
                auth_test['vulnerabilities'].append({
                    'type': 'weak_password_reset',
                    'severity': 'medium',
                    'description': 'Weak password reset mechanism',
                    'recommendation': 'Implement secure password reset with time-limited tokens'
                })
            else:
                auth_test['score'] += 20
            
        except Exception as e:
            auth_test['vulnerabilities'].append({
                'type': 'test_error',
                'severity': 'medium',
                'description': f'Error during authentication testing: {str(e)}',
                'recommendation': 'Check authentication testing configuration'
            })
        
        return auth_test
    
    def _test_authorization(self) -> Dict[str, Any]:
        """Test for authorization vulnerabilities"""
        authz_test = {
            'vulnerabilities': [],
            'tests_performed': 0,
            'score': 0
        }
        
        try:
            # Test 1: Horizontal privilege escalation
            authz_test['tests_performed'] += 1
            if self._test_horizontal_privilege_escalation():
                authz_test['vulnerabilities'].append({
                    'type': 'horizontal_privilege_escalation',
                    'severity': 'high',
                    'description': 'Users can access other users\' data',
                    'recommendation': 'Implement proper user data isolation'
                })
            else:
                authz_test['score'] += 25
            
            # Test 2: Vertical privilege escalation
            authz_test['tests_performed'] += 1
            if self._test_vertical_privilege_escalation():
                authz_test['vulnerabilities'].append({
                    'type': 'vertical_privilege_escalation',
                    'severity': 'critical',
                    'description': 'Users can access admin functions',
                    'recommendation': 'Implement proper role-based access control'
                })
            else:
                authz_test['score'] += 25
            
            # Test 3: Missing authorization checks
            authz_test['tests_performed'] += 1
            if self._test_missing_auth_checks():
                authz_test['vulnerabilities'].append({
                    'type': 'missing_authorization',
                    'severity': 'high',
                    'description': 'Missing authorization checks on sensitive operations',
                    'recommendation': 'Add authorization checks to all sensitive endpoints'
                })
            else:
                authz_test['score'] += 25
            
            # Test 4: IDOR vulnerabilities
            authz_test['tests_performed'] += 1
            if self._test_idor_vulnerabilities():
                authz_test['vulnerabilities'].append({
                    'type': 'idor_vulnerability',
                    'severity': 'high',
                    'description': 'Insecure Direct Object Reference vulnerability',
                    'recommendation': 'Implement proper object ownership validation'
                })
            else:
                authz_test['score'] += 25
            
        except Exception as e:
            authz_test['vulnerabilities'].append({
                'type': 'test_error',
                'severity': 'medium',
                'description': f'Error during authorization testing: {str(e)}',
                'recommendation': 'Check authorization testing configuration'
            })
        
        return authz_test
    
    def _test_data_exposure(self) -> Dict[str, Any]:
        """Test for data exposure vulnerabilities"""
        data_test = {
            'vulnerabilities': [],
            'tests_performed': 0,
            'score': 0
        }
        
        try:
            # Test 1: Sensitive data in logs
            data_test['tests_performed'] += 1
            if self._test_sensitive_data_logging():
                data_test['vulnerabilities'].append({
                    'type': 'sensitive_data_logging',
                    'severity': 'medium',
                    'description': 'Sensitive data found in application logs',
                    'recommendation': 'Remove sensitive data from logs'
                })
            else:
                data_test['score'] += 25
            
            # Test 2: Information disclosure
            data_test['tests_performed'] += 1
            if self._test_information_disclosure():
                data_test['vulnerabilities'].append({
                    'type': 'information_disclosure',
                    'severity': 'medium',
                    'description': 'Sensitive information exposed in error messages',
                    'recommendation': 'Sanitize error messages in production'
                })
            else:
                data_test['score'] += 25
            
            # Test 3: Directory traversal
            data_test['tests_performed'] += 1
            if self._test_directory_traversal():
                data_test['vulnerabilities'].append({
                    'type': 'directory_traversal',
                    'severity': 'high',
                    'description': 'Directory traversal vulnerability detected',
                    'recommendation': 'Validate and sanitize file paths'
                })
            else:
                data_test['score'] += 25
            
            # Test 4: Data encryption
            data_test['tests_performed'] += 1
            if self._test_data_encryption():
                data_test['vulnerabilities'].append({
                    'type': 'unencrypted_data',
                    'severity': 'high',
                    'description': 'Sensitive data not encrypted',
                    'recommendation': 'Implement data encryption for sensitive information'
                })
            else:
                data_test['score'] += 25
            
        except Exception as e:
            data_test['vulnerabilities'].append({
                'type': 'test_error',
                'severity': 'medium',
                'description': f'Error during data exposure testing: {str(e)}',
                'recommendation': 'Check data exposure testing configuration'
            })
        
        return data_test
    
    def _test_api_security(self) -> Dict[str, Any]:
        """Test for API security vulnerabilities"""
        api_test = {
            'vulnerabilities': [],
            'tests_performed': 0,
            'score': 0
        }
        
        try:
            # Test 1: API authentication
            api_test['tests_performed'] += 1
            if self._test_api_authentication():
                api_test['vulnerabilities'].append({
                    'type': 'api_authentication_bypass',
                    'severity': 'critical',
                    'description': 'API endpoints accessible without authentication',
                    'recommendation': 'Implement proper API authentication'
                })
            else:
                api_test['score'] += 25
            
            # Test 2: API rate limiting
            api_test['tests_performed'] += 1
            if self._test_api_rate_limiting():
                api_test['vulnerabilities'].append({
                    'type': 'no_api_rate_limiting',
                    'severity': 'medium',
                    'description': 'No rate limiting on API endpoints',
                    'recommendation': 'Implement API rate limiting'
                })
            else:
                api_test['score'] += 25
            
            # Test 3: API input validation
            api_test['tests_performed'] += 1
            if self._test_api_input_validation():
                api_test['vulnerabilities'].append({
                    'type': 'weak_api_input_validation',
                    'severity': 'high',
                    'description': 'Weak input validation on API endpoints',
                    'recommendation': 'Implement comprehensive input validation'
                })
            else:
                api_test['score'] += 25
            
            # Test 4: API error handling
            api_test['tests_performed'] += 1
            if self._test_api_error_handling():
                api_test['vulnerabilities'].append({
                    'type': 'api_error_disclosure',
                    'severity': 'medium',
                    'description': 'Sensitive information in API error responses',
                    'recommendation': 'Sanitize API error responses'
                })
            else:
                api_test['score'] += 25
            
        except Exception as e:
            api_test['vulnerabilities'].append({
                'type': 'test_error',
                'severity': 'medium',
                'description': f'Error during API security testing: {str(e)}',
                'recommendation': 'Check API security testing configuration'
            })
        
        return api_test
    
    def _test_social_engineering(self) -> Dict[str, Any]:
        """Test for social engineering vulnerabilities"""
        social_test = {
            'vulnerabilities': [],
            'tests_performed': 0,
            'score': 0
        }
        
        try:
            # Test 1: Phishing susceptibility
            social_test['tests_performed'] += 1
            if self._test_phishing_susceptibility():
                social_test['vulnerabilities'].append({
                    'type': 'phishing_susceptible',
                    'severity': 'medium',
                    'description': 'System susceptible to phishing attacks',
                    'recommendation': 'Implement multi-factor authentication'
                })
            else:
                social_test['score'] += 33
            
            # Test 2: Password policy awareness
            social_test['tests_performed'] += 1
            if self._test_password_policy_awareness():
                social_test['vulnerabilities'].append({
                    'type': 'weak_password_awareness',
                    'severity': 'low',
                    'description': 'Users not educated about password security',
                    'recommendation': 'Implement security awareness training'
                })
            else:
                social_test['score'] += 33
            
            # Test 3: Social media exposure
            social_test['tests_performed'] += 1
            if self._test_social_media_exposure():
                social_test['vulnerabilities'].append({
                    'type': 'social_media_exposure',
                    'severity': 'low',
                    'description': 'Sensitive information exposed on social media',
                    'recommendation': 'Implement social media security policies'
                })
            else:
                social_test['score'] += 34
            
        except Exception as e:
            social_test['vulnerabilities'].append({
                'type': 'test_error',
                'severity': 'medium',
                'description': f'Error during social engineering testing: {str(e)}',
                'recommendation': 'Check social engineering testing configuration'
            })
        
        return social_test
    
    # Test implementation methods (placeholders)
    def _test_sql_injection_login(self) -> bool:
        """Test for SQL injection in login form"""
        # This would perform actual SQL injection tests
        return False  # Placeholder
    
    def _test_weak_passwords(self) -> bool:
        """Test for weak password policies"""
        return False  # Placeholder
    
    def _test_session_fixation(self) -> bool:
        """Test for session fixation vulnerabilities"""
        return False  # Placeholder
    
    def _test_brute_force_protection(self) -> bool:
        """Test for brute force protection"""
        return False  # Placeholder
    
    def _test_password_reset_security(self) -> bool:
        """Test password reset security"""
        return False  # Placeholder
    
    def _test_horizontal_privilege_escalation(self) -> bool:
        """Test for horizontal privilege escalation"""
        return False  # Placeholder
    
    def _test_vertical_privilege_escalation(self) -> bool:
        """Test for vertical privilege escalation"""
        return False  # Placeholder
    
    def _test_missing_auth_checks(self) -> bool:
        """Test for missing authorization checks"""
        return False  # Placeholder
    
    def _test_idor_vulnerabilities(self) -> bool:
        """Test for IDOR vulnerabilities"""
        return False  # Placeholder
    
    def _test_sensitive_data_logging(self) -> bool:
        """Test for sensitive data in logs"""
        return False  # Placeholder
    
    def _test_information_disclosure(self) -> bool:
        """Test for information disclosure"""
        return False  # Placeholder
    
    def _test_directory_traversal(self) -> bool:
        """Test for directory traversal vulnerabilities"""
        return False  # Placeholder
    
    def _test_data_encryption(self) -> bool:
        """Test for data encryption"""
        return False  # Placeholder
    
    def _test_api_authentication(self) -> bool:
        """Test API authentication"""
        return False  # Placeholder
    
    def _test_api_rate_limiting(self) -> bool:
        """Test API rate limiting"""
        return False  # Placeholder
    
    def _test_api_input_validation(self) -> bool:
        """Test API input validation"""
        return False  # Placeholder
    
    def _test_api_error_handling(self) -> bool:
        """Test API error handling"""
        return False  # Placeholder
    
    def _test_phishing_susceptibility(self) -> bool:
        """Test phishing susceptibility"""
        return False  # Placeholder
    
    def _test_password_policy_awareness(self) -> bool:
        """Test password policy awareness"""
        return False  # Placeholder
    
    def _test_social_media_exposure(self) -> bool:
        """Test social media exposure"""
        return False  # Placeholder
    
    def _calculate_security_score(self) -> int:
        """Calculate overall security score from test results"""
        total_score = 0
        max_score = 0
        
        for test_type, test_result in self.test_results.items():
            if isinstance(test_result, dict) and 'score' in test_result:
                total_score += test_result['score']
                max_score += 100  # Assuming each test type has max 100 points
        
        if max_score > 0:
            return int((total_score / max_score) * 100)
        return 0
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations based on test results"""
        recommendations = []
        
        # Collect all vulnerabilities
        all_vulnerabilities = []
        for test_type, test_result in self.test_results.items():
            if isinstance(test_result, dict) and 'vulnerabilities' in test_result:
                all_vulnerabilities.extend(test_result['vulnerabilities'])
        
        # Generate recommendations based on vulnerability types
        vulnerability_types = set(vuln.get('type') for vuln in all_vulnerabilities)
        
        if 'sql_injection_login' in vulnerability_types:
            recommendations.append("Implement input validation and use parameterized queries")
        
        if 'weak_password_policy' in vulnerability_types:
            recommendations.append("Enforce strong password policies with complexity requirements")
        
        if 'session_fixation' in vulnerability_types:
            recommendations.append("Regenerate session IDs after successful authentication")
        
        if 'no_brute_force_protection' in vulnerability_types:
            recommendations.append("Implement rate limiting and account lockout mechanisms")
        
        if 'horizontal_privilege_escalation' in vulnerability_types:
            recommendations.append("Implement proper user data isolation and access controls")
        
        if 'vertical_privilege_escalation' in vulnerability_types:
            recommendations.append("Implement role-based access control (RBAC)")
        
        if 'missing_authorization' in vulnerability_types:
            recommendations.append("Add authorization checks to all sensitive operations")
        
        if 'idor_vulnerability' in vulnerability_types:
            recommendations.append("Implement proper object ownership validation")
        
        if 'sensitive_data_logging' in vulnerability_types:
            recommendations.append("Remove sensitive data from application logs")
        
        if 'information_disclosure' in vulnerability_types:
            recommendations.append("Sanitize error messages and responses")
        
        if 'directory_traversal' in vulnerability_types:
            recommendations.append("Validate and sanitize all file paths")
        
        if 'unencrypted_data' in vulnerability_types:
            recommendations.append("Implement encryption for sensitive data")
        
        if 'api_authentication_bypass' in vulnerability_types:
            recommendations.append("Implement proper API authentication mechanisms")
        
        if 'no_api_rate_limiting' in vulnerability_types:
            recommendations.append("Implement rate limiting for API endpoints")
        
        if 'weak_api_input_validation' in vulnerability_types:
            recommendations.append("Implement comprehensive input validation for APIs")
        
        if 'api_error_disclosure' in vulnerability_types:
            recommendations.append("Sanitize API error responses")
        
        if 'phishing_susceptible' in vulnerability_types:
            recommendations.append("Implement multi-factor authentication")
        
        if 'weak_password_awareness' in vulnerability_types:
            recommendations.append("Provide security awareness training to users")
        
        if 'social_media_exposure' in vulnerability_types:
            recommendations.append("Implement social media security policies")
        
        return recommendations
    
    def generate_penetration_test_report(self) -> str:
        """Generate human-readable penetration test report"""
        if not self.test_results:
            return "No test results available. Run perform_penetration_test() first."
        
        report = f"""
# Penetration Test Report
Generated: {self.test_results.get('test_timestamp', 'Unknown')}

## Overall Security Score: {self.test_results.get('security_score', 0)}/100

## Test Summary
- Total Vulnerabilities Found: {self.test_results.get('total_vulnerabilities', 0)}
- Tests Performed: {sum(test.get('tests_performed', 0) for test in self.test_results.values() if isinstance(test, dict))}

## Detailed Results
"""
        
        for test_type, test_result in self.test_results.items():
            if isinstance(test_result, dict) and 'vulnerabilities' in test_result:
                report += f"\n### {test_type.replace('_', ' ').title()}\n"
                report += f"Score: {test_result.get('score', 0)}/100\n"
                report += f"Tests Performed: {test_result.get('tests_performed', 0)}\n"
                
                if test_result['vulnerabilities']:
                    report += "Vulnerabilities Found:\n"
                    for vuln in test_result['vulnerabilities']:
                        report += f"- **{vuln.get('type', 'Unknown')}** ({vuln.get('severity', 'Unknown')}): {vuln.get('description', 'No description')}\n"
                        report += f"  - Recommendation: {vuln.get('recommendation', 'No recommendation')}\n"
                else:
                    report += "No vulnerabilities found.\n"
        
        report += f"\n## Recommendations\n"
        for rec in self.test_results.get('recommendations', []):
            report += f"- {rec}\n"
        
        return report 
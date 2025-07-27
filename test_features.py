#!/usr/bin/env python3
"""
Comprehensive CRM Feature Testing Script
Tests all implemented features and identifies issues
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

class CRMFeatureTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {
            'passed': [],
            'failed': [],
            'errors': []
        }
        
    def log_test(self, test_name, status, message=""):
        """Log test results"""
        if status == 'PASS':
            self.test_results['passed'].append(test_name)
            print(f"✅ {test_name}: PASS")
        elif status == 'FAIL':
            self.test_results['failed'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAIL - {message}")
        else:
            self.test_results['errors'].append(f"{test_name}: {message}")
            print(f"🚨 {test_name}: ERROR - {message}")
    
    def test_server_connection(self):
        """Test if the server is running"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            if response.status_code == 200:
                self.log_test("Server Connection", "PASS")
                return True
            else:
                self.log_test("Server Connection", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Server Connection", "ERROR", str(e))
            return False
    
    def test_home_page(self):
        """Test home page accessibility"""
        try:
            response = self.session.get(urljoin(self.base_url, "/home"), timeout=5)
            if response.status_code == 200:
                self.log_test("Home Page", "PASS")
                return True
            else:
                self.log_test("Home Page", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Home Page", "ERROR", str(e))
            return False
    
    def test_login_page(self):
        """Test login page accessibility"""
        try:
            response = self.session.get(urljoin(self.base_url, "/login"), timeout=5)
            if response.status_code == 200:
                self.log_test("Login Page", "PASS")
                return True
            else:
                self.log_test("Login Page", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Login Page", "ERROR", str(e))
            return False
    
    def test_register_page(self):
        """Test register page accessibility"""
        try:
            response = self.session.get(urljoin(self.base_url, "/register"), timeout=5)
            if response.status_code == 200:
                self.log_test("Register Page", "PASS")
                return True
            else:
                self.log_test("Register Page", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Register Page", "ERROR", str(e))
            return False
    
    def test_login_functionality(self):
        """Test login functionality"""
        try:
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            response = self.session.post(urljoin(self.base_url, "/login"), data=login_data, timeout=5)
            if response.status_code == 200:
                # Check if we're redirected to dashboard
                if 'dashboard' in response.url or 'crm' in response.url:
                    self.log_test("Login Functionality", "PASS")
                    return True
                else:
                    self.log_test("Login Functionality", "FAIL", "Not redirected to dashboard")
                    return False
            else:
                self.log_test("Login Functionality", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Login Functionality", "ERROR", str(e))
            return False
    
    def test_crm_dashboard(self):
        """Test CRM dashboard accessibility"""
        try:
            response = self.session.get(urljoin(self.base_url, "/crm/dashboard"), timeout=5)
            if response.status_code == 200:
                self.log_test("CRM Dashboard", "PASS")
                return True
            else:
                self.log_test("CRM Dashboard", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("CRM Dashboard", "ERROR", str(e))
            return False
    
    def test_leads_list(self):
        """Test leads list page"""
        try:
            response = self.session.get(urljoin(self.base_url, "/crm/leads/list"), timeout=5)
            if response.status_code == 200:
                self.log_test("Leads List", "PASS")
                return True
            else:
                self.log_test("Leads List", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Leads List", "ERROR", str(e))
            return False
    
    def test_accounts_list(self):
        """Test accounts list page"""
        try:
            response = self.session.get(urljoin(self.base_url, "/crm/accounts/list"), timeout=5)
            if response.status_code == 200:
                self.log_test("Accounts List", "PASS")
                return True
            else:
                self.log_test("Accounts List", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Accounts List", "ERROR", str(e))
            return False
    
    def test_contacts_list(self):
        """Test contacts list page"""
        try:
            response = self.session.get(urljoin(self.base_url, "/crm/contacts/list"), timeout=5)
            if response.status_code == 200:
                self.log_test("Contacts List", "PASS")
                return True
            else:
                self.log_test("Contacts List", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Contacts List", "ERROR", str(e))
            return False
    
    def test_opportunities_list(self):
        """Test opportunities list page"""
        try:
            response = self.session.get(urljoin(self.base_url, "/crm/opportunities/list"), timeout=5)
            if response.status_code == 200:
                self.log_test("Opportunities List", "PASS")
                return True
            else:
                self.log_test("Opportunities List", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Opportunities List", "ERROR", str(e))
            return False
    
    def test_activities_list(self):
        """Test activities list page"""
        try:
            response = self.session.get(urljoin(self.base_url, "/crm/activities/list"), timeout=5)
            if response.status_code == 200:
                self.log_test("Activities List", "PASS")
                return True
            else:
                self.log_test("Activities List", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Activities List", "ERROR", str(e))
            return False
    
    def test_quotes_list(self):
        """Test quotes list page"""
        try:
            response = self.session.get(urljoin(self.base_url, "/crm/quotes/list"), timeout=5)
            if response.status_code == 200:
                self.log_test("Quotes List", "PASS")
                return True
            else:
                self.log_test("Quotes List", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Quotes List", "ERROR", str(e))
            return False
    
    def test_security_features(self):
        """Test security features"""
        try:
            response = self.session.get(urljoin(self.base_url, "/security/audit"), timeout=5)
            if response.status_code == 200:
                self.log_test("Security Audit", "PASS")
                return True
            else:
                self.log_test("Security Audit", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Security Audit", "ERROR", str(e))
            return False
    
    def test_backup_features(self):
        """Test backup features"""
        try:
            response = self.session.get(urljoin(self.base_url, "/backup/manager"), timeout=5)
            if response.status_code == 200:
                self.log_test("Backup Manager", "PASS")
                return True
            else:
                self.log_test("Backup Manager", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Backup Manager", "ERROR", str(e))
            return False
    
    def test_monitoring_features(self):
        """Test monitoring features"""
        try:
            response = self.session.get(urljoin(self.base_url, "/monitoring/dashboard"), timeout=5)
            if response.status_code == 200:
                self.log_test("Monitoring Dashboard", "PASS")
                return True
            else:
                self.log_test("Monitoring Dashboard", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Monitoring Dashboard", "ERROR", str(e))
            return False
    
    def test_admin_features(self):
        """Test admin features"""
        try:
            response = self.session.get(urljoin(self.base_url, "/admin/dashboard"), timeout=5)
            if response.status_code == 200:
                self.log_test("Admin Dashboard", "PASS")
                return True
            else:
                self.log_test("Admin Dashboard", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Admin Dashboard", "ERROR", str(e))
            return False
    
    def test_api_documentation(self):
        """Test API documentation"""
        try:
            response = self.session.get(urljoin(self.base_url, "/api/docs"), timeout=5)
            if response.status_code == 200:
                self.log_test("API Documentation", "PASS")
                return True
            else:
                self.log_test("API Documentation", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("API Documentation", "ERROR", str(e))
            return False
    
    def test_mobile_features(self):
        """Test mobile features"""
        try:
            response = self.session.get(urljoin(self.base_url, "/mobile/dashboard"), timeout=5)
            if response.status_code == 200:
                self.log_test("Mobile Dashboard", "PASS")
                return True
            else:
                self.log_test("Mobile Dashboard", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Mobile Dashboard", "ERROR", str(e))
            return False
    
    def test_developer_features(self):
        """Test developer features"""
        try:
            response = self.session.get(urljoin(self.base_url, "/developer/portal"), timeout=5)
            if response.status_code == 200:
                self.log_test("Developer Portal", "PASS")
                return True
            else:
                self.log_test("Developer Portal", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Developer Portal", "ERROR", str(e))
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive CRM Feature Testing...")
        print("=" * 60)
        
        # Test basic connectivity
        if not self.test_server_connection():
            print("❌ Server is not running. Please start the application first.")
            return
        
        # Test public pages
        print("\n📄 Testing Public Pages:")
        self.test_home_page()
        self.test_login_page()
        self.test_register_page()
        
        # Test authentication
        print("\n🔐 Testing Authentication:")
        self.test_login_functionality()
        
        # Test CRM features
        print("\n💼 Testing CRM Features:")
        self.test_crm_dashboard()
        self.test_leads_list()
        self.test_accounts_list()
        self.test_contacts_list()
        self.test_opportunities_list()
        self.test_activities_list()
        self.test_quotes_list()
        
        # Test advanced features
        print("\n🔧 Testing Advanced Features:")
        self.test_security_features()
        self.test_backup_features()
        self.test_monitoring_features()
        self.test_admin_features()
        self.test_api_documentation()
        self.test_mobile_features()
        self.test_developer_features()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {len(self.test_results['passed'])}")
        print(f"❌ Failed: {len(self.test_results['failed'])}")
        print(f"🚨 Errors: {len(self.test_results['errors'])}")
        
        if self.test_results['failed']:
            print("\n❌ FAILED TESTS:")
            for failure in self.test_results['failed']:
                print(f"  - {failure}")
        
        if self.test_results['errors']:
            print("\n🚨 ERRORS:")
            for error in self.test_results['errors']:
                print(f"  - {error}")
        
        total_tests = len(self.test_results['passed']) + len(self.test_results['failed']) + len(self.test_results['errors'])
        success_rate = (len(self.test_results['passed']) / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Most features are working correctly!")
        elif success_rate >= 60:
            print("⚠️  Some features need attention.")
        else:
            print("🚨 Many features need to be fixed.")

if __name__ == "__main__":
    tester = CRMFeatureTester()
    tester.run_all_tests() 
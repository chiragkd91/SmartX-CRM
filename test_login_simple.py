#!/usr/bin/env python3
"""
Simple test to verify login functionality
"""

import requests
import sys

def test_login():
    """Test login functionality"""
    base_url = "http://localhost:5000"
    
    # Test credentials
    username = "admin"
    password = "admin123"
    
    print("=== Testing Login Functionality ===")
    print(f"URL: {base_url}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print()
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # Get the login page first
        print("1. Getting login page...")
        response = session.get(f"{base_url}/login")
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print("   ❌ Failed to get login page")
            return False
        
        # Submit login form
        print("2. Submitting login form...")
        login_data = {
            'username': username,
            'password': password
        }
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Login successful - redirected")
            redirect_location = response.headers.get('Location', '')
            print(f"   Redirect to: {redirect_location}")
            
            # Follow the redirect
            print("3. Following redirect...")
            response = session.get(f"{base_url}{redirect_location}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Successfully reached dashboard")
                return True
            else:
                print("   ❌ Failed to reach dashboard")
                return False
        else:
            print("   ❌ Login failed - no redirect")
            print(f"   Response content: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the Flask app is running")
        print("   Run: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = test_login()
    if success:
        print("\n✅ Login test passed!")
        sys.exit(0)
    else:
        print("\n❌ Login test failed!")
        sys.exit(1) 
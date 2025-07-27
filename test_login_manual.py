#!/usr/bin/env python3
"""
Manual test script to verify login functionality
"""

from app import create_app, db
from app.models.crm import User
from werkzeug.security import check_password_hash

def test_login_manual():
    """Manual test of login functionality"""
    app = create_app()
    
    with app.app_context():
        print("=== Manual Login Test ===\n")
        
        # Test credentials
        username = "admin"
        password = "admin123"
        
        print(f"Testing login with:")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print()
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print("❌ User not found!")
            return False
        
        print(f"✅ User found:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"  Active: {user.is_active}")
        print()
        
        # Test password
        if check_password_hash(user.password_hash, password):
            print("✅ Password is correct!")
            print("✅ Login should work!")
            return True
        else:
            print("❌ Password is incorrect!")
            return False

if __name__ == '__main__':
    success = test_login_manual()
    if success:
        print("\n🎉 Login test passed! You can use admin/admin123 to log in.")
    else:
        print("\n💥 Login test failed!") 
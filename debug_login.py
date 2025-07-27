#!/usr/bin/env python3
"""
Debug script to help identify login issues
"""

from app import create_app, db
from app.models.crm import User
from werkzeug.security import check_password_hash, generate_password_hash

def debug_login():
    """Debug login functionality"""
    app = create_app()
    
    with app.app_context():
        print("=== CRM Login Debug ===\n")
        
        # Check if database exists and has users
        try:
            users = User.query.all()
            print(f"Found {len(users)} users in database:")
            
            for user in users:
                print(f"  - Username: {user.username}")
                print(f"    Email: {user.email}")
                print(f"    Role: {user.role}")
                print(f"    Active: {user.is_active}")
                print(f"    Password hash: {user.password_hash[:20]}...")
                print()
                
        except Exception as e:
            print(f"Error accessing database: {e}")
            return
        
        # Test common passwords
        print("=== Testing Common Passwords ===")
        common_passwords = [
            'admin123',
            'admin',
            'password',
            '123456',
            'testpass123',
            'admin@123',
            'Admin123',
            'admin123!'
        ]
        
        for username in ['admin', 'testuser']:
            user = User.query.filter_by(username=username).first()
            if user:
                print(f"\nTesting user: {username}")
                for password in common_passwords:
                    if check_password_hash(user.password_hash, password):
                        print(f"  ✅ Password found: {password}")
                        break
                else:
                    print(f"  ❌ None of the common passwords worked")
        
        # Create a test user if none exist
        if not users:
            print("\n=== Creating Test User ===")
            test_user = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                role='Admin'
            )
            db.session.add(test_user)
            db.session.commit()
            print("Created test user: admin / admin123")
        
        # Test login with known credentials
        print("\n=== Testing Login ===")
        test_credentials = [
            ('admin', 'admin123'),
            ('admin', 'password'),
            ('testuser', 'testpass123')
        ]
        
        for username, password in test_credentials:
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password_hash, password):
                    print(f"✅ Login successful: {username} / {password}")
                else:
                    print(f"❌ Login failed: {username} / {password}")
            else:
                print(f"❌ User not found: {username}")

if __name__ == '__main__':
    debug_login() 
#!/usr/bin/env python3
"""
Script to create a test user for the CRM system
Run this script to create a test user for authentication testing
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.crm import User

def create_test_user():
    """Create a test user for authentication testing"""
    app = create_app()
    
    with app.app_context():
        # Check if test user already exists
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            print("Test user 'admin' already exists!")
            print(f"Username: {existing_user.username}")
            print(f"Email: {existing_user.email}")
            print(f"Role: {existing_user.role}")
            return
        
        # Create test user
        test_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            role='Admin',
            is_active=True
        )
        
        try:
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("Email: admin@example.com")
            print("\nYou can now log in to the CRM system using these credentials.")
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_test_user() 
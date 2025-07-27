import pytest
import tempfile
import os
from app import create_app, db
from app.models.crm import User, Lead, Account, Contact, Opportunity, Activity, Quote, Territory
from app.models.crm_business_processes import Workflow, Campaign, LeadScoring, AutomationRule
from app.models.crm_integrations import Integration, EmailIntegration, CalendarIntegration
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        create_test_data()
    
    yield app
    
    # Clean up the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """A test client with authenticated user."""
    # Login first
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    return client

def create_test_data():
    """Create test data for the database."""
    # Create test user (check if exists first)
    existing_user = User.query.filter_by(username='testuser').first()
    if not existing_user:
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('testpass123'),
            first_name='Test',
            last_name='User',
            role='Admin'
        )
        db.session.add(test_user)
    
    # Create test territory (check if exists first)
    existing_territory = Territory.query.filter_by(name='Test Territory').first()
    if not existing_territory:
        territory = Territory(
            name='Test Territory',
            description='Test territory for testing',
            manager_id=1
        )
        db.session.add(territory)
    
    # Create test account (check if exists first)
    existing_account = Account.query.filter_by(name='Test Company').first()
    if not existing_account:
        account = Account(
            name='Test Company',
            industry='Technology',
            website='www.testcompany.com',
            phone='+1-555-0001',
            email='info@testcompany.com',
            annual_revenue=1000000,
            employee_count=10,
            status='Active',
            type='Customer',
            assigned_to=1,
            territory_id=1
        )
        db.session.add(account)
    
    # Create test lead (check if exists first)
    existing_lead = Lead.query.filter_by(email='john.doe@example.com').first()
    if not existing_lead:
        lead = Lead(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='+1-555-0123',
            company='Test Company',
            job_title='CTO',
            industry='Technology',
            source='Website',
            status='New',
            score=75,
            assigned_to=1
        )
        db.session.add(lead)
    
    # Create test contact (check if exists first)
    existing_contact = Contact.query.filter_by(email='jane.smith@example.com').first()
    if not existing_contact:
        contact = Contact(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='+1-555-0456',
            job_title='Marketing Director',
            department='Marketing',
            account_id=1,
            status='Active',
            assigned_to=1
        )
        db.session.add(contact)
    
    # Create test opportunity
    opportunity = Opportunity(
        name='Test Opportunity',
        account_id=1,
        contact_id=1,
        lead_id=1,
        stage='Prospecting',
        amount=50000,
        probability=25,
        type='New Business',
        source='Website',
        description='Test opportunity for testing',
        assigned_to=1
    )
    db.session.add(opportunity)
    
    # Create test activity
    activity = Activity(
        subject='Test Activity',
        type='Call',
        status='Planned',
        priority='Medium',
        description='Test activity for testing',
        account_id=1,
        contact_id=1,
        lead_id=1,
        opportunity_id=1,
        assigned_to=1,
        created_by=1
    )
    db.session.add(activity)
    
    db.session.commit() 
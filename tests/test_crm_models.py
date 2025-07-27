import pytest
from datetime import datetime, date
from app.models.crm import User, Lead, Account, Contact, Opportunity, Activity, Quote, Territory
from app import db

class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self, app):
        """Test user creation with valid data."""
        with app.app_context():
            user = User(
                username='testuser2',
                email='test2@example.com',
                password_hash='hashed_password',
                first_name='Test',
                last_name='User2',
                role='User'
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'testuser2'
            assert user.email == 'test2@example.com'
            assert user.full_name == 'Test User2'
    
    def test_user_repr(self, app):
        """Test user string representation."""
        with app.app_context():
            user = User.query.first()
            assert str(user) == f'<User {user.username}>'
    
    def test_user_get_id(self, app):
        """Test user get_id method for Flask-Login."""
        with app.app_context():
            user = User.query.first()
            assert user.get_id() == str(user.id)

class TestLeadModel:
    """Test cases for Lead model."""
    
    def test_lead_creation(self, app):
        """Test lead creation with valid data."""
        with app.app_context():
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
            db.session.commit()
            
            assert lead.id is not None
            assert lead.full_name == 'John Doe'
            assert lead.email == 'john.doe@example.com'
    
    def test_lead_repr(self, app):
        """Test lead string representation."""
        with app.app_context():
            lead = Lead.query.first()
            assert str(lead) == f'<Lead {lead.first_name} {lead.last_name}>'

class TestAccountModel:
    """Test cases for Account model."""
    
    def test_account_creation(self, app):
        """Test account creation with valid data."""
        with app.app_context():
            account = Account(
                name='Test Account',
                industry='Technology',
                website='www.testaccount.com',
                phone='+1-555-0001',
                email='info@testaccount.com',
                annual_revenue=1000000,
                employee_count=50,
                status='Active',
                type='Customer',
                assigned_to=1,
                territory_id=1
            )
            db.session.add(account)
            db.session.commit()
            
            assert account.id is not None
            assert account.name == 'Test Account'
    
    def test_account_repr(self, app):
        """Test account string representation."""
        with app.app_context():
            account = Account.query.first()
            assert str(account) == f'<Account {account.name}>'

class TestContactModel:
    """Test cases for Contact model."""
    
    def test_contact_creation(self, app):
        """Test contact creation with valid data."""
        with app.app_context():
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
            db.session.commit()
            
            assert contact.id is not None
            assert contact.full_name == 'Jane Smith'
    
    def test_contact_repr(self, app):
        """Test contact string representation."""
        with app.app_context():
            contact = Contact.query.first()
            assert str(contact) == f'<Contact {contact.first_name} {contact.last_name}>'

class TestOpportunityModel:
    """Test cases for Opportunity model."""
    
    def test_opportunity_creation(self, app):
        """Test opportunity creation with valid data."""
        with app.app_context():
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
                description='Test opportunity',
                assigned_to=1
            )
            db.session.add(opportunity)
            db.session.commit()
            
            assert opportunity.id is not None
            assert opportunity.name == 'Test Opportunity'
            assert opportunity.amount == 50000
    
    def test_opportunity_repr(self, app):
        """Test opportunity string representation."""
        with app.app_context():
            opportunity = Opportunity.query.first()
            assert str(opportunity) == f'<Opportunity {opportunity.name}>'

class TestActivityModel:
    """Test cases for Activity model."""
    
    def test_activity_creation(self, app):
        """Test activity creation with valid data."""
        with app.app_context():
            activity = Activity(
                subject='Test Activity',
                type='Call',
                status='Planned',
                priority='Medium',
                description='Test activity description',
                account_id=1,
                contact_id=1,
                lead_id=1,
                opportunity_id=1,
                assigned_to=1,
                created_by=1
            )
            db.session.add(activity)
            db.session.commit()
            
            assert activity.id is not None
            assert activity.subject == 'Test Activity'
            assert activity.type == 'Call'
    
    def test_activity_repr(self, app):
        """Test activity string representation."""
        with app.app_context():
            activity = Activity.query.first()
            assert str(activity) == f'<Activity {activity.subject}>'

class TestTerritoryModel:
    """Test cases for Territory model."""
    
    def test_territory_creation(self, app):
        """Test territory creation with valid data."""
        with app.app_context():
            territory = Territory(
                name='Test Territory',
                description='Test territory description',
                manager_id=1
            )
            db.session.add(territory)
            db.session.commit()
            
            assert territory.id is not None
            assert territory.name == 'Test Territory'
    
    def test_territory_repr(self, app):
        """Test territory string representation."""
        with app.app_context():
            territory = Territory.query.first()
            assert str(territory) == f'<Territory {territory.name}>'

class TestModelRelationships:
    """Test cases for model relationships."""
    
    def test_user_leads_relationship(self, app):
        """Test user-leads relationship."""
        with app.app_context():
            user = User.query.first()
            assert user.leads.count() >= 1
    
    def test_user_accounts_relationship(self, app):
        """Test user-accounts relationship."""
        with app.app_context():
            user = User.query.first()
            assert user.accounts.count() >= 1
    
    def test_account_contacts_relationship(self, app):
        """Test account-contacts relationship."""
        with app.app_context():
            account = Account.query.first()
            assert account.contacts.count() >= 1
    
    def test_lead_activities_relationship(self, app):
        """Test lead-activities relationship."""
        with app.app_context():
            lead = Lead.query.first()
            assert lead.activities.count() >= 1
    
    def test_opportunity_activities_relationship(self, app):
        """Test opportunity-activities relationship."""
        with app.app_context():
            opportunity = Opportunity.query.first()
            assert opportunity.activities.count() >= 1 
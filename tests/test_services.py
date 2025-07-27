import pytest
from app.services.lead_service import LeadService
from app.services.account_service import AccountService
from app.services.contact_service import ContactService
from app.services.opportunity_service import OpportunityService
from app.services.activity_service import ActivityService
from app.models.crm import Lead, Account, Contact, Opportunity, Activity, User

class TestLeadService:
    """Test cases for LeadService."""
    
    def test_create_lead(self, app):
        """Test lead creation through service."""
        with app.app_context():
            service = LeadService()
            
            lead_data = {
                'first_name': 'Service',
                'last_name': 'Lead',
                'email': 'servicelead@example.com',
                'phone': '+1-555-0999',
                'company': 'Service Company',
                'job_title': 'Manager',
                'industry': 'Technology',
                'source': 'Service',
                'status': 'New',
                'score': 80,
                'assigned_to': 1
            }
            
            lead = service.create_lead(lead_data)
            
            assert lead is not None
            assert lead.first_name == 'Service'
            assert lead.last_name == 'Lead'
            assert lead.email == 'servicelead@example.com'
    
    def test_get_lead_by_id(self, app):
        """Test getting lead by ID through service."""
        with app.app_context():
            service = LeadService()
            
            lead = service.get_lead_by_id(1)
            
            assert lead is not None
            assert lead.id == 1
    
    def test_get_all_leads(self, app):
        """Test getting all leads through service."""
        with app.app_context():
            service = LeadService()
            
            leads = service.get_all_leads()
            
            assert leads is not None
            assert len(leads) >= 1
    
    def test_update_lead(self, app):
        """Test lead update through service."""
        with app.app_context():
            service = LeadService()
            
            lead = service.get_lead_by_id(1)
            original_name = lead.first_name
            
            updated_data = {'first_name': 'Updated'}
            updated_lead = service.update_lead(1, updated_data)
            
            assert updated_lead.first_name == 'Updated'
            assert updated_lead.first_name != original_name
    
    def test_delete_lead(self, app):
        """Test lead deletion through service."""
        with app.app_context():
            service = LeadService()
            
            # Create a new lead to delete
            lead_data = {
                'first_name': 'Delete',
                'last_name': 'Lead',
                'email': 'deletelead@example.com',
                'assigned_to': 1
            }
            
            lead = service.create_lead(lead_data)
            lead_id = lead.id
            
            # Delete the lead
            result = service.delete_lead(lead_id)
            
            assert result == True
            
            # Verify lead is deleted
            deleted_lead = service.get_lead_by_id(lead_id)
            assert deleted_lead is None
    
    def test_search_leads(self, app):
        """Test lead search through service."""
        with app.app_context():
            service = LeadService()
            
            # Search by company name
            results = service.search_leads('Test Company')
            
            assert results is not None
            assert len(results) >= 1
    
    def test_get_leads_by_status(self, app):
        """Test getting leads by status through service."""
        with app.app_context():
            service = LeadService()
            
            new_leads = service.get_leads_by_status('New')
            
            assert new_leads is not None
            assert len(new_leads) >= 1

class TestAccountService:
    """Test cases for AccountService."""
    
    def test_create_account(self, app):
        """Test account creation through service."""
        with app.app_context():
            service = AccountService()
            
            account_data = {
                'name': 'Service Account',
                'industry': 'Technology',
                'website': 'www.serviceaccount.com',
                'phone': '+1-555-0004',
                'email': 'info@serviceaccount.com',
                'annual_revenue': 4000000,
                'employee_count': 100,
                'status': 'Active',
                'type': 'Customer',
                'assigned_to': 1,
                'territory_id': 1
            }
            
            account = service.create_account(account_data)
            
            assert account is not None
            assert account.name == 'Service Account'
            assert account.industry == 'Technology'
    
    def test_get_account_by_id(self, app):
        """Test getting account by ID through service."""
        with app.app_context():
            service = AccountService()
            
            account = service.get_account_by_id(1)
            
            assert account is not None
            assert account.id == 1
    
    def test_get_all_accounts(self, app):
        """Test getting all accounts through service."""
        with app.app_context():
            service = AccountService()
            
            accounts = service.get_all_accounts()
            
            assert accounts is not None
            assert len(accounts) >= 1
    
    def test_update_account(self, app):
        """Test account update through service."""
        with app.app_context():
            service = AccountService()
            
            account = service.get_account_by_id(1)
            original_name = account.name
            
            updated_data = {'name': 'Updated Account'}
            updated_account = service.update_account(1, updated_data)
            
            assert updated_account.name == 'Updated Account'
            assert updated_account.name != original_name
    
    def test_delete_account(self, app):
        """Test account deletion through service."""
        with app.app_context():
            service = AccountService()
            
            # Create a new account to delete
            account_data = {
                'name': 'Delete Account',
                'industry': 'Technology',
                'assigned_to': 1,
                'territory_id': 1
            }
            
            account = service.create_account(account_data)
            account_id = account.id
            
            # Delete the account
            result = service.delete_account(account_id)
            
            assert result == True
            
            # Verify account is deleted
            deleted_account = service.get_account_by_id(account_id)
            assert deleted_account is None
    
    def test_search_accounts(self, app):
        """Test account search through service."""
        with app.app_context():
            service = AccountService()
            
            # Search by name
            results = service.search_accounts('Test Company')
            
            assert results is not None
            assert len(results) >= 1
    
    def test_get_accounts_by_industry(self, app):
        """Test getting accounts by industry through service."""
        with app.app_context():
            service = AccountService()
            
            tech_accounts = service.get_accounts_by_industry('Technology')
            
            assert tech_accounts is not None
            assert len(tech_accounts) >= 1

class TestContactService:
    """Test cases for ContactService."""
    
    def test_create_contact(self, app):
        """Test contact creation through service."""
        with app.app_context():
            service = ContactService()
            
            contact_data = {
                'first_name': 'Service',
                'last_name': 'Contact',
                'email': 'servicecontact@example.com',
                'phone': '+1-555-0459',
                'job_title': 'Director',
                'department': 'Sales',
                'account_id': 1,
                'status': 'Active',
                'assigned_to': 1
            }
            
            contact = service.create_contact(contact_data)
            
            assert contact is not None
            assert contact.first_name == 'Service'
            assert contact.last_name == 'Contact'
    
    def test_get_contact_by_id(self, app):
        """Test getting contact by ID through service."""
        with app.app_context():
            service = ContactService()
            
            contact = service.get_contact_by_id(1)
            
            assert contact is not None
            assert contact.id == 1
    
    def test_get_all_contacts(self, app):
        """Test getting all contacts through service."""
        with app.app_context():
            service = ContactService()
            
            contacts = service.get_all_contacts()
            
            assert contacts is not None
            assert len(contacts) >= 1
    
    def test_update_contact(self, app):
        """Test contact update through service."""
        with app.app_context():
            service = ContactService()
            
            contact = service.get_contact_by_id(1)
            original_name = contact.first_name
            
            updated_data = {'first_name': 'Updated'}
            updated_contact = service.update_contact(1, updated_data)
            
            assert updated_contact.first_name == 'Updated'
            assert updated_contact.first_name != original_name
    
    def test_delete_contact(self, app):
        """Test contact deletion through service."""
        with app.app_context():
            service = ContactService()
            
            # Create a new contact to delete
            contact_data = {
                'first_name': 'Delete',
                'last_name': 'Contact',
                'email': 'deletecontact@example.com',
                'account_id': 1,
                'assigned_to': 1
            }
            
            contact = service.create_contact(contact_data)
            contact_id = contact.id
            
            # Delete the contact
            result = service.delete_contact(contact_id)
            
            assert result == True
            
            # Verify contact is deleted
            deleted_contact = service.get_contact_by_id(contact_id)
            assert deleted_contact is None
    
    def test_search_contacts(self, app):
        """Test contact search through service."""
        with app.app_context():
            service = ContactService()
            
            # Search by name
            results = service.search_contacts('Jane Smith')
            
            assert results is not None
            assert len(results) >= 1
    
    def test_get_contacts_by_account(self, app):
        """Test getting contacts by account through service."""
        with app.app_context():
            service = ContactService()
            
            account_contacts = service.get_contacts_by_account(1)
            
            assert account_contacts is not None
            assert len(account_contacts) >= 1

class TestOpportunityService:
    """Test cases for OpportunityService."""
    
    def test_create_opportunity(self, app):
        """Test opportunity creation through service."""
        with app.app_context():
            service = OpportunityService()
            
            opportunity_data = {
                'name': 'Service Opportunity',
                'account_id': 1,
                'contact_id': 1,
                'lead_id': 1,
                'stage': 'Prospecting',
                'amount': 125000,
                'probability': 50,
                'type': 'New Business',
                'source': 'Service',
                'description': 'Service opportunity description',
                'assigned_to': 1
            }
            
            opportunity = service.create_opportunity(opportunity_data)
            
            assert opportunity is not None
            assert opportunity.name == 'Service Opportunity'
            assert opportunity.amount == 125000
    
    def test_get_opportunity_by_id(self, app):
        """Test getting opportunity by ID through service."""
        with app.app_context():
            service = OpportunityService()
            
            opportunity = service.get_opportunity_by_id(1)
            
            assert opportunity is not None
            assert opportunity.id == 1
    
    def test_get_all_opportunities(self, app):
        """Test getting all opportunities through service."""
        with app.app_context():
            service = OpportunityService()
            
            opportunities = service.get_all_opportunities()
            
            assert opportunities is not None
            assert len(opportunities) >= 1
    
    def test_update_opportunity(self, app):
        """Test opportunity update through service."""
        with app.app_context():
            service = OpportunityService()
            
            opportunity = service.get_opportunity_by_id(1)
            original_name = opportunity.name
            
            updated_data = {'name': 'Updated Opportunity'}
            updated_opportunity = service.update_opportunity(1, updated_data)
            
            assert updated_opportunity.name == 'Updated Opportunity'
            assert updated_opportunity.name != original_name
    
    def test_delete_opportunity(self, app):
        """Test opportunity deletion through service."""
        with app.app_context():
            service = OpportunityService()
            
            # Create a new opportunity to delete
            opportunity_data = {
                'name': 'Delete Opportunity',
                'account_id': 1,
                'contact_id': 1,
                'lead_id': 1,
                'stage': 'Prospecting',
                'amount': 50000,
                'assigned_to': 1
            }
            
            opportunity = service.create_opportunity(opportunity_data)
            opportunity_id = opportunity.id
            
            # Delete the opportunity
            result = service.delete_opportunity(opportunity_id)
            
            assert result == True
            
            # Verify opportunity is deleted
            deleted_opportunity = service.get_opportunity_by_id(opportunity_id)
            assert deleted_opportunity is None
    
    def test_get_opportunities_by_stage(self, app):
        """Test getting opportunities by stage through service."""
        with app.app_context():
            service = OpportunityService()
            
            prospecting_opportunities = service.get_opportunities_by_stage('Prospecting')
            
            assert prospecting_opportunities is not None
            assert len(prospecting_opportunities) >= 1
    
    def test_calculate_pipeline_value(self, app):
        """Test pipeline value calculation through service."""
        with app.app_context():
            service = OpportunityService()
            
            pipeline_value = service.calculate_pipeline_value()
            
            assert pipeline_value is not None
            assert pipeline_value >= 0

class TestActivityService:
    """Test cases for ActivityService."""
    
    def test_create_activity(self, app):
        """Test activity creation through service."""
        with app.app_context():
            service = ActivityService()
            
            activity_data = {
                'subject': 'Service Activity',
                'type': 'Meeting',
                'status': 'Planned',
                'priority': 'High',
                'description': 'Service activity description',
                'account_id': 1,
                'contact_id': 1,
                'lead_id': 1,
                'opportunity_id': 1,
                'assigned_to': 1,
                'created_by': 1
            }
            
            activity = service.create_activity(activity_data)
            
            assert activity is not None
            assert activity.subject == 'Service Activity'
            assert activity.type == 'Meeting'
    
    def test_get_activity_by_id(self, app):
        """Test getting activity by ID through service."""
        with app.app_context():
            service = ActivityService()
            
            activity = service.get_activity_by_id(1)
            
            assert activity is not None
            assert activity.id == 1
    
    def test_get_all_activities(self, app):
        """Test getting all activities through service."""
        with app.app_context():
            service = ActivityService()
            
            activities = service.get_all_activities()
            
            assert activities is not None
            assert len(activities) >= 1
    
    def test_update_activity(self, app):
        """Test activity update through service."""
        with app.app_context():
            service = ActivityService()
            
            activity = service.get_activity_by_id(1)
            original_subject = activity.subject
            
            updated_data = {'subject': 'Updated Activity'}
            updated_activity = service.update_activity(1, updated_data)
            
            assert updated_activity.subject == 'Updated Activity'
            assert updated_activity.subject != original_subject
    
    def test_delete_activity(self, app):
        """Test activity deletion through service."""
        with app.app_context():
            service = ActivityService()
            
            # Create a new activity to delete
            activity_data = {
                'subject': 'Delete Activity',
                'type': 'Call',
                'status': 'Planned',
                'priority': 'Medium',
                'description': 'Delete activity description',
                'account_id': 1,
                'contact_id': 1,
                'lead_id': 1,
                'opportunity_id': 1,
                'assigned_to': 1,
                'created_by': 1
            }
            
            activity = service.create_activity(activity_data)
            activity_id = activity.id
            
            # Delete the activity
            result = service.delete_activity(activity_id)
            
            assert result == True
            
            # Verify activity is deleted
            deleted_activity = service.get_activity_by_id(activity_id)
            assert deleted_activity is None
    
    def test_get_activities_by_type(self, app):
        """Test getting activities by type through service."""
        with app.app_context():
            service = ActivityService()
            
            call_activities = service.get_activities_by_type('Call')
            
            assert call_activities is not None
            assert len(call_activities) >= 1
    
    def test_get_activities_by_status(self, app):
        """Test getting activities by status through service."""
        with app.app_context():
            service = ActivityService()
            
            planned_activities = service.get_activities_by_status('Planned')
            
            assert planned_activities is not None
            assert len(planned_activities) >= 1 
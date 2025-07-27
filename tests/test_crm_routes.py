import pytest
from app.models.crm import Lead, Account, Contact, Opportunity, Activity

class TestCRMRoutes:
    """Test cases for CRM routes."""
    
    def test_dashboard_requires_auth(self, client):
        """Test that dashboard requires authentication."""
        response = client.get('/crm/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_dashboard_accessible_when_authenticated(self, auth_client):
        """Test that dashboard is accessible when authenticated."""
        response = auth_client.get('/crm/dashboard')
        assert response.status_code == 200
        assert b'dashboard' in response.data.lower()
    
    def test_leads_list_requires_auth(self, client):
        """Test that leads list requires authentication."""
        response = client.get('/crm/leads')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_leads_list_accessible_when_authenticated(self, auth_client):
        """Test that leads list is accessible when authenticated."""
        response = auth_client.get('/crm/leads')
        assert response.status_code == 200
        assert b'leads' in response.data.lower()
    
    def test_create_lead_form_accessible(self, auth_client):
        """Test that create lead form is accessible."""
        response = auth_client.get('/crm/leads/create')
        assert response.status_code == 200
        assert b'create' in response.data.lower()
    
    def test_create_lead_success(self, auth_client):
        """Test successful lead creation."""
        response = auth_client.post('/crm/leads/create', data={
            'first_name': 'New',
            'last_name': 'Lead',
            'email': 'newlead@example.com',
            'phone': '+1-555-0999',
            'company': 'New Company',
            'job_title': 'Manager',
            'industry': 'Technology',
            'source': 'Website',
            'status': 'New'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_create_lead_missing_required_fields(self, auth_client):
        """Test lead creation with missing required fields."""
        response = auth_client.post('/crm/leads/create', data={
            'first_name': 'New',
            'last_name': 'Lead'
            # Missing email and other required fields
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should show validation error
    
    def test_lead_detail_accessible(self, auth_client):
        """Test that lead detail page is accessible."""
        response = auth_client.get('/crm/leads/1')
        assert response.status_code == 200
        assert b'lead' in response.data.lower()
    
    def test_accounts_list_requires_auth(self, client):
        """Test that accounts list requires authentication."""
        response = client.get('/crm/accounts')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_accounts_list_accessible_when_authenticated(self, auth_client):
        """Test that accounts list is accessible when authenticated."""
        response = auth_client.get('/crm/accounts')
        assert response.status_code == 200
        assert b'accounts' in response.data.lower()
    
    def test_create_account_form_accessible(self, auth_client):
        """Test that create account form is accessible."""
        response = auth_client.get('/crm/accounts/create')
        assert response.status_code == 200
        assert b'create' in response.data.lower()
    
    def test_create_account_success(self, auth_client):
        """Test successful account creation."""
        response = auth_client.post('/crm/accounts/create', data={
            'name': 'New Account',
            'industry': 'Technology',
            'website': 'www.newaccount.com',
            'phone': '+1-555-0002',
            'email': 'info@newaccount.com',
            'annual_revenue': 2000000,
            'employee_count': 25,
            'status': 'Active',
            'type': 'Customer'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_account_detail_accessible(self, auth_client):
        """Test that account detail page is accessible."""
        response = auth_client.get('/crm/accounts/1')
        assert response.status_code == 200
        assert b'account' in response.data.lower()
    
    def test_contacts_list_requires_auth(self, client):
        """Test that contacts list requires authentication."""
        response = client.get('/crm/contacts')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_contacts_list_accessible_when_authenticated(self, auth_client):
        """Test that contacts list is accessible when authenticated."""
        response = auth_client.get('/crm/contacts')
        assert response.status_code == 200
        assert b'contacts' in response.data.lower()
    
    def test_create_contact_form_accessible(self, auth_client):
        """Test that create contact form is accessible."""
        response = auth_client.get('/crm/contacts/create')
        assert response.status_code == 200
        assert b'create' in response.data.lower()
    
    def test_create_contact_success(self, auth_client):
        """Test successful contact creation."""
        response = auth_client.post('/crm/contacts/create', data={
            'first_name': 'New',
            'last_name': 'Contact',
            'email': 'newcontact@example.com',
            'phone': '+1-555-0457',
            'job_title': 'Director',
            'department': 'Sales',
            'account_id': 1,
            'status': 'Active'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_contact_detail_accessible(self, auth_client):
        """Test that contact detail page is accessible."""
        response = auth_client.get('/crm/contacts/1')
        assert response.status_code == 200
        assert b'contact' in response.data.lower()
    
    def test_opportunities_list_requires_auth(self, client):
        """Test that opportunities list requires authentication."""
        response = client.get('/crm/opportunities')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_opportunities_list_accessible_when_authenticated(self, auth_client):
        """Test that opportunities list is accessible when authenticated."""
        response = auth_client.get('/crm/opportunities')
        assert response.status_code == 200
        assert b'opportunities' in response.data.lower()
    
    def test_create_opportunity_form_accessible(self, auth_client):
        """Test that create opportunity form is accessible."""
        response = auth_client.get('/crm/opportunities/create')
        assert response.status_code == 200
        assert b'create' in response.data.lower()
    
    def test_create_opportunity_success(self, auth_client):
        """Test successful opportunity creation."""
        response = auth_client.post('/crm/opportunities/create', data={
            'name': 'New Opportunity',
            'account_id': 1,
            'contact_id': 1,
            'lead_id': 1,
            'stage': 'Prospecting',
            'amount': 75000,
            'probability': 30,
            'type': 'New Business',
            'source': 'Website',
            'description': 'New opportunity description'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_opportunity_detail_accessible(self, auth_client):
        """Test that opportunity detail page is accessible."""
        response = auth_client.get('/crm/opportunities/1')
        assert response.status_code == 200
        assert b'opportunity' in response.data.lower()
    
    def test_activities_list_requires_auth(self, client):
        """Test that activities list requires authentication."""
        response = client.get('/crm/activities')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_activities_list_accessible_when_authenticated(self, auth_client):
        """Test that activities list is accessible when authenticated."""
        response = auth_client.get('/crm/activities')
        assert response.status_code == 200
        assert b'activities' in response.data.lower()
    
    def test_create_activity_form_accessible(self, auth_client):
        """Test that create activity form is accessible."""
        response = auth_client.get('/crm/activities/create')
        assert response.status_code == 200
        assert b'create' in response.data.lower()
    
    def test_create_activity_success(self, auth_client):
        """Test successful activity creation."""
        response = auth_client.post('/crm/activities/create', data={
            'subject': 'New Activity',
            'type': 'Meeting',
            'status': 'Planned',
            'priority': 'High',
            'description': 'New activity description',
            'account_id': 1,
            'contact_id': 1,
            'lead_id': 1,
            'opportunity_id': 1
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_activity_detail_accessible(self, auth_client):
        """Test that activity detail page is accessible."""
        response = auth_client.get('/crm/activities/1')
        assert response.status_code == 200
        assert b'activity' in response.data.lower()
    
    def test_reports_requires_auth(self, client):
        """Test that reports require authentication."""
        response = client.get('/crm/reports')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_reports_accessible_when_authenticated(self, auth_client):
        """Test that reports are accessible when authenticated."""
        response = auth_client.get('/crm/reports')
        assert response.status_code == 200
        assert b'reports' in response.data.lower()
    
    def test_settings_requires_auth(self, client):
        """Test that settings require authentication."""
        response = client.get('/crm/settings')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_settings_accessible_when_authenticated(self, auth_client):
        """Test that settings are accessible when authenticated."""
        response = auth_client.get('/crm/settings')
        assert response.status_code == 200
        assert b'settings' in response.data.lower() 
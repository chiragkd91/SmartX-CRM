import pytest
import json
from app.models.crm import Lead, Account, Contact, Opportunity, Activity

class TestAPIRoutes:
    """Test cases for API routes."""
    
    def test_api_docs_requires_auth(self, client):
        """Test that API docs require authentication."""
        response = client.get('/api/docs')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_api_docs_accessible_when_authenticated(self, auth_client):
        """Test that API docs are accessible when authenticated."""
        response = auth_client.get('/api/docs')
        assert response.status_code == 200
        assert b'api' in response.data.lower()
    
    def test_api_dashboard_requires_auth(self, client):
        """Test that API dashboard requires authentication."""
        response = client.get('/api/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_api_dashboard_accessible_when_authenticated(self, auth_client):
        """Test that API dashboard is accessible when authenticated."""
        response = auth_client.get('/api/dashboard')
        assert response.status_code == 200
        assert b'dashboard' in response.data.lower()
    
    def test_api_leads_endpoint_requires_auth(self, client):
        """Test that API leads endpoint requires authentication."""
        response = client.get('/api/leads')
        assert response.status_code == 401
    
    def test_api_leads_endpoint_accessible_when_authenticated(self, auth_client):
        """Test that API leads endpoint is accessible when authenticated."""
        response = auth_client.get('/api/leads')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'leads' in data
    
    def test_api_create_lead_requires_auth(self, client):
        """Test that API create lead requires authentication."""
        response = client.post('/api/leads', json={
            'first_name': 'API',
            'last_name': 'Lead',
            'email': 'apilead@example.com'
        })
        assert response.status_code == 401
    
    def test_api_create_lead_success(self, auth_client):
        """Test successful API lead creation."""
        response = auth_client.post('/api/leads', json={
            'first_name': 'API',
            'last_name': 'Lead',
            'email': 'apilead@example.com',
            'phone': '+1-555-0999',
            'company': 'API Company',
            'job_title': 'Manager',
            'industry': 'Technology',
            'source': 'API',
            'status': 'New'
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['first_name'] == 'API'
        assert data['last_name'] == 'Lead'
    
    def test_api_create_lead_missing_required_fields(self, auth_client):
        """Test API lead creation with missing required fields."""
        response = auth_client.post('/api/leads', json={
            'first_name': 'API',
            'last_name': 'Lead'
            # Missing email
        })
        assert response.status_code == 400
    
    def test_api_get_lead_requires_auth(self, client):
        """Test that API get lead requires authentication."""
        response = client.get('/api/leads/1')
        assert response.status_code == 401
    
    def test_api_get_lead_success(self, auth_client):
        """Test successful API get lead."""
        response = auth_client.get('/api/leads/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'id' in data
        assert 'first_name' in data
    
    def test_api_get_lead_not_found(self, auth_client):
        """Test API get lead with non-existent ID."""
        response = auth_client.get('/api/leads/999')
        assert response.status_code == 404
    
    def test_api_update_lead_requires_auth(self, client):
        """Test that API update lead requires authentication."""
        response = client.put('/api/leads/1', json={
            'first_name': 'Updated'
        })
        assert response.status_code == 401
    
    def test_api_update_lead_success(self, auth_client):
        """Test successful API lead update."""
        response = auth_client.put('/api/leads/1', json={
            'first_name': 'Updated',
            'last_name': 'Lead'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['first_name'] == 'Updated'
    
    def test_api_delete_lead_requires_auth(self, client):
        """Test that API delete lead requires authentication."""
        response = client.delete('/api/leads/1')
        assert response.status_code == 401
    
    def test_api_delete_lead_success(self, auth_client):
        """Test successful API lead deletion."""
        response = auth_client.delete('/api/leads/1')
        assert response.status_code == 204
    
    def test_api_accounts_endpoint_requires_auth(self, client):
        """Test that API accounts endpoint requires authentication."""
        response = client.get('/api/accounts')
        assert response.status_code == 401
    
    def test_api_accounts_endpoint_accessible_when_authenticated(self, auth_client):
        """Test that API accounts endpoint is accessible when authenticated."""
        response = auth_client.get('/api/accounts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'accounts' in data
    
    def test_api_create_account_success(self, auth_client):
        """Test successful API account creation."""
        response = auth_client.post('/api/accounts', json={
            'name': 'API Account',
            'industry': 'Technology',
            'website': 'www.apiaccount.com',
            'phone': '+1-555-0003',
            'email': 'info@apiaccount.com',
            'annual_revenue': 3000000,
            'employee_count': 75,
            'status': 'Active',
            'type': 'Customer'
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'API Account'
    
    def test_api_contacts_endpoint_requires_auth(self, client):
        """Test that API contacts endpoint requires authentication."""
        response = client.get('/api/contacts')
        assert response.status_code == 401
    
    def test_api_contacts_endpoint_accessible_when_authenticated(self, auth_client):
        """Test that API contacts endpoint is accessible when authenticated."""
        response = auth_client.get('/api/contacts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'contacts' in data
    
    def test_api_create_contact_success(self, auth_client):
        """Test successful API contact creation."""
        response = auth_client.post('/api/contacts', json={
            'first_name': 'API',
            'last_name': 'Contact',
            'email': 'apicontact@example.com',
            'phone': '+1-555-0458',
            'job_title': 'Director',
            'department': 'Sales',
            'account_id': 1,
            'status': 'Active'
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['first_name'] == 'API'
        assert data['last_name'] == 'Contact'
    
    def test_api_opportunities_endpoint_requires_auth(self, client):
        """Test that API opportunities endpoint requires authentication."""
        response = client.get('/api/opportunities')
        assert response.status_code == 401
    
    def test_api_opportunities_endpoint_accessible_when_authenticated(self, auth_client):
        """Test that API opportunities endpoint is accessible when authenticated."""
        response = auth_client.get('/api/opportunities')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'opportunities' in data
    
    def test_api_create_opportunity_success(self, auth_client):
        """Test successful API opportunity creation."""
        response = auth_client.post('/api/opportunities', json={
            'name': 'API Opportunity',
            'account_id': 1,
            'contact_id': 1,
            'lead_id': 1,
            'stage': 'Prospecting',
            'amount': 100000,
            'probability': 40,
            'type': 'New Business',
            'source': 'API',
            'description': 'API opportunity description'
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'API Opportunity'
    
    def test_api_activities_endpoint_requires_auth(self, client):
        """Test that API activities endpoint requires authentication."""
        response = client.get('/api/activities')
        assert response.status_code == 401
    
    def test_api_activities_endpoint_accessible_when_authenticated(self, auth_client):
        """Test that API activities endpoint is accessible when authenticated."""
        response = auth_client.get('/api/activities')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'activities' in data
    
    def test_api_create_activity_success(self, auth_client):
        """Test successful API activity creation."""
        response = auth_client.post('/api/activities', json={
            'subject': 'API Activity',
            'type': 'Meeting',
            'status': 'Planned',
            'priority': 'High',
            'description': 'API activity description',
            'account_id': 1,
            'contact_id': 1,
            'lead_id': 1,
            'opportunity_id': 1
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['subject'] == 'API Activity'
    
    def test_api_invalid_json(self, auth_client):
        """Test API with invalid JSON."""
        response = auth_client.post('/api/leads', 
                                  data='invalid json',
                                  content_type='application/json')
        assert response.status_code == 400
    
    def test_api_method_not_allowed(self, auth_client):
        """Test API with method not allowed."""
        response = auth_client.patch('/api/leads/1')
        assert response.status_code == 405 
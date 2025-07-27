"""
CRM SDK for CRM System
Software development kit for integrations
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import hmac

class CRMSDK:
    """Software development kit for CRM system integrations"""
    
    def __init__(self, api_key: str = None, base_url: str = "http://localhost:5000/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'CRM-SDK/1.0.0'
        })
        
        if api_key:
            self.session.headers['X-API-Key'] = api_key
    
    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate and get access token"""
        try:
            response = self.session.post(f"{self.base_url}/auth/login", json={
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('token')
                if token:
                    self.session.headers['Authorization'] = f'Bearer {token}'
                    return {'success': True, 'token': token}
                else:
                    return {'success': False, 'error': 'No token received'}
            else:
                return {'success': False, 'error': f'Authentication failed: {response.status_code}'}
                
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.session.headers['Authorization'] = f'Bearer {token}'
    
    # Contact Management
    def get_contacts(self, page: int = 1, limit: int = 20, filters: Dict = None) -> Dict[str, Any]:
        """Get list of contacts"""
        try:
            params = {'page': page, 'limit': limit}
            if filters:
                params.update(filters)
            
            response = self.session.get(f"{self.base_url}/contacts", params=params)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting contacts: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_contact(self, contact_id: int) -> Dict[str, Any]:
        """Get contact by ID"""
        try:
            response = self.session.get(f"{self.base_url}/contacts/{contact_id}")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting contact: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new contact"""
        try:
            response = self.session.post(f"{self.base_url}/contacts", json=contact_data)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error creating contact: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def update_contact(self, contact_id: int, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update contact"""
        try:
            response = self.session.put(f"{self.base_url}/contacts/{contact_id}", json=contact_data)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error updating contact: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def delete_contact(self, contact_id: int) -> Dict[str, Any]:
        """Delete contact"""
        try:
            response = self.session.delete(f"{self.base_url}/contacts/{contact_id}")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error deleting contact: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    # Lead Management
    def get_leads(self, page: int = 1, limit: int = 20, filters: Dict = None) -> Dict[str, Any]:
        """Get list of leads"""
        try:
            params = {'page': page, 'limit': limit}
            if filters:
                params.update(filters)
            
            response = self.session.get(f"{self.base_url}/leads", params=params)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting leads: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_lead(self, lead_id: int) -> Dict[str, Any]:
        """Get lead by ID"""
        try:
            response = self.session.get(f"{self.base_url}/leads/{lead_id}")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting lead: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new lead"""
        try:
            response = self.session.post(f"{self.base_url}/leads", json=lead_data)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error creating lead: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def update_lead(self, lead_id: int, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update lead"""
        try:
            response = self.session.put(f"{self.base_url}/leads/{lead_id}", json=lead_data)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error updating lead: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def delete_lead(self, lead_id: int) -> Dict[str, Any]:
        """Delete lead"""
        try:
            response = self.session.delete(f"{self.base_url}/leads/{lead_id}")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error deleting lead: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    # Opportunity Management
    def get_opportunities(self, page: int = 1, limit: int = 20, filters: Dict = None) -> Dict[str, Any]:
        """Get list of opportunities"""
        try:
            params = {'page': page, 'limit': limit}
            if filters:
                params.update(filters)
            
            response = self.session.get(f"{self.base_url}/opportunities", params=params)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting opportunities: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_opportunity(self, opportunity_id: int) -> Dict[str, Any]:
        """Get opportunity by ID"""
        try:
            response = self.session.get(f"{self.base_url}/opportunities/{opportunity_id}")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting opportunity: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_opportunity(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new opportunity"""
        try:
            response = self.session.post(f"{self.base_url}/opportunities", json=opportunity_data)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error creating opportunity: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def update_opportunity(self, opportunity_id: int, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update opportunity"""
        try:
            response = self.session.put(f"{self.base_url}/opportunities/{opportunity_id}", json=opportunity_data)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error updating opportunity: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def delete_opportunity(self, opportunity_id: int) -> Dict[str, Any]:
        """Delete opportunity"""
        try:
            response = self.session.delete(f"{self.base_url}/opportunities/{opportunity_id}")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error deleting opportunity: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    # Analytics and Reports
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        try:
            response = self.session.get(f"{self.base_url}/analytics/dashboard")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard stats: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_sales_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Get sales report"""
        try:
            params = {}
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
            
            response = self.session.get(f"{self.base_url}/analytics/sales", params=params)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting sales report: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_lead_analytics(self, period: str = "30d") -> Dict[str, Any]:
        """Get lead analytics"""
        try:
            response = self.session.get(f"{self.base_url}/analytics/leads", params={'period': period})
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting lead analytics: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    # File Upload
    def upload_file(self, file_path: str, file_type: str = "document") -> Dict[str, Any]:
        """Upload file"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'type': file_type}
                response = self.session.post(f"{self.base_url}/files/upload", files=files, data=data)
                return self._handle_response(response)
                
        except Exception as e:
            self.logger.error(f"Error uploading file: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    # Webhook Management
    def create_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create webhook"""
        try:
            response = self.session.post(f"{self.base_url}/webhooks", json=webhook_data)
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error creating webhook: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_webhooks(self) -> Dict[str, Any]:
        """Get webhooks"""
        try:
            response = self.session.get(f"{self.base_url}/webhooks")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting webhooks: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def delete_webhook(self, webhook_id: int) -> Dict[str, Any]:
        """Delete webhook"""
        try:
            response = self.session.delete(f"{self.base_url}/webhooks/{webhook_id}")
            return self._handle_response(response)
            
        except Exception as e:
            self.logger.error(f"Error deleting webhook: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    # Utility Methods
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            if response.status_code in [200, 201]:
                return {'success': True, 'data': response.json()}
            elif response.status_code == 401:
                return {'success': False, 'error': 'Unauthorized - check your API key or token'}
            elif response.status_code == 403:
                return {'success': False, 'error': 'Forbidden - insufficient permissions'}
            elif response.status_code == 404:
                return {'success': False, 'error': 'Resource not found'}
            elif response.status_code == 429:
                return {'success': False, 'error': 'Rate limit exceeded'}
            elif response.status_code >= 500:
                return {'success': False, 'error': 'Server error'}
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}: {response.text}'}
                
        except json.JSONDecodeError:
            return {'success': False, 'error': 'Invalid JSON response'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def set_timeout(self, timeout: int):
        """Set request timeout"""
        self.session.timeout = timeout
    
    def set_retry_policy(self, max_retries: int = 3, backoff_factor: float = 0.3):
        """Set retry policy"""
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def enable_logging(self, level: str = "INFO"):
        """Enable SDK logging"""
        logging.basicConfig(level=getattr(logging, level.upper()))
    
    def get_sdk_info(self) -> Dict[str, Any]:
        """Get SDK information"""
        return {
            'version': '1.0.0',
            'base_url': self.base_url,
            'has_auth': bool(self.session.headers.get('Authorization') or self.session.headers.get('X-API-Key')),
            'timeout': getattr(self.session, 'timeout', None)
        }

# Example usage and documentation
class CRMClient:
    """High-level client for common CRM operations"""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:5000/api/v1"):
        self.sdk = CRMSDK(api_key, base_url)
    
    def sync_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sync contact data"""
        email = contact_data.get('email')
        if not email:
            return {'success': False, 'error': 'Email is required'}
        
        # Check if contact exists
        contacts = self.sdk.get_contacts(filters={'email': email})
        if contacts.get('success') and contacts['data'].get('contacts'):
            # Update existing contact
            contact_id = contacts['data']['contacts'][0]['id']
            return self.sdk.update_contact(contact_id, contact_data)
        else:
            # Create new contact
            return self.sdk.create_contact(contact_data)
    
    def convert_lead_to_contact(self, lead_id: int) -> Dict[str, Any]:
        """Convert lead to contact"""
        # Get lead data
        lead = self.sdk.get_lead(lead_id)
        if not lead.get('success'):
            return lead
        
        lead_data = lead['data']
        
        # Create contact from lead data
        contact_data = {
            'first_name': lead_data.get('first_name', ''),
            'last_name': lead_data.get('last_name', ''),
            'email': lead_data.get('email'),
            'phone': lead_data.get('phone', ''),
            'company': lead_data.get('company', ''),
            'source': lead_data.get('source', 'lead_conversion')
        }
        
        # Create contact
        contact_result = self.sdk.create_contact(contact_data)
        if contact_result.get('success'):
            # Delete the lead
            self.sdk.delete_lead(lead_id)
        
        return contact_result
    
    def get_contact_opportunities(self, contact_id: int) -> Dict[str, Any]:
        """Get opportunities for a contact"""
        return self.sdk.get_opportunities(filters={'contact_id': contact_id})
    
    def create_opportunity_from_contact(self, contact_id: int, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create opportunity for a contact"""
        opportunity_data['contact_id'] = contact_id
        return self.sdk.create_opportunity(opportunity_data) 
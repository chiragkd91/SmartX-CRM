"""
API Testing Tool for CRM System
API testing utilities and test runner
"""

import requests
import json
import logging
from typing import Dict, Any

class APITestingTool:
    """API testing utilities for CRM endpoints"""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
    def run_test(self, endpoint: str, method: str = 'GET', data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Dict[str, Any]:
        url = self.base_url + endpoint
        try:
            if method == 'GET':
                resp = requests.get(url, headers=headers)
            elif method == 'POST':
                resp = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                resp = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                resp = requests.delete(url, headers=headers)
            else:
                return {'error': 'Unsupported HTTP method'}
            return {
                'status_code': resp.status_code,
                'response': resp.json() if resp.headers.get('Content-Type', '').startswith('application/json') else resp.text
            }
        except Exception as e:
            self.logger.error(f"API test failed: {str(e)}")
            return {'error': str(e)} 
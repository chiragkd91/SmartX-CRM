"""
Input Validator for CRM System
Advanced input validation and sanitization
"""

import re
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

class InputValidator:
    """Advanced input validation and sanitization system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_rules = self._load_validation_rules()
    
    def validate_user_input(self, data: Dict[str, Any], input_type: str = 'general') -> Dict[str, Any]:
        """Validate and sanitize user input"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'sanitized_data': {},
            'warnings': []
        }
        
        try:
            if input_type == 'form':
                validation_result = self._validate_form_data(data)
            elif input_type == 'api':
                validation_result = self._validate_api_data(data)
            elif input_type == 'file':
                validation_result = self._validate_file_upload(data)
            else:
                validation_result = self._validate_general_data(data)
                
        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
            self.logger.error(f"Input validation failed: {str(e)}")
        
        return validation_result
    
    def _validate_form_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate form data"""
        result = {'is_valid': True, 'errors': [], 'sanitized_data': {}, 'warnings': []}
        
        for field, value in data.items():
            if field in self.validation_rules['form']:
                field_result = self._validate_field(value, self.validation_rules['form'][field])
                if not field_result['is_valid']:
                    result['is_valid'] = False
                    result['errors'].extend(field_result['errors'])
                else:
                    result['sanitized_data'][field] = field_result['sanitized_value']
        
        return result
    
    def _validate_api_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate API data"""
        result = {'is_valid': True, 'errors': [], 'sanitized_data': {}, 'warnings': []}
        
        for field, value in data.items():
            if field in self.validation_rules['api']:
                field_result = self._validate_field(value, self.validation_rules['api'][field])
                if not field_result['is_valid']:
                    result['is_valid'] = False
                    result['errors'].extend(field_result['errors'])
                else:
                    result['sanitized_data'][field] = field_result['sanitized_value']
        
        return result
    
    def _validate_file_upload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate file upload"""
        result = {'is_valid': True, 'errors': [], 'sanitized_data': {}, 'warnings': []}
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
        if data.get('content_type') not in allowed_types:
            result['is_valid'] = False
            result['errors'].append("Invalid file type")
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if data.get('size', 0) > max_size:
            result['is_valid'] = False
            result['errors'].append("File too large")
        
        return result
    
    def _validate_general_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate general data"""
        result = {'is_valid': True, 'errors': [], 'sanitized_data': {}, 'warnings': []}
        
        for field, value in data.items():
            field_result = self._validate_field(value, self.validation_rules['general'])
            if not field_result['is_valid']:
                result['is_valid'] = False
                result['errors'].extend(field_result['errors'])
            else:
                result['sanitized_data'][field] = field_result['sanitized_value']
        
        return result
    
    def _validate_field(self, value: Any, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Validate individual field"""
        result = {'is_valid': True, 'errors': [], 'sanitized_value': value}
        
        # Check required
        if rules.get('required', False) and not value:
            result['is_valid'] = False
            result['errors'].append("Field is required")
            return result
        
        # Check type
        if 'type' in rules:
            if not self._validate_type(value, rules['type']):
                result['is_valid'] = False
                result['errors'].append(f"Invalid type. Expected {rules['type']}")
        
        # Check length
        if 'min_length' in rules and len(str(value)) < rules['min_length']:
            result['is_valid'] = False
            result['errors'].append(f"Minimum length is {rules['min_length']}")
        
        if 'max_length' in rules and len(str(value)) > rules['max_length']:
            result['is_valid'] = False
            result['errors'].append(f"Maximum length is {rules['max_length']}")
        
        # Check pattern
        if 'pattern' in rules:
            if not re.match(rules['pattern'], str(value)):
                result['is_valid'] = False
                result['errors'].append("Invalid format")
        
        # Sanitize if valid
        if result['is_valid']:
            result['sanitized_value'] = self._sanitize_value(value, rules)
        
        return result
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate data type"""
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'integer':
            return isinstance(value, int) or (isinstance(value, str) and value.isdigit())
        elif expected_type == 'email':
            return self._is_valid_email(value)
        elif expected_type == 'url':
            return self._is_valid_url(value)
        elif expected_type == 'date':
            return self._is_valid_date(value)
        return True
    
    def _sanitize_value(self, value: Any, rules: Dict[str, Any]) -> Any:
        """Sanitize input value"""
        if isinstance(value, str):
            # Remove HTML tags
            value = re.sub(r'<[^>]+>', '', value)
            
            # Remove script tags
            value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove dangerous characters
            value = value.replace('javascript:', '').replace('vbscript:', '')
            
            # Trim whitespace
            value = value.strip()
        
        return value
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Validate date format"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules"""
        return {
            'form': {
                'email': {'type': 'email', 'required': True, 'max_length': 255},
                'password': {'type': 'string', 'required': True, 'min_length': 8, 'max_length': 128},
                'name': {'type': 'string', 'required': True, 'max_length': 100},
                'phone': {'type': 'string', 'pattern': r'^\+?[\d\s\-\(\)]+$', 'max_length': 20},
                'url': {'type': 'url', 'max_length': 255}
            },
            'api': {
                'id': {'type': 'integer', 'required': True},
                'data': {'type': 'string', 'max_length': 10000},
                'timestamp': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'}
            },
            'general': {
                'type': 'string',
                'max_length': 1000
            }
        }
    
    def add_validation_rule(self, rule_name: str, rule_config: Dict[str, Any]):
        """Add custom validation rule"""
        self.validation_rules['custom'][rule_name] = rule_config
        self.logger.info(f"Added validation rule: {rule_name}")
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Get current validation rules"""
        return self.validation_rules 
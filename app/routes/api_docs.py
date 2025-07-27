"""
API Documentation & Testing Routes for CRM System
Integration of API documentation and testing tools
"""

from flask import Blueprint, request, jsonify, render_template, current_app
from app.api.documentation import APIDocumentation
from app.api.testing_tool import APITestingTool
import logging
import json

bp = Blueprint('api_docs', __name__, url_prefix='/api/docs')

# Initialize API documentation and testing services
api_docs = APIDocumentation()
api_tester = APITestingTool('http://localhost:5000')  # Base URL for testing

@bp.route('/')
def api_documentation():
    """Serve API documentation"""
    try:
        docs = api_docs.get_docs()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': docs
            })
        else:
            return render_template('api/docs.html', docs=docs)
            
    except Exception as e:
        logging.error(f"API documentation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/swagger')
def swagger_ui():
    """Serve Swagger UI"""
    try:
        docs = api_docs.get_docs()
        return render_template('api/swagger_ui.html', docs=docs)
        
    except Exception as e:
        logging.error(f"Swagger UI failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/test', methods=['GET', 'POST'])
def api_test():
    """API testing interface"""
    try:
        if request.method == 'POST':
            endpoint = request.form.get('endpoint', '/')
            method = request.form.get('method', 'GET')
            data = request.form.get('data', '{}')
            headers = request.form.get('headers', '{}')
            
            # Parse JSON data and headers
            try:
                data_dict = json.loads(data) if data else {}
                headers_dict = json.loads(headers) if headers else {}
            except json.JSONDecodeError:
                return jsonify({'success': False, 'error': 'Invalid JSON format'})
            
            # Run API test
            test_result = api_tester.run_test(endpoint, method, data_dict, headers_dict)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': test_result
                })
            else:
                return render_template('api/test_results.html', 
                                     test_result=test_result)
        else:
            return render_template('api/test_form.html')
            
    except Exception as e:
        logging.error(f"API testing failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/endpoints')
def list_endpoints():
    """List all available API endpoints"""
    try:
        # Get all registered routes
        routes = []
        for rule in current_app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': str(rule)
            })
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': routes
            })
        else:
            return render_template('api/endpoints.html', routes=routes)
            
    except Exception as e:
        logging.error(f"Endpoint listing failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/examples')
def api_examples():
    """Show API usage examples"""
    try:
        examples = {
            'contacts': {
                'get_contacts': {
                    'method': 'GET',
                    'endpoint': '/crm/contacts',
                    'description': 'Get all contacts'
                },
                'create_contact': {
                    'method': 'POST',
                    'endpoint': '/crm/contacts',
                    'description': 'Create a new contact',
                    'data': {
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'email': 'john.doe@example.com'
                    }
                }
            },
            'leads': {
                'get_leads': {
                    'method': 'GET',
                    'endpoint': '/crm/leads',
                    'description': 'Get all leads'
                },
                'create_lead': {
                    'method': 'POST',
                    'endpoint': '/crm/leads',
                    'description': 'Create a new lead',
                    'data': {
                        'name': 'New Lead',
                        'email': 'lead@example.com',
                        'source': 'website'
                    }
                }
            }
        }
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': examples
            })
        else:
            return render_template('api/examples.html', examples=examples)
            
    except Exception as e:
        logging.error(f"API examples failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/download')
def download_docs():
    """Download API documentation"""
    try:
        docs = api_docs.get_docs()
        format_type = request.args.get('format', 'json')
        
        if format_type == 'json':
            return jsonify(docs)
        elif format_type == 'yaml':
            # Convert to YAML (would need PyYAML)
            return jsonify({'error': 'YAML format not implemented'})
        else:
            return jsonify({'error': 'Unsupported format'})
            
    except Exception as e:
        logging.error(f"Documentation download failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
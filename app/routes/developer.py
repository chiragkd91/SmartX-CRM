"""
Developer Portal Routes for CRM System
Integration of developer portal and SDK features
"""

from flask import Blueprint, request, jsonify, render_template
from app.developer.developer_portal import DeveloperPortal
from app.sdk.crm_sdk import CRMSDK
import logging

bp = Blueprint('developer', __name__, url_prefix='/developer')

# Initialize developer services
developer_portal = DeveloperPortal()
crm_sdk = CRMSDK('http://localhost:5000')  # Base URL for SDK

@bp.route('/')
def developer_home():
    """Developer portal home page"""
    try:
        portal_data = {
            'documentation': developer_portal.get_documentation(),
            'tutorials': developer_portal.get_tutorials(),
            'resources': developer_portal.get_developer_resources()
        }
        
        return render_template('developer/home.html', portal_data=portal_data)
        
    except Exception as e:
        logging.error(f"Developer home failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/docs')
def documentation():
    """Documentation page"""
    try:
        section = request.args.get('section')
        docs = developer_portal.get_documentation(section)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': docs
            })
        else:
            return render_template('developer/documentation.html', docs=docs)
            
    except Exception as e:
        logging.error(f"Documentation retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/examples')
def code_examples():
    """Code examples page"""
    try:
        language = request.args.get('language')
        examples = developer_portal.get_code_examples(language)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': examples
            })
        else:
            return render_template('developer/examples.html', examples=examples)
            
    except Exception as e:
        logging.error(f"Code examples retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api-reference')
def api_reference():
    """API reference page"""
    try:
        endpoint = request.args.get('endpoint')
        api_ref = developer_portal.get_api_reference(endpoint)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': api_ref
            })
        else:
            return render_template('developer/api_reference.html', api_ref=api_ref)
            
    except Exception as e:
        logging.error(f"API reference retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/tutorials')
def tutorials():
    """Tutorials page"""
    try:
        difficulty = request.args.get('difficulty')
        tutorials_data = developer_portal.get_tutorials(difficulty)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': tutorials_data
            })
        else:
            return render_template('developer/tutorials.html', tutorials=tutorials_data)
            
    except Exception as e:
        logging.error(f"Tutorials retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/search')
def search_documentation():
    """Search documentation"""
    try:
        query = request.args.get('q', '')
        results = developer_portal.search_documentation(query)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': results
            })
        else:
            return render_template('developer/search_results.html', 
                                 query=query, 
                                 results=results)
            
    except Exception as e:
        logging.error(f"Documentation search failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/resources')
def developer_resources():
    """Developer resources page"""
    try:
        resources = developer_portal.get_developer_resources()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': resources
            })
        else:
            return render_template('developer/resources.html', resources=resources)
            
    except Exception as e:
        logging.error(f"Developer resources retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/sdk')
def sdk_documentation():
    """SDK documentation page"""
    try:
        sdk_info = crm_sdk.get_sdk_info()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': sdk_info
            })
        else:
            return render_template('developer/sdk.html', sdk_info=sdk_info)
            
    except Exception as e:
        logging.error(f"SDK documentation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/sdk/test')
def test_sdk():
    """Test SDK connection"""
    try:
        connection_test = crm_sdk.test_connection()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': {'connected': connection_test}
            })
        else:
            return render_template('developer/sdk_test.html', 
                                 connected=connection_test)
            
    except Exception as e:
        logging.error(f"SDK test failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api-docs/openapi')
def openapi_spec():
    """Get OpenAPI specification"""
    try:
        openapi_spec = developer_portal.generate_api_docs()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': openapi_spec
            })
        else:
            return openapi_spec, 200, {'Content-Type': 'application/json'}
            
    except Exception as e:
        logging.error(f"OpenAPI spec generation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/downloads/<sdk_type>')
def download_sdk(sdk_type):
    """Download SDK"""
    try:
        resources = developer_portal.get_developer_resources()
        sdk_downloads = resources.get('sdk_downloads', {})
        
        if sdk_type in sdk_downloads:
            download_info = sdk_downloads[sdk_type]
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': download_info
                })
            else:
                return render_template('developer/download.html', 
                                     sdk_type=sdk_type, 
                                     download_info=download_info)
        else:
            return jsonify({'success': False, 'error': 'SDK not found'})
            
    except Exception as e:
        logging.error(f"SDK download failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/webhooks')
def webhook_documentation():
    """Webhook documentation"""
    try:
        resources = developer_portal.get_developer_resources()
        webhooks = resources.get('webhooks', {})
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': webhooks
            })
        else:
            return render_template('developer/webhooks.html', webhooks=webhooks)
            
    except Exception as e:
        logging.error(f"Webhook documentation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/rate-limits')
def rate_limits():
    """Rate limits documentation"""
    try:
        resources = developer_portal.get_developer_resources()
        rate_limits = resources.get('rate_limits', {})
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': rate_limits
            })
        else:
            return render_template('developer/rate_limits.html', rate_limits=rate_limits)
            
    except Exception as e:
        logging.error(f"Rate limits documentation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/dashboard')
def developer_dashboard():
    """Developer dashboard"""
    try:
        dashboard_data = {
            'sdk_info': crm_sdk.get_sdk_info(),
            'api_info': crm_sdk.get_api_info(),
            'resources': developer_portal.get_developer_resources(),
            'tutorials_count': len(developer_portal.get_tutorials()),
            'examples_count': len(developer_portal.get_code_examples())
        }
        
        return render_template('developer/dashboard.html', 
                             dashboard_data=dashboard_data)
                             
    except Exception as e:
        logging.error(f"Developer dashboard failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
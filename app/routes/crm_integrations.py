from flask import Blueprint, request, jsonify
from app.models.crm_integrations import Integration, EmailIntegration, CalendarIntegration, Webhook, APIToken
from app import db
import json

bp = Blueprint('crm_integrations', __name__, url_prefix='/crm/integrations')

# Integration Routes
@bp.route('/integrations', methods=['GET'])
def get_integrations():
    """Get all integrations"""
    try:
        integrations = Integration.query.all()
        return jsonify({
            'success': True,
            'data': [integration.__dict__ for integration in integrations]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/integrations', methods=['POST'])
def create_integration():
    """Create a new integration"""
    try:
        integration_data = request.get_json()
        
        integration = Integration(
            name=integration_data['name'],
            type=integration_data.get('type'),
            provider=integration_data.get('provider'),
            config=integration_data.get('config'),
            is_active=integration_data.get('is_active', True),
            created_by=integration_data.get('created_by')
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': integration.__dict__,
            'message': 'Integration created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/integrations/<int:integration_id>', methods=['GET'])
def get_integration(integration_id):
    """Get a specific integration"""
    try:
        integration = Integration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Integration not found'})
        
        return jsonify({'success': True, 'data': integration.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/integrations/<int:integration_id>', methods=['PUT'])
def update_integration(integration_id):
    """Update an integration"""
    try:
        integration = Integration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Integration not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(integration, field):
                setattr(integration, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': integration.__dict__,
            'message': 'Integration updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/integrations/<int:integration_id>', methods=['DELETE'])
def delete_integration(integration_id):
    """Delete an integration"""
    try:
        integration = Integration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Integration not found'})
        
        db.session.delete(integration)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Integration deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Email Integration Routes
@bp.route('/email-integrations', methods=['GET'])
def get_email_integrations():
    """Get all email integrations"""
    try:
        integrations = EmailIntegration.query.all()
        return jsonify({
            'success': True,
            'data': [integration.__dict__ for integration in integrations]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/email-integrations', methods=['POST'])
def create_email_integration():
    """Create a new email integration"""
    try:
        integration_data = request.get_json()
        
        integration = EmailIntegration(
            integration_id=integration_data.get('integration_id'),
            email_provider=integration_data.get('email_provider'),
            email_address=integration_data.get('email_address'),
            smtp_server=integration_data.get('smtp_server'),
            smtp_port=integration_data.get('smtp_port'),
            smtp_username=integration_data.get('smtp_username'),
            smtp_password=integration_data.get('smtp_password'),
            use_ssl=integration_data.get('use_ssl', True),
            is_active=integration_data.get('is_active', True)
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': integration.__dict__,
            'message': 'Email integration created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/email-integrations/<int:integration_id>', methods=['GET'])
def get_email_integration(integration_id):
    """Get a specific email integration"""
    try:
        integration = EmailIntegration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Email integration not found'})
        
        return jsonify({'success': True, 'data': integration.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/email-integrations/<int:integration_id>', methods=['PUT'])
def update_email_integration(integration_id):
    """Update an email integration"""
    try:
        integration = EmailIntegration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Email integration not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(integration, field):
                setattr(integration, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': integration.__dict__,
            'message': 'Email integration updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/email-integrations/<int:integration_id>', methods=['DELETE'])
def delete_email_integration(integration_id):
    """Delete an email integration"""
    try:
        integration = EmailIntegration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Email integration not found'})
        
        db.session.delete(integration)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Email integration deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Calendar Integration Routes
@bp.route('/calendar-integrations', methods=['GET'])
def get_calendar_integrations():
    """Get all calendar integrations"""
    try:
        integrations = CalendarIntegration.query.all()
        return jsonify({
            'success': True,
            'data': [integration.__dict__ for integration in integrations]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/calendar-integrations', methods=['POST'])
def create_calendar_integration():
    """Create a new calendar integration"""
    try:
        integration_data = request.get_json()
        
        integration = CalendarIntegration(
            integration_id=integration_data.get('integration_id'),
            calendar_provider=integration_data.get('calendar_provider'),
            calendar_id=integration_data.get('calendar_id'),
            api_key=integration_data.get('api_key'),
            sync_direction=integration_data.get('sync_direction', 'Bidirectional'),
            is_active=integration_data.get('is_active', True)
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': integration.__dict__,
            'message': 'Calendar integration created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/calendar-integrations/<int:integration_id>', methods=['GET'])
def get_calendar_integration(integration_id):
    """Get a specific calendar integration"""
    try:
        integration = CalendarIntegration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Calendar integration not found'})
        
        return jsonify({'success': True, 'data': integration.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/calendar-integrations/<int:integration_id>', methods=['PUT'])
def update_calendar_integration(integration_id):
    """Update a calendar integration"""
    try:
        integration = CalendarIntegration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Calendar integration not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(integration, field):
                setattr(integration, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': integration.__dict__,
            'message': 'Calendar integration updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/calendar-integrations/<int:integration_id>', methods=['DELETE'])
def delete_calendar_integration(integration_id):
    """Delete a calendar integration"""
    try:
        integration = CalendarIntegration.query.get(integration_id)
        if not integration:
            return jsonify({'success': False, 'error': 'Calendar integration not found'})
        
        db.session.delete(integration)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Calendar integration deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Webhook Routes
@bp.route('/webhooks', methods=['GET'])
def get_webhooks():
    """Get all webhooks"""
    try:
        webhooks = Webhook.query.all()
        return jsonify({
            'success': True,
            'data': [webhook.__dict__ for webhook in webhooks]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/webhooks', methods=['POST'])
def create_webhook():
    """Create a new webhook"""
    try:
        webhook_data = request.get_json()
        
        webhook = Webhook(
            name=webhook_data['name'],
            url=webhook_data['url'],
            event_type=webhook_data.get('event_type'),
            headers=webhook_data.get('headers'),
            is_active=webhook_data.get('is_active', True),
            created_by=webhook_data.get('created_by')
        )
        
        db.session.add(webhook)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': webhook.__dict__,
            'message': 'Webhook created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/webhooks/<int:webhook_id>', methods=['GET'])
def get_webhook(webhook_id):
    """Get a specific webhook"""
    try:
        webhook = Webhook.query.get(webhook_id)
        if not webhook:
            return jsonify({'success': False, 'error': 'Webhook not found'})
        
        return jsonify({'success': True, 'data': webhook.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/webhooks/<int:webhook_id>', methods=['PUT'])
def update_webhook(webhook_id):
    """Update a webhook"""
    try:
        webhook = Webhook.query.get(webhook_id)
        if not webhook:
            return jsonify({'success': False, 'error': 'Webhook not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(webhook, field):
                setattr(webhook, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': webhook.__dict__,
            'message': 'Webhook updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/webhooks/<int:webhook_id>', methods=['DELETE'])
def delete_webhook(webhook_id):
    """Delete a webhook"""
    try:
        webhook = Webhook.query.get(webhook_id)
        if not webhook:
            return jsonify({'success': False, 'error': 'Webhook not found'})
        
        db.session.delete(webhook)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Webhook deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# API Token Routes
@bp.route('/api-tokens', methods=['GET'])
def get_api_tokens():
    """Get all API tokens"""
    try:
        tokens = APIToken.query.all()
        return jsonify({
            'success': True,
            'data': [token.__dict__ for token in tokens]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api-tokens', methods=['POST'])
def create_api_token():
    """Create a new API token"""
    try:
        token_data = request.get_json()
        
        # Generate a secure token (in production, use proper token generation)
        import secrets
        token = secrets.token_urlsafe(32)
        
        api_token = APIToken(
            name=token_data['name'],
            token=token,
            permissions=token_data.get('permissions'),
            expires_at=token_data.get('expires_at'),
            is_active=token_data.get('is_active', True),
            created_by=token_data.get('created_by')
        )
        
        db.session.add(api_token)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': api_token.__dict__,
            'message': 'API token created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api-tokens/<int:token_id>', methods=['GET'])
def get_api_token(token_id):
    """Get a specific API token"""
    try:
        token = APIToken.query.get(token_id)
        if not token:
            return jsonify({'success': False, 'error': 'API token not found'})
        
        return jsonify({'success': True, 'data': token.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api-tokens/<int:token_id>', methods=['PUT'])
def update_api_token(token_id):
    """Update an API token"""
    try:
        token = APIToken.query.get(token_id)
        if not token:
            return jsonify({'success': False, 'error': 'API token not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(token, field):
                setattr(token, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': token.__dict__,
            'message': 'API token updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api-tokens/<int:token_id>', methods=['DELETE'])
def delete_api_token(token_id):
    """Delete an API token"""
    try:
        token = APIToken.query.get(token_id)
        if not token:
            return jsonify({'success': False, 'error': 'API token not found'})
        
        db.session.delete(token)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'API token deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}) 
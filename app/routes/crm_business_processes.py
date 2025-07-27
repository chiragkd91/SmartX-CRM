from flask import Blueprint, request, jsonify
from app.models.crm_business_processes import Workflow, Campaign, LeadScoring, AutomationRule
from app import db
import json

bp = Blueprint('crm_business_processes', __name__, url_prefix='/crm/business-processes')

# Workflow Routes
@bp.route('/workflows', methods=['GET'])
def get_workflows():
    """Get all workflows"""
    try:
        workflows = Workflow.query.all()
        return jsonify({
            'success': True,
            'data': [workflow.__dict__ for workflow in workflows]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/workflows', methods=['POST'])
def create_workflow():
    """Create a new workflow"""
    try:
        workflow_data = request.get_json()
        
        workflow = Workflow(
            name=workflow_data['name'],
            description=workflow_data.get('description'),
            trigger_type=workflow_data.get('trigger_type'),
            trigger_conditions=workflow_data.get('trigger_conditions'),
            is_active=workflow_data.get('is_active', True),
            created_by=workflow_data.get('created_by')
        )
        
        db.session.add(workflow)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': workflow.__dict__,
            'message': 'Workflow created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/workflows/<int:workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """Get a specific workflow"""
    try:
        workflow = Workflow.query.get(workflow_id)
        if not workflow:
            return jsonify({'success': False, 'error': 'Workflow not found'})
        
        return jsonify({'success': True, 'data': workflow.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/workflows/<int:workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    """Update a workflow"""
    try:
        workflow = Workflow.query.get(workflow_id)
        if not workflow:
            return jsonify({'success': False, 'error': 'Workflow not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(workflow, field):
                setattr(workflow, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': workflow.__dict__,
            'message': 'Workflow updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/workflows/<int:workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    """Delete a workflow"""
    try:
        workflow = Workflow.query.get(workflow_id)
        if not workflow:
            return jsonify({'success': False, 'error': 'Workflow not found'})
        
        db.session.delete(workflow)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Workflow deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Campaign Routes
@bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns"""
    try:
        campaigns = Campaign.query.all()
        return jsonify({
            'success': True,
            'data': [campaign.__dict__ for campaign in campaigns]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/campaigns', methods=['POST'])
def create_campaign():
    """Create a new campaign"""
    try:
        campaign_data = request.get_json()
        
        campaign = Campaign(
            name=campaign_data['name'],
            description=campaign_data.get('description'),
            type=campaign_data.get('type'),
            status=campaign_data.get('status', 'Draft'),
            start_date=campaign_data.get('start_date'),
            end_date=campaign_data.get('end_date'),
            budget=campaign_data.get('budget'),
            target_audience=campaign_data.get('target_audience'),
            created_by=campaign_data.get('created_by')
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': campaign.__dict__,
            'message': 'Campaign created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Get a specific campaign"""
    try:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'success': False, 'error': 'Campaign not found'})
        
        return jsonify({'success': True, 'data': campaign.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    """Update a campaign"""
    try:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'success': False, 'error': 'Campaign not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(campaign, field):
                setattr(campaign, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': campaign.__dict__,
            'message': 'Campaign updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete a campaign"""
    try:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'success': False, 'error': 'Campaign not found'})
        
        db.session.delete(campaign)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Campaign deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Lead Scoring Routes
@bp.route('/lead-scoring', methods=['GET'])
def get_lead_scoring_rules():
    """Get all lead scoring rules"""
    try:
        rules = LeadScoring.query.all()
        return jsonify({
            'success': True,
            'data': [rule.__dict__ for rule in rules]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/lead-scoring', methods=['POST'])
def create_lead_scoring_rule():
    """Create a new lead scoring rule"""
    try:
        rule_data = request.get_json()
        
        rule = LeadScoring(
            name=rule_data['name'],
            description=rule_data.get('description'),
            criteria=rule_data.get('criteria'),
            is_active=rule_data.get('is_active', True),
            created_by=rule_data.get('created_by')
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.__dict__,
            'message': 'Lead scoring rule created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/lead-scoring/<int:rule_id>', methods=['GET'])
def get_lead_scoring_rule(rule_id):
    """Get a specific lead scoring rule"""
    try:
        rule = LeadScoring.query.get(rule_id)
        if not rule:
            return jsonify({'success': False, 'error': 'Lead scoring rule not found'})
        
        return jsonify({'success': True, 'data': rule.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/lead-scoring/<int:rule_id>', methods=['PUT'])
def update_lead_scoring_rule(rule_id):
    """Update a lead scoring rule"""
    try:
        rule = LeadScoring.query.get(rule_id)
        if not rule:
            return jsonify({'success': False, 'error': 'Lead scoring rule not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(rule, field):
                setattr(rule, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.__dict__,
            'message': 'Lead scoring rule updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/lead-scoring/<int:rule_id>', methods=['DELETE'])
def delete_lead_scoring_rule(rule_id):
    """Delete a lead scoring rule"""
    try:
        rule = LeadScoring.query.get(rule_id)
        if not rule:
            return jsonify({'success': False, 'error': 'Lead scoring rule not found'})
        
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lead scoring rule deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Automation Rules Routes
@bp.route('/automation-rules', methods=['GET'])
def get_automation_rules():
    """Get all automation rules"""
    try:
        rules = AutomationRule.query.all()
        return jsonify({
            'success': True,
            'data': [rule.__dict__ for rule in rules]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/automation-rules', methods=['POST'])
def create_automation_rule():
    """Create a new automation rule"""
    try:
        rule_data = request.get_json()
        
        rule = AutomationRule(
            name=rule_data['name'],
            description=rule_data.get('description'),
            trigger_event=rule_data.get('trigger_event'),
            trigger_conditions=rule_data.get('trigger_conditions'),
            actions=rule_data.get('actions'),
            is_active=rule_data.get('is_active', True),
            created_by=rule_data.get('created_by')
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.__dict__,
            'message': 'Automation rule created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/automation-rules/<int:rule_id>', methods=['GET'])
def get_automation_rule(rule_id):
    """Get a specific automation rule"""
    try:
        rule = AutomationRule.query.get(rule_id)
        if not rule:
            return jsonify({'success': False, 'error': 'Automation rule not found'})
        
        return jsonify({'success': True, 'data': rule.__dict__})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/automation-rules/<int:rule_id>', methods=['PUT'])
def update_automation_rule(rule_id):
    """Update an automation rule"""
    try:
        rule = AutomationRule.query.get(rule_id)
        if not rule:
            return jsonify({'success': False, 'error': 'Automation rule not found'})
        
        update_data = request.get_json()
        for field, value in update_data.items():
            if hasattr(rule, field):
                setattr(rule, field, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.__dict__,
            'message': 'Automation rule updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/automation-rules/<int:rule_id>', methods=['DELETE'])
def delete_automation_rule(rule_id):
    """Delete an automation rule"""
    try:
        rule = AutomationRule.query.get(rule_id)
        if not rule:
            return jsonify({'success': False, 'error': 'Automation rule not found'})
        
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Automation rule deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}) 
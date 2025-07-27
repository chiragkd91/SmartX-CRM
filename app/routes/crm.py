from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from app.services.crm_service import CRMService
from app.services.lead_service import LeadService
from app.services.account_service import AccountService
from app.services.contact_service import ContactService
from app.services.opportunity_service import OpportunityService
from app.services.activity_service import ActivityService
from app.models.crm import Lead, Account, Contact, Opportunity, Activity
from app import db
from datetime import datetime
import json

bp = Blueprint('crm', __name__, url_prefix='/crm')

# Initialize services
crm_service = CRMService()
lead_service = LeadService()
account_service = AccountService()
contact_service = ContactService()
opportunity_service = OpportunityService()
activity_service = ActivityService()

# Dashboard Routes
@bp.route('/dashboard')
def dashboard():
    """CRM Dashboard"""
    try:
        # Get CRM statistics
        stats_result = crm_service.get_crm_stats()
        pipeline_result = crm_service.get_sales_pipeline()
        conversion_result = crm_service.get_lead_conversion_rate()
        
        if stats_result['success'] and pipeline_result['success'] and conversion_result['success']:
            return render_template('crm/dashboard.html',
                                 stats=stats_result['data'],
                                 pipeline=pipeline_result['data'],
                                 conversion=conversion_result['data'])
        else:
            return render_template('crm/dashboard.html', error="Failed to load dashboard data")
    except Exception as e:
        return render_template('crm/dashboard.html', error=str(e))

# Lead Routes
@bp.route('/leads', methods=['GET'])
def get_leads():
    """Get all leads with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = lead_service.get_leads(filters=filters_dict, page=page, per_page=per_page)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            return render_template('crm/leads/list.html', leads_data=result['data'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/list')
def leads_list():
    """Leads list page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = lead_service.get_leads(filters=filters_dict, page=page, per_page=per_page)
        
        return render_template('crm/leads/list.html', leads_data=result['data'])
    except Exception as e:
        return render_template('crm/leads/list.html', error=str(e))

@bp.route('/leads/form')
@bp.route('/leads/new')
def leads_form():
    """Lead form page for creating new leads"""
    return render_template('crm/leads/form.html')

@bp.route('/leads/<int:lead_id>/form')
def lead_edit_form(lead_id):
    """Lead form page for editing existing leads"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        return render_template('crm/leads/form.html', lead=lead)
    except Exception as e:
        return render_template('crm/leads/form.html', error=str(e))

# Contact Form Routes
@bp.route('/contacts/form')
@bp.route('/contacts/new')
def contacts_form():
    """Contact form page for creating new contacts"""
    return render_template('crm/contacts/form.html')

@bp.route('/contacts/<int:contact_id>/form')
def contact_edit_form(contact_id):
    """Contact form page for editing existing contacts"""
    try:
        contact = Contact.query.get_or_404(contact_id)
        return render_template('crm/contacts/form.html', contact=contact)
    except Exception as e:
        return render_template('crm/contacts/form.html', error=str(e))

# Opportunity Form Routes
@bp.route('/opportunities/form')
@bp.route('/opportunities/new')
def opportunities_form():
    """Opportunity form page for creating new opportunities"""
    return render_template('crm/opportunities/form.html')

@bp.route('/opportunities/<int:opportunity_id>/form')
def opportunity_edit_form(opportunity_id):
    """Opportunity form page for editing existing opportunities"""
    try:
        opportunity = Opportunity.query.get_or_404(opportunity_id)
        return render_template('crm/opportunities/form.html', opportunity=opportunity)
    except Exception as e:
        return render_template('crm/opportunities/form.html', error=str(e))

# Activity Form Routes
@bp.route('/activities/form')
@bp.route('/activities/new')
def activities_form():
    """Activity form page for creating new activities"""
    return render_template('crm/activities/form.html')

@bp.route('/activities/<int:activity_id>/form')
def activity_edit_form(activity_id):
    """Activity form page for editing existing activities"""
    try:
        activity = Activity.query.get_or_404(activity_id)
        return render_template('crm/activities/form.html', activity=activity)
    except Exception as e:
        return render_template('crm/activities/form.html', error=str(e))

# Account Form Routes
@bp.route('/accounts/form')
@bp.route('/accounts/new')
def accounts_form():
    """Account form page for creating new accounts"""
    return render_template('crm/accounts/form.html')

@bp.route('/accounts/<int:account_id>/form')
def account_edit_form(account_id):
    """Account form page for editing existing accounts"""
    try:
        account = Account.query.get_or_404(account_id)
        return render_template('crm/accounts/form.html', account=account)
    except Exception as e:
        return render_template('crm/accounts/form.html', error=str(e))

@bp.route('/leads', methods=['POST'])
def create_lead():
    """Create a new lead"""
    try:
        if request.is_json:
            lead_data = request.get_json()
        else:
            lead_data = request.form.to_dict()
        
        # Clean and validate data
        lead_data = {k: v.strip() if isinstance(v, str) else v for k, v in lead_data.items()}
        
        result = lead_service.create_lead(lead_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                flash('Lead created successfully!', 'success')
                return redirect(url_for('crm.lead_detail', lead_id=result['data'].id))
            else:
                flash(result['error'], 'error')
                return render_template('crm/leads/form.html', error=result['error'])
    except Exception as e:
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'success': False, 'error': str(e)})
        else:
            flash(str(e), 'error')
            return render_template('crm/leads/form.html', error=str(e))

@bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get a specific lead"""
    try:
        result = lead_service.get_lead(lead_id)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/leads/detail.html', lead=result['data'])
            else:
                return render_template('crm/leads/list.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/<int:lead_id>/detail')
def lead_detail(lead_id):
    """Lead detail page"""
    try:
        result = lead_service.get_lead(lead_id)
        if result['success']:
            return render_template('crm/leads/detail.html', lead=result['data'])
        else:
            flash(result['error'], 'error')
            return redirect(url_for('crm.leads_list'))
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('crm.leads_list'))

@bp.route('/leads/<int:lead_id>', methods=['PUT', 'POST'])
def update_lead(lead_id):
    """Update a lead"""
    try:
        if request.is_json:
            update_data = request.get_json()
        else:
            update_data = request.form.to_dict()
        
        # Clean and validate data
        update_data = {k: v.strip() if isinstance(v, str) else v for k, v in update_data.items()}
        
        result = lead_service.update_lead(lead_id, update_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                flash('Lead updated successfully!', 'success')
                return redirect(url_for('crm.lead_detail', lead_id=lead_id))
            else:
                flash(result['error'], 'error')
                return render_template('crm/leads/form.html', lead=result.get('data'), error=result['error'])
    except Exception as e:
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'success': False, 'error': str(e)})
        else:
            flash(str(e), 'error')
            return render_template('crm/leads/form.html', error=str(e))

@bp.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete a lead"""
    try:
        result = lead_service.delete_lead(lead_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/<int:lead_id>/qualify', methods=['POST'])
def qualify_lead(lead_id):
    """Qualify a lead"""
    try:
        qualification_data = request.get_json() if request.is_json else request.form.to_dict()
        result = lead_service.qualify_lead(lead_id, qualification_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/<int:lead_id>/score', methods=['POST'])
def score_lead(lead_id):
    """Score a lead"""
    try:
        result = lead_service.score_lead(lead_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/<int:lead_id>/nurture', methods=['POST'])
def nurture_lead(lead_id):
    """Nurture a lead"""
    try:
        nurturing_data = request.get_json() if request.is_json else request.form.to_dict()
        result = lead_service.nurture_lead(lead_id, nurturing_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/<int:lead_id>/convert', methods=['POST'])
def convert_lead(lead_id):
    """Convert a lead"""
    try:
        conversion_data = request.get_json() if request.is_json else request.form.to_dict()
        result = lead_service.convert_lead(lead_id, conversion_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/bulk-action', methods=['POST'])
def bulk_action_leads():
    """Perform bulk actions on leads"""
    try:
        data = request.get_json()
        action = data.get('action')
        lead_ids = data.get('lead_ids', [])
        
        if not lead_ids:
            return jsonify({'success': False, 'error': 'No leads selected'})
        
        results = []
        for lead_id in lead_ids:
            if action == 'delete':
                result = lead_service.delete_lead(lead_id)
            elif action == 'qualify':
                result = lead_service.qualify_lead(lead_id, {'status': 'Qualified'})
            elif action == 'contact':
                result = lead_service.qualify_lead(lead_id, {'status': 'Contacted'})
            else:
                result = {'success': False, 'error': f'Unknown action: {action}'}
            results.append(result)
        
        success_count = sum(1 for r in results if r['success'])
        return jsonify({
            'success': True,
            'message': f'{success_count} leads processed successfully',
            'results': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/import', methods=['POST'])
def import_leads():
    """Import leads from file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and file.filename.endswith('.csv'):
            # Parse CSV file
            import csv
            import io
            
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            leads_data = []
            for row in csv_reader:
                leads_data.append(row)
            
            result = lead_service.import_leads(leads_data)
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': 'Only CSV files are supported'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/export')
def export_leads():
    """Export leads to CSV"""
    try:
        from flask import send_file
        import csv
        import io
        
        # Get filters from query parameters
        filters = {}
        for key, value in request.args.items():
            if value and key not in ['page', 'per_page']:
                filters[key] = value
        
        result = lead_service.export_leads(filters)
        
        if not result['success']:
            return jsonify(result)
        
        # Create CSV file
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'id', 'first_name', 'last_name', 'email', 'phone', 'company',
            'job_title', 'industry', 'source', 'status', 'score', 'budget',
            'timeline', 'notes', 'created_at', 'updated_at'
        ])
        
        writer.writeheader()
        for lead in result['data']:
            writer.writerow(lead)
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'leads_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/leads/reports')
def lead_reports():
    """Generate lead reports"""
    try:
        result = lead_service.generate_lead_reports()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/leads/reports.html', report=result['data'])
            else:
                return render_template('crm/leads/reports.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Account Routes
@bp.route('/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = account_service.get_accounts(filters=filters_dict, page=page, per_page=per_page)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            return render_template('crm/accounts/list.html', accounts_data=result['data'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/accounts', methods=['POST'])
def create_account():
    """Create a new account"""
    try:
        if request.is_json:
            account_data = request.get_json()
        else:
            account_data = request.form.to_dict()
        
        result = account_service.create_account(account_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/accounts/form.html', message="Account created successfully")
            else:
                return render_template('crm/accounts/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """Get a specific account"""
    try:
        result = account_service.get_account(account_id)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/accounts/detail.html', account=result['data'])
            else:
                return render_template('crm/accounts/list.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/accounts/<int:account_id>', methods=['PUT', 'POST'])
def update_account(account_id):
    """Update an account"""
    try:
        if request.is_json:
            update_data = request.get_json()
        else:
            update_data = request.form.to_dict()
        
        result = account_service.update_account(account_id, update_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/accounts/detail.html', account=result['data'], message="Account updated successfully")
            else:
                return render_template('crm/accounts/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    """Delete an account"""
    try:
        result = account_service.delete_account(account_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/accounts/list')
def accounts_list():
    """Accounts list page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = account_service.get_accounts(filters=filters_dict, page=page, per_page=per_page)
        
        return render_template('crm/accounts/list.html', accounts_data=result['data'])
    except Exception as e:
        return render_template('crm/accounts/list.html', error=str(e))

# Contact Routes
@bp.route('/contacts', methods=['GET'])
def get_contacts():
    """Get all contacts"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = contact_service.get_contacts(filters=filters_dict, page=page, per_page=per_page)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            return render_template('crm/contacts/list.html', contacts_data=result['data'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/contacts', methods=['POST'])
def create_contact():
    """Create a new contact"""
    try:
        if request.is_json:
            contact_data = request.get_json()
        else:
            contact_data = request.form.to_dict()
        
        result = contact_service.create_contact(contact_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/contacts/form.html', message="Contact created successfully")
            else:
                return render_template('crm/contacts/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Get a specific contact"""
    try:
        result = contact_service.get_contact(contact_id)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/contacts/detail.html', contact=result['data'])
            else:
                return render_template('crm/contacts/list.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/contacts/<int:contact_id>', methods=['PUT', 'POST'])
def update_contact(contact_id):
    """Update a contact"""
    try:
        if request.is_json:
            update_data = request.get_json()
        else:
            update_data = request.form.to_dict()
        
        result = contact_service.update_contact(contact_id, update_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/contacts/detail.html', contact=result['data'], message="Contact updated successfully")
            else:
                return render_template('crm/contacts/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete a contact"""
    try:
        result = contact_service.delete_contact(contact_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/contacts/list')
def contacts_list():
    """Contacts list page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = contact_service.get_contacts(filters=filters_dict, page=page, per_page=per_page)
        
        return render_template('crm/contacts/list.html', contacts_data=result['data'])
    except Exception as e:
        return render_template('crm/contacts/list.html', error=str(e))

# Opportunity Routes
@bp.route('/opportunities', methods=['GET'])
def get_opportunities():
    """Get all opportunities"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = opportunity_service.get_opportunities(filters=filters_dict, page=page, per_page=per_page)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            return render_template('crm/opportunities/list.html', opportunities_data=result['data'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/opportunities', methods=['POST'])
def create_opportunity():
    """Create a new opportunity"""
    try:
        if request.is_json:
            opportunity_data = request.get_json()
        else:
            opportunity_data = request.form.to_dict()
        
        result = opportunity_service.create_opportunity(opportunity_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/opportunities/form.html', message="Opportunity created successfully")
            else:
                return render_template('crm/opportunities/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/opportunities/<int:opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    """Get a specific opportunity"""
    try:
        result = opportunity_service.get_opportunity(opportunity_id)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/opportunities/detail.html', opportunity=result['data'])
            else:
                return render_template('crm/opportunities/list.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/opportunities/<int:opportunity_id>', methods=['PUT', 'POST'])
def update_opportunity(opportunity_id):
    """Update an opportunity"""
    try:
        if request.is_json:
            update_data = request.get_json()
        else:
            update_data = request.form.to_dict()
        
        result = opportunity_service.update_opportunity(opportunity_id, update_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/opportunities/detail.html', opportunity=result['data'], message="Opportunity updated successfully")
            else:
                return render_template('crm/opportunities/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/opportunities/<int:opportunity_id>', methods=['DELETE'])
def delete_opportunity(opportunity_id):
    """Delete an opportunity"""
    try:
        result = opportunity_service.delete_opportunity(opportunity_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/opportunities/list')
def opportunities_list():
    """Opportunities list page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = opportunity_service.get_opportunities(filters=filters_dict, page=page, per_page=per_page)
        
        return render_template('crm/opportunities/list.html', opportunities_data=result['data'])
    except Exception as e:
        return render_template('crm/opportunities/list.html', error=str(e))

# Activity Routes
@bp.route('/activities', methods=['GET'])
def get_activities():
    """Get all activities"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = activity_service.get_activities(filters=filters_dict, page=page, per_page=per_page)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            return render_template('crm/activities/list.html', activities_data=result['data'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/activities', methods=['POST'])
def create_activity():
    """Create a new activity"""
    try:
        if request.is_json:
            activity_data = request.get_json()
        else:
            activity_data = request.form.to_dict()
        
        result = activity_service.create_activity(activity_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/activities/form.html', message="Activity created successfully")
            else:
                return render_template('crm/activities/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/activities/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    """Get a specific activity"""
    try:
        result = activity_service.get_activity(activity_id)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/activities/detail.html', activity=result['data'])
            else:
                return render_template('crm/activities/list.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/activities/<int:activity_id>', methods=['PUT', 'POST'])
def update_activity(activity_id):
    """Update an activity"""
    try:
        if request.is_json:
            update_data = request.get_json()
        else:
            update_data = request.form.to_dict()
        
        result = activity_service.update_activity(activity_id, update_data)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            if result['success']:
                return render_template('crm/activities/detail.html', activity=result['data'], message="Activity updated successfully")
            else:
                return render_template('crm/activities/form.html', error=result['error'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/activities/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    """Delete an activity"""
    try:
        result = activity_service.delete_activity(activity_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/activities/list')
def activities_list():
    """Activities list page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.get('filters', '{}')
        
        filters_dict = json.loads(filters) if filters else {}
        
        result = activity_service.get_activities(filters=filters_dict, page=page, per_page=per_page)
        
        return render_template('crm/activities/list.html', activities_data=result['data'])
    except Exception as e:
        return render_template('crm/activities/list.html', error=str(e))

@bp.route('/quotes/list')
def quotes_list():
    """Quotes list page"""
    try:
        from app.models.crm import Quote
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        quotes = Quote.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template('crm/quotes/list.html', quotes=quotes)
    except Exception as e:
        return render_template('crm/quotes/list.html', error=str(e))

@bp.route('/quotes')
def quotes():
    """Quotes list page (alias for quotes_list)"""
    return quotes_list()

@bp.route('/workflows')
def workflows():
    """Workflows list page"""
    try:
        # This would typically fetch workflows from a workflows service
        # For now, return a simple template
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Mock data for workflows
        workflows = {
            'items': [],
            'total': 0,
            'pages': 0,
            'page': page,
            'per_page': per_page,
            'has_prev': False,
            'has_next': False,
            'prev_num': None,
            'next_num': None
        }
        
        return render_template('crm/workflows/list.html', workflows=workflows)
    except Exception as e:
        return render_template('crm/workflows/list.html', error=str(e))

# Analytics and Reports Routes
@bp.route('/analytics')
def analytics():
    """CRM Analytics Dashboard"""
    try:
        # Get various analytics data
        stats_result = crm_service.get_crm_stats()
        pipeline_result = crm_service.get_sales_pipeline()
        conversion_result = crm_service.get_lead_conversion_rate()
        clv_result = crm_service.get_customer_lifetime_value()
        forecast_result = crm_service.get_sales_forecast()
        
        analytics_data = {
            'stats': stats_result['data'] if stats_result['success'] else {},
            'pipeline': pipeline_result['data'] if pipeline_result['success'] else [],
            'conversion': conversion_result['data'] if conversion_result['success'] else {},
            'clv': clv_result['data'] if clv_result['success'] else {},
            'forecast': forecast_result['data'] if forecast_result['success'] else {}
        }
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'success': True, 'data': analytics_data})
        else:
            return render_template('crm/analytics.html', analytics=analytics_data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/reports')
def reports():
    """Generate CRM reports"""
    try:
        report_type = request.args.get('type', 'all')
        result = crm_service.generate_crm_reports(report_type)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)
        else:
            return render_template('crm/reports.html', reports=result['data'])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Export Routes
@bp.route('/export/<data_type>')
def export_data(data_type):
    """Export CRM data"""
    try:
        filters = request.args.get('filters', '{}')
        filters_dict = json.loads(filters) if filters else {}
        
        result = crm_service.export_crm_data(data_type, filters_dict)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}) 
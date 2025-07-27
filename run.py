from app import create_app, db
from app.models.crm import User, Lead, Account, Contact, Opportunity, Activity, Quote, Territory
from app.models.crm_business_processes import Workflow, Campaign, LeadScoring, AutomationRule
from app.models.crm_integrations import Integration, EmailIntegration, CalendarIntegration
from werkzeug.security import generate_password_hash
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Lead': Lead,
        'Account': Account,
        'Contact': Contact,
        'Opportunity': Opportunity,
        'Activity': Activity,
        'Quote': Quote,
        'Territory': Territory,
        'Workflow': Workflow,
        'Campaign': Campaign,
        'LeadScoring': LeadScoring,
        'AutomationRule': AutomationRule,
        'Integration': Integration,
        'EmailIntegration': EmailIntegration,
        'CalendarIntegration': CalendarIntegration
    }

@app.cli.command()
def init_db():
    """Initialize the database with sample data"""
    db.create_all()
    
    # Create sample user
    if not User.query.filter_by(email='admin@example.com').first():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            role='Admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Created admin user: admin@example.com / admin123")
    
    # Create sample territory
    if not Territory.query.filter_by(name='North America').first():
        territory = Territory(
            name='North America',
            description='North American sales territory',
            manager_id=1
        )
        db.session.add(territory)
        db.session.commit()
        print("Created sample territory: North America")
    
    print("Database initialized successfully!")

@app.cli.command()
def create_sample_data():
    """Create sample CRM data"""
    # Create sample leads
    sample_leads = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0123',
            'company': 'Tech Solutions Inc',
            'job_title': 'CTO',
            'industry': 'Technology',
            'source': 'Website',
            'status': 'New',
            'score': 75
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '+1-555-0456',
            'company': 'Marketing Pro',
            'job_title': 'Marketing Director',
            'industry': 'Marketing',
            'source': 'LinkedIn',
            'status': 'Qualified',
            'score': 85
        }
    ]
    
    for lead_data in sample_leads:
        if not Lead.query.filter_by(email=lead_data['email']).first():
            lead = Lead(**lead_data, assigned_to=1)
            db.session.add(lead)
    
    # Create sample accounts
    sample_accounts = [
        {
            'name': 'Tech Solutions Inc',
            'industry': 'Technology',
            'website': 'www.techsolutions.com',
            'phone': '+1-555-0001',
            'email': 'info@techsolutions.com',
            'annual_revenue': 5000000,
            'employee_count': 50,
            'status': 'Active',
            'type': 'Customer'
        },
        {
            'name': 'Marketing Pro',
            'industry': 'Marketing',
            'website': 'www.marketingpro.com',
            'phone': '+1-555-0002',
            'email': 'contact@marketingpro.com',
            'annual_revenue': 2000000,
            'employee_count': 25,
            'status': 'Active',
            'type': 'Prospect'
        }
    ]
    
    for account_data in sample_accounts:
        if not Account.query.filter_by(name=account_data['name']).first():
            account = Account(**account_data, assigned_to=1, territory_id=1)
            db.session.add(account)
    
    db.session.commit()
    print("Sample data created successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
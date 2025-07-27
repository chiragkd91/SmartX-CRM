from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Workflow(db.Model):
    __tablename__ = 'workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    trigger_type = db.Column(db.String(50))  # Lead Created, Opportunity Updated, etc.
    trigger_conditions = db.Column(JSON)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    workflow_steps = db.relationship('WorkflowStep', backref='workflow', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Workflow {self.name}>'

class WorkflowStep(db.Model):
    __tablename__ = 'workflow_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50))  # Send Email, Create Task, Update Field, etc.
    action_config = db.Column(JSON)
    delay_minutes = db.Column(db.Integer, default=0)
    conditions = db.Column(JSON)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<WorkflowStep {self.action_type}>'

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))  # Email, Social Media, etc.
    status = db.Column(db.String(50), default='Draft')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Numeric(15, 2))
    target_audience = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    campaign_leads = db.relationship('CampaignLead', backref='campaign', lazy='dynamic')
    
    def __repr__(self):
        return f'<Campaign {self.name}>'

class CampaignLead(db.Model):
    __tablename__ = 'campaign_leads'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    status = db.Column(db.String(50), default='Added')
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CampaignLead {self.campaign_id}-{self.lead_id}>'

class SalesProcess(db.Model):
    __tablename__ = 'sales_processes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    stages = db.Column(JSON)  # Array of stage objects
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<SalesProcess {self.name}>'

class LeadScoring(db.Model):
    __tablename__ = 'lead_scoring'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    criteria = db.Column(JSON)  # Scoring criteria and weights
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<LeadScoring {self.name}>'

class AutomationRule(db.Model):
    __tablename__ = 'automation_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    trigger_event = db.Column(db.String(100))
    trigger_conditions = db.Column(JSON)
    actions = db.Column(JSON)  # Array of actions to perform
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<AutomationRule {self.name}>' 
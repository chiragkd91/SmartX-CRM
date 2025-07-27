from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from app import db

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(200))
    job_title = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    source = db.Column(db.String(100))
    status = db.Column(db.String(50), default='New')
    score = db.Column(db.Integer, default=0)
    budget = db.Column(db.Numeric(10, 2))
    timeline = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    activities = db.relationship('Activity', backref='lead', lazy='dynamic')
    opportunities = db.relationship('Opportunity', backref='lead', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lead {self.first_name} {self.last_name}>'
    
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100))
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    annual_revenue = db.Column(db.Numeric(15, 2))
    employee_count = db.Column(db.Integer)
    status = db.Column(db.String(50), default='Active')
    type = db.Column(db.String(50))
    parent_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    territory_id = db.Column(db.Integer, db.ForeignKey('territories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    contacts = db.relationship('Contact', backref='account', lazy='dynamic')
    opportunities = db.relationship('Opportunity', backref='account', lazy='dynamic')
    activities = db.relationship('Activity', backref='account', lazy='dynamic')
    child_accounts = db.relationship('Account', backref=db.backref('parent', remote_side=[id]))
    
    def __repr__(self):
        return f'<Account {self.name}>'

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    job_title = db.Column(db.String(100))
    department = db.Column(db.String(100))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    lead_source = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Active')
    preferred_contact_method = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    activities = db.relationship('Activity', backref='contact', lazy='dynamic')
    opportunities = db.relationship('Opportunity', backref='contact', lazy='dynamic')
    
    def __repr__(self):
        return f'<Contact {self.first_name} {self.last_name}>'
    
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    stage = db.Column(db.String(50), default='Prospecting')
    amount = db.Column(db.Numeric(15, 2))
    probability = db.Column(db.Integer, default=0)
    expected_close_date = db.Column(db.Date)
    actual_close_date = db.Column(db.Date)
    type = db.Column(db.String(50))
    source = db.Column(db.String(100))
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    activities = db.relationship('Activity', backref='opportunity', lazy='dynamic')
    quotes = db.relationship('Quote', backref='opportunity', lazy='dynamic')
    
    def __repr__(self):
        return f'<Opportunity {self.name}>'

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Call, Email, Meeting, Task
    status = db.Column(db.String(50), default='Planned')
    priority = db.Column(db.String(20), default='Medium')
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # in minutes
    location = db.Column(db.String(200))
    
    # Foreign keys
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Activity {self.subject}>'

class Quote(db.Model):
    __tablename__ = 'quotes'
    
    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.String(50), unique=True, nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))
    status = db.Column(db.String(50), default='Draft')
    valid_until = db.Column(db.Date)
    total_amount = db.Column(db.Numeric(15, 2))
    tax_amount = db.Column(db.Numeric(15, 2))
    discount_amount = db.Column(db.Numeric(15, 2))
    grand_total = db.Column(db.Numeric(15, 2))
    notes = db.Column(db.Text)
    terms_conditions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    quote_items = db.relationship('QuoteItem', backref='quote', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quote {self.quote_number}>'

class QuoteItem(db.Model):
    __tablename__ = 'quote_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'))
    product_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(15, 2))
    discount_percent = db.Column(db.Numeric(5, 2), default=0)
    total_amount = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<QuoteItem {self.product_name}>'

class Territory(db.Model):
    __tablename__ = 'territories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    accounts = db.relationship('Account', backref='territory', lazy='dynamic')
    
    def __repr__(self):
        return f'<Territory {self.name}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(50), default='User')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    leads = db.relationship('Lead', backref='user', lazy='dynamic', foreign_keys='Lead.assigned_to')
    accounts = db.relationship('Account', backref='user', lazy='dynamic', foreign_keys='Account.assigned_to')
    contacts = db.relationship('Contact', backref='user', lazy='dynamic', foreign_keys='Contact.assigned_to')
    opportunities = db.relationship('Opportunity', backref='user', lazy='dynamic', foreign_keys='Opportunity.assigned_to')
    activities = db.relationship('Activity', backref='user', lazy='dynamic', foreign_keys='Activity.assigned_to')
    created_activities = db.relationship('Activity', backref='creator', lazy='dynamic', foreign_keys='Activity.created_by')
    quotes = db.relationship('Quote', backref='creator', lazy='dynamic', foreign_keys='Quote.created_by')
    territories = db.relationship('Territory', backref='manager', lazy='dynamic', foreign_keys='Territory.manager_id')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_id(self):
        return str(self.id) 
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Integration(db.Model):
    __tablename__ = 'integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))  # Email, Calendar, Social Media, etc.
    provider = db.Column(db.String(100))
    config = db.Column(JSON)  # API keys, endpoints, etc.
    is_active = db.Column(db.Boolean, default=True)
    last_sync = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Integration {self.name}>'

class EmailIntegration(db.Model):
    __tablename__ = 'email_integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.Integer, db.ForeignKey('integrations.id'))
    email_provider = db.Column(db.String(50))  # Gmail, Outlook, etc.
    email_address = db.Column(db.String(120))
    smtp_server = db.Column(db.String(100))
    smtp_port = db.Column(db.Integer)
    smtp_username = db.Column(db.String(100))
    smtp_password = db.Column(db.String(255))
    use_ssl = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<EmailIntegration {self.email_address}>'

class CalendarIntegration(db.Model):
    __tablename__ = 'calendar_integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.Integer, db.ForeignKey('integrations.id'))
    calendar_provider = db.Column(db.String(50))  # Google Calendar, Outlook, etc.
    calendar_id = db.Column(db.String(200))
    api_key = db.Column(db.String(255))
    sync_direction = db.Column(db.String(20), default='Bidirectional')  # One-way, Bidirectional
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<CalendarIntegration {self.calendar_provider}>'

class SocialMediaIntegration(db.Model):
    __tablename__ = 'social_media_integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.Integer, db.ForeignKey('integrations.id'))
    platform = db.Column(db.String(50))  # LinkedIn, Twitter, Facebook, etc.
    account_name = db.Column(db.String(100))
    api_key = db.Column(db.String(255))
    api_secret = db.Column(db.String(255))
    access_token = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<SocialMediaIntegration {self.platform}>'

class Webhook(db.Model):
    __tablename__ = 'webhooks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    event_type = db.Column(db.String(100))  # Lead Created, Opportunity Updated, etc.
    headers = db.Column(JSON)
    is_active = db.Column(db.Boolean, default=True)
    last_triggered = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Webhook {self.name}>'

class APIToken(db.Model):
    __tablename__ = 'api_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    permissions = db.Column(JSON)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    last_used = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<APIToken {self.name}>'

class SyncLog(db.Model):
    __tablename__ = 'sync_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.Integer, db.ForeignKey('integrations.id'))
    sync_type = db.Column(db.String(50))  # Import, Export, Sync
    status = db.Column(db.String(20))  # Success, Failed, Partial
    records_processed = db.Column(db.Integer, default=0)
    records_successful = db.Column(db.Integer, default=0)
    records_failed = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<SyncLog {self.integration_id}-{self.sync_type}>' 
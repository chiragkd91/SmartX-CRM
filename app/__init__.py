from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Changed from 'auth.login' to 'main.login'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.crm import User
        return User.query.get(int(user_id))
    
    # Register main blueprint first
    from app.routes import main
    app.register_blueprint(main.bp)
    
    # Register blueprints
    from app.routes import crm, crm_business_processes, crm_integrations
    app.register_blueprint(crm.bp)
    app.register_blueprint(crm_business_processes.bp)
    app.register_blueprint(crm_integrations.bp)
    
    # Register new feature blueprints
    from app.routes import security, backup, monitoring, api_docs, admin, mobile, developer
    app.register_blueprint(security.bp)
    app.register_blueprint(backup.bp)
    app.register_blueprint(monitoring.bp)
    app.register_blueprint(api_docs.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(mobile.bp)
    app.register_blueprint(developer.bp)
    
    # Initialize security headers
    from app.security.security_headers import SecurityHeaders
    security_headers = SecurityHeaders()
    security_headers.init_app(app)
    
    return app 
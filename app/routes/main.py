"""
Main Routes for CRM System
Handles root routes and main navigation
"""

from flask import Blueprint, redirect, url_for, render_template, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.crm import User, db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Root route - redirect to CRM dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('crm.dashboard'))
    return redirect(url_for('main.login'))

@bp.route('/home')
def home():
    """Home page with navigation options"""
    return render_template('main/home.html')

@bp.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return render_template('main/dashboard.html')

@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@bp.route('/help')
def help():
    """Help page"""
    return render_template('main/help.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect(url_for('crm.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password', 'error')
            return render_template('main/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('crm.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('main/login.html')

@bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register route"""
    if current_user.is_authenticated:
        return redirect(url_for('crm.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if not all([username, email, password, confirm_password, first_name, last_name]):
            flash('Please fill in all fields', 'error')
            return render_template('main/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('main/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('main/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('main/register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('main/register.html')

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """User settings page"""
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        # Handle settings update
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('main.settings'))
    
    return render_template('main/settings.html')

@bp.route('/profile')
def profile():
    """User profile page"""
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    
    return render_template('main/profile.html') 
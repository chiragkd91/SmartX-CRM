"""
Admin Dashboard for CRM System
Centralized access to all system features
"""

from flask import Blueprint, request, jsonify, render_template, current_app
from app.security.security_auditor import SecurityAuditor
from app.backup.backup_manager import BackupManager
from app.monitoring.app_monitor import ApplicationMonitor
import logging

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Initialize services
security_auditor = SecurityAuditor()
backup_manager = BackupManager()
app_monitor = ApplicationMonitor()

@bp.route('/dashboard')
def admin_dashboard():
    """Main admin dashboard"""
    try:
        # Get system overview
        system_overview = {
            'security': {
                'last_audit': security_auditor.audit_results.get('timestamp'),
                'critical_issues': len(security_auditor.critical_issues),
                'security_score': security_auditor.audit_results.get('overall_score', 0)
            },
            'backup': {
                'total_backups': len(backup_manager.list_backups()),
                'last_backup': backup_manager.list_backups()[-1]['timestamp'] if backup_manager.list_backups() else None
            },
            'monitoring': {
                'uptime': app_monitor._calculate_uptime(),
                'alerts': len(app_monitor.get_alerts())
            }
        }
        
        return render_template('admin/dashboard.html', 
                             system_overview=system_overview)
                             
    except Exception as e:
        logging.error(f"Admin dashboard failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/security')
def security_overview():
    """Security overview"""
    try:
        security_data = {
            'audit_results': security_auditor.audit_results,
            'critical_issues': security_auditor.critical_issues,
            'warnings': security_auditor.warnings,
            'recommendations': security_auditor.recommendations
        }
        
        return render_template('admin/security_overview.html', 
                             security_data=security_data)
                             
    except Exception as e:
        logging.error(f"Security overview failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/backup')
def backup_overview():
    """Backup overview"""
    try:
        backups = backup_manager.list_backups()
        
        backup_data = {
            'backups': backups,
            'total_backups': len(backups),
            'recent_backups': [b for b in backups if b.get('status') == 'success'][:5],
            'failed_backups': [b for b in backups if b.get('status') == 'failed']
        }
        
        return render_template('admin/backup_overview.html', 
                             backup_data=backup_data)
                             
    except Exception as e:
        logging.error(f"Backup overview failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/monitoring')
def monitoring_overview():
    """Monitoring overview"""
    try:
        monitoring_data = app_monitor.monitor_application()
        
        return render_template('admin/monitoring_overview.html', 
                             monitoring_data=monitoring_data)
                             
    except Exception as e:
        logging.error(f"Monitoring overview failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api')
def api_overview():
    """API overview"""
    try:
        # Get all registered routes
        routes = []
        for rule in current_app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': str(rule)
            })
        
        api_data = {
            'total_endpoints': len(routes),
            'endpoints': routes[:20],  # Show first 20 endpoints
            'documentation_url': '/api/docs/',
            'testing_url': '/api/docs/test'
        }
        
        return render_template('admin/api_overview.html', 
                             api_data=api_data)
                             
    except Exception as e:
        logging.error(f"API overview failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/system-status')
def system_status():
    """System status check"""
    try:
        # Perform comprehensive system check
        status = {
            'security': {
                'audit_status': 'completed' if security_auditor.audit_results else 'pending',
                'score': security_auditor.audit_results.get('overall_score', 0) if security_auditor.audit_results else 0
            },
            'backup': {
                'status': 'healthy' if backup_manager.list_backups() else 'no_backups',
                'last_backup': backup_manager.list_backups()[-1]['timestamp'] if backup_manager.list_backups() else None
            },
            'monitoring': {
                'status': 'active',
                'uptime': app_monitor._calculate_uptime(),
                'alerts': len(app_monitor.get_alerts())
            },
            'overall_status': 'healthy'
        }
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': status
            })
        else:
            return render_template('admin/system_status.html', 
                                 status=status)
                             
    except Exception as e:
        logging.error(f"System status failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/quick-actions')
def quick_actions():
    """Quick action buttons for common tasks"""
    try:
        actions = [
            {
                'name': 'Run Security Audit',
                'url': '/security/audit',
                'method': 'POST',
                'description': 'Perform comprehensive security audit'
            },
            {
                'name': 'Create Backup',
                'url': '/backup/create',
                'method': 'POST',
                'description': 'Create automated backup'
            },
            {
                'name': 'Check System Health',
                'url': '/monitoring/health',
                'method': 'GET',
                'description': 'Check system health status'
            },
            {
                'name': 'View API Docs',
                'url': '/api/docs/',
                'method': 'GET',
                'description': 'View API documentation'
            }
        ]
        
        return render_template('admin/quick_actions.html', 
                             actions=actions)
                             
    except Exception as e:
        logging.error(f"Quick actions failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
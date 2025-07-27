"""
Backup & Recovery Routes for CRM System
Integration of automated backups and data recovery procedures
"""

from flask import Blueprint, request, jsonify, render_template
from app.backup.backup_manager import BackupManager
from app.backup.recovery_manager import RecoveryManager
import logging

bp = Blueprint('backup', __name__, url_prefix='/backup')

# Initialize backup and recovery services
backup_manager = BackupManager()
recovery_manager = RecoveryManager()

@bp.route('/create', methods=['GET', 'POST'])
def create_backup():
    """Create automated backup"""
    try:
        if request.method == 'POST':
            backup_type = request.form.get('backup_type', 'full')
            
            # Create backup
            backup_result = backup_manager.create_automated_backup(backup_type)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': backup_result
                })
            else:
                return render_template('backup/backup_results.html', 
                                     backup_result=backup_result)
        else:
            return render_template('backup/backup_form.html')
            
    except Exception as e:
        logging.error(f"Backup creation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/recover', methods=['GET', 'POST'])
def recover_data():
    """Recover data from backup"""
    try:
        if request.method == 'POST':
            backup_id = request.form.get('backup_id')
            
            # Execute recovery
            recovery_result = recovery_manager.execute_recovery_plan(backup_id)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': recovery_result
                })
            else:
                return render_template('backup/recovery_results.html', 
                                     recovery_result=recovery_result)
        else:
            # Get available backups
            available_backups = backup_manager.list_backups()
            return render_template('backup/recovery_form.html', 
                                 available_backups=available_backups)
            
    except Exception as e:
        logging.error(f"Data recovery failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/list')
def list_backups():
    """List all available backups"""
    try:
        backups = backup_manager.list_backups()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': backups
            })
        else:
            return render_template('backup/backup_list.html', backups=backups)
            
    except Exception as e:
        logging.error(f"Backup listing failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/verify/<backup_id>')
def verify_backup(backup_id):
    """Verify backup integrity"""
    try:
        verification_result = backup_manager.verify_backup(backup_id)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': verification_result
            })
        else:
            return render_template('backup/verification_results.html', 
                                 verification_result=verification_result)
            
    except Exception as e:
        logging.error(f"Backup verification failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/schedule', methods=['GET', 'POST'])
def schedule_backup():
    """Schedule automated backups"""
    try:
        if request.method == 'POST':
            schedule_type = request.form.get('schedule_type', 'daily')
            time = request.form.get('time', '02:00')
            
            # Schedule backup
            schedule_result = backup_manager.schedule_backup(schedule_type, time)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': schedule_result
                })
            else:
                return render_template('backup/schedule_results.html', 
                                     schedule_result=schedule_result)
        else:
            return render_template('backup/schedule_form.html')
            
    except Exception as e:
        logging.error(f"Backup scheduling failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/cleanup', methods=['POST'])
def cleanup_backups():
    """Clean up old backups"""
    try:
        cleanup_result = backup_manager.cleanup_old_backups()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': cleanup_result
            })
        else:
            return render_template('backup/cleanup_results.html', 
                                 cleanup_result=cleanup_result)
            
    except Exception as e:
        logging.error(f"Backup cleanup failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/dashboard')
def backup_dashboard():
    """Backup dashboard"""
    try:
        # Get backup overview
        backups = backup_manager.list_backups()
        
        backup_overview = {
            'total_backups': len(backups),
            'recent_backups': [b for b in backups if b.get('status') == 'success'][:5],
            'failed_backups': [b for b in backups if b.get('status') == 'failed'],
            'total_size': sum(b.get('backup_size', 0) for b in backups),
            'last_backup': max([b.get('timestamp') for b in backups]) if backups else None
        }
        
        return render_template('backup/dashboard.html', 
                             backup_overview=backup_overview)
                             
    except Exception as e:
        logging.error(f"Backup dashboard failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
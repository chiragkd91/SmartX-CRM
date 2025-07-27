"""
Monitoring Routes for CRM System
Integration of application performance monitoring
"""

from flask import Blueprint, request, jsonify, render_template
from app.monitoring.app_monitor import ApplicationMonitor
import logging

bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')

# Initialize monitoring service
app_monitor = ApplicationMonitor()

@bp.route('/dashboard')
def monitoring_dashboard():
    """Application monitoring dashboard"""
    try:
        # Get monitoring data
        monitoring_data = app_monitor.monitor_application()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': monitoring_data
            })
        else:
            return render_template('monitoring/dashboard.html', 
                                 monitoring_data=monitoring_data)
            
    except Exception as e:
        logging.error(f"Monitoring dashboard failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/metrics')
def get_metrics():
    """Get performance metrics"""
    try:
        metrics_summary = app_monitor.get_metrics_summary()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': metrics_summary
            })
        else:
            return render_template('monitoring/metrics.html', 
                                 metrics=metrics_summary)
            
    except Exception as e:
        logging.error(f"Metrics retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/alerts')
def get_alerts():
    """Get system alerts"""
    try:
        severity = request.args.get('severity')
        alerts = app_monitor.get_alerts(severity)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': alerts
            })
        else:
            return render_template('monitoring/alerts.html', alerts=alerts)
            
    except Exception as e:
        logging.error(f"Alerts retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/alerts/clear', methods=['POST'])
def clear_alerts():
    """Clear system alerts"""
    try:
        app_monitor.clear_alerts()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'message': 'Alerts cleared successfully'
            })
        else:
            return render_template('monitoring/alerts_cleared.html')
            
    except Exception as e:
        logging.error(f"Alert clearing failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/health')
def health_check():
    """System health check"""
    try:
        monitoring_data = app_monitor.monitor_application()
        health_status = monitoring_data.get('system_health', {})
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': health_status
            })
        else:
            return render_template('monitoring/health.html', 
                                 health_status=health_status)
            
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/export')
def export_metrics():
    """Export monitoring metrics"""
    try:
        export_format = request.args.get('format', 'json')
        exported_data = app_monitor.export_metrics(export_format)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': exported_data
            })
        else:
            return render_template('monitoring/export.html', 
                                 exported_data=exported_data)
            
    except Exception as e:
        logging.error(f"Metrics export failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/report')
def generate_report():
    """Generate monitoring report"""
    try:
        report = app_monitor.generate_monitoring_report()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': report
            })
        else:
            return render_template('monitoring/report.html', report=report)
            
    except Exception as e:
        logging.error(f"Report generation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
"""
Security Routes for CRM System
Integration of security audit, vulnerability scanning, and penetration testing
"""

from flask import Blueprint, request, jsonify, render_template, current_app
from app.security.security_auditor import SecurityAuditor
from app.security.vulnerability_scanner import VulnerabilityScanner
from app.security.penetration_tester import PenetrationTester
from app.security.security_headers import SecurityHeaders
from app.security.input_validator import InputValidator
import logging

bp = Blueprint('security', __name__, url_prefix='/security')

# Initialize security services
security_auditor = SecurityAuditor()
vulnerability_scanner = VulnerabilityScanner()
penetration_tester = PenetrationTester()
input_validator = InputValidator()

@bp.route('/audit', methods=['GET', 'POST'])
def security_audit():
    """Perform security audit"""
    try:
        if request.method == 'POST':
            # Perform comprehensive security audit
            audit_results = security_auditor.perform_security_audit()
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': audit_results
                })
            else:
                return render_template('security/audit_results.html', 
                                     audit_results=audit_results)
        else:
            return render_template('security/audit_form.html')
            
    except Exception as e:
        logging.error(f"Security audit failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/vulnerability-scan', methods=['GET', 'POST'])
def vulnerability_scan():
    """Perform vulnerability scanning"""
    try:
        if request.method == 'POST':
            scan_type = request.form.get('scan_type', 'full')
            
            if scan_type == 'dependencies':
                scan_results = vulnerability_scanner.scan_dependencies()
            elif scan_type == 'code':
                scan_results = vulnerability_scanner.scan_code_security()
            elif scan_type == 'network':
                scan_results = vulnerability_scanner.scan_network_security()
            else:
                scan_results = vulnerability_scanner.perform_full_scan()
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': scan_results
                })
            else:
                return render_template('security/vulnerability_results.html', 
                                     scan_results=scan_results)
        else:
            return render_template('security/vulnerability_form.html')
            
    except Exception as e:
        logging.error(f"Vulnerability scan failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/penetration-test', methods=['GET', 'POST'])
def penetration_test():
    """Perform penetration testing"""
    try:
        if request.method == 'POST':
            # Perform penetration testing
            test_results = penetration_tester.perform_penetration_test()
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': test_results
                })
            else:
                return render_template('security/penetration_results.html', 
                                     test_results=test_results)
        else:
            return render_template('security/penetration_form.html')
            
    except Exception as e:
        logging.error(f"Penetration test failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/security-headers', methods=['GET', 'POST'])
def configure_security_headers():
    """Configure security headers"""
    try:
        if request.method == 'POST':
            # Configure security headers
            security_headers = SecurityHeaders()
            config_result = security_headers.configure_security_headers(current_app)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': config_result
                })
            else:
                return render_template('security/headers_config.html', 
                                     config_result=config_result)
        else:
            return render_template('security/headers_form.html')
            
    except Exception as e:
        logging.error(f"Security headers configuration failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/input-validation', methods=['GET', 'POST'])
def validate_input():
    """Validate user input"""
    try:
        if request.method == 'POST':
            input_data = request.get_json() if request.is_json else request.form.to_dict()
            input_type = request.args.get('type', 'general')
            
            # Validate input
            validation_result = input_validator.validate_user_input(input_data, input_type)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': validation_result
                })
            else:
                return render_template('security/validation_results.html', 
                                     validation_result=validation_result)
        else:
            return render_template('security/validation_form.html')
            
    except Exception as e:
        logging.error(f"Input validation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/dashboard')
def security_dashboard():
    """Security dashboard"""
    try:
        # Get security overview
        security_overview = {
            'last_audit': security_auditor.audit_results.get('timestamp'),
            'last_scan': vulnerability_scanner.scan_timestamp,
            'last_penetration_test': penetration_tester.test_timestamp,
            'critical_issues': len(security_auditor.critical_issues),
            'vulnerabilities': len(vulnerability_scanner.vulnerabilities),
            'security_score': security_auditor.audit_results.get('overall_score', 0)
        }
        
        return render_template('security/dashboard.html', 
                             security_overview=security_overview)
                             
    except Exception as e:
        logging.error(f"Security dashboard failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/reports')
def security_reports():
    """Generate security reports"""
    try:
        report_type = request.args.get('type', 'all')
        
        reports = {}
        
        if report_type in ['all', 'audit']:
            reports['audit'] = security_auditor.generate_security_report()
            
        if report_type in ['all', 'vulnerability']:
            reports['vulnerability'] = vulnerability_scanner.generate_vulnerability_report()
            
        if report_type in ['all', 'penetration']:
            reports['penetration'] = penetration_tester.generate_penetration_test_report()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': reports
            })
        else:
            return render_template('security/reports.html', reports=reports)
            
    except Exception as e:
        logging.error(f"Security reports failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
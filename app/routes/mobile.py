"""
Mobile Routes for CRM System
Integration of mobile app, cross-platform support, offline functionality, and push notifications
"""

from flask import Blueprint, request, jsonify, render_template
from app.mobile.mobile_app import MobileApp
from app.mobile.cross_platform import CrossPlatformSupport
from app.mobile.offline_manager import OfflineManager
from app.notifications.push_notifications import PushNotificationService
import logging

bp = Blueprint('mobile', __name__, url_prefix='/mobile')

# Initialize mobile services
mobile_app = MobileApp()
cross_platform = CrossPlatformSupport()
offline_manager = OfflineManager()
push_notifications = PushNotificationService()

@bp.route('/manifest')
def get_manifest():
    """Get PWA manifest"""
    try:
        manifest = mobile_app.generate_manifest()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': manifest
            })
        else:
            return manifest, 200, {'Content-Type': 'application/json'}
            
    except Exception as e:
        logging.error(f"Manifest generation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/features')
def get_mobile_features():
    """Get mobile features"""
    try:
        features = mobile_app.get_mobile_features()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': features
            })
        else:
            return render_template('mobile/features.html', features=features)
            
    except Exception as e:
        logging.error(f"Mobile features retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/features/<feature_name>/enable', methods=['POST'])
def enable_feature(feature_name):
    """Enable mobile feature"""
    try:
        success = mobile_app.enable_feature(feature_name)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': success,
                'message': f"Feature {feature_name} {'enabled' if success else 'not found'}"
            })
        else:
            return render_template('mobile/feature_status.html', 
                                 feature_name=feature_name, 
                                 enabled=success)
            
    except Exception as e:
        logging.error(f"Feature enable failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/features/<feature_name>/disable', methods=['POST'])
def disable_feature(feature_name):
    """Disable mobile feature"""
    try:
        success = mobile_app.disable_feature(feature_name)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': success,
                'message': f"Feature {feature_name} {'disabled' if success else 'not found'}"
            })
        else:
            return render_template('mobile/feature_status.html', 
                                 feature_name=feature_name, 
                                 enabled=not success)
            
    except Exception as e:
        logging.error(f"Feature disable failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/platforms')
def get_platforms():
    """Get supported platforms"""
    try:
        platforms = cross_platform.get_cross_platform_config()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': platforms
            })
        else:
            return render_template('mobile/platforms.html', platforms=platforms)
            
    except Exception as e:
        logging.error(f"Platforms retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/platforms/<platform>')
def get_platform_info(platform):
    """Get platform-specific information"""
    try:
        platform_info = cross_platform.get_platform_features(platform)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': platform_info
            })
        else:
            return render_template('mobile/platform_info.html', 
                                 platform=platform, 
                                 platform_info=platform_info)
            
    except Exception as e:
        logging.error(f"Platform info retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/platforms/<platform>/config')
def get_platform_config(platform):
    """Get platform configuration"""
    try:
        config = cross_platform.generate_platform_config(platform)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': config
            })
        else:
            return config, 200, {'Content-Type': 'application/json'}
            
    except Exception as e:
        logging.error(f"Platform config generation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/offline/data', methods=['GET', 'POST'])
def offline_data():
    """Handle offline data operations"""
    try:
        if request.method == 'POST':
            data_type = request.form.get('data_type')
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            success = offline_manager.store_offline_data(data_type, data)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': success,
                    'message': f"Data {'stored' if success else 'not stored'} for offline access"
                })
            else:
                return render_template('mobile/offline_status.html', 
                                     data_type=data_type, 
                                     stored=success)
        else:
            data_type = request.args.get('type')
            offline_data = offline_manager.get_offline_data(data_type)
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'success': True,
                    'data': offline_data
                })
            else:
                return render_template('mobile/offline_data.html', 
                                     offline_data=offline_data)
            
    except Exception as e:
        logging.error(f"Offline data operation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/offline/sync', methods=['POST'])
def sync_offline_data():
    """Synchronize offline data"""
    try:
        sync_results = offline_manager.sync_data()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': sync_results
            })
        else:
            return render_template('mobile/sync_results.html', 
                                 sync_results=sync_results)
            
    except Exception as e:
        logging.error(f"Offline sync failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/offline/status')
def get_offline_status():
    """Get offline sync status"""
    try:
        status = offline_manager.get_sync_status()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': status
            })
        else:
            return render_template('mobile/offline_status.html', 
                                 status=status)
            
    except Exception as e:
        logging.error(f"Offline status retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/notifications/send', methods=['POST'])
def send_push_notification():
    """Send push notification"""
    try:
        title = request.form.get('title')
        message = request.form.get('message')
        recipients = request.form.getlist('recipients')
        platform = request.form.get('platform', 'all')
        data = request.get_json() if request.is_json else {}
        
        notification = push_notifications.send_push_notification(
            title=title,
            message=message,
            recipients=recipients,
            platform=platform,
            data=data
        )
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': notification
            })
        else:
            return render_template('mobile/notification_sent.html', 
                                 notification=notification)
            
    except Exception as e:
        logging.error(f"Push notification failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/notifications/subscribe', methods=['POST'])
def subscribe_notifications():
    """Subscribe to push notifications"""
    try:
        user_id = request.form.get('user_id')
        platform = request.form.get('platform')
        token = request.form.get('token')
        
        success = push_notifications.subscribe_user(user_id, platform, token)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': success,
                'message': f"User {'subscribed' if success else 'not subscribed'} to notifications"
            })
        else:
            return render_template('mobile/subscription_status.html', 
                                 user_id=user_id, 
                                 platform=platform, 
                                 subscribed=success)
            
    except Exception as e:
        logging.error(f"Notification subscription failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/notifications/history')
def get_notification_history():
    """Get notification history"""
    try:
        user_id = request.args.get('user_id')
        limit = int(request.args.get('limit', 50))
        
        history = push_notifications.get_notification_history(user_id, limit)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'data': history
            })
        else:
            return render_template('mobile/notification_history.html', 
                                 history=history)
            
    except Exception as e:
        logging.error(f"Notification history retrieval failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/dashboard')
def mobile_dashboard():
    """Mobile dashboard"""
    try:
        dashboard_data = {
            'mobile_features': mobile_app.get_mobile_features(),
            'platforms': cross_platform.get_cross_platform_config(),
            'offline_status': offline_manager.get_sync_status(),
            'notification_config': push_notifications.notification_config
        }
        
        return render_template('mobile/dashboard.html', 
                             dashboard_data=dashboard_data)
                             
    except Exception as e:
        logging.error(f"Mobile dashboard failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}) 
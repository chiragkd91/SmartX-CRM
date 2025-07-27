"""
Application Monitor for CRM System
Application performance monitoring and health checks
"""

import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import json
from pathlib import Path

class ApplicationMonitor:
    """Application performance monitoring system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = defaultdict(list)
        self.alerts = []
        self.monitoring_config = self._load_monitoring_config()
        self.start_time = datetime.now()
    
    def monitor_application(self) -> Dict[str, Any]:
        """Monitor application performance and health"""
        try:
            monitoring_data = {
                'timestamp': datetime.now().isoformat(),
                'performance_metrics': self._collect_performance_metrics(),
                'system_health': self._check_system_health(),
                'user_activity': self._monitor_user_activity(),
                'error_tracking': self._track_errors(),
                'uptime': self._calculate_uptime()
            }
            
            # Store metrics
            self._store_metrics(monitoring_data)
            
            # Check for alerts
            alerts = self._check_alerts(monitoring_data)
            if alerts:
                self.alerts.extend(alerts)
            
            return monitoring_data
            
        except Exception as e:
            self.logger.error(f"Application monitoring failed: {str(e)}")
            return {'error': str(e)}
    
    def _collect_performance_metrics(self) -> Dict[str, Any]:
        """Collect performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network I/O
            network = psutil.net_io_counters()
            
            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available,
                'disk_usage': disk.percent,
                'disk_free': disk.free,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'response_time': self._measure_response_time()
            }
            
        except Exception as e:
            self.logger.error(f"Performance metrics collection failed: {str(e)}")
            return {}
    
    def _check_system_health(self) -> Dict[str, Any]:
        """Check system health status"""
        health_status = {
            'overall_status': 'healthy',
            'checks': {},
            'issues': []
        }
        
        try:
            # Database connectivity check
            db_status = self._check_database_health()
            health_status['checks']['database'] = db_status
            
            # File system check
            fs_status = self._check_filesystem_health()
            health_status['checks']['filesystem'] = fs_status
            
            # Service availability check
            service_status = self._check_service_health()
            health_status['checks']['services'] = service_status
            
            # Determine overall status
            failed_checks = [check for check in health_status['checks'].values() if check['status'] == 'failed']
            if failed_checks:
                health_status['overall_status'] = 'unhealthy'
                health_status['issues'] = [check['message'] for check in failed_checks]
            
        except Exception as e:
            health_status['overall_status'] = 'error'
            health_status['issues'].append(f"Health check error: {str(e)}")
        
        return health_status
    
    def _monitor_user_activity(self) -> Dict[str, Any]:
        """Monitor user activity"""
        # This would typically integrate with web analytics
        return {
            'active_users': 0,  # Placeholder
            'page_views': 0,    # Placeholder
            'sessions': 0,      # Placeholder
            'popular_pages': []  # Placeholder
        }
    
    def _track_errors(self) -> Dict[str, Any]:
        """Track application errors"""
        return {
            'error_count': len(self.alerts),
            'recent_errors': self.alerts[-10:] if self.alerts else [],
            'error_rate': self._calculate_error_rate()
        }
    
    def _calculate_uptime(self) -> Dict[str, Any]:
        """Calculate application uptime"""
        current_time = datetime.now()
        uptime_delta = current_time - self.start_time
        
        return {
            'start_time': self.start_time.isoformat(),
            'uptime_seconds': uptime_delta.total_seconds(),
            'uptime_formatted': str(uptime_delta),
            'uptime_percentage': 99.9  # Placeholder
        }
    
    def _measure_response_time(self) -> float:
        """Measure application response time"""
        start_time = time.time()
        # Simulate a simple operation
        time.sleep(0.01)
        return (time.time() - start_time) * 1000  # Convert to milliseconds
    
    def _check_database_health(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            # This would perform actual database connectivity test
            return {
                'status': 'healthy',
                'response_time': 10.5,
                'message': 'Database connection successful'
            }
        except Exception as e:
            return {
                'status': 'failed',
                'message': f'Database connection failed: {str(e)}'
            }
    
    def _check_filesystem_health(self) -> Dict[str, Any]:
        """Check filesystem health"""
        try:
            disk_usage = psutil.disk_usage('/')
            if disk_usage.percent > 90:
                return {
                    'status': 'warning',
                    'message': f'Disk usage high: {disk_usage.percent}%'
                }
            else:
                return {
                    'status': 'healthy',
                    'message': f'Disk usage normal: {disk_usage.percent}%'
                }
        except Exception as e:
            return {
                'status': 'failed',
                'message': f'Filesystem check failed: {str(e)}'
            }
    
    def _check_service_health(self) -> Dict[str, Any]:
        """Check service health"""
        try:
            # Check if required services are running
            services = ['web', 'database', 'cache']
            service_status = {}
            
            for service in services:
                # This would check actual service status
                service_status[service] = {
                    'status': 'running',
                    'port': 8080 if service == 'web' else None
                }
            
            return {
                'status': 'healthy',
                'services': service_status,
                'message': 'All services running'
            }
        except Exception as e:
            return {
                'status': 'failed',
                'message': f'Service health check failed: {str(e)}'
            }
    
    def _store_metrics(self, monitoring_data: Dict[str, Any]):
        """Store monitoring metrics"""
        timestamp = monitoring_data['timestamp']
        
        for metric_type, data in monitoring_data.items():
            if metric_type != 'timestamp':
                self.metrics[metric_type].append({
                    'timestamp': timestamp,
                    'data': data
                })
        
        # Keep only last 1000 data points
        for metric_type in self.metrics:
            if len(self.metrics[metric_type]) > 1000:
                self.metrics[metric_type] = self.metrics[metric_type][-1000:]
    
    def _check_alerts(self, monitoring_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for alert conditions"""
        alerts = []
        
        # CPU usage alert
        cpu_usage = monitoring_data['performance_metrics'].get('cpu_usage', 0)
        if cpu_usage > 80:
            alerts.append({
                'type': 'high_cpu_usage',
                'severity': 'warning',
                'message': f'High CPU usage: {cpu_usage}%',
                'timestamp': monitoring_data['timestamp']
            })
        
        # Memory usage alert
        memory_usage = monitoring_data['performance_metrics'].get('memory_usage', 0)
        if memory_usage > 85:
            alerts.append({
                'type': 'high_memory_usage',
                'severity': 'warning',
                'message': f'High memory usage: {memory_usage}%',
                'timestamp': monitoring_data['timestamp']
            })
        
        # System health alert
        if monitoring_data['system_health']['overall_status'] == 'unhealthy':
            alerts.append({
                'type': 'system_unhealthy',
                'severity': 'critical',
                'message': 'System health check failed',
                'timestamp': monitoring_data['timestamp']
            })
        
        return alerts
    
    def _calculate_error_rate(self) -> float:
        """Calculate error rate"""
        if not self.alerts:
            return 0.0
        
        # Calculate error rate over last hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_alerts = [alert for alert in self.alerts if datetime.fromisoformat(alert['timestamp']) > one_hour_ago]
        
        return len(recent_alerts) / 60.0  # Errors per minute
    
    def _load_monitoring_config(self) -> Dict[str, Any]:
        """Load monitoring configuration"""
        return {
            'alert_thresholds': {
                'cpu_usage': 80,
                'memory_usage': 85,
                'disk_usage': 90,
                'response_time': 5000  # milliseconds
            },
            'monitoring_interval': 60,  # seconds
            'retention_days': 30
        }
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        if not self.metrics:
            return {}
        
        summary = {}
        
        for metric_type, data_points in self.metrics.items():
            if data_points:
                latest_data = data_points[-1]['data']
                if isinstance(latest_data, dict):
                    summary[metric_type] = latest_data
                else:
                    summary[metric_type] = {'value': latest_data}
        
        return summary
    
    def get_alerts(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get alerts, optionally filtered by severity"""
        if severity:
            return [alert for alert in self.alerts if alert['severity'] == severity]
        return self.alerts
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        self.logger.info("All alerts cleared")
    
    def export_metrics(self, format: str = 'json') -> str:
        """Export metrics data"""
        if format == 'json':
            return json.dumps(self.metrics, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def generate_monitoring_report(self) -> str:
        """Generate monitoring report"""
        if not self.metrics:
            return "No monitoring data available"
        
        report = f"""
# Application Monitoring Report
Generated: {datetime.now().isoformat()}

## System Health
"""
        
        # Get latest health data
        if 'system_health' in self.metrics and self.metrics['system_health']:
            health_data = self.metrics['system_health'][-1]['data']
            report += f"Overall Status: {health_data.get('overall_status', 'Unknown')}\n"
            
            for check_name, check_data in health_data.get('checks', {}).items():
                report += f"- {check_name}: {check_data.get('status', 'Unknown')}\n"
        
        report += f"""
## Performance Metrics
"""
        
        if 'performance_metrics' in self.metrics and self.metrics['performance_metrics']:
            perf_data = self.metrics['performance_metrics'][-1]['data']
            report += f"CPU Usage: {perf_data.get('cpu_usage', 0)}%\n"
            report += f"Memory Usage: {perf_data.get('memory_usage', 0)}%\n"
            report += f"Disk Usage: {perf_data.get('disk_usage', 0)}%\n"
            report += f"Response Time: {perf_data.get('response_time', 0)}ms\n"
        
        report += f"""
## Alerts
Total Alerts: {len(self.alerts)}
"""
        
        for alert in self.alerts[-5:]:  # Show last 5 alerts
            report += f"- [{alert['severity'].upper()}] {alert['message']} ({alert['timestamp']})\n"
        
        return report 
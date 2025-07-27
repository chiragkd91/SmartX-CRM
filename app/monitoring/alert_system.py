"""
Alert System Module
Handles system alerts and notifications
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import logging


class AlertSystem:
    """Handles system alerts and notifications"""
    
    def __init__(self):
        self.alerts = []
        self.logger = logging.getLogger(__name__)
    
    def create_alert(self, level: str, message: str, source: str = "system") -> Dict[str, Any]:
        """Create a new alert"""
        alert = {
            'id': len(self.alerts) + 1,
            'level': level,
            'message': message,
            'source': source,
            'timestamp': datetime.now(),
            'acknowledged': False
        }
        self.alerts.append(alert)
        self.logger.warning(f"Alert created: {level} - {message}")
        return alert
    
    def get_alerts(self, level: Optional[str] = None, acknowledged: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get alerts with optional filtering"""
        filtered_alerts = self.alerts
        
        if level:
            filtered_alerts = [a for a in filtered_alerts if a['level'] == level]
        
        if acknowledged is not None:
            filtered_alerts = [a for a in filtered_alerts if a['acknowledged'] == acknowledged]
        
        return filtered_alerts
    
    def acknowledge_alert(self, alert_id: int) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                return True
        return False
    
    def clear_old_alerts(self, days: int = 30):
        """Clear alerts older than specified days"""
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
        
        self.alerts = [a for a in self.alerts if a['timestamp'] > cutoff_date]
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary statistics"""
        total_alerts = len(self.alerts)
        unacknowledged = len([a for a in self.alerts if not a['acknowledged']])
        
        level_counts = {}
        for alert in self.alerts:
            level = alert['level']
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            'total_alerts': total_alerts,
            'unacknowledged': unacknowledged,
            'level_counts': level_counts
        } 
"""
Performance Tracker Module
Tracks application performance metrics
"""

import time
import psutil
from datetime import datetime
from typing import Dict, List, Any


class PerformanceTracker:
    """Tracks application performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'uptime': time.time() - self.start_time
        }
    
    def track_request(self, endpoint: str, duration: float):
        """Track request performance"""
        if endpoint not in self.metrics:
            self.metrics[endpoint] = []
        
        self.metrics[endpoint].append({
            'timestamp': datetime.now(),
            'duration': duration
        })
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        summary = {}
        for endpoint, requests in self.metrics.items():
            if requests:
                durations = [r['duration'] for r in requests]
                summary[endpoint] = {
                    'total_requests': len(requests),
                    'avg_duration': sum(durations) / len(durations),
                    'min_duration': min(durations),
                    'max_duration': max(durations)
                }
        return summary 
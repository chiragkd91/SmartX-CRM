"""
Backup Module for CRM System
Automated backup and recovery management
"""

from .backup_manager import BackupManager
from .recovery_manager import RecoveryManager

__all__ = ['BackupManager', 'RecoveryManager'] 
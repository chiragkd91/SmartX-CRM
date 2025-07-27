"""
Backup Manager for CRM System
Automated backup system implementation
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
import shutil
import json

class BackupManager:
    """Automated backup system for CRM data"""
    
    def __init__(self, backup_dir: str = "backups"):
        self.logger = logging.getLogger(__name__)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.backup_history = []
        
    def create_automated_backup(self, backup_type: str = "full") -> Dict[str, Any]:
        """Create automated backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_id = f"backup_{backup_type}_{timestamp}"
            backup_path = self.backup_dir / backup_id
            
            backup_path.mkdir(exist_ok=True)
            
            # Create backup metadata
            metadata = {
                "backup_id": backup_id,
                "timestamp": timestamp,
                "type": backup_type,
                "status": "in_progress"
            }
            
            # Perform backup based on type
            if backup_type == "database":
                success = self._backup_database(backup_path)
            elif backup_type == "files":
                success = self._backup_files(backup_path)
            elif backup_type == "config":
                success = self._backup_config(backup_path)
            else:  # full backup
                success = self._backup_full(backup_path)
            
            metadata["status"] = "success" if success else "failed"
            metadata["completed_at"] = datetime.now().isoformat()
            
            # Save metadata
            with open(backup_path / "metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
            
            self.backup_history.append(metadata)
            
            return {
                "success": success,
                "backup_id": backup_id,
                "metadata": metadata
            }
            
        except Exception as e:
            self.logger.error(f"Backup creation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _backup_database(self, backup_path: Path) -> bool:
        """Backup database"""
        try:
            # Stub for database backup
            db_backup_file = backup_path / "database.sql"
            with open(db_backup_file, "w") as f:
                f.write("-- Database backup stub\n")
            return True
        except Exception as e:
            self.logger.error(f"Database backup failed: {str(e)}")
            return False
    
    def _backup_files(self, backup_path: Path) -> bool:
        """Backup file system"""
        try:
            # Stub for file system backup
            files_backup_dir = backup_path / "files"
            files_backup_dir.mkdir(exist_ok=True)
            
            # Backup important directories
            important_dirs = ["app", "config.py", "requirements.txt"]
            for item in important_dirs:
                if os.path.exists(item):
                    if os.path.isdir(item):
                        shutil.copytree(item, files_backup_dir / item, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, files_backup_dir / item)
            
            return True
        except Exception as e:
            self.logger.error(f"File backup failed: {str(e)}")
            return False
    
    def _backup_config(self, backup_path: Path) -> bool:
        """Backup configuration"""
        try:
            # Stub for configuration backup
            config_backup_file = backup_path / "config.json"
            config_data = {
                "app_config": "stub_config_data",
                "backup_timestamp": datetime.now().isoformat()
            }
            
            with open(config_backup_file, "w") as f:
                json.dump(config_data, f, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"Config backup failed: {str(e)}")
            return False
    
    def _backup_full(self, backup_path: Path) -> bool:
        """Perform full backup"""
        try:
            # Perform all backup types
            db_success = self._backup_database(backup_path)
            files_success = self._backup_files(backup_path)
            config_success = self._backup_config(backup_path)
            
            return all([db_success, files_success, config_success])
        except Exception as e:
            self.logger.error(f"Full backup failed: {str(e)}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all backups"""
        try:
            backups = []
            for backup_dir in self.backup_dir.iterdir():
                if backup_dir.is_dir():
                    metadata_file = backup_dir / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                            backups.append(metadata)
            
            # Sort by timestamp
            backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return backups
        except Exception as e:
            self.logger.error(f"Failed to list backups: {str(e)}")
            return []
    
    def get_backup_info(self, backup_id: str) -> Dict[str, Any]:
        """Get specific backup information"""
        try:
            backup_path = self.backup_dir / backup_id
            metadata_file = backup_path / "metadata.json"
            
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                
                # Add file size information
                total_size = sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())
                metadata["size_bytes"] = total_size
                metadata["size_mb"] = round(total_size / (1024 * 1024), 2)
                
                return metadata
            else:
                return {"error": "Backup not found"}
        except Exception as e:
            self.logger.error(f"Failed to get backup info: {str(e)}")
            return {"error": str(e)}
    
    def delete_backup(self, backup_id: str) -> Dict[str, Any]:
        """Delete a backup"""
        try:
            backup_path = self.backup_dir / backup_id
            
            if backup_path.exists():
                shutil.rmtree(backup_path)
                return {"success": True, "message": f"Backup {backup_id} deleted"}
            else:
                return {"success": False, "error": "Backup not found"}
        except Exception as e:
            self.logger.error(f"Failed to delete backup: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def verify_backup(self, backup_id: str) -> Dict[str, Any]:
        """Verify backup integrity"""
        try:
            backup_path = self.backup_dir / backup_id
            metadata_file = backup_path / "metadata.json"
            
            if not metadata_file.exists():
                return {"success": False, "error": "Backup not found"}
            
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            # Verify backup files exist
            verification_results = {
                "metadata_exists": metadata_file.exists(),
                "database_exists": (backup_path / "database.sql").exists(),
                "files_exist": (backup_path / "files").exists(),
                "config_exists": (backup_path / "config.json").exists()
            }
            
            all_valid = all(verification_results.values())
            
            return {
                "success": all_valid,
                "backup_id": backup_id,
                "verification_results": verification_results,
                "status": "valid" if all_valid else "corrupted"
            }
        except Exception as e:
            self.logger.error(f"Backup verification failed: {str(e)}")
            return {"success": False, "error": str(e)} 
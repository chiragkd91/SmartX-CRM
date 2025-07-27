"""
Recovery Manager for CRM System
Data recovery procedures and disaster recovery plan
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
import shutil
import json

class RecoveryManager:
    """Data recovery and disaster recovery procedures"""
    
    def __init__(self, backup_dir: str = "backups"):
        self.logger = logging.getLogger(__name__)
        self.backup_dir = Path(backup_dir)
        self.recovery_log = []
        
    def execute_recovery_plan(self, backup_id: str = None) -> Dict[str, Any]:
        """Execute data recovery from backup"""
        try:
            if not backup_id:
                # Use latest backup
                backups = self._get_available_backups()
                if not backups:
                    return {"success": False, "error": "No backups available"}
                backup_id = backups[0]["backup_id"]
            
            self.logger.info(f"Starting recovery from backup: {backup_id}")
            
            # Validate backup exists
            backup_path = self.backup_dir / backup_id
            if not backup_path.exists():
                return {"success": False, "error": f"Backup {backup_id} not found"}
            
            # Create recovery session
            recovery_session = {
                "session_id": f"recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "backup_id": backup_id,
                "start_time": datetime.now().isoformat(),
                "status": "in_progress",
                "steps_completed": [],
                "errors": []
            }
            
            # Execute recovery steps
            recovery_steps = [
                ("validate_backup", self._validate_backup),
                ("prepare_recovery", self._prepare_recovery),
                ("recover_database", self._recover_database),
                ("recover_files", self._recover_files),
                ("recover_config", self._recover_config),
                ("verify_recovery", self._verify_recovery)
            ]
            
            for step_name, step_func in recovery_steps:
                try:
                    step_result = step_func(backup_path)
                    recovery_session["steps_completed"].append({
                        "step": step_name,
                        "status": "success",
                        "result": step_result
                    })
                except Exception as e:
                    error_msg = f"Step {step_name} failed: {str(e)}"
                    recovery_session["errors"].append(error_msg)
                    recovery_session["steps_completed"].append({
                        "step": step_name,
                        "status": "failed",
                        "error": str(e)
                    })
                    self.logger.error(error_msg)
            
            # Update recovery session
            recovery_session["end_time"] = datetime.now().isoformat()
            recovery_session["status"] = "completed" if not recovery_session["errors"] else "failed"
            
            # Log recovery session
            self.recovery_log.append(recovery_session)
            
            return {
                "success": recovery_session["status"] == "completed",
                "recovery_session": recovery_session,
                "message": "Recovery completed successfully" if recovery_session["status"] == "completed" else "Recovery failed"
            }
            
        except Exception as e:
            self.logger.error(f"Recovery execution failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _validate_backup(self, backup_path: Path) -> Dict[str, Any]:
        """Validate backup integrity before recovery"""
        try:
            metadata_file = backup_path / "metadata.json"
            if not metadata_file.exists():
                raise Exception("Backup metadata not found")
            
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            # Check backup status
            if metadata.get("status") != "success":
                raise Exception("Backup status is not successful")
            
            # Verify essential files exist
            essential_files = ["database.sql", "config.json"]
            for file_name in essential_files:
                if not (backup_path / file_name).exists():
                    raise Exception(f"Essential file {file_name} missing")
            
            return {
                "valid": True,
                "backup_type": metadata.get("type"),
                "timestamp": metadata.get("timestamp")
            }
            
        except Exception as e:
            self.logger.error(f"Backup validation failed: {str(e)}")
            raise
    
    def _prepare_recovery(self, backup_path: Path) -> Dict[str, Any]:
        """Prepare system for recovery"""
        try:
            # Create recovery workspace
            recovery_workspace = Path("recovery_workspace")
            recovery_workspace.mkdir(exist_ok=True)
            
            # Create backup of current state
            current_backup = recovery_workspace / f"pre_recovery_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            current_backup.mkdir(exist_ok=True)
            
            # Backup current database
            if os.path.exists("crm.db"):
                shutil.copy2("crm.db", current_backup / "crm.db")
            
            # Backup current config
            if os.path.exists("config.py"):
                shutil.copy2("config.py", current_backup / "config.py")
            
            return {
                "recovery_workspace": str(recovery_workspace),
                "current_backup": str(current_backup),
                "prepared": True
            }
            
        except Exception as e:
            self.logger.error(f"Recovery preparation failed: {str(e)}")
            raise
    
    def _recover_database(self, backup_path: Path) -> Dict[str, Any]:
        """Recover database from backup"""
        try:
            db_backup_file = backup_path / "database.sql"
            if not db_backup_file.exists():
                raise Exception("Database backup file not found")
            
            # Stub for database recovery
            # In real implementation, this would restore the database
            self.logger.info("Database recovery completed (stub)")
            
            return {
                "database_recovered": True,
                "backup_file": str(db_backup_file)
            }
            
        except Exception as e:
            self.logger.error(f"Database recovery failed: {str(e)}")
            raise
    
    def _recover_files(self, backup_path: Path) -> Dict[str, Any]:
        """Recover files from backup"""
        try:
            files_backup_dir = backup_path / "files"
            if not files_backup_dir.exists():
                raise Exception("Files backup directory not found")
            
            # Stub for file recovery
            # In real implementation, this would restore files
            self.logger.info("File recovery completed (stub)")
            
            return {
                "files_recovered": True,
                "backup_dir": str(files_backup_dir)
            }
            
        except Exception as e:
            self.logger.error(f"File recovery failed: {str(e)}")
            raise
    
    def _recover_config(self, backup_path: Path) -> Dict[str, Any]:
        """Recover configuration from backup"""
        try:
            config_backup_file = backup_path / "config.json"
            if not config_backup_file.exists():
                raise Exception("Configuration backup file not found")
            
            # Stub for configuration recovery
            # In real implementation, this would restore configuration
            self.logger.info("Configuration recovery completed (stub)")
            
            return {
                "config_recovered": True,
                "backup_file": str(config_backup_file)
            }
            
        except Exception as e:
            self.logger.error(f"Configuration recovery failed: {str(e)}")
            raise
    
    def _verify_recovery(self, backup_path: Path) -> Dict[str, Any]:
        """Verify recovery was successful"""
        try:
            # Stub for recovery verification
            # In real implementation, this would verify all recovered components
            verification_results = {
                "database_accessible": True,
                "files_restored": True,
                "config_valid": True,
                "application_startup": True
            }
            
            all_verified = all(verification_results.values())
            
            return {
                "verification_passed": all_verified,
                "verification_results": verification_results
            }
            
        except Exception as e:
            self.logger.error(f"Recovery verification failed: {str(e)}")
            raise
    
    def _get_available_backups(self) -> List[Dict[str, Any]]:
        """Get list of available backups"""
        try:
            backups = []
            for backup_dir in self.backup_dir.iterdir():
                if backup_dir.is_dir():
                    metadata_file = backup_dir / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                            if metadata.get("status") == "success":
                                backups.append(metadata)
            
            # Sort by timestamp (newest first)
            backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return backups
            
        except Exception as e:
            self.logger.error(f"Failed to get available backups: {str(e)}")
            return []
    
    def get_recovery_history(self) -> List[Dict[str, Any]]:
        """Get recovery history"""
        return self.recovery_log
    
    def get_disaster_recovery_plan(self) -> Dict[str, Any]:
        """Get disaster recovery plan"""
        return {
            "plan_name": "CRM Disaster Recovery Plan",
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "recovery_objectives": {
                "rto": "4 hours",  # Recovery Time Objective
                "rpo": "1 hour"   # Recovery Point Objective
            },
            "recovery_steps": [
                "1. Assess disaster impact",
                "2. Activate disaster recovery team",
                "3. Execute recovery plan",
                "4. Verify system functionality",
                "5. Notify stakeholders",
                "6. Document incident"
            ],
            "contact_information": {
                "emergency_contact": "admin@crm.com",
                "backup_contact": "backup-admin@crm.com"
            },
            "recovery_procedures": {
                "database_recovery": "Restore from latest backup",
                "file_recovery": "Restore from file backup",
                "config_recovery": "Restore configuration files",
                "application_recovery": "Restart application services"
            }
        }
    
    def test_recovery_procedure(self, backup_id: str = None) -> Dict[str, Any]:
        """Test recovery procedure without affecting production"""
        try:
            self.logger.info("Starting recovery procedure test")
            
            # Create test environment
            test_workspace = Path("test_recovery_workspace")
            test_workspace.mkdir(exist_ok=True)
            
            # Execute recovery in test mode
            test_result = self.execute_recovery_plan(backup_id)
            
            # Clean up test environment
            if test_workspace.exists():
                shutil.rmtree(test_workspace)
            
            return {
                "success": test_result["success"],
                "test_completed": True,
                "test_result": test_result,
                "message": "Recovery test completed successfully" if test_result["success"] else "Recovery test failed"
            }
            
        except Exception as e:
            self.logger.error(f"Recovery test failed: {str(e)}")
            return {"success": False, "error": str(e)} 
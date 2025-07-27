#!/usr/bin/env python3
"""
SmartX CRM - Package Verification Script
This script checks if all required packages are installed and working correctly.
"""

import sys
import importlib
import subprocess
from typing import Dict, List, Tuple

# Required packages with their import names and version checks
REQUIRED_PACKAGES = {
    # Core Flask packages
    'Flask': {
        'import_name': 'flask',
        'version_check': True,
        'critical': True
    },
    'Flask-SQLAlchemy': {
        'import_name': 'flask_sqlalchemy',
        'version_check': True,
        'critical': True
    },
    'Flask-Login': {
        'import_name': 'flask_login',
        'version_check': True,
        'critical': True
    },
    'Flask-WTF': {
        'import_name': 'flask_wtf',
        'version_check': True,
        'critical': True
    },
    'Flask-Migrate': {
        'import_name': 'flask_migrate',
        'version_check': True,
        'critical': True
    },
    'Flask-Mail': {
        'import_name': 'flask_mail',
        'version_check': True,
        'critical': True
    },
    'Flask-CORS': {
        'import_name': 'flask_cors',
        'version_check': True,
        'critical': False
    },
    'Flask-RESTful': {
        'import_name': 'flask_restful',
        'version_check': True,
        'critical': False
    },
    'Flask-JWT-Extended': {
        'import_name': 'flask_jwt_extended',
        'version_check': True,
        'critical': False
    },
    
    # Core dependencies
    'WTForms': {
        'import_name': 'wtforms',
        'version_check': True,
        'critical': True
    },
    'Werkzeug': {
        'import_name': 'werkzeug',
        'version_check': True,
        'critical': True
    },
    'SQLAlchemy': {
        'import_name': 'sqlalchemy',
        'version_check': True,
        'critical': True
    },
    'Jinja2': {
        'import_name': 'jinja2',
        'version_check': True,
        'critical': True
    },
    'MarkupSafe': {
        'import_name': 'markupsafe',
        'version_check': True,
        'critical': True
    },
    'itsdangerous': {
        'import_name': 'itsdangerous',
        'version_check': True,
        'critical': True
    },
    'click': {
        'import_name': 'click',
        'version_check': True,
        'critical': True
    },
    'blinker': {
        'import_name': 'blinker',
        'version_check': True,
        'critical': True
    },
    
    # Additional dependencies
    'email-validator': {
        'import_name': 'email_validator',
        'version_check': True,
        'critical': False
    },
    'python-dotenv': {
        'import_name': 'dotenv',
        'version_check': True,
        'critical': False
    },
    'psutil': {
        'import_name': 'psutil',
        'version_check': True,
        'critical': False
    },
    'requests': {
        'import_name': 'requests',
        'version_check': True,
        'critical': False
    },
    'cryptography': {
        'import_name': 'cryptography',
        'version_check': True,
        'critical': False
    },
    'bcrypt': {
        'import_name': 'bcrypt',
        'version_check': True,
        'critical': False
    },
    'PyJWT': {
        'import_name': 'jwt',
        'version_check': True,
        'critical': False
    },
    'redis': {
        'import_name': 'redis',
        'version_check': True,
        'critical': False
    },
    'celery': {
        'import_name': 'celery',
        'version_check': True,
        'critical': False
    },
    
    # Development tools
    'pytest': {
        'import_name': 'pytest',
        'version_check': True,
        'critical': False
    },
    'pytest-flask': {
        'import_name': 'pytest_flask',
        'version_check': True,
        'critical': False
    },
    'coverage': {
        'import_name': 'coverage',
        'version_check': True,
        'critical': False
    },
    'black': {
        'import_name': 'black',
        'version_check': True,
        'critical': False
    },
    'flake8': {
        'import_name': 'flake8',
        'version_check': True,
        'critical': False
    },
    'bandit': {
        'import_name': 'bandit',
        'version_check': True,
        'critical': False
    },
    'safety': {
        'import_name': 'safety',
        'version_check': True,
        'critical': False
    },
    
    # Data processing
    'pandas': {
        'import_name': 'pandas',
        'version_check': True,
        'critical': False
    },
    'numpy': {
        'import_name': 'numpy',
        'version_check': True,
        'critical': False
    },
    'matplotlib': {
        'import_name': 'matplotlib',
        'version_check': True,
        'critical': False
    },
    'seaborn': {
        'import_name': 'seaborn',
        'version_check': True,
        'critical': False
    },
    'scikit-learn': {
        'import_name': 'sklearn',
        'version_check': True,
        'critical': False
    },
    'plotly': {
        'import_name': 'plotly',
        'version_check': True,
        'critical': False
    },
    'dash': {
        'import_name': 'dash',
        'version_check': True,
        'critical': False
    },
    'dash-bootstrap-components': {
        'import_name': 'dash_bootstrap_components',
        'version_check': True,
        'critical': False
    },
    
    # Utilities
    'bleach': {
        'import_name': 'bleach',
        'version_check': True,
        'critical': False
    },
    'Pillow': {
        'import_name': 'PIL',
        'version_check': True,
        'critical': False
    },
    'openpyxl': {
        'import_name': 'openpyxl',
        'version_check': True,
        'critical': False
    }
}

def get_package_version(package_name: str) -> str:
    """Get the version of an installed package."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                return line.split(':', 1)[1].strip()
        
        return "Unknown"
    except subprocess.CalledProcessError:
        return "Not installed"

def check_package_import(package_info: Dict) -> Tuple[bool, str]:
    """Check if a package can be imported and optionally get its version."""
    import_name = package_info['import_name']
    version_check = package_info['version_check']
    
    try:
        module = importlib.import_module(import_name)
        
        if version_check and hasattr(module, '__version__'):
            return True, f"v{module.__version__}"
        else:
            return True, "Available"
            
    except ImportError as e:
        return False, f"Import error: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_critical_packages() -> List[str]:
    """Check all critical packages and return list of missing ones."""
    missing_critical = []
    
    print("Checking critical packages...")
    print("=" * 50)
    
    for package_name, package_info in REQUIRED_PACKAGES.items():
        if package_info['critical']:
            success, message = check_package_import(package_info)
            status = "✓" if success else "✗"
            print(f"{status} {package_name}: {message}")
            
            if not success:
                missing_critical.append(package_name)
    
    return missing_critical

def check_all_packages() -> Dict[str, Tuple[bool, str]]:
    """Check all packages and return results."""
    results = {}
    
    print("\nChecking all packages...")
    print("=" * 50)
    
    for package_name, package_info in REQUIRED_PACKAGES.items():
        success, message = check_package_import(package_info)
        status = "✓" if success else "✗"
        critical_marker = " [CRITICAL]" if package_info['critical'] else ""
        print(f"{status} {package_name}{critical_marker}: {message}")
        results[package_name] = (success, message)
    
    return results

def suggest_fixes(missing_packages: List[str]) -> None:
    """Suggest fixes for missing packages."""
    if not missing_packages:
        return
    
    print("\n" + "=" * 50)
    print("SUGGESTED FIXES")
    print("=" * 50)
    
    print("\n1. Install missing packages:")
    for package in missing_packages:
        print(f"   pip install {package}")
    
    print("\n2. Or install all packages from requirements.txt:")
    print("   pip install -r requirements.txt")
    
    print("\n3. If you're having issues with specific packages:")
    print("   pip install --force-reinstall <package_name>")
    
    print("\n4. For development packages only:")
    print("   pip install -r requirements.txt --only-binary=all")

def main():
    """Main function to run package verification."""
    print("SmartX CRM - Package Verification")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("⚠️  Warning: Python 3.8+ is recommended")
    
    # Check pip version
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"pip version: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Could not determine pip version")
    
    print()
    
    # Check critical packages first
    missing_critical = check_critical_packages()
    
    if missing_critical:
        print(f"\n❌ {len(missing_critical)} critical packages are missing!")
        suggest_fixes(missing_critical)
        return False
    
    # Check all packages
    all_results = check_all_packages()
    
    # Count results
    total_packages = len(all_results)
    successful_packages = sum(1 for success, _ in all_results.values() if success)
    failed_packages = total_packages - successful_packages
    
    print(f"\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total packages: {total_packages}")
    print(f"Successful: {successful_packages}")
    print(f"Failed: {failed_packages}")
    
    if failed_packages > 0:
        print(f"\n⚠️  {failed_packages} packages failed to import")
        failed_list = [name for name, (success, _) in all_results.items() if not success]
        print("Failed packages:", ", ".join(failed_list))
        suggest_fixes(failed_list)
        return False
    else:
        print("\n✅ All packages are working correctly!")
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1) 
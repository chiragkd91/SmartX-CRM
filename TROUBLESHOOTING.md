# SmartX CRM - Troubleshooting Guide

## 🚨 Common Issues and Solutions

This guide helps you resolve common problems during SmartX CRM setup and installation.

## 📋 Quick Diagnostic

Before diving into specific issues, run our diagnostic script:

```bash
# Windows
python check_packages.py

# Linux/Mac
python3 check_packages.py
```

This will identify missing packages and provide specific solutions.

## 🔧 Python Installation Issues

### Issue: Python is not installed

**Symptoms:**
- `python --version` returns "command not found"
- `python3 --version` returns "command not found"

**Solutions:**

#### Windows:
1. **Download Python manually:**
   - Visit https://www.python.org/downloads/
   - Download Python 3.11.7 or later
   - Run installer with "Add to PATH" checked

2. **Use our setup script:**
   ```cmd
   setup.bat
   ```

3. **Verify installation:**
   ```cmd
   python --version
   ```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Linux (CentOS/RHEL):
```bash
sudo yum install python3 python3-pip
# or
sudo dnf install python3 python3-pip
```

#### macOS:
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

### Issue: Python version is too old

**Symptoms:**
- Python version < 3.8
- Import errors for newer features

**Solutions:**
1. **Upgrade Python:**
   ```bash
   # Windows: Download newer version from python.org
   # Linux: Use package manager
   sudo apt install python3.11  # Ubuntu
   # macOS: Use Homebrew
   brew install python@3.11
   ```

2. **Use virtual environment with newer Python:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

## 📦 Package Installation Issues

### Issue: pip is not installed

**Symptoms:**
- `pip --version` returns "command not found"
- `python -m pip --version` fails

**Solutions:**
```bash
# Install pip
python -m ensurepip --upgrade

# Or download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### Issue: Package installation fails

**Common causes and solutions:**

#### 1. Network/Proxy Issues
```bash
# Use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Or use alternative index
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

#### 2. Permission Issues
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

#### 3. Compilation Issues (Windows)
```bash
# Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use pre-compiled wheels
pip install --only-binary=all -r requirements.txt
```

#### 4. Specific Package Issues

**Flask-SQLAlchemy:**
```bash
pip install --force-reinstall Flask-SQLAlchemy
```

**Flask-Login:**
```bash
pip install --force-reinstall Flask-Login
```

**Flask-Migrate:**
```bash
pip install --force-reinstall Flask-Migrate
```

**Flask-Mail:**
```bash
pip install --force-reinstall Flask-Mail
```

### Issue: Virtual environment problems

**Symptoms:**
- Virtual environment not activating
- Packages installed globally instead of in venv

**Solutions:**
```bash
# Recreate virtual environment
rm -rf venv  # Linux/Mac
# or
rmdir /s venv  # Windows

python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## 🗄️ Database Issues

### Issue: Database creation fails

**Symptoms:**
- `db.create_all()` fails
- SQLite permission errors

**Solutions:**

#### 1. Check file permissions
```bash
# Linux/Mac: Ensure write permissions
chmod 755 instance/
touch instance/crm.db
chmod 644 instance/crm.db
```

#### 2. Check disk space
```bash
# Linux/Mac
df -h

# Windows
dir
```

#### 3. Manual database creation
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Database created successfully")
```

### Issue: Database connection errors

**Symptoms:**
- "Database is locked" errors
- Connection timeout

**Solutions:**
1. **Close other applications** using the database
2. **Check for multiple instances** of the application
3. **Use different database path:**
   ```python
   # In config.py
   SQLALCHEMY_DATABASE_URI = 'sqlite:///path/to/your/crm.db'
   ```

## 🔐 Authentication Issues

### Issue: Login not working

**Symptoms:**
- Login page shows but authentication fails
- "Invalid credentials" error

**Solutions:**

#### 1. Create test user
```bash
python create_test_user.py
```

#### 2. Check user table
```python
from app import create_app, db
from app.models.crm import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"User: {user.username}, Email: {user.email}")
```

#### 3. Reset password
```python
from app import create_app, db
from app.models.crm import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='admin@smartxcrm.com').first()
    if user:
        user.password_hash = generate_password_hash('newpassword123')
        db.session.commit()
        print("Password updated")
```

## 🌐 Application Startup Issues

### Issue: Application won't start

**Symptoms:**
- `python run.py` fails
- Import errors
- Port already in use

**Solutions:**

#### 1. Check imports
```bash
python -c "from app import create_app; print('Imports OK')"
```

#### 2. Check port availability
```bash
# Linux/Mac
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

#### 3. Use different port
```python
# In run.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

#### 4. Check environment variables
```bash
# Create .env file
echo "FLASK_APP=run.py" > .env
echo "FLASK_ENV=development" >> .env
echo "SECRET_KEY=your-secret-key" >> .env
```

### Issue: Template errors

**Symptoms:**
- "Template not found" errors
- Jinja2 syntax errors

**Solutions:**
1. **Check template directory structure**
2. **Verify template syntax**
3. **Clear template cache:**
   ```python
   app.jinja_env.cache = {}
   ```

## 📱 Mobile/API Issues

### Issue: API endpoints not working

**Symptoms:**
- 404 errors on API routes
- CORS errors in browser

**Solutions:**

#### 1. Check route registration
```python
# In your app
print(app.url_map)
```

#### 2. Enable CORS
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

#### 3. Check API authentication
```python
# Ensure JWT tokens are valid
# Check Authorization headers
```

## 🔍 Debugging Tools

### 1. Enable Debug Mode
```python
# In run.py
app.run(debug=True)
```

### 2. Use Flask Debugger
```python
# Add breakpoints
import pdb; pdb.set_trace()
```

### 3. Check Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 4. Database Inspection
```python
# SQLite browser
# Download from: https://sqlitebrowser.org/

# Or use Python
import sqlite3
conn = sqlite3.connect('instance/crm.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)
```

## 🛠️ System-Specific Issues

### Windows Issues

#### 1. Path problems
```cmd
# Add Python to PATH
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts
```

#### 2. PowerShell execution policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Visual C++ Build Tools
- Download from Microsoft Visual Studio
- Install C++ build tools

### Linux Issues

#### 1. Package manager conflicts
```bash
# Use virtual environment to avoid conflicts
python3 -m venv venv
source venv/bin/activate
```

#### 2. Permission issues
```bash
# Fix ownership
sudo chown -R $USER:$USER /path/to/project
```

#### 3. Missing system libraries
```bash
# Ubuntu/Debian
sudo apt install python3-dev build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
```

### macOS Issues

#### 1. Homebrew issues
```bash
# Update Homebrew
brew update
brew upgrade python3
```

#### 2. Xcode Command Line Tools
```bash
xcode-select --install
```

## 📞 Getting Help

### 1. Check Documentation
- [README.md](README.md)
- [USER_GUIDE.md](USER_GUIDE.md)
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)

### 2. Run Diagnostics
```bash
python check_packages.py
```

### 3. Check Logs
- Application logs in console
- System logs
- Database logs

### 4. Common Error Messages

#### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install Flask in virtual environment
```bash
source venv/bin/activate
pip install Flask
```

#### "Permission denied"
**Solution:** Check file permissions and ownership

#### "Address already in use"
**Solution:** Change port or kill existing process
```bash
# Linux/Mac
kill -9 $(lsof -t -i:5000)

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### "Database is locked"
**Solution:** Close other applications using the database

## 🔄 Recovery Procedures

### Complete Reset
If all else fails, perform a complete reset:

```bash
# 1. Remove virtual environment
rm -rf venv

# 2. Remove database
rm -f instance/crm.db

# 3. Remove cache
rm -rf __pycache__
rm -rf .pytest_cache

# 4. Reinstall everything
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Recreate database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# 6. Create test user
python create_test_user.py
```

---

**Remember:** Most issues can be resolved by ensuring you're using a virtual environment and have all required packages installed correctly.

*Last Updated: December 2024* 
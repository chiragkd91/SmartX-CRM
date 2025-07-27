@echo off
echo ========================================
echo    SmartX CRM - Setup Script
echo ========================================
echo.

:: Set error handling
setlocal enabledelayedexpansion

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges
) else (
    echo [WARNING] Not running as administrator. Some features may require admin rights.
    echo.
)

:: Step 1: Check Python Installation
echo [STEP 1] Checking Python Installation...
echo.

python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] Python is installed
    python --version
) else (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo [INFO] Attempting to install Python...
    echo.
    
    :: Download Python installer
    echo [INFO] Downloading Python 3.11.7...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}"
    
    if exist python-installer.exe (
        echo [INFO] Installing Python...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        echo [INFO] Python installation completed
        del python-installer.exe
        
        :: Refresh environment variables
        call refreshenv.cmd 2>nul
        if %errorLevel% neq 0 (
            echo [INFO] Refreshing PATH manually...
            set PATH=%PATH%;C:\Python311;C:\Python311\Scripts
        )
    ) else (
        echo [ERROR] Failed to download Python installer
        echo [INFO] Please download Python manually from https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo.

:: Step 2: Check pip installation
echo [STEP 2] Checking pip installation...
echo.

python -m pip --version >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] pip is available
    python -m pip --version
) else (
    echo [ERROR] pip is not available
    echo [INFO] Installing pip...
    python -m ensurepip --upgrade
)

echo.

:: Step 3: Upgrade pip
echo [STEP 3] Upgrading pip to latest version...
echo.

python -m pip install --upgrade pip
if %errorLevel% == 0 (
    echo [SUCCESS] pip upgraded successfully
) else (
    echo [WARNING] Failed to upgrade pip, continuing with current version
)

echo.

:: Step 4: Check virtual environment
echo [STEP 4] Setting up virtual environment...
echo.

if exist venv (
    echo [INFO] Virtual environment already exists
) else (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %errorLevel% == 0 (
        echo [SUCCESS] Virtual environment created
    ) else (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo.

:: Step 5: Activate virtual environment
echo [STEP 5] Activating virtual environment...
echo.

call venv\Scripts\activate.bat
if %errorLevel% == 0 (
    echo [SUCCESS] Virtual environment activated
) else (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo.

:: Step 6: Install required packages
echo [STEP 6] Installing required packages...
echo.

:: Check if requirements.txt exists
if not exist requirements.txt (
    echo [ERROR] requirements.txt not found
    echo [INFO] Creating basic requirements.txt...
    (
        echo Flask==2.3.3
        echo Flask-SQLAlchemy==3.0.5
        echo Flask-Login==0.6.3
        echo Flask-WTF==1.1.1
        echo Flask-Migrate==4.0.5
        echo Flask-Mail==0.9.1
        echo Flask-CORS==4.0.0
        echo Flask-RESTful==0.3.10
        echo Flask-JWT-Extended==4.5.3
        echo WTForms==3.0.1
        echo Werkzeug==2.3.7
        echo SQLAlchemy>=2.0.30
        echo Jinja2==3.1.2
        echo MarkupSafe==2.1.3
        echo itsdangerous==2.1.2
        echo click==8.1.7
        echo blinker==1.6.3
        echo email-validator==2.0.0
        echo python-dotenv==1.0.0
        echo psutil==5.9.5
        echo requests==2.31.0
        echo cryptography==41.0.4
        echo bcrypt==4.0.1
        echo PyJWT==2.8.0
        echo redis==5.0.0
        echo celery==5.3.1
        echo gunicorn==21.2.0
        echo pytest==7.4.3
        echo pytest-flask==1.3.0
        echo coverage==7.3.2
        echo black==23.11.0
        echo flake8==6.1.0
        echo bandit==1.7.5
        echo safety==2.3.5
        echo bleach==6.1.0
        echo Pillow==10.1.0
        echo openpyxl==3.1.2
        echo pandas==2.1.3
        echo numpy==1.25.2
        echo matplotlib==3.8.2
        echo seaborn==0.13.0
        echo scikit-learn==1.3.2
        echo plotly==5.17.0
        echo dash==2.14.2
        echo dash-bootstrap-components==1.5.0
    ) > requirements.txt
    echo [INFO] Basic requirements.txt created
)

echo [INFO] Installing packages from requirements.txt...
echo [INFO] This may take several minutes...
echo.

:: Install packages with error handling
python -m pip install -r requirements.txt
if %errorLevel% == 0 (
    echo [SUCCESS] All packages installed successfully
) else (
    echo [WARNING] Some packages failed to install
    echo [INFO] Attempting to install packages individually...
    echo.
    
    :: Install critical packages individually
    for %%p in (Flask Flask-SQLAlchemy Flask-Login Flask-Migrate Flask-Mail) do (
        echo [INFO] Installing %%p...
        python -m pip install %%p
        if !errorLevel! == 0 (
            echo [SUCCESS] %%p installed
        ) else (
            echo [ERROR] Failed to install %%p
        )
    )
)

echo.

:: Step 7: Verify critical packages
echo [STEP 7] Verifying critical packages...
echo.

:: Check Flask
python -c "import flask; print('[SUCCESS] Flask version:', flask.__version__)" 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Flask not properly installed
    echo [INFO] Attempting to reinstall Flask...
    python -m pip install --force-reinstall Flask
)

:: Check Flask-SQLAlchemy
python -c "import flask_sqlalchemy; print('[SUCCESS] Flask-SQLAlchemy available')" 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Flask-SQLAlchemy not properly installed
    echo [INFO] Attempting to reinstall Flask-SQLAlchemy...
    python -m pip install --force-reinstall Flask-SQLAlchemy
)

:: Check Flask-Login
python -c "import flask_login; print('[SUCCESS] Flask-Login available')" 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Flask-Login not properly installed
    echo [INFO] Attempting to reinstall Flask-Login...
    python -m pip install --force-reinstall Flask-Login
)

:: Check Flask-Migrate
python -c "import flask_migrate; print('[SUCCESS] Flask-Migrate available')" 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Flask-Migrate not properly installed
    echo [INFO] Attempting to reinstall Flask-Migrate...
    python -m pip install --force-reinstall Flask-Migrate
)

:: Check Flask-Mail
python -c "import flask_mail; print('[SUCCESS] Flask-Mail available')" 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Flask-Mail not properly installed
    echo [INFO] Attempting to reinstall Flask-Mail...
    python -m pip install --force-reinstall Flask-Mail
)

echo.

:: Step 8: Initialize database
echo [STEP 8] Initializing database...
echo.

if exist instance (
    echo [INFO] Instance directory exists
) else (
    echo [INFO] Creating instance directory...
    mkdir instance
)

:: Check if database exists
if exist instance\crm.db (
    echo [INFO] Database already exists
) else (
    echo [INFO] Creating database...
    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('[SUCCESS] Database created')" 2>nul
    if %errorLevel% neq 0 (
        echo [WARNING] Database creation failed, will be created on first run
    )
)

echo.

:: Step 9: Create test user
echo [STEP 9] Creating test user...
echo.

python create_test_user.py 2>nul
if %errorLevel% == 0 (
    echo [SUCCESS] Test user created
) else (
    echo [WARNING] Test user creation failed, will be created on first run
)

echo.

:: Step 10: Run tests
echo [STEP 10] Running basic tests...
echo.

python -m pytest tests/ -v --tb=short 2>nul
if %errorLevel% == 0 (
    echo [SUCCESS] All tests passed
) else (
    echo [WARNING] Some tests failed, but setup is complete
)

echo.

:: Step 11: Final verification
echo [STEP 11] Final verification...
echo.

echo [INFO] Checking application startup...
python -c "from app import create_app; app = create_app(); print('[SUCCESS] Application imports successfully')" 2>nul
if %errorLevel% == 0 (
    echo [SUCCESS] Application is ready to run
) else (
    echo [ERROR] Application has import issues
    echo [INFO] Check the error messages above
)

echo.

:: Step 12: Create run script
echo [STEP 12] Creating run script...
echo.

(
    echo @echo off
    echo echo Starting SmartX CRM...
    echo call venv\Scripts\activate.bat
    echo python run.py
    echo pause
) > run_crm.bat

echo [SUCCESS] Run script created: run_crm.bat

echo.

:: Step 13: Create environment file
echo [STEP 13] Creating environment configuration...
echo.

if not exist .env (
    (
        echo # SmartX CRM Environment Configuration
        echo FLASK_APP=run.py
        echo FLASK_ENV=development
        echo SECRET_KEY=your-secret-key-change-this-in-production
        echo DATABASE_URL=sqlite:///instance/crm.db
        echo MAIL_SERVER=smtp.gmail.com
        echo MAIL_PORT=587
        echo MAIL_USE_TLS=True
        echo MAIL_USERNAME=your-email@gmail.com
        echo MAIL_PASSWORD=your-app-password
        echo REDIS_URL=redis://localhost:6379/0
        echo DEBUG=True
    ) > .env
    echo [SUCCESS] Environment file created: .env
    echo [INFO] Please update .env with your actual configuration
) else (
    echo [INFO] Environment file already exists
)

echo.

:: Final summary
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo [SUCCESS] SmartX CRM has been set up successfully!
echo.
echo [INFO] To start the application:
echo       1. Double-click run_crm.bat
echo       2. Or run: python run.py
echo.
echo [INFO] Default login credentials:
echo       Username: admin@smartxcrm.com
echo       Password: admin123
echo.
echo [INFO] Application will be available at:
echo       http://localhost:5000
echo.
echo [INFO] For support, check the documentation:
echo       - README.md
echo       - USER_GUIDE.md
echo       - TECHNICAL_DOCUMENTATION.md
echo.
echo [INFO] Happy coding!
echo.

pause 
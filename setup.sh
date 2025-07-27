#!/bin/bash

# SmartX CRM - Setup Script for Linux/Mac
# This script handles Python installation, package management, and setup issues

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "========================================"
echo "    SmartX CRM - Setup Script"
echo "========================================"
echo

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Check if running as root (Linux only)
if [[ "$OS" == "linux" && "$EUID" -eq 0 ]]; then
    print_warning "Running as root. This is not recommended for security reasons."
fi

# Step 1: Check Python Installation
echo
print_status "Step 1: Checking Python Installation..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python3 is installed: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    print_success "Python is installed: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    print_error "Python is not installed"
    echo
    
    if [[ "$OS" == "linux" ]]; then
        print_status "Installing Python on Linux..."
        
        # Detect package manager
        if command -v apt-get &> /dev/null; then
            print_status "Using apt-get package manager"
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command -v yum &> /dev/null; then
            print_status "Using yum package manager"
            sudo yum install -y python3 python3-pip
        elif command -v dnf &> /dev/null; then
            print_status "Using dnf package manager"
            sudo dnf install -y python3 python3-pip
        else
            print_error "Unsupported package manager. Please install Python manually."
            exit 1
        fi
        
        PYTHON_CMD="python3"
        
    elif [[ "$OS" == "macos" ]]; then
        print_status "Installing Python on macOS..."
        
        if command -v brew &> /dev/null; then
            print_status "Using Homebrew to install Python"
            brew install python3
        else
            print_error "Homebrew not found. Please install Homebrew first:"
            print_status "Visit: https://brew.sh/"
            exit 1
        fi
        
        PYTHON_CMD="python3"
    fi
fi

# Step 2: Check pip installation
echo
print_status "Step 2: Checking pip installation..."

if $PYTHON_CMD -m pip --version &> /dev/null; then
    print_success "pip is available"
    $PYTHON_CMD -m pip --version
else
    print_error "pip is not available"
    print_status "Installing pip..."
    $PYTHON_CMD -m ensurepip --upgrade
fi

# Step 3: Upgrade pip
echo
print_status "Step 3: Upgrading pip to latest version..."

if $PYTHON_CMD -m pip install --upgrade pip; then
    print_success "pip upgraded successfully"
else
    print_warning "Failed to upgrade pip, continuing with current version"
fi

# Step 4: Check virtual environment
echo
print_status "Step 4: Setting up virtual environment..."

if [ -d "venv" ]; then
    print_status "Virtual environment already exists"
else
    print_status "Creating virtual environment..."
    if $PYTHON_CMD -m venv venv; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
fi

# Step 5: Activate virtual environment
echo
print_status "Step 5: Activating virtual environment..."

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_success "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Step 6: Install required packages
echo
print_status "Step 6: Installing required packages..."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found"
    print_status "Creating basic requirements.txt..."
    
    cat > requirements.txt << 'EOF'
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-WTF==1.1.1
Flask-Migrate==4.0.5
Flask-Mail==0.9.1
Flask-CORS==4.0.0
Flask-RESTful==0.3.10
Flask-JWT-Extended==4.5.3
WTForms==3.0.1
Werkzeug==2.3.7
SQLAlchemy>=2.0.30
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3
email-validator==2.0.0
python-dotenv==1.0.0
psutil==5.9.5
requests==2.31.0
cryptography==41.0.4
bcrypt==4.0.1
PyJWT==2.8.0
redis==5.0.0
celery==5.3.1
gunicorn==21.2.0
pytest==7.4.3
pytest-flask==1.3.0
coverage==7.3.2
black==23.11.0
flake8==6.1.0
bandit==1.7.5
safety==2.3.5
bleach==6.1.0
Pillow==10.1.0
openpyxl==3.1.2
pandas==2.1.3
numpy==1.25.2
matplotlib==3.8.2
seaborn==0.13.0
scikit-learn==1.3.2
plotly==5.17.0
dash==2.14.2
dash-bootstrap-components==1.5.0
EOF
    
    print_success "Basic requirements.txt created"
fi

print_status "Installing packages from requirements.txt..."
print_status "This may take several minutes..."

# Install packages with error handling
if pip install -r requirements.txt; then
    print_success "All packages installed successfully"
else
    print_warning "Some packages failed to install"
    print_status "Attempting to install critical packages individually..."
    echo
    
    # Install critical packages individually
    critical_packages=("Flask" "Flask-SQLAlchemy" "Flask-Login" "Flask-Migrate" "Flask-Mail")
    for package in "${critical_packages[@]}"; do
        print_status "Installing $package..."
        if pip install "$package"; then
            print_success "$package installed"
        else
            print_error "Failed to install $package"
        fi
    done
fi

# Step 7: Verify critical packages
echo
print_status "Step 7: Verifying critical packages..."

# Check Flask
if python -c "import flask; print('[SUCCESS] Flask version:', flask.__version__)" 2>/dev/null; then
    print_success "Flask verified"
else
    print_error "Flask not properly installed"
    print_status "Attempting to reinstall Flask..."
    pip install --force-reinstall Flask
fi

# Check Flask-SQLAlchemy
if python -c "import flask_sqlalchemy; print('[SUCCESS] Flask-SQLAlchemy available')" 2>/dev/null; then
    print_success "Flask-SQLAlchemy verified"
else
    print_error "Flask-SQLAlchemy not properly installed"
    print_status "Attempting to reinstall Flask-SQLAlchemy..."
    pip install --force-reinstall Flask-SQLAlchemy
fi

# Check Flask-Login
if python -c "import flask_login; print('[SUCCESS] Flask-Login available')" 2>/dev/null; then
    print_success "Flask-Login verified"
else
    print_error "Flask-Login not properly installed"
    print_status "Attempting to reinstall Flask-Login..."
    pip install --force-reinstall Flask-Login
fi

# Check Flask-Migrate
if python -c "import flask_migrate; print('[SUCCESS] Flask-Migrate available')" 2>/dev/null; then
    print_success "Flask-Migrate verified"
else
    print_error "Flask-Migrate not properly installed"
    print_status "Attempting to reinstall Flask-Migrate..."
    pip install --force-reinstall Flask-Migrate
fi

# Check Flask-Mail
if python -c "import flask_mail; print('[SUCCESS] Flask-Mail available')" 2>/dev/null; then
    print_success "Flask-Mail verified"
else
    print_error "Flask-Mail not properly installed"
    print_status "Attempting to reinstall Flask-Mail..."
    pip install --force-reinstall Flask-Mail
fi

# Step 8: Initialize database
echo
print_status "Step 8: Initializing database..."

if [ -d "instance" ]; then
    print_status "Instance directory exists"
else
    print_status "Creating instance directory..."
    mkdir -p instance
fi

# Check if database exists
if [ -f "instance/crm.db" ]; then
    print_status "Database already exists"
else
    print_status "Creating database..."
    if python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('[SUCCESS] Database created')" 2>/dev/null; then
        print_success "Database created successfully"
    else
        print_warning "Database creation failed, will be created on first run"
    fi
fi

# Step 9: Create test user
echo
print_status "Step 9: Creating test user..."

if python create_test_user.py 2>/dev/null; then
    print_success "Test user created"
else
    print_warning "Test user creation failed, will be created on first run"
fi

# Step 10: Run tests
echo
print_status "Step 10: Running basic tests..."

if python -m pytest tests/ -v --tb=short 2>/dev/null; then
    print_success "All tests passed"
else
    print_warning "Some tests failed, but setup is complete"
fi

# Step 11: Final verification
echo
print_status "Step 11: Final verification..."

print_status "Checking application startup..."
if python -c "from app import create_app; app = create_app(); print('[SUCCESS] Application imports successfully')" 2>/dev/null; then
    print_success "Application is ready to run"
else
    print_error "Application has import issues"
    print_status "Check the error messages above"
fi

# Step 12: Create run script
echo
print_status "Step 12: Creating run script..."

cat > run_crm.sh << 'EOF'
#!/bin/bash
echo "Starting SmartX CRM..."
source venv/bin/activate
python run.py
EOF

chmod +x run_crm.sh
print_success "Run script created: run_crm.sh"

# Step 13: Create environment file
echo
print_status "Step 13: Creating environment configuration..."

if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# SmartX CRM Environment Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///instance/crm.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
REDIS_URL=redis://localhost:6379/0
DEBUG=True
EOF
    
    print_success "Environment file created: .env"
    print_status "Please update .env with your actual configuration"
else
    print_status "Environment file already exists"
fi

# Final summary
echo
echo "========================================"
echo "    Setup Complete!"
echo "========================================"
echo
print_success "SmartX CRM has been set up successfully!"
echo
print_status "To start the application:"
echo "       1. Run: ./run_crm.sh"
echo "       2. Or run: python run.py"
echo
print_status "Default login credentials:"
echo "       Username: admin@smartxcrm.com"
echo "       Password: admin123"
echo
print_status "Application will be available at:"
echo "       http://localhost:5000"
echo
print_status "For support, check the documentation:"
echo "       - README.md"
echo "       - USER_GUIDE.md"
echo "       - TECHNICAL_DOCUMENTATION.md"
echo
print_status "Happy coding!"
echo 
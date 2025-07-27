# SmartX CRM - Technical Documentation

## 🏗️ System Architecture

### Technology Stack

#### Backend Framework
- **Framework**: Flask 2.3.x
- **Language**: Python 3.8+
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **API**: RESTful API with OpenAPI 3.0 specification

#### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript**: ES6+ with modern features
- **Responsive Design**: Mobile-first approach
- **Progressive Web App**: PWA capabilities

#### Development Tools
- **Version Control**: Git
- **Testing**: pytest
- **Code Quality**: flake8, black
- **Documentation**: Sphinx
- **CI/CD**: GitHub Actions

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    SmartX CRM System                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Web UI    │  │  Mobile App │  │   API       │        │
│  │  (Flask)    │  │  (React)    │  │  (REST)     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Services  │  │   Models    │  │   Security  │        │
│  │  (Business) │  │  (Data)     │  │  (Auth)     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Database   │  │   Cache     │  │   Storage   │        │
│  │  (SQLite)   │  │  (Redis)    │  │  (Files)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
SmartX-CRM/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app initialization
│   ├── models/                  # Database models
│   │   ├── crm.py              # CRM data models
│   │   ├── crm_business_processes.py
│   │   └── crm_integrations.py
│   ├── routes/                  # Route handlers
│   │   ├── main.py             # Main routes
│   │   ├── crm.py              # CRM routes
│   │   ├── admin.py            # Admin routes
│   │   └── api_docs.py         # API documentation
│   ├── services/               # Business logic
│   │   ├── crm_service.py
│   │   ├── contact_service.py
│   │   ├── lead_service.py
│   │   └── opportunity_service.py
│   ├── templates/              # HTML templates
│   │   ├── crm/               # CRM templates
│   │   ├── main/              # Main templates
│   │   └── security/          # Security templates
│   ├── static/                # Static assets
│   │   ├── css/              # Stylesheets
│   │   ├── js/               # JavaScript files
│   │   └── images/           # Images
│   ├── security/             # Security modules
│   │   ├── input_validator.py
│   │   ├── security_auditor.py
│   │   └── vulnerability_scanner.py
│   ├── monitoring/           # Monitoring tools
│   │   ├── app_monitor.py
│   │   ├── performance_tracker.py
│   │   └── alert_system.py
│   ├── backup/              # Backup system
│   │   ├── backup_manager.py
│   │   └── recovery_manager.py
│   ├── mobile/              # Mobile features
│   │   ├── mobile_app.py
│   │   ├── cross_platform.py
│   │   └── offline_manager.py
│   ├── api/                 # API modules
│   │   ├── documentation.py
│   │   ├── sdk.py
│   │   └── testing_tool.py
│   └── sdk/                 # SDK components
│       └── crm_sdk.py
├── tests/                   # Test suite
│   ├── test_crm_routes.py
│   ├── test_services.py
│   └── test_models.py
├── deployment/              # Deployment scripts
├── backups/                 # Backup storage
├── instance/               # Instance-specific files
├── requirements.txt        # Python dependencies
├── config.py              # Configuration
├── run.py                 # Application entry point
└── README.md              # Project documentation
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (version control)
- SQLite (included with Python)

### Development Setup

1. **Clone Repository**
```bash
git clone https://github.com/chiragkd91/SmartX-CRM.git
cd SmartX-CRM
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize Database**
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

5. **Run Application**
```bash
python run.py
```

### Production Setup

1. **Environment Configuration**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://user:pass@localhost/crm_db
```

2. **Database Setup**
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
createdb crm_db

# Run migrations
flask db upgrade
```

3. **Web Server Setup**
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## 🗄️ Database Schema

### Core Tables

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Contacts Table
```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120),
    phone VARCHAR(20),
    company VARCHAR(100),
    position VARCHAR(100),
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### Leads Table
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER,
    source VARCHAR(50),
    status VARCHAR(20) DEFAULT 'new',
    score INTEGER DEFAULT 0,
    assigned_to INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contact_id) REFERENCES contacts(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);
```

#### Opportunities Table
```sql
CREATE TABLE opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    title VARCHAR(200) NOT NULL,
    amount DECIMAL(10,2),
    stage VARCHAR(50) DEFAULT 'prospecting',
    probability INTEGER DEFAULT 0,
    close_date DATE,
    assigned_to INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);
```

## 🔌 API Documentation

### Authentication

All API endpoints require authentication using JWT tokens.

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "password123"
}
```

Response:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "user@example.com",
        "role": "admin"
    }
}
```

### CRM Endpoints

#### Get All Contacts
```http
GET /api/contacts
Authorization: Bearer <token>
```

#### Create Contact
```http
POST /api/contacts
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "company": "Example Corp"
}
```

#### Get Contact by ID
```http
GET /api/contacts/{id}
Authorization: Bearer <token>
```

#### Update Contact
```http
PUT /api/contacts/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com"
}
```

#### Delete Contact
```http
DELETE /api/contacts/{id}
Authorization: Bearer <token>
```

### Lead Management

#### Get All Leads
```http
GET /api/leads
Authorization: Bearer <token>
```

#### Create Lead
```http
POST /api/leads
Authorization: Bearer <token>
Content-Type: application/json

{
    "contact_id": 1,
    "source": "website",
    "status": "new",
    "assigned_to": 2
}
```

### Opportunity Management

#### Get All Opportunities
```http
GET /api/opportunities
Authorization: Bearer <token>
```

#### Create Opportunity
```http
POST /api/opportunities
Authorization: Bearer <token>
Content-Type: application/json

{
    "lead_id": 1,
    "title": "Enterprise Software License",
    "amount": 50000.00,
    "stage": "proposal",
    "probability": 75,
    "close_date": "2024-03-15"
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_crm_routes.py

# Run with coverage
pytest --cov=app

# Run with verbose output
pytest -v
```

### Test Structure

```python
# Example test
def test_create_contact(client, auth_headers):
    """Test creating a new contact"""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    
    response = client.post('/api/contacts', 
                          json=data, 
                          headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json['first_name'] == 'John'
```

## 🔒 Security Implementation

### Authentication Flow

1. **User Login**: Username/password validation
2. **JWT Generation**: Secure token creation
3. **Token Validation**: Middleware validation
4. **Role-Based Access**: Permission checking

### Security Headers

```python
# Security headers configuration
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'"
}
```

### Input Validation

```python
# Example input validation
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(data):
    """Sanitize user input"""
    return bleach.clean(data, strip=True)
```

## 📊 Performance Optimization

### Database Optimization

```python
# Index creation for performance
CREATE INDEX idx_contacts_email ON contacts(email);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_opportunities_stage ON opportunities(stage);
```

### Caching Strategy

```python
# Redis caching implementation
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_data(key):
    """Get data from cache"""
    return redis_client.get(key)

def set_cached_data(key, value, expire=3600):
    """Set data in cache"""
    redis_client.setex(key, expire, value)
```

### Query Optimization

```python
# Optimized database queries
def get_contacts_with_activities():
    """Get contacts with recent activities"""
    return Contact.query\
        .join(Activity, Contact.id == Activity.contact_id)\
        .filter(Activity.created_at >= datetime.now() - timedelta(days=30))\
        .options(joinedload(Contact.activities))\
        .all()
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/crm_db
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=crm_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Cloud Deployment

#### AWS Deployment
```bash
# Deploy to AWS Elastic Beanstalk
eb init crm-app
eb create crm-production
eb deploy
```

#### Heroku Deployment
```bash
# Deploy to Heroku
heroku create crm-app
git push heroku main
```

## 📈 Monitoring & Logging

### Application Monitoring

```python
# Performance monitoring
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Log performance metrics
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper
```

### Error Logging

```python
# Error logging configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🔄 Backup & Recovery

### Automated Backup

```python
# Backup script
def create_backup():
    """Create database backup"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"backup_{timestamp}.sql"
    
    subprocess.run([
        'sqlite3', 'instance/crm.db',
        f'.backup backups/{backup_file}'
    ])
    
    return backup_file
```

### Recovery Process

```python
# Recovery script
def restore_backup(backup_file):
    """Restore from backup"""
    subprocess.run([
        'sqlite3', 'instance/crm.db',
        f'.restore backups/{backup_file}'
    ])
```

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JWT Documentation](https://jwt.io/)
- [REST API Best Practices](https://restfulapi.net/)

---

**SmartX CRM** - Technical excellence for modern business solutions.

*Last Updated: December 2024* 
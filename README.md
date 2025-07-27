# CRM (Customer Relationship Management) System

A comprehensive CRM system built with Flask, SQLAlchemy, and modern web technologies. This system provides complete customer relationship management capabilities including lead management, account management, contact management, opportunity tracking, activity management, and advanced analytics.

## 🚀 Features

### Core CRM Features
- **Lead Management**: Capture, qualify, score, and nurture leads
- **Account Management**: Manage customer accounts with hierarchy and relationships
- **Contact Management**: Track contacts with segmentation and communication preferences
- **Opportunity Management**: Sales pipeline management with forecasting
- **Activity Management**: Task tracking, scheduling, and automation
- **Quote Management**: Generate and manage quotes and proposals

### Advanced Features
- **Sales Analytics**: Pipeline analysis, forecasting, and performance metrics
- **Lead Scoring**: Automated lead scoring based on custom criteria
- **Workflow Automation**: Automated processes and triggers
- **Reporting**: Comprehensive reporting and analytics
- **Data Import/Export**: Bulk data operations
- **Integration Ready**: API endpoints for external integrations

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL (recommended) or SQLite
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CRM_Project_Structure
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///crm.db
   FLASK_APP=run.py
   FLASK_ENV=development
   ```

5. **Initialize the database**
   ```bash
   flask init-db
   flask create-sample-data
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

## 🗄️ Database Schema

### Core Tables
- **users**: User accounts and authentication
- **leads**: Lead information and scoring
- **accounts**: Customer account management
- **contacts**: Contact information and relationships
- **opportunities**: Sales opportunities and pipeline
- **activities**: Tasks, calls, meetings, and activities
- **quotes**: Quote generation and management
- **territories**: Sales territory management

### Business Process Tables
- **workflows**: Automated workflow definitions
- **campaigns**: Marketing campaign management
- **lead_scoring**: Lead scoring rules and criteria
- **automation_rules**: Business automation rules

### Integration Tables
- **integrations**: External system integrations
- **webhooks**: Webhook configurations
- **api_tokens**: API authentication tokens

## 🔌 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/register` - User registration

### Lead Management
- `GET /crm/leads` - Get all leads
- `POST /crm/leads` - Create new lead
- `GET /crm/leads/<id>` - Get specific lead
- `PUT /crm/leads/<id>` - Update lead
- `DELETE /crm/leads/<id>` - Delete lead
- `POST /crm/leads/<id>/qualify` - Qualify lead
- `POST /crm/leads/<id>/score` - Score lead
- `POST /crm/leads/<id>/convert` - Convert lead

### Account Management
- `GET /crm/accounts` - Get all accounts
- `POST /crm/accounts` - Create new account
- `GET /crm/accounts/<id>` - Get specific account
- `PUT /crm/accounts/<id>` - Update account
- `DELETE /crm/accounts/<id>` - Delete account

### Contact Management
- `GET /crm/contacts` - Get all contacts
- `POST /crm/contacts` - Create new contact
- `GET /crm/contacts/<id>` - Get specific contact
- `PUT /crm/contacts/<id>` - Update contact
- `DELETE /crm/contacts/<id>` - Delete contact

### Opportunity Management
- `GET /crm/opportunities` - Get all opportunities
- `POST /crm/opportunities` - Create new opportunity
- `GET /crm/opportunities/<id>` - Get specific opportunity
- `PUT /crm/opportunities/<id>` - Update opportunity
- `DELETE /crm/opportunities/<id>` - Delete opportunity

### Activity Management
- `GET /crm/activities` - Get all activities
- `POST /crm/activities` - Create new activity
- `GET /crm/activities/<id>` - Get specific activity
- `PUT /crm/activities/<id>` - Update activity
- `DELETE /crm/activities/<id>` - Delete activity

### Analytics and Reports
- `GET /crm/analytics` - Get CRM analytics
- `GET /crm/reports` - Generate reports
- `GET /crm/export/<data_type>` - Export data

## 📊 Usage Examples

### Creating a Lead
```python
import requests

# Create a new lead
lead_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "company": "Tech Solutions Inc",
    "job_title": "CTO",
    "industry": "Technology",
    "source": "Website",
    "status": "New"
}

response = requests.post('http://localhost:5000/crm/leads', json=lead_data)
print(response.json())
```

### Creating an Account
```python
account_data = {
    "name": "Tech Solutions Inc",
    "industry": "Technology",
    "website": "www.techsolutions.com",
    "phone": "+1-555-0001",
    "email": "info@techsolutions.com",
    "annual_revenue": 5000000,
    "employee_count": 50,
    "status": "Active",
    "type": "Customer"
}

response = requests.post('http://localhost:5000/crm/accounts', json=account_data)
print(response.json())
```

### Creating an Opportunity
```python
opportunity_data = {
    "name": "Enterprise Software License",
    "account_id": 1,
    "contact_id": 1,
    "stage": "Prospecting",
    "amount": 50000,
    "probability": 25,
    "expected_close_date": "2024-03-31",
    "type": "New Business",
    "source": "Referral"
}

response = requests.post('http://localhost:5000/crm/opportunities', json=opportunity_data)
print(response.json())
```

### Creating an Activity
```python
activity_data = {
    "subject": "Follow up call with John Doe",
    "type": "Call",
    "status": "Planned",
    "priority": "High",
    "description": "Follow up on proposal sent last week",
    "due_date": "2024-01-15T10:00:00",
    "duration": 30,
    "contact_id": 1,
    "opportunity_id": 1
}

response = requests.post('http://localhost:5000/crm/activities', json=activity_data)
print(response.json())
```

## 🔧 Configuration

### Database Configuration
The system supports multiple database backends:

**SQLite (Default)**
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///crm.db'
```

**PostgreSQL**
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/crm_db'
```

**MySQL**
```python
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/crm_db'
```

### Email Configuration
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

## 🚀 Deployment

### Production Deployment with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 📈 Monitoring and Logging

The system includes comprehensive logging and monitoring capabilities:

- **Application Logs**: Flask application logging
- **Database Logs**: SQLAlchemy query logging
- **Error Tracking**: Exception handling and reporting
- **Performance Monitoring**: Request timing and performance metrics

## 🔒 Security Features

- **Authentication**: User authentication and session management
- **Authorization**: Role-based access control
- **Data Validation**: Input validation and sanitization
- **SQL Injection Protection**: Parameterized queries
- **CSRF Protection**: Cross-site request forgery protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0** - Initial release with core CRM functionality
- **v1.1.0** - Added advanced analytics and reporting
- **v1.2.0** - Enhanced automation and workflow features
- **v1.3.0** - Improved API and integration capabilities

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)

---

**Note**: This is a comprehensive CRM system designed for production use. Make sure to configure security settings, backup strategies, and monitoring before deploying to production. 
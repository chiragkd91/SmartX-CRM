#!/usr/bin/env python3
"""
Production Deployment Setup Script for CRM Application
Handles server configuration, SSL certificates, domain setup, load balancing, and CDN integration
"""

import os
import sys
import subprocess
import json
import yaml
import requests
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProductionDeployment:
    def __init__(self, config_file='deployment_config.yaml'):
        self.config_file = config_file
        self.config = self.load_config()
        self.deployment_dir = Path(__file__).parent
        self.project_root = self.deployment_dir.parent
        
    def load_config(self):
        """Load deployment configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_file} not found!")
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            'server': {
                'host': 'your-domain.com',
                'port': 443,
                'environment': 'production',
                'workers': 4,
                'max_requests': 1000,
                'timeout': 30
            },
            'ssl': {
                'enabled': True,
                'certificate_path': '/etc/ssl/certs/crm.crt',
                'private_key_path': '/etc/ssl/private/crm.key',
                'auto_renew': True
            },
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'crm_production',
                'user': 'crm_user',
                'password': 'secure_password_here'
            },
            'load_balancer': {
                'enabled': True,
                'type': 'nginx',
                'upstream_servers': ['127.0.0.1:8000', '127.0.0.1:8001'],
                'health_check': True
            },
            'cdn': {
                'enabled': True,
                'provider': 'cloudflare',
                'zone_id': 'your_zone_id',
                'api_token': 'your_api_token'
            },
            'monitoring': {
                'enabled': True,
                'log_level': 'INFO',
                'metrics_collection': True,
                'alerting': True
            },
            'backup': {
                'enabled': True,
                'frequency': 'daily',
                'retention_days': 30,
                'storage_path': '/backups/crm'
            }
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        logger.info(f"Created default configuration file: {self.config_file}")
        logger.warning("Please update the configuration with your actual values!")
        return default_config
    
    def check_system_requirements(self):
        """Check if system meets deployment requirements"""
        logger.info("Checking system requirements...")
        
        requirements = {
            'python': '3.8+',
            'nginx': '1.18+',
            'postgresql': '12+',
            'redis': '6.0+',
            'certbot': 'latest'
        }
        
        for requirement, version in requirements.items():
            try:
                result = subprocess.run([requirement, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"✓ {requirement} is installed")
                else:
                    logger.warning(f"⚠ {requirement} not found or not accessible")
            except FileNotFoundError:
                logger.error(f"✗ {requirement} is not installed")
                return False
        
        return True
    
    def setup_environment(self):
        """Setup production environment"""
        logger.info("Setting up production environment...")
        
        # Create production environment file
        env_file = self.project_root / '.env.production'
        env_content = f"""
# Production Environment Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY={self.generate_secret_key()}

# Database Configuration
DATABASE_URL=postgresql://{self.config['database']['user']}:{self.config['database']['password']}@{self.config['database']['host']}:{self.config['database']['port']}/{self.config['database']['name']}

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Security Configuration
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
CSRF_ENABLED=True

# Logging Configuration
LOG_LEVEL={self.config['monitoring']['log_level']}
LOG_FILE=/var/log/crm/app.log

# CDN Configuration
CDN_ENABLED={str(self.config['cdn']['enabled']).lower()}
CDN_DOMAIN=cdn.{self.config['server']['host']}

# Backup Configuration
BACKUP_ENABLED={str(self.config['backup']['enabled']).lower()}
BACKUP_PATH={self.config['backup']['storage_path']}
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content.strip())
        
        logger.info(f"Created production environment file: {env_file}")
    
    def setup_database(self):
        """Setup production database"""
        logger.info("Setting up production database...")
        
        db_config = self.config['database']
        
        # Create database setup script
        db_setup_script = f"""
-- Database Setup Script for CRM Production
CREATE DATABASE {db_config['name']};
CREATE USER {db_config['user']} WITH PASSWORD '{db_config['password']}';
GRANT ALL PRIVILEGES ON DATABASE {db_config['name']} TO {db_config['user']};
ALTER USER {db_config['user']} CREATEDB;
"""
        
        db_script_path = self.deployment_dir / 'database_setup.sql'
        with open(db_script_path, 'w') as f:
            f.write(db_setup_script)
        
        logger.info(f"Created database setup script: {db_script_path}")
        logger.info("Please run the database setup script manually:")
        logger.info(f"sudo -u postgres psql -f {db_script_path}")
    
    def setup_nginx_config(self):
        """Setup Nginx configuration for load balancing"""
        logger.info("Setting up Nginx configuration...")
        
        nginx_config = f"""
# Nginx Configuration for CRM Application
upstream crm_backend {{
    least_conn;
    {' '.join([f'server {server};' for server in self.config['load_balancer']['upstream_servers']])}
    
    # Health check
    keepalive 32;
}}

# Rate limiting
limit_req_zone $binary_remote_addr zone=crm_limit:10m rate=10r/s;

server {{
    listen 80;
    server_name {self.config['server']['host']};
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {self.config['server']['host']};
    
    # SSL Configuration
    ssl_certificate {self.config['ssl']['certificate_path']};
    ssl_certificate_key {self.config['ssl']['private_key_path']};
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:;";
    
    # Rate limiting
    limit_req zone=crm_limit burst=20 nodelay;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Static files
    location /static/ {{
        alias /var/www/crm/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
    
    # Media files
    location /media/ {{
        alias /var/www/crm/media/;
        expires 1y;
        add_header Cache-Control "public";
    }}
    
    # Main application
    location / {{
        proxy_pass http://crm_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }}
    
    # Health check endpoint
    location /health {{
        access_log off;
        return 200 "healthy\\n";
        add_header Content-Type text/plain;
    }}
}}
"""
        
        nginx_config_path = self.deployment_dir / 'nginx.conf'
        with open(nginx_config_path, 'w') as f:
            f.write(nginx_config)
        
        logger.info(f"Created Nginx configuration: {nginx_config_path}")
        logger.info("Please copy this configuration to /etc/nginx/sites-available/crm")
    
    def setup_ssl_certificate(self):
        """Setup SSL certificate using Let's Encrypt"""
        logger.info("Setting up SSL certificate...")
        
        if not self.config['ssl']['enabled']:
            logger.info("SSL is disabled in configuration")
            return
        
        domain = self.config['server']['host']
        
        # Certbot command for Let's Encrypt
        certbot_cmd = [
            'certbot', 'certonly', '--nginx',
            '-d', domain,
            '--non-interactive',
            '--agree-tos',
            '--email', 'admin@' + domain,
            '--expand'
        ]
        
        try:
            logger.info(f"Running certbot for domain: {domain}")
            result = subprocess.run(certbot_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✓ SSL certificate obtained successfully")
                
                # Setup auto-renewal
                if self.config['ssl']['auto_renew']:
                    self.setup_ssl_auto_renewal()
            else:
                logger.error(f"✗ Failed to obtain SSL certificate: {result.stderr}")
                
        except FileNotFoundError:
            logger.error("Certbot not found. Please install certbot first.")
    
    def setup_ssl_auto_renewal(self):
        """Setup automatic SSL certificate renewal"""
        logger.info("Setting up SSL auto-renewal...")
        
        # Create renewal script
        renewal_script = """#!/bin/bash
# SSL Certificate Auto-Renewal Script
certbot renew --quiet --nginx
systemctl reload nginx
"""
        
        renewal_script_path = self.deployment_dir / 'ssl_renewal.sh'
        with open(renewal_script_path, 'w') as f:
            f.write(renewal_script)
        
        # Make script executable
        os.chmod(renewal_script_path, 0o755)
        
        # Setup cron job for renewal
        cron_job = "0 12 * * * /path/to/ssl_renewal.sh"
        logger.info(f"Add this cron job for SSL renewal: {cron_job}")
    
    def setup_cdn_integration(self):
        """Setup CDN integration"""
        if not self.config['cdn']['enabled']:
            logger.info("CDN is disabled in configuration")
            return
        
        logger.info("Setting up CDN integration...")
        
        cdn_config = self.config['cdn']
        
        if cdn_config['provider'] == 'cloudflare':
            self.setup_cloudflare_cdn(cdn_config)
        else:
            logger.warning(f"CDN provider {cdn_config['provider']} not supported yet")
    
    def setup_cloudflare_cdn(self, cdn_config):
        """Setup Cloudflare CDN"""
        logger.info("Setting up Cloudflare CDN...")
        
        # Cloudflare API configuration
        headers = {
            'Authorization': f'Bearer {cdn_config["api_token"]}',
            'Content-Type': 'application/json'
        }
        
        # Create DNS record for CDN
        dns_record = {
            'type': 'CNAME',
            'name': 'cdn',
            'content': self.config['server']['host'],
            'ttl': 1,
            'proxied': True
        }
        
        try:
            url = f"https://api.cloudflare.com/client/v4/zones/{cdn_config['zone_id']}/dns_records"
            response = requests.post(url, headers=headers, json=dns_record)
            
            if response.status_code == 200:
                logger.info("✓ CDN DNS record created successfully")
            else:
                logger.error(f"✗ Failed to create CDN DNS record: {response.text}")
                
        except requests.RequestException as e:
            logger.error(f"✗ Error setting up CDN: {e}")
    
    def setup_monitoring(self):
        """Setup monitoring and logging"""
        logger.info("Setting up monitoring and logging...")
        
        # Create log directory
        log_dir = Path('/var/log/crm')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create systemd service file
        service_file = f"""[Unit]
Description=CRM Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory={self.project_root}
Environment=PATH={self.project_root}/venv/bin
ExecStart={self.project_root}/venv/bin/gunicorn -w {self.config['server']['workers']} -b 127.0.0.1:8000 run:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""
        
        service_path = self.deployment_dir / 'crm.service'
        with open(service_path, 'w') as f:
            f.write(service_file)
        
        logger.info(f"Created systemd service file: {service_path}")
        logger.info("Please copy this file to /etc/systemd/system/")
    
    def setup_backup_system(self):
        """Setup automated backup system"""
        if not self.config['backup']['enabled']:
            logger.info("Backup system is disabled in configuration")
            return
        
        logger.info("Setting up backup system...")
        
        backup_config = self.config['backup']
        backup_script = f"""#!/bin/bash
# Automated Backup Script for CRM Application

BACKUP_DIR="{backup_config['storage_path']}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="crm_backup_$DATE.sql"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -h {self.config['database']['host']} -U {self.config['database']['user']} -d {self.config['database']['name']} > $BACKUP_DIR/$BACKUP_FILE

# Compress backup
gzip $BACKUP_DIR/$BACKUP_FILE

# Remove old backups (keep last {backup_config['retention_days']} days)
find $BACKUP_DIR -name "crm_backup_*.sql.gz" -mtime +{backup_config['retention_days']} -delete

# Log backup
echo "$(date): Backup completed - $BACKUP_FILE.gz" >> $BACKUP_DIR/backup.log
"""
        
        backup_script_path = self.deployment_dir / 'backup.sh'
        with open(backup_script_path, 'w') as f:
            f.write(backup_script)
        
        os.chmod(backup_script_path, 0o755)
        
        # Setup cron job for backup
        if backup_config['frequency'] == 'daily':
            cron_job = "0 2 * * * /path/to/backup.sh"
        elif backup_config['frequency'] == 'weekly':
            cron_job = "0 2 * * 0 /path/to/backup.sh"
        else:
            cron_job = "0 2 * * * /path/to/backup.sh"
        
        logger.info(f"Created backup script: {backup_script_path}")
        logger.info(f"Add this cron job for backups: {cron_job}")
    
    def generate_secret_key(self):
        """Generate a secure secret key"""
        import secrets
        return secrets.token_hex(32)
    
    def create_deployment_script(self):
        """Create a comprehensive deployment script"""
        deployment_script = f"""#!/bin/bash
# Complete CRM Production Deployment Script

set -e

echo "🚀 Starting CRM Production Deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server certbot python3-certbot-nginx

# Create application user
echo "👤 Creating application user..."
sudo useradd -r -s /bin/false crm_user || true

# Create application directories
echo "📁 Creating application directories..."
sudo mkdir -p /var/www/crm
sudo mkdir -p /var/log/crm
sudo mkdir -p {self.config['backup']['storage_path']}
sudo chown -R crm_user:crm_user /var/www/crm
sudo chown -R crm_user:crm_user /var/log/crm
sudo chown -R crm_user:crm_user {self.config['backup']['storage_path']}

# Copy application files
echo "📋 Copying application files..."
sudo cp -r {self.project_root}/* /var/www/crm/

# Setup Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd /var/www/crm
sudo -u crm_user python3 -m venv venv
sudo -u crm_user venv/bin/pip install -r requirements.txt

# Setup database
echo "🗄️ Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE {self.config['database']['name']};" || true
sudo -u postgres psql -c "CREATE USER {self.config['database']['user']} WITH PASSWORD '{self.config['database']['password']}';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {self.config['database']['name']} TO {self.config['database']['user']};"

# Setup SSL certificate
echo "🔒 Setting up SSL certificate..."
sudo certbot certonly --nginx -d {self.config['server']['host']} --non-interactive --agree-tos --email admin@{self.config['server']['host']} || echo "SSL setup failed, continuing..."

# Setup Nginx
echo "🌐 Setting up Nginx..."
sudo cp {self.deployment_dir}/nginx.conf /etc/nginx/sites-available/crm
sudo ln -sf /etc/nginx/sites-available/crm /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# Setup systemd service
echo "⚙️ Setting up systemd service..."
sudo cp {self.deployment_dir}/crm.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crm
sudo systemctl start crm

# Setup monitoring
echo "📊 Setting up monitoring..."
sudo cp {self.deployment_dir}/backup.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/backup.sh

# Setup firewall
echo "🔥 Setting up firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "✅ Deployment completed successfully!"
echo "🌐 Your CRM application is now available at: https://{self.config['server']['host']}"
echo "📊 Monitor logs with: sudo journalctl -u crm -f"
echo "🔄 Restart service with: sudo systemctl restart crm"
"""
        
        script_path = self.deployment_dir / 'deploy.sh'
        with open(script_path, 'w') as f:
            f.write(deployment_script)
        
        os.chmod(script_path, 0o755)
        logger.info(f"Created deployment script: {script_path}")
    
    def run_deployment(self):
        """Run the complete deployment process"""
        logger.info("🚀 Starting production deployment...")
        
        # Check system requirements
        if not self.check_system_requirements():
            logger.error("System requirements not met. Please install missing dependencies.")
            return False
        
        try:
            # Setup environment
            self.setup_environment()
            
            # Setup database
            self.setup_database()
            
            # Setup Nginx configuration
            self.setup_nginx_config()
            
            # Setup SSL certificate
            self.setup_ssl_certificate()
            
            # Setup CDN integration
            self.setup_cdn_integration()
            
            # Setup monitoring
            self.setup_monitoring()
            
            # Setup backup system
            self.setup_backup_system()
            
            # Create deployment script
            self.create_deployment_script()
            
            logger.info("✅ Production deployment setup completed successfully!")
            logger.info("📋 Next steps:")
            logger.info("1. Update the configuration file with your actual values")
            logger.info("2. Run the deployment script: ./deploy.sh")
            logger.info("3. Monitor the deployment logs")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            return False

def main():
    """Main function"""
    print("🚀 CRM Production Deployment Setup")
    print("=" * 50)
    
    deployment = ProductionDeployment()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--run':
        # Run actual deployment
        success = deployment.run_deployment()
        sys.exit(0 if success else 1)
    else:
        # Setup configuration only
        print("📋 Configuration setup completed!")
        print("Please update the configuration file and run:")
        print("python production_setup.py --run")

if __name__ == "__main__":
    main() 
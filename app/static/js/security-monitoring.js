/**
 * Security & Monitoring Features for CRM System
 * Includes: Security Audit, Vulnerability Scanning, Penetration Testing,
 * Backup Management, Recovery Procedures, Application Monitoring,
 * Error Tracking, Performance Logging, User Activity Monitoring,
 * System Health Dashboard
 */

class SecurityMonitoring {
    constructor() {
        this.securityAlerts = [];
        this.vulnerabilities = [];
        this.backupStatus = {};
        this.systemMetrics = {};
        this.userActivities = [];
        this.errorLogs = [];
        
        this.init();
    }

    init() {
        this.initSecurityAudit();
        this.initVulnerabilityScanner();
        this.initPenetrationTester();
        this.initBackupManager();
        this.initRecoveryProcedures();
        this.initApplicationMonitor();
        this.initErrorTracker();
        this.initPerformanceLogger();
        this.initUserActivityMonitor();
        this.initSystemHealthDashboard();
    }

    // ==================== SECURITY AUDIT DASHBOARD ====================
    initSecurityAudit() {
        this.createSecurityAuditDashboard();
        this.startSecurityMonitoring();
    }

    createSecurityAuditDashboard() {
        const container = document.getElementById('security-audit');
        if (!container) return;

        container.innerHTML = `
            <div class="security-audit-dashboard">
                <div class="audit-header">
                    <h3>Security Audit Dashboard</h3>
                    <div class="audit-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.runSecurityAudit()">
                            <i class="fas fa-shield-alt"></i> Run Security Audit
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.exportAuditReport()">
                            <i class="fas fa-download"></i> Export Report
                        </button>
                    </div>
                </div>
                
                <div class="security-overview">
                    <div class="security-score-card">
                        <h4>Security Score</h4>
                        <div class="score-circle">
                            <span class="score-value" id="security-score">85</span>
                            <span class="score-label">/ 100</span>
                        </div>
                        <div class="score-status">Good</div>
                    </div>
                    
                    <div class="security-metrics">
                        <div class="metric-item">
                            <span class="metric-value" id="critical-issues">2</span>
                            <span class="metric-label">Critical Issues</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-value" id="high-issues">5</span>
                            <span class="metric-label">High Issues</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-value" id="medium-issues">12</span>
                            <span class="metric-label">Medium Issues</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-value" id="low-issues">8</span>
                            <span class="metric-label">Low Issues</span>
                        </div>
                    </div>
                </div>
                
                <div class="security-alerts">
                    <h4>Security Alerts</h4>
                    <div class="alerts-list" id="security-alerts-list">
                        <!-- Alerts will be populated here -->
                    </div>
                </div>
                
                <div class="compliance-status">
                    <h4>Compliance Status</h4>
                    <div class="compliance-grid">
                        <div class="compliance-item">
                            <span class="compliance-name">GDPR</span>
                            <span class="compliance-status compliant">Compliant</span>
                        </div>
                        <div class="compliance-item">
                            <span class="compliance-name">SOC 2</span>
                            <span class="compliance-status compliant">Compliant</span>
                        </div>
                        <div class="compliance-item">
                            <span class="compliance-name">ISO 27001</span>
                            <span class="compliance-status warning">In Progress</span>
                        </div>
                        <div class="compliance-item">
                            <span class="compliance-name">HIPAA</span>
                            <span class="compliance-status compliant">Compliant</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.loadSecurityAlerts();
    }

    // ==================== VULNERABILITY SCANNING ====================
    initVulnerabilityScanner() {
        this.createVulnerabilityScanner();
    }

    createVulnerabilityScanner() {
        const container = document.getElementById('vulnerability-scanner');
        if (!container) return;

        container.innerHTML = `
            <div class="vulnerability-scanner">
                <div class="scanner-header">
                    <h3>Vulnerability Scanner</h3>
                    <div class="scanner-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.startVulnerabilityScan()">
                            <i class="fas fa-search"></i> Start Scan
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.scheduleScan()">
                            <i class="fas fa-clock"></i> Schedule Scan
                        </button>
                    </div>
                </div>
                
                <div class="scan-configuration">
                    <h4>Scan Configuration</h4>
                    <div class="config-options">
                        <label>
                            <input type="checkbox" checked> Web Application Scan
                        </label>
                        <label>
                            <input type="checkbox" checked> Network Scan
                        </label>
                        <label>
                            <input type="checkbox"> Database Scan
                        </label>
                        <label>
                            <input type="checkbox"> API Security Scan
                        </label>
                    </div>
                </div>
                
                <div class="vulnerability-results">
                    <h4>Scan Results</h4>
                    <div class="results-summary">
                        <div class="result-item critical">
                            <span class="result-count">3</span>
                            <span class="result-label">Critical</span>
                        </div>
                        <div class="result-item high">
                            <span class="result-count">7</span>
                            <span class="result-label">High</span>
                        </div>
                        <div class="result-item medium">
                            <span class="result-count">15</span>
                            <span class="result-label">Medium</span>
                        </div>
                        <div class="result-item low">
                            <span class="result-count">23</span>
                            <span class="result-label">Low</span>
                        </div>
                    </div>
                    
                    <div class="vulnerabilities-list" id="vulnerabilities-list">
                        <!-- Vulnerabilities will be populated here -->
                    </div>
                </div>
            </div>
        `;

        this.loadVulnerabilities();
    }

    // ==================== PENETRATION TESTING ====================
    initPenetrationTester() {
        this.createPenetrationTester();
    }

    createPenetrationTester() {
        const container = document.getElementById('penetration-tester');
        if (!container) return;

        container.innerHTML = `
            <div class="penetration-tester">
                <div class="tester-header">
                    <h3>Penetration Testing Tools</h3>
                    <div class="tester-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.startPenetrationTest()">
                            <i class="fas fa-bug"></i> Start Test
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.generateReport()">
                            <i class="fas fa-file-alt"></i> Generate Report
                        </button>
                    </div>
                </div>
                
                <div class="test-modules">
                    <div class="test-module">
                        <h4>SQL Injection Test</h4>
                        <p>Test for SQL injection vulnerabilities</p>
                        <button class="btn btn-sm btn-primary" onclick="securityMonitoring.runSQLInjectionTest()">
                            Run Test
                        </button>
                    </div>
                    
                    <div class="test-module">
                        <h4>XSS Test</h4>
                        <p>Test for Cross-Site Scripting vulnerabilities</p>
                        <button class="btn btn-sm btn-primary" onclick="securityMonitoring.runXSSTest()">
                            Run Test
                        </button>
                    </div>
                    
                    <div class="test-module">
                        <h4>Authentication Test</h4>
                        <p>Test authentication mechanisms</p>
                        <button class="btn btn-sm btn-primary" onclick="securityMonitoring.runAuthTest()">
                            Run Test
                        </button>
                    </div>
                    
                    <div class="test-module">
                        <h4>Authorization Test</h4>
                        <p>Test authorization controls</p>
                        <button class="btn btn-sm btn-primary" onclick="securityMonitoring.runAuthzTest()">
                            Run Test
                        </button>
                    </div>
                </div>
                
                <div class="test-results" id="penetration-results">
                    <!-- Test results will be displayed here -->
                </div>
            </div>
        `;
    }

    // ==================== BACKUP MANAGEMENT ====================
    initBackupManager() {
        this.createBackupManager();
    }

    createBackupManager() {
        const container = document.getElementById('backup-manager');
        if (!container) return;

        container.innerHTML = `
            <div class="backup-manager">
                <div class="backup-header">
                    <h3>Backup Management</h3>
                    <div class="backup-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.createBackup()">
                            <i class="fas fa-save"></i> Create Backup
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.restoreBackup()">
                            <i class="fas fa-undo"></i> Restore
                        </button>
                    </div>
                </div>
                
                <div class="backup-status">
                    <h4>Backup Status</h4>
                    <div class="status-grid">
                        <div class="status-item">
                            <span class="status-label">Last Backup</span>
                            <span class="status-value" id="last-backup-time">2024-01-15 14:30:00</span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Backup Size</span>
                            <span class="status-value" id="backup-size">2.5 GB</span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Status</span>
                            <span class="status-value success" id="backup-status">Successful</span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Next Scheduled</span>
                            <span class="status-value" id="next-backup">2024-01-16 02:00:00</span>
                        </div>
                    </div>
                </div>
                
                <div class="backup-history">
                    <h4>Backup History</h4>
                    <div class="history-table" id="backup-history">
                        <!-- Backup history will be populated here -->
                    </div>
                </div>
                
                <div class="backup-settings">
                    <h4>Backup Settings</h4>
                    <div class="settings-form">
                        <div class="form-group">
                            <label>Backup Frequency</label>
                            <select id="backup-frequency">
                                <option value="daily">Daily</option>
                                <option value="weekly">Weekly</option>
                                <option value="monthly">Monthly</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Retention Period</label>
                            <select id="retention-period">
                                <option value="7">7 days</option>
                                <option value="30">30 days</option>
                                <option value="90">90 days</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Backup Location</label>
                            <input type="text" id="backup-location" value="/backups/crm/">
                        </div>
                        <button class="btn btn-primary" onclick="securityMonitoring.saveBackupSettings()">
                            Save Settings
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.loadBackupHistory();
    }

    // ==================== RECOVERY PROCEDURES ====================
    initRecoveryProcedures() {
        this.createRecoveryProcedures();
    }

    createRecoveryProcedures() {
        const container = document.getElementById('recovery-procedures');
        if (!container) return;

        container.innerHTML = `
            <div class="recovery-procedures">
                <div class="recovery-header">
                    <h3>Recovery Procedures</h3>
                    <div class="recovery-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.testRecovery()">
                            <i class="fas fa-play"></i> Test Recovery
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.viewProcedures()">
                            <i class="fas fa-book"></i> View Procedures
                        </button>
                    </div>
                </div>
                
                <div class="recovery-plans">
                    <div class="recovery-plan">
                        <h4>Database Recovery</h4>
                        <p>Step-by-step database recovery procedures</p>
                        <div class="plan-steps">
                            <ol>
                                <li>Stop all application services</li>
                                <li>Restore database from latest backup</li>
                                <li>Apply transaction logs</li>
                                <li>Verify data integrity</li>
                                <li>Restart application services</li>
                            </ol>
                        </div>
                        <button class="btn btn-sm btn-primary" onclick="securityMonitoring.executeDatabaseRecovery()">
                            Execute Recovery
                        </button>
                    </div>
                    
                    <div class="recovery-plan">
                        <h4>Application Recovery</h4>
                        <p>Application-level recovery procedures</p>
                        <div class="plan-steps">
                            <ol>
                                <li>Identify affected components</li>
                                <li>Restore application files</li>
                                <li>Update configuration</li>
                                <li>Restart services</li>
                                <li>Verify functionality</li>
                            </ol>
                        </div>
                        <button class="btn btn-sm btn-primary" onclick="securityMonitoring.executeApplicationRecovery()">
                            Execute Recovery
                        </button>
                    </div>
                    
                    <div class="recovery-plan">
                        <h4>Disaster Recovery</h4>
                        <p>Full system disaster recovery procedures</p>
                        <div class="plan-steps">
                            <ol>
                                <li>Activate disaster recovery site</li>
                                <li>Restore complete system</li>
                                <li>Update DNS and routing</li>
                                <li>Verify all services</li>
                                <li>Notify stakeholders</li>
                            </ol>
                        </div>
                        <button class="btn btn-sm btn-primary" onclick="securityMonitoring.executeDisasterRecovery()">
                            Execute Recovery
                        </button>
                    </div>
                </div>
                
                <div class="recovery-status">
                    <h4>Recovery Status</h4>
                    <div class="status-indicators">
                        <div class="status-indicator">
                            <span class="indicator-label">Database</span>
                            <span class="indicator-status healthy">Healthy</span>
                        </div>
                        <div class="status-indicator">
                            <span class="indicator-label">Application</span>
                            <span class="indicator-status healthy">Healthy</span>
                        </div>
                        <div class="status-indicator">
                            <span class="indicator-label">Backup System</span>
                            <span class="indicator-status healthy">Healthy</span>
                        </div>
                        <div class="status-indicator">
                            <span class="indicator-label">Recovery Site</span>
                            <span class="indicator-status warning">Standby</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // ==================== APPLICATION MONITORING ====================
    initApplicationMonitor() {
        this.createApplicationMonitor();
        this.startApplicationMonitoring();
    }

    createApplicationMonitor() {
        const container = document.getElementById('application-monitor');
        if (!container) return;

        container.innerHTML = `
            <div class="application-monitor">
                <div class="monitor-header">
                    <h3>Application Monitoring</h3>
                    <div class="monitor-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.refreshMetrics()">
                            <i class="fas fa-sync"></i> Refresh
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.configureAlerts()">
                            <i class="fas fa-bell"></i> Configure Alerts
                        </button>
                    </div>
                </div>
                
                <div class="monitoring-metrics">
                    <div class="metric-card">
                        <h4>Response Time</h4>
                        <div class="metric-value" id="avg-response-time">245ms</div>
                        <div class="metric-trend positive">↓ 12%</div>
                    </div>
                    
                    <div class="metric-card">
                        <h4>Error Rate</h4>
                        <div class="metric-value" id="error-rate">0.2%</div>
                        <div class="metric-trend positive">↓ 5%</div>
                    </div>
                    
                    <div class="metric-card">
                        <h4>CPU Usage</h4>
                        <div class="metric-value" id="cpu-usage">45%</div>
                        <div class="metric-trend neutral">→ 0%</div>
                    </div>
                    
                    <div class="metric-card">
                        <h4>Memory Usage</h4>
                        <div class="metric-value" id="memory-usage">68%</div>
                        <div class="metric-trend negative">↑ 8%</div>
                    </div>
                </div>
                
                <div class="service-status">
                    <h4>Service Status</h4>
                    <div class="services-grid" id="services-status">
                        <!-- Service status will be populated here -->
                    </div>
                </div>
                
                <div class="performance-charts">
                    <h4>Performance Trends</h4>
                    <div class="charts-container">
                        <div class="chart-container">
                            <canvas id="response-time-chart"></canvas>
                        </div>
                        <div class="chart-container">
                            <canvas id="error-rate-chart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.loadServiceStatus();
        this.initPerformanceCharts();
    }

    // ==================== ERROR TRACKING ====================
    initErrorTracker() {
        this.createErrorTracker();
        this.startErrorTracking();
    }

    createErrorTracker() {
        const container = document.getElementById('error-tracker');
        if (!container) return;

        container.innerHTML = `
            <div class="error-tracker">
                <div class="tracker-header">
                    <h3>Error Tracking</h3>
                    <div class="tracker-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.clearErrors()">
                            <i class="fas fa-trash"></i> Clear Errors
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.exportErrorLog()">
                            <i class="fas fa-download"></i> Export Log
                        </button>
                    </div>
                </div>
                
                <div class="error-summary">
                    <div class="error-stat">
                        <span class="stat-value" id="total-errors">1,234</span>
                        <span class="stat-label">Total Errors</span>
                    </div>
                    <div class="error-stat">
                        <span class="stat-value" id="critical-errors">23</span>
                        <span class="stat-label">Critical</span>
                    </div>
                    <div class="error-stat">
                        <span class="stat-value" id="resolved-errors">1,156</span>
                        <span class="stat-label">Resolved</span>
                    </div>
                    <div class="error-stat">
                        <span class="stat-value" id="open-errors">78</span>
                        <span class="stat-label">Open</span>
                    </div>
                </div>
                
                <div class="error-filters">
                    <div class="filter-group">
                        <label>Error Level</label>
                        <select id="error-level-filter">
                            <option value="all">All Levels</option>
                            <option value="critical">Critical</option>
                            <option value="error">Error</option>
                            <option value="warning">Warning</option>
                            <option value="info">Info</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Time Range</label>
                        <select id="time-range-filter">
                            <option value="1h">Last Hour</option>
                            <option value="24h">Last 24 Hours</option>
                            <option value="7d">Last 7 Days</option>
                            <option value="30d">Last 30 Days</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" onclick="securityMonitoring.applyErrorFilters()">
                        Apply Filters
                    </button>
                </div>
                
                <div class="error-list" id="error-list">
                    <!-- Error list will be populated here -->
                </div>
            </div>
        `;

        this.loadErrorLogs();
    }

    // ==================== PERFORMANCE LOGGING ====================
    initPerformanceLogger() {
        this.createPerformanceLogger();
        this.startPerformanceLogging();
    }

    createPerformanceLogger() {
        const container = document.getElementById('performance-logger');
        if (!container) return;

        container.innerHTML = `
            <div class="performance-logger">
                <div class="logger-header">
                    <h3>Performance Logging</h3>
                    <div class="logger-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.startLogging()">
                            <i class="fas fa-play"></i> Start Logging
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.stopLogging()">
                            <i class="fas fa-stop"></i> Stop Logging
                        </button>
                    </div>
                </div>
                
                <div class="logging-configuration">
                    <h4>Logging Configuration</h4>
                    <div class="config-options">
                        <label>
                            <input type="checkbox" checked> Database Queries
                        </label>
                        <label>
                            <input type="checkbox" checked> API Calls
                        </label>
                        <label>
                            <input type="checkbox" checked> Page Load Times
                        </label>
                        <label>
                            <input type="checkbox"> Memory Usage
                        </label>
                        <label>
                            <input type="checkbox"> CPU Usage
                        </label>
                    </div>
                </div>
                
                <div class="performance-metrics">
                    <h4>Performance Metrics</h4>
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <span class="metric-name">Average Query Time</span>
                            <span class="metric-value">45ms</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-name">Slow Queries (>1s)</span>
                            <span class="metric-value">12</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-name">API Response Time</span>
                            <span class="metric-value">180ms</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-name">Page Load Time</span>
                            <span class="metric-value">850ms</span>
                        </div>
                    </div>
                </div>
                
                <div class="performance-logs" id="performance-logs">
                    <!-- Performance logs will be displayed here -->
                </div>
            </div>
        `;

        this.loadPerformanceLogs();
    }

    // ==================== USER ACTIVITY MONITORING ====================
    initUserActivityMonitor() {
        this.createUserActivityMonitor();
        this.startUserActivityMonitoring();
    }

    createUserActivityMonitor() {
        const container = document.getElementById('user-activity-monitor');
        if (!container) return;

        container.innerHTML = `
            <div class="user-activity-monitor">
                <div class="activity-header">
                    <h3>User Activity Monitoring</h3>
                    <div class="activity-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.refreshActivity()">
                            <i class="fas fa-sync"></i> Refresh
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.exportActivity()">
                            <i class="fas fa-download"></i> Export
                        </button>
                    </div>
                </div>
                
                <div class="activity-summary">
                    <div class="summary-item">
                        <span class="summary-value" id="active-users">45</span>
                        <span class="summary-label">Active Users</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-value" id="total-sessions">156</span>
                        <span class="summary-label">Total Sessions</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-value" id="failed-logins">8</span>
                        <span class="summary-label">Failed Logins</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-value" id="suspicious-activities">3</span>
                        <span class="summary-label">Suspicious Activities</span>
                    </div>
                </div>
                
                <div class="activity-filters">
                    <div class="filter-group">
                        <label>User</label>
                        <select id="user-filter">
                            <option value="all">All Users</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Activity Type</label>
                        <select id="activity-type-filter">
                            <option value="all">All Activities</option>
                            <option value="login">Login</option>
                            <option value="logout">Logout</option>
                            <option value="data_access">Data Access</option>
                            <option value="data_modification">Data Modification</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Time Range</label>
                        <select id="activity-time-filter">
                            <option value="1h">Last Hour</option>
                            <option value="24h">Last 24 Hours</option>
                            <option value="7d">Last 7 Days</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" onclick="securityMonitoring.applyActivityFilters()">
                        Apply Filters
                    </button>
                </div>
                
                <div class="activity-timeline" id="activity-timeline">
                    <!-- Activity timeline will be populated here -->
                </div>
            </div>
        `;

        this.loadUserActivities();
    }

    // ==================== SYSTEM HEALTH DASHBOARD ====================
    initSystemHealthDashboard() {
        this.createSystemHealthDashboard();
        this.startSystemHealthMonitoring();
    }

    createSystemHealthDashboard() {
        const container = document.getElementById('system-health');
        if (!container) return;

        container.innerHTML = `
            <div class="system-health-dashboard">
                <div class="health-header">
                    <h3>System Health Dashboard</h3>
                    <div class="health-controls">
                        <button class="btn btn-primary" onclick="securityMonitoring.refreshHealth()">
                            <i class="fas fa-heartbeat"></i> Refresh Health
                        </button>
                        <button class="btn btn-secondary" onclick="securityMonitoring.generateHealthReport()">
                            <i class="fas fa-file-medical"></i> Health Report
                        </button>
                    </div>
                </div>
                
                <div class="health-overview">
                    <div class="health-score">
                        <h4>Overall Health Score</h4>
                        <div class="health-circle">
                            <span class="health-value" id="health-score">92</span>
                            <span class="health-label">/ 100</span>
                        </div>
                        <div class="health-status">Excellent</div>
                    </div>
                    
                    <div class="health-metrics">
                        <div class="health-metric">
                            <span class="metric-name">System Uptime</span>
                            <span class="metric-value" id="uptime">99.8%</span>
                        </div>
                        <div class="health-metric">
                            <span class="metric-name">Disk Usage</span>
                            <span class="metric-value" id="disk-usage">67%</span>
                        </div>
                        <div class="health-metric">
                            <span class="metric-name">Network Status</span>
                            <span class="metric-value" id="network-status">Healthy</span>
                        </div>
                        <div class="health-metric">
                            <span class="metric-name">Security Status</span>
                            <span class="metric-value" id="security-status">Secure</span>
                        </div>
                    </div>
                </div>
                
                <div class="system-components">
                    <h4>System Components</h4>
                    <div class="components-grid" id="components-status">
                        <!-- Component status will be populated here -->
                    </div>
                </div>
                
                <div class="health-alerts">
                    <h4>Health Alerts</h4>
                    <div class="alerts-list" id="health-alerts">
                        <!-- Health alerts will be populated here -->
                    </div>
                </div>
            </div>
        `;

        this.loadSystemComponents();
        this.loadHealthAlerts();
    }

    // ==================== UTILITY METHODS ====================
    startSecurityMonitoring() {
        setInterval(() => {
            this.updateSecurityMetrics();
        }, 30000); // Update every 30 seconds
    }

    startApplicationMonitoring() {
        setInterval(() => {
            this.updateApplicationMetrics();
        }, 10000); // Update every 10 seconds
    }

    startErrorTracking() {
        setInterval(() => {
            this.updateErrorMetrics();
        }, 5000); // Update every 5 seconds
    }

    startPerformanceLogging() {
        setInterval(() => {
            this.logPerformanceMetrics();
        }, 60000); // Log every minute
    }

    startUserActivityMonitoring() {
        setInterval(() => {
            this.updateUserActivityMetrics();
        }, 15000); // Update every 15 seconds
    }

    startSystemHealthMonitoring() {
        setInterval(() => {
            this.updateSystemHealthMetrics();
        }, 30000); // Update every 30 seconds
    }

    showNotification(message, type = 'info') {
        if (window.enhancedUX) {
            window.enhancedUX.showNotification(message, type);
        }
    }

    // Placeholder methods for actual implementation
    runSecurityAudit() {
        this.showNotification('Running security audit...', 'info');
        setTimeout(() => {
            this.showNotification('Security audit completed successfully', 'success');
        }, 3000);
    }

    startVulnerabilityScan() {
        this.showNotification('Starting vulnerability scan...', 'info');
        setTimeout(() => {
            this.showNotification('Vulnerability scan completed', 'success');
        }, 5000);
    }

    createBackup() {
        this.showNotification('Creating backup...', 'info');
        setTimeout(() => {
            this.showNotification('Backup created successfully', 'success');
        }, 2000);
    }

    loadSecurityAlerts() {
        // Implementation for loading security alerts
    }

    loadVulnerabilities() {
        // Implementation for loading vulnerabilities
    }

    loadBackupHistory() {
        // Implementation for loading backup history
    }

    loadServiceStatus() {
        // Implementation for loading service status
    }

    loadErrorLogs() {
        // Implementation for loading error logs
    }

    loadPerformanceLogs() {
        // Implementation for loading performance logs
    }

    loadUserActivities() {
        // Implementation for loading user activities
    }

    loadSystemComponents() {
        // Implementation for loading system components
    }

    loadHealthAlerts() {
        // Implementation for loading health alerts
    }

    initPerformanceCharts() {
        // Implementation for initializing performance charts
    }

    updateSecurityMetrics() {
        // Implementation for updating security metrics
    }

    updateApplicationMetrics() {
        // Implementation for updating application metrics
    }

    updateErrorMetrics() {
        // Implementation for updating error metrics
    }

    logPerformanceMetrics() {
        // Implementation for logging performance metrics
    }

    updateUserActivityMetrics() {
        // Implementation for updating user activity metrics
    }

    updateSystemHealthMetrics() {
        // Implementation for updating system health metrics
    }
}

// Initialize Security Monitoring when DOM is loaded
let securityMonitoring;
document.addEventListener('DOMContentLoaded', () => {
    securityMonitoring = new SecurityMonitoring();
});

// Export for global access
window.securityMonitoring = securityMonitoring; 
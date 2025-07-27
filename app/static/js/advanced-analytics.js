/**
 * Advanced Analytics Features for CRM System
 * Includes: Predictive Analytics, Custom Dashboard Builder, 
 * Advanced Data Filtering, Data Mining, Machine Learning Insights
 */

class AdvancedAnalytics {
    constructor() {
        this.charts = new Map();
        this.dashboards = new Map();
        this.filters = new Map();
        this.mlModels = new Map();
        this.dataCache = new Map();
        
        this.init();
    }

    init() {
        this.initPredictiveAnalytics();
        this.initDashboardBuilder();
        this.initAdvancedFiltering();
        this.initDataMining();
        this.initMachineLearning();
    }

    // ==================== PREDICTIVE ANALYTICS ====================
    initPredictiveAnalytics() {
        this.createPredictiveDashboard();
        this.loadPredictiveModels();
    }

    createPredictiveDashboard() {
        const container = document.getElementById('predictive-analytics');
        if (!container) return;

        container.innerHTML = `
            <div class="predictive-dashboard">
                <div class="dashboard-header">
                    <h3>Predictive Analytics Dashboard</h3>
                    <div class="dashboard-controls">
                        <button class="btn btn-primary" onclick="advancedAnalytics.refreshPredictions()">
                            <i class="fas fa-sync"></i> Refresh Predictions
                        </button>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.exportPredictions()">
                            <i class="fas fa-download"></i> Export
                        </button>
                    </div>
                </div>
                
                <div class="predictive-grid">
                    <div class="prediction-card">
                        <h4>Lead Conversion Probability</h4>
                        <div class="prediction-chart" id="lead-conversion-chart"></div>
                        <div class="prediction-stats">
                            <div class="stat">
                                <span class="stat-value" id="avg-conversion-rate">0%</span>
                                <span class="stat-label">Avg Conversion Rate</span>
                            </div>
                            <div class="stat">
                                <span class="stat-value" id="predicted-conversions">0</span>
                                <span class="stat-label">Predicted This Month</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prediction-card">
                        <h4>Revenue Forecasting</h4>
                        <div class="prediction-chart" id="revenue-forecast-chart"></div>
                        <div class="prediction-stats">
                            <div class="stat">
                                <span class="stat-value" id="predicted-revenue">$0</span>
                                <span class="stat-label">Predicted Revenue</span>
                            </div>
                            <div class="stat">
                                <span class="stat-value" id="growth-rate">0%</span>
                                <span class="stat-label">Growth Rate</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prediction-card">
                        <h4>Churn Prediction</h4>
                        <div class="prediction-chart" id="churn-prediction-chart"></div>
                        <div class="prediction-stats">
                            <div class="stat">
                                <span class="stat-value" id="churn-risk">0%</span>
                                <span class="stat-label">High Risk Customers</span>
                            </div>
                            <div class="stat">
                                <span class="stat-value" id="retention-rate">0%</span>
                                <span class="stat-label">Retention Rate</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prediction-card">
                        <h4>Next Best Action</h4>
                        <div class="action-recommendations" id="action-recommendations">
                            <div class="loading">Loading recommendations...</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.initPredictionCharts();
    }

    initPredictionCharts() {
        // Lead Conversion Chart
        this.createChart('lead-conversion-chart', {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Actual Conversion Rate',
                    data: [12, 15, 18, 14, 20, 22],
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)'
                }, {
                    label: 'Predicted Conversion Rate',
                    data: [null, null, null, 16, 19, 24],
                    borderColor: '#28a745',
                    borderDash: [5, 5],
                    backgroundColor: 'rgba(40, 167, 69, 0.1)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Lead Conversion Trends'
                    }
                }
            }
        });

        // Revenue Forecast Chart
        this.createChart('revenue-forecast-chart', {
            type: 'bar',
            data: {
                labels: ['Q1', 'Q2', 'Q3', 'Q4'],
                datasets: [{
                    label: 'Actual Revenue',
                    data: [150000, 180000, 220000, null],
                    backgroundColor: '#007bff'
                }, {
                    label: 'Predicted Revenue',
                    data: [null, null, null, 250000],
                    backgroundColor: '#28a745'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Revenue Forecast'
                    }
                }
            }
        });

        // Churn Prediction Chart
        this.createChart('churn-prediction-chart', {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: [65, 25, 10],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Customer Churn Risk'
                    }
                }
            }
        });
    }

    // ==================== CUSTOM DASHBOARD BUILDER ====================
    initDashboardBuilder() {
        this.createDashboardBuilder();
    }

    createDashboardBuilder() {
        const container = document.getElementById('dashboard-builder');
        if (!container) return;

        container.innerHTML = `
            <div class="dashboard-builder">
                <div class="builder-header">
                    <h3>Custom Dashboard Builder</h3>
                    <div class="builder-controls">
                        <button class="btn btn-primary" onclick="advancedAnalytics.saveDashboard()">
                            <i class="fas fa-save"></i> Save Dashboard
                        </button>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.loadDashboard()">
                            <i class="fas fa-folder-open"></i> Load Dashboard
                        </button>
                    </div>
                </div>
                
                <div class="builder-layout">
                    <div class="widget-palette">
                        <h4>Available Widgets</h4>
                        <div class="widget-list">
                            <div class="widget-item" draggable="true" data-widget="chart">
                                <i class="fas fa-chart-line"></i>
                                <span>Chart Widget</span>
                            </div>
                            <div class="widget-item" draggable="true" data-widget="metric">
                                <i class="fas fa-tachometer-alt"></i>
                                <span>Metric Widget</span>
                            </div>
                            <div class="widget-item" draggable="true" data-widget="table">
                                <i class="fas fa-table"></i>
                                <span>Table Widget</span>
                            </div>
                            <div class="widget-item" draggable="true" data-widget="filter">
                                <i class="fas fa-filter"></i>
                                <span>Filter Widget</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="dashboard-canvas">
                        <h4>Dashboard Canvas</h4>
                        <div class="canvas-grid" id="dashboard-canvas">
                            <div class="drop-zone">Drop widgets here to build your dashboard</div>
                        </div>
                    </div>
                    
                    <div class="widget-properties">
                        <h4>Widget Properties</h4>
                        <div class="properties-panel" id="widget-properties">
                            <p>Select a widget to configure its properties</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.initDashboardDragAndDrop();
    }

    initDashboardDragAndDrop() {
        const canvas = document.getElementById('dashboard-canvas');
        const widgets = document.querySelectorAll('.widget-item');

        widgets.forEach(widget => {
            widget.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', widget.dataset.widget);
            });
        });

        canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        canvas.addEventListener('drop', (e) => {
            e.preventDefault();
            const widgetType = e.dataTransfer.getData('text/plain');
            this.addWidgetToCanvas(widgetType, e.clientX, e.clientY);
        });
    }

    addWidgetToCanvas(widgetType, x, y) {
        const canvas = document.getElementById('dashboard-canvas');
        const widget = this.createWidget(widgetType);
        
        // Position widget at drop location
        const rect = canvas.getBoundingClientRect();
        const relativeX = x - rect.left;
        const relativeY = y - rect.top;
        
        widget.style.position = 'absolute';
        widget.style.left = relativeX + 'px';
        widget.style.top = relativeY + 'px';
        
        canvas.appendChild(widget);
        this.makeWidgetDraggable(widget);
    }

    createWidget(type) {
        const widget = document.createElement('div');
        widget.className = 'dashboard-widget';
        widget.dataset.widgetType = type;
        
        switch(type) {
            case 'chart':
                widget.innerHTML = `
                    <div class="widget-header">
                        <h5>Chart Widget</h5>
                        <div class="widget-controls">
                            <button onclick="advancedAnalytics.configureWidget(this.parentElement.parentElement)">⚙️</button>
                            <button onclick="advancedAnalytics.removeWidget(this.parentElement.parentElement)">×</button>
                        </div>
                    </div>
                    <div class="widget-content">
                        <canvas id="chart-${Date.now()}"></canvas>
                    </div>
                `;
                break;
            case 'metric':
                widget.innerHTML = `
                    <div class="widget-header">
                        <h5>Metric Widget</h5>
                        <div class="widget-controls">
                            <button onclick="advancedAnalytics.configureWidget(this.parentElement.parentElement)">⚙️</button>
                            <button onclick="advancedAnalytics.removeWidget(this.parentElement.parentElement)">×</button>
                        </div>
                    </div>
                    <div class="widget-content">
                        <div class="metric-value">0</div>
                        <div class="metric-label">Metric Name</div>
                    </div>
                `;
                break;
            case 'table':
                widget.innerHTML = `
                    <div class="widget-header">
                        <h5>Table Widget</h5>
                        <div class="widget-controls">
                            <button onclick="advancedAnalytics.configureWidget(this.parentElement.parentElement)">⚙️</button>
                            <button onclick="advancedAnalytics.removeWidget(this.parentElement.parentElement)">×</button>
                        </div>
                    </div>
                    <div class="widget-content">
                        <table class="data-table">
                            <thead><tr><th>Column 1</th><th>Column 2</th></tr></thead>
                            <tbody><tr><td>Data 1</td><td>Data 2</td></tr></tbody>
                        </table>
                    </div>
                `;
                break;
        }
        
        return widget;
    }

    // ==================== ADVANCED DATA FILTERING ====================
    initAdvancedFiltering() {
        this.createAdvancedFilters();
    }

    createAdvancedFilters() {
        const container = document.getElementById('advanced-filters');
        if (!container) return;

        container.innerHTML = `
            <div class="advanced-filters">
                <div class="filters-header">
                    <h3>Advanced Data Filtering</h3>
                    <button class="btn btn-primary" onclick="advancedAnalytics.applyFilters()">
                        Apply Filters
                    </button>
                </div>
                
                <div class="filters-container">
                    <div class="filter-group">
                        <h4>Date Range</h4>
                        <div class="filter-controls">
                            <input type="date" id="start-date" class="form-control">
                            <span>to</span>
                            <input type="date" id="end-date" class="form-control">
                        </div>
                    </div>
                    
                    <div class="filter-group">
                        <h4>Lead Status</h4>
                        <div class="filter-controls">
                            <label><input type="checkbox" value="new"> New</label>
                            <label><input type="checkbox" value="qualified"> Qualified</label>
                            <label><input type="checkbox" value="converted"> Converted</label>
                            <label><input type="checkbox" value="lost"> Lost</label>
                        </div>
                    </div>
                    
                    <div class="filter-group">
                        <h4>Revenue Range</h4>
                        <div class="filter-controls">
                            <input type="number" id="min-revenue" placeholder="Min Revenue" class="form-control">
                            <span>to</span>
                            <input type="number" id="max-revenue" placeholder="Max Revenue" class="form-control">
                        </div>
                    </div>
                    
                    <div class="filter-group">
                        <h4>Custom Filters</h4>
                        <div class="custom-filters" id="custom-filters">
                            <button class="btn btn-secondary" onclick="advancedAnalytics.addCustomFilter()">
                                <i class="fas fa-plus"></i> Add Filter
                            </button>
                        </div>
                    </div>
                </div>
                
                <div class="filter-results">
                    <h4>Filter Results</h4>
                    <div class="results-summary">
                        <span id="filtered-count">0</span> records match your filters
                    </div>
                    <div class="results-table" id="filtered-results">
                        <!-- Results will be populated here -->
                    </div>
                </div>
            </div>
        `;
    }

    // ==================== DATA MINING CAPABILITIES ====================
    initDataMining() {
        this.createDataMiningInterface();
    }

    createDataMiningInterface() {
        const container = document.getElementById('data-mining');
        if (!container) return;

        container.innerHTML = `
            <div class="data-mining">
                <div class="mining-header">
                    <h3>Data Mining & Pattern Analysis</h3>
                    <button class="btn btn-primary" onclick="advancedAnalytics.runDataMining()">
                        <i class="fas fa-search"></i> Run Analysis
                    </button>
                </div>
                
                <div class="mining-tools">
                    <div class="mining-tool">
                        <h4>Correlation Analysis</h4>
                        <p>Find relationships between different data points</p>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.runCorrelationAnalysis()">
                            Analyze Correlations
                        </button>
                    </div>
                    
                    <div class="mining-tool">
                        <h4>Trend Analysis</h4>
                        <p>Identify patterns and trends in your data</p>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.runTrendAnalysis()">
                            Analyze Trends
                        </button>
                    </div>
                    
                    <div class="mining-tool">
                        <h4>Anomaly Detection</h4>
                        <p>Find unusual patterns in your data</p>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.runAnomalyDetection()">
                            Detect Anomalies
                        </button>
                    </div>
                    
                    <div class="mining-tool">
                        <h4>Segmentation Analysis</h4>
                        <p>Group similar data points together</p>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.runSegmentationAnalysis()">
                            Segment Data
                        </button>
                    </div>
                </div>
                
                <div class="mining-results" id="mining-results">
                    <!-- Results will be displayed here -->
                </div>
            </div>
        `;
    }

    // ==================== MACHINE LEARNING INSIGHTS ====================
    initMachineLearning() {
        this.createMLInsightsInterface();
    }

    createMLInsightsInterface() {
        const container = document.getElementById('ml-insights');
        if (!container) return;

        container.innerHTML = `
            <div class="ml-insights">
                <div class="ml-header">
                    <h3>Machine Learning Insights</h3>
                    <button class="btn btn-primary" onclick="advancedAnalytics.refreshMLInsights()">
                        <i class="fas fa-brain"></i> Refresh Insights
                    </button>
                </div>
                
                <div class="insights-grid">
                    <div class="insight-card">
                        <h4>Lead Scoring Model</h4>
                        <div class="model-status">
                            <span class="status-indicator active"></span>
                            <span>Model Active</span>
                        </div>
                        <div class="model-metrics">
                            <div class="metric">
                                <span class="metric-value">94.2%</span>
                                <span class="metric-label">Accuracy</span>
                            </div>
                            <div class="metric">
                                <span class="metric-value">0.89</span>
                                <span class="metric-label">Precision</span>
                            </div>
                        </div>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.retrainModel('lead-scoring')">
                            Retrain Model
                        </button>
                    </div>
                    
                    <div class="insight-card">
                        <h4>Churn Prediction Model</h4>
                        <div class="model-status">
                            <span class="status-indicator active"></span>
                            <span>Model Active</span>
                        </div>
                        <div class="model-metrics">
                            <div class="metric">
                                <span class="metric-value">91.8%</span>
                                <span class="metric-label">Accuracy</span>
                            </div>
                            <div class="metric">
                                <span class="metric-value">0.87</span>
                                <span class="metric-label">Recall</span>
                            </div>
                        </div>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.retrainModel('churn-prediction')">
                            Retrain Model
                        </button>
                    </div>
                    
                    <div class="insight-card">
                        <h4>Revenue Forecasting Model</h4>
                        <div class="model-status">
                            <span class="status-indicator active"></span>
                            <span>Model Active</span>
                        </div>
                        <div class="model-metrics">
                            <div class="metric">
                                <span class="metric-value">88.5%</span>
                                <span class="metric-label">Accuracy</span>
                            </div>
                            <div class="metric">
                                <span class="metric-value">0.92</span>
                                <span class="metric-label">R² Score</span>
                            </div>
                        </div>
                        <button class="btn btn-secondary" onclick="advancedAnalytics.retrainModel('revenue-forecast')">
                            Retrain Model
                        </button>
                    </div>
                </div>
                
                <div class="ml-recommendations">
                    <h4>AI Recommendations</h4>
                    <div class="recommendations-list" id="ai-recommendations">
                        <!-- AI recommendations will be populated here -->
                    </div>
                </div>
            </div>
        `;

        this.loadMLRecommendations();
    }

    // ==================== UTILITY METHODS ====================
    createChart(canvasId, config) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const chart = new Chart(ctx, config);
        this.charts.set(canvasId, chart);
        return chart;
    }

    refreshPredictions() {
        // Simulate API call to refresh predictions
        this.showNotification('Refreshing predictions...', 'info');
        
        setTimeout(() => {
            this.updatePredictionStats();
            this.showNotification('Predictions updated successfully', 'success');
        }, 2000);
    }

    updatePredictionStats() {
        // Update prediction statistics
        document.getElementById('avg-conversion-rate').textContent = '18.5%';
        document.getElementById('predicted-conversions').textContent = '45';
        document.getElementById('predicted-revenue').textContent = '$285,000';
        document.getElementById('growth-rate').textContent = '+12.3%';
        document.getElementById('churn-risk').textContent = '8.2%';
        document.getElementById('retention-rate').textContent = '91.8%';
    }

    loadMLRecommendations() {
        const recommendations = [
            {
                type: 'optimization',
                title: 'Lead Nurturing Optimization',
                description: 'Based on recent data, leads contacted within 5 minutes have 3x higher conversion rates.',
                action: 'Optimize lead response time'
            },
            {
                type: 'alert',
                title: 'High Churn Risk Detected',
                description: '15 customers show high churn probability. Recommend proactive outreach.',
                action: 'Review at-risk customers'
            },
            {
                type: 'opportunity',
                title: 'Revenue Growth Opportunity',
                description: 'Cross-selling to existing customers could increase revenue by 23%.',
                action: 'Create cross-sell campaign'
            }
        ];

        const container = document.getElementById('ai-recommendations');
        container.innerHTML = recommendations.map(rec => `
            <div class="recommendation-item ${rec.type}">
                <div class="recommendation-icon">
                    <i class="fas fa-${rec.type === 'optimization' ? 'cog' : rec.type === 'alert' ? 'exclamation-triangle' : 'lightbulb'}"></i>
                </div>
                <div class="recommendation-content">
                    <h5>${rec.title}</h5>
                    <p>${rec.description}</p>
                    <button class="btn btn-sm btn-primary">${rec.action}</button>
                </div>
            </div>
        `).join('');
    }

    showNotification(message, type = 'info') {
        if (window.enhancedUX) {
            window.enhancedUX.showNotification(message, type);
        }
    }
}

// Initialize Advanced Analytics when DOM is loaded
let advancedAnalytics;
document.addEventListener('DOMContentLoaded', () => {
    advancedAnalytics = new AdvancedAnalytics();
});

// Export for global access
window.advancedAnalytics = advancedAnalytics; 
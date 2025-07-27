/**
 * Modern CRM JavaScript Framework
 * Enhanced UI interactions, animations, and functionality
 */

class ModernCRM {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupAnimations();
        this.setupResponsive();
    }

    setupEventListeners() {
        // Navigation scroll effect
        window.addEventListener('scroll', this.handleScroll.bind(this));
        
        // Form interactions
        document.addEventListener('DOMContentLoaded', () => {
            this.setupFormInteractions();
            this.setupCardInteractions();
            this.setupButtonInteractions();
            this.setupModalInteractions();
            this.setupTableInteractions();
        });

        // Touch interactions for mobile
        if ('ontouchstart' in window) {
            this.setupTouchInteractions();
        }
    }

    handleScroll() {
        const navbar = document.querySelector('.modern-navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    }

    setupFormInteractions() {
        // Enhanced form inputs
        const formInputs = document.querySelectorAll('.form-control, .form-input');
        formInputs.forEach(input => {
            // Focus effects
            input.addEventListener('focus', (e) => {
                this.addFocusEffect(e.target);
            });

            input.addEventListener('blur', (e) => {
                this.removeFocusEffect(e.target);
            });

            // Real-time validation feedback
            input.addEventListener('input', (e) => {
                this.validateInput(e.target);
            });
        });

        // Form submission with loading states
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmission(e);
            });
        });
    }

    addFocusEffect(element) {
        element.style.transform = 'translateY(-2px)';
        element.style.boxShadow = '0 0 20px rgba(0, 212, 255, 0.3)';
        
        // Add floating label effect
        const label = element.parentElement.querySelector('.form-label');
        if (label) {
            label.style.color = 'var(--neon-blue)';
            label.style.transform = 'translateY(-5px) scale(0.9)';
        }
    }

    removeFocusEffect(element) {
        element.style.transform = 'translateY(0)';
        element.style.boxShadow = '';
        
        // Remove floating label effect
        const label = element.parentElement.querySelector('.form-label');
        if (label) {
            label.style.color = 'var(--text-secondary)';
            label.style.transform = 'translateY(0) scale(1)';
        }
    }

    validateInput(element) {
        const value = element.value.trim();
        const isValid = value.length > 0;
        
        if (isValid) {
            element.classList.add('is-valid');
            element.classList.remove('is-invalid');
        } else {
            element.classList.remove('is-valid');
            element.classList.add('is-invalid');
        }
    }

    handleFormSubmission(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        
        if (submitBtn) {
            // Add loading state
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            
            // Update button text
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            
            // Reset after form submission (you can customize this)
            setTimeout(() => {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 3000);
        }
    }

    setupCardInteractions() {
        const cards = document.querySelectorAll('.glass-card, .card');
        cards.forEach(card => {
            // Hover effects
            card.addEventListener('mouseenter', (e) => {
                this.addCardHoverEffect(e.target);
            });

            card.addEventListener('mouseleave', (e) => {
                this.removeCardHoverEffect(e.target);
            });

            // Click effects
            card.addEventListener('click', (e) => {
                this.addCardClickEffect(e.target);
            });
        });
    }

    addCardHoverEffect(card) {
        card.style.transform = 'translateY(-5px) scale(1.02)';
        card.style.boxShadow = 'var(--shadow-glass), var(--shadow-float)';
    }

    removeCardHoverEffect(card) {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = 'var(--shadow-glass)';
    }

    addCardClickEffect(card) {
        card.style.transform = 'scale(0.98)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);
    }

    setupButtonInteractions() {
        const buttons = document.querySelectorAll('.btn-modern, .btn-neon, .btn');
        buttons.forEach(button => {
            // Ripple effect
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e);
            });

            // Loading states
            if (button.type === 'submit') {
                button.addEventListener('click', (e) => {
                    this.addButtonLoadingState(e.target);
                });
            }
        });
    }

    createRippleEffect(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        button.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    addButtonLoadingState(button) {
        button.classList.add('loading');
        button.disabled = true;
        
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        
        setTimeout(() => {
            button.classList.remove('loading');
            button.disabled = false;
            button.innerHTML = originalText;
        }, 2000);
    }

    setupModalInteractions() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            // Enhanced modal animations
            modal.addEventListener('show.bs.modal', (e) => {
                this.animateModalShow(e.target);
            });

            modal.addEventListener('hide.bs.modal', (e) => {
                this.animateModalHide(e.target);
            });
        });
    }

    animateModalShow(modal) {
        const modalContent = modal.querySelector('.modal-content');
        modalContent.style.transform = 'scale(0.8)';
        modalContent.style.opacity = '0';
        
        setTimeout(() => {
            modalContent.style.transform = 'scale(1)';
            modalContent.style.opacity = '1';
        }, 100);
    }

    animateModalHide(modal) {
        const modalContent = modal.querySelector('.modal-content');
        modalContent.style.transform = 'scale(0.8)';
        modalContent.style.opacity = '0';
    }

    setupTableInteractions() {
        const tables = document.querySelectorAll('.table-modern, .table');
        tables.forEach(table => {
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.addEventListener('mouseenter', (e) => {
                    e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
                });

                row.addEventListener('mouseleave', (e) => {
                    e.target.style.backgroundColor = '';
                });
            });
        });
    }

    setupTouchInteractions() {
        // Touch-friendly interactions
        const touchElements = document.querySelectorAll('.btn-modern, .card, .nav-link');
        touchElements.forEach(element => {
            element.addEventListener('touchstart', (e) => {
                this.addTouchEffect(e.target);
            });

            element.addEventListener('touchend', (e) => {
                this.removeTouchEffect(e.target);
            });
        });
    }

    addTouchEffect(element) {
        element.style.transform = 'scale(0.95)';
        element.style.transition = 'transform 0.1s ease';
    }

    removeTouchEffect(element) {
        element.style.transform = 'scale(1)';
    }

    initializeComponents() {
        // Initialize tooltips
        this.initializeTooltips();
        
        // Initialize notifications
        this.initializeNotifications();
        
        // Initialize search functionality
        this.initializeSearch();
        
        // Initialize charts (if Chart.js is available)
        this.initializeCharts();
    }

    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                template: '<div class="tooltip modern-tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
            });
        });
    }

    initializeNotifications() {
        // Auto-dismiss notifications
        const notifications = document.querySelectorAll('.alert');
        notifications.forEach(notification => {
            setTimeout(() => {
                this.dismissNotification(notification);
            }, 5000);
        });
    }

    dismissNotification(notification) {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }

    initializeSearch() {
        const searchInputs = document.querySelectorAll('.search-input, input[type="search"]');
        searchInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                this.handleSearch(e.target);
            });
        });
    }

    handleSearch(input) {
        const searchTerm = input.value.toLowerCase();
        const searchableElements = document.querySelectorAll('[data-searchable]');
        
        searchableElements.forEach(element => {
            const text = element.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                element.style.display = '';
                element.style.opacity = '1';
            } else {
                element.style.opacity = '0.3';
            }
        });
    }

    initializeCharts() {
        // Initialize charts if Chart.js is available
        if (typeof Chart !== 'undefined') {
            this.setupChartDefaults();
            this.initializeDashboardCharts();
        }
    }

    setupChartDefaults() {
        Chart.defaults.color = '#a1a1aa';
        Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
        Chart.defaults.plugins.legend.labels.color = '#a1a1aa';
    }

    initializeDashboardCharts() {
        // Initialize dashboard charts
        const chartElements = document.querySelectorAll('[data-chart]');
        chartElements.forEach(element => {
            const chartType = element.dataset.chart;
            const chartData = JSON.parse(element.dataset.chartData || '{}');
            
            this.createChart(element, chartType, chartData);
        });
    }

    createChart(canvas, type, data) {
        const ctx = canvas.getContext('2d');
        return new Chart(ctx, {
            type: type,
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#a1a1aa'
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#a1a1aa'
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#a1a1aa'
                        }
                    }
                }
            }
        });
    }

    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        const animatedElements = document.querySelectorAll('.glass-card, .stat-card, .quick-action-card');
        animatedElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            element.style.transition = `all 0.6s ease ${index * 0.1}s`;
            observer.observe(element);
        });
    }

    setupResponsive() {
        // Handle responsive behavior
        this.handleResize();
        window.addEventListener('resize', this.handleResize.bind(this));
    }

    handleResize() {
        const isMobile = window.innerWidth <= 768;
        const isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
        
        // Adjust layout based on screen size
        if (isMobile) {
            document.body.classList.add('mobile-view');
            document.body.classList.remove('tablet-view', 'desktop-view');
        } else if (isTablet) {
            document.body.classList.add('tablet-view');
            document.body.classList.remove('mobile-view', 'desktop-view');
        } else {
            document.body.classList.add('desktop-view');
            document.body.classList.remove('mobile-view', 'tablet-view');
        }
    }

    // Utility methods
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} modern-alert`;
        notification.innerHTML = `
            <div class="alert-content">
                <i class="fas fa-${this.getNotificationIcon(type)} alert-icon"></i>
                <span class="alert-message">${message}</span>
            </div>
            <button type="button" class="btn-close modern-close" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            this.dismissNotification(notification);
        }, duration);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // API helper methods
    async apiRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, finalOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Request failed');
            }
            
            return data;
        } catch (error) {
            this.showNotification(error.message, 'error');
            throw error;
        }
    }
}

// Initialize Modern CRM when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.modernCRM = new ModernCRM();
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .modern-tooltip .tooltip-inner {
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: var(--text-primary);
    }
    
    .modern-tooltip .tooltip-arrow::before {
        border-top-color: var(--bg-glass);
    }
    
    .loading {
        position: relative;
        pointer-events: none;
    }
    
    .loading::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 20px;
        height: 20px;
        margin: -10px 0 0 -10px;
        border: 2px solid transparent;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .mobile-view .glass-card {
        margin: 0.5rem;
        padding: 1rem;
    }
    
    .tablet-view .glass-card {
        margin: 0.75rem;
        padding: 1.5rem;
    }
    
    .desktop-view .glass-card {
        margin: 1rem;
        padding: 2rem;
    }
`;
document.head.appendChild(style); 
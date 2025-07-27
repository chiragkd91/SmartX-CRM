/**
 * Enhanced Touch Interface for Modern CRM
 * Provides smooth touch interactions and mobile-optimized experiences
 */

class TouchInterface {
    constructor() {
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.touchEndX = 0;
        this.touchEndY = 0;
        this.isScrolling = false;
        this.touchStartTime = 0;
        this.longPressTimer = null;
        this.longPressDelay = 500;
        
        this.init();
    }

    init() {
        this.setupTouchEvents();
        this.setupSwipeGestures();
        this.setupLongPress();
        this.setupPullToRefresh();
        this.setupTouchFeedback();
        this.setupMobileOptimizations();
    }

    setupTouchEvents() {
        // Prevent zoom on double tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (event) => {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);

        // Prevent zoom on input focus (iOS)
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                if (this.isMobile()) {
                    input.style.fontSize = '16px';
                }
            });
        });

        // Add touch feedback to interactive elements
        const touchElements = document.querySelectorAll('.btn-modern, .btn-neon, .card, .nav-link, .quick-action-item');
        touchElements.forEach(element => {
            element.addEventListener('touchstart', (e) => {
                this.addTouchFeedback(e.target);
            });

            element.addEventListener('touchend', (e) => {
                this.removeTouchFeedback(e.target);
            });

            element.addEventListener('touchcancel', (e) => {
                this.removeTouchFeedback(e.target);
            });
        });
    }

    setupSwipeGestures() {
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.changedTouches[0].screenX;
            this.touchStartY = e.changedTouches[0].screenY;
            this.touchStartTime = Date.now();
            this.isScrolling = false;
        });

        document.addEventListener('touchmove', (e) => {
            if (!this.touchStartX || !this.touchStartY) return;

            this.touchEndX = e.changedTouches[0].screenX;
            this.touchEndY = e.changedTouches[0].screenY;

            const diffX = this.touchStartX - this.touchEndX;
            const diffY = this.touchStartY - this.touchEndY;

            // Detect if user is scrolling
            if (Math.abs(diffY) > Math.abs(diffX)) {
                this.isScrolling = true;
            }
        });

        document.addEventListener('touchend', (e) => {
            if (!this.touchStartX || !this.touchStartY) return;

            const diffX = this.touchStartX - this.touchEndX;
            const diffY = this.touchStartY - this.touchEndY;
            const touchDuration = Date.now() - this.touchStartTime;

            // Only handle swipe if not scrolling and touch duration is short
            if (!this.isScrolling && touchDuration < 300) {
                if (Math.abs(diffX) > Math.abs(diffY)) {
                    // Horizontal swipe
                    if (diffX > 50) {
                        this.handleSwipeLeft(e);
                    } else if (diffX < -50) {
                        this.handleSwipeRight(e);
                    }
                } else {
                    // Vertical swipe
                    if (diffY > 50) {
                        this.handleSwipeUp(e);
                    } else if (diffY < -50) {
                        this.handleSwipeDown(e);
                    }
                }
            }

            // Reset values
            this.touchStartX = 0;
            this.touchStartY = 0;
            this.touchEndX = 0;
            this.touchEndY = 0;
        });
    }

    handleSwipeLeft(e) {
        // Handle left swipe - could be used for navigation
        const target = e.target.closest('[data-swipe-left]');
        if (target) {
            const action = target.dataset.swipeLeft;
            this.executeSwipeAction(action, target);
        }
    }

    handleSwipeRight(e) {
        // Handle right swipe - could be used for navigation
        const target = e.target.closest('[data-swipe-right]');
        if (target) {
            const action = target.dataset.swipeRight;
            this.executeSwipeAction(action, target);
        }
    }

    handleSwipeUp(e) {
        // Handle up swipe - could be used for actions
        const target = e.target.closest('[data-swipe-up]');
        if (target) {
            const action = target.dataset.swipeUp;
            this.executeSwipeAction(action, target);
        }
    }

    handleSwipeDown(e) {
        // Handle down swipe - could be used for refresh
        const target = e.target.closest('[data-swipe-down]');
        if (target) {
            const action = target.dataset.swipeDown;
            this.executeSwipeAction(action, target);
        }
    }

    executeSwipeAction(action, element) {
        switch (action) {
            case 'delete':
                this.confirmDelete(element);
                break;
            case 'edit':
                this.editItem(element);
                break;
            case 'refresh':
                this.refreshContent();
                break;
            case 'navigate':
                const url = element.dataset.navigateUrl;
                if (url) window.location.href = url;
                break;
            default:
                // Custom action
                if (typeof window[action] === 'function') {
                    window[action](element);
                }
        }
    }

    setupLongPress() {
        document.addEventListener('touchstart', (e) => {
            const element = e.target.closest('[data-long-press]');
            if (element) {
                this.longPressTimer = setTimeout(() => {
                    this.handleLongPress(element, e);
                }, this.longPressDelay);
            }
        });

        document.addEventListener('touchend', () => {
            if (this.longPressTimer) {
                clearTimeout(this.longPressTimer);
                this.longPressTimer = null;
            }
        });

        document.addEventListener('touchmove', () => {
            if (this.longPressTimer) {
                clearTimeout(this.longPressTimer);
                this.longPressTimer = null;
            }
        });
    }

    handleLongPress(element, event) {
        event.preventDefault();
        
        const action = element.dataset.longPress;
        switch (action) {
            case 'context-menu':
                this.showContextMenu(element, event);
                break;
            case 'select':
                this.selectItem(element);
                break;
            case 'preview':
                this.previewItem(element);
                break;
            default:
                // Custom long press action
                if (typeof window[action] === 'function') {
                    window[action](element, event);
                }
        }
    }

    setupPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        let isPulling = false;
        let refreshElement = null;

        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                isPulling = true;
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (!isPulling) return;

            currentY = e.touches[0].clientY;
            pullDistance = currentY - startY;

            if (pullDistance > 0 && window.scrollY === 0) {
                e.preventDefault();
                
                if (!refreshElement) {
                    refreshElement = this.createRefreshIndicator();
                }
                
                this.updateRefreshIndicator(refreshElement, pullDistance);
            }
        });

        document.addEventListener('touchend', () => {
            if (isPulling && pullDistance > 100) {
                this.triggerRefresh();
            }
            
            if (refreshElement) {
                this.hideRefreshIndicator(refreshElement);
                refreshElement = null;
            }
            
            isPulling = false;
            pullDistance = 0;
        });
    }

    createRefreshIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'pull-refresh-indicator';
        indicator.innerHTML = `
            <div class="refresh-content">
                <i class="fas fa-spinner fa-spin"></i>
                <span>Pull to refresh</span>
            </div>
        `;
        document.body.appendChild(indicator);
        return indicator;
    }

    updateRefreshIndicator(indicator, distance) {
        const maxDistance = 150;
        const progress = Math.min(distance / maxDistance, 1);
        
        indicator.style.transform = `translateY(${Math.min(distance, maxDistance)}px)`;
        indicator.style.opacity = progress;
        
        const text = indicator.querySelector('span');
        if (distance > 100) {
            text.textContent = 'Release to refresh';
        } else {
            text.textContent = 'Pull to refresh';
        }
    }

    hideRefreshIndicator(indicator) {
        indicator.style.transform = 'translateY(-100%)';
        indicator.style.opacity = '0';
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        }, 300);
    }

    triggerRefresh() {
        // Trigger page refresh or data reload
        if (typeof window.modernCRM !== 'undefined') {
            window.modernCRM.showNotification('Refreshing...', 'info');
        }
        
        setTimeout(() => {
            window.location.reload();
        }, 500);
    }

    setupTouchFeedback() {
        // Add haptic feedback for touch devices
        if ('vibrate' in navigator) {
            const touchElements = document.querySelectorAll('.btn-modern, .btn-neon, .nav-link');
            touchElements.forEach(element => {
                element.addEventListener('touchstart', () => {
                    navigator.vibrate(10);
                });
            });
        }

        // Add visual feedback
        const style = document.createElement('style');
        style.textContent = `
            .touch-feedback {
                transform: scale(0.95);
                transition: transform 0.1s ease;
            }
            
            .pull-refresh-indicator {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                height: 60px;
                background: var(--bg-glass);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                transform: translateY(-100%);
                transition: all 0.3s ease;
            }
            
            .refresh-content {
                display: flex;
                align-items: center;
                gap: 10px;
                color: var(--text-primary);
            }
            
            .context-menu {
                position: fixed;
                background: var(--bg-glass);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: var(--radius-md);
                padding: 0.5rem;
                box-shadow: var(--shadow-glass);
                z-index: 10000;
                min-width: 150px;
            }
            
            .context-menu-item {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 0.75rem 1rem;
                color: var(--text-secondary);
                text-decoration: none;
                border-radius: var(--radius-sm);
                transition: all var(--transition-normal);
                cursor: pointer;
            }
            
            .context-menu-item:hover {
                background: rgba(255, 255, 255, 0.1);
                color: var(--text-primary);
            }
        `;
        document.head.appendChild(style);
    }

    setupMobileOptimizations() {
        // Optimize for mobile devices
        if (this.isMobile()) {
            this.optimizeMobileLayout();
            this.setupMobileNavigation();
            this.setupMobileForms();
        }
    }

    optimizeMobileLayout() {
        // Add mobile-specific classes
        document.body.classList.add('mobile-device');
        
        // Optimize viewport
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
        }
        
        // Add mobile-specific styles
        const mobileStyle = document.createElement('style');
        mobileStyle.textContent = `
            .mobile-device .glass-card {
                margin: 0.5rem;
                padding: 1rem;
            }
            
            .mobile-device .btn-modern,
            .mobile-device .btn-neon {
                min-height: 44px;
                padding: 0.75rem 1rem;
            }
            
            .mobile-device .nav-link {
                min-height: 44px;
                padding: 0.75rem 1rem;
            }
            
            .mobile-device .form-control {
                font-size: 16px;
                padding: 0.75rem;
            }
        `;
        document.head.appendChild(mobileStyle);
    }

    setupMobileNavigation() {
        // Enhance mobile navigation
        const navbar = document.querySelector('.modern-navbar');
        if (navbar) {
            // Add swipe to open/close mobile menu
            let startX = 0;
            let currentX = 0;
            
            navbar.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
            });
            
            navbar.addEventListener('touchmove', (e) => {
                currentX = e.touches[0].clientX;
            });
            
            navbar.addEventListener('touchend', () => {
                const diffX = currentX - startX;
                if (Math.abs(diffX) > 50) {
                    const navbarCollapse = navbar.querySelector('.navbar-collapse');
                    if (navbarCollapse) {
                        if (diffX > 0) {
                            // Swipe right - open menu
                            navbarCollapse.classList.add('show');
                        } else {
                            // Swipe left - close menu
                            navbarCollapse.classList.remove('show');
                        }
                    }
                }
            });
        }
    }

    setupMobileForms() {
        // Optimize forms for mobile
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            // Add mobile-friendly input types
            const inputs = form.querySelectorAll('input');
            inputs.forEach(input => {
                if (input.type === 'text' && input.name.includes('email')) {
                    input.type = 'email';
                } else if (input.type === 'text' && input.name.includes('phone')) {
                    input.type = 'tel';
                } else if (input.type === 'text' && input.name.includes('url')) {
                    input.type = 'url';
                }
            });
        });
    }

    addTouchFeedback(element) {
        element.classList.add('touch-feedback');
    }

    removeTouchFeedback(element) {
        element.classList.remove('touch-feedback');
    }

    showContextMenu(element, event) {
        // Remove existing context menu
        const existingMenu = document.querySelector('.context-menu');
        if (existingMenu) {
            existingMenu.remove();
        }

        // Create context menu
        const menu = document.createElement('div');
        menu.className = 'context-menu';
        
        const actions = element.dataset.contextActions ? JSON.parse(element.dataset.contextActions) : [];
        
        actions.forEach(action => {
            const item = document.createElement('div');
            item.className = 'context-menu-item';
            item.innerHTML = `<i class="fas fa-${action.icon}"></i><span>${action.label}</span>`;
            item.addEventListener('click', () => {
                if (typeof window[action.handler] === 'function') {
                    window[action.handler](element);
                }
                menu.remove();
            });
            menu.appendChild(item);
        });

        // Position menu
        menu.style.left = `${event.touches[0].clientX}px`;
        menu.style.top = `${event.touches[0].clientY}px`;
        
        document.body.appendChild(menu);

        // Close menu when clicking outside
        setTimeout(() => {
            document.addEventListener('touchstart', closeMenu, { once: true });
        }, 100);

        function closeMenu() {
            if (menu.parentNode) {
                menu.parentNode.removeChild(menu);
            }
        }
    }

    confirmDelete(element) {
        if (confirm('Are you sure you want to delete this item?')) {
            if (typeof window.deleteItem === 'function') {
                window.deleteItem(element);
            }
        }
    }

    editItem(element) {
        const editUrl = element.dataset.editUrl;
        if (editUrl) {
            window.location.href = editUrl;
        }
    }

    selectItem(element) {
        element.classList.toggle('selected');
        if (typeof window.onItemSelect === 'function') {
            window.onItemSelect(element);
        }
    }

    previewItem(element) {
        const previewUrl = element.dataset.previewUrl;
        if (previewUrl) {
            window.open(previewUrl, '_blank');
        }
    }

    refreshContent() {
        if (typeof window.refreshContent === 'function') {
            window.refreshContent();
        } else {
            window.location.reload();
        }
    }

    isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }

    isTablet() {
        return window.innerWidth > 768 && window.innerWidth <= 1024;
    }

    isTouchDevice() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    }
}

// Initialize Touch Interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.touchInterface = new TouchInterface();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TouchInterface;
} 
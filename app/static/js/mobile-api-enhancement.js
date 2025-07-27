/**
 * Mobile & API Enhancement Features for CRM System
 * Includes: Mobile-responsive optimization, Touch-friendly interface,
 * Mobile-specific features, Offline functionality, Push notifications,
 * API documentation portal, Developer portal, SDK development tools,
 * Native mobile app, Cross-platform support
 */

class MobileAPIEnhancement {
    constructor() {
        this.isMobile = this.detectMobile();
        this.isOnline = navigator.onLine;
        this.pushSubscription = null;
        this.offlineData = new Map();
        this.apiDocs = new Map();
        this.sdkTools = new Map();
        
        this.init();
    }

    init() {
        this.initMobileOptimization();
        this.initTouchInterface();
        this.initMobileFeatures();
        this.initOfflineFunctionality();
        this.initPushNotifications();
        this.initAPIDocumentation();
        this.initDeveloperPortal();
        this.initSDKDevelopment();
        this.initNativeMobileApp();
        this.initCrossPlatformSupport();
    }

    // ==================== MOBILE RESPONSIVE OPTIMIZATION ====================
    initMobileOptimization() {
        this.optimizeForMobile();
        this.setupResponsiveBreakpoints();
        this.optimizeImages();
        this.optimizeFonts();
    }

    optimizeForMobile() {
        if (this.isMobile) {
            this.addMobileMetaTags();
            this.optimizeViewport();
            this.enableTouchOptimizations();
            this.optimizePerformance();
        }
    }

    addMobileMetaTags() {
        const metaTags = [
            { name: 'viewport', content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no' },
            { name: 'mobile-web-app-capable', content: 'yes' },
            { name: 'apple-mobile-web-app-capable', content: 'yes' },
            { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
            { name: 'theme-color', content: '#007bff' }
        ];

        metaTags.forEach(tag => {
            if (!document.querySelector(`meta[name="${tag.name}"]`)) {
                const meta = document.createElement('meta');
                meta.name = tag.name;
                meta.content = tag.content;
                document.head.appendChild(meta);
            }
        });
    }

    optimizeViewport() {
        // Ensure proper viewport scaling
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
        }
    }

    enableTouchOptimizations() {
        // Add touch-specific CSS classes
        document.body.classList.add('touch-device');
        
        // Optimize touch targets
        const touchTargets = document.querySelectorAll('button, a, input, select, textarea');
        touchTargets.forEach(target => {
            if (target.offsetHeight < 44 || target.offsetWidth < 44) {
                target.classList.add('touch-target');
            }
        });
    }

    optimizePerformance() {
        // Lazy load images
        this.setupLazyLoading();
        
        // Optimize animations for mobile
        this.optimizeAnimations();
        
        // Reduce network requests
        this.optimizeNetworkRequests();
    }

    setupLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    optimizeAnimations() {
        // Reduce motion for users who prefer it
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.body.classList.add('reduce-motion');
        }
    }

    optimizeNetworkRequests() {
        // Implement request batching
        this.setupRequestBatching();
        
        // Cache frequently accessed data
        this.setupDataCaching();
    }

    setupResponsiveBreakpoints() {
        const breakpoints = {
            mobile: 768,
            tablet: 1024,
            desktop: 1200
        };

        // Add responsive classes to body
        const updateResponsiveClass = () => {
            const width = window.innerWidth;
            document.body.className = document.body.className.replace(/responsive-\w+/g, '');
            
            if (width < breakpoints.mobile) {
                document.body.classList.add('responsive-mobile');
            } else if (width < breakpoints.tablet) {
                document.body.classList.add('responsive-tablet');
            } else {
                document.body.classList.add('responsive-desktop');
            }
        };

        updateResponsiveClass();
        window.addEventListener('resize', updateResponsiveClass);
    }

    optimizeImages() {
        // Implement responsive images
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (!img.srcset) {
                this.generateSrcSet(img);
            }
        });
    }

    generateSrcSet(img) {
        const src = img.src;
        const baseName = src.substring(0, src.lastIndexOf('.'));
        const extension = src.substring(src.lastIndexOf('.'));
        
        img.srcset = `
            ${baseName}-320w${extension} 320w,
            ${baseName}-480w${extension} 480w,
            ${baseName}-768w${extension} 768w,
            ${baseName}-1024w${extension} 1024w
        `;
        img.sizes = '(max-width: 320px) 280px, (max-width: 480px) 440px, (max-width: 768px) 720px, 1024px';
    }

    optimizeFonts() {
        // Preload critical fonts
        const criticalFonts = [
            '/static/fonts/roboto-regular.woff2',
            '/static/fonts/roboto-bold.woff2'
        ];

        criticalFonts.forEach(font => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = font;
            link.as = 'font';
            link.type = 'font/woff2';
            link.crossOrigin = 'anonymous';
            document.head.appendChild(link);
        });
    }

    // ==================== TOUCH-FRIENDLY INTERFACE ====================
    initTouchInterface() {
        this.setupTouchGestures();
        this.optimizeTouchTargets();
        this.setupSwipeNavigation();
        this.implementPullToRefresh();
    }

    setupTouchGestures() {
        // Swipe gestures
        this.setupSwipeGestures();
        
        // Pinch to zoom
        this.setupPinchToZoom();
        
        // Long press actions
        this.setupLongPress();
    }

    setupSwipeGestures() {
        let startX, startY, endX, endY;
        const minSwipeDistance = 50;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    this.handleSwipeRight();
                } else {
                    this.handleSwipeLeft();
                }
            } else if (Math.abs(deltaY) > minSwipeDistance) {
                if (deltaY > 0) {
                    this.handleSwipeDown();
                } else {
                    this.handleSwipeUp();
                }
            }
        });
    }

    handleSwipeRight() {
        // Navigate back or open sidebar
        if (this.isMobile) {
            this.toggleSidebar();
        }
    }

    handleSwipeLeft() {
        // Close sidebar or navigate forward
        if (this.isMobile) {
            this.closeSidebar();
        }
    }

    handleSwipeDown() {
        // Pull to refresh
        this.triggerPullToRefresh();
    }

    handleSwipeUp() {
        // Scroll to top or show quick actions
        this.scrollToTop();
    }

    setupPinchToZoom() {
        let initialDistance = 0;
        let currentScale = 1;

        document.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                initialDistance = this.getDistance(e.touches[0], e.touches[1]);
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (e.touches.length === 2) {
                e.preventDefault();
                const currentDistance = this.getDistance(e.touches[0], e.touches[1]);
                const scale = currentDistance / initialDistance;
                
                if (scale > 0.5 && scale < 3) {
                    currentScale = scale;
                    this.applyZoom(currentScale);
                }
            }
        });
    }

    getDistance(touch1, touch2) {
        const dx = touch1.clientX - touch2.clientX;
        const dy = touch1.clientY - touch2.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    applyZoom(scale) {
        document.body.style.transform = `scale(${scale})`;
        document.body.style.transformOrigin = 'center top';
    }

    setupLongPress() {
        let pressTimer;
        const longPressDelay = 500;

        document.addEventListener('touchstart', (e) => {
            pressTimer = setTimeout(() => {
                this.handleLongPress(e);
            }, longPressDelay);
        });

        document.addEventListener('touchend', () => {
            clearTimeout(pressTimer);
        });

        document.addEventListener('touchmove', () => {
            clearTimeout(pressTimer);
        });
    }

    handleLongPress(e) {
        // Show context menu or additional options
        this.showContextMenu(e);
    }

    optimizeTouchTargets() {
        const touchTargets = document.querySelectorAll('button, a, input, select, textarea, .touch-target');
        touchTargets.forEach(target => {
            // Ensure minimum touch target size
            const rect = target.getBoundingClientRect();
            if (rect.height < 44 || rect.width < 44) {
                target.classList.add('touch-target');
            }
        });
    }

    setupSwipeNavigation() {
        // Implement swipe navigation for mobile
        if (this.isMobile) {
            this.setupTabSwipe();
            this.setupPageSwipe();
        }
    }

    setupTabSwipe() {
        const tabs = document.querySelectorAll('.nav-tabs, .tab-navigation');
        tabs.forEach(tabContainer => {
            let startX = 0;
            let currentTab = 0;
            const tabItems = tabContainer.querySelectorAll('.tab-item, .nav-item');
            
            tabContainer.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
            });

            tabContainer.addEventListener('touchend', (e) => {
                const endX = e.changedTouches[0].clientX;
                const deltaX = endX - startX;
                
                if (Math.abs(deltaX) > 50) {
                    if (deltaX > 0 && currentTab > 0) {
                        currentTab--;
                    } else if (deltaX < 0 && currentTab < tabItems.length - 1) {
                        currentTab++;
                    }
                    this.switchTab(tabItems[currentTab]);
                }
            });
        });
    }

    implementPullToRefresh() {
        let startY = 0;
        let pullDistance = 0;
        const pullThreshold = 80;

        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (window.scrollY === 0 && startY > 0) {
                pullDistance = e.touches[0].clientY - startY;
                
                if (pullDistance > 0) {
                    e.preventDefault();
                    this.showPullToRefreshIndicator(pullDistance);
                }
            }
        });

        document.addEventListener('touchend', () => {
            if (pullDistance > pullThreshold) {
                this.refreshContent();
            }
            this.hidePullToRefreshIndicator();
            startY = 0;
            pullDistance = 0;
        });
    }

    // ==================== MOBILE-SPECIFIC FEATURES ====================
    initMobileFeatures() {
        this.setupMobileNavigation();
        this.implementBottomSheet();
        this.setupFloatingActionButton();
        this.implementMobileSearch();
        this.setupMobileFilters();
    }

    setupMobileNavigation() {
        if (this.isMobile) {
            this.createMobileNav();
            this.setupBottomNavigation();
            this.implementDrawerNavigation();
        }
    }

    createMobileNav() {
        const mobileNav = document.createElement('nav');
        mobileNav.className = 'mobile-navigation';
        mobileNav.innerHTML = `
            <div class="mobile-nav-header">
                <button class="menu-toggle" onclick="mobileAPI.toggleMobileMenu()">
                    <i class="fas fa-bars"></i>
                </button>
                <h1 class="mobile-title">CRM System</h1>
                <button class="search-toggle" onclick="mobileAPI.toggleMobileSearch()">
                    <i class="fas fa-search"></i>
                </button>
            </div>
            <div class="mobile-nav-content">
                <div class="mobile-menu" id="mobile-menu">
                    <!-- Mobile menu items will be populated here -->
                </div>
            </div>
        `;
        
        document.body.insertBefore(mobileNav, document.body.firstChild);
        this.populateMobileMenu();
    }

    setupBottomNavigation() {
        const bottomNav = document.createElement('nav');
        bottomNav.className = 'bottom-navigation';
        bottomNav.innerHTML = `
            <div class="bottom-nav-item active" data-page="dashboard">
                <i class="fas fa-home"></i>
                <span>Dashboard</span>
            </div>
            <div class="bottom-nav-item" data-page="leads">
                <i class="fas fa-user-plus"></i>
                <span>Leads</span>
            </div>
            <div class="bottom-nav-item" data-page="contacts">
                <i class="fas fa-address-book"></i>
                <span>Contacts</span>
            </div>
            <div class="bottom-nav-item" data-page="opportunities">
                <i class="fas fa-chart-line"></i>
                <span>Sales</span>
            </div>
            <div class="bottom-nav-item" data-page="more">
                <i class="fas fa-ellipsis-h"></i>
                <span>More</span>
            </div>
        `;
        
        document.body.appendChild(bottomNav);
        this.setupBottomNavEvents();
    }

    implementBottomSheet() {
        this.createBottomSheet();
        this.setupBottomSheetTriggers();
    }

    createBottomSheet() {
        const bottomSheet = document.createElement('div');
        bottomSheet.className = 'bottom-sheet';
        bottomSheet.innerHTML = `
            <div class="bottom-sheet-handle"></div>
            <div class="bottom-sheet-content">
                <div class="bottom-sheet-header">
                    <h3>Quick Actions</h3>
                    <button class="close-sheet" onclick="mobileAPI.closeBottomSheet()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="bottom-sheet-body">
                    <!-- Bottom sheet content will be populated here -->
                </div>
            </div>
        `;
        
        document.body.appendChild(bottomSheet);
    }

    setupFloatingActionButton() {
        const fab = document.createElement('button');
        fab.className = 'floating-action-button';
        fab.innerHTML = '<i class="fas fa-plus"></i>';
        fab.onclick = () => this.showQuickActions();
        
        document.body.appendChild(fab);
    }

    implementMobileSearch() {
        this.createMobileSearch();
        this.setupSearchSuggestions();
    }

    createMobileSearch() {
        const mobileSearch = document.createElement('div');
        mobileSearch.className = 'mobile-search';
        mobileSearch.innerHTML = `
            <div class="search-header">
                <button class="search-back" onclick="mobileAPI.closeMobileSearch()">
                    <i class="fas fa-arrow-left"></i>
                </button>
                <div class="search-input-container">
                    <input type="text" class="search-input" placeholder="Search..." autocomplete="off">
                    <button class="search-clear" onclick="mobileAPI.clearSearch()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="search-results" id="mobile-search-results">
                <!-- Search results will be populated here -->
            </div>
        `;
        
        document.body.appendChild(mobileSearch);
        this.setupSearchEvents();
    }

    // ==================== OFFLINE FUNCTIONALITY ====================
    initOfflineFunctionality() {
        this.setupServiceWorker();
        this.implementOfflineStorage();
        this.setupSyncQueue();
        this.createOfflineUI();
    }

    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('Service Worker registered successfully');
                    this.serviceWorkerRegistration = registration;
                })
                .catch(error => {
                    console.error('Service Worker registration failed:', error);
                });
        }
    }

    implementOfflineStorage() {
        // Use IndexedDB for offline data storage
        this.setupIndexedDB();
        
        // Cache important resources
        this.setupResourceCaching();
        
        // Implement offline data sync
        this.setupDataSync();
    }

    setupIndexedDB() {
        const request = indexedDB.open('CRMOfflineDB', 1);
        
        request.onerror = () => {
            console.error('IndexedDB error:', request.error);
        };
        
        request.onsuccess = () => {
            this.db = request.result;
            console.log('IndexedDB opened successfully');
        };
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            
            // Create object stores for different data types
            if (!db.objectStoreNames.contains('leads')) {
                db.createObjectStore('leads', { keyPath: 'id' });
            }
            if (!db.objectStoreNames.contains('contacts')) {
                db.createObjectStore('contacts', { keyPath: 'id' });
            }
            if (!db.objectStoreNames.contains('opportunities')) {
                db.createObjectStore('opportunities', { keyPath: 'id' });
            }
            if (!db.objectStoreNames.contains('syncQueue')) {
                db.createObjectStore('syncQueue', { keyPath: 'id', autoIncrement: true });
            }
        };
    }

    setupSyncQueue() {
        // Queue operations when offline
        this.syncQueue = [];
        
        // Process queue when back online
        window.addEventListener('online', () => {
            this.processSyncQueue();
        });
    }

    createOfflineUI() {
        const offlineIndicator = document.createElement('div');
        offlineIndicator.className = 'offline-indicator';
        offlineIndicator.innerHTML = `
            <div class="offline-content">
                <i class="fas fa-wifi-slash"></i>
                <span>You're offline. Some features may be limited.</span>
            </div>
        `;
        
        document.body.appendChild(offlineIndicator);
        
        // Show/hide based on connection status
        window.addEventListener('online', () => {
            offlineIndicator.classList.remove('show');
        });
        
        window.addEventListener('offline', () => {
            offlineIndicator.classList.add('show');
        });
    }

    // ==================== PUSH NOTIFICATIONS ====================
    initPushNotifications() {
        this.setupPushNotifications();
        this.requestNotificationPermission();
        this.setupNotificationPreferences();
    }

    setupPushNotifications() {
        if ('serviceWorker' in navigator && 'PushManager' in window) {
            this.setupPushManager();
        }
    }

    async requestNotificationPermission() {
        if ('Notification' in window) {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.subscribeToPushNotifications();
            }
        }
    }

    async subscribeToPushNotifications() {
        try {
            const registration = await navigator.serviceWorker.ready;
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: this.urlBase64ToUint8Array('YOUR_VAPID_PUBLIC_KEY')
            });
            
            this.pushSubscription = subscription;
            this.sendSubscriptionToServer(subscription);
        } catch (error) {
            console.error('Failed to subscribe to push notifications:', error);
        }
    }

    setupNotificationPreferences() {
        this.createNotificationSettings();
    }

    createNotificationSettings() {
        const settings = {
            newLeads: true,
            leadUpdates: true,
            opportunityUpdates: true,
            systemAlerts: true,
            marketingCampaigns: false
        };
        
        localStorage.setItem('notificationPreferences', JSON.stringify(settings));
    }

    // ==================== API DOCUMENTATION PORTAL ====================
    initAPIDocumentation() {
        this.createAPIDocumentationPortal();
        this.loadAPIDocumentation();
        this.setupInteractiveExamples();
    }

    createAPIDocumentationPortal() {
        const container = document.getElementById('api-documentation');
        if (!container) return;

        container.innerHTML = `
            <div class="api-documentation-portal">
                <div class="api-header">
                    <h3>API Documentation</h3>
                    <div class="api-controls">
                        <button class="btn btn-primary" onclick="mobileAPI.downloadAPIDocs()">
                            <i class="fas fa-download"></i> Download
                        </button>
                        <button class="btn btn-secondary" onclick="mobileAPI.testAPI()">
                            <i class="fas fa-play"></i> Test API
                        </button>
                    </div>
                </div>
                
                <div class="api-navigation">
                    <div class="api-sidebar">
                        <div class="api-section">
                            <h4>Authentication</h4>
                            <ul>
                                <li><a href="#auth-overview">Overview</a></li>
                                <li><a href="#auth-tokens">Tokens</a></li>
                                <li><a href="#auth-oauth">OAuth 2.0</a></li>
                            </ul>
                        </div>
                        
                        <div class="api-section">
                            <h4>Endpoints</h4>
                            <ul>
                                <li><a href="#leads-api">Leads API</a></li>
                                <li><a href="#contacts-api">Contacts API</a></li>
                                <li><a href="#opportunities-api">Opportunities API</a></li>
                                <li><a href="#accounts-api">Accounts API</a></li>
                            </ul>
                        </div>
                        
                        <div class="api-section">
                            <h4>Examples</h4>
                            <ul>
                                <li><a href="#curl-examples">cURL Examples</a></li>
                                <li><a href="#javascript-examples">JavaScript</a></li>
                                <li><a href="#python-examples">Python</a></li>
                                <li><a href="#php-examples">PHP</a></li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="api-content">
                        <div class="api-endpoint">
                            <h4>GET /api/v1/leads</h4>
                            <p>Retrieve a list of leads with optional filtering and pagination.</p>
                            
                            <div class="endpoint-details">
                                <div class="parameter-section">
                                    <h5>Query Parameters</h5>
                                    <table class="parameter-table">
                                        <thead>
                                            <tr>
                                                <th>Parameter</th>
                                                <th>Type</th>
                                                <th>Required</th>
                                                <th>Description</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>page</td>
                                                <td>integer</td>
                                                <td>No</td>
                                                <td>Page number for pagination</td>
                                            </tr>
                                            <tr>
                                                <td>limit</td>
                                                <td>integer</td>
                                                <td>No</td>
                                                <td>Number of items per page</td>
                                            </tr>
                                            <tr>
                                                <td>status</td>
                                                <td>string</td>
                                                <td>No</td>
                                                <td>Filter by lead status</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                
                                <div class="response-section">
                                    <h5>Response Example</h5>
                                    <pre><code class="json">{
  "success": true,
  "data": {
    "leads": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "status": "new",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 100,
      "pages": 10
    }
  }
}</code></pre>
                                </div>
                                
                                <div class="try-it-section">
                                    <h5>Try it out</h5>
                                    <div class="api-tester">
                                        <div class="tester-url">
                                            <span class="method get">GET</span>
                                            <input type="text" value="/api/v1/leads" readonly>
                                        </div>
                                        <div class="tester-params">
                                            <label>Page: <input type="number" value="1" min="1"></label>
                                            <label>Limit: <input type="number" value="10" min="1" max="100"></label>
                                            <label>Status: <select><option value="">All</option><option value="new">New</option><option value="qualified">Qualified</option></select></label>
                                        </div>
                                        <button class="btn btn-primary" onclick="mobileAPI.testEndpoint()">
                                            <i class="fas fa-play"></i> Send Request
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // ==================== DEVELOPER PORTAL ====================
    initDeveloperPortal() {
        this.createDeveloperPortal();
        this.setupDeveloperTools();
        this.implementAPITesting();
    }

    createDeveloperPortal() {
        const container = document.getElementById('developer-portal');
        if (!container) return;

        container.innerHTML = `
            <div class="developer-portal">
                <div class="portal-header">
                    <h3>Developer Portal</h3>
                    <div class="portal-controls">
                        <button class="btn btn-primary" onclick="mobileAPI.createAPIKey()">
                            <i class="fas fa-key"></i> Create API Key
                        </button>
                        <button class="btn btn-secondary" onclick="mobileAPI.viewUsage()">
                            <i class="fas fa-chart-bar"></i> Usage Stats
                        </button>
                    </div>
                </div>
                
                <div class="portal-dashboard">
                    <div class="dashboard-card">
                        <h4>API Usage</h4>
                        <div class="usage-stats">
                            <div class="stat-item">
                                <span class="stat-value" id="total-requests">1,234</span>
                                <span class="stat-label">Total Requests</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-value" id="success-rate">98.5%</span>
                                <span class="stat-label">Success Rate</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-value" id="avg-response">245ms</span>
                                <span class="stat-label">Avg Response</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="dashboard-card">
                        <h4>API Keys</h4>
                        <div class="api-keys-list" id="api-keys-list">
                            <!-- API keys will be populated here -->
                        </div>
                        <button class="btn btn-primary" onclick="mobileAPI.generateNewKey()">
                            Generate New Key
                        </button>
                    </div>
                    
                    <div class="dashboard-card">
                        <h4>Rate Limits</h4>
                        <div class="rate-limits">
                            <div class="limit-item">
                                <span class="limit-name">Requests per minute</span>
                                <span class="limit-value">1000</span>
                            </div>
                            <div class="limit-item">
                                <span class="limit-name">Requests per hour</span>
                                <span class="limit-value">50,000</span>
                            </div>
                            <div class="limit-item">
                                <span class="limit-name">Requests per day</span>
                                <span class="limit-value">1,000,000</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="webhook-configuration">
                    <h4>Webhook Configuration</h4>
                    <div class="webhook-form">
                        <div class="form-group">
                            <label>Webhook URL</label>
                            <input type="url" id="webhook-url" placeholder="https://your-domain.com/webhook">
                        </div>
                        <div class="form-group">
                            <label>Events</label>
                            <div class="event-checkboxes">
                                <label><input type="checkbox" value="lead.created"> Lead Created</label>
                                <label><input type="checkbox" value="lead.updated"> Lead Updated</label>
                                <label><input type="checkbox" value="contact.created"> Contact Created</label>
                                <label><input type="checkbox" value="opportunity.created"> Opportunity Created</label>
                            </div>
                        </div>
                        <button class="btn btn-primary" onclick="mobileAPI.saveWebhook()">
                            Save Webhook
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.loadAPIKeys();
    }

    // ==================== SDK DEVELOPMENT TOOLS ====================
    initSDKDevelopment() {
        this.createSDKDevelopmentTools();
        this.setupCodeGenerator();
        this.implementSDKTesting();
    }

    createSDKDevelopmentTools() {
        const container = document.getElementById('sdk-development');
        if (!container) return;

        container.innerHTML = `
            <div class="sdk-development-tools">
                <div class="sdk-header">
                    <h3>SDK Development Tools</h3>
                    <div class="sdk-controls">
                        <button class="btn btn-primary" onclick="mobileAPI.downloadSDK()">
                            <i class="fas fa-download"></i> Download SDK
                        </button>
                        <button class="btn btn-secondary" onclick="mobileAPI.viewSDKDocs()">
                            <i class="fas fa-book"></i> SDK Docs
                        </button>
                    </div>
                </div>
                
                <div class="sdk-languages">
                    <div class="language-card">
                        <h4>JavaScript SDK</h4>
                        <p>Official JavaScript SDK for browser and Node.js environments</p>
                        <div class="sdk-features">
                            <span class="feature">TypeScript Support</span>
                            <span class="feature">Promise-based</span>
                            <span class="feature">Browser Compatible</span>
                        </div>
                        <button class="btn btn-primary" onclick="mobileAPI.downloadJavaScriptSDK()">
                            Download JavaScript SDK
                        </button>
                    </div>
                    
                    <div class="language-card">
                        <h4>Python SDK</h4>
                        <p>Python SDK for server-side integration and automation</p>
                        <div class="sdk-features">
                            <span class="feature">Async Support</span>
                            <span class="feature">Type Hints</span>
                            <span class="feature">Pandas Integration</span>
                        </div>
                        <button class="btn btn-primary" onclick="mobileAPI.downloadPythonSDK()">
                            Download Python SDK
                        </button>
                    </div>
                    
                    <div class="language-card">
                        <h4>PHP SDK</h4>
                        <p>PHP SDK for web applications and server-side processing</p>
                        <div class="sdk-features">
                            <span class="feature">Composer Package</span>
                            <span class="feature">PSR Standards</span>
                            <span class="feature">Laravel Integration</span>
                        </div>
                        <button class="btn btn-primary" onclick="mobileAPI.downloadPHPSDK()">
                            Download PHP SDK
                        </button>
                    </div>
                </div>
                
                <div class="code-generator">
                    <h4>Code Generator</h4>
                    <div class="generator-form">
                        <div class="form-group">
                            <label>Programming Language</label>
                            <select id="code-language">
                                <option value="javascript">JavaScript</option>
                                <option value="python">Python</option>
                                <option value="php">PHP</option>
                                <option value="java">Java</option>
                                <option value="csharp">C#</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>API Endpoint</label>
                            <select id="api-endpoint">
                                <option value="leads">Leads API</option>
                                <option value="contacts">Contacts API</option>
                                <option value="opportunities">Opportunities API</option>
                                <option value="accounts">Accounts API</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Operation</label>
                            <select id="api-operation">
                                <option value="get">GET (Retrieve)</option>
                                <option value="post">POST (Create)</option>
                                <option value="put">PUT (Update)</option>
                                <option value="delete">DELETE (Remove)</option>
                            </select>
                        </div>
                        <button class="btn btn-primary" onclick="mobileAPI.generateCode()">
                            Generate Code
                        </button>
                    </div>
                    
                    <div class="generated-code" id="generated-code">
                        <!-- Generated code will be displayed here -->
                    </div>
                </div>
            </div>
        `;
    }

    // ==================== NATIVE MOBILE APP ====================
    initNativeMobileApp() {
        this.setupPWA();
        this.implementAppManifest();
        this.setupAppInstallation();
    }

    setupPWA() {
        // Progressive Web App setup
        this.createAppManifest();
        this.setupAppShell();
        this.implementOfflineCapabilities();
    }

    createAppManifest() {
        const manifest = {
            name: "CRM System",
            short_name: "CRM",
            description: "Complete CRM system for managing leads, contacts, and opportunities",
            start_url: "/",
            display: "standalone",
            background_color: "#ffffff",
            theme_color: "#007bff",
            icons: [
                {
                    src: "/static/icons/icon-192x192.png",
                    sizes: "192x192",
                    type: "image/png"
                },
                {
                    src: "/static/icons/icon-512x512.png",
                    sizes: "512x512",
                    type: "image/png"
                }
            ]
        };

        const manifestBlob = new Blob([JSON.stringify(manifest)], { type: 'application/json' });
        const manifestUrl = URL.createObjectURL(manifestBlob);

        const link = document.createElement('link');
        link.rel = 'manifest';
        link.href = manifestUrl;
        document.head.appendChild(link);
    }

    setupAppInstallation() {
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            this.showInstallPrompt();
        });
        
        window.addEventListener('appinstalled', () => {
            this.hideInstallPrompt();
            console.log('App installed successfully');
        });
    }

    showInstallPrompt() {
        const installPrompt = document.createElement('div');
        installPrompt.className = 'install-prompt';
        installPrompt.innerHTML = `
            <div class="install-content">
                <div class="install-icon">
                    <i class="fas fa-download"></i>
                </div>
                <div class="install-text">
                    <h4>Install CRM App</h4>
                    <p>Add this app to your home screen for quick access</p>
                </div>
                <div class="install-actions">
                    <button class="btn btn-primary" onclick="mobileAPI.installApp()">
                        Install
                    </button>
                    <button class="btn btn-secondary" onclick="mobileAPI.dismissInstallPrompt()">
                        Not Now
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(installPrompt);
    }

    // ==================== CROSS-PLATFORM SUPPORT ====================
    initCrossPlatformSupport() {
        this.setupPlatformDetection();
        this.implementPlatformSpecificFeatures();
        this.setupResponsiveDesign();
    }

    setupPlatformDetection() {
        this.platform = this.detectPlatform();
        this.applyPlatformStyles();
    }

    detectPlatform() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        if (/iphone|ipad|ipod/.test(userAgent)) {
            return 'ios';
        } else if (/android/.test(userAgent)) {
            return 'android';
        } else if (/windows/.test(userAgent)) {
            return 'windows';
        } else if (/macintosh|mac os x/.test(userAgent)) {
            return 'macos';
        } else if (/linux/.test(userAgent)) {
            return 'linux';
        } else {
            return 'web';
        }
    }

    applyPlatformStyles() {
        document.body.classList.add(`platform-${this.platform}`);
        
        // Apply platform-specific styles
        if (this.platform === 'ios') {
            this.applyIOSStyles();
        } else if (this.platform === 'android') {
            this.applyAndroidStyles();
        }
    }

    // ==================== UTILITY METHODS ====================
    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }

    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    showNotification(message, type = 'info') {
        if (window.enhancedUX) {
            window.enhancedUX.showNotification(message, type);
        }
    }

    // Placeholder methods for actual implementation
    toggleMobileMenu() {
        const menu = document.getElementById('mobile-menu');
        menu.classList.toggle('active');
    }

    toggleMobileSearch() {
        const search = document.querySelector('.mobile-search');
        search.classList.toggle('active');
    }

    closeMobileSearch() {
        const search = document.querySelector('.mobile-search');
        search.classList.remove('active');
    }

    clearSearch() {
        const searchInput = document.querySelector('.search-input');
        searchInput.value = '';
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('active');
    }

    closeSidebar() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.remove('active');
    }

    triggerPullToRefresh() {
        this.showNotification('Refreshing...', 'info');
        setTimeout(() => {
            location.reload();
        }, 1000);
    }

    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    showContextMenu(e) {
        // Implementation for context menu
    }

    switchTab(tabElement) {
        // Implementation for tab switching
    }

    showPullToRefreshIndicator(distance) {
        // Implementation for pull to refresh indicator
    }

    hidePullToRefreshIndicator() {
        // Implementation for hiding pull to refresh indicator
    }

    refreshContent() {
        // Implementation for content refresh
    }

    populateMobileMenu() {
        // Implementation for populating mobile menu
    }

    setupBottomNavEvents() {
        // Implementation for bottom navigation events
    }

    setupBottomSheetTriggers() {
        // Implementation for bottom sheet triggers
    }

    closeBottomSheet() {
        // Implementation for closing bottom sheet
    }

    showQuickActions() {
        // Implementation for showing quick actions
    }

    setupSearchEvents() {
        // Implementation for search events
    }

    setupSearchSuggestions() {
        // Implementation for search suggestions
    }

    setupResourceCaching() {
        // Implementation for resource caching
    }

    setupDataSync() {
        // Implementation for data sync
    }

    processSyncQueue() {
        // Implementation for processing sync queue
    }

    setupPushManager() {
        // Implementation for push manager
    }

    sendSubscriptionToServer(subscription) {
        // Implementation for sending subscription to server
    }

    loadAPIDocumentation() {
        // Implementation for loading API documentation
    }

    setupInteractiveExamples() {
        // Implementation for interactive examples
    }

    downloadAPIDocs() {
        // Implementation for downloading API docs
    }

    testAPI() {
        // Implementation for testing API
    }

    testEndpoint() {
        // Implementation for testing endpoint
    }

    setupDeveloperTools() {
        // Implementation for developer tools
    }

    implementAPITesting() {
        // Implementation for API testing
    }

    createAPIKey() {
        // Implementation for creating API key
    }

    viewUsage() {
        // Implementation for viewing usage
    }

    loadAPIKeys() {
        // Implementation for loading API keys
    }

    generateNewKey() {
        // Implementation for generating new key
    }

    saveWebhook() {
        // Implementation for saving webhook
    }

    setupCodeGenerator() {
        // Implementation for code generator
    }

    implementSDKTesting() {
        // Implementation for SDK testing
    }

    downloadSDK() {
        // Implementation for downloading SDK
    }

    viewSDKDocs() {
        // Implementation for viewing SDK docs
    }

    downloadJavaScriptSDK() {
        // Implementation for downloading JavaScript SDK
    }

    downloadPythonSDK() {
        // Implementation for downloading Python SDK
    }

    downloadPHPSDK() {
        // Implementation for downloading PHP SDK
    }

    generateCode() {
        // Implementation for generating code
    }

    setupAppShell() {
        // Implementation for app shell
    }

    implementOfflineCapabilities() {
        // Implementation for offline capabilities
    }

    installApp() {
        // Implementation for app installation
    }

    dismissInstallPrompt() {
        // Implementation for dismissing install prompt
    }

    hideInstallPrompt() {
        // Implementation for hiding install prompt
    }

    implementPlatformSpecificFeatures() {
        // Implementation for platform specific features
    }

    setupResponsiveDesign() {
        // Implementation for responsive design
    }

    applyIOSStyles() {
        // Implementation for iOS styles
    }

    applyAndroidStyles() {
        // Implementation for Android styles
    }

    setupRequestBatching() {
        // Implementation for request batching
    }

    setupDataCaching() {
        // Implementation for data caching
    }
}

// Initialize Mobile API Enhancement when DOM is loaded
let mobileAPI;
document.addEventListener('DOMContentLoaded', () => {
    mobileAPI = new MobileAPIEnhancement();
});

// Export for global access
window.mobileAPI = mobileAPI; 
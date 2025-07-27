/**
 * Enhanced UX Features for CRM System
 * Includes: Drag-and-drop, Real-time notifications, Progress indicators,
 * Keyboard shortcuts, Auto-save, Undo/redo, Contextual help, Onboarding wizard
 */

class EnhancedUX {
    constructor() {
        this.undoStack = [];
        this.redoStack = [];
        this.autoSaveInterval = null;
        this.notificationQueue = [];
        this.isProcessingNotifications = false;
        this.onboardingStep = 0;
        this.onboardingComplete = false;
        this.keyboardShortcuts = new Map();
        this.progressIndicators = new Map();
        
        this.init();
    }

    init() {
        this.initDragAndDrop();
        this.initNotifications();
        this.initKeyboardShortcuts();
        this.initAutoSave();
        this.initUndoRedo();
        this.initContextualHelp();
        this.initOnboarding();
        this.initProgressIndicators();
    }

    // ==================== DRAG AND DROP INTERFACE ====================
    initDragAndDrop() {
        // Make elements draggable
        document.addEventListener('DOMContentLoaded', () => {
            this.makeDraggable('.draggable');
            this.makeDroppable('.droppable');
        });
    }

    makeDraggable(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.setAttribute('draggable', 'true');
            element.addEventListener('dragstart', this.handleDragStart.bind(this));
            element.addEventListener('dragend', this.handleDragEnd.bind(this));
        });
    }

    makeDroppable(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.addEventListener('dragover', this.handleDragOver.bind(this));
            element.addEventListener('drop', this.handleDrop.bind(this));
            element.addEventListener('dragenter', this.handleDragEnter.bind(this));
            element.addEventListener('dragleave', this.handleDragLeave.bind(this));
        });
    }

    handleDragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.id);
        e.target.classList.add('dragging');
        this.showNotification('Drag started', 'info');
    }

    handleDragEnd(e) {
        e.target.classList.remove('dragging');
        this.showNotification('Drag ended', 'info');
    }

    handleDragOver(e) {
        e.preventDefault();
    }

    handleDragEnter(e) {
        e.preventDefault();
        e.target.classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.target.classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        e.target.classList.remove('drag-over');
        
        const draggedId = e.dataTransfer.getData('text/plain');
        const draggedElement = document.getElementById(draggedId);
        const dropZone = e.target.closest('.droppable');
        
        if (draggedElement && dropZone) {
            dropZone.appendChild(draggedElement);
            this.showNotification('Item dropped successfully', 'success');
            this.saveState();
        }
    }

    // ==================== REAL-TIME NOTIFICATIONS ====================
    initNotifications() {
        this.createNotificationContainer();
        this.startNotificationProcessor();
    }

    createNotificationContainer() {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'notification-container';
        document.body.appendChild(container);
    }

    showNotification(message, type = 'info', duration = 5000) {
        const notification = {
            id: Date.now(),
            message,
            type,
            duration,
            timestamp: new Date()
        };

        this.notificationQueue.push(notification);
        this.processNotificationQueue();
    }

    async processNotificationQueue() {
        if (this.isProcessingNotifications || this.notificationQueue.length === 0) {
            return;
        }

        this.isProcessingNotifications = true;

        while (this.notificationQueue.length > 0) {
            const notification = this.notificationQueue.shift();
            await this.displayNotification(notification);
            await this.sleep(300); // Delay between notifications
        }

        this.isProcessingNotifications = false;
    }

    async displayNotification(notification) {
        const container = document.getElementById('notification-container');
        const element = document.createElement('div');
        element.className = `notification notification-${notification.type}`;
        element.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${notification.message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="notification-progress"></div>
        `;

        container.appendChild(element);

        // Animate in
        element.style.transform = 'translateX(100%)';
        setTimeout(() => {
            element.style.transform = 'translateX(0)';
        }, 10);

        // Progress bar animation
        const progressBar = element.querySelector('.notification-progress');
        progressBar.style.width = '100%';
        progressBar.style.transition = `width ${notification.duration}ms linear`;

        // Auto remove
        setTimeout(() => {
            if (element.parentElement) {
                element.style.transform = 'translateX(100%)';
                setTimeout(() => element.remove(), 300);
            }
        }, notification.duration);
    }

    startNotificationProcessor() {
        setInterval(() => {
            this.processNotificationQueue();
        }, 1000);
    }

    // ==================== PROGRESS INDICATORS ====================
    initProgressIndicators() {
        // Global progress indicator
        this.createGlobalProgressIndicator();
    }

    createGlobalProgressIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'global-progress';
        indicator.className = 'global-progress';
        indicator.innerHTML = `
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
            <div class="progress-text">Loading...</div>
        `;
        document.body.appendChild(indicator);
    }

    showProgress(id, message = 'Processing...', percentage = 0) {
        const indicator = this.progressIndicators.get(id) || this.createProgressIndicator(id);
        indicator.message = message;
        indicator.percentage = percentage;
        this.updateProgressIndicator(indicator);
    }

    createProgressIndicator(id) {
        const indicator = {
            id,
            element: document.createElement('div'),
            message: 'Processing...',
            percentage: 0
        };

        indicator.element.className = 'progress-indicator';
        indicator.element.innerHTML = `
            <div class="progress-header">
                <span class="progress-title">${id}</span>
                <button class="progress-close" onclick="enhancedUX.hideProgress('${id}')">×</button>
            </div>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
            <div class="progress-text">Processing...</div>
        `;

        document.body.appendChild(indicator.element);
        this.progressIndicators.set(id, indicator);
        return indicator;
    }

    updateProgressIndicator(indicator) {
        const fill = indicator.element.querySelector('.progress-fill');
        const text = indicator.element.querySelector('.progress-text');
        
        fill.style.width = `${indicator.percentage}%`;
        text.textContent = indicator.message;
    }

    hideProgress(id) {
        const indicator = this.progressIndicators.get(id);
        if (indicator) {
            indicator.element.remove();
            this.progressIndicators.delete(id);
        }
    }

    // ==================== KEYBOARD SHORTCUTS ====================
    initKeyboardShortcuts() {
        this.registerDefaultShortcuts();
        document.addEventListener('keydown', this.handleKeyboardShortcut.bind(this));
    }

    registerDefaultShortcuts() {
        this.registerShortcut('ctrl+s', 'Save', () => this.autoSave());
        this.registerShortcut('ctrl+z', 'Undo', () => this.undo());
        this.registerShortcut('ctrl+y', 'Redo', () => this.redo());
        this.registerShortcut('ctrl+f', 'Search', () => this.focusSearch());
        this.registerShortcut('ctrl+n', 'New', () => this.createNew());
        this.registerShortcut('ctrl+h', 'Help', () => this.showHelp());
        this.registerShortcut('escape', 'Close', () => this.closeModals());
    }

    registerShortcut(key, description, action) {
        this.keyboardShortcuts.set(key, { description, action });
    }

    handleKeyboardShortcut(e) {
        const key = this.getKeyCombo(e);
        const shortcut = this.keyboardShortcuts.get(key);
        
        if (shortcut) {
            e.preventDefault();
            shortcut.action();
            this.showNotification(`Shortcut: ${shortcut.description}`, 'info', 2000);
        }
    }

    getKeyCombo(e) {
        const keys = [];
        if (e.ctrlKey) keys.push('ctrl');
        if (e.altKey) keys.push('alt');
        if (e.shiftKey) keys.push('shift');
        if (e.key !== 'Control' && e.key !== 'Alt' && e.key !== 'Shift') {
            keys.push(e.key.toLowerCase());
        }
        return keys.join('+');
    }

    // ==================== AUTO-SAVE FUNCTIONALITY ====================
    initAutoSave() {
        this.startAutoSave();
    }

    startAutoSave() {
        this.autoSaveInterval = setInterval(() => {
            this.autoSave();
        }, 30000); // Auto-save every 30 seconds
    }

    autoSave() {
        const forms = document.querySelectorAll('form[data-autosave]');
        forms.forEach(form => {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            // Save to localStorage
            const key = `autosave_${form.id || 'form'}`;
            localStorage.setItem(key, JSON.stringify({
                data,
                timestamp: Date.now()
            }));

            this.showNotification('Auto-saved', 'info', 2000);
        });
    }

    loadAutoSave(formId) {
        const key = `autosave_${formId}`;
        const saved = localStorage.getItem(key);
        
        if (saved) {
            const { data, timestamp } = JSON.parse(saved);
            const form = document.getElementById(formId);
            
            if (form) {
                Object.keys(data).forEach(key => {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input) input.value = data[key];
                });
                
                this.showNotification('Auto-saved data restored', 'info', 3000);
            }
        }
    }

    // ==================== UNDO/REDO SYSTEM ====================
    initUndoRedo() {
        this.maxUndoSteps = 50;
    }

    saveState() {
        const state = this.captureCurrentState();
        this.undoStack.push(state);
        
        // Limit undo stack size
        if (this.undoStack.length > this.maxUndoSteps) {
            this.undoStack.shift();
        }
        
        // Clear redo stack when new action is performed
        this.redoStack = [];
    }

    captureCurrentState() {
        const state = {
            timestamp: Date.now(),
            forms: {},
            selections: {},
            scrollPositions: {}
        };

        // Capture form data
        document.querySelectorAll('form').forEach(form => {
            const formData = new FormData(form);
            state.forms[form.id] = Object.fromEntries(formData);
        });

        // Capture selections
        if (window.getSelection) {
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
                state.selections = {
                    range: selection.getRangeAt(0).cloneContents().textContent
                };
            }
        }

        // Capture scroll positions
        state.scrollPositions = {
            window: { x: window.scrollX, y: window.scrollY }
        };

        return state;
    }

    undo() {
        if (this.undoStack.length === 0) {
            this.showNotification('Nothing to undo', 'warning');
            return;
        }

        const currentState = this.captureCurrentState();
        this.redoStack.push(currentState);

        const previousState = this.undoStack.pop();
        this.restoreState(previousState);
        
        this.showNotification('Undone', 'info', 2000);
    }

    redo() {
        if (this.redoStack.length === 0) {
            this.showNotification('Nothing to redo', 'warning');
            return;
        }

        const currentState = this.captureCurrentState();
        this.undoStack.push(currentState);

        const nextState = this.redoStack.pop();
        this.restoreState(nextState);
        
        this.showNotification('Redone', 'info', 2000);
    }

    restoreState(state) {
        // Restore form data
        Object.keys(state.forms).forEach(formId => {
            const form = document.getElementById(formId);
            if (form) {
                Object.keys(state.forms[formId]).forEach(fieldName => {
                    const input = form.querySelector(`[name="${fieldName}"]`);
                    if (input) input.value = state.forms[formId][fieldName];
                });
            }
        });

        // Restore scroll positions
        if (state.scrollPositions.window) {
            window.scrollTo(state.scrollPositions.window.x, state.scrollPositions.window.y);
        }
    }

    // ==================== CONTEXTUAL HELP ====================
    initContextualHelp() {
        this.createHelpOverlay();
        this.attachHelpTriggers();
    }

    createHelpOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'help-overlay';
        overlay.className = 'help-overlay';
        overlay.innerHTML = `
            <div class="help-content">
                <div class="help-header">
                    <h3>Contextual Help</h3>
                    <button class="help-close" onclick="enhancedUX.hideHelp()">×</button>
                </div>
                <div class="help-body"></div>
                <div class="help-footer">
                    <button class="help-prev">Previous</button>
                    <button class="help-next">Next</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    attachHelpTriggers() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('help-trigger')) {
                e.preventDefault();
                const helpData = e.target.dataset.help;
                this.showContextualHelp(helpData);
            }
        });
    }

    showContextualHelp(helpData) {
        const overlay = document.getElementById('help-overlay');
        const body = overlay.querySelector('.help-body');
        
        // Load help content based on context
        const helpContent = this.getHelpContent(helpData);
        body.innerHTML = helpContent;
        
        overlay.classList.add('active');
    }

    hideHelp() {
        const overlay = document.getElementById('help-overlay');
        overlay.classList.remove('active');
    }

    getHelpContent(context) {
        const helpData = {
            'lead-creation': `
                <h4>Creating a New Lead</h4>
                <p>Fill in the required fields to create a new lead:</p>
                <ul>
                    <li><strong>Name:</strong> Full name of the lead</li>
                    <li><strong>Email:</strong> Primary email address</li>
                    <li><strong>Phone:</strong> Contact phone number</li>
                    <li><strong>Company:</strong> Company name</li>
                    <li><strong>Source:</strong> How you found this lead</li>
                </ul>
                <p><strong>Tip:</strong> Use the auto-save feature (Ctrl+S) to save your progress.</p>
            `,
            'contact-management': `
                <h4>Managing Contacts</h4>
                <p>Use these features to manage your contacts effectively:</p>
                <ul>
                    <li><strong>Search:</strong> Use Ctrl+F to quickly search contacts</li>
                    <li><strong>Filter:</strong> Use advanced filters to find specific contacts</li>
                    <li><strong>Bulk Actions:</strong> Select multiple contacts for bulk operations</li>
                    <li><strong>Import/Export:</strong> Use CSV or Excel files for data management</li>
                </ul>
            `,
            'dashboard': `
                <h4>Dashboard Overview</h4>
                <p>Your dashboard provides key insights:</p>
                <ul>
                    <li><strong>KPIs:</strong> Key performance indicators at a glance</li>
                    <li><strong>Charts:</strong> Interactive charts for data visualization</li>
                    <li><strong>Recent Activity:</strong> Latest updates and activities</li>
                    <li><strong>Quick Actions:</strong> Fast access to common tasks</li>
                </ul>
            `
        };

        return helpData[context] || '<p>Help content not available for this context.</p>';
    }

    // ==================== ONBOARDING WIZARD ====================
    initOnboarding() {
        if (!this.onboardingComplete && !localStorage.getItem('onboarding_complete')) {
            this.startOnboarding();
        }
    }

    startOnboarding() {
        this.onboardingStep = 0;
        this.createOnboardingOverlay();
        this.showOnboardingStep();
    }

    createOnboardingOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'onboarding-overlay';
        overlay.className = 'onboarding-overlay';
        overlay.innerHTML = `
            <div class="onboarding-content">
                <div class="onboarding-header">
                    <h3>Welcome to CRM System</h3>
                    <button class="onboarding-skip" onclick="enhancedUX.skipOnboarding()">Skip</button>
                </div>
                <div class="onboarding-body"></div>
                <div class="onboarding-footer">
                    <button class="onboarding-prev" onclick="enhancedUX.prevOnboardingStep()">Previous</button>
                    <span class="onboarding-progress"></span>
                    <button class="onboarding-next" onclick="enhancedUX.nextOnboardingStep()">Next</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    showOnboardingStep() {
        const steps = [
            {
                title: 'Welcome to Your CRM',
                content: `
                    <p>Welcome to your new CRM system! This wizard will help you get started.</p>
                    <p>You'll learn about:</p>
                    <ul>
                        <li>Creating and managing leads</li>
                        <li>Tracking opportunities</li>
                        <li>Managing contacts and accounts</li>
                        <li>Using analytics and reports</li>
                    </ul>
                `
            },
            {
                title: 'Lead Management',
                content: `
                    <p>Start by creating your first lead:</p>
                    <ol>
                        <li>Click "New Lead" in the sidebar</li>
                        <li>Fill in the lead information</li>
                        <li>Use auto-save (Ctrl+S) to save progress</li>
                        <li>Assign the lead to a team member</li>
                    </ol>
                `
            },
            {
                title: 'Dashboard Overview',
                content: `
                    <p>Your dashboard shows key metrics:</p>
                    <ul>
                        <li><strong>Total Leads:</strong> Number of leads in your system</li>
                        <li><strong>Conversion Rate:</strong> Percentage of leads converted</li>
                        <li><strong>Revenue:</strong> Total revenue from opportunities</li>
                        <li><strong>Activities:</strong> Recent activities and tasks</li>
                    </ul>
                `
            },
            {
                title: 'Keyboard Shortcuts',
                content: `
                    <p>Use these keyboard shortcuts for faster navigation:</p>
                    <ul>
                        <li><strong>Ctrl+S:</strong> Save current form</li>
                        <li><strong>Ctrl+Z:</strong> Undo last action</li>
                        <li><strong>Ctrl+Y:</strong> Redo last action</li>
                        <li><strong>Ctrl+F:</strong> Search</li>
                        <li><strong>Ctrl+H:</strong> Show help</li>
                    </ul>
                `
            },
            {
                title: 'You\'re All Set!',
                content: `
                    <p>Congratulations! You're ready to start using your CRM system.</p>
                    <p>Remember:</p>
                    <ul>
                        <li>Use the help system (?) for contextual assistance</li>
                        <li>Enable notifications for real-time updates</li>
                        <li>Use drag-and-drop for easy organization</li>
                        <li>Explore advanced features as you become comfortable</li>
                    </ul>
                `
            }
        ];

        const currentStep = steps[this.onboardingStep];
        const overlay = document.getElementById('onboarding-overlay');
        const body = overlay.querySelector('.onboarding-body');
        const progress = overlay.querySelector('.onboarding-progress');
        const prevBtn = overlay.querySelector('.onboarding-prev');
        const nextBtn = overlay.querySelector('.onboarding-next');

        body.innerHTML = `
            <h4>${currentStep.title}</h4>
            ${currentStep.content}
        `;

        progress.textContent = `${this.onboardingStep + 1} of ${steps.length}`;
        prevBtn.style.display = this.onboardingStep === 0 ? 'none' : 'block';
        nextBtn.textContent = this.onboardingStep === steps.length - 1 ? 'Finish' : 'Next';

        overlay.classList.add('active');
    }

    nextOnboardingStep() {
        const steps = 5; // Total number of steps
        if (this.onboardingStep < steps - 1) {
            this.onboardingStep++;
            this.showOnboardingStep();
        } else {
            this.completeOnboarding();
        }
    }

    prevOnboardingStep() {
        if (this.onboardingStep > 0) {
            this.onboardingStep--;
            this.showOnboardingStep();
        }
    }

    skipOnboarding() {
        this.completeOnboarding();
    }

    completeOnboarding() {
        const overlay = document.getElementById('onboarding-overlay');
        overlay.classList.remove('active');
        this.onboardingComplete = true;
        localStorage.setItem('onboarding_complete', 'true');
        this.showNotification('Onboarding completed! Welcome to your CRM system.', 'success', 5000);
    }

    // ==================== UTILITY FUNCTIONS ====================
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    focusSearch() {
        const searchInput = document.querySelector('input[type="search"], .search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }

    createNew() {
        const newButtons = document.querySelectorAll('.btn-new, .new-button');
        if (newButtons.length > 0) {
            newButtons[0].click();
        }
    }

    showHelp() {
        this.showContextualHelp('general');
    }

    closeModals() {
        const modals = document.querySelectorAll('.modal, .overlay');
        modals.forEach(modal => {
            if (modal.classList.contains('active')) {
                modal.classList.remove('active');
            }
        });
    }
}

// Initialize Enhanced UX when DOM is loaded
let enhancedUX;
document.addEventListener('DOMContentLoaded', () => {
    enhancedUX = new EnhancedUX();
});

// Export for global access
window.enhancedUX = enhancedUX; 
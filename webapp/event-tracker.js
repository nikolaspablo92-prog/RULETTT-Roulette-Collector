/**
 * 📊 RULETTT Frontend Event Tracker
 * Отслеживание всех действий пользователя, ошибок JS, performance metrics
 */

class RoulettEventTracker {
    constructor(options = {}) {
        this.options = {
            apiEndpoint: options.apiEndpoint || '/api/events',
            maxQueueSize: options.maxQueueSize || 100,
            flushInterval: options.flushInterval || 5000, // 5 seconds
            captureClicks: options.captureClicks !== false,
            captureNavigation: options.captureNavigation !== false,
            captureErrors: options.captureErrors !== false,
            capturePerformance: options.capturePerformance !== false,
            captureNetwork: options.captureNetwork !== false,
            userId: options.userId || 'anonymous',
            sessionId: options.sessionId || this.generateSessionId(),
            debug: options.debug || false
        };
        
        this.eventQueue = [];
        this.userActions = [];
        this.maxUserActions = 50;
        this.startTime = Date.now();
        
        this.init();
    }
    
    init() {
        if (this.options.debug) {
            console.log('🔍 RULETTT Event Tracker initialized', this.options);
        }
        
        // Автоматическая отправка событий
        this.flushTimer = setInterval(() => this.flush(), this.options.flushInterval);
        
        // Отправка при закрытии страницы
        window.addEventListener('beforeunload', () => this.flush(true));
        
        // Отслеживание различных событий
        if (this.options.captureClicks) this.captureClicks();
        if (this.options.captureNavigation) this.captureNavigation();
        if (this.options.captureErrors) this.captureErrors();
        if (this.options.capturePerformance) this.capturePerformance();
        if (this.options.captureNetwork) this.captureNetwork();
        
        // Отслеживание видимости страницы
        document.addEventListener('visibilitychange', () => {
            this.trackEvent('page_visibility', {
                state: document.hidden ? 'hidden' : 'visible'
            });
        });
        
        // Начальное событие
        this.trackEvent('tracker_initialized', {
            url: window.location.href,
            referrer: document.referrer,
            screen: {
                width: window.screen.width,
                height: window.screen.height
            },
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            userAgent: navigator.userAgent
        });
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    trackEvent(eventType, details = {}, level = 'info') {
        const event = {
            type: eventType,
            timestamp: new Date().toISOString(),
            sessionId: this.options.sessionId,
            userId: this.options.userId,
            level: level,
            details: details,
            page: {
                url: window.location.href,
                pathname: window.location.pathname,
                title: document.title
            },
            performance: {
                timeOnPage: Date.now() - this.startTime,
                memory: performance.memory ? {
                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                    totalJSHeapSize: performance.memory.totalJSHeapSize
                } : null
            }
        };
        
        this.eventQueue.push(event);
        
        // Добавляем в историю действий пользователя
        this.userActions.push({
            type: eventType,
            timestamp: event.timestamp,
            details: details
        });
        
        // Ограничиваем размер истории
        if (this.userActions.length > this.maxUserActions) {
            this.userActions.shift();
        }
        
        if (this.options.debug) {
            console.log('📝 Event tracked:', eventType, details);
        }
        
        // Отправляем сразу если очередь переполнена
        if (this.eventQueue.length >= this.options.maxQueueSize) {
            this.flush();
        }
        
        return event;
    }
    
    captureClicks() {
        document.addEventListener('click', (e) => {
            const target = e.target;
            const tagName = target.tagName.toLowerCase();
            
            const details = {
                element: tagName,
                id: target.id || null,
                className: target.className || null,
                text: target.textContent?.substring(0, 50) || null,
                x: e.clientX,
                y: e.clientY
            };
            
            // Специальная обработка для кнопок и ссылок
            if (tagName === 'button' || tagName === 'a') {
                details.href = target.href || null;
                details.action = target.getAttribute('data-action') || null;
            }
            
            this.trackEvent('click', details);
        }, true);
    }
    
    captureNavigation() {
        // History API
        const originalPushState = history.pushState;
        const originalReplaceState = history.replaceState;
        const self = this;
        
        history.pushState = function(...args) {
            originalPushState.apply(this, args);
            self.trackEvent('navigation', {
                type: 'pushState',
                url: window.location.href
            });
        };
        
        history.replaceState = function(...args) {
            originalReplaceState.apply(this, args);
            self.trackEvent('navigation', {
                type: 'replaceState',
                url: window.location.href
            });
        };
        
        // Browser back/forward
        window.addEventListener('popstate', () => {
            this.trackEvent('navigation', {
                type: 'popstate',
                url: window.location.href
            });
        });
        
        // Hash changes
        window.addEventListener('hashchange', () => {
            this.trackEvent('navigation', {
                type: 'hashchange',
                hash: window.location.hash
            });
        });
    }
    
    captureErrors() {
        // JavaScript errors
        window.addEventListener('error', (e) => {
            this.trackEvent('js_error', {
                message: e.message,
                filename: e.filename,
                lineno: e.lineno,
                colno: e.colno,
                stack: e.error?.stack || null,
                userActions: this.userActions.slice(-10) // Последние 10 действий
            }, 'error');
            
            // Отправляем немедленно
            this.flush();
        });
        
        // Unhandled promise rejections
        window.addEventListener('unhandledrejection', (e) => {
            this.trackEvent('promise_rejection', {
                reason: e.reason?.toString() || 'Unknown',
                promise: e.promise?.toString() || null,
                userActions: this.userActions.slice(-10)
            }, 'error');
            
            this.flush();
        });
        
        // Console errors (monkey patch)
        const originalError = console.error;
        const self = this;
        console.error = function(...args) {
            originalError.apply(console, args);
            self.trackEvent('console_error', {
                message: args.map(a => String(a)).join(' ')
            }, 'error');
        };
    }
    
    capturePerformance() {
        // Page load performance
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    this.trackEvent('page_load_performance', {
                        loadTime: perfData.loadEventEnd - perfData.fetchStart,
                        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.fetchStart,
                        domInteractive: perfData.domInteractive - perfData.fetchStart,
                        redirectTime: perfData.redirectEnd - perfData.redirectStart,
                        dnsTime: perfData.domainLookupEnd - perfData.domainLookupStart,
                        tcpTime: perfData.connectEnd - perfData.connectStart,
                        requestTime: perfData.responseEnd - perfData.requestStart,
                        responseTime: perfData.responseEnd - perfData.responseStart
                    });
                }
                
                // Resource timing
                const resources = performance.getEntriesByType('resource');
                const slowResources = resources
                    .filter(r => r.duration > 1000) // Медленнее 1 секунды
                    .map(r => ({
                        name: r.name,
                        duration: r.duration,
                        type: r.initiatorType
                    }));
                
                if (slowResources.length > 0) {
                    this.trackEvent('slow_resources', {
                        resources: slowResources
                    }, 'warning');
                }
            }, 0);
        });
        
        // Long tasks (если доступно)
        if ('PerformanceObserver' in window) {
            try {
                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.duration > 50) { // Длинные задачи > 50ms
                            this.trackEvent('long_task', {
                                duration: entry.duration,
                                startTime: entry.startTime
                            }, 'warning');
                        }
                    }
                });
                observer.observe({ entryTypes: ['longtask'] });
            } catch (e) {
                // Long tasks API не поддерживается
            }
        }
    }
    
    captureNetwork() {
        // Monkey patch fetch
        const originalFetch = window.fetch;
        const self = this;
        
        window.fetch = async function(...args) {
            const startTime = performance.now();
            const url = args[0];
            
            try {
                const response = await originalFetch.apply(this, args);
                const duration = performance.now() - startTime;
                
                self.trackEvent('network_request', {
                    url: typeof url === 'string' ? url : url.url,
                    method: args[1]?.method || 'GET',
                    status: response.status,
                    duration: duration,
                    ok: response.ok
                });
                
                return response;
            } catch (error) {
                const duration = performance.now() - startTime;
                
                self.trackEvent('network_error', {
                    url: typeof url === 'string' ? url : url.url,
                    method: args[1]?.method || 'GET',
                    duration: duration,
                    error: error.message
                }, 'error');
                
                throw error;
            }
        };
        
        // Monkey patch XMLHttpRequest
        const originalXHROpen = XMLHttpRequest.prototype.open;
        const originalXHRSend = XMLHttpRequest.prototype.send;
        
        XMLHttpRequest.prototype.open = function(method, url, ...rest) {
            this._requestStart = performance.now();
            this._method = method;
            this._url = url;
            return originalXHROpen.apply(this, [method, url, ...rest]);
        };
        
        XMLHttpRequest.prototype.send = function(...args) {
            this.addEventListener('load', function() {
                const duration = performance.now() - this._requestStart;
                self.trackEvent('xhr_request', {
                    url: this._url,
                    method: this._method,
                    status: this.status,
                    duration: duration
                });
            });
            
            this.addEventListener('error', function() {
                const duration = performance.now() - this._requestStart;
                self.trackEvent('xhr_error', {
                    url: this._url,
                    method: this._method,
                    duration: duration
                }, 'error');
            });
            
            return originalXHRSend.apply(this, args);
        };
    }
    
    trackButtonClick(buttonId, additionalData = {}) {
        this.trackEvent('button_click', {
            buttonId: buttonId,
            ...additionalData
        });
    }
    
    trackFormSubmit(formId, formData = {}) {
        this.trackEvent('form_submit', {
            formId: formId,
            fields: Object.keys(formData)
        });
    }
    
    trackCustomEvent(eventName, data = {}) {
        this.trackEvent(eventName, data);
    }
    
    async flush(sync = false) {
        if (this.eventQueue.length === 0) return;
        
        const events = [...this.eventQueue];
        this.eventQueue = [];
        
        if (this.options.debug) {
            console.log(`📤 Flushing ${events.length} events to server`);
        }
        
        try {
            if (sync && navigator.sendBeacon) {
                // Используем sendBeacon для синхронной отправки при закрытии страницы
                const blob = new Blob([JSON.stringify(events)], { type: 'application/json' });
                navigator.sendBeacon(this.options.apiEndpoint, blob);
            } else {
                // Обычная отправка
                await fetch(this.options.apiEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ events: events })
                });
            }
            
            if (this.options.debug) {
                console.log('✅ Events sent successfully');
            }
        } catch (error) {
            console.error('❌ Failed to send events:', error);
            // Возвращаем события обратно в очередь
            this.eventQueue.unshift(...events);
        }
    }
    
    getUserActions(count = 20) {
        return this.userActions.slice(-count);
    }
    
    getErrorContext() {
        return {
            userActions: this.getUserActions(),
            sessionId: this.options.sessionId,
            userId: this.options.userId,
            url: window.location.href,
            timeOnPage: Date.now() - this.startTime
        };
    }
    
    destroy() {
        clearInterval(this.flushTimer);
        this.flush(true);
    }
}

// Автоматическая инициализация глобального трекера
if (typeof window !== 'undefined') {
    window.roulettTracker = new RoulettEventTracker({
        debug: window.location.hostname === 'localhost',
        userId: localStorage.getItem('userId') || 'anonymous',
        sessionId: sessionStorage.getItem('sessionId') || undefined
    });
    
    // Сохраняем sessionId
    if (!sessionStorage.getItem('sessionId')) {
        sessionStorage.setItem('sessionId', window.roulettTracker.options.sessionId);
    }
    
    console.log('🔍 RULETTT Event Tracker активирован');
}

// Export для использования в модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RoulettEventTracker;
}

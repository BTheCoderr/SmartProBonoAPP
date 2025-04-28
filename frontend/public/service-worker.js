const VERSION = '1.0.0';
const CACHE_NAME = `smartprobono-v${VERSION}`;

const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/static/js/main.*.js',
  '/static/js/bundle.*.js',
  '/static/css/main.*.css',
  '/manifest.json',
  '/favicon.ico',
  '/logo192.png',
  '/logo512.png'
];

const API_CACHE_NAME = `smartprobono-api-v${VERSION}`;
const API_ROUTES = [
  '/api/users/profile',
  '/api/cases',
  '/api/notifications',
  '/api/resources',
  '/api/templates'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log(`[ServiceWorker] Caching static assets for version ${VERSION}`);
        return cache.addAll(STATIC_ASSETS.map(path => 
          path.includes('*') ? 
            new Request(path.replace('*', '')) : 
            path
        ));
      })
      .catch(error => {
        console.error('[ServiceWorker] Error caching static assets:', error);
      })
  );
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(cacheName => {
              return (cacheName.startsWith('smartprobono-') && 
                     !cacheName.includes(VERSION));
            })
            .map(cacheName => {
              console.log(`[ServiceWorker] Deleting old cache: ${cacheName}`);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log(`[ServiceWorker] Version ${VERSION} activated and handling fetches`);
      })
  );
  self.clients.claim();
});

// Fetch event - serve from cache, then network
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Handle API requests
  if (API_ROUTES.some(route => url.pathname.startsWith(route))) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response.ok) {
            const clonedResponse = response.clone();
            caches.open(API_CACHE_NAME)
              .then(cache => cache.put(event.request, clonedResponse))
              .catch(err => console.error('[ServiceWorker] Error caching API response:', err));
          }
          return response;
        })
        .catch(() => {
          return caches.match(event.request)
            .then(cachedResponse => {
              if (cachedResponse) {
                return cachedResponse;
              }
              throw new Error('No cached response available');
            });
        })
    );
    return;
  }

  // Handle navigation requests
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          return caches.match('/offline.html')
            .then(response => response || new Response('Offline page not found'));
        })
    );
    return;
  }

  // Handle static assets and other requests
  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }
        
        return fetch(event.request)
          .then(response => {
            if (response.ok && !url.pathname.startsWith('/api/')) {
              const clonedResponse = response.clone();
              caches.open(CACHE_NAME)
                .then(cache => cache.put(event.request, clonedResponse))
                .catch(err => console.error('[ServiceWorker] Error caching response:', err));
            }
            return response;
          })
          .catch(error => {
            console.error('[ServiceWorker] Fetch error:', error);
            throw error;
          });
      })
  );
});

// Handle push notifications
self.addEventListener('push', event => {
  try {
    const data = event.data.json();
    
    const options = {
      body: data.body || 'New notification from SmartProBono',
      icon: '/logo192.png',
      badge: '/logo192.png',
      vibrate: [100, 50, 100],
      data: {
        dateOfArrival: Date.now(),
        primaryKey: data.id || 1,
        url: data.url || '/'
      },
      actions: [
        {
          action: 'open',
          title: 'View Details'
        },
        {
          action: 'close',
          title: 'Dismiss'
        }
      ]
    };

    event.waitUntil(
      self.registration.showNotification(data.title || 'SmartProBono', options)
    );
  } catch (error) {
    console.error('[ServiceWorker] Push event error:', error);
  }
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'open') {
    const urlToOpen = event.notification.data?.url || '/';
    
    event.waitUntil(
      clients.matchAll({
        type: 'window',
        includeUncontrolled: true
      })
      .then(windowClients => {
        // If a window client is available, focus it
        for (const client of windowClients) {
          if (client.url === urlToOpen && 'focus' in client) {
            return client.focus();
          }
        }
        // If no window client is available, open a new window
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
    );
  }
}); 
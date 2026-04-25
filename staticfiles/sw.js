// Service Worker para Censo Web PWA
// Versión: 1.0.0
// Cache Strategy: Network First con Fallback a Cache

const CACHE_VERSION = 'censo-v1.0.0';
const CACHE_STATIC = `${CACHE_VERSION}-static`;
const CACHE_DYNAMIC = `${CACHE_VERSION}-dynamic`;
const CACHE_IMAGES = `${CACHE_VERSION}-images`;

// Recursos estáticos críticos para caché inicial
const STATIC_ASSETS = [
  '/',
  '/static/assets/css/nucleo-icons.css',
  '/static/assets/css/nucleo-svg.css',
  '/static/assets/js/core/popper.min.js',
  '/static/assets/js/core/bootstrap.min.js',
  '/static/assets/js/plugins/perfect-scrollbar.min.js',
  '/static/assets/js/soft-ui-dashboard.min.js',
  'https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js',
];

// URLs que SIEMPRE deben ir a la red (no cachear)
const NETWORK_ONLY_URLS = [
  '/admin/',
  '/api/',
  '/logout/',
  '/accounts/logout/',
];

// ==============================================
// INSTALL EVENT - Caché inicial
// ==============================================
self.addEventListener('install', event => {
  console.log('[SW] Installing Service Worker...', CACHE_VERSION);

  event.waitUntil(
    caches.open(CACHE_STATIC)
      .then(cache => {
        console.log('[SW] Precaching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .catch(err => {
        console.warn('[SW] Precache failed for some assets:', err);
      })
  );

  // Activar inmediatamente
  self.skipWaiting();
});

// ==============================================
// ACTIVATE EVENT - Limpiar cachés antiguas
// ==============================================
self.addEventListener('activate', event => {
  console.log('[SW] Activating Service Worker...', CACHE_VERSION);

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName.startsWith('censo-') && cacheName !== CACHE_STATIC &&
              cacheName !== CACHE_DYNAMIC && cacheName !== CACHE_IMAGES) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );

  // Tomar control inmediatamente
  return self.clients.claim();
});

// ==============================================
// FETCH EVENT - Estrategias de caché
// ==============================================
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Ignorar requests no HTTP/HTTPS
  if (!request.url.startsWith('http')) {
    return;
  }

  // Network Only para URLs específicas
  if (NETWORK_ONLY_URLS.some(path => url.pathname.startsWith(path))) {
    return; // Dejar pasar sin interceptar
  }

  // POST, PUT, DELETE siempre a la red
  if (request.method !== 'GET') {
    event.respondWith(
      fetch(request).catch(() => {
        return new Response(
          JSON.stringify({
            error: 'Sin conexión',
            offline: true,
            message: 'Esta operación requiere conexión a internet'
          }),
          {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
          }
        );
      })
    );
    return;
  }

  // Estrategia según tipo de recurso
  if (request.destination === 'image') {
    event.respondWith(cacheFirst(request, CACHE_IMAGES));
  } else if (url.pathname.startsWith('/static/')) {
    event.respondWith(cacheFirst(request, CACHE_STATIC));
  } else {
    event.respondWith(networkFirst(request, CACHE_DYNAMIC));
  }
});

// ==============================================
// ESTRATEGIA: Cache First (Estáticos)
// ==============================================
async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);

  if (cachedResponse) {
    // Retornar del caché y actualizar en background
    updateCache(request, cacheName);
    return cachedResponse;
  }

  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('[SW] Fetch failed for:', request.url);
    return offlineFallback(request);
  }
}

// ==============================================
// ESTRATEGIA: Network First (HTML, API)
// ==============================================
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed, trying cache for:', request.url);

    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    return offlineFallback(request);
  }
}

// ==============================================
// ACTUALIZAR CACHÉ EN BACKGROUND
// ==============================================
async function updateCache(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse);
    }
  } catch (error) {
    // Silencioso - no es crítico
  }
}

// ==============================================
// FALLBACK OFFLINE
// ==============================================
function offlineFallback(request) {
  if (request.destination === 'document') {
    return caches.match('/').then(response => {
      return response || new Response(
        '<h1>Sin Conexión</h1><p>Por favor verifica tu conexión a internet.</p>',
        { headers: { 'Content-Type': 'text/html' } }
      );
    });
  }

  if (request.destination === 'image') {
    return new Response(
      '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="#ccc"/></svg>',
      { headers: { 'Content-Type': 'image/svg+xml' } }
    );
  }

  return new Response('Offline', { status: 503 });
}

// ==============================================
// BACKGROUND SYNC - Sincronización Diferida
// ==============================================
self.addEventListener('sync', event => {
  console.log('[SW] Background sync:', event.tag);

  if (event.tag === 'sync-data') {
    event.waitUntil(syncPendingData());
  }
});

async function syncPendingData() {
  console.log('[SW] Syncing pending data...');

  // Aquí iría la lógica para sincronizar datos pendientes
  // Por ejemplo, formularios guardados localmente

  try {
    const pendingData = await getStoredPendingData();

    for (const data of pendingData) {
      await fetch(data.url, {
        method: data.method,
        headers: data.headers,
        body: data.body
      });
    }

    await clearPendingData();
    console.log('[SW] Sync completed');
  } catch (error) {
    console.error('[SW] Sync failed:', error);
    throw error; // Re-intentará automáticamente
  }
}

async function getStoredPendingData() {
  // Implementar según necesidad
  return [];
}

async function clearPendingData() {
  // Implementar según necesidad
}

// ==============================================
// PUSH NOTIFICATIONS
// ==============================================
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'Nueva notificación de Censo Web',
    icon: '/static/pwa/icon-192x192.png',
    badge: '/static/pwa/icon-72x72.png',
    vibrate: [200, 100, 200],
    tag: 'censo-notification',
    requireInteraction: false
  };

  event.waitUntil(
    self.registration.showNotification('Censo Web', options)
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();

  event.waitUntil(
    clients.openWindow('/')
  );
});

// ==============================================
// MENSAJES DESDE EL CLIENTE
// ==============================================
self.addEventListener('message', event => {
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }

  if (event.data.action === 'clearCache') {
    event.waitUntil(
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => caches.delete(cacheName))
        );
      })
    );
  }
});

console.log('[SW] Service Worker loaded', CACHE_VERSION);

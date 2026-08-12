// عوافي · afiyah — offline app-shell cache
const CACHE = 'afiyah-v3';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './apple-touch-icon.png',
  './icon-192.png',
  './icon-512.png',
  './logo.png',
  './sound-on.png',
  './sound-off.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      // cache assets individually so one failure doesn't abort the whole install
      .then((c) => Promise.all(ASSETS.map((a) => c.add(a).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function cacheable(req, res) {
  if (!res || res.status !== 200) return false;               // never cache errors/partials
  const url = new URL(req.url);
  return url.origin === location.origin || url.host.includes('gstatic') || url.host.includes('googleapis');
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  // The HTML document is network-first (fresh when online, cached copy offline).
  const isDoc = req.mode === 'navigate' || req.destination === 'document';
  if (isDoc) {
    e.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put('./index.html', copy)).catch(() => {});
          }
          return res;
        })
        .catch(() => caches.match('./index.html').then((c) => c || caches.match('./')))
    );
    return;
  }

  // Everything else: stale-while-revalidate. Serve a good cached copy fast,
  // refresh it in the background, and only ever cache successful (200) responses.
  e.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req)
        .then((res) => {
          if (cacheable(req, res)) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          }
          return res;
        })
        .catch(() => cached);
      // only trust a cached response that actually succeeded
      return (cached && (cached.ok || cached.status === 0)) ? cached : network;
    })
  );
});

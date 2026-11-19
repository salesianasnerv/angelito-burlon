/* Service worker de la web del Angelito Burlón.
   Sube el número de VERSION cada vez que cambies la web, para que los móviles descarguen lo nuevo. */
const VERSION = 'angelito-v2';
const BASICO = ['./', 'index.html', 'manifest.webmanifest', 'favicon.ico', 'icons/icon-192.png', 'icons/icon-512.png',
  'img/logos/nervion-blanco.png', 'img/logos/nervion-color.png', 'img/escenas/escena00-1600.webp', 'img/escenas/escena00-800.webp',
  'img/personaje/angelito-vuela.webp', 'img/personaje/angelito-yo.webp', 'img/personaje/angelito-pie.webp', 'img/personaje/angelito-risa.webp'];

self.addEventListener('install', e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(BASICO)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.headers.has('range') || req.destination === 'video') return; // los vídeos van directos (streaming)
  if (req.mode === 'navigate') { // la página: primero la red, si no hay conexión la copia guardada
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(VERSION).then(k => k.put('index.html', c)); return r; })
      .catch(() => caches.match('index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
    if (r.ok) { const c = r.clone(); caches.open(VERSION).then(k => k.put(req, c)); }
    return r;
  })));
});

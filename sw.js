// Offline support: keep every app file on the device. Bump VERSION when files change.
const VERSION = "family-bee-v5";
const FILES = ["./", "index.html", "manifest.webmanifest", "fonts/fredoka.woff2", "fonts/nunito.woff2",
  "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const isPage = e.request.mode === "navigate";
  if (isPage) {
    // Try the network first so updates arrive, fall back to the saved copy offline.
    e.respondWith(fetch(e.request).then(r => {
      const copy = r.clone(); caches.open(VERSION).then(c => c.put("index.html", copy)); return r;
    }).catch(() => caches.match("index.html")));
    return;
  }
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request)));
});

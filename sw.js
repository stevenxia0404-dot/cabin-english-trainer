/* 公务英语AI陪练 · Service Worker
 * 缓存名 SW_CACHE 必须与 index.html 中的常量保持一致。
 *
 * 缓存策略：
 *  - 安装时预缓存 shell（index.html / data.js / manifest.json / icons/*.png），
 *    让首屏在离线时也能打开。
 *  - 音频（/audio/*）：cache-first + content-type 防护。
 *    内容哈希命名，跨版本稳定；首次播放/预载即写入缓存，离线可听。
 *  - 其它（html / js / manifest / icons）：network-first，离线回退缓存。
 *    关键：data.js 必须每次在线都取最新，否则会出现「index.html 内联清单是新版、
 *    data.js 却是旧版」的错配。所以这些资源不走 cache-first。
 *  - 不自动 skipWaiting：新版本由页面弹「点此刷新」，用户确认后才接管，
 *    避免学员练到一半被静默换版。
 */
const SW_CACHE = 'speakeasy-sw-v6';
const SHELL = [
  './',
  './index.html',
  './data.js',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-512-maskable.png',
  './icons/apple-touch-icon-180.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(SW_CACHE).then(c => c.addAll(SHELL)).catch(() => {})
  );
  // 注意：此处不调用 skipWaiting()，更新由页面提示用户确认
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== SW_CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isAudio = url.pathname.indexOf('/audio/') === 0;

  if (isAudio) {
    // 音频：cache-first，命中即返回；未命中则取网络并写入缓存
    event.respondWith(
      caches.match(req).then(cached => {
        if (cached) return cached;
        return fetch(req).then(res => {
          // 防护：CloudStudio 的 SPA fallback 对未知路径返回 text/html，
          // 绝不能把 HTML 当 mp3 缓存进去（否则离线时音频变白屏）
          const ct = res.headers.get('content-type') || '';
          if (res.ok && !ct.includes('text/html')) {
            const copy = res.clone();
            caches.open(SW_CACHE).then(c => c.put(req, copy)).catch(() => {});
          }
          return res;
        });
      })
    );
    return;
  }

  // 其余资源：network-first，离线时回退缓存（首屏可开）
  event.respondWith(
    fetch(req).then(res => {
      const copy = res.clone();
      caches.open(SW_CACHE).then(c => c.put(req, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
  );
});

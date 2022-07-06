// const cacheName = 'news-v1';
// const staticAssets = [
//   './',
//   'C:/Users/Fahad Mustafa/Desktop/ProjextLogistic/projectX/truckService/templates/login.html',
  
// ];

// self.addEventListener('install', async e => {
//   const cache = await caches.open(cacheName);
//   await cache.addAll(staticAssets);
//   return self.skipWaiting();
// });

// self.addEventListener('activate', e => {
//   self.clients.claim();
// });

// self.addEventListener('fetch', async e => {
//   const req = e.request;
//   const url = new URL(req.url);

//   if (url.origin === location.origin) {
//     e.respondWith(cacheFirst(req));
//   } else {
//     e.respondWith(networkAndCache(req));
//   }
// });

// async function cacheFirst(req) {
//   const cache = await caches.open(cacheName);
//   const cached = await cache.match(req);
//   return cached || fetch(req);
// }

// async function networkAndCache(req) {
//   const cache = await caches.open(cacheName);
//   try {
//     const fresh = await fetch(req);
//     await cache.put(req, fresh.clone());
//     return fresh;
//   } catch (e) {
//     const cached = await cache.match(req);
//     return cached;
//   }
// }

// // var staticCacheName = 'djangopwa-v1';

// // self.addEventListener('install', function(event) {
// // event.waitUntil(
// // 	caches.open(staticCacheName).then(function(cache) {
// // 	return cache.addAll([
// // 		'',
// // 	]);
// // 	})
// // );
// // });

// // self.addEventListener('fetch', function(event) {
// // var requestUrl = new URL(event.request.url);
// // 	if (requestUrl.origin === location.origin) {
// // 	if ((requestUrl.pathname === '/')) {
// // 		event.respondWith(caches.match(''));
// // 		return;
// // 	}
// // 	}
// // 	event.respondWith(
// // 	caches.match(event.request).then(function(response) {
// // 		return response || fetch(event.request);
// // 	})
// // 	);
// // });


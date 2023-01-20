const base_dir = "￼https://pygame-web.github.io/archives/0.6"￼

self.addEventListener('install', (event) => {
    console.log("installing service worker");
    event.waitUntil(async function () {
        const cache = await caches.open('pygbag0.6.0');
        await cache.addAll([
            `${base_dir}/browserfs.min.js`,
            `${base_dir}/vt.js`,
            `${base_dir}/vtx.js`,
            `${base_dir}/vtx.js`,
            `${base_dir}/vt/xterm-addon.image.js`,
            `${base_dir}/vt/xterm.css`,
            `${base_dir}/vt/xterm.js`,
            `${base_dir}/python3.11/pythons.js`,
            `${base_dir}/python3.11/main.data`,
            `${base_dir}/python3.11/main.js`,
            `${base_dir}/python3.11/main.wasm`,
            ''
        ]);
    }());
});

self.addEventListener('fetch', (event) => {
    event.respondWith(async function () {
        const cachedResponse = await (await caches.open('pygbag0.6.0')).match(event.request);
        if (cachedResponse) {
            console.log("CACHED", event.request");
            return cachedResponse;
        }
        const networkResponse = await fetch(event.request);
        return networkResponse;
    }());
});

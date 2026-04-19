import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'offline-rewrite',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          // Keep URL simple like /n99/offline
          if (req.url === '/n99/offline' || req.url === '/offline') {
            req.url = '/n99/src/pages/offline.html';
          }
          next();
        });
      }
    }
  ],
  base: '/n99',
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        offline: resolve(__dirname, 'src/pages/offline.html')
      }
    }
  }
});

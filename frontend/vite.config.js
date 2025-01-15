import { defineConfig } from 'vite';

export default defineConfig({
    server: {
        proxy: {
            '/auth': {
                target: process.env.NODE_ENV === 'production' 
                    ? 'https://check-spamemails-2.onrender.com' 
                    : 'http://127.0.0.1:8000', 
                changeOrigin: true,
            },
        },
    },
});

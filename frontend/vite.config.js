import { defineConfig } from 'vite';

export default defineConfig({
    base: '/',
    server: {
        proxy: {
            '/auth': {
                target:'https://check-spamemails-2.onrender.com' , 
                   
                changeOrigin: true,
            },
        },
    },
});
